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
import re
import subprocess
import sys

import _yaml_lite
import build_etom_index
import yaml

# A component's own component.yaml declares its exposed/dependent APIs by TMFxxx
# id -- a genuine forward link (spec/spec.md 5.0), unlike the reverse use_cases
# link below. Some function blocks (managementFunction's metrics/dependentAPI
# entries) carry template placeholder ids (e.g. "exposedAPI_id") instead of a
# real TMFxxx id -- this pattern is what tells a real API apart from a stub.
TMF_API_ID_RE = re.compile(r"^TMF\d+$")

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


def extract_forward_apis(yaml_path):
    """Every real TMFxxx id a component's own component.yaml declares as an
    exposed or dependent API, across coreFunction/managementFunction/
    securityFunction -- the forward link half of spec/spec.md 5.0's
    links.apis, authored straight from the component's own spec, not
    computed from anything else in the corpus."""
    with open(yaml_path, encoding="utf-8") as f:
        spec = yaml.safe_load(f) or {}
    body = spec.get("spec", {}) or {}
    apis = {}
    for block_name in ("coreFunction", "managementFunction", "securityFunction"):
        block = body.get(block_name, {}) or {}
        for key in ("exposedAPIs", "dependentAPIs"):
            for api in block.get(key, []) or []:
                api_id = api.get("id")
                if api_id and TMF_API_ID_RE.match(str(api_id)):
                    apis.setdefault(api_id, api.get("name"))
    return [{"id": api_id, "name": apis[api_id]} for api_id in sorted(apis)]


def sync_component_links(components, use_cases):
    """Writes links.apis (forward, from the component's own component.yaml)
    and links.use_cases (reverse, reconciled used_by already computed above)
    back into each component's own component.meta.json and TMFCxxx.md
    frontmatter, so a skill reading a single component file sees both
    without a second index lookup -- see spec/spec.md 5.0/5.2 and the
    add_reconciled_component_used_by docstring above for how used_by itself
    is derived."""
    name_by_use_case = {uc["id"]: uc["name"] for uc in use_cases}

    for row in components:
        comp_id = row["id"]
        comp_dir = os.path.join(KNOWLEDGE_DIR, "components", comp_id)
        yaml_path = os.path.join(comp_dir, "component.yaml")
        apis = extract_forward_apis(yaml_path) if os.path.exists(yaml_path) else []
        use_case_ids = sorted({entry["use_case"] for entry in row["used_by"]})
        use_cases_links = [{"id": uc_id, "name": name_by_use_case.get(uc_id, uc_id)} for uc_id in use_case_ids]
        links = {"apis": apis, "use_cases": use_cases_links}

        meta_path = os.path.join(comp_dir, "component.meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            meta["links"] = links
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
                f.write("\n")

        md_path = os.path.join(comp_dir, f"{comp_id}.md")
        if os.path.exists(md_path):
            with open(md_path, encoding="utf-8") as f:
                data, body = _yaml_lite.split(f.read())
            data["links"] = links
            _yaml_lite.write(md_path, data, body)


def main():
    use_cases = load_use_cases()
    components = add_reconciled_component_used_by(load_meta_rows("components"), use_cases)
    apis = add_reverse_links(load_meta_rows("apis"), use_cases, "apis")
    sync_component_links(components, use_cases)

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
