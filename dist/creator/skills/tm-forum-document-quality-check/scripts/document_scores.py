"""Score one document for its own report, and keep the record a combined report reads later.

Reads the document's entry.json (the same fields as one document in a combined report's manifest;
see combined_report.py beside it), runs the same scans the combined report runs,
and prints the document's score row as Markdown, to go directly under the report's title. The row is
taken from combined_report.py's own document table for this one document, so it has the same
columns, figures, z and classes as the document's row in a combined report built later.

Usage:
  python -I document_scores.py <entry.json> [--sources <dir>] [--as-of YYYY-MM-DD] [--out <scores.md>]

entry.json sits in work/documents/<key>/, with paths relative to that folder:
  {"key": "IG1242", "label": "IG1242 v26.0.0", "dir": ".",
   "docx": "../../../source/IG1242_....docx", "figure_mismatches": 0,
   "ownership": {"words": 9603, "items": [{"item": "...", "weight": 1.0, "cited": 0.5}]},
   "web_check": {"searched": 20, "outside": 0}, ...}
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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The scans and the document table are in combined_report.py, beside this script.
sys.path.insert(0, HERE)
import combined_report as cr  # noqa: E402


def cells(d, s, sources, as_of):
    """This document's row in combined_report.py's document table, without the Document and Authors cells."""
    lines = cr.report({}, [d], s, sources, as_of, core_age_only=False).splitlines()
    head = next(i for i, l in enumerate(lines) if l.startswith("| Document | Authors |"))
    split = lambda l: [c.strip() for c in l.strip().strip("|").split(" | ")]  # noqa: E731
    return split(lines[head])[2:], split(lines[head + 2])[2:]


def block(columns, row, scanned, spreadsheet=False):
    out = ["**Document score.**\n",
           "| %s |" % " | ".join(columns),
           "|%s" % ("---|" * len(columns)),
           "| %s |" % " | ".join(row),
           "",
           "Cells give the score and its class. Each measure, and the evidence behind it, is "
           "set out in its own section below."]
    if not scanned:
        out[-1] += " Poorly cited ownership is \"not scanned\" because no ownership items were judged."
    if spreadsheet:
        out += ["", "**Not comparable with the Word documents.** " + cr.SPREADSHEET_NOTE]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entry")
    ap.add_argument("--sources")
    ap.add_argument("--as-of", type=datetime.date.fromisoformat, default=datetime.date.today(),
                    help="date the core citation's age is counted to (default today)")
    ap.add_argument("--out", help="also write the block to this file")
    a = ap.parse_args()
    a.sources = graceful.sources(a.sources)
    sys.stdout.reconfigure(encoding="utf-8")
    folder = os.path.dirname(os.path.abspath(a.entry))
    with open(a.entry, encoding="utf-8") as f:
        entry = json.load(f)
    entry.setdefault("dir", ".")
    for field in ("dir", "docx"):
        if entry.get(field) and not os.path.isabs(entry[field]):
            entry[field] = os.path.normpath(os.path.join(folder, entry[field]))
    s = cr.reference_stats()
    d = cr.scan(entry, a.sources, cr.held_names(a.sources), s, a.as_of)
    text = block(*cells(d, s, a.sources, a.as_of), d["poor"] is not None, d["spreadsheet"])
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)


if __name__ == "__main__":
    main()
