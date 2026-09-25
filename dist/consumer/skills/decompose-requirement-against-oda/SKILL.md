---
name: decompose-requirement-against-oda
description: Given a plain-language requirement that `recommend-oda-components-for-requirement` couldn't match to an existing use case, produces a structured ODA-aligned decomposition (business intent, candidate eTOM processes, candidate components/APIs, candidate information entities, and explicit open questions) instead of leaving the requirement as unstructured prose. Use this when nothing in `${CLAUDE_PLUGIN_ROOT}/knowledge/index/use-cases.json` matches closely enough to reuse.
---

# Decompose Requirement Against ODA — Skill Instructions

## What this skill answers

"We have a requirement with no close existing use case — what does ODA say about it anyway?" The companion to `recommend-oda-components-for-requirement`, picking up exactly where that skill's own Step 1 stops ("if nothing matches closely, say so"). This skill doesn't find an analog; it decomposes the requirement itself into ODA-aligned pieces, cross-checked against the real cached corpus at every step, same discipline as every other skill here.

**ODA-first, not ODA-only.** Prefer an existing ODA capability, Component, Open API, or information entity over inventing one. Extend only where the cached corpus genuinely has no equivalent, and say explicitly when that's what's happening (cross-referencing `${CLAUDE_PLUGIN_ROOT}/knowledge/index/gaps-backlog.md`) rather than presenting an extension as if it were already standard.

## Step 0 — Confirm `recommend-oda-components-for-requirement` actually came up empty

Run it first if it hasn't already been run against this exact requirement. This skill exists for the specific case where that one has nothing close — not a shortcut around it. If it actually found a partial match, use that skill's own output instead; don't decompose from scratch when a real (even imperfect) analog exists.

## Step 1 — State the business intent

From the requirement's own wording, extract:

```yaml
business_intent:
  actor: <who initiates or benefits — a role/party, not a system>
  objective: <what outcome they want, in one sentence>
```

