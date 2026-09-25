# TM Forum ODA Consumer Agent Skills — Extension Spec

**Status:** Draft v1
**Owner:** Lester Thomas
**Extends:** [`spec.md`](./spec.md) §8/§11.1 (the pilot consumer skills and the consumer half of the skill backlog) and the `tm-forum-oda-consumer` plugin's 9 already-shipped skills. Read `spec.md` first, particularly §1's nine design principles — this document reviews and expands the *consumer* skill set against outside input; it doesn't restate the `knowledge/` layout those two documents already cover, and it doesn't touch the Creator-side skills (`spec.md` §11.2), which are a genuinely different audience.

## 1. The gap this closes

All 9 of `spec.md` §8/§11.1's consumer skills are now built and shipped (root [`README.md`](../README.md)'s Consumer table). Looking at them as a set rather than as a backlog that got worked through one item at a time: they cluster heavily around **Discover** and **Design** (find the right use case, draft requirements, propose a starting architecture, draw a diagram, validate a design's assumptions) and **Assurance-after-the-fact** (audit an implementation, assess a change's blast radius). Nothing in the set touches **Build** (turning an approved design into code) or **Test** in the sense of *running* a conformance check against a real API contract, and nothing reviews architecture-level ODA conformance independent of one specific use case's narrative.

That gap was suspected, not confirmed, until a wide external framing of "agent skills for the ODA SDLC" was reviewed against it — an external conversation exploring exactly that question, provided for this purpose (§2 below). This spec does three things: extracts what's genuinely useful from that conversation, checks every idea against what `knowledge/` actually contains before accepting it (the same discipline `spec.md` §11's closing note applies to its own backlog), and produces a merged, concrete set of skills to add or enhance — reconciled against this repo's own Consumer/Creator split, which the source conversation doesn't draw the same way.

## 2. Source material: an external "Propose ODA Agent Skills" conversation

A conversation with an AI assistant exploring an initial set of ODA agent skills spanning the end-to-end SDLC, reviewed for ideas worth merging into this repo's own consumer skill set. Provided directly for this purpose rather than discovered independently; treated the same way any external proposal is treated throughout this spec — checked against what `knowledge/` actually contains before anything from it is accepted (§6), never taken at face value.

### 2.1 The proposed skill set

An initial ~16 skills, grouped into five stages:

| # | Skill | What it does |
|---|---|---|
| 1 | `oda-architecture-navigator` | Given a concept (order fallout, product qualification, ...), identifies the relevant ODA domains, Components, Open APIs, SID entities, and eTOM processes |
| 2 | `oda-business-capability-mapper` | Converts a requirement/epic into an ODA-aligned capability decomposition — actors, processes, capabilities, information entities, candidate Components |
| 3 | `oda-information-modeler` | Maps requirements/domain objects to SID entities; detects duplicated/proprietary concepts that already have a TM Forum equivalent |
| 4 | `oda-component-designer` | Determines a Component boundary and produces/updates a Component specification (Core Function APIs, dependent APIs, events, Supporting Functions) |
| 5 | `oda-solution-architect` | Composes an end-to-end solution from interacting Components — component diagrams, interaction flows, responsibility allocation |
| 6 | `oda-api-designer` | Selects an existing Open API before allowing a proprietary one; maps requirements to operations/resources; drafts justified extensions |
| 7 | `oda-event-designer` | Designs event contracts between Components — payloads, producers/consumers — aligned to TM Forum resource semantics |
| 8 | `oda-code-generator` | Generates service scaffolding (controllers, domain layer, adapters, OpenAPI models, event handlers, tests) from an approved design |
| 9 | `oda-integration-adapter` | Generates anti-corruption/adapter layers so legacy/non-ODA interfaces don't leak into the Component architecture |
| 10 | `oda-architecture-reviewer` | Reviews a proposed architecture/ADR/repo for ODA alignment — boundary violations, duplicated entities, point-to-point coupling, cross-domain leakage |
| 11 | `oda-api-conformance-tester` | Generates contract tests against a TM Forum Open API spec/conformance profile; reports deviations |
| 12 | `oda-component-conformance-reviewer` | Checks an implementation against a Component spec, distinguishing Core Function from Supporting Function conformance |
| 13 | `oda-canvas-packager` | Converts an implementation into deployable Component artefacts (Kubernetes resources, Component metadata, observability declarations) |
| 14 | `oda-canvas-deployer` | Deploys/plans deployment of Components onto an ODA Canvas |
| 15 | `oda-operability-engineer` | Adds health/metrics/logging/tracing/scaling/resilience per Component Supporting Functions |
| 16 | `oda-requirements-engineer` | Converts unstructured requirement text into a structured ODA-aware spec: `business_intent`, `candidate_processes`, `candidate_components`, `candidate_apis`, `information_entities`, and an explicit `questions` list for genuine ambiguity |

### 2.2 Structural ideas worth adopting independent of the skill list itself

