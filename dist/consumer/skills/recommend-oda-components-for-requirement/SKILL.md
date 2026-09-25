---
name: recommend-oda-components-for-requirement
description: Given a plain-language business requirement (not yet a TMFSxxx id), finds the closest-matching existing use case(s) by name and component/API overlap, and proposes a starting architecture grounded in real component/API ids -- never invented ones. Use this at the start of a design, before a requirement has been mapped to a specific ODA use case.
---

# Recommend ODA Components for a Requirement — Skill Instructions

## What this skill answers

"We need to do X — what ODA components and APIs should this be built
on?" The greenfield counterpart to `validate-design-against-oda`, which
checks a design someone has already proposed; this one proposes a
starting point from a plain-language description.

## Step 1 — Find the closest existing use case(s)

Read every row's `name` in `${CLAUDE_PLUGIN_ROOT}/knowledge/index/use-cases.json` and compare
against the requirement. Don't stop at the first plausible-sounding name
— read the `# Objective of the use case` / `# Scope` sections of the top
2-3 candidates (`${CLAUDE_PLUGIN_ROOT}/knowledge/use-cases/{ID}/{ID}.md`) to confirm the match
actually holds, not just that the title sounds related. A name like
"Order Fallout Management" (TMFS011) and a requirement about "handling
failed orders automatically" are a real match; a name like "Problem
Management" (TMFS031) and a requirement about "customer complaints" might
only be a partial one — check the Objective before committing to it as
the closest analog.

If nothing matches closely, say so — don't force the nearest available
use case as if it were a real fit. A weak analog cited honestly is more
useful than a good-sounding wrong one.

## Step 2 — Check whether this is actually a known gap, not a match

Before proposing an architecture from an imperfect analog, check
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/gaps-backlog.md` — if the requirement matches one of the
already-identified capability gaps there (e.g. a requirement for
cross-organization API exposure matches the API-exposure/"Delegate
Component" gap), say so explicitly instead of stretching an unrelated
existing use case's components to fit. Recommending real components that
don't actually cover the requirement is worse than saying "this isn't
built yet, here's what's proposed and its current status."

## Step 3 — Propose the starting architecture

From the closest matching use case(s)' own frontmatter `links.components`/
`links.apis`, propose those as the starting point — cite them with the id
and name exactly as they appear in frontmatter, never a paraphrased or
invented id. If more than one use case matched closely, note where their
component lists agree (higher confidence) and where they diverge (call
out the difference, don't silently merge into one list).

Check each proposed component's `status` in `${CLAUDE_PLUGIN_ROOT}/knowledge/index/components.json`
and each API's in `apis.json` — a `not_yet_specified` component or
`fetch_failed` API is a real caveat for the recommendation, not something
to omit.

**Secondary cross-check via eTOM.** Scan `${CLAUDE_PLUGIN_ROOT}/knowledge/etom/processes.json`
for a process whose `name`/`brief_description` matches the requirement's
own verbs/nouns (favour Level 2–4). For any match, read
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/etom-index.json` → `implemented_by[<id>]` for the
`TMFCxxx` ids that implement that eTOM activity. Use this only to
**corroborate or widen** the Step 1-derived list — a component that shows
up both via the closest use case *and* via a matching eTOM process is a
higher-confidence recommendation; one that shows up only via eTOM is worth
naming as a candidate the use-case analog didn't surface. Don't let it
replace Step 1: the eTOM↔component join is built from mappings authored
against eTOM v21.5–v25.0, so it's a supporting signal, not a primary
source. If no eTOM process matches, skip this — it's not required output.

## Output format

State the requirement as understood, the closest use case(s) and why they
match (cite the Objective/Scope text that grounds the match, not just the
title), the proposed component/API list with ids, and any gap-backlog
cross-reference from Step 2. If the match is partial, say explicitly what
part of the requirement the analog doesn't cover.

## What this skill does NOT do

- Does not invent a component/API id that isn't in `${CLAUDE_PLUGIN_ROOT}/knowledge/index/{components,apis}.json` — an imperfect real analog is always preferable to a fabricated perfect-sounding one.
- Does not draft a new use case document — that's `draft-new-usecase-from-scenario`'s job, for when no existing use case or gap-backlog entry is close enough to reuse.
- Does not check use-case maturity itself — run `check-usecase-maturity` on the matched id(s) too if the recommendation needs a trust verdict, not just a components list.
