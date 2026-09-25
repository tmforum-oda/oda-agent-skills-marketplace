# knowledge/etom/

The agent-facing view of TM Forum's **Business Process Framework (eTOM)** —
guidebook `GB921`, version 26.0. Generated from the Excel export under
[`../../references/eTOM/`](../../references/eTOM/) by
[`tools/build_etom.py`](../../tools/build_etom.py).

If you're an AI agent, read [`AGENTS.md`](AGENTS.md) here first.

## Contents

| File | |
|---|---|
| `GB921.md` | provenance envelope + a one-page orientation to eTOM |
| `processes.json` | the corpus — 2,915 process elements, one entry each (`id`, `uid`, `name`, `level`, `domain`, `parent`, `children`, brief + extended description, `added_in`, `renamed_from`) |
| `deleted.json` | ~481 process ids removed over eTOM's history — so a stale id resolves to "removed" rather than "unknown" |

Two derived files live in [`../index/`](../index/) alongside the other
cross-reference catalogs:

| File | |
|---|---|
| `etom-index.json` | `by_domain`, plus the eTOM-process → ODA-component join (`implemented_by`) and the component references that don't resolve against v26.0 (`stale_component_refs`) |
| `etom-anomalies.md` | data-quality findings in the raw TM Forum export, reviewed once per refresh |

## Where it comes from

`references/eTOM/GB921_..._v26.0.xlsx` is the source of record;
`references/eTOM/etom_v26.0.json` is a lossy secondary file used only to
cross-check the extraction. eTOM ships with TM Forum's Frameworx release
(~2×/year, member-gated), not IG1228's 8-week cadence — see the root
[`README.md`](../../README.md#running-a-refresh) and
[`spec/spec-etom.md`](../../spec/spec-etom.md) §7 for the refresh steps.

## A note on the eTOM↔component join

ODA Components map their eTOM activities against whatever eTOM release was
current when the mapping was authored (v21.5–v25.0 across today's corpus).
eTOM 26.0 renumbered part of the tree, so `implemented_by` resolves each
component reference as far as the data honestly allows (direct id, then exact
name match) and `stale_component_refs` records every one that didn't resolve
by id. It is an honest partial join, not an authority — see `AGENTS.md` rule 5.
