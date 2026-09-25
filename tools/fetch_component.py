"""Reads: knowledge/index/component-folder-map.json (rebuilt from GitHub if
missing or via --refresh-map).
Writes: knowledge/index/component-folder-map.json;
knowledge/components/{TMFCxxx}/component.yaml + .meta.json.
Track: automated (spec.md 6.2) -- public, unauthenticated, safe to schedule.

tools/fetch_component.py -- ODA Component ID -> cached spec (spec/spec.md 5.2, 5.2.1).

Two steps:
  1. List the tmforum-rand/TMForum-ODA-Ready-for-publication tree once at the
     pinned tag, split each folder name on its first '-' to build {id: folder},
     cache it as knowledge/index/component-folder-map.json. This is the
     generated equivalent of tmforum-oda/reference-example-components's
     hand-maintained skills/create-oda-component/references/component-list.md
     -- same data, same URL pattern, generated instead of hand-checked.
  2. For a given TMFCxxx id, look up its folder, fetch
     {folder}/Specification/{folder}.yaml unmodified, and write the universal
     envelope alongside it as component.meta.json, with componentMetadata.status
     (IG1242's own vocabulary: future/planned/specified/prototype/available)
     read straight out of the fetched YAML, not guessed.

If an id isn't in the folder map at all, it has no published spec yet: write
component.meta.json only (status: "not_yet_specified"), no component.yaml --
spec/spec.md 5.2 wants that to be a clean, unambiguous answer, not a 404 a
caller has to interpret itself.

Public, unauthenticated, safe to run on a schedule (spec/spec.md 6.2).

Usage:
    python fetch_component.py <TMFCxxx> [<TMFCxxx> ...]
    python fetch_component.py --all-referenced   # every id in knowledge/use-cases/**/*.md
    python fetch_component.py --refresh-map      # just rebuild the folder map, fetch nothing
"""
import datetime as _dt
import glob
import hashlib
import json
import os
import sys

import _http
import _yaml_lite
import yaml

REPO = "tmforum-rand/TMForum-ODA-Ready-for-publication"
TAG = "v1.0.0"
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")
MAP_PATH = os.path.join(KNOWLEDGE_DIR, "index", "component-folder-map.json")


def build_folder_map():
    """spec/spec.md 5.2.1 -- one directory listing at the pinned tag, not one
    request per component; this is what makes the id->folder lookup below
    a local dict read instead of N more network round-trips."""
    entries = _http.get_json(f"https://api.github.com/repos/{REPO}/contents/?ref={TAG}")
    folder_map = {}
    for entry in entries:
        name = entry["name"]
        if entry["type"] == "dir" and name.startswith("TMFC") and "-" in name:
            comp_id, _, _short = name.partition("-")
            folder_map[comp_id] = name
    os.makedirs(os.path.dirname(MAP_PATH), exist_ok=True)
    with open(MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(folder_map, f, indent=2, sort_keys=True)
    print(f"component-folder-map.json: {len(folder_map)} components")
    return folder_map


def load_folder_map():
    if not os.path.exists(MAP_PATH):
        return build_folder_map()
    with open(MAP_PATH, encoding="utf-8") as f:
        return json.load(f)


def read_meta(meta_path):
    if not os.path.exists(meta_path):
        return None
    with open(meta_path, encoding="utf-8") as f:
        return json.load(f)


def fetch_one(comp_id, folder_map):
    out_dir = os.path.join(KNOWLEDGE_DIR, "components", comp_id)
    os.makedirs(out_dir, exist_ok=True)
    yaml_path = os.path.join(out_dir, "component.yaml")
    meta_path = os.path.join(out_dir, "component.meta.json")
    old_meta = read_meta(meta_path)

    folder = folder_map.get(comp_id)
    if folder is None:
        if old_meta and old_meta.get("status") == "not_yet_specified":
            return "not_yet_specified (unchanged)"
        write_not_yet_specified(comp_id, meta_path)
        return "not_yet_specified"

    url = f"https://raw.githubusercontent.com/{REPO}/{TAG}/{folder}/Specification/{folder}.yaml"
    raw = _http.get_bytes(url)
    new_sha = hashlib.sha256(raw).hexdigest()
    if old_meta and old_meta.get("source", {}).get("sha256") == new_sha:
        # Content is byte-identical to what's already cached -- spec.md 6.2 says this
        # track "only rewrite[s] files that actually changed"; bumping `retrieved` to
        # today on unchanged bytes would make every refresh cycle dirty every file,
        # defeating task 5.3's "confirm zero files rewritten" check. Fetching was still
        # necessary to know that (no ETag/conditional-GET support in _http.py), but the
        # write itself is skipped.
        return f"{old_meta['status']} (unchanged)"

    with open(yaml_path, "wb") as f:
        f.write(raw)

    spec = yaml.safe_load(raw)
    meta = (spec or {}).get("spec", {}).get("componentMetadata", {})
    envelope = {
        "id": comp_id,
        "type": "component",
        "name": meta.get("name", comp_id),
        "version": str(meta.get("version", "unknown")),
        "status": meta.get("status", "unknown"),
        "source": {
            "origin": url,
            "license": "RAND",
            "retrieved": _dt.date.today().isoformat(),
            "sha256": hashlib.sha256(raw).hexdigest(),
        },
        # Placeholder -- tools/build_index.py's sync_component_links() fills this
        # in on its next run: links.apis (forward, read straight back out of this
        # same component.yaml) and links.use_cases (reverse, from the corpus-wide
        # used_by it already computes) -- spec/spec-components.md 4.
        "links": {"apis": [], "use_cases": []},
    }
    write_json(meta_path, envelope)
    return envelope["status"]


def write_not_yet_specified(comp_id, meta_path):
    envelope = {
        "id": comp_id,
        "type": "component",
        "name": comp_id,
        "version": "none",
        "status": "not_yet_specified",
        "source": {"origin": None, "license": "RAND", "retrieved": _dt.date.today().isoformat()},
        "links": {"apis": [], "use_cases": []},
    }
    write_json(meta_path, envelope)


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def referenced_component_ids():
    """Every TMFCxxx named in links.components across knowledge/use-cases/**/*.md."""
    ids = set()
    for path in glob.glob(os.path.join(KNOWLEDGE_DIR, "use-cases", "**", "*.md"), recursive=True):
        with open(path, encoding="utf-8") as f:
            data, _ = _yaml_lite.split(f.read())
        for c in data.get("links", {}).get("components", []):
            ids.add(c["id"])
    return sorted(ids)


def main():
    args = sys.argv[1:]
    if not args or args == ["--refresh-map"]:
        build_folder_map()
        if not args:
            print("no component ids given -- pass ids, --all-referenced, or --refresh-map")
        return

    folder_map = load_folder_map()
    ids = referenced_component_ids() if args == ["--all-referenced"] else args

    for comp_id in ids:
        try:
            status = fetch_one(comp_id, folder_map)
            print(f"{comp_id}: {status}")
        except _http.FetchError as e:
            print(f"{comp_id}: FETCH FAILED -- {e}")


if __name__ == "__main__":
    main()
