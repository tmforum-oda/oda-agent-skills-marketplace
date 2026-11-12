"""How much of a document is about TM Forum's ODA, counted by term density.

Counts, per 1,000 words of the document's text, the terms that name TM Forum's
own items in seven parts of ODA:

  components    TMF component numbers (TMFCnnn) that TM Forum has published,
                "ODA Component"; component specification, inventory or definition
                in TM Forum context
  canvas        "ODA Canvas", oda-canvas, Canvas CTK; Canvas operator, API or
                platform in TM Forum context
  APIs          TMF Open API numbers that TM Forum has published, "TM Forum Open
                API", "ODA Open API"; "Open API" in TM Forum context
  frameworks    eTOM, Frameworx, GB921, GB922, GB929, GB1033, "Open Digital
                Architecture", "ODA Functional Architecture", "ODA Technical
                Architecture"; SID, TAM, the Business Process, Information,
                Application and Functional Frameworks in TM Forum context
  use cases     "ODA use case", "TM Forum use case"; use cases and UC numbers in
                TM Forum context
  HVS           "HVS", "high-value scenario" in TM Forum context
  solution packages  "solution package" in TM Forum context

Only TM Forum's items count. A term that is TM Forum's by name (eTOM, ODA
Canvas, a published TMFC or TMF Open API number) always counts. A generic term
(use case, SID, Open API, Information Framework, solution package) counts only
in TM Forum context: when its paragraph, or the paragraph either side, names
TM Forum, ODA, eTOM, Frameworx, a TMF or TMFC number, or a TM Forum document
number (GBnnn, IGnnnn, TRnnn). A TMF or TMFC number TM Forum hasn't published
(references/tmforum-identifiers.json) doesn't count. "OpenAPI" (the
OpenAPI Specification, one word) and "Open API Specification" never count.
The terms left out are counted and printed beside the ones that count.

The score is the sum of the seven rates (equal weights). It counts mentions
only: it does not look at the title or document type, and it does not show
whether a document defines, implements or only cites the thing it names.

The document's own identifier is removed first (found in the first lines of
the text), so a document is not scored for naming itself. Remove anything
else that is the document's own name with --exclude-own, a regular
expression (for example "TMF ?44[345]" for the three AI-agent specifications
that cite each other, or "Functional Architecture" for a document with that
title).

The class is a fixed rule (references/oda-reference.json):
  light    score below 5 per 1,000 words
  typical  5 to 20
  heavy    above 20
set by Hugo Vaughan. The reference table shows the same rule applied to the
38 reference documents.

Usage:
  python -I oda_score.py <output-dir> [--exclude-own REGEX]
  python -I oda_score.py --reference          (print the reference table)
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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCE = os.path.join(HERE, "..", "references", "oda-reference.json")
IDENTIFIERS = os.path.join(HERE, "..", "references", "tmforum-identifiers.json")

with open(IDENTIFIERS, encoding="utf-8") as _f:
    _ids = json.load(_f)
TMF_COMPONENTS = set(_ids["components"])
TMF_APIS = set(_ids["apis"])

# Each part has terms that are TM Forum's by name ("own") and generic terms that
# count only in TM Forum context ("context"). Acronyms are case-sensitive.
CATEGORIES = [
    ("components",
     r"\bTMFC\d{3}\b|(?i:\bODA[- ]Components?\b)",
     r"(?i:\bcomponent specifications?\b|\bComponent (?:Inventory|Definition|Catalogue|Catalog)\b)"),
    ("canvas",
     r"(?i:\bODA Canvas\b|\boda-canvas\b|\bCanvas CTK\b)",
     r"(?i:\bComponent Canvas\b|\bCanvas\b(?= (?:operator|API|implementation|reference|platform|environment)))"),
    ("APIs",
     r"\bTMF ?\d{3}[A-Z]?\b|(?i:\bTM ?Forum Open APIs?\b|\bODA Open APIs?\b)",
     r"(?i:\bOpen APIs?\b(?! Specification| Initiative))"),
    ("frameworks",
     r"\beTOM\b|(?i:\bFrameworx\b|\bGB ?(?:921|922|929|1033)\b|\bOpen Digital (?:Architecture|Framework)\b"
     r"|\bODA (?:Functional|Technical|Reference) Architecture\b|\bODA Architecture\b)",
     r"\bSID\b|\bTAM\b|(?i:\bBusiness Process Framework\b|\bInformation Framework\b|\bApplication Framework\b"
     r"|\bFunctional Framework\b|\bTechnical Architecture\b)"),
    ("use cases",
     r"(?i:\b(?:ODA|TM ?Forum) use[- ]cases?\b)",
     r"(?i:\buse[- ]cases?\b)|\bUC-?\d{2,4}\b"),
    ("HVS",
     None,
     r"\bHVSs?\b|(?i:\bhigh[- ]value scenarios?\b)"),
    ("solution packages",
     None,
     r"(?i:\bsolution packages?\b)"),
]
COMPILED = [(name, re.compile(own) if own else None, re.compile(ctx)) for name, own, ctx in CATEGORIES]
TMF_CONTEXT = re.compile(r"(?i:\bTM ?Forum\b|\bTMForum\b|\bODA\b|\bFrameworx\b)|\beTOM\b|\bTMFC?\d{3}\b"
                         r"|\b(?:GB|IG|TR)\d{3,4}[A-Z]?\b")
OWN_ID = re.compile(r"\b(?:TMF|GB|IG|TR|TAC)-?\d{3,4}[A-Z]?\b", re.I)
HEAD_LINES = 8  # the cover names the document once; later lines may cite other documents


def own_ids(text):
    """The document's own number: identifiers named in the first few lines (the cover) of the text."""
    head = "\n".join([l for l in text.splitlines() if l.strip()][:HEAD_LINES])
    return sorted({m.group(0) for m in OWN_ID.finditer(head)})