- **A three-way taxonomy**: *Knowledge* skills (reason over ODA — #1-4), *Transformation* skills (turn one artefact into another — #5-9, #16), *Assurance* skills (criticise rather than create — #10-12), kept deliberately separate so the same skill never both generates an artefact and marks its own homework.
- **"ODA-first, not ODA-only"** — an explicit reuse-before-invent policy every skill should follow: look for an existing capability → Component → Open API → information entity, in that order; reuse where appropriate; extend only where necessary; document any deviation explicitly. Framed as the antidote to "we're ODA-compliant because our REST API has a TMF-style JSON payload."
- **An "ODA Knowledge Resolver"** underneath every skill, so a skill never hardcodes "`TMFxxx` version `x.y` is current" as static prose — it resolves the current cached version dynamically instead.
- **Skills vs. workflows** — an orchestration layer (e.g. `deliver-oda-use-case`) that chains individual skills in sequence, distinct from the skills doing the actual reasoning.
- **SDLC-stage framing**: Discover → Design → Build → Test → Run, each stage backed by ODA skills, all ultimately grounded in eTOM/SID/Functional-Architecture knowledge feeding Components and Open APIs.

### 2.3 Two existing, already-built TM Forum reference skills

Different in kind from §2.1's brainstormed list: these two already exist, are already used, and live in TM Forum's own repositories, built independently of this spec and its `knowledge/`-reading model. Surfaced after §2.1/§2.2 were drafted and folded in directly rather than re-derived as new proposals.

- **`create-oda-component`** (github.com/tmforum-oda/reference-example-components, `skills/create-oda-component/`) — given a `TMFCxxx` id, generates a *complete* Node.js microservice implementation (one service per exposed API, role-management and metrics init jobs, an optional MCP server) plus a full Kubernetes Helm chart (Component CRD, deployments, services, PVC), then **builds/pushes the Docker images and can `helm install` the result**. Ships with ~60KB of bundled reference material: `references/{component-list,source-patterns,chart-patterns}.md`, plus `templates/source/` (14 shared Node.js utility files, role-init and metrics microservice implementations, an MCP-server reference) and `templates/charts/` (a conditional role-management Helm template, a chart README template). This is well past scaffolding — a complete, opinionated reference-implementation generator covering **Build** and, via its own Steps 7-9, **Deploy**, in one pass.
- **`create-oda-operator`** (github.com/tmforum-oda/oda-canvas, `skills/create-oda-operator/`) — a pattern-library skill for building the **Canvas's own** Kubernetes operators (Python/KOPF): CRD lifecycle handlers, admission webhooks, peering priorities, Helm chart conventions for an operator's own deployment. Its subject is the Canvas platform itself (`source/operators/TMFOP###-.../`), not an ODA Component's business logic — a materially different audience from "someone building a product using ODA components."

**Neither reads from this repo's `knowledge/` today.** `create-oda-component` fetches the Component YAML and OpenAPI schema directly from the same upstream GitHub/S3 sources this repo's own `tools/fetch_component.py`/`fetch_api.py` already cache locally — duplicating a network round-trip this repo exists specifically to avoid (`spec.md` principle 6). `create-oda-operator` doesn't touch ODA Component/API data at all; its reference material is Canvas operator source code and kopf framework docs. §6.1 below covers what adapting each one to this repo's conventions actually requires.

## 3. What's already built, reclassified against the source conversation's taxonomy

Mapping the 9 shipped consumer skills onto §2.2's three-way taxonomy and the Discover/Design/Build/Test/Run stages makes the gap concrete:

| Skill | Taxonomy | SDLC stage |
|---|---|---|
| `check-usecase-maturity` | Knowledge | Discover |
| `recommend-oda-components-for-requirement` | Knowledge + Transformation | Discover → Design |
| `capture-requirements-from-usecase` | Transformation | Design |
| `draft-architecture-diagram-from-usecase` | Transformation | Design |
| `generate-test-cases-from-usecase` | Transformation | Test (authoring) |
| `generate-api-mocks-from-usecase` | Transformation | Build (enabling) |
| `validate-design-against-oda` | Assurance | Design (pre-build gate) |
| `audit-implementation-against-usecase` | Assurance | Run (post-build) |
| `assess-change-impact` | Assurance | Run (change management) |

**Discover and Design are well covered, twice over in places** (both a Knowledge-style matcher and a Transformation-style drafter exist for going from a plain-language ask to a grounded starting point). **Build has no skill that touches actual implementation content** — `generate-api-mocks-from-usecase` scaffolds test doubles, not the service itself. **Test only covers *authoring* scenarios**, not *running* a conformance check against a real API contract. **Run has impact analysis and use-case-level drift auditing, but nothing that reviews a whole proposed architecture for ODA boundary conformance, and nothing that checks a Component's Core-vs-Supporting-Function conformance specifically.**

## 4. Where this repo's Consumer/Creator split cuts across the source conversation's proposal

The source conversation doesn't distinguish "building a product using ODA" from "extending ODA itself" — this repo already does, deliberately (`spec.md` §11, root `README.md`'s two skill tables). Several of §2.1's proposals land squarely on the Creator side of that line, already covered there, and are **out of scope for this spec**:

