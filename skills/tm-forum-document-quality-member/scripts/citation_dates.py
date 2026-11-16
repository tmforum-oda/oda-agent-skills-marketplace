"""Find the publication date of each source a document credits, and which
credited source is core to the document. The script doesn't search the
web itself: a date read from a credited source opened during the web check
goes in references/citation-dates.json, and the script picks it up.

Sources are grouped as in credit_check.py (cited.txt, written by
extract_docx.py). For each one the date comes from the first of:

  stated     a date in the credit itself: the source line, the
             reference-list line in text.txt that a marker such as "[29]" in
             the source line points to, a /2023/ path in the link, or an
             arXiv identifier (2506.12469 is June 2025).
             Years after "accessed", "retrieved" or "viewed" are skipped.
  held       the first date on the front pages of a held source (--sources)
             whose file name carries a document number the credit names
             (RFC 6749 -> rfc6749.txt "October 2012"; 3GPP and ETSI
             "V19.5.0 (2025-09)").
  lookup     references/citation-dates.json, document numbers or links with a
             known date and where that date came from.
  not found  none of these.

Age is in years from the publication date to --as-of (default today).

Core citation: the outside source the document leans on most. Credited
passages count first, then mentions in text.txt of the document numbers the
credit names. TM Forum's own sources (a TM Forum link or a TMF, TMFC, GB,
IG or TR number; also example.com and yaml.org) are left out, and so is a
bare marker with no reference-list entry ("[0]" from "schemes[0]") or a
link with no host. --core names it instead: a source line as printed, or
the name of a work the document rests on without a credit cited.txt picks
up (it is added as a row with 0 passages and dated the same way).

Writes citations.json to the output folder and prints the table.

Usage:
  python -I citation_dates.py <output-dir> [--sources <dir>] [--as-of YYYY-MM-DD] [--core <source>]
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import copy_check  # noqa: E402  (same folder; -I doesn't add it to sys.path)
import credit_check  # noqa: E402
import dependence  # noqa: E402
from triage import TM_HOSTS  # noqa: E402

LOOKUP = os.path.join(HERE, "..", "references", "citation-dates.json")

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
MONTH = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|" \
        r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
YEAR = r"(?:19[5-9]\d|20[0-4]\d)"
ISO_DATE = re.compile(r"(?<!\d)(%s)-(0[1-9]|1[0-2])(?:-(?:0[1-9]|[12]\d|3[01]))?(?!\d)" % YEAR)
MONTH_DATE = re.compile(r"\b(?:\d{1,2}(?:st|nd|rd|th)?\s+)?(%s)\.?,?\s+(?:\d{1,2}(?:st|nd|rd|th)?,?\s+)?(%s)\b"
                        % (MONTH, YEAR), re.I)
BARE_YEAR = re.compile(r"(?<![\w.-])(%s)(?![\w-]|\.\d)" % YEAR)
# A year straight after a document number's prefix is part of the number ("RFC 2023", "ISO 2001").
NOT_A_YEAR = re.compile(r"(?:RFC|TS|TR|GS|GR|ISO|IEC|IEEE|MEF|ITU-T|IG|GB|TMF|TMFC|Release|Rel\.?|Version|v)\s*$",
                        re.I)
ACCESSED = re.compile(r"(?:accessed|retrieved|viewed|visited)(?:\s+on)?:?\s*$", re.I)
REF_ENTRY = re.compile(r"^\s*\[\s*(\d{1,3})\s*\]")
MARKER = re.compile(r"\[\s*(\d{1,3})\s*\]")
NO_HOST = re.compile(r"^https?://[^.\s]*$", re.I)
URL_OR_WORDS = re.compile(r"https?://|www\.|[A-Za-z]{3,}")
RFC_LINK = re.compile(r"/rfc(\d{3,5})\b", re.I)  # ietf.org/rfc/rfc6749.txt, tools.ietf.org/html/rfc7519
# ETSI work items written without "GS" and a space ("NFV IFA011", "ZSM002"), which dependence.DOC_ID misses.
ETSI_ITEM = re.compile(r"\b(?:NFV[- ]?)?(?:IFA|SOL|ZSM|MEC|ENI|EVE|TST|SEC)[- ]?\d{3}\b")
# TM Forum's own documents named as the source ("Source: TR315", "IG1228"). "TR-069" (with a hyphen) is
# Broadband Forum's, so a TR number counts only without one.
TMF_DOC = re.compile(r"\b(?:TMFC?|GB|IG)\s?\d{3,4}|\bTR\s?\d{3}\b")
# "http://Forum.org": a tmforum.org link cut short when the text was extracted.
TMF_CUT = re.compile(r"^https?://(?:www\.)?forum\.org/?$", re.I)
# arXiv identifiers start with the year and month of submission: arxiv.org/abs/2506.12469 is June 2025.
ARXIV = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{2})(0[1-9]|1[0-2])\.\d{4,5}", re.I)


def find_date(text):
    """First publication date in text, as ("YYYY-MM" or "YYYY", year as a float), or None."""
    best, months = None, {}
    for rx, kind in ((ISO_DATE, "iso"), (MONTH_DATE, "month"), (BARE_YEAR, "year")):
        for m in rx.finditer(text):
            before = text[max(0, m.start() - 25):m.start()]
            if ACCESSED.search(before) or (kind == "year" and NOT_A_YEAR.search(before)):
                continue
            if kind == "iso":
                y, mo = int(m.group(1)), int(m.group(2))
            elif kind == "month":
                y, mo = int(m.group(2)), MONTHS.index(m.group(1)[:3].lower()) + 1
            else:
                y, mo = int(m.group(1)), None
            if mo:
                months.setdefault(y, mo)
            if best is None or m.start() < best[0]:
                best = (m.start(), y, mo)
            break
    if best is None:
        return None
    _, y, mo = best
    # "ISO/IEC 14764:2022 ... Jan 2022": the year comes first, but the month given later for that year is better.
    mo = mo or months.get(y)
    return ("%d-%02d" % (y, mo), y + (mo - 0.5) / 12) if mo else ("%d" % y, y + 0.5)


def norm_id(i):
    return re.sub(r"[\s._-]", "", i.lower())


def held_files(sources):
    files = []
    for root, _, names in os.walk(sources or ""):
        files += [os.path.join(root, n) for n in names]
    return files


def held_date(ids, files):
    """Date from the front pages of a held source named by one of the credit's document numbers."""
    for i in ids:
        r = re.sub(r"^(?:3gpp|etsi)?(?:ts|tr|gs|gr|en|es)?", "", norm_id(i))
        if len(r) < 4:
            continue
        for path in files:
            if r in norm_id(os.path.splitext(os.path.basename(path))[0]):
                try:
                    text = copy_check.read_text(path)
                except Exception:  # an unreadable held file just gives no date
                    text = None
                found = find_date(text[:6000]) if text else None
                if found:
                    return found, os.path.basename(path)
    return None, None


