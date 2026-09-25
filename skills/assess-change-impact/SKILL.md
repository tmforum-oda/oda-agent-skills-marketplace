---
name: assess-change-impact
description: Given a TM Forum ODA component (TMFCxxx), Open API (TMFxxx), or eTOM process (GB921 id such as 1.2.20) and a proposed change (deprecation, breaking version bump, removal), lists every TMFSxxx use case that depends on it, describes specifically how each one uses it, and drafts a maturity-weighted migration/impact report. Use this before deprecating, breaking, or removing a component, API, or eTOM process.
---

# Assess Change Impact — Skill Instructions

## What this skill answers

"If we change TMFC020 (or TMF632, or eTOM process 1.2.20, or a specific
version of an API), which use cases break, how exactly do they depend on
it, and how risky is that?"

## Step 0 — If the id is an eTOM process, resolve it to components first

A dotted-numeric id (`1.2.20`, optionally written `GB921:1.2.20`) is an
**eTOM process**, not a component or API. eTOM processes don't link to use
cases directly — they link through the ODA Components that implement them.

1. Confirm it in `knowledge/etom/processes.json` (an id not there isn't a
   v26.0 process — check `knowledge/etom/deleted.json`, and if it's gone,
   say so and stop; `explain-etom-process` is the skill for that lookup).
2. Read `knowledge/index/etom-index.json` → `implemented_by[<id>]` for the
   list of `TMFCxxx` ids that map this process. Also check
   `stale_component_refs` for entries whose `resolved_to` is this id — a
   component reaching it by renumbered name still counts as a dependent.
3. If `implemented_by` is empty, the report is short: **no cached ODA
   Component maps this eTOM activity, so no use case depends on it through
   the corpus.** Say that plainly rather than reporting zero impact as if
   it were a clean bill of health — it may just mean the mapping isn't
   filled in.
4. Otherwise, run Steps 1–4 below **once per implementing component**, then
   combine: the affected use cases are the union across all of them. The
   report must carry the eTOM caveat (see Output format) — the
   eTOM↔component join is built from mappings authored against eTOM
   v21.5–v25.0 against a v26.0 corpus, so `implemented_by` is "the join
   the data supports," not a guaranteed-complete list of implementers.

For a `TMFCxxx` / `TMFxxx` id, skip this step.

## Step 1 — Identify the id type and look it up

`TMFCxxx` is a component, `TMFxxx` (not `TMFCxxx`) is an API — the id's
own shape tells you which without asking. Look it up in the matching
index file:

```
knowledge/index/components.json   -- one row per component, keyed by id
knowledge/index/apis.json         -- one row per (id, version) pair
```

**Components are unique per id** — `components.json` has exactly one row
per `TMFCxxx`, so there's no ambiguity to resolve.

**APIs are not** — `apis.json` can have multiple rows for the same `id`
at different `version`s, since more than one version of an API can be
cached side by side. If the proposed change is version-specific
("deprecating v4 in favor of v5"), match on **both** `id` and `version`
and report only that version's `used_by` — merging across versions would
overstate the blast radius of a version-specific change. If the caller
hasn't specified a version, list every cached version's `used_by`
separately, not merged into one number.

If the id isn't in the index at all, say so plainly — don't guess a
nearby id. A component with `status: "not_yet_specified"` or an API with
`status: "fetch_failed"` has no real spec to change yet; report that
directly rather than proceeding as if it had one.

## Step 2 — Read `used_by`

Every row in `components.json`/`apis.json` carries a `used_by` field —
this is the starting "which use cases depend on this" list. Its shape
differs by artefact type, deliberately, and both differences matter to
what you report:

**`components.json`'s `used_by` is already reconciled** —
`tools/build_index.py` builds it as the union of each use case's own
frontmatter (`links.components`) and IG1228's independently-sourced
`usecase-component-matrix.json`, so it's a list of `{use_case, source}`
entries rather than a bare id list:
- `source: "confirmed"` — both the use case's own document and IG1228's
  matrix agree.
- `source: "frontmatter_only"` — the use case's own document names this
  component; IG1228's matrix doesn't credit it.
- `source: "matrix_only"` — IG1228's matrix credits this use case with
  the component; the use case's own document doesn't say so. Per
  `knowledge/index/matrix-discrepancies.md`'s Phase 4 findings this is
  the *more common* of the two disagreement directions, not the rarer
  one — report these use cases as real, reportable dependents (noting
  the source), not as a footnote under the confirmed ones. Overall,
  `matrix-discrepancies.md`'s corpus-wide check found the two sources
  disagree for the majority of use cases (14 of 24), so expect
  `frontmatter_only`/`matrix_only` entries often, not rarely.

No separate matrix lookup is needed for a component id — the
reconciliation already happened when the index was built. Group the
report by `source` (§ Output format) rather than treating `used_by` as
one flat list.

**`apis.json`'s `used_by` is a plain frontmatter-derived id list, with no
`source` tag** — IG1228 chapter 2's matrix is a use-case↔**component**
table; it has no API-level data at all, so there's nothing to reconcile
against for a `TMFxxx` id (confirm the file's `usecase-component-matrix.json`
carries no `apis` key rather than assume it). State this plainly rather
than implying an API id got the same two-source reconciliation a
component id gets — those are genuinely different completeness
guarantees, and the difference matters to a reviewer deciding how much
to trust the number.