Don't paraphrase into generic terms that lose the requirement's actual scope (e.g. "manage service" when the requirement specifically says "temporarily suspend an active service" — keep "temporarily suspend" in `objective`, don't widen it).

## Step 2 — Candidate eTOM processes (bounded, not a taxonomy walk)

There is now a real eTOM corpus to search: **`${CLAUDE_PLUGIN_ROOT}/knowledge/etom/processes.json`** (`GB921` v26.0, ~2,915 process elements — see `spec-etom.md`). Each entry has `id`, `name`, `level`, `domain`, `brief_description`, `extended_description`, `parent`, `children`.

Scan `processes.json` for entries whose `name` or `brief_description` words overlap the requirement's own verbs/nouns. Favour the higher levels (Level 2–4) — a Level-2/3 process names a capability area, which is what a decomposition wants, not a Level-7 leaf activity. List matches as `candidate_processes`, citing `id · name` verbatim (and `uid` for an unambiguous reference), never a paraphrased name. Prefer 3–8 well-matched candidates over an exhaustive list — this is a bounded relevance scan, not a taxonomy walk.

Then, as a **secondary signal**, cross-check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/etom-index.json`'s `implemented_by`: if a candidate process id maps to one or more `TMFCxxx`, that's a strong hint for Step 3's component list (the eTOM activity is already implemented by a real ODA Component). Note that the eTOM↔component join reflects mappings authored against eTOM v21.5–v25.0 — treat `implemented_by` as supporting evidence, not proof.

If nothing overlaps, say so plainly — an empty `candidate_processes` list is a real, valid finding, not a sign to search harder until something fits.

## Step 3 — Candidate components and APIs

Search `${CLAUDE_PLUGIN_ROOT}/knowledge/index/components.json`/`apis.json` by `name` for entries whose function plausibly matches the requirement — same matching discipline `recommend-oda-components-for-requirement` Step 1 already uses, just without a use case as the intermediary. Cite only real ids from these files, exactly as they appear (`id`, `name`). Check each candidate's `status` — a `not_yet_specified` component or `fetch_failed` API is a real caveat to carry into the output, not to omit.

## Step 4 — Candidate information entities

List the domain nouns the requirement actually names (e.g. "service," "product," "party"). For each, search every cached `component.yaml`'s `componentMetadata.SIDs` list (pipe-delimited, e.g. `Product_Domain|Product_Configuration_ABE|v25.0`) for an entity that already covers it. This is the narrowed, groundable slice of full SID-entity reasoning `spec-skills-consumer.md` §6 describes — a corpus-wide duplication check across what's already cached, not a walk of the full SID model (`${CLAUDE_PLUGIN_ROOT}/knowledge/sid/` is still reserved and empty — unlike `${CLAUDE_PLUGIN_ROOT}/knowledge/etom/`, which Step 2 now searches directly). If a domain noun the requirement names doesn't appear in any component's `SIDs` list, list it as a candidate new information entity, not a silently-assumed-covered one.

## Step 5 — Surface genuine ambiguity, don't resolve it by guessing

If the requirement is genuinely underspecified in a way that changes which components/APIs/entities apply (e.g. "is this a configuration change or a lifecycle state transition?"), list it under `questions`. A question here must be one where a different real answer leads to a different `candidate_components`/`candidate_apis` list — not a generic caveat. Never silently pick one interpretation and present it as the only reading.

## Step 6 — Check for a genuine capability gap before finishing

If Step 3 or Step 4 comes back with a real candidate list that's empty or clearly doesn't cover the requirement (not just imperfect), check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/gaps-backlog.md` for a matching already-identified gap before concluding ODA simply has nothing here. If it matches a logged gap, say so and cite it. If it doesn't match anything logged either, say that too — this is exactly the situation `feedback-harvest-gaps-from-lessons-learned` and `propose-component-or-api-extension` exist for; this skill identifies the gap, it doesn't propose the fix.

## Output format

```yaml
business_intent:
  actor: ...
  objective: ...
candidate_processes:
  - id: "1.2.20"
    name: Product Catalog Lifecycle Management
    level: 2
    implemented_by: [TMFC001]   # from etom-index.json, secondary signal — omit if none
  # or [] if genuinely none found
candidate_components:
  - id: TMFCxxx
    name: ...
    status: specified   # from ${CLAUDE_PLUGIN_ROOT}/knowledge/index/components.json, carried through as a caveat
candidate_apis:
  - id: TMFxxx
    name: ...
    status: specified
information_entities:
  - name: ...
    covered_by: TMFCxxx   # cite the component whose SIDs list already includes it, or omit if genuinely new
questions:
  - ...
```

State plainly, in prose alongside the YAML, which sections came back empty and why (no eTOM/SID overlap found vs. a genuine gap vs. ambiguity blocking further decomposition) — an empty list with no explanation reads as an incomplete run, not a real finding.

## What this skill does NOT do

- Does not run instead of `recommend-oda-components-for-requirement` — that skill runs first, always; this one only picks up where it comes up empty (Step 0).
- Does not invent a `TMFCxxx`/`TMFxxx` id, an eTOM process id, or a SID entity name that isn't found in the real cached corpus — an empty candidate list is always preferable to a fabricated one.
- Does not attempt full eTOM or SID taxonomy reasoning. Step 2 is a bounded relevance scan of `${CLAUDE_PLUGIN_ROOT}/knowledge/etom/processes.json` (the real eTOM v26.0 corpus), not a tree walk or a completeness claim; Step 4's SID check is still bounded to what's cached per-component (`${CLAUDE_PLUGIN_ROOT}/knowledge/sid/` remains reserved and empty — `spec-skills-consumer.md` §6).
- Does not propose a fix for a genuine gap it finds — that's `propose-component-or-api-extension`'s job, handed off explicitly in Step 6, not attempted here.
- Does not resolve a genuine ambiguity by picking the more likely-sounding interpretation — Step 5's `questions` list is required output for real ambiguity, not an optional nicety.
