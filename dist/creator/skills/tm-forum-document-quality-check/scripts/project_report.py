"""Build the combined report (combined_report.py) with a Project scores table: for each project, the share
of its documents flagged on each measure, weighted, classed by a fixed rule (see project_section). Each document is matched to its TM Forum project in a Compass asset-list export (sheet
"IP check status": column B the file name, column C the project), by file name, else by another version of
the same document. Then render the report with make_report.py.

Usage: python -I project_report.py <manifest.json> <compass.xlsx> <report.md> <sources-dir> <as-of YYYY-MM-DD>
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import datetime
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combined_report as cr  # noqa: E402
import editorial_score  # noqa: E402
import openpyxl  # noqa: E402

# Compass spells two projects two ways; merged like spellings of one person in the author table.
MERGE = {"Digital Maturity Model": "Digital Maturity Model Project",
         "Open Digitial Architecture (ODA)": "Open Digital Architecture Project"}


def strip(s):
    return re.sub(r"( \(1\))?\.(docx|xlsx|pdf)$", "", s or "")


def compass_projects(xlsx, manifest):
    rows = [r for r in list(openpyxl.load_workbook(xlsx, read_only=True)["IP check status"].iter_rows(values_only=True))[1:]
            if r[1]]
    out = {}
    for e in manifest["documents"]:
        key = e.get("key") or e["label"].split()[0]
        stem = strip((e.get("docx") or "").replace("\\", "/").split("/")[-1])
        hit = next((r for r in rows if strip(r[1]) == stem), None)
        how = "same file"
        if not hit:  # another version of the same document series is in Compass
            pre = e["label"].split()[0] + "_"
            hit = next((r for r in rows if r[1].startswith(pre) and r[0] != "Not checked"), None) \
                or next((r for r in rows if r[1].startswith(pre)), None)
            ver = re.search(r"v?(\d+\.\d+\.\d+)", e["label"])
            how = "same file" if hit and ver and ("v" + ver.group(1)) in hit[1] else "other version"
        if hit and hit[2]:
            out[key] = (MERGE.get(hit[2], hit[2]), how, hit[1])
        else:
            out[key] = (None, None, None)
    return out


# Project score: the share of a project's documents flagged on each measure, weighted by how much the measure
# matters for IP, averaged over the measures its documents have. Pointers are shown but carry no weight:
# dependence on other bodies' work isn't an IP risk.
MEASURES = [  # (field, column title, flagged when, weight)
    ("poor_cls", "Poorly cited ownership (bad)", lambda v: v == "bad", 3),
    ("copy_cls", "Copied (heavy)", lambda v: v == "heavy", 2),
    ("ai_cls", "Automation Indicators (high)", lambda v: v.startswith("high"), 1),
    ("ed_cls", "Editorial (inconsistent)", lambda v: v in editorial_score.FLAGGED, 1),
    ("ptr_cls", "Pointers (heavy)", lambda v: v == "heavy", 0),
]
MIN_PROJECT_DOCS = 2      # fewer scored documents than this: the project is listed but not classed
CLASS_RULE = (0.10, 0.30)  # low up to the first, medium up to the second, high above


def version_of(label):
    m = re.search(r"\bv(\d+(?:\.\d+)*)\b", label)
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


def series_of(label):
    return re.sub(r"\s*\bv\d+(?:\.\d+)*\b.*$", "", label).strip()


def scored_docs(docs):
    """The documents a project score counts: Word documents only, and only the latest version of each."""
    latest = {}
    for d in docs:
        if d["project"] and not d["spreadsheet"]:
            s = series_of(d["label"])
            if s not in latest or version_of(d["label"]) > version_of(latest[s]["label"]):
                latest[s] = d
    return {id(d) for d in latest.values()}


def project_class(score):
    return "low" if score <= CLASS_RULE[0] else "medium" if score <= CLASS_RULE[1] else "high"


def project_rows(docs):
    counted = scored_docs(docs)
    by = {}
    for d in docs:
        if d["project"]:
            by.setdefault(d["project"], {"docs": [], "counted": []})["docs"].append(d)
            if id(d) in counted:
                by[d["project"]]["counted"].append(d)
    rows = []
    for n, e in by.items():
        cols, num, den = [], 0.0, 0
        for field, _, flagged, weight in MEASURES:
            have = [x for x in e["counted"] if x[field] is not None]
            hits = sum(1 for x in have if flagged(x[field]))
            cols.append((hits, len(have)))
            if have and weight:
                num += weight * hits / len(have)
                den += weight
        score = num / den if den else None
        rows.append((score, n, e, cols))
    return sorted(rows, key=lambda r: (len(r[2]["counted"]) < MIN_PROJECT_DOCS, -(r[0] or 0), r[1]))


def project_section(docs, k, compass_name):
    out = []
    w = out.append
    w("## Project scores\n")
    w("**Project.** The TM Forum project that owns the document, as the Compass asset list (%s) gives it. A "
      "document is matched to Compass by its file name; where Compass holds a different version of the same "
      "document (%s), that version's project is used. Two projects that Compass spells two ways are merged "
      "(Digital Maturity Model with Digital Maturity Model Project, and Open Digitial Architecture (ODA) with "
      "Open Digital Architecture Project).\n"
      % (compass_name, ", ".join(d["key"] for d in docs if d["project_how"] == "other version") or "none"))
    w("**Documents.** The documents the project owns, by short name. The score counts Word documents only, and "
      "only the latest version of each document; spreadsheets (whose scores aren't comparable with the Word "
      "documents') and earlier versions are listed in brackets but not counted.\n")
    w("**The measure columns.** How many of the counted documents are flagged on each measure, out of those that "
      "have it: poorly cited ownership classed **bad**, copied words **heavy**, Automation Indicators **high**, "
      "editorial consistency **inconsistent** or **very inconsistent**, pointers **heavy**. A dash means none of "
      "the counted documents has the measure.\n")
    w("**Project score and Project class.** The share of flagged documents on each measure, weighted by how much the measure "
      "matters for IP and averaged over the measures the project's documents have: poorly cited ownership %d, "
      "copied words %d, Automation Indicators %d, editorial consistency %d. Pointers are shown but carry no "
      "weight, because dependence on other bodies' work isn't an IP risk. The score runs from 0 (no document "
      "flagged) to 1 (every document flagged on every measure). The class is a fixed rule: **low** up to %.2f, "
      "**medium** up to %.2f, **high** above %.2f. A project needs at least %d counted documents to be classed; "
      "one with fewer is listed at the end as \"too few to class\". Colours: a measure cell is green when no "
      "document is flagged, amber when up to 30%% are, red above that (grey shades for copied words and pointers, "
      "as elsewhere in this report); the score and class are green for low, amber for medium and red for high. "
      "The class describes the documents checked, "
      "which aren't a sample chosen to represent each project.\n"
      % (MEASURES[0][3], MEASURES[1][3], MEASURES[2][3], MEASURES[3][3], CLASS_RULE[0], CLASS_RULE[1],
         CLASS_RULE[1], MIN_PROJECT_DOCS))
    w("| Project | Documents | %s | Project score | Project class |" % " | ".join(m[1] for m in MEASURES))
    w("|---|---|%s---|---|" % ("---|" * len(MEASURES)))
    for score, n, e, cols in project_rows(docs):
        counted = {id(x) for x in e["counted"]}
        names = ", ".join(d["key"] if id(d) in counted else "(%s)" % d["key"] for d in e["docs"])
        cells = ["-" if have == 0 else "%d of %d" % (hits, have) for hits, have in cols]
        if score is None or len(e["counted"]) < MIN_PROJECT_DOCS:
            sc, cl = ("-" if score is None else "%.2f" % score), "too few to class"
        else:
            sc, cl = "%.2f" % score, project_class(score)
        w("| %s | %s | %s | %s | %s |" % (n, names, " | ".join(cells), sc, cl))
    none = [d["key"] for d in docs if not d["project"]]
    if none:
        w("\nDocuments not in the Compass asset list (%s) aren't in the project table.\n" % ", ".join(none))
    return "\n".join(out) + "\n"


def main():
    manifest_p, xlsx, out_p, sources, as_of = sys.argv[1:6]
    sources = graceful.sources(sources)
    sys.stdout.reconfigure(encoding="utf-8")
    as_of = datetime.date.fromisoformat(as_of)
    manifest = cr.load(manifest_p)
    base = os.path.dirname(os.path.abspath(manifest_p))
    for e in manifest["documents"]:
        for field in ("dir", "docx"):
            if e.get(field) and not os.path.isabs(e[field]):
                e[field] = os.path.normpath(os.path.join(base, e[field]))
    proj = compass_projects(xlsx, manifest)
    s = cr.reference_stats()
    held = cr.held_names(sources)
    docs = [cr.scan(e, sources, held, s, as_of) for e in manifest["documents"]]
    for d in docs:
        d["project"], d["project_how"], d["compass_file"] = proj[d["key"]]
        print(d["key"], "->", d["project"], "|", d["project_how"], "|", d["compass_file"])
    text = cr.report(manifest, docs, s, sources, as_of)
    marker = "## Evidence behind"
    i = text.index(marker)
    text = text[:i] + project_section(docs, s["k"], os.path.basename(xlsx)) + "\n" + text[i:]
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(text)
    print("Wrote %s: %d projects" % (out_p, len(project_rows(docs))))


if __name__ == "__main__":
    main()
