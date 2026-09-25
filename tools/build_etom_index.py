"""Reads: knowledge/etom/processes.json and knowledge/etom/deleted.json
(build_etom.py's output); every knowledge/components/*/component.yaml
(`spec.componentMetadata.eTOMs`).
Writes: knowledge/index/etom-index.json.
Track: shared -- run after build_etom.py and any component refresh. Called
automatically at the end of tools/build_index.py.

tools/build_etom_index.py -- the join that makes the eTOM corpus useful to the
consumer skills (spec/spec-etom.md 5): which ODA component implements which
eTOM process, plus a by-domain id list and an honest account of the
component references that don't resolve against v26.0.

Each component declares the eTOM activities it is responsible for as
`spec.componentMetadata.eTOMs` -- pipe-delimited `id|Name|vXX.0` entries, the
version being the eTOM release the mapping was authored against (v21.5-v25.0
across the current corpus; the cached eTOM corpus is v26.0). eTOM was
renumbered for 25.5/26.0, so a good fraction of those ids no longer exist at
their old number. This script resolves each reference as far as the data
honestly allows:

  in_v26        id still exists in processes.json                -> implemented_by
  name_matched  id gone, but its Name resolves to exactly one    -> implemented_by
                v26 process (renumbered, same activity)             (also flagged)
  deleted_in_X  id is on the eTOM Deleted sheet                   -> stale only
  not_in_v26    id gone, Name doesn't resolve, not on Deleted     -> stale only
  malformed     not a dotted-numeric id                          -> stale only

`implemented_by` is therefore "the join TM Forum's own data currently
supports", not "complete" -- a skill reading it must say so (spec-etom.md 8).
The component `component.yaml` files are NOT rewritten to fix stale ids
(spec.md's report-both-versions-don't-reconcile rule).

Idempotent: every list sorted (process ids hierarchically, component ids
lexically), byte-identical output on a re-run with unchanged inputs.

Usage:
    python build_etom_index.py
"""
import glob
import json
import os
import re

import yaml

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
KNOWLEDGE_DIR = os.path.join(REPO_ROOT, "knowledge")
PROCESSES_PATH = os.path.join(KNOWLEDGE_DIR, "etom", "processes.json")
DELETED_PATH = os.path.join(KNOWLEDGE_DIR, "etom", "deleted.json")
COMPONENTS_GLOB = os.path.join(KNOWLEDGE_DIR, "components", "*", "component.yaml")
OUT_PATH = os.path.join(KNOWLEDGE_DIR, "index", "etom-index.json")

DOTTED_ID_RE = re.compile(r"\d+(\.\d+)*")


def natkey(pid):
    return tuple(int(p) for p in str(pid).split("."))


def norm_name(s):
    """Fold a component eTOM name (`Negotiate_Sales/Contract`) and an eTOM
    process name (`Negotiate Sales/Contract`) onto the same key."""
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def parse_etom_entry(raw):
    """`id|Name|vXX.0` -> (id, name, version). Tolerates a stray extra `|` in
    the name field (seen once: `...|Product_Configuration_Management|Manage_Product_Configuration|v25.0`)."""
    parts = [p.strip() for p in str(raw).split("|")]
    pid = parts[0]
    version = parts[-1] if len(parts) > 1 else None
    name = "|".join(parts[1:-1]) if len(parts) > 2 else (parts[1] if len(parts) == 2 else "")
    return pid, name, version


def load_components():
    """cid -> list of (etom_id, etom_name, etom_version), sorted by cid."""
    out = {}
    for path in sorted(glob.glob(COMPONENTS_GLOB)):
        cid = os.path.basename(os.path.dirname(path))
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        etoms = (((doc or {}).get("spec") or {}).get("componentMetadata") or {}).get("eTOMs") or []
        if etoms:
            out[cid] = [parse_etom_entry(e) for e in etoms]
    return out


