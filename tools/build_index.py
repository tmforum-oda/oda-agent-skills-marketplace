"""Reads: every knowledge/use-cases/**/*.md frontmatter block; every
knowledge/{components,apis}/**/*.meta.json; (via build_etom_index) every
knowledge/components/*/component.yaml and knowledge/etom/{processes,deleted}.json.
Writes: knowledge/index/{use-cases,components,apis}.json, and
knowledge/index/etom-index.json (delegated to build_etom_index.py).
Track: shared -- run at the end of either refresh track (or both) to
regenerate the corpus-wide index; gates on validate_envelope.py.

tools/build_index.py -- regenerate knowledge/index/{use-cases,components,apis}.json
from every artefact's envelope (spec/spec.md 5.4).

Walks the envelope the same way regardless of artefact type -- frontmatter for
knowledge/use-cases/**/*.md, *.meta.json for knowledge/components/** and
knowledge/apis/** -- per the "one envelope, shared by every artefact type"
principle (spec.md 5.0/§3 principle 9). No type-specific parsing needed here
beyond which reader function opens the file.

components.json's used_by is RECONCILED against usecase-component-matrix.json
(IG1228 ch.2's independently-sourced use-case/component table) -- the union of
each use case's own forward links.components (frontmatter) and the matrix's
own reverse index, with every entry tagged "confirmed" / "frontmatter_only" /
"matrix_only" so the disagreement signal survives the merge instead of being
silently erased by it (spec/spec-ontology.md §2/§8, knowledge/index/
matrix-discrepancies.md). This used to be deliberately left unmerged -- the
reconciliation now happens once, here, instead of being re-derived by every
skill that needs it.

apis.json's used_by stays plain frontmatter-only (a sorted TMFSxxx id list, no
per-entry source tag): the matrix is IG1228 ch.2's use-case/COMPONENT table,
it has no API-level data to reconcile against at all, so there is nothing to
merge for an API id -- this is a real, structural asymmetry between the two
artefact types, not an oversight (see spec.md 5.4).

Must be idempotent (spec.md principle 7, success criterion in §9): run twice
with no input changes, byte-identical output. That's why every dict below is
built with explicit, sorted key order rather than relying on iteration order
of a directory listing or a set.

Runs tools/validate_envelope.py --strict as its last step -- an index built
from a corpus with an incomplete envelope is worse than no index (a lookup
would silently return partial data), so that check gates a successful run.

Usage:
    python build_index.py
"""
import glob
import json
import os
import subprocess
import sys

import _yaml_lite
import build_etom_index

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
KNOWLEDGE_DIR = os.path.join(REPO_ROOT, "knowledge")
INDEX_DIR = os.path.join(KNOWLEDGE_DIR, "index")


def rel(path):
    return os.path.relpath(path, REPO_ROOT).replace("\\", "/")


def load_use_cases():
    rows = []
    for path in sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, "use-cases", "*", "*.md"))):
        with open(path, encoding="utf-8") as f:
            data, _ = _yaml_lite.split(f.read())
        rows.append(
            {
                "id": data["id"],
                "type": data["type"],
                "name": data["name"],
                "version": data["version"],
                "status": data["status"],
                "maturity": data.get("maturity"),
                "approval_status": data.get("approval_status"),
                "release_status": data.get("release_status"),
                "components": sorted(c["id"] for c in data.get("links", {}).get("components", [])),
                "apis": sorted(a["id"] for a in data.get("links", {}).get("apis", [])),
                "path": rel(path),
            }
        )
    return sorted(rows, key=lambda r: r["id"])


def load_meta_rows(subdir):
    rows = []
    for path in sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, subdir, "*", "*.meta.json"))):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        content_path = path[: -len(".meta.json")] + (".yaml" if subdir == "components" else ".json")
        rows.append(
            {
                "id": data["id"],
                "type": data["type"],
                "name": data["name"],
                "version": data["version"],
                "status": data["status"],
                "source_origin": data.get("source", {}).get("origin"),
                "path": rel(content_path) if os.path.exists(content_path) else None,
                "meta_path": rel(path),
            }
        )
    return rows


def add_reverse_links(rows, use_cases, link_key):
    """rows: apis.json rows, keyed by id. link_key: 'apis'. Plain frontmatter-only
    reverse index -- see module docstring for why apis.json doesn't get the
    matrix reconciliation components.json gets."""
    used_by = {}
    for uc in use_cases:
        for ref_id in uc[link_key]:
            used_by.setdefault(ref_id, set()).add(uc["id"])
    for row in rows:
        row["used_by"] = sorted(used_by.get(row["id"], []))
    return rows


def load_matrix_component_used_by():
    """TMFCxxx -> sorted TMFSxxx ids IG1228 ch.2 credits with using this
    component -- usecase-component-matrix.json's own components[id].used_by,
    already a precomputed reverse index, not re-derived from the use_cases
    side of that same file."""
    path = os.path.join(INDEX_DIR, "usecase-component-matrix.json")
    with open(path, encoding="utf-8") as f:
        matrix = json.load(f)
    return {cid: sorted(row.get("used_by", [])) for cid, row in matrix.get("components", {}).items()}


def add_reconciled_component_used_by(rows, use_cases):
    """rows: components.json rows. Replaces the old frontmatter-only used_by
    with the union of each use case's own forward links.components and the
    matrix's independently-sourced used_by, every entry tagged with which
    source(s) actually support it -- see module docstring."""
    frontmatter_used_by = {}
    for uc in use_cases:
        for cid in uc["components"]:
            frontmatter_used_by.setdefault(cid, set()).add(uc["id"])

    matrix_used_by = load_matrix_component_used_by()

    for row in rows:
        cid = row["id"]
        fm = frontmatter_used_by.get(cid, set())
        mx = set(matrix_used_by.get(cid, []))
        entries = []
        for uc_id in sorted(fm | mx):
            if uc_id in fm and uc_id in mx:
                source = "confirmed"
            elif uc_id in fm:
                source = "frontmatter_only"
            else:
                source = "matrix_only"
            entries.append({"use_case": uc_id, "source": source})
        row["used_by"] = entries
    return rows


def main():
    use_cases = load_use_cases()
    components = add_reconciled_component_used_by(load_meta_rows("components"), use_cases)
    apis = add_reverse_links(load_meta_rows("apis"), use_cases, "apis")

    os.makedirs(INDEX_DIR, exist_ok=True)
    outputs = {
        "use-cases.json": sorted(use_cases, key=lambda r: r["id"]),
        "components.json": sorted(components, key=lambda r: r["id"]),
        "apis.json": sorted(apis, key=lambda r: r["id"]),
    }
    for filename, data in outputs.items():
        with open(os.path.join(INDEX_DIR, filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=False)
            f.write("\n")

    print(f"use-cases.json: {len(use_cases)} rows")
    print(f"components.json: {len(components)} rows")
    print(f"apis.json: {len(apis)} rows")

    # eTOM corpus <-> component join (spec/spec-etom.md 5). No-ops with a message
    # if knowledge/etom/processes.json isn't there yet (build_etom.py not run).
    build_etom_index.main()

    print("\nRunning validate_envelope.py --strict as the gating check...")
    result = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "validate_envelope.py"), "--strict", KNOWLEDGE_DIR]
    )
    if result.returncode != 0:
        sys.exit("build_index.py: validate_envelope.py --strict failed -- index was written but is built on an incomplete corpus, fix the envelope gaps above and re-run")


if __name__ == "__main__":
    main()
