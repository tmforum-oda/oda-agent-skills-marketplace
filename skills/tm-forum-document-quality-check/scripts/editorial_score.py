"""Score and render a document's editorial consistency check.

The check itself is a person's (or a model's) reading of the document against
itself; this script only scores the findings and writes the report section, so
every document is scored and laid out the same way.

Usage:
  python -I editorial_score.py <doc-dir> [--md <out.md>] [--update-entry]
                                                           score one document
  python -I editorial_score.py --build-reference <documents-dir>
                                                           rebuild the reference set
  python -I editorial_score.py --reference                 print the reference set

<doc-dir>/editorial.json:
  {"key": "GB1096", "words": 9238,
   "not_checked": "whether the domain content is technically correct",
   "findings": [{"category": "inconsistent", "location": "§5.2 The Mapping to Gates",
                 "finding": "..."}]}

Categories and weights (weight = how far the finding stops a reader relying on
the document):
  inconsistent  3  internally inconsistent rules
  normative     2  implementation detail given more normative weight than its evidence
  specificity   2  unsupported specificity
  reference     1  incomplete references and cross-references
  duplicate     1  duplicate concepts

Length. Weighted findings don't grow in proportion to length: some faults
happen once per document (an empty section, a missing glossary), so a plain
rate per 1,000 words would make every short document look worse. The reference
set fits expected weighted findings = a x (words / 1,000)^b, and the score is
the document's weighted findings divided by the number expected for its length:
1.00 is what a document of that length typically has, 1.50 half as many again.
The score is classed by a fixed rule (CLASS_RULE): consistent up to 1.15,
improving up to 1.3, inconsistent up to 1.5, very inconsistent above 1.5. Each
band is wider than one weight-3 finding moves the score for a document of
3,000 words or more. Its z against the reference set is reported for context.

The curve (a and b) is frozen: --build-reference keeps the a and b already in
the reference file, so a rebuild doesn't move every score and with it the
classes. Pass --refit to fit them again.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references", "editorial-reference.json")
K = 0.8
# Fixed class rule on the length-adjusted score (upper limits); z is reported for context only.
CLASS_RULE = [(1.15, "consistent"), (1.3, "improving"), (1.5, "inconsistent"), (None, "very inconsistent")]
FLAGGED = ("inconsistent", "very inconsistent")


def class_of(score):
    return next(c for limit, c in CLASS_RULE if limit is None or score <= limit)


def rule_text():
    return ("consistent up to %.2f, improving up to %.2f, inconsistent up to %.2f, very inconsistent above %.2f"
            % (CLASS_RULE[0][0], CLASS_RULE[1][0], CLASS_RULE[2][0], CLASS_RULE[2][0]))

CATEGORIES = [
    ("duplicate", "Duplicate concepts", 1),
    ("inconsistent", "Internally inconsistent rules", 3),
    ("reference", "Incomplete references and cross-references", 1),
    ("specificity", "Unsupported specificity", 2),
    ("normative", "Implementation detail given more normative weight than the evidence supports", 2),
]
WEIGHT = {c: w for c, _, w in CATEGORIES}

MARKER = (
    "> **This skill's addition, not an IP or licence finding.** This is a reading of the "
    "document against itself. It doesn't come from the six references and isn't one of the "
    "IP scores; its score is shown here and in the document score block. Locations are "
    "given as the section number and heading from the document's table of contents."
)


def load(doc_dir):
    p = os.path.join(doc_dir, "editorial.json")
    with open(p, encoding="utf-8") as f:
        e = json.load(f)
    bad = [x.get("category") for x in e["findings"] if x.get("category") not in WEIGHT]
    if bad:
        sys.exit("unknown categories in %s: %s" % (p, sorted(set(map(str, bad)))))
    if not e.get("words"):
        sys.exit("%s has no words count" % p)
    return e


def counts_of(e):
    counts = {c: 0 for c in WEIGHT}
    for x in e["findings"]:
        counts[x["category"]] += 1
    return counts


def reference():
    if not os.path.exists(REF):
        return None
    with open(REF, encoding="utf-8") as f:
        return json.load(f)


def evaluate(counts, words, ref):
    """Weighted findings, the rate per 1,000 words, and (with a reference set) the length-adjusted
    score, its z and class."""
    weighted = sum(WEIGHT[c] * n for c, n in counts.items())
    r = {"counts": counts, "words": words, "weighted": weighted, "rate": weighted * 1000.0 / words,
         "expected": None, "score": None, "z": None, "class": "not classed (no reference set)"}
    if ref:
        r["expected"] = ref["a"] * (words / 1000.0) ** ref["b"]
        r["score"] = weighted / r["expected"]
        r["z"] = (r["score"] - ref["mean"]) / ref["sigma"] if ref["sigma"] else 0.0
        r["class"] = class_of(r["score"])
    return r


def build_reference(docs_dir, refit=False):
    rows = []
    for p in sorted(glob.glob(os.path.join(docs_dir, "*", "editorial.json"))):
        e = load(os.path.dirname(p))
        rows.append({"key": e["key"], "words": e["words"],
                     "weighted": sum(WEIGHT[c] * n for c, n in counts_of(e).items())})
    rows = [r for r in rows if r["weighted"] > 0]
    if len(rows) < 3:
        sys.exit("need at least three documents with findings")
    x = [math.log(r["words"] / 1000.0) for r in rows]
    y = [math.log(r["weighted"]) for r in rows]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    b = sum((u - mx) * (v - my) for u, v in zip(x, y)) / sum((u - mx) ** 2 for u in x)
    a = math.exp(my - b * mx)
    old = reference()
    if old and not refit:
        print("keeping the frozen curve a %.4f, b %.4f (a fresh fit would give a %.4f, b %.4f; --refit to use it)"
              % (old["a"], old["b"], a, b))
        a, b = old["a"], old["b"]
    for r in rows:
        r["score"] = round(r["weighted"] / (a * (r["words"] / 1000.0) ** b), 3)
    s = [r["score"] for r in rows]
    m = sum(s) / len(s)
    sd = math.sqrt(sum((v - m) ** 2 for v in s) / (len(s) - 1))
    ref = {"note": "Editorial consistency reference set: every document in work/documents with an "
                   "editorial.json. Expected weighted findings = a x (words/1000)^b, fitted on logs; "
                   "score = weighted / expected; mean and sigma of the scores give z for context; the class "
                   "is a fixed rule in editorial_score.py. a and b are frozen: a rebuild keeps them unless "
                   "--refit is given.",
           "k": K, "n": len(rows), "a": round(a, 4), "b": round(b, 4),
           "mean": round(m, 4), "sigma": round(sd, 4), "documents": rows}
    with open(REF, "w", encoding="utf-8") as f:
        json.dump(ref, f, indent=1, ensure_ascii=False)
    print("reference set: %d documents; expected = %.2f x (words/1000)^%.3f; score mean %.3f, sigma %.3f; "
          "classes by the fixed rule: %s" % (len(rows), a, b, m, sd, rule_text()))


def esc(s):
    return s.replace("|", "\\|").replace("\n", " ")


def render(e, r, ref):
    out = ["## Editorial consistency check", "", MARKER, ""]
    out += ["| Category | Weight | Findings | Weighted |", "|---|---|---|---|"]
    for c, title, w in CATEGORIES:
        out.append("| %s | %d | %d | %d |" % (title, w, r["counts"][c], w * r["counts"][c]))
    out.append("| **Total** | | **%d** | **%d** |" % (sum(r["counts"].values()), r["weighted"]))
    out.append("")
    if r["score"] is None:
        out.append("**Editorial consistency score:** not classed (no reference set). Weighted findings %d, "
                   "%.2f per 1,000 words (%d words)." % (r["weighted"], r["rate"], r["words"]))
    else:
        out.append("**Editorial consistency score:** %.2f, z %+.2f, **%s**. The document has %d weighted findings "
                   "(%.2f per 1,000 words of its %s); a document of its length is expected to have %.1f. "
                   "The class is set by a fixed rule: %s. For context, the reference set of %d documents has a "
                   "mean score of %.2f and σ %.2f."
                   % (r["score"], r["z"], r["class"], r["weighted"], r["rate"], format(r["words"], ","), r["expected"],
                      rule_text(), ref["n"], ref["mean"], ref["sigma"]))
    out.append("")
    out.append("Weights: internally inconsistent rules 3; unsupported specificity and normative weight 2 each; "
               "incomplete references and duplicate concepts 1 each. The score is the weighted findings divided "
               "by the number expected for a document of this length (1.00 is typical for its length), because "
               "some faults occur once per document whatever its size. Like the other scores, the class is a "
               "finding: no fixes follow from it.")
    for c, title, _ in CATEGORIES:
        rows = [x for x in e["findings"] if x["category"] == c]
        out += ["", "### " + title, ""]
        if not rows:
            out.append("None found.")
            continue
        out += ["| Location | Finding |", "|---|---|"]
        for x in rows:
            out.append("| %s | %s |" % (esc(x["location"]), esc(x["finding"])))
    nc = e.get("not_checked", "whether the domain content is technically correct").rstrip(".")
    out += ["", "Not checked: %s." % nc]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("doc_dir", nargs="?")
    ap.add_argument("--md")
    ap.add_argument("--update-entry", action="store_true",
                    help="write the counts into <doc-dir>/entry.json, for the document score and combined report")
    ap.add_argument("--build-reference")
    ap.add_argument("--refit", action="store_true", help="with --build-reference, fit a and b again")
    ap.add_argument("--reference", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.build_reference:
        build_reference(a.build_reference, a.refit)
        return
    if a.reference:
        print(json.dumps(reference(), indent=1, ensure_ascii=False))
        return
    if not a.doc_dir:
        ap.error("doc_dir is required")
    e = load(a.doc_dir)
    ref = reference()
    r = evaluate(counts_of(e), e["words"], ref)
    print("%s: %s, weighted %d (%.2f per 1,000 words); %s"
          % (e["key"], r["counts"], r["weighted"], r["rate"],
             r["class"] if r["score"] is None else "score %.2f (expected %.1f), z %+.2f, %s"
             % (r["score"], r["expected"], r["z"], r["class"])))
    if a.md:
        with open(a.md, "w", encoding="utf-8") as f:
            f.write(render(e, r, ref))
    if a.update_entry:
        p = os.path.join(a.doc_dir, "entry.json")
        with open(p, encoding="utf-8") as f:
            entry = json.load(f)
        entry["editorial"] = {"words": r["words"], "counts": r["counts"]}
        with open(p, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