def load_lookup():
    if not os.path.isfile(LOOKUP):
        graceful.warn("references/citation-dates.json not found: publication dates come only from the "
                      "credits and held sources.")
        return {}
    with open(LOOKUP, encoding="utf-8") as f:
        return {norm_id(k): v for k, v in json.load(f).get("dates", {}).items()}


def lookup_date(ids, source, table):
    for key in [source] + sorted(ids):
        e = table.get(norm_id(key))
        if e:
            found = find_date(e["date"])
            if found:
                return found, e.get("basis", "")
    return None, None


def reference_lines(text):
    """Reference-list entries in text.txt by number: "[12] RFC3198 Terminology ..." -> {"12": line}."""
    refs = {}
    for line in text.splitlines():
        m = REF_ENTRY.match(line)
        if m and len(line.split()) >= 2:
            refs.setdefault(m.group(1), line.strip())
    return refs


def citations(outdir, sources=None, as_of=None, core=None):
    as_of = as_of or datetime.date.today()
    now = as_of.year + (as_of.timetuple().tm_yday - 0.5) / 365.25
    with open(os.path.join(outdir, "text.txt"), encoding="utf-8", errors="replace") as f:
        text = f.read()
    flat = re.sub(r"\s+", "", text.lower())
    refs = reference_lines(text)
    files = held_files(sources)
    table = load_lookup()

    def row(source, passages):
        # Only the credit itself: the passages under one source can carry other entries' numbers, because some
        # documents keep stale marker links pointing at another entry's address.
        markers = MARKER.findall(source)
        credit = " ".join([source] + [refs[n] for n in markers if n in refs])
        # A bare marker with no reference-list entry ("[0]" from "schemes[0]") or a link with no host
        # ("https://`") names no work.
        stray = (bool(markers) and not any(n in refs and n != "0" for n in markers)
                 and not URL_OR_WORDS.search(MARKER.sub("", source).replace("citation marker", ""))) \
            or bool(NO_HOST.match(source))
        ids = dependence.doc_ids(credit) | {"RFC " + n for n in RFC_LINK.findall(credit)} \
            | {m.group() for m in ETSI_ITEM.finditer(credit)}
        found, how, basis = find_date(credit), "stated", ""
        arxiv = ARXIV.search(credit)
        if not found and arxiv:
            y, mo = 2000 + int(arxiv.group(1)), int(arxiv.group(2))
            found = ("%d-%02d" % (y, mo), y + (mo - 0.5) / 12)
        if not found:
            found, basis = held_date(ids, files)
            how = "held"
        if not found:
            found, basis = lookup_date(ids, source, table)
            how = "lookup"
        return {
            "source": source, "passages": passages, "ids": sorted(ids),
            # A bare marker ("citation marker [78]") is shown by the reference-list entry it points to.
            "label": credit[len(source):].strip() if markers and credit != source and not URL_OR_WORDS.search(
                MARKER.sub("", source).replace("citation marker", "")) else source,
            "mentions": sum(flat.count(norm_id(i)) for i in ids),
            "tm_forum": bool(TM_HOSTS.search(credit) or TMF_DOC.search(credit) or TMF_CUT.match(source)),
            "stray": stray,
            "published": found[0] if found else None,
            "age": round(max(0.0, now - found[1]), 1) if found else None,
            "how": how if found else "not found", "basis": basis or "",
        }

    rows = [row(source, len(passages))
            for source, passages in credit_check.read_cited(os.path.join(outdir, "cited.txt")).items()]
    outside = [r for r in rows if not r["tm_forum"] and not r["stray"]]
    if core:
        pick = next((r for r in rows if r["source"] == core), None)
        if pick is None:
            # A work the document rests on but credits nowhere cited.txt sees (its declared base, say).
            pick = row(core, 0)
            rows.append(pick)
    else:
        pick = max(outside, key=lambda r: (r["passages"], r["mentions"]), default=None)
    for r in rows:
        r["core"] = r is pick
    result = {"as_of": as_of.isoformat(), "core_chosen_by": "named" if core else "most passages, then mentions",
              "citations": rows}
    with open(os.path.join(outdir, "citations.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1)
    return result


def published_cell(r):
    if not r["published"]:
        return "not found"
    how = {"stated": "stated in credit", "held": "held source %s" % r["basis"],
           "lookup": "lookup%s" % (": " + r["basis"] if r["basis"] else "")}[r["how"]]
    return "%s (%s)" % (r["published"], how)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("--sources")
    ap.add_argument("--as-of", type=datetime.date.fromisoformat)
    ap.add_argument("--core")
    a = ap.parse_args()
    a.sources = graceful.sources(a.sources)
    sys.stdout.reconfigure(encoding="utf-8")
    res = citations(a.outdir, a.sources, a.as_of, a.core)
    rows = res["citations"]
    print("### Citation dates (age as of %s)\n" % res["as_of"])
    if not rows:
        print("No credited passages in cited.txt.\n")
        return
    print("| Source credited | Passages | Mentions | Published | Age (years) | Core |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        print("| %s | %d | %d | %s | %s | %s |" % (
            r["source"][:90].replace("|", "/"), r["passages"], r["mentions"], published_cell(r),
            "%.1f" % r["age"] if r["age"] is not None else "-", "**core**" if r["core"] else ""))
    core = next((r for r in rows if r["core"]), None)
    print("\nCore citation (%s): %s" % (res["core_chosen_by"], core["source"] if core else "none outside TM Forum"))
    print("Dated: %d of %d sources.\n" % (sum(1 for r in rows if r["published"]), len(rows)))


if __name__ == "__main__":
    main()
