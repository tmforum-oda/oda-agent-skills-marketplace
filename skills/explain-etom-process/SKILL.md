---
name: explain-etom-process
description: Given a TM Forum eTOM (Business Process Framework / GB921) process id such as 1.2.20 or GB921:1.2.20, reads the cached process record and returns a plain-language explanation -- what the process is, where it sits in the hierarchy, whether it was added or renamed recently, and which ODA Components implement it. Reads only knowledge/etom/, no document-body parsing. Use this to understand a single eTOM process id you've encountered in a component spec, a use case, or a design.
---

# Explain eTOM Process — Skill Instructions

## What this skill answers

"What is eTOM process `1.2.20`, and who implements it?" — a short verdict
from the cached eTOM corpus, not a raw JSON dump. The eTOM counterpart to
`check-usecase-maturity`: one id in, one grounded explanation out, zero
prose parsing.

## Where the data lives

Everything this skill needs is in three files — no directory scan, no
search, no network:

```
knowledge/etom/processes.json        -- the corpus, one entry per process id
knowledge/etom/deleted.json          -- process ids removed over eTOM's history
knowledge/index/etom-index.json      -- implemented_by + stale_component_refs
```

Accept the id as `1.2.20` or `GB921:1.2.20` (strip a `GB921:` prefix if
present). eTOM ids are dotted-numeric; the leading digit is the framework
root, so **`level` is one less than the dotted-id depth is not a thing to
compute** — read the `level` field.

## Step 1 — Find the process in `processes.json`

`processes.json` is a flat array; find the entry whose `id` matches
exactly. Its fields:

| Field | Use it for |
|---|---|
| `name`, `level`, `domain` | the one-line identity |
| `domain_inferred` | if `true`, the domain was back-filled by the build from the id hierarchy (the source left it blank — every 25.5/26.0 addition). Say "domain (inferred)" in the verdict, not a bare domain. |
| `parent`, `children` | where it sits — `parent: null` means it's a Level-2 process directly under a domain |
| `brief_description`, `extended_description` | the explanation itself. `extended_description` can be `null` (the source had only a placeholder) — fall back to `brief_description` and say the extended one isn't published. |
| `added_in` | `"25.5"` / `"26.0"` if this process is new in that release, else `null` |
| `renamed_from` | the process's previous name if it was renamed, else `null` |
| `uid` | eTOM's own stable numeric key — cite it, but note it is **not unique** in the export (don't present it as a second lookup key) |

## Step 2 — If it's not in `processes.json`, check `deleted.json`

An id absent from `processes.json` is genuinely not in eTOM 26.0 — do not
fabricate a description for it. Look it up in `deleted.json`:

- **Found** → report it as a removed process: its `name`, `framework_status`,
  `deleted_in` (may be `null` — the sheet is a cumulative historical list,
  not all one release), and `original_process_identifier` if set. Say
  plainly that it is not part of the current framework.
- **Not found there either** → before concluding, check
  `knowledge/index/etom-index.json`'s `stale_component_refs` for an entry
  whose `etom_id` equals this id. If one exists, the id is gone from v26.0
  but one or more ODA Components still reference it — report that
  (`"1.1.19 is not a v26.0 process; TMFC001 and TMFC005 still map it,
  unresolved (resolution: not_in_v26)"`), and point at
  `knowledge/index/etom-anomalies.md`. If there's no stale ref either, say
  plainly the id isn't in the eTOM 26.0 corpus at all — not a live
  process, not a recorded deletion, not referenced by any cached
  component. Either way, stop here; there is nothing more to say about an
  id the corpus doesn't contain.

## Step 3 — Which ODA Components implement it

Read `knowledge/index/etom-index.json`:

- **`implemented_by[<id>]`** — a sorted list of `TMFCxxx` ids whose
  `component.yaml` maps this process. Empty / absent is a real, valid
  answer: "no cached ODA Component currently maps this activity."
- **`stale_component_refs`** — scan for any entry whose `resolved_to`
  equals this id. That means a component references the process under its
  *old* number (`etom_id`) and this skill's id is where it landed after
  renumbering. Report it: "TMFC0xx maps this activity under its pre-26.0
  id `1.1.x` (`resolution: name_matched`)." Also scan for an entry whose
  `etom_id` equals the queried id with `resolution` `not_in_v26` /
  `deleted` — that means a component still points at this id but it no
  longer resolves; worth stating.

Do not read `component.yaml` files directly — `etom-index.json` is the
pre-computed reverse of exactly that data. State that the eTOM↔component
join reflects mappings authored against eTOM v21.5–v25.0 against a v26.0
corpus, so it is "the join the data supports," not a guarantee of
completeness.

## Output format

A short explanation, not a field dump. Example, for `1.2.20`:

> **eTOM 1.2.20 — Product Catalog Lifecycle Management** (Level 2, Product
> Domain, uid 3471). A set of business activities that manage the lifecycle
> of an organisation's catalog from design to build against defined
> requirements. Sits directly under the Product Domain; has 3 child
> processes (`1.2.20.1`–`1.2.20.3`). Not flagged as new or renamed in a
> recent release.
>
> **Implemented by:** TMFC001 (Product Catalog Management).

Example, for a renamed process:

> **eTOM 1.12.9 — Selling** (Level 3, Sales Domain, uid …). … Renamed —
> previously "Sales Opportunity Handling" (`renamed_from`). Also note:
> ODA Components TMFC002 and TMFC036 map this activity under its pre-26.0
> id `1.1.9` (`name_matched` in `etom-index.json`).

Always cite the id, `name`, `level`, `domain` (marked inferred where it
is), and `uid` verbatim, plus `added_in` / `renamed_from` when non-null,
so the reader can see the raw fields behind the explanation.

## What this skill does NOT do

- Does not search `processes.json` by name or keyword — that's
  `decompose-requirement-against-oda` Step 2's job. This skill takes a
  known id and explains it.
- Does not walk the process tree (list a whole subtree, trace all
  ancestors) — it reports the immediate `parent` and the `children` list /
  count, nothing deeper.
- Does not fabricate a name, description, level, or domain for an id the
  corpus doesn't contain — an "id not in the corpus" answer is the correct
  output, per Step 2.
- Does not read `component.yaml` files, use-case documents, or query TM
  Forum's website — `knowledge/etom/` and `knowledge/index/etom-index.json`
  are sufficient, and a skill must answer without a network call.
- Does not rewrite or reconcile a component's version-stamped eTOM
  reference against v26.0 — it reports the drift (`stale_component_refs`),
  it doesn't fix it.