def published(term):
    """True unless the term is a TMF or TMFC number TM Forum hasn't published."""
    m = re.fullmatch(r"TMF(C?) ?(\d{3})[A-Z]?", term)
    if not m:
        return True
    return ("TMFC" + m.group(2)) in TMF_COMPONENTS if m.group(1) else ("TMF" + m.group(2)) in TMF_APIS


def count_terms(text):
    """Counted and left-out terms per part. Context is the paragraph and the one either side."""
    paras = [p for p in text.splitlines() if p.strip()]
    marked = [bool(TMF_CONTEXT.search(p)) for p in paras]
    counted = {name: 0 for name, _, _ in COMPILED}
    left_out = {name: 0 for name, _, _ in COMPILED}
    unpublished = set()
    for i, p in enumerate(paras):
        context = any(marked[max(0, i - 1):i + 2])
        for name, own, ctx in COMPILED:
            spans = []
            if own:
                for m in own.finditer(p):
                    spans.append(m.span())
                    if published(m.group(0)):
                        counted[name] += 1
                    else:
                        left_out[name] += 1
                        unpublished.add(m.group(0).replace(" ", ""))
            for m in ctx.finditer(p):
                if any(s <= m.start() < e for s, e in spans):
                    continue
                if context:
                    counted[name] += 1
                else:
                    left_out[name] += 1
    return counted, left_out, sorted(unpublished)


def measure(text, exclude_own=None, rule=None):
    removed = own_ids(text)
    for i in removed:
        text = re.sub(re.escape(i), " ", text)
    if exclude_own:
        text = re.sub(exclude_own, " ", text, flags=re.I)
    words = len(text.split()) or 1
    counts, left_out, unpublished = count_terms(text)
    rates = {n: c * 1000 / words for n, c in counts.items()}
    score = sum(rates.values())
    return {"words": words, "counts": counts, "left_out": left_out, "unpublished": unpublished,
            "rates": rates, "score": score,
            "categories": sum(1 for v in rates.values() if v >= 1), "removed": removed,
            "class": classify(score, rule)}


def load_reference():
    with open(REFERENCE, encoding="utf-8") as f:
        return json.load(f)


def classify(score, rule=None):
    rule = rule or load_reference()["class_rule"]
    return "heavy" if score > rule["heavy_above"] else "light" if score < rule["light_below"] else "typical"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir", nargs="?")
    ap.add_argument("--exclude-own", help="regular expression for other names to remove before counting")
    ap.add_argument("--reference", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    ref = load_reference()
    rule = ref["class_rule"]
    if a.reference:
        print("ODA content reference: %d documents; light < %g, typical %g to %g, heavy > %g per 1,000 words"
              % (len(ref["documents"]), rule["light_below"], rule["light_below"], rule["heavy_above"], rule["heavy_above"]))
        for d in sorted(ref["documents"], key=lambda d: -d["score"]):
            print("  %-60s %6.1f  %-8s  %d of 7 parts" % (d["name"], d["score"], classify(d["score"], rule), d["categories"]))
        return
    if not a.outdir:
        ap.error("give <output-dir>, or --reference")

    with open(os.path.join(a.outdir, "text.txt"), encoding="utf-8", errors="replace") as f:
        text = f.read()
    r = measure(text, a.exclude_own, rule)
    r["text_words"] = len(text.split())
    if a.json:
        print(json.dumps(r))
        return
    print("### ODA content\n")
    print("Words: %d (text.txt has %d; the rates here are after removing the document's own identifier%s%s)\n"
          % (r["words"], r["text_words"], "s" if len(r["removed"]) > 1 else "",
             ": " + ", ".join(r["removed"]) if r["removed"] else ""))
    print("| Part of ODA | TM Forum terms | Per 1,000 words | Left out (generic or unpublished) |\n|---|---|---|---|")
    for name, _, _ in CATEGORIES:
        print("| %s | %d | %.2f | %d |" % (name, r["counts"][name], r["rates"][name], r["left_out"][name]))
    print()
    print("**ODA content score:** %.1f per 1,000 words, **%s** (light below %g, typical %g to %g, heavy above %g). "
          "%d of the 7 parts have at least 1 term per 1,000 words.\n"
          % (r["score"], r["class"], rule["light_below"], rule["light_below"], rule["heavy_above"],
             rule["heavy_above"], r["categories"]))
    if r["unpublished"]:
        print("TMF or TMFC numbers left out because TM Forum hasn't published them: %s.\n" % ", ".join(r["unpublished"]))
    print("Only TM Forum's items count: generic terms (use case, SID, Open API, solution package) count only in a "
          "paragraph that names TM Forum, ODA, eTOM, a TMF or TMFC number or a TM Forum document, or next to one. "
          "This counts mentions only. It doesn't use the title or document type, and it doesn't show whether the "
          "document defines, implements or only cites what it names.\n")


if __name__ == "__main__":
    main()
