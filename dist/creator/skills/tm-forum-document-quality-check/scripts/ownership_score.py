"""Score a document on ownership, and on poorly cited ownership, and
classify both against the reference set.

Items are material owned by non-Contributors. Each has:
  weight  1.0 whole figure or word-for-word passage;
          0.5 adapted figure, close paraphrase or unconfirmed origin
  cited   1.0 complete credit (title, author, source, licence, date);
          0.75 complete but for the date;
          0.5 partial (right source, but no licence, author or quote marks);
          0   none, or credited to the wrong source
Clip art and icons, contributing Members' own material and reworded ideas
are not items.

  ownership score              = sum(weight) per 1,000 words
  poorly cited ownership score = sum(weight * (1 - cited)) per 1,000 words

Only the poorly cited ownership score is classified; the ownership score
is reported with its z for context. The class is the fixed rule
"class_rule" in references/ownership-reference.json:
  good       score up to good_at_most (0.05 per 1,000 words), and no whole
             figure or word-for-word passage (weight 1.0) with no credit
             at all (cited 0)
  bad        score above bad_above (0.15 per 1,000 words)
  improving  in between
Without a class_rule it falls back to the mean and standard deviation
(sigma) of the reference documents at k = "sigma_multiplier" (0.8).

Usage:
  python -I ownership_score.py --words 12345 --items 1:0.5,1:0,0.5:0.5
      (each item is weight:cited)
  python -I ownership_score.py --reference      (print the reference table)
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import json
import os
import statistics
import sys

REFERENCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "ownership-reference.json")


def scores(words, items):
    """Return (ownership, poorly cited ownership) for (weight, cited) items."""
    own = sum(w for w, _ in items) / words * 1e3
    poor = sum(w * (1 - c) for w, c in items) / words * 1e3
    return own, poor


def fixed_poor_class(value, items, rule):
    """Poorly cited ownership by the fixed rule; items are (weight, cited) pairs."""
    if value > rule["bad_above"]:
        return "bad"
    whole_uncredited = any(w >= 1 and c == 0 for w, c in items)
    if value <= rule["good_at_most"] and not (rule.get("good_needs_no_uncredited_whole_item") and whole_uncredited):
        return "good"
    return "improving"


def rule_text(rule):
    extra = (", with no whole figure or word-for-word passage left with no credit"
             if rule.get("good_needs_no_uncredited_whole_item") else "")
    return "good up to %.2f%s, bad above %.2f, improving in between" % (rule["good_at_most"], extra, rule["bad_above"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--words", type=int)
    ap.add_argument("--items", default="", help="comma-separated weight:cited pairs, e.g. 1:0.5,0.5:0 (empty for none)")
    ap.add_argument("--reference", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    with open(REFERENCE, encoding="utf-8") as f:
        ref = json.load(f)
    k = ref["sigma_multiplier"]
    ref_scores = [scores(d["words"], [(i["weight"], i["cited"]) for i in d["items"]]) for d in ref["documents"]]
    stats = []
    for col in (0, 1):
        vals = [s[col] for s in ref_scores]
        m, sd = statistics.mean(vals), statistics.pstdev(vals)
        stats.append((m, sd, m - k * sd, m + k * sd))

    def classify(value, col, items=()):
        m, sd, low, high = stats[col]
        text = "%.3f z %+.2f" % (value, (value - m) / sd)
        if col == 1:  # only the poorly cited ownership score is classified
            text += " " + poor_class(value, low, high, items)
        return text

    def poor_class(value, low, high, items):
        rule = ref.get("class_rule")
        if rule:  # a fixed rule, not the mean and sigma of the reference set
            return fixed_poor_class(value, items, rule)
        return "bad" if value > high else "good" if value < low else "improving"

    m, sd, _, _ = stats[0]
    print("Ownership reference: mean %.3f, sigma %.3f (not classified)" % (m, sd))
    m, sd, low, high = stats[1]
    print("Poorly cited ownership reference: mean %.3f, sigma %.3f (for context)" % (m, sd))
    rule = ref.get("class_rule")
    if rule:
        print("  Classed by a fixed rule: %s" % rule_text(rule))
    else:
        print("  Classed at k %.1f: good < %.2f, bad > %.2f" % (k, low, high))
    if a.reference:
        print("  %-55s  %-28s  %s" % ("Document", "Ownership", "Poorly cited ownership"))
        for d, (own, poor) in sorted(zip(ref["documents"], ref_scores), key=lambda x: x[1][1]):
            pairs = [(i["weight"], i["cited"]) for i in d["items"]]
            print("  %-55s  %-28s  %s" % (d["name"], classify(own, 0), classify(poor, 1, pairs)))
    if a.words:
        items = []
        for pair in filter(None, (p.strip() for p in a.items.split(","))):
            w, c = pair.split(":")
            items.append((float(w), float(c)))
        own, poor = scores(a.words, items)
        print("This document: %d items" % len(items))
        print("  Ownership:              %s" % classify(own, 0))
        print("  Poorly cited ownership: %s" % classify(poor, 1, items))
    elif not a.reference:
        ap.error("give --words (and --items), or --reference")


if __name__ == "__main__":
    main()
