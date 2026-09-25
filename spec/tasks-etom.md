# eTOM Corpus — Build Tasks

Companion to [`spec-etom.md`](./spec-etom.md), the same way [`tasks.md`](./tasks.md) is companion to `spec.md`. Check off as completed; leave notes inline where a task surfaces a decision or a bug, the convention `tasks.md` uses throughout.

**Starting state:** `references/eTOM/` holds the v26.0 `.xlsx` + `.json` (commit `5ca41a1`). `knowledge/etom/` is a `.gitkeep` plus three "reserved, not populated" docs. Nothing consumes eTOM yet — `skills/decompose-requirement-against-oda` routes around the empty folder on purpose.

**Do Phase 1 (build the corpus) and Phase 2 (the index join) before touching any skill.** The skill changes in Phase 4 depend on `processes.json` and `etom-index.json` existing and being trusted.

---

## Phase 0 — Tooling

- [x] **0.1** Added `tools/requirements.txt` (`PyYAML`, `python-docx`, `pdfplumber`, `openpyxl`), each line annotated with the tool that imports it — the repo had no dependency manifest at all before this. `import openpyxl` confirmed working (Python 3.13, this environment).
- [x] **0.2** Wrote `tools/build_etom.py` — see its docstring for the full rule list. Two deviations from this task's original sketch, both deliberate:
  - **`etom-anomalies.md` lands in `knowledge/index/`, not `knowledge/etom/`.** It's a report, not an artefact (no envelope), so it belongs next to `matrix-discrepancies.md` — and `knowledge/index/` is the one tree `validate_envelope.py` already skips, so a frontmatter-less `.md` there doesn't trip the strict gate. `spec-etom.md` §3/§4.4 updated to match.
  - **`build_etom.py` writes the *whole* `GB921.md`, not just the `version`+`source` block** — it emits the full frontmatter deterministically via `_yaml_lite` and preserves whatever body is on disk (seeding `DEFAULT_BODY` only when the file doesn't exist yet). Same net effect (body is hand-owned, frontmatter is generated), simpler and more obviously idempotent than a surgical in-place block rewrite.
  - `source.sha256` (xlsx) and `source.secondary.sha256` (json) are computed from the files at run time, not hand-pasted. `--origin` / `--retrieved` are CLI flags; `source.origin` currently carries a `TODO:` string (no public URL for a member-gated Frameworx download — 1.1).
- [x] **0.3** `validate_envelope.py` needed **no change**. `knowledge/etom/GB921.md` passes the five-field check as-is (`id/type/name/version/status` all present); `processes.json`/`deleted.json` are plain `.json` (not `.meta.json`) so they're ignored; `etom-anomalies.md` sits under `knowledge/index/` which is already excluded. `python tools/validate_envelope.py --strict knowledge` → **132 artefacts, 0 failures, 0 TODO stubs**.

## Phase 1 — Build the corpus

- [x] **1.1** `GB921.md` body authored — it lives as `DEFAULT_BODY` in `build_etom.py` (seeded on first run, preserved thereafter), which keeps the "hand-authored orientation" text in version control and the tool self-contained. Covers what eTOM is, the file map, id-vs-level (`1.1.1` is Level 2), `uid`, the 8 domains + `domain_inferred`, and the "absence is signal" / v24→v26 renumbering caveat. `source.origin` is a marked `TODO:` — a real member-download URL isn't known; fill via `--origin` on a future refresh.
- [x] **1.2** Ran `build_etom.py`. Actuals vs. the rough estimate: **2,915** distinct process ids from **3,194** rows (166 duplicated ids collapsed — matches); **511** distinct ids with a back-filled domain (`domain_inferred: true`) — the 538 blank *rows* estimate was pre-dedup; **481** records in `deleted.json` (from 562 sheet rows — 46 "(This Process ID has been deliberately unused!)" placeholder rows and a batch of triplicated `1.5.7.*` / duplicate ids dropped); **53** `renamed_from` extracted; **94** ids tagged `added_in` (`25.5` / `26.0`). All 8 domains present, **zero** null domains in the output, levels 2–7.
- [x] **1.3** Reviewed `knowledge/index/etom-anomalies.md` (204 findings, 6 non-empty categories). Confirmed:
  - **JSON cross-check: 0 mismatches** — `etom_v26.0.json` is a faithful (if lossy) projection; every id/name/level/domain we kept agrees with it.
  - The 4 `Issue`-column description-spillover ids (`1.3.2`, `1.5.21.3.2`, `1.7.2`, `1.7.11`) — all flagged, `added_in` correctly `null` for them.
  - `1.6.1` conflicting-UID case flagged (`[1893, 4774]`, kept 1893 — the row carrying a Domain).
  - **New finding not in the spec:** UID **3892** is shared by two distinct processes (`1.2.27.1.2`, `1.3.3.11.1`) — a real UID collision in the source. Logged under its own category.
  - **New finding:** 5 orphaned processes under `1.7.2.*` (Enterprise Risk) whose Level-3 parent rows are absent from the sheet; 27 ids appear on the Deleted sheet *and* as live v26.0 processes (Enterprise Risk/Security renumbering churn). Both logged.
  - One residual placeholder leak (`1.3.7.1.3` — real description text with "Not used for this process element" tacked on the end); left as-is, the description is still useful.
- [x] **1.4** Idempotence confirmed — ran `build_etom.py` twice, `diff`'d `processes.json`, `deleted.json`, `GB921.md`, `etom-anomalies.md`: all four byte-identical on the re-run.

## Phase 2 — The index join

- [x] **2.1** Wrote `tools/build_etom_index.py` (standalone, importable). `build_index.py` calls `build_etom_index.main()` at the end of its own run — so one `python tools/build_index.py` regenerates all four index files. `build_etom_index` no-ops with a message if `knowledge/etom/processes.json` isn't there yet (fresh clone mid-migration). Emits `summary`, `by_domain` (all 2,915 ids grouped by domain, hierarchically sorted), `implemented_by`, `stale_component_refs`.
  - **The eTOMs live at `spec.componentMetadata.eTOMs`, not top-level `componentMetadata.eTOMs`** — matters for the YAML path. `functionalFrameworkFunctions` sits right next to it and is *also* pipe-delimited, which is what polluted Phase 1's raw-regex "408 distinct ids / 279 stale" estimate.
- [x] **2.2** Resolution pass built. Real numbers (proper YAML parse of 26 `component.yaml`): **19 components** carry an eTOM mapping, **148 distinct eTOM ids** referenced (mapped against eTOM v21.5–v25.0), classified:
  - `in_v26` (129) — id still exists → `implemented_by`
  - `name_matched` (15) — id gone, exact normalized name (`_`→space, strip non-alphanumerics, lowercase) resolves to exactly one v26 process → folded into `implemented_by`, also listed in `stale_component_refs` with `resolved_to`. Almost all are the Sales `1.1.x → 1.12.x` and Loyalty `1.1.19.x → 1.3.4.5.x` renumberings.
  - `deleted` (2) — `1.5.6` / `1.5.6.7` Resource Provisioning, on the Deleted sheet
  - `not_in_v26` (2) — `1.1.19` (Loyalty Program Management) and `1.1.7` (Market Sales Support & Readiness): parent nodes whose whole subtree was reorganized, no single name match
  - `malformed` (0) — the "bare `1026`" the spec worried about doesn't exist once you parse the YAML properly

  Net: **144 of 148** referenced ids resolve to a v26 process. `spec-etom.md` §5/§6 rewritten with these numbers (the ~68%-broken claim was the regex artefact).
- [x] **2.3** Idempotence confirmed — ran `build_etom.py` + `build_index.py` twice, `diff`'d `processes.json`, `deleted.json`, `GB921.md`, `etom-anomalies.md`, `etom-index.json`, `components.json`: all byte-identical.
- [x] **2.4** Round-trip check passed — every one of the 7 eTOM ids in `TMFC001.md` §2.1's table (`1.2.7`, `1.2.19`–`1.2.23`, `1.6.4`) resolves: `implemented_by[id]` contains `TMFC001`. TMFC001's full `implemented_by` footprint is 11 ids, incl. `1.3.4.5.1` reached by name-match from its stale `1.1.19.1` ref. 4 processes have >1 implementing component (e.g. `1.4.5` ← TMFC003/007/009).

## Phase 3 — Documentation

- [x] **3.1** Rewrote `knowledge/etom/AGENTS.md` and `README.md` from scratch — file map, the six corpus-specific rules (id-depth vs level, non-unique `uid`, `domain_inferred`, absence-is-signal, the join-is-drifted caveat, don't-hand-edit), and a pointer to the inline `component.yaml` data for anyone who only needs one component's activities. `CLAUDE.md` unchanged. `.gitkeep` was already removed in Phase 1.
- [x] **3.2** Updated the subfolder tables in `knowledge/AGENTS.md` and `knowledge/README.md` — `etom/` now reads as populated (v26.0, 2,915 processes).
- [x] **3.3** `knowledge/index/id-registry.md` — `GB921` row now points at `knowledge/etom/` (spec-etom.md); `GB922`/SID still reserved. Same edit applied to the mirror table in `spec/spec.md` §4.1.
- [x] **3.4** `spec/spec.md` — added `etom` to the §5.0 `type` enum (`etom-process` still reserved); §7's eTOM bullet struck through and replaced with a "now built, shipped as Excel not XMI" note pointing at `spec-etom.md`; SID half left reserved.
- [x] **3.5** Added section **6a** to `spec/refresh-runbook.md` — check the Frameworx/`GB921` catalog page, drop the new `.xlsx` into `references/eTOM/`, `build_etom.py --retrieved <date>` → `build_index.py` → review `etom-anomalies.md`. Notes that the v26.0 filenames are hard-coded in `build_etom.py` and must be bumped by hand on a version change.
- [x] **3.6** Extended `tools/refresh_report.py` with a `format_etom_section()` — diffs `knowledge/etom/processes.json` by id (watching `name`/`level`/`domain`/`renamed_from`, capped at 15 lines each way since a Frameworx bump moves hundreds at once) and surfaces `etom-index.json`'s `summary` deltas (`processes_with_an_implementer`, `stale_component_refs`, `unresolvable_component_refs`). Verified against the from-scratch state (reports all 2,915 as added + the three summary numbers). The test-run `CHANGELOG.md` it produced was deleted — no real refresh cycle has landed yet, matching `spec.md` §9.

## Phase 4 — Skill wiring (after Phases 1–2 are trusted)

- [x] **4.1** `skills/decompose-requirement-against-oda/SKILL.md` Step 2 rewritten — now a bounded relevance scan of `knowledge/etom/processes.json` (`name` / `brief_description` overlap, favour Level 2–4), citing `id · name` + `uid`, with `etom-index.json` `implemented_by` as a **secondary** signal feeding Step 3's component list. `candidate_processes` output shape changed from a bare pipe-string to `{id, name, level, implemented_by}`. "Empty list is a valid finding" kept. The two "reserved and empty / can't do this" notes (Step 2 body + the What-it-does-NOT-do bullet) updated; the SID half of Step 4 still correctly says `knowledge/sid/` is reserved.
- [x] **4.2** `skills/assess-change-impact/SKILL.md` — new **Step 0**: a dotted-numeric / `GB921:` id is an eTOM process → confirm in `processes.json` (or report it removed via `deleted.json`) → `etom-index.json` `implemented_by` (+ `stale_component_refs` where `resolved_to` matches) → run Steps 1–4 once per implementing component, union the affected use cases. Empty `implemented_by` is reported as "no component maps this, so no use-case dependency through the corpus" — not a clean bill of health. Output format gains an eTOM example + a mandatory eTOM-join caveat; `description` and two NOT-do bullets updated. Walked through for `1.4.5` (Service Activation Management) → TMFC003/007/009 → union of 15 use cases with source tags.
- [x] **4.3** `skills/recommend-oda-components-for-requirement/SKILL.md` Step 3 — added a "Secondary cross-check via eTOM" paragraph: scan `processes.json` by name, follow `implemented_by`, use it only to corroborate or widen the Step 1 list, never replace it. Fits the existing shape cleanly (it's the same corroboration role the matrix already plays for components), so done rather than deferred.
- [x] **4.4** Repo-wide sweep done. Fixed: `spec/spec.md` §4 layout tree (`etom/ RESERVED` → populated) + index/tools tree entries; `spec/spec-skills-consumer.md` §6 `oda-architecture-navigator` row (No → "Partially — eTOM half now buildable"); `spec/spec-ontology.md` §8.3 revisit-trigger (data half now met, skill half not). `skills/process-component-media` and `skills/propose-component-or-api-extension` mention eTOM only in the diagram/field-list sense — not stale, left alone. Historical mentions in `spec-etom.md` / `tasks-etom.md` describe the starting state and are correct as written.

## Phase 5 — New skill (mirrors `check-usecase-maturity`)

- [x] **5.1** Created `skills/explain-etom-process/SKILL.md` — one eTOM id in, a grounded explanation out. Single-file reads of `processes.json` / `deleted.json` / `etom-index.json`, zero prose parsing. Handles: live process (name/level/domain+`domain_inferred`/uid/parent/children/`added_in`/`renamed_from` + `implemented_by`); deleted process (from `deleted.json`, "not part of the current framework"); absent-but-stale-referenced (scan `stale_component_refs` for `etom_id ==` the query before concluding "not in corpus"). Classified into `CONSUMER_SKILLS` in `build_plugin.py` (+ `SKILL_EXAMPLES` entry) so the packager doesn't fail on an unclassified skill; added to the root `README.md` Consumer table.
- [x] **5.2** Walked through against `1.4.5` / `1.4.5.6` (live, not touched during the build) → full record + `implemented_by` of 3 / 2 components; `1.5.6` (`deleted.json` only) → "removed process, original id 1.1.3.2", no fabricated description; `1.1.19` (in neither file) → reported via its `stale_component_refs` entry (TMFC001/TMFC005 map it under the pre-26.0 id, `not_in_v26`); `9.9.9` → "not in the corpus at all". All four behave as the SKILL.md specifies.

## Phase 6 — Distribution refresh

- [x] **6.1** Ran `python tools/build_plugin.py` — regenerated `dist/consumer/` + `dist/creator/`. The diff was small and clean (27 files, mirroring exactly the `knowledge/` + `skills/` changes: eTOM corpus files, `explain-etom-process`, rewritten AGENTS/README, `.gitkeep` removed), not the feared ~3k — most of `knowledge/` was already vendored and unchanged. Verified idempotent (3 runs, stable). Committed together with the rest of the eTOM work.
