"""Pick the provisional depth of check (the tier) for a document, from what
the cheap first pass has found.

The first pass is: extract_docx.py, key_extracts.py, credit_check.py,
image_scan.py, and the held-source comparison. This script reads their
output and says how deep the rest of the check should go:

  light       nothing found so far
              -> the floor: one contact-sheet pass, batch 1 of the web
                 check, one fetch per credited source
  doubled     something found, but the provisional poorly cited score is
              not above 0.15 per 1,000 words
              -> every credited passage placed, all three web batches,
                 flow-style and textbook-looking figures at full size,
                 every figure label compared with the text
  redoubled   the provisional poorly cited score is above 0.15 per 1,000
              words, or 10 or more words per 1,000 are copied word for
              word from held sources
              -> the doubled work, plus the sections around each finding,
                 each credited source opened in full, every distinctive
                 figure label searched, headers, footers and captions read

What counts as "something found" (any one):
  - a passage credited to a source outside TM Forum (cited.txt, leaving
    out TM Forum's own hosts, example.com addresses and yaml.org);
  - words copied word for word from a held source (with --sources, or
    with --copied given from an earlier copy check);
  - a judged ownership item (--items weight:cited,...).
A scan flag on its own doesn't raise the tier: flags add image looks, not
depth (most flags on text-heavy diagrams are false alarms), but the count
is reported.

Re-run it as items are found: the tier only goes up during a run, and the
final tier is the one the report states. The thresholds come from the 38
reference documents (references/scoring-notes.md): this trigger caught 7 of
8 bad and 12 of 16 improving documents and fired on 3 of 14 good ones. It
is a guide to effort, not a score: it has no class of its own and no fixes
follow from it.

Usage:
  python -I triage.py <output-dir> [--sources <dir>] [--copied <per 1,000>]
         [--items 1:0.5,0.5:0] [--words N]
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

BAD_ABOVE = 0.15         # per 1,000 words; the poorly cited ownership rule
REDOUBLE_COPIED = 10.0   # words copied from held sources per 1,000
TM_HOSTS = re.compile(r"tm\s?forum|tmforum|example\.(?:com|org)|yaml\.org", re.I)

CHECKLIST = {
    "light": [
        "extract, key extracts, credit check, held-source copy check",
        "images: credited ones from the caption, flagged ones one at a time, the rest on contact sheets",
        "figure-label check on figures whose caption or text names their parts",
        "web check: each credited source opened once; batch 1 (7) of the other sentences, stop if clean",
    ],
    "doubled": [
        "everything in the light tier",
        "place every credited passage: compare each with its source, and search distinctive sentences when the credited page lacks it",
        "web check: all three batches of other sentences",
        "look at flow-style, architecture and textbook-looking figures at full size, one at a time",
        "figure-label check on every figure that carries text",
    ],
    "redoubled": [
        "everything in the doubled tier",
        "search the sections around each finding, sentence by sentence",
        "open each credited source in full; search every distinctive figure label set",
        "read headers, footers and captions for notice and credit problems",
        "judge each item at the stricter reading and list what stayed unconfirmed and why",
    ],
}


def read_cited(path):
    entries = []
    if os.path.isfile(path):
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if " | " in line:
                    entries.append(line.rstrip("\n").split(" | ", 1))
    return entries


def count_flags(path):
    n = 0
    if os.path.isfile(path):
        with open(path, encoding="utf-8", errors="replace") as f:
            n = sum(1 for line in f if "FLAGGED" in line)
    return n


def copied_per_1000(outdir, sources):
    import dependence  # noqa: E402  (same folder; -I doesn't add it to sys.path)
    with open(os.path.join(outdir, "text.txt"), encoding="utf-8", errors="replace") as f:
        text = "\n".join(l for l in f.read().splitlines() if not dependence.CONTENTS_LINE.match(l.strip()))
    c = dependence.copy_measures(text, sources, {}, 8, 12)
    return (1 - c["original"]) * 1000


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("--sources", help="folder of held sources, to measure copied words")
    ap.add_argument("--copied", type=float, help="copied words per 1,000 from an earlier copy check")
    ap.add_argument("--items", default="", help="judged ownership items so far, weight:cited pairs")
    ap.add_argument("--words", type=int, help="word count (default: from text.txt)")
    a = ap.parse_args()
    a.sources = graceful.sources(a.sources)
    sys.stdout.reconfigure(encoding="utf-8")

    text_path = os.path.join(a.outdir, "text.txt")
    words = a.words
    if not words and os.path.isfile(text_path):
        with open(text_path, encoding="utf-8", errors="replace") as f:
            words = len(f.read().split())
    words = words or 1

    entries = read_cited(os.path.join(a.outdir, "cited.txt"))
    outside = [(s, p) for s, p in entries if not TM_HOSTS.search(s)]
    sources = {s.strip() for s, _ in outside}
    flags = count_flags(os.path.join(a.outdir, "image_flags.txt"))

    copied = a.copied
    if copied is None and a.sources:
        copied = copied_per_1000(a.outdir, a.sources)

    items = []
    for pair in filter(None, (p.strip() for p in a.items.split(","))):
        w, c = pair.split(":")
        items.append((float(w), float(c)))
    poor = sum(w * (1 - c) for w, c in items) / words * 1000 if items else 0.0

    reasons = []
    tier = "light"
    if outside:
        tier = "doubled"
        reasons.append("%d passage(s) credited to %d source(s) outside TM Forum" % (len(outside), len(sources)))
    if copied:
        tier = "doubled"
        reasons.append("%.1f words per 1,000 copied word for word from held sources" % copied)
    if items:
        tier = "doubled"
        reasons.append("%d judged ownership item(s), provisional poorly cited score %.3f per 1,000 words"
                       % (len(items), poor))
    if poor > BAD_ABOVE:
        tier = "redoubled"
        reasons.append("provisional poorly cited score above %.2f per 1,000 words" % BAD_ABOVE)
    if copied and copied >= REDOUBLE_COPIED:
        tier = "redoubled"
        reasons.append("copied words at or above %g per 1,000" % REDOUBLE_COPIED)
    if not reasons:
        reasons.append("no outside credited passage, no copying from held sources, no judged item")

    print("### Depth of check\n")
    print("**Provisional tier: %s** (%d words). Triggers: %s.\n" % (tier, words, "; ".join(reasons)))
    print("Scan flags: %d (these add image looks, not depth).\n" % flags)
    print("What this tier asks for:\n")
    for line in CHECKLIST[tier]:
        print("- " + line)
    print("\nThe tier can only go up as items are found; re-run with --items. State the final tier in the report.\n")


if __name__ == "__main__":
    main()