def build(processes, deleted, components):
    live_ids = {p["id"] for p in processes}
    deleted_by_id = {d["id"]: d for d in deleted}
    name_to_ids = {}
    for p in processes:
        name_to_ids.setdefault(norm_name(p["name"]), set()).add(p["id"])

    by_domain = {}
    for p in processes:
        by_domain.setdefault(p["domain"], []).append(p["id"])
    by_domain = {d: sorted(v, key=natkey) for d, v in sorted(by_domain.items())}

    implemented_by = {}
    stale = {}  # keyed by etom_id so multiple components on one bad id collapse to one record

    for cid, entries in components.items():
        for etom_id, etom_name, etom_version in entries:
            if etom_id in live_ids:
                implemented_by.setdefault(etom_id, set()).add(cid)
                continue

            hits = name_to_ids.get(norm_name(etom_name.replace("_", " ")), set())
            if not DOTTED_ID_RE.fullmatch(etom_id):
                resolution, resolved_to = "malformed", None
            elif len(hits) == 1:
                resolved_to = next(iter(hits))
                resolution = "name_matched"
                implemented_by.setdefault(resolved_to, set()).add(cid)
            elif etom_id in deleted_by_id:
                rel = deleted_by_id[etom_id].get("deleted_in")
                resolution = f"deleted_in_{rel}" if rel else "deleted"
                resolved_to = None
            else:
                resolution, resolved_to = "not_in_v26", None

            rec = stale.setdefault(
                etom_id,
                {
                    "etom_id": etom_id,
                    "etom_name": etom_name,
                    "components": set(),
                    "component_etom_versions": set(),
                    "resolution": resolution,
                    "resolved_to": resolved_to,
                },
            )
            rec["components"].add(cid)
            if etom_version:
                rec["component_etom_versions"].add(etom_version)

    implemented_by = {k: sorted(implemented_by[k]) for k in sorted(implemented_by, key=natkey)}
    stale_list = [
        {
            "etom_id": r["etom_id"],
            "etom_name": r["etom_name"],
            "components": sorted(r["components"]),
            "component_etom_versions": sorted(r["component_etom_versions"]),
            "resolution": r["resolution"],
            "resolved_to": r["resolved_to"],
        }
        for r in sorted(stale.values(), key=lambda r: natkey(r["etom_id"]))
    ]

    unresolvable = sum(1 for r in stale_list if r["resolution"] != "name_matched")
    return {
        "summary": {
            "components_with_etom_mappings": len(components),
            "processes_with_an_implementer": len(implemented_by),
            "stale_component_refs": len(stale_list),
            "unresolvable_component_refs": unresolvable,
            "by_resolution": _count_by_resolution(stale_list),
        },
        "by_domain": by_domain,
        "implemented_by": implemented_by,
        "stale_component_refs": stale_list,
    }


def _count_by_resolution(stale_list):
    counts = {}
    for r in stale_list:
        counts[r["resolution"]] = counts.get(r["resolution"], 0) + 1
    return {k: counts[k] for k in sorted(counts)}


def main():
    if not os.path.exists(PROCESSES_PATH):
        print("build_etom_index.py: knowledge/etom/processes.json not found -- run build_etom.py first; skipping")
        return
    with open(PROCESSES_PATH, encoding="utf-8") as f:
        processes = json.load(f)
    with open(DELETED_PATH, encoding="utf-8") as f:
        deleted = json.load(f)
    components = load_components()

    index = build(processes, deleted, components)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, sort_keys=False, ensure_ascii=False)
        f.write("\n")

    s = index["summary"]
    print(
        f"etom-index.json: {s['processes_with_an_implementer']} eTOM processes <- "
        f"{s['components_with_etom_mappings']} components; "
        f"{s['stale_component_refs']} stale refs "
        f"({s['unresolvable_component_refs']} unresolvable) {s['by_resolution']}"
    )


if __name__ == "__main__":
    main()