Separately, a component/API can also be named only in a use case's body
prose rather than its References section (like TMFS020's own
`TMFC001`/`002`/`023`) — neither `used_by` nor the matrix catches that,
since both are References-section-derived. Step 4's own document read is
what surfaces this category — a third, smaller way `used_by` can
undercount, worth keeping in mind alongside the matrix gap above.

## Step 3 — Cross-check each affected use case's own maturity

For every use case in `used_by` (each entry's `use_case` field for a
component id; each plain id for an API id), look up that row in
`knowledge/index/use-cases.json` and read its
`maturity`/`approval_status`/`release_status` fields (the same ones
`check-usecase-maturity` reads):

- `GA` / `TM Forum Approved` use cases are firm, stable dependents — a
  breaking change here has real consumers relying on the current shape.
- `Alpha`/`Beta` use cases are still provisional themselves (per
  `check-usecase-maturity`'s own decision table) — a dependent that's
  itself not yet settled is lower-risk to disrupt than one that's GA.

## Step 4 — Describe specifically how each affected use case depends on it

A bare id + maturity level isn't enough detail to act on — read each
affected use case's own document to find *how* it actually uses the
component/API, the same way `generate-test-cases-from-usecase` resolves
a use case's real interaction flow:

```
knowledge/use-cases/{ID}/{ID}.md
```

Search the `# Description` and `# Sequence diagrams` sections for where
the target id (or its name) actually appears, including the diagram
images themselves where relevant — the real step-by-step usage often
lives there, not just in a components list. Summarize specifically what
the use case does with it (e.g. "TMFC020 verifies the customer's identity
at account-creation step 2, before Party Management proceeds" rather than
"TMFS001 depends on TMFC020"). This is what turns "6 use cases are
affected" into something a reviewer can actually act on — which specific
step in each use case's flow needs a migration plan, not just which ids
are on a list.

For a long `used_by` list, prioritize this detailed read for the
highest-risk (GA/TM Forum Approved) dependents first — do all of them if
asked, but don't let a large list become an excuse to skip Step 4
entirely for the ones that matter most.

## Output format

A short report, not a raw dump of `used_by`. Example, for "deprecating
TMF632 v4.0.0":

> **TMF632 v4.0.0** (Party Management, currently generation `v4`) — 6
> use cases depend on it via their own frontmatter:
>
> | Use case | Maturity / approval | Risk | How it's actually used |
> |---|---|---|---|
> | TMFS001 | GA / TM Forum Approved | **High** | Creates the Individual resource at account-creation step 3; also read/updated later for profile changes |
> | TMFS006 | GA / TM Forum Approved | **High** | Looks up the existing Individual to attach a Legal Guardian relationship |
> | TMFS030 | Beta / Member Evaluated | Low — itself still provisional | References the Party as the MNO/SNO contracting entity, not a core flow step |
>
> 4 of 6 dependents are GA — a breaking change to TMF632 v4 needs a
> migration path for those before it ships, starting with TMFS001's
> create-and-update flow since it's the deepest dependency. TMF632 is an
> API id, so `used_by` is `apis.json`'s plain frontmatter-derived list —
> IG1228's matrix has no API-level data to reconcile against (Step 2).

For a `TMFCxxx` id, the same table gains a **Source** column
(`confirmed` / `frontmatter_only` / `matrix_only`, straight from
`components.json`'s own `used_by` entries) instead of that closing
caveat — e.g. "6 of 9 dependents confirmed by both sources; 3 are
matrix-only (IG1228 credits them, the use case's own document doesn't)."
Always state which of the two cases actually applied for this particular
id — the reconciled component table or the frontmatter-only API list —
not just that the distinction exists in the abstract.

For an **eTOM process id** (Step 0), open the report by naming the
implementing components and then give the combined table. Example, for
"removing eTOM 1.4.5":

> **eTOM 1.4.5 — Service Activation Management** (Level 2, Service Domain).
> Implemented by 3 cached ODA Components: **TMFC003, TMFC007, TMFC009**
> (`etom-index.json` `implemented_by`). Use-case impact is assessed through
> those components:
>
> | Component | Use case | Maturity / approval | Source | How it's used |
> |---|---|---|---|---|
> | TMFC003 | TMFS009 | GA / TM Forum Approved | confirmed | … |
> | … | … | … | … | … |
>
> **eTOM-join caveat:** `implemented_by` is derived from each component's
> `spec.componentMetadata.eTOMs`, authored against eTOM v21.5–v25.0 (this
> corpus is v26.0). A component that implements this activity but hasn't
> filled in or has an outdated eTOM mapping would not appear here.

## What this skill does NOT do

- Does not modify anything — this is a read-only impact report to inform a human decision, not an automated approval or rejection of the change.
- Does not assume `used_by` is exhaustive even after reconciliation — a component/API named only in a use case's body prose (Step 2's closing note) is still invisible to both sources, and Step 4's document read is required to catch it for the high-risk dependents at least.
- Does not treat a component id's `matrix_only` dependents as a footnote — they get reported with the same weight as `confirmed` ones, per Step 2.
- Does not imply an API id got the same two-source reconciliation a component id gets — `apis.json`'s `used_by` has no `source` tag at all, and the report says so rather than staying silent about it.
- Does not stop at a bare id list — Step 4's per-use-case detail is required for at least the high-risk dependents, not an optional enrichment.
- Does not treat an eTOM process's `implemented_by` as a complete list of implementers — it is built from component eTOM mappings authored against an older eTOM release, and the report must say so (Step 0, Output format).
- Does not chase an eTOM process id's parent/child processes — the change is assessed for the id as given; a caller who means "1.4.5 and everything under it" should ask for the subtree explicitly.
