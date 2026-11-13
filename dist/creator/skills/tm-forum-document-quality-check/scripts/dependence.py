"""Measure how much a document depends on outside standards bodies and sources.

Two kinds of dependence, measured separately:

  By reference (always): how often the document sends the reader to another
  body's documents to understand it.
    - SDO mentions per 1,000 words, by body, and the top body's share
      (concentration).
    - Pointers per 1,000 words: "as defined in", "see", "according to",
      "specified in" ... followed within a few words by a body or a
      document identifier. This is the stand-alone test.
    - Distinct outside document identifiers (3GPP TS 28.531, MEF 55,
      RFC 8299, ...).
    - Declared base: bodies the document says it builds on ("based on",
      "extends", "expands on", "aligned with" ... near a body's name) in
      its title or first 15% of text, plus any given with --declared-base.

  By copying (only with --sources): the copied-text matches from
  copy_check.py, sorted by the source's role:
    base        a source whose file name names a declared-base body
    cited       a source the document names (its identifier or file name
                appears in the text)
    undeclared  any other source
    TM Forum (expected)  a file named like a TM Forum document (IG..., GB..., TR..., TMF...)
  For each source: matched words, share of the document, longest run, and
  share of normative text (sentences with shall / must / should / may not /
  required). Then the document's original share (text matching no outside
  source; TM Forum matches still count as original) and its original share
  of normative text.

The pointer rate is classed against references/dependence-reference.json,
separately for documents with and without a declared base, because a
document that says it expands on another body's work is expected to point
to it:
  heavy   rate > mean + k*sigma of its group, and at least min_heavy_pointers pointers
  light   rate < mean - k*sigma; for a group listed in pointer_light_at_zero
          (documents without a declared base), a rate of 0: no pointers at all
  typical in between

With --sources, the copied words per 1,000 words (the share matching an outside
source, times 1,000) are classed by the fixed rule copied_class_rule in the
reference file (light below 1, heavy above 20, typical in between), for
documents that cite a held source only.
TM Forum's §14.1 notice, adapted from the ISOC statement in older RFCs, is
masked out first using references/TMF-IPR-Policy-v6.md.

Usage:
  python -I dependence.py <output-dir> [--sources <dir>] [--declared-base 3GPP,ETSI]
         [--n 8] [--min-words 12]
  python -I dependence.py --reference          (print the reference table)

<output-dir> is the folder written by extract_docx.py (text.txt is used).
Prints a Markdown report.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import copy_check  # noqa: E402  (same folder; -I doesn't add it to sys.path)

REFERENCE = os.path.join(HERE, "..", "references", "dependence-reference.json")
IPR_POLICY = os.path.join(HERE, "..", "references", "TMF-IPR-Policy-v6.md")

# Standards bodies and open-source foundations a TM Forum document may lean on.
# Name -> pattern (case-sensitive, so "mef" or "bbf" in ordinary words don't match).
BODIES = {
    "3GPP": r"3GPP",
    "ETSI": r"ETSI",
    "MEF": r"MEF",
    "IETF": r"IETF|RFC ?\d{3,5}",
    "ITU-T": r"ITU(?:-T)?",
    "O-RAN": r"O-RAN",
    "ONAP": r"ONAP",
    "GSMA": r"GSMA",
    "NGMN": r"NGMN",
    "BBF": r"BBF|Broadband Forum",
    "IEEE": r"IEEE",
    "ISO/IEC": r"ISO(?:/IEC)?(?= ?\d)|ISO/IEC",
    "W3C": r"W3C",
    "OASIS": r"OASIS",
    "CNCF": r"CNCF",
    "Linux Foundation": r"Linux Foundation|LF Networking",
    "NIST": r"NIST",
    "CAMARA": r"CAMARA",
    "OpenID Foundation": r"OpenID",
}
BODY = {k: re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z])" % v) for k, v in BODIES.items()}
ANY_BODY = re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z])" % "|".join(BODIES.values()))

# Outside document identifiers, spelled the many ways documents write them:
# "3GPP TS 28.531", "TS28.541", "3GPP 28531", "ETSI TS123 501", "ETSI GS ZSM 002",
# "MEF 55.1", "RFC 8299", "ITU-T Y.3172", "IEEE 802.1Q", "TR-069", "ISO/IEC 27001".
DOC_ID = re.compile(
    r"\b(?:(?:3GPP|ETSI)\s*)?(?:TS|TR|GS|GR|EN|ES)\s*[A-Z]{0,4}\s*\d{2,3}[ .]?\d{3}(?:-\d+)?"
    r"|\b3GPP\s+\d{5}\b"
    r"|\bETSI\s+(?:GS|GR)\s+[A-Z]{2,4}(?:-[A-Z]+)?\s+\d{3}"
    r"|\bMEF\s*\d{2,3}(?:\.\d+)*"
    r"|\bRFC\s*\d{3,5}"
    r"|\bITU-T\s+[A-Z]\.\d{2,4}(?:\.\d+)?"
    r"|(?<![/\w])IEEE\s+\d{3,4}(?!\d)(?:\.\d+[A-Za-z]*)?"
    r"|\bTR-\d{3}"
    r"|\bISO(?:/IEC)?(?:/IEEE)?\s+\d{4,5}(?!\d)(?:-\d+)?")

POINTER = re.compile(r"\b(?:as (?:defined|specified|described|per)|defined (?:in|by)|specified (?:in|by)"
                     r"|described in|according to|in accordance with|refer(?:s|red)? to|see|per|"
                     r"compliant with|conform(?:s|ing)? to|based on)\b", re.I)
POINTER_REACH = 10  # words after the pointer phrase in which a body or identifier must appear

DECLARE = re.compile(r"\b(?:based on|build(?:s|ing)? (?:on|upon)|extend(?:s|ing)?|expand(?:s|ing)? (?:on|upon)"
                     r"|elaborat(?:es|ing) on|align(?:s|ed)? with|derived from|complement(?:s|ing)?"
                     r"|bridg(?:e|es|ing)|adopt(?:s|ing)?|profile(?:s)? of|reuse(?:s)?"
                     r"|map(?:s|ped|ping)? (?:to|onto)|realiz(?:es|ed|ation of))\b", re.I)
DECLARE_REACH = 0.15  # share of the document, from the start, treated as title, scope and introduction

# Contents and figure-list lines ("6.1.2.OAuth flow RFC6749 Fig 1 ...22", "Figure 51 ETSI ZSM ...28")
# repeat headings and captions, so they would count every mention twice.
# A section number needs a full stop ("6.1.2." or "6."), so "3GPP TS 28.312" in a table cell isn't read as a
# contents line ending in a page number.
CONTENTS_LINE = re.compile(r"^(?:\d+(?:\.\d+)+\.?|\d+\.|Figure\s*\d+|Table\s*\d+)\s*\S.{0,200}?\D\d{1,3}$")

MIN_BASE_MENTIONS = 5  # fewer body mentions than this are too few to suggest an undeclared base
TMF_SOURCE = re.compile(r"^(?:IG|GB|TR|TMF|TMFC)\d", re.I)  # TM Forum's own documents as sources

NORMATIVE = re.compile(r"\b(?:shall|must|should|may not|required|mandatory)\b", re.I)
SENTENCE = re.compile(r"(?<=[.!?])\s+|\n")


def words_in(text):
    return len(text.split())


def bodies_in(text):
    return [k for k, rx in BODY.items() if rx.search(text)]


def doc_ids(text):
    return {" ".join(m.group().split()) for m in DOC_ID.finditer(text)}


def declared_bases(text):
    """Bodies the opening of the document says it builds on, with the sentence that says so."""
    cut = text[:max(1, int(len(text) * DECLARE_REACH))]
    found = {}
    for s in SENTENCE.split(cut):
        if DECLARE.search(s):
            for b in bodies_in(s):
                found.setdefault(b, " ".join(s.split())[:240])
    return found


def pointers(text):
    """Pointer phrases followed within POINTER_REACH words by a body or document identifier."""
    hits = []
    for m in POINTER.finditer(text):
        after = " ".join(text[m.end():m.end() + 400].split()[:POINTER_REACH])
        if ANY_BODY.search(after) or doc_ids(after):
            hits.append(bodies_in(after) or ["(identifier)"])
    return hits


def reference_measures(text):
    words = words_in(text)
    mentions = {k: len(rx.findall(text)) for k, rx in BODY.items()}
    mentions = {k: v for k, v in mentions.items() if v}
    total = sum(mentions.values())
    ptr = pointers(text)
    return {
        "words": words,
        "mentions": mentions,
        "mention_rate": total / words * 1e3 if words else 0,
        "concentration": max(mentions.values()) / total if total else 0,
        "top_body": max(mentions, key=mentions.get) if mentions else None,
        "pointers": len(ptr),
        "pointer_rate": len(ptr) / words * 1e3 if words else 0,
        "doc_ids": sorted(doc_ids(text)),
        "declared": declared_bases(text),
    }


def copy_measures(text, sources, declared, n, min_words):
    """Per-source matched words, longest run and normative share, by role."""
    dwords, doffs = copy_check.tokens(text)
    # Mark each draft word that sits in a normative sentence.
    spans, pos = [], 0
    for s in SENTENCE.split(text):
        start = text.find(s, pos)
        pos = start + len(s)
        if s and NORMATIVE.search(s):
            spans.append((start, pos))
    normative, j = [False] * len(dwords), 0
    for i, (a, _) in enumerate(doffs):
        while j < len(spans) and spans[j][1] <= a:
            j += 1
        normative[i] = j < len(spans) and spans[j][0] <= a
    index = {}
    for i in range(len(dwords) - n + 1):
        index.setdefault(tuple(dwords[i:i + n]), []).append(i)
    lower_text = text.lower()
    # Identifiers reduced to the part a file name carries: "3GPP TS 28.312" -> "28312",
    # "ETSI GS ZSM 002" -> "zsm002", "RFC 6749" -> "rfc6749".
    ids = {re.sub(r"^(?:3gpp|etsi)?(?:ts|tr|gs|gr|en|es)?", "", re.sub(r"[\s._-]", "", i.lower()))
           for i in doc_ids(text)}

    def stretches(stext, mask):
        """Draft words in stretches of min_words or more shared with stext, ignoring
        masked words; and the longest stretch."""
        swords, _ = copy_check.tokens(stext)
        hit = [False] * len(dwords)
        for j in range(len(swords) - n + 1):
            for i in index.get(tuple(swords[j:j + n]), ()):
                for k in range(i, i + n):
                    hit[k] = not mask[k]
        matched, longest, i = [False] * len(dwords), 0, 0
        while i < len(dwords):
            if not hit[i]:
                i += 1
                continue
            start = i
            while i < len(dwords) and hit[i]:
                i += 1
            if i - start >= min_words:
                longest = max(longest, i - start)
                for k in range(start, i):
                    matched[k] = True
        return matched, longest

    # TM Forum's §14.1 notice is adapted from the ISOC copyright statement in older
    # RFCs, so every TM Forum document matches them; mask the notice out first.
    with open(IPR_POLICY, encoding="utf-8") as f:
        notice, _ = stretches(f.read(), [False] * len(dwords))

    any_hit = [False] * len(dwords)
    rows, skipped = [], []
    for root, _, files in os.walk(sources):
        for name in sorted(files):
            path = os.path.join(root, name)
            stext = copy_check.read_text(path)
            if stext is None:
                skipped.append(os.path.relpath(path, sources))
                continue
            matched, longest = stretches(stext, notice)
            m = sum(matched)
            if not m:
                continue
            rel = os.path.relpath(path, sources)
            stem = os.path.splitext(os.path.basename(name))[0]
            if TMF_SOURCE.match(name):
                role = "TM Forum (expected)"
            elif any(re.search(re.escape(b), rel, re.I) for b in declared):
                role = "base"
            elif stem.lower() in lower_text or any(len(i) >= 5 and i in re.sub(r"[\s._-]", "", stem.lower())
                                                   for i in ids):
                role = "cited"
            else:
                role = "undeclared"
            if role != "TM Forum (expected)":  # TM Forum's own text still counts as original
                for k in range(len(dwords)):
                    any_hit[k] = any_hit[k] or matched[k]
            rows.append({"source": rel, "role": role, "words": m, "longest": longest,
                         "normative": sum(1 for k in range(len(dwords)) if matched[k] and normative[k])})
    total, norm_total = len(dwords), sum(normative)
    return {
        "rows": sorted(rows, key=lambda r: -r["words"]),
        "skipped": skipped,
        "words": total,
        "normative_words": norm_total,
        "original": 1 - sum(any_hit) / total if total else 1,
        "original_normative": (1 - sum(1 for k in range(total) if any_hit[k] and normative[k]) / norm_total)
        if norm_total else None,
    }


def load_reference():
    with open(REFERENCE, encoding="utf-8") as f:
        ref = json.load(f)
    groups = {}
    for d in ref["documents"]:
        groups.setdefault("declared" if d["declared_base"] else "none", []).append(d["pointer_rate"])
    stats = {g: (statistics.mean(v), statistics.pstdev(v)) for g, v in groups.items() if len(v) >= 2}
    # Copied share is classed only against documents whose cited sources were held.
    copied = [d["copied_per_1000"] for d in ref["documents"] if d.get("cites_held_source")]
    if len(copied) >= 2:
        stats["copied"] = (statistics.mean(copied), statistics.pstdev(copied))
    return ref, stats


def classify(rate, count, group, ref, stats):
    """Most documents without a declared base have no pointers at all, so one or
    two in a short document would read as heavy; heavy also needs min_heavy_pointers."""
    m, sd = stats[group]
    k = ref["sigma_multiplier"]
    z = (rate - m) / sd if sd else 0
    if rate > m + k * sd and count >= ref["min_heavy_pointers"]:
        cls = "heavy"
    elif group in ref.get("pointer_light_at_zero", []):
        # mean - k*sigma is below zero for this group (most of its documents have no pointers), so light
        # would be impossible: light is no pointers at all
        cls = "light" if count == 0 else "typical"
    else:
        cls = "light" if rate < m - k * sd else "typical"
    return z, cls


def copy_class(share, ref):
    """Copied words per 1,000, by the fixed rule: mean - k*sigma was below zero, so light was impossible."""
    rule = ref["copied_class_rule"]
    return "heavy" if share > rule["heavy_above"] else "light" if share < rule["light_below"] else "typical"


def held_names(sources):
    names = []
    for _, _, files in os.walk(sources or ""):
        names += [re.sub(r"[\s._-]", "", os.path.splitext(f)[0].lower()) for f in files]
    return names


def cites_held(ids, held):
    """Whether the document names a document number found in a held source's file name."""
    for i in ids:
        r = re.sub(r"^(?:3gpp|etsi)?(?:ts|tr|gs|gr|en|es)?", "", re.sub(r"[\s._-]", "", i.lower()))
        if len(r) >= 5 and any(r in h for h in held):
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir", nargs="?")
    ap.add_argument("--sources")
    ap.add_argument("--declared-base", default="", help="comma-separated bodies the document builds on")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--min-words", type=int, default=12)
    ap.add_argument("--cites-held", action="store_true",
                    help="the document cites a held source in a way the identifiers miss (as TR255's 'NFV IFA011')")
    ap.add_argument("--reference", action="store_true")
    ap.add_argument("--json", action="store_true", help="print the measures as JSON (for building the reference set)")
    a = ap.parse_args()
    sources_given = a.sources
    a.sources = graceful.sources(a.sources)
    sys.stdout.reconfigure(encoding="utf-8")

    ref = stats = None
    if os.path.exists(REFERENCE):
        ref, stats = load_reference()
    if a.reference:
        if not ref:
            sys.exit("No reference set yet: %s" % REFERENCE)
        k = ref["sigma_multiplier"]
        for g, label in (("declared", "With a declared base"), ("none", "Without a declared base")):
            if g in stats:
                m, sd = stats[g]
                light = "no pointers" if g in ref.get("pointer_light_at_zero", []) else "< %.2f" % (m - k * sd)
                print("%s: pointer rate mean %.2f, sigma %.2f, k %.1f -> light %s, heavy > %.2f"
                      % (label, m, sd, k, light, m + k * sd))
        for d in sorted(ref["documents"], key=lambda d: d["pointer_rate"]):
            g = "declared" if d["declared_base"] else "none"
            z, cls = classify(d["pointer_rate"], d["pointers"], g, ref, stats) if g in stats else (0, "unclassed")
            print("  %-60s %-14s %5.2f z %+.2f %-8s copied %5.1f per 1,000%s"
                  % (d["name"], ",".join(d["declared_base"]) or "-", d["pointer_rate"], z, cls,
                     d.get("copied_per_1000", 0), "" if d.get("cites_held_source") else " (sources not held)"))
        rule = ref["copied_class_rule"]
        m, sd = stats.get("copied", (0, 0))
        print("Copied words per 1,000 (fixed rule): light < %g, heavy > %g; for context mean %.1f, sigma %.1f"
              % (rule["light_below"], rule["heavy_above"], m, sd))
        return
    if not a.outdir:
        ap.error("give <output-dir>, or --reference")

    with open(os.path.join(a.outdir, "text.txt"), encoding="utf-8") as f:
        raw = f.read()
    text = "\n".join(l for l in raw.splitlines() if not CONTENTS_LINE.match(l.strip()))
    r = reference_measures(text)
    declared = dict(r["declared"])
    for b in filter(None, (x.strip() for x in a.declared_base.split(","))):
        declared.setdefault(b, "(given with --declared-base)")

    if a.json:
        print(json.dumps({**r, "declared_base": sorted(declared)}, indent=2))
        return

    print("### Dependence on outside sources\n")
    print("Words: %d (text.txt has %d; the rates here leave out contents lines)\n" % (r["words"], len(raw.split())))
    print("**Declared base:** " + (", ".join(sorted(declared)) if declared else "none found") + "\n")
    for b, s in sorted(declared.items()):
        print("- %s: \"%s\"" % (b, s))
    if declared:
        print()
    print("**By reference**\n")
    print("| Measure | Value |\n|---|---|")
    print("| Body mentions per 1,000 words | %.2f |" % r["mention_rate"])
    print("| Top body and its share of mentions | %s, %.0f%% |" % (r["top_body"] or "-", r["concentration"] * 100))
    print("| Pointers per 1,000 words | %.2f (%d) |" % (r["pointer_rate"], r["pointers"]))
    print("| Distinct outside document identifiers | %d |" % len(r["doc_ids"]))
    print()
    if r["mentions"]:
        print("Mentions by body: " + ", ".join("%s %d" % kv for kv in sorted(r["mentions"].items(), key=lambda kv: -kv[1])) + "\n")
    if r["doc_ids"]:
        print("Identifiers: " + ", ".join(r["doc_ids"]) + "\n")
    group = "declared" if declared else "none"
    if stats and group in stats:
        z, cls = classify(r["pointer_rate"], r["pointers"], group, ref, stats)
        m, sd = stats[group]
        print("**Pointer rate class:** %s (z %+.2f against documents %s a declared base: mean %.2f, sigma %.2f)\n"
              % (cls, z, "with" if declared else "without", m, sd))
    if r["top_body"] and r["concentration"] >= 0.5 and sum(r["mentions"].values()) >= MIN_BASE_MENTIONS \
            and r["top_body"] not in declared:
        print("**Possible undeclared base:** %s has %.0f%% of body mentions (%d) but isn't declared as a base "
              "in the title, scope or introduction.\n"
              % (r["top_body"], r["concentration"] * 100, r["mentions"][r["top_body"]]))

    if sources_given and not a.sources:
        print("**By copying:** not checked: the held-sources folder `%s` was not found.\n" % sources_given)
    if a.sources:
        c = copy_measures(text, a.sources, declared, a.n, a.min_words)
        print("**By copying** (stretches of %d+ words shared word for word)\n" % a.min_words)
        if c["rows"]:
            print("| Source | Role | Words matched | Per 1,000 words of the document | Longest run | In normative text |")
            print("|---|---|---|---|---|---|")
            for row in c["rows"]:
                print("| `%s` | %s | %d | %.1f | %d | %d |" % (row["source"], row["role"], row["words"],
                                                                row["words"] / c["words"] * 1000,
                                                                row["longest"], row["normative"]))
            print()
        else:
            print("No shared stretches found.\n")
        print("Original words: %.1f per 1,000 words of the document" % (c["original"] * 1000)
              + (", %.1f per 1,000 words of its normative text (%d words)" % (c["original_normative"] * 1000, c["normative_words"])
                 if c["original_normative"] is not None else ", no normative text found") + "\n")
        share = (1 - c["original"]) * 1000  # copied words per 1,000
        # Classed only if the document names a held source (by number, or --cites-held says
        # so): for any other a result of 0 only means there was nothing to compare it with.
        cites = a.cites_held or cites_held(r["doc_ids"], held_names(a.sources))
        if not cites:
            print("**Copied words:** %s (the document cites no held source, so not classed)\n"
                  % ("%.1f per 1,000 words matched a held source" % share if share > 0
                     else "none found; sources not held"))
        elif ref:
            rule = ref["copied_class_rule"]
            m, sd = stats.get("copied", (0, 0))
            print("**Copied words class:** %s (%.1f per 1,000 words copied from outside sources; fixed rule: light "
                  "below %g, heavy above %g; z %+.2f against documents whose cited sources were held, mean %.1f, "
                  "sigma %.1f, for context)\n"
                  % (copy_class(share, ref), share, rule["light_below"], rule["heavy_above"],
                     (share - m) / sd if sd else 0, m, sd))
        if c["skipped"]:
            print("Not checked (couldn't be read): " + ", ".join("`%s`" % s for s in c["skipped"]) + "\n")


if __name__ == "__main__":
    main()