| External proposal | Already covered by (Creator side) |
|---|---|
| `oda-component-designer` (author a *new* Component spec) | `propose-component-or-api-extension` |
| `oda-api-designer`, in the sense of drafting a *new* API extension | `propose-component-or-api-extension` |
| Part of `oda-business-capability-mapper` (surfacing a capability ODA doesn't have yet) | `feedback-harvest-gaps-from-lessons-learned` |

What the source conversation calls `oda-api-designer`/`oda-component-designer` in the *selection* sense — "which existing Component/API should this be built on" — is squarely Consumer territory and is what `recommend-oda-components-for-requirement` already does. The dividing line adopted here: **choosing among existing ODA assets is Consumer work; authoring new ones is Creator work.** Every proposal kept in §7 below respects that line; every one dropped for crossing it is noted in §6.

### 4.1 A third audience surfaces: Canvas platform engineering

§2.3's `create-oda-operator` doesn't fit either side of the line above. It isn't "building a product using ODA Components" (Consumer) or "extending the ODA specification itself — new use cases, new Component/API proposals" (Creator) — it's building the **Canvas platform's own** operators, the software that runs Components, not a Component or a spec. That's a third, genuinely distinct audience this repo's plugin split has never had to account for before.

**Resolved (`tasks-skills-consumer.md` 0.2):** left out of scope for now. Rather than force it into either plugin or stand up a third plugin for what is currently a single skill, `implement-oda-canvas-operator` is not vendored as part of this plan — §7.9 and Phase 5 are recorded as deferred, not built. Revisit once there's a real second Canvas-platform-engineering skill to justify a dedicated home for the audience, or once there's a specific reason to want this one integrated after all.

## 5. Already satisfied without new work

- **The "ODA Knowledge Resolver."** This repo already *is* one — `knowledge/index/{use-cases,components,apis}.json` plus the shared five-field envelope (`spec.md` §5.0, principles 6/7/9) means no skill needs to hardcode a version number; every existing skill resolves the current cached version by reading the index or the artefact's own frontmatter at run time. Confirmed by re-reading `assess-change-impact` and `validate-design-against-oda`'s own instructions (§3 above) — both explicitly tell the agent to look up the id in the index rather than assume a version. Nothing to build here; the pattern the source conversation asks for is already this project's foundation, not a gap.
- **"ODA-first, not ODA-only."** Every shipped skill already states some form of "never invent an id, cite the real one or say it doesn't exist" (each `SKILL.md`'s own "What this skill does NOT do" section). The source conversation's contribution is naming this as one explicit, shared policy rather than nine independently-worded instances of it. Adopted here as a named cross-cutting principle (below), not a new skill — there's nothing to *run*, it's a constraint every skill (existing and new) should state in the same words:

  > **ODA-first, not ODA-only.** Prefer an existing ODA capability, Component, Open API, or information entity over inventing one. Extend only where the cached corpus genuinely has no equivalent, and say explicitly when that's what's happening (cross-referencing `knowledge/index/gaps-backlog.md` where relevant) rather than presenting an extension as if it were already standard. Every skill in §7 below states this explicitly rather than leaving it implicit.

## 6. Grounding check — is each remaining idea actually buildable today?

Following `spec.md` §11's own discipline (an idea earns a place in the backlog only if it's grounded in what `knowledge/` actually contains, not speculative): checking the source conversation's remaining proposals — after removing §4's Creator-scoped ones — against real data.

| Idea | Buildable now? | Why |
|---|---|---|
| `oda-requirements-engineer` (structured decomposition + open questions) | **Yes** | Pure reasoning over a plain-language input plus the same index files `recommend-oda-components-for-requirement` already reads. No new data needed. |
| `oda-event-designer` | **Yes** | Every `component.yaml`'s `eventNotification.publishedEvents`/`subscribedEvents` blocks (confirmed present and structurally consistent across every fetched component, e.g. `TMFC062`) already give a real, machine-readable shape to design new events consistently with. |
| `oda-api-conformance-tester` | **Yes** | The cached OpenAPI schemas (`knowledge/apis/{TMFxxx}/*.json`) plus real sample payloads (`knowledge/apis/{TMFxxx}/samples/`, `spec.md` §5.3.1) are exactly what a conformance-test generator needs. |
| `oda-component-conformance-reviewer` | **Yes** | `component.yaml` already carries the Core-vs-Supporting-Function split machine-readably: `spec.coreFunction` (exposed/dependent APIs) is structurally distinct from `spec.managementFunction`/`spec.securityFunction` (confirmed against `TMFC062`'s real cached YAML) — a reviewer can cite this distinction directly instead of inferring it. |
| `oda-architecture-reviewer` (whole-system, not one use case) | **Yes** | `knowledge/index/components.json`/`apis.json` already give a corpus-wide view of what "belongs" to which Component — enough to check a proposed architecture for boundary violations or duplicated ownership without needing eTOM/SID at all. |
| `oda-code-generator` | **Partially** | Scaffolding request/response models and route stubs directly from a cached OpenAPI schema is grounded and buildable now. Generating real business/domain logic is not something a schema alone grounds — scope narrowed accordingly in §7. |
| `oda-integration-adapter` | **Not yet, as its own skill** | By definition reasons about an *external*, non-ODA interface `knowledge/` has no cached data about — nothing to ground it in beyond "map to the chosen ODA contract," which the narrowed code-generator already covers as a mode. |
| `oda-information-modeler` (full SID dedup reasoning) | **No** | `knowledge/sid/` is reserved and unpopulated (`spec.md` §7, confirmed empty except `.gitkeep`). A full information-model reasoning skill has no SID corpus to check duplication against yet. |
| `oda-architecture-navigator` (full eTOM/SID concept lookup) | **Partially — eTOM half now buildable** | `knowledge/etom/` is now a real corpus (`GB921` v26.0, `spec-etom.md`) with `knowledge/index/etom-index.json`'s eTOM↔component join. `explain-etom-process` (one id → explanation + implementers) and `decompose-requirement-against-oda` Step 2 (name scan of `processes.json`) already cover the concrete eTOM lookups a navigator would do; a broader "walk the concept graph" skill still isn't warranted, and the SID half stays blocked — `knowledge/sid/` is still reserved and unpopulated. |
| `oda-canvas-packager` / `oda-canvas-deployer` / `oda-operability-engineer`, as brainstormed §2.1 proposals with nothing existing to vendor | **No — wrong shape of skill, not a data gap** | Every skill in this corpus is "read-only against `knowledge/`, no network calls needed at skill-run time" (root `README.md`'s own framing, `spec.md` principle 3). Packaging/deploying/operating a live Canvas needs cluster credentials and produces real side effects outside `knowledge/` entirely — a fundamentally different kind of tool than anything in this repo, not a `knowledge/`-reading skill with a data gap. Still flagged as future work if built from scratch, the same way `spec-components.md` §8.4 flagged the pipeline's own missing discovery script as future work rather than quietly building it in passing. **Revised by §2.3/§6.1 below**: `create-oda-component` already does the packaging+deploy half for a *Component* (not the Canvas itself), already exists, and is explicitly requested for integration — accepted as a deliberate, named exception to the read-only posture, not a silent contradiction of it. |

### 6.1 Integration path for the two existing reference skills (§2.3)

Unlike §2.1's brainstormed proposals, these two already run — the question isn't whether they're groundable, it's what adapting them to this repo's conventions actually requires before vendoring them in.

**`create-oda-component` → `implement-oda-component`** (renamed per instruction — also avoids collision with the Creator-side `propose-component-or-api-extension`, which drafts a *new* spec; this one builds a real implementation of an *existing, already-specified* one, a Consumer activity):

1. Repoint Step 1's spec fetch from the live GitHub URL to this repo's own cached `knowledge/components/{TMFCxxx}/component.yaml` first, falling back to a live fetch (then a `tools/fetch_component.py` write-back) only if the id isn't cached yet — the same "reuse the cache, don't refetch" discipline every other skill here already follows.
2. Repoint the OpenAPI download in Step 4a from the spec's own `specification[0].url` to this repo's cached `knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json`, same reasoning — falling back the same way if a version isn't cached yet.
3. Steps 7 and 9 (`docker buildx ... --push`, `helm install`) are genuine, real-world side effects outside `knowledge/`. This is new territory for this plugin — §6's table above assumed no consumer skill has side effects; this one legitimately does, by explicit request, not by accident. **Resolved (`tasks-skills-consumer.md` 0.3):** state it as a bolded `⚠ Builds & deploys —` prefix on the skill's own `Produces` cell in root `README.md`'s Consumer table, rather than a new table column (which would force updating every existing row for one skill) or leaving it to the skill's own `SKILL.md` alone (a reader scanning the table should see it before opening the skill at all).
4. **Investigated (`tasks-skills-consumer.md` 0.1), then cleared by explicit user direction.** This session's own repeated checks (`gh api`, twice) found `github.com/tmforum-oda/reference-example-components` carrying no `LICENSE`/`LICENSE.md` file and GitHub's own repo metadata reporting `license: null`, with the `tmforum-oda` org's `.github` fallback repo unlicensed too — under GitHub's default terms that reads as "all rights reserved," not confirmed reusable. The user then confirmed directly that `create-oda-component` is Apache License 2.0, and Phase 4 proceeded on that basis. Recorded transparently: this session's own tooling never independently located that license; the clearance rests on the user's statement. Contrast: `github.com/tmforum-oda/oda-canvas` (source of `create-oda-operator`, §7.9, deferred) **is** independently confirmed Apache-2.0 via GitHub's own repo metadata directly, with no such gap.

**`create-oda-operator` → `implement-oda-canvas-operator`**: **deferred, out of scope for now** (`tasks-skills-consumer.md` 0.2, §4.1) — not vendored as part of this plan. See §7.9.

## 7. Proposed additions and enhancements

Six new skills authored from scratch, one orchestration skill, and two vendored-and-adapted from existing TM Forum reference skills (§2.3/§6.1) — every one grounded per §6, every one respecting the Consumer/Creator line in §4, every one required to state the §5 "ODA-first, not ODA-only" policy explicitly.

### 7.1 `decompose-requirement-against-oda` *(new — Discover)*

Companion to `recommend-oda-components-for-requirement`, picking up exactly where that skill's own Step 1 says "if nothing matches closely, say so" and stops. Given a plain-language requirement with no close existing use-case match, produces a structured ODA-aligned decomposition rather than leaving the requirement as unstructured prose:

```yaml
business_intent: {actor, objective}
candidate_processes: []       # named in plain language, cross-checked against any per-component
                               # eTOM activity names already cached (componentMetadata.eTOMs) —
                               # not a full eTOM taxonomy walk, §6 explains why that's out of reach
candidate_components: []      # real TMFCxxx ids only, from knowledge/index/components.json
candidate_apis: []            # real TMFxxx ids only, from knowledge/index/apis.json
information_entities: []      # cross-checked against every candidate component's own
                               # componentMetadata.SIDs list for likely duplication —
                               # the narrowed, groundable slice of oda-information-modeler (§6)
questions: []                 # genuine architectural ambiguity, surfaced explicitly, never
                               # silently resolved by guessing
```

Absorbs §2.1's `oda-requirements-engineer` and the groundable slice of `oda-business-capability-mapper`/`oda-information-modeler`. Explicitly cross-references `recommend-oda-components-for-requirement` (run that one first; this one is for when it comes up empty) and `feedback-harvest-gaps-from-lessons-learned`/`propose-component-or-api-extension` (the Creator-side handoff when `candidate_components`/`candidate_apis` turn up genuinely empty, not just imperfect).

### 7.2 `draft-event-design-for-component` *(new — Design)*

Given a `TMFCxxx` id (or a requirement already mapped to one via §7.1) and the APIs it's being designed to expose/depend on, drafts published/subscribed event definitions in the same shape every cached `component.yaml`'s `eventNotification` block already uses — resource-level create/attributeValueChange/stateChange/delete events, matched to the real resource names in the chosen APIs' cached schemas, not invented event types. Cites at least one existing component's `eventNotification` block as the structural precedent for the drafted shape. Absorbs §2.1's `oda-event-designer`.

### 7.3 `generate-implementation-scaffold-from-usecase` *(new — Build)*

Given a `TMFSxxx` id (or a component/API set from §7.1/`recommend-oda-components-for-requirement`), generates **scaffolding**, not business logic: typed request/response models and route/handler stubs generated directly from the linked APIs' cached OpenAPI schemas (`knowledge/apis/{TMFxxx}/*.json`), with a `TODO` marker at every point real domain logic belongs — the same "TODO stub, not a bug" convention `validate_envelope.py` already treats as expected mid-pipeline, reused here as expected mid-scaffold. Deliberately narrower than §2.1's `oda-code-generator`: a schema grounds a model/route shape; it does not ground what the business logic inside a handler should do, and this skill must not pretend otherwise. Absorbs §2.1's `oda-code-generator` (narrowed) and folds `oda-integration-adapter` in as an explicit *mode*: when a target interface isn't itself an ODA API, generate the adapter layer translating to/from the chosen ODA contract, clearly commented as an anti-corruption boundary, not scaffolding for the ODA side itself.

Coexists with, doesn't get superseded by, `implement-oda-component` (§7.8): this skill is the lightweight, language-agnostic, no-side-effects option; §7.8 is TM Forum's own complete, opinionated Node.js/Helm reference stack, real build+deploy included. Different trade-off, both kept.

**Cross-cutting finding from piloting this skill (`tasks-skills-consumer.md` Phase 2), relevant beyond just this one skill**: a cached API's `samples/` payloads are not guaranteed to be the same version as its cached schema. Confirmed on `TMF679`: schema cached at `v4.0.0`, but every file under `knowledge/apis/TMF679/samples/` is v5-shaped (v5 `href`s, v5 subclassed `@type`s, field names the v4 schema doesn't define) — parsing one straight into a model built from the v4 schema silently drops the mismatched fields rather than erroring. This skill's own Step 3 now requires validating a sample against the schema before citing it. The same risk likely applies to `generate-api-mocks-from-usecase` (already shipped) and the new `generate-api-conformance-tests` (§7.4) — both cite `knowledge/apis/{TMFxxx}/samples/` the same way — but auditing or fixing those wasn't attempted here (out of scope for this skill's own pilot); flagged as a genuine follow-up in §11.

### 7.4 `generate-api-conformance-tests` *(new — Test)*

Given a `TMFxxx` id + version, generates conformance test assertions directly from the cached OpenAPI schema: required-field presence, enum-value validity, declared operations per path, and expected status codes — using the real sample payloads under `knowledge/apis/{TMFxxx}/samples/` as concrete fixtures wherever they exist, generic ones from the schema alone where they don't. If an implementation (a base URL, or a set of example request/response pairs) is supplied, also reports pass/fail per assertion; without one, produces a standalone test suite ready to run once an implementation exists. Naming deliberately mirrors `generate-test-cases-from-usecase`/`generate-api-mocks-from-usecase` — same family, API-conformance-specific rather than use-case-flow-specific. Absorbs §2.1's `oda-api-conformance-tester`.

### 7.5 `audit-implementation-against-component` *(new — Run)*

Given a `TMFCxxx` id and a description of an implementation, checks conformance at **Component-boundary granularity**, explicitly split the way `component.yaml` itself is: does the implementation's exposed surface match `spec.coreFunction.exposedAPIs`; does it correctly consume `spec.coreFunction.dependentAPIs`; separately, does it provide the Supporting-Function-level behaviors `spec.managementFunction`/`spec.securityFunction` describe (metrics endpoint, secrets-management pattern, security role). Reports the two conformance dimensions separately, never blended into one score — the same distinction §6 confirmed `component.yaml` already draws machine-readably. Complements rather than replaces `audit-implementation-against-usecase`: that skill checks *flow* fidelity against one use case's narrative; this one checks *boundary* fidelity against one component's full contract, independent of any specific use case. Absorbs §2.1's `oda-component-conformance-reviewer`.

### 7.6 `review-architecture-against-oda` *(new — Run, but also usable pre-build)*

Given a description of a proposed or existing multi-component architecture (not scoped to one use case), reviews it against `knowledge/index/components.json`/`apis.json` for: a capability implemented by more than one component where ODA already designates one owner (duplicated ownership), point-to-point coupling where an existing Open API already mediates the same interaction, and a component's declared boundary (its own `coreFunction`) being bypassed by a direct call to another component's internals. Broader than `validate-design-against-oda` (which checks specific claimed dependencies against real specs) and than `audit-implementation-against-usecase`/`audit-implementation-against-component` (both scoped to one use case or one component) — this is the only proposed skill that reasons about a *whole* architecture's ODA conformance at once. Absorbs §2.1's `oda-architecture-reviewer`.

### 7.7 `deliver-oda-requirement` *(new — orchestration)*

The one orchestration skill proposed here, directly modeled on §2.2's skills-vs-workflows distinction and the source conversation's own `deliver-oda-use-case` example. Not a new source of ODA knowledge — its entire job is to invoke the right skill at the right step and hand its output to the next one, stopping at genuine build/deploy (out of scope per §6):

```
requirement
    → recommend-oda-components-for-requirement  (or decompose-requirement-against-oda
       if that one comes up empty)
    → capture-requirements-from-usecase          (once a use case is identified)
    → draft-architecture-diagram-from-usecase
    → draft-event-design-for-component           (§7.2, if new events are needed)
    → validate-design-against-oda                (gate before scaffolding)
    → generate-implementation-scaffold-from-usecase (§7.3)   ┐  choose one, see below
       or implement-oda-component (§7.8)                     ┘
    → generate-api-mocks-from-usecase            (parallel to real backend work)
    → generate-test-cases-from-usecase
    → generate-api-conformance-tests             (§7.4, once a real implementation exists)
    → audit-implementation-against-usecase / audit-implementation-against-component (§7.5)
```

Every arrow is an existing or §7-proposed skill; `deliver-oda-requirement` adds no ODA reasoning of its own, matching the source conversation's own point that a workflow skill's value is orchestration, not knowledge. The Build step forks deliberately: `generate-implementation-scaffold-from-usecase` (§7.3) for a lightweight, language-agnostic, no-side-effects scaffold; `implement-oda-component` (§7.8) when the full opinionated Node.js/Helm reference stack — and an actual build+deploy — is wanted instead. `deliver-oda-requirement` should ask which, not guess.

### 7.8 `implement-oda-component` *(vendored from `create-oda-component`, §2.3/§6.1 — Build + Deploy)* — **built and piloted**

Given a `TMFCxxx` id, generates a complete Node.js reference implementation and Helm chart, then builds/pushes the Docker images and can `helm install` the result — vendored from `github.com/tmforum-oda/reference-example-components`'s `create-oda-component` skill (its `SKILL.md`, `references/`, and `templates/` copied in near-verbatim, 30 files), renamed to fit this repo's naming family and adapted per §6.1: reads the Component spec and OpenAPI schema from this repo's own `knowledge/components/`/`knowledge/apis/` cache first, falling back to a live fetch (and caching the result back via `tools/fetch_component.py`/`fetch_api.py`) only when the id isn't cached yet — confirmed byte-identical to a fresh live fetch for a real id (`tasks-skills-consumer.md` 4.5).

Piloted end to end through `helm lint` against `TMFC009` (`tasks-skills-consumer.md` Phase 4), surfacing two real corrections to the *upstream* skill's own logic, folded back into the vendored copy and its bundled `references/chart-patterns.md`, not just worked around for one pilot:
- The upstream skill defaults to `TMF672` (Permission Specification Set) for every component's security API. Checking every component currently cached in `knowledge/components/` found **26 of 26** actually declare `TMF669` (Party Role Management) instead — the opposite of the documented default. Fixed to check the spec's own `securityFunction.exposedAPIs` rather than assume.
- The bundled Service-template pattern names ports `http-{{.Release.Name}}-{apishortname}api`, which exceeds Kubernetes' 15-character port-name limit for almost any realistic name — confirmed concretely: `helm lint` passed clean against a chart using this exact pattern while the rendered manifest's port name was 18 characters, which a real `kubectl apply` would reject. Fixed to reuse the container's own short abbreviated port name for the Service too, and added an explicit post-lint length check to the skill's own Step 6 instructions, since lint alone doesn't catch this.

**The one skill in this whole plugin with real side effects** — building and pushing Docker images, and optionally deploying via `helm install` — stated explicitly in its own `SKILL.md`, not left implicit. Everything else in `tm-forum-oda-consumer` is read-only against `knowledge/`; this is a deliberate, named exception (§6's table), not a quiet departure from the plugin's normal posture. `deliver-oda-requirement` (§7.7) treats it as one of two Build-stage options, not the only one.

### 7.9 `implement-oda-canvas-operator` — **deferred, out of scope for now**

Was: a pattern-library skill for writing a new ODA Canvas Kubernetes operator (Python/KOPF) — CRD lifecycle handlers, admission webhooks, peering configuration, the operator's own Helm chart conventions — vendored from `github.com/tmforum-oda/oda-canvas`'s `create-oda-operator` skill (Apache-2.0 licensed, confirmed clear to vendor whenever this is picked back up), renamed to fit this repo's naming family.

**Resolved (`tasks-skills-consumer.md` 0.2, §4.1):** not built as part of this plan. §4.1's real open question — its audience (Canvas platform engineering) is neither "building a product using ODA" nor "extending the ODA specification," the two audiences this repo's plugin split was built around — was decided by leaving it out rather than forcing a fit or standing up a third plugin for one skill. Kept here, marked deferred rather than deleted, so the option (and the fact that its license is already clear) isn't lost if a second Canvas-platform-engineering skill later justifies revisiting this.

## 8. Merge decisions — summary

| Item | Decision |
|---|---|
| `recommend-oda-components-for-requirement` | Keep as-is; cross-referenced (not modified) by the new §7.1 |
| `validate-design-against-oda` | Keep as-is; explicitly distinguished from the broader §7.6 |
| `audit-implementation-against-usecase` | Keep as-is; explicitly distinguished from the narrower-scope, boundary-focused §7.5 |
| Every other existing consumer skill | Keep as-is — no proposal from the source conversation overlapped closely enough to warrant a change |
| `oda-requirements-engineer`, groundable slice of `oda-business-capability-mapper`/`oda-information-modeler` | Merged into new §7.1 `decompose-requirement-against-oda` |
| `oda-event-designer` | New §7.2 `draft-event-design-for-component` |
| `oda-code-generator`, `oda-integration-adapter` | Merged, narrowed, into new §7.3 `generate-implementation-scaffold-from-usecase` |
| `oda-api-conformance-tester` | New §7.4 `generate-api-conformance-tests` |
| `oda-component-conformance-reviewer` | New §7.5 `audit-implementation-against-component` |
| `oda-architecture-reviewer` | New §7.6 `review-architecture-against-oda` |
| `deliver-oda-use-case` (workflow concept) | New §7.7 `deliver-oda-requirement` |
| `oda-component-designer`, `oda-api-designer` (authoring sense) | Out of scope — already Creator-side (§4) |
| `oda-architecture-navigator`, full `oda-information-modeler` | Deferred — no eTOM/SID corpus to ground them yet (§6) |
| `oda-canvas-packager`, `oda-canvas-deployer`, `oda-operability-engineer`, as brainstormed §2.1 ideas | Deferred — wrong shape of skill for this repo's read-only model, and nothing existing to vendor (§6) |
| `create-oda-component` (external, already built) | Vendored and adapted as new §7.8 `implement-oda-component`, built and piloted — accepted as a named exception to the read-only posture (§6/§6.1); this session's own checks found no license, cleared to proceed by explicit user confirmation (Apache-2.0) rather than by anything this session located itself (§6.1 point 4, §11) |
| `create-oda-operator` (external, already built) | **Deferred, out of scope for now** — audience-fit question (§4.1) resolved by leaving it out rather than forcing a fit (§7.9); its own license (Apache-2.0) was never the blocker |
| "ODA Knowledge Resolver" | Already satisfied by existing architecture (§5) — no action |
| "ODA-first, not ODA-only" policy | Adopted as a named, explicitly-stated cross-cutting principle (§5) — no new skill |

## 9. Repo layout — considered and deliberately left as-is

The source conversation proposes grouping skills into subdirectories by SDLC stage (`foundations/`, `architecture/`, `development/`, `verification/`, `platform/`, `workflows/`). Considered and rejected for this repo: `skills/` is currently flat, one folder per skill, with staging expressed instead through the README's own category tables (Consumer/Creator/repo-maintenance) and `tools/build_plugin.py`'s `INTERNAL_ONLY_SKILLS` set. Restructuring into nested directories would touch `build_plugin.py`'s skill-discovery glob, every skill's own path references, and both dist plugins' layouts, for a purely organizational change with no functional benefit — the README's category tables already give a reader the same grouping this spec's own §3/§7 tables provide. Revisit only if the flat directory genuinely becomes hard to navigate at a much larger skill count — re-confirmed once at 24 total (`tasks-skills-consumer.md` 0.4, before this plan's builds) and still holding now that all of it has shipped.

## 10. Next steps

Built and tracked in [`spec/tasks-skills-consumer.md`](./tasks-skills-consumer.md) — the same companion relationship `tasks-components.md` has to `spec-components.md`. All of Phases 0-4 and 6-7 are complete: the 6 new skills (§7.1-§7.6), the orchestration skill (§7.7), and `implement-oda-component` (§7.8, vendored) are built, piloted against real data, and registered in root `README.md`/`tools/build_plugin.py` — `tm-forum-oda-consumer` now ships 17 skills. Phase 5 (`implement-oda-canvas-operator`, §7.9) remains deferred per §4.1/§11, not abandoned.

## 11. Open questions

- **Resolved**: `generate-implementation-scaffold-from-usecase` (§7.3) was piloted against a single use case (`TMFS020`/`TMF679`, `tasks-skills-consumer.md` Phase 2) before being finalized, the same way `spec.md` piloted the whole knowledge-base layout against `TMFC039` alone before batching. The pilot held up the skill's original scope — no narrowing needed — but surfaced real instruction gaps (bounded `$ref` recursion depth, `_Create`/`_Update` being distinct schemas, and the sample/schema version-mismatch finding below), all folded back into the skill directly.
- **Partially resolved, from the Phase 2 pilot above**: `generate-api-conformance-tests` (§7.4) was built in Phase 3 with the schema-vs-sample mismatch check baked into its own Step 3 from the start (not discovered the hard way like `generate-implementation-scaffold-from-usecase` was) — its own exposure is addressed by design, confirmed by the Phase 3 pilot's negative-case test against `TMF679`'s known-mismatched sample. **Still genuinely open**: `generate-api-mocks-from-usecase` (already shipped before this whole effort, never revisited) was not audited for the same exposure — worth a targeted check and a matching instruction fix if the pattern recurs there too, not attempted as part of this pass.
- **Resolved**: `deliver-oda-requirement` (§7.7) was built in Phase 6, last, exactly as recommended here — every step it chains together (§7.1-§7.6, plus `implement-oda-component`) was already real by the time it was written and piloted.
- Whether a future eTOM/SID export (`spec.md` §7) should trigger revisiting the two fully-deferred ideas in §6 (`oda-architecture-navigator`, full `oda-information-modeler`) as a dedicated follow-up spec, or fold into whichever spec introduces that export in the first place. Not decided here — flagged so it isn't lost.
- **Resolved by explicit user direction, from §6.1/§7.8** (`tasks-skills-consumer.md` 0.1): this session's own repeated checks found `github.com/tmforum-oda/reference-example-components` carrying no license (no `LICENSE`/`LICENSE.md` file, GitHub metadata reports `license: null`, the org's community-health repo unlicensed too) — the user then confirmed directly that `create-oda-component` is Apache License 2.0, and Phase 4 proceeded on that basis. This session's own tooling never independently located that license; recorded so the gap isn't silently forgotten if it matters later (e.g. if the vendored content is ever redistributed further and someone asks for the source).
- **Resolved, from §4.1/§7.9** (`tasks-skills-consumer.md` 0.2): `implement-oda-canvas-operator` is deferred, out of scope for now, rather than forced into either audience or given its own plugin for one skill — see §4.1/§7.9.
- **New, from §7.8**: now that `implement-oda-component` is actually vendored, confirm its repointed spec/schema lookups (§6.1 points 1-2) don't silently diverge from the upstream skill's own future updates — a vendored-and-modified copy needs its own drift check the same way this repo already tracks drift between `component.yaml` and a `TMFCxxx.md`'s PDF version (`spec-components.md` §5), not a one-time copy assumed to stay in sync forever. Not set up as part of this pass.
- **New, from the Phase 4 pilot**: the two corrections folded into the vendored `implement-oda-component` (the `TMF669`-vs-`TMF672` default, the Service port-name length bug) are real bugs in the **upstream** `create-oda-component` skill too, not just this vendored copy — worth reporting back to `tmforum-oda/reference-example-components` upstream so every consumer of that skill benefits, not just this repo's fork of it. Not attempted as part of this pass (no established relationship with that repo's maintainers to route it through).
