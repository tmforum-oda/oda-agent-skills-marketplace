# knowledge/etom/ — Agent Instructions

The agent-facing view of TM Forum's **Business Process Framework (eTOM)**,
`GB921`, v26.0. Generated from the Excel export in `references/eTOM/` by
[`tools/build_etom.py`](../../tools/build_etom.py); the component↔process join
in `../index/etom-index.json` by [`tools/build_etom_index.py`](../../tools/build_etom_index.py).
Full design rationale: [`spec/spec-etom.md`](../../spec/spec-etom.md).

## What's here

| File | Read it for |
|---|---|
| `GB921.md` | the envelope (`version`, `source`, provenance) + a prose orientation to eTOM. Static body — the tool regenerates only the frontmatter. |
| `processes.json` | **the corpus.** Flat array, 2,915 distinct process elements, hierarchically sorted. One entry per id with `uid`, `name`, `level`, `domain`, `domain_inferred`, `vertical_groups`, `parent`, `children`, `brief_description`, `extended_description`, `added_in`, `renamed_from`. |
| `deleted.json` | process ids removed at some point in eTOM's history (cumulative, not v26.0-only). Use it to resolve an id that isn't in `processes.json`. |
| `../index/etom-index.json` | `by_domain` (ids per domain); `implemented_by` (eTOM process id → ODA component ids); `stale_component_refs` (component eTOM mappings that don't resolve cleanly against v26.0). |
| `../index/etom-anomalies.md` | data-quality findings in the raw export — read before treating an oddity as a bug in the pipeline. |

## Rules specific to this corpus

1. **Identifier depth is one more than the level.** `1.1.1` is a **Level 2**
   process; `1.1.1.1` is Level 3. `parent` is `null` at Level 2 (its parent
   is the domain root, e.g. `1.1`, which is not a process row). Don't derive
   the level by counting dots — read the `level` field.
2. **`uid` is eTOM's own stable numeric key** and survives renumbering better
   than the dotted id. It is **not unique** in this export (one confirmed
   collision — see `etom-anomalies.md`); don't assume `uid` → one process.
3. **`domain_inferred: true`** means the workbook left `Domain` blank and the
   tool filled it from the process hierarchy (true for every 25.5/26.0
   addition). Treat it as a repo-derived best guess, not a published fact.
4. **Absence is signal.** An id not in `processes.json` is genuinely not in
   eTOM 26.0. Check `deleted.json` before calling it unknown. Never fabricate
   a process description, name, or id to fill a gap — say the id isn't in the
   corpus.
5. **The eTOM↔component join is version-drifted, not authoritative.**
   Components map their processes against eTOM v21.5–v25.0; this corpus is
   v26.0, which renumbered a chunk of the tree. `implemented_by` folds in
   both direct-id and exact-name-match resolutions; `stale_component_refs`
   lists every reference that didn't resolve by id (including the
   name-matched ones, still flagged). Report it as "the join the data
   supports", not "complete", and **never rewrite a component's
   version-stamped eTOM reference** to make it line up (`spec.md` §5.0).
6. **Generated output — don't hand-edit** `processes.json`, `deleted.json`,
   `etom-index.json`, or `etom-anomalies.md`; re-run the tool. `GB921.md`'s
   prose body is the one hand-maintained exception (it lives as
   `DEFAULT_BODY` in `build_etom.py` and is preserved across runs).

## If you need a component's eTOM activities and nothing else

They're also inline in that component's own record —
`spec.componentMetadata.eTOMs` in `../components/{TMFCxxx}/component.yaml`
(`{id}|{Name}|v{rel}`), and a `TMFCxxx.md` §2.1 table where a narrative PDF
exists. `../index/etom-index.json`'s `implemented_by` is the pre-computed
reverse of exactly that data.
