"""Check, from the extracted text alone, how complete each credit in a
document is. No web search is used.

For every passage the document credits to an outside source (cited.txt,
written by extract_docx.py), and every image that has a credit or source
note next to it (images.txt), it looks for the four parts of a credit that
Creative Commons recommends (TASL), plus a fifth this skill adds:

  Title     the credit names the work, not just a site or a body
  Author    a person or organisation is named as the author, or there is
            "et al." or an author-year citation
  Source    a link to where the work can be found
  Licence   a licence or copyright statement (CC BY, Apache, MIT, (c),
            "all rights reserved", "licence")
  Date      the credit itself gives the work's publication date (a date
            found only from a held copy or the citation-dates list doesn't
            count: the reader of the document can't see it)

Passages are grouped by source, so each source is judged once. A credit is
  complete           all five parts
  complete, no date  Title, Author, Source and Licence, but no date
  partial            one to four parts otherwise
  none               none of the five (for example a bare domain or marker)
In the ownership score these are worth 1.0, 0.75, 0.5 and 0: a missing
date costs a quarter, the other parts a half.

It reports what the credit contains. It can't tell whether the credit
points at the right work, or whether the text really comes from there:
that needs the source opened (see spot_check_candidates.py). A credit in
a caption or surrounding text that extract_docx.py didn't put in cited.txt
shows up only in the image table below.

Each source also gets its publication date and age, and the core citation
(the outside source the document leans on most) is marked; see
citation_dates.py for how both are found. Pass --sources to date credits
from held sources' front pages.

For images it also notes the ones whose credit names a TM Forum
deliverable (TM Forum, TMF/GB/IG/TR numbers, SID, eTOM). Those are TM
Forum's own material or a contributing Member's own, and don't need
looking at for outside origin. A mention of ODA or TM Forum that is not a
credit doesn't count.

Usage:
  python -I credit_check.py <output-dir> [--sources <dir>] [--as-of YYYY-MM-DD] [--core <source>]
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # for citation_dates; -I doesn't add it

URL = re.compile(r"https?://|www\.|\b[a-z0-9-]+\.(?:com|org|io|net|dev|int|eu|edu|github\.io)\b", re.I)
LICENCE = re.compile(r"licen[cs]e|CC[- ]BY|creative commons|apache|\bMIT\b|©|\(c\)|copyright|all rights reserved|"
                     r"terms of use", re.I)
AUTHOR = re.compile(r"\bby\s+[A-Z][a-z]+|\b[A-Z][a-z]+,\s*[A-Z]\.|et al\.?|\(\d{4}\)|\b(?:19|20)\d{2}\b")
TMF = r"(?:tm\s?forum|tmforum|\b(?:TMF|GB|IG|TR)\s?-?\d{3,4}|\bSID\b|eTOM)"
TMF_CREDIT = re.compile(r"(?:source|from|credit|©|copyright|adapted|reproduced|see|ref)[^\n]{0,60}" + TMF + "|"
                        + TMF + r"[^\n]{0,60}(?:source|©|copyright)", re.I)
IMAGE_CUE = re.compile(r"source\s*:|\(source|credit|courtesy|©|copyright|adapted from|reproduced from|"
                       r"figure from|image from|https?://|www\.|\[\d+\]|\bRFC ?\d+|"
                       r"\b(?:3GPP|ETSI|IETF|OASIS|W3C|ITU|IEEE|ISO(?:/IEC)?)\b", re.I)


def grade(credit, dated=None):
    """Grade a credit on Title, Author, Source, Licence and Date. dated: whether the credit states a date, when
    citation_dates.py has already looked (it also reads the reference-list entry a marker points to)."""
    import citation_dates  # noqa: E402  (imports this module, so not at the top)
    c = credit.strip()
    if c.endswith(": no source named"):  # extract_xlsx.py: a cell in a "Source" column that names no source
        return "none", dict.fromkeys(("Title", "Author", "Source", "Licence", "Date"), False)
    parts = {
        "Title": len(re.sub(r"https?://\S+", "", c).split()) >= 3,
        "Author": bool(AUTHOR.search(c)),
        "Source": bool(URL.search(c)),
        "Licence": bool(LICENCE.search(c)),
        "Date": bool(citation_dates.find_date(c)) if dated is None else dated,
    }
    n = sum(parts.values())
    if n == len(parts):
        return "complete", parts
    if n == len(parts) - 1 and not parts["Date"]:
        return "complete, no date", parts
    return ("none" if n == 0 else "partial"), parts


def read_cited(path):
    groups = {}
    if os.path.isfile(path):
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if " | " in line:
                    source, passage = line.rstrip("\n").split(" | ", 1)
                    groups.setdefault(source.strip(), []).append(passage)
    return groups


def read_images(path):
    images, cur = {}, None
    if os.path.isfile(path):
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("== "):
                    cur = line[3:].strip()
                    images[cur] = []
                elif cur and line.strip():
                    images[cur].append(line.strip())
    return images


def classify_images(images):
    """Split images.txt entries into (credited to TM Forum, other credit or source note, nothing nearby)."""
    credited, tmf, plain = [], [], []
    for name, ctx in images.items():
        # One line at a time: a credit on one line says nothing about the figure on the next.
        if any(TMF_CREDIT.search(l) for l in ctx):
            tmf.append(name)
            continue
        hit = next((l for l in ctx if IMAGE_CUE.search(l)), None)
        if hit:
            credited.append((name, hit))
        else:
            plain.append(name)
    return tmf, credited, plain


def yn(v):
    return "yes" if v else "no"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("--sources")
    ap.add_argument("--as-of", type=datetime.date.fromisoformat)
    ap.add_argument("--core")
    a = ap.parse_args()
    a.sources = graceful.sources(a.sources)
    sys.stdout.reconfigure(encoding="utf-8")

    groups = read_cited(os.path.join(a.outdir, "cited.txt"))
    images = read_images(os.path.join(a.outdir, "images.txt"))
    total = sum(len(v) for v in groups.values())

    print("### Credit check (from the extracted text, no web search)\n")
    if groups:
        import citation_dates  # noqa: E402  (imports this module, so not at the top)
        dated = citation_dates.citations(a.outdir, a.sources, a.as_of, a.core)
        by_source = {r["source"]: r for r in dated["citations"]}
        print("%d credited passages from %d sources. Ages are as of %s.\n" % (total, len(groups), dated["as_of"]))
        print("| Source credited | Passages | Title | Author | Source link | Licence | Date | Credit | Published "
              "| Age (years) |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        tally = {"complete": 0, "complete, no date": 0, "partial": 0, "none": 0}
        for source, passages in groups.items():
            r = by_source[source]
            g, p = grade(source, dated=r["how"] == "stated")
            tally[g] += len(passages)
            print("| %s%s | %d | %s | %s | %s | %s | %s | **%s** | %s | %s |" % (
                r["label"][:90].replace("|", "/"), " (**core**)" if r["core"] else "", len(passages), yn(p["Title"]),
                yn(p["Author"]), yn(p["Source"]), yn(p["Licence"]), yn(p["Date"]), g,
                citation_dates.published_cell(r), "%.1f" % r["age"] if r["age"] is not None else "-"))
        print("\nBy passage: %d complete, %d complete with no date, %d partial, %d none.\n" % (
            tally["complete"], tally["complete, no date"], tally["partial"], tally["none"]))
        core = next((r for r in dated["citations"] if r["core"]), None)
        print("Core citation (%s): %s.\n" % (dated["core_chosen_by"], (
            "%s, published %s, %s years old" % (core["label"], core["published"], "%.1f" % core["age"])
            if core and core["published"] else "%s, publication date not found" % core["label"] if core
            else "none outside TM Forum")))
    else:
        print("No credited passages in cited.txt.\n")

    if images:
        tmf, credited, plain = classify_images(images)
        print("Images listed in images.txt: %d. With a credit to a TM Forum deliverable (not looked at for outside "
              "origin): %d. With another credit or source note: %d. With none: %d.\n"
              % (len(images), len(tmf), len(credited), len(plain)))
        if credited:
            print("| Image | Credit or source note nearby | Title | Author | Source link | Licence | Date | Credit |")
            print("|---|---|---|---|---|---|---|---|")
            for name, text in credited:
                cue = IMAGE_CUE.search(text)
                note = text[max(0, cue.start() - 20):cue.start() + 120].replace("|", "/")
                g, p = grade(note)
                print("| %s | %s | %s | %s | %s | %s | %s | **%s** |" % (
                    name, note, yn(p["Title"]), yn(p["Author"]), yn(p["Source"]), yn(p["Licence"]), yn(p["Date"]),
                    g))
            print()
        if tmf:
            print("Credited to TM Forum: " + ", ".join(tmf) + "\n")
        if plain:
            print("No credit nearby (look at these, flagged ones one by one and the rest on contact sheets): "
                  + ", ".join(plain) + "\n")
    print("This reports what each credit contains. It doesn't show that a credit is to the right work or that "
          "the credited text really comes from it.\n")


if __name__ == "__main__":
    main()
