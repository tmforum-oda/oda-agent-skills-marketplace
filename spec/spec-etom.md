# eTOM Business Process Framework — Extension Spec

**Status:** Draft v1
**Owner:** Lester Thomas
**Extends:** [`spec.md`](./spec.md) §5.0 (universal envelope), §5.4 (indexes), §7 (extensibility — `knowledge/etom/` reserved). Read that first. This document fills the one reservation §7 left open for eTOM: `references/eTOM/` now holds a real v26.0 export (added in commit `5ca41a1`), and `knowledge/etom/` is still a `.gitkeep`.

This spec covers **eTOM only**. SID (`GB922`) and the Functional Framework (`GB1033F`) were committed in the same change and have the same source shape (an Excel workbook plus a lossy JSON projection); a `spec-sid.md` should follow this document's pattern rather than re-deriving it.

## 1. The gap this closes

`spec.md` §7 said eTOM would arrive "as a separate, heavier effort … a proposed XMI → structured YAML → Markdown pipeline". That turned out not to be the delivery format. TM Forum published the v26.0 eTOM as:

- `references/eTOM/GB921_Business_Process_Framework_Processes_Excel_v26.0.xlsx` — the full model: one row per process element with `Extended Description`, `Brief Description`, `Domain`, `Vertical Group`, `UID`, and a release/`Issue` tag. Plus an `eTOM Deleted` sheet (562 rows; ~481 real process ids after dropping "deliberately unused" placeholder rows and triplicates) and an `All 26.0 changes` sheet.
- `references/eTOM/etom_v26.0.json` — a **lossy** projection of the workbook's main sheet: `{id, name, token, domain, level}` only, no descriptions, no UID, no vertical group. 3,194 rows, 1:1 with the sheet's data rows.

The skills that would use eTOM already assume this folder is empty and route around it — `skills/decompose-requirement-against-oda/SKILL.md` Step 2 says outright "`knowledge/etom/` is reserved and empty … there is no standalone eTOM corpus to search" and falls back to grepping `componentMetadata.eTOMs` lists across every `component.yaml`. This spec gives those skills a real corpus to read, following the same principles already established for use cases and components: ID-first, provenance-in-envelope, generated-not-hand-authored, absence-is-signal.

## 2. Source of record: the workbook, not the JSON

**Build from `GB921_..._v26.0.xlsx`. Use `etom_v26.0.json` only as a cross-check.** The JSON drops every descriptive field — for an eTOM corpus that *is* the content; a skill needs to know what "1.2.20 Product Catalog Lifecycle Management" means, not just that the id exists. Reasons, all confirmed against the actual files:

| | Workbook (`eTOM26.0` sheet) | JSON (`entries`) |
|---|---|---|
| Extended / Brief description | yes | **dropped** |
| `UID` (stable numeric id) | yes | **dropped** |
| `Vertical Group` | yes | **dropped** |
| Release tag (`Issue`) | yes | **dropped** |
| Domain | yes (538 blank) | yes (538 `null`) |
| Duplicate rows | 166 ids duplicated | 278 rows become exact duplicates once `Vertical Group` is gone |

The workbook needs a real xlsx reader. `openpyxl` is a **new tool dependency** — acceptable: `tools/` already pulls in `python-docx` and `pdfplumber` for the other two source formats, and there is no requirements file to keep minimal. Record it in `tools/` alongside those (see `tasks-etom.md` 0.1).

## 3. Repository layout addition

```
references/
└── eTOM/                                                    # already present (commit 5ca41a1)
    ├── GB921_Business_Process_Framework_Processes_Excel_v26.0.xlsx   # source of record
    └── etom_v26.0.json                                              # secondary, cross-check only

knowledge/
└── etom/
    ├── GB921.md              # NEW — envelope frontmatter + short narrative (§4.1)
    ├── processes.json        # NEW — the corpus: one entry per distinct process element (§4.2)
    ├── deleted.json          # NEW — the eTOM Deleted sheet, so a stale id resolves to "removed" not "unknown" (§4.3)
    ├── AGENTS.md             # REWRITE — currently says "reserved, not populated"
    ├── README.md             # REWRITE
    └── CLAUDE.md             # unchanged (@AGENTS.md)

knowledge/index/
├── etom-anomalies.md         # NEW — generated-once, human-reviewed: upstream data-quality findings (§4.4)
└── etom-index.json           # NEW — by_domain + the eTOM↔component reverse join (§5)
```

