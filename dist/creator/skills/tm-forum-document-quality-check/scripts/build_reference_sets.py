"""Rebuild the four reference sets from a manifest of checked documents.

The scores in a report are classed against reference sets: the ownership,
AI-indicator and dependence scores (and, within the dependence set, the
copied-text share). Rather than keep each set by hand, build them all from
the same manifest used by combined_report.py, so every set covers the same
documents.

Usage:
  python -I build_reference_sets.py <manifest.json> --sources <sources-dir> [--dry-run]

For each document in the manifest it runs the automatic scans (as
combined_report.py does) and takes the ownership items a person judged from
the manifest. It then writes, in ../references/:
  ownership-reference.json      words and ownership items
  ai-indicators-reference.json  the five AI-indicator measures and the score
  dependence-reference.json     pointer and mention rates, declared base,
                                copied share and whether a held source is cited
Each manifest entry may carry a "name" (the long document name used in the
reference tables); it defaults to the label. Notes already written against a
document in the old dependence set are kept. Prints how each document's class
changes against the new sets.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import combined_report as cr  # noqa: E402

REF = os.path.join(HERE, "..", "references")


def path(name):
    return os.path.join(REF, name)


def load_old(name):
    p = path(name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"documents": []}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest")
    ap.add_argument("--sources", required=True)
    ap.add_argument("--dry-run", action="store_true", help="print the summary without writing the files")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    manifest = cr.load(a.manifest)
    base = os.path.dirname(os.path.abspath(a.manifest))
    for e in manifest["documents"]:
        for field in ("dir", "docx"):
            if e.get(field) and not os.path.isabs(e[field]):
                e[field] = os.path.normpath(os.path.join(base, e[field]))

    old_stats = cr.reference_stats()  # only used to run the scans; the classes it gives are discarded
    held = cr.held_names(a.sources)
    docs = [cr.scan(e, a.sources, held, old_stats) for e in manifest["documents"]]
    for d, e in zip(docs, manifest["documents"]):
        d["name"] = e.get("name") or e["label"]
        if not e.get("ownership"):
            sys.exit("%s has no judged ownership items: it can't join the reference set" % d["name"])

    old_own, old_ai, old_dep = (load_old(n) for n in
                                ("ownership-reference.json", "ai-indicators-reference.json",
                                 "dependence-reference.json"))
    k = old_dep.get("sigma_multiplier", 0.8)
    notes = {x["name"].split()[0]: x["note"] for x in old_dep["documents"] if x.get("note")}
    notes.update({x["name"].split()[0]: x["note"] for x in old_own["documents"] if x.get("note")})

    own_docs, ai_docs, dep_docs = [], [], []
    for d, e in zip(docs, manifest["documents"]):
        key = d["key"]
        o = {"name": d["name"], "words": e["ownership"]["words"], "items": e["ownership"]["items"]}
        if key in notes:
            o["note"] = notes[key]
        own_docs.append(o)
        x = d["ai"]
        ai_docs.append({"name": d["name"], "words": x["words"], "assistant": len(x["assistant"]),
                        "provenance": len(x["provenance"]), "figure_mismatches": x["mismatches"],
                        "style_shift": round(x["shift"], 3), "wording_per_1000": round(x["wording_rate"], 2),
                        "em_dash_per_1000": round(x["dash_rate"], 2), "score": round(x["score"], 2)})
        r = d["dep"]
        entry = {"name": d["name"], "words": r["words"], "declared_base": d["declared"],
                 "pointer_rate": round(r["pointer_rate"], 2), "mention_rate": round(r["mention_rate"], 2),
                 "top_body": r["top_body"], "concentration": round(r["concentration"], 2),
                 "doc_ids": len(r["doc_ids"]), "pointers": r["pointers"],
                 "copied_per_1000": round(d["copied"], 1), "cites_held_source": d["cites_held"]}
        if key in notes:
            entry["note"] = notes[key]
        dep_docs.append(entry)

    n = len(docs)
    n_held = sum(1 for x in dep_docs if x["cites_held_source"])
    n_base = sum(1 for x in dep_docs if x["declared_base"])
    out = {
        "ownership-reference.json": {
            "description": ("Ownership reference set: %d documents checked on 2026-10-20 and 2026-10-21 (the same "
                            "documents as the other reference sets; drafts still being written are left out). Items "
                            "are material owned by non-Contributors. weight: whole figure, word-for-word passage, "
                            "close paraphrase or reworded idea from an identifiable work 1.0; adapted figure or "
                            "unconfirmed origin 0.5. cited: complete credit "
                            "(title, author, source, licence) 1.0; partial (right source, but no licence, author or "
                            "quotation marks) 0.5; none or wrong source 0. Clip art and icons, contributing "
                            "Members' own material, and ideas common across a field are excluded. Ownership score = total weight "
                            "per 1,000 words; poorly cited ownership score = total weight x (1 - cited) per 1,000 "
                            "words." % n),
            "sigma_multiplier": k,
            **({"class_rule": old_own["class_rule"]} if old_own.get("class_rule") else {}),
            "documents": own_docs},
        "ai-indicators-reference.json": {
            "description": ("AI-indicator reference scores, computed by ai_indicators.py for the same %d documents "
                            "as the ownership reference set." % n),
            "sigma_multiplier": k,
            **{key: old_ai[key] for key in ("class_rule", "style_shift_rule") if key in old_ai},
            "documents": ai_docs},
        "dependence-reference.json": {
            "description": ("Reference dependence measures for the same %d documents (%d with a declared base, %d "
                            "that cite a source held in sdo-sources). pointer_rate = pointer phrases ('as defined "
                            "in', 'see', 'according to' ...) followed within 10 words by a standards body or outside "
                            "document identifier, per 1,000 words, contents lines excluded. Only pointer_rate is "
                            "classed, separately for documents with and without a declared base. copied_per_1000 = words per 1,000 of "
                            "the document's words in stretches of 12+ words shared word for word with an outside "
                            "source in sdo-sources, with TM Forum's section 14.1 notice masked out; it is classed "
                            "only against the documents that cite a held source (cites_held_source), since for the "
                            "rest a zero only means their sources weren't held. Heavy also needs at least "
                            "min_heavy_pointers pointers, because most documents without a declared base have none "
                            "and one or two in a short document would otherwise class as heavy." % (n, n_base, n_held)),
            "sigma_multiplier": k, "min_heavy_pointers": old_dep.get("min_heavy_pointers", 3),
            **{key: old_dep[key] for key in ("copied_class_rule", "pointer_light_at_zero", "pointer_light_note")
               if key in old_dep},
            "documents": dep_docs}}

    # Class changes against the old sets, for the report to the user.
    new_stats = {
        "poor": (lambda v: (sum(v) / len(v), (sum((x - sum(v) / len(v)) ** 2 for x in v) / len(v)) ** 0.5))(
            [cr.poorly_cited(o["words"], o["items"]) for o in own_docs]),
        "ai": (lambda v: (sum(v) / len(v), (sum((x - sum(v) / len(v)) ** 2 for x in v) / len(v)) ** 0.5))(
            [x["score"] for x in ai_docs])}
    new_cuts = cr.ai_indicators.class_cuts({"class_rule": old_ai.get("class_rule", {"low_share": 0.25, "high_share": 0.2}),
                                            "documents": ai_docs})
    print("Reference sets over %d documents (%d with a declared base, %d citing a held source)" % (n, n_base, n_held))
    print("  poorly cited ownership: old mean %.2f sigma %.2f -> new mean %.2f sigma %.2f"
          % (*old_stats["poor"], *new_stats["poor"]))
    print("  AI indicators:          old mean %.2f sigma %.2f -> new mean %.2f sigma %.2f"
          % (*old_stats["ai"], *new_stats["ai"]))
    changes = 0
    for d, o in zip(docs, own_docs):
        pv = cr.poorly_cited(o["words"], o["items"])
        old_c = cr.poor_class(pv, cr.z(pv, old_stats["poor"]), old_stats, k, o["items"])
        new_c = cr.poor_class(pv, cr.z(pv, new_stats["poor"]), old_stats, k, o["items"])  # same fixed rule when there is one
        if old_c != new_c:
            changes += 1
            print("  ownership class %-10s %-9s -> %s" % (d["key"], old_c, new_c))
    for d, x in zip(docs, ai_docs):
        if x["assistant"] or x["provenance"]:
            continue
        old_c = cr.ai_indicators.class_of(x["score"], old_stats["ai_cuts"])
        new_c = cr.ai_indicators.class_of(x["score"], new_cuts)
        if old_c != new_c:
            changes += 1
            print("  AI class        %-10s %-9s -> %s" % (d["key"], old_c, new_c))
    print("  class changes so far: %d (pointer and copied classes are shown by the reports)" % changes)

    if a.dry_run:
        print("Dry run: nothing written.")
        return
    for fname, content in out.items():
        with open(path(fname), "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print("Wrote %s" % ", ".join(out))


if __name__ == "__main__":
    main()