The two derived cross-reference / report files live in `knowledge/index/` next to `matrix-discrepancies.md` and the other `*.json` catalogs — that folder is where "what links to what" and "where the source data disagrees with itself" already live, and it is the one tree `validate_envelope.py` skips (so a report with no envelope doesn't trip the gate). The *corpus* (`GB921.md`, `processes.json`, `deleted.json`) lives in `knowledge/etom/`, matching how the use-case and component corpora sit in their own folders while their indexes sit in `index/`.

Delete `knowledge/etom/.gitkeep`. One file per process (2,915 of them) is deliberately **not** the shape — nothing else in the corpus is that granular, and no skill needs a process as an addressable document. The corpus is one JSON array plus a Markdown cover sheet, the same way `knowledge/index/*.json` holds catalogs.

## 4. Data model

### 4.1 `knowledge/etom/GB921.md` — the envelope

Frontmatter follows `spec.md` §5.0 exactly. `type: etom` is a new value — update §5.0's enum (it currently reserves `etom-process`; the corpus-level artefact is `etom`, and if individual processes are ever split into their own files they would be `etom-process`).

```yaml
---
id: GB921
type: etom
name: Business Process Framework (eTOM)
version: v26.0                                          # matches the source workbook / etom_v26.0.json's own "version"
status: Frameworx 26.0 - TM Forum published             # eTOM has no per-process maturity ladder
source:
  origin: <TM Forum Frameworx 26.0 release download — member-gated; --origin fills it at build>
  license: TM Forum (Frameworx / GB921)
  retrieved: 2026-09-08                                 # date the workbook entered references/eTOM/ (commit 5ca41a1)
  sha256: e84dd5272df4cbf8614431cf0ddd0630c823c14d8dd9c0389f9248b2c7b75e06   # the xlsx, computed at build
  raw_path: ../references/eTOM/GB921_Business_Process_Framework_Processes_Excel_v26.0.xlsx
  secondary:
    path: ../references/eTOM/etom_v26.0.json
    sha256: 7c4b736cfa143d275100d0461650694d1a5bc4278a3b8f9104c216176e1ea2f3
links:
  components: []      # reverse-computed into etom-index.json, never written back here (§5.0 principle 7)
---
```

`raw_path` is `../references/...` (relative to `knowledge/`, the same loose convention `docx2md.py` uses for use cases). Both `sha256` values are computed from the files at build time, not hand-entered.

Body: a short (~1 page) orientation — what eTOM is, the domain list with process counts, the level scheme (L1 domain → L2 → … → L7), how the id and `uid` differ, and a pointer to `processes.json` / `etom-index.json` as the things a skill actually queries. Static prose, hand-authored once; the tool does not regenerate it.

### 4.2 `knowledge/etom/processes.json` — the corpus

Flat JSON array, sorted by process id in hierarchical order (`1.1` < `1.1.1` < `1.1.2` < `1.1.10`), one entry per **distinct process element**:

```json
{
  "id": "1.2.20",
  "uid": 3471,
  "name": "Product Catalog Lifecycle Management",
  "level": 2,
  "domain": "Product Domain",
  "domain_inferred": false,
  "vertical_groups": ["Business Value Development"],
  "parent": null,
  "children": ["1.2.20.1", "1.2.20.2", "1.2.20.3"],
  "brief_description": "Catalog Lifecycle Management business process covers a set of business activities that enable manage the lifecycle of an organizations catalog from design to build according to defined requirements.",
  "extended_description": "Catalog Lifecycle Management business process covers a set of business activities …",
  "added_in": null,
  "renamed_from": null
}
```

(`parent` is `null` here because `1.2.20` is Level 2 — its parent is the domain root `1.2` "Product Domain", which is not itself a process row. A Level-3+ process gets its real one-up id.)

Build rules — every one of these is here because the raw data violates it somewhere (§6):

1. **De-duplicate on `id`.** The workbook lists a process once per `Vertical Group` it belongs to (166 ids duplicated, some tripled — e.g. `1.3.4`, `1.3.2`). Collapse to one entry; `vertical_groups` is the sorted union of the `Vertical Group` values across those rows. Empty array when the source cell is blank.
2. **Decode HTML entities** in all text fields: `&amp;` → `&` (82 rows), `&nbsp;` → space (11), numeric `&#…;` (3). The JSON cross-check will not catch these because it inherited them too.
3. **Backfill `domain`** when blank (538 rows — all recent 25.5/26.0 additions: Brand Management `1.1.16.*`, most of Enterprise `1.7.*`, parts of `1.5`/`1.6`). Infer from the id prefix using the prefix→domain map derived from rows that *do* carry a domain (`1.1.* → Market Domain`, `1.7.* → Enterprise Domain`, …). Set `domain_inferred: true` on those entries so a consumer can tell a published fact from a repo-derived one.
4. **`parent` / `children`** computed from the dotted id, not read from any column. `parent` is `null` for L2 (the L1 domain root is not itself a row).
5. **Normalize placeholder descriptions** — `"Not used for this process element"` and empty strings → `null`.
6. **Split trailing change-log text** out of `extended_description`. Several entries append a sentence like *"this process was renamed in 23.5 old name was Market Strategy & Policy"*. Parse `old name was X` → `renamed_from: "X"` where the pattern is clean; otherwise leave the sentence in place (do not drop content on a failed parse).
7. **`added_in`** from the `Issue` column, normalized to a bare version (`"Added in 25.5"` / `"created in 25.5"` / `"Rel 26.0 addition"` → `"25.5"` / `"26.0"`). Four rows (`1.3.2`, `1.7.2`, `1.7.11`, `1.5.21.3.2`) have a full description paragraph in `Issue` instead of a tag — treat as spillover, set `added_in: null`, and log to `etom-anomalies.md`.
8. **Genuine id conflicts** (same id, different `UID`, conflicting domain — e.g. `1.6.1` appears as `Business Partner Domain`/UID 1893 and `null`/UID 4774): keep the row with a non-blank domain, record the discarded `UID` in `etom-anomalies.md`. Never silently merge two different UIDs.

**Cross-check against `etom_v26.0.json`:** after building, every entry's `id`, `name`, `level`, and non-inferred `domain` must equal the JSON's row for that id. Mismatches are a build warning and an `etom-anomalies.md` line, not a silent overwrite in either direction.

### 4.3 `knowledge/etom/deleted.json`

The `eTOM Deleted` sheet, lightly normalized: `{id, uid, name, level, domain, deleted_in, framework_status, brief_description, original_process_identifier}`. Rows whose id is (or contains) `(This Process ID has been deliberately unused!)` are dropped, and duplicate ids collapsed — 562 sheet rows → ~481 records. Purpose: a component whose eTOM mapping names a process id gone from v26 (§6, finding 5) resolves to a real "removed" fact instead of a blank. Note this sheet is **not** a renumbering crosswalk — it is a cumulative historical list of removed process ids, not v26.0-only, and it explains only 2 of the 19 `stale_component_refs`.

### 4.4 `knowledge/index/etom-anomalies.md`

Same role as `knowledge/index/matrix-discrepancies.md`: a generated list of upstream data-quality findings, reviewed by a human once per refresh, kept in git so the disagreement is visible rather than silently resolved. `build_etom.py` writes it, regenerating it in full on every build. A "Build summary" header (row counts, de-dup count, inferred-domain count) then one `## section (N)` per finding category: duplicated ids; conflicting-UID ids; one UID shared by distinct ids; orphaned processes (parent row absent); description text in the `Issue` column; unrecognized `Issue` tags; ids on the Deleted sheet that are also live; `etom_v26.0.json` cross-check mismatches.

## 5. Index addition — `knowledge/index/etom-index.json`

The join that makes eTOM useful to the consumer skills. Built by `tools/build_etom_index.py`, which `build_index.py` calls at the end of its own run (so one `build_index.py` regenerates all four index files). Idempotent, sorted keys.

```json
{
  "summary": {
    "components_with_etom_mappings": 19,
    "processes_with_an_implementer": 144,
    "stale_component_refs": 19,
    "unresolvable_component_refs": 4,
    "by_resolution": { "deleted": 2, "name_matched": 15, "not_in_v26": 2 }
  },
  "by_domain": { "Product Domain": ["1.2.1", "1.2.1.1", "..."], "...": [] },
  "implemented_by": {
    "1.2.20": ["TMFC001"],
    "1.3.3":  ["TMFC002", "TMFC003"]
  },
  "stale_component_refs": [
    { "etom_id": "1.1.19", "etom_name": "Loyalty_Program_Management",
      "components": ["TMFC001", "TMFC005"], "component_etom_versions": ["v24.0"],
      "resolution": "not_in_v26", "resolved_to": null },
    { "etom_id": "1.1.19.1", "etom_name": "Loyalty_Program_Development_&_Retirement",
      "components": ["TMFC001"], "component_etom_versions": ["v24.0"],
      "resolution": "name_matched", "resolved_to": "1.3.4.5.1" }
  ]
}
```

- **`by_domain`** — every process id in `processes.json`, grouped by domain, hierarchically sorted. A convenience filter; no new data.
- **`implemented_by`** — reverse of every `component.yaml`'s `spec.componentMetadata.eTOMs` (pipe-delimited `id|Name|vXX.0`, the version being the eTOM release the mapping was authored against — v21.5–v25.0 across the current corpus). This is what turns "if we change eTOM 1.2.20, which components care?" into a lookup.
- **`stale_component_refs`** — the honest part. Components map to eTOM v21.5–v25.0 and eTOM was renumbered for 25.5/26.0, so some referenced ids no longer exist at their old number. **Measured against the real `spec.componentMetadata.eTOMs` data: 19 components carry a mapping, 148 distinct eTOM ids referenced, 129 still resolve by id, 15 more resolve by exact name match (renumbered — mostly the Sales `1.1.x → 1.12.x` and Loyalty `1.1.19.x → 1.3.4.5.x` moves), 2 are on the Deleted sheet, and only 2 are genuinely unresolvable** (`1.1.19` and `1.1.7` — parent nodes whose whole subtree was reorganized). Every reference that doesn't resolve by id is listed here — even the `name_matched` ones, which *are* folded into `implemented_by` but stay flagged so a consumer can see the id changed — with `resolution` one of `name_matched` / `deleted_in_<rel>` / `not_in_v26` / `malformed`. A skill reading `implemented_by` should still say it is "the join TM Forum's own data supports", not "complete"; `spec.md`'s report-both-versions-don't-reconcile rule (§5.0) applies — don't rewrite the components' version-stamped refs.

## 6. Findings from the raw data (the reason each build rule exists)

Confirmed directly against the two files, 2026-09-08:

1. **The JSON is lossy** — 5 of the workbook's 9 columns kept; all description text discarded. → §2: build from xlsx.
2. **166 duplicated process ids** in the workbook (some tripled), driven by multi-valued `Vertical Group`; in the JSON these are 278 exact-duplicate rows with no distinguishing field left. → §4.2 rule 1.
3. **538 blank domains** — every one a 25.5/26.0 addition. → §4.2 rule 3.
4. **HTML entities not decoded** in description text (`&amp;` ×82, `&nbsp;` ×11, `&#…;` ×3); process *name* cells are clean. The `’` that renders as `�` in a Windows console is a correct U+2019 in the file — not corruption, don't "fix" it. → §4.2 rule 2.
5. **eTOM↔component join has real but modest version drift** — of 148 distinct eTOM ids referenced by cached components (mapped against eTOM v21.5–v25.0), 129 resolve directly in v26.0, 15 resolve by exact name after renumbering, 4 don't resolve. No crosswalk exists in the export; name-matching is the only bridge. → §5 `stale_component_refs`. *(An earlier draft of this spec put the failure at ~68%; that was a regex over raw `component.yaml` text that also swept up the pipe-delimited `functionalFrameworkFunctions` entries — a proper YAML parse of `spec.componentMetadata.eTOMs` gives the numbers above.)*
6. **`Issue` column misused** — 4 rows carry a description paragraph instead of a release tag; the `All 26.0 changes` sheet has every row doubled. → §4.2 rule 7, §4.4.
7. **`1.6.1` and other ids appear twice with different UIDs** and conflicting domain. → §4.2 rule 8.
8. **Change-log prose mixed into `Extended Description`** ("renamed in 23.5 …"). → §4.2 rule 6.

Findings 2, 3, 6, 7 are upstream TM Forum data-quality issues worth reporting back to the eTOM team; `etom-anomalies.md` is the artefact that makes them a tracked fact rather than a lost observation. The build pipeline defends against them regardless.

## 7. Refresh

eTOM ships with TM Forum's **Frameworx release train (~2×/year)**, not IG1228's 8-week cadence. The workbook is member-gated (same access tier as `spec.md` §6.1 / IG1228), so this is the **assisted track**:

1. A member checks the TM Forum Frameworx / GB921 catalog page for a new version, downloads the `.xlsx` (and the `.json` if still published) into `references/eTOM/`, replacing the old files.
2. `python tools/build_etom.py` — regenerates `knowledge/etom/processes.json`, `deleted.json`, `knowledge/index/etom-anomalies.md`, and the `version`/`source` block of `GB921.md` (not its narrative body).
3. `python tools/build_index.py` — regenerates `etom-index.json` (and the rest).
4. `python tools/validate_envelope.py --strict` — gate.
5. `python tools/refresh_report.py` — `CHANGELOG.md` entry; must surface process add/remove/rename counts and any new `etom-anomalies.md` lines.
6. Review `etom-anomalies.md` by hand; if the eTOM↔component resolution rate moved sharply, note why in the changelog.

Add the download step to `spec/refresh-runbook.md` next to the IG1228 steps. `build_etom.py` and `build_index.py` must be idempotent — byte-identical output on a re-run with no input change (`spec.md` §9).

## 8. Consumption — what changes for skills

Not built here, but the layout is validated against these:

- **`decompose-requirement-against-oda`** Step 2 — replace the "reserved and empty" fallback with a real search over `processes.json` (`name` / `brief_description` word overlap against the requirement), citing `id · name · uid`. Keep the per-component `componentMetadata.eTOMs` read as a secondary signal, and keep "an empty candidate list is a valid finding".
- **`assess-change-impact`** — extend from components/APIs to eTOM: given an `etom_id`, `etom-index.json`'s `implemented_by` gives the affected components, then the existing component→use-case reverse index chains the rest. Must state the `stale_component_refs` caveat in the report.
- **`recommend-oda-components-for-requirement`** — an eTOM process match is another route to a component shortlist via `implemented_by`.
- A future **`explain-etom-process`** — the simplest possible skill (mirrors `check-usecase-maturity`): id in, `processes.json` entry out in plain language, including `added_in` / `renamed_from` / whether any component implements it.

Update `knowledge/etom/{AGENTS,README}.md`, `knowledge/AGENTS.md` + `knowledge/README.md` subfolder tables, and `knowledge/index/id-registry.md` (`GB921` is no longer reserved). Mark `spec.md` §7's eTOM bullet done and add `etom` to the §5.0 type enum.

## 9. Open questions

1. **Narrative body of `GB921.md`** — hand-authored once (this spec's assumption) vs. generated domain-summary tables. Recommend hand-authored: it is orientation, not data, and regenerating prose invites churn.
2. **`processes.json` size** — ~2,915 entries with full `extended_description` will be a multi-MB file. Acceptable for a grep/`jq`-style read; if a skill needs random access by id, add a slim `processes-lite.json` (`id`, `name`, `level`, `domain`, `parent`) rather than splitting into per-process files. Decide when a skill actually hits the limit, not now.
3. **SID / Functional Framework** — same source shape, same lossy-JSON problem. Confirm they follow this spec's pattern (`spec-sid.md`, `build_sid.py`) before generalizing `build_etom.py` into a shared workbook reader — one concrete second case first.
