# ODA Agent Skills Marketplace

A set of Agent skills for **Consumers** and **Creators** of the TM Forum Open Digital Architecture, backed by an agent-friendly **knowledge** base.

The skills are packaged into two plugins `tm-forum-oda-consumer` and `tm-forum-oda-creator` and made available in a Marketplace. You can view the skills in:

[dist/consumer/skills](dist/consumer/skills)

[dist/creator/skills](dist/creator/skills)

The [knowledge](knowledge) is a machine-readable knowledge base built from TM Forum's
Open Digital Architecture (ODA) — use cases (`TMFSxxx`), ODA Components
(`TMFCxxx`), and Open APIs (`TMFxxx`) — organized so that Agent
Skills can query it directly, without re-parsing DOCX/PDF.

The full design rationale lives in [`spec/spec.md`](spec/spec.md); build
history and the reasoning behind every real bug/decision found along the
way is in [`spec/tasks.md`](spec/tasks.md). The human-readable Component
Specification PDF narrative alongside each `component.yaml` (see below)
has its own companion pair, [`spec/spec-components.md`](spec/spec-components.md)
and [`spec/tasks-components.md`](spec/tasks-components.md). The
cross-reference layer's use-case/component disagreement is reconciled
directly in `components.json` (not left for every skill to re-derive), and a
derived OWL/RDF export of the same graph is generated at
`knowledge/index/ontology.ttl` — both covered in
[`spec/spec-ontology.md`](spec/spec-ontology.md), including why the JSON
stays the primary, skill-facing lookup path either way.

## Using the marketplace 

The two plugins are published as a plugin marketplace at
[`tmforum-oda/oda-agent-skills-marketplace`](https://github.com/tmforum-oda/oda-agent-skills-marketplace). The instructions below show how to install in Claude code (the skills will also work with most popular AI Coding Agents).

Each step below works either as a plain-English prompt (just type it into
Claude Code) or as a `/plugin` slash command / `claude plugin` CLI call in
an interactive session.

### Add the marketplace

| | |
|---|---|
| Prompt | `Add https://github.com/tmforum-oda/oda-agent-skills-marketplace as a plugin marketplace` |
| Slash command | `/plugin marketplace add https://github.com/tmforum-oda/oda-agent-skills-marketplace` |
| CLI | `claude plugin marketplace add https://github.com/tmforum-oda/oda-agent-skills-marketplace` |

![Adding the marketplace from a prompt](images/Add%20Marketplace.png)

### List the configured marketplaces

| | |
|---|---|
| Prompt | `list the plugin marketplaces` |
| CLI | `claude plugin marketplace list` |

Shows every marketplace Claude Code knows about — e.g. `claude-plugins-official`
and `tm-forum-oda-marketplace`.

![Listing marketplaces](images/list%20marketplaces.png)

### List the plugins in a marketplace

| | |
|---|---|
| Prompt | `list the plugins in tm-forum-oda-marketplace` |

The marketplace offers two plugins: **`tm-forum-oda-consumer`** (build software
against ODA) and **`tm-forum-oda-creator`** (extend and contribute to ODA itself).

![Listing plugins in the marketplace](images/list%20plugins.png)

### Install a plugin

| | |
|---|---|
| Prompt | `install tm-forum-oda-consumer` &nbsp;(or `install tm-forum-oda-creator`) |
| Slash command | `/plugin install tm-forum-oda-consumer@tm-forum-oda-marketplace` |
| CLI | `claude plugin install tm-forum-oda-consumer@tm-forum-oda-marketplace` |

Installs at user scope; restart Claude Code so it picks up the new skills.

![Installing a plugin](images/install%20plugin.png)

### Execute a skill

Skills are namespaced by plugin. Type `/` followed by the plugin name to browse
them — `/tm-forum-oda-consumer:` lists every consumer skill with its description.

| | |
|---|---|
| Browse | `/tm-forum-oda-consumer:` &nbsp;then pick a skill (e.g. `check-usecase-maturity`) |
| List from a prompt | `list the skills in tm-forum-oda-creator` |
| Run explicitly | `/tm-forum-oda-consumer:check-usecase-maturity TMFS030` |
| Run implicitly | just describe the task — `Is TMFS030 safe to build against?` — and Claude picks the skill |

![Executing a skill](images/execute%20skill.png)

## Repository Layout

```
references/   raw downloaded input -- DOCX/PDF, unmodified, for provenance and re-conversion
knowledge/    generated, agent-facing corpus -- what skills actually read
skills/       Agent Skills built against knowledge/
tools/        the conversion/fetch/index pipeline that produces knowledge/ from references/
spec/         spec.md (design), tasks.md (build log), refresh-runbook.md (assisted-track checklist)
```

**`references/` contains the source artefacts and  `knowledge/`** contains the agent-friendly view
(spec.md principle 3). `references/` holds TM Forum member-gated content (IG1228, the `TMFSxxx` use-case
DOCX files) that a fresh clone has no other way to reproduce without a
TM Forum login; see spec.md §10 for the full reasoning. `knowledge/` is
regeneratable from `references/` plus the public GitHub/S3 sources —
skills should never need to touch `references/` directly.

Within `knowledge/`:

```
knowledge/use-cases/{TMFSxxx}/{TMFSxxx}.md   one Markdown file per use case, YAML frontmatter + body
knowledge/components/{TMFCxxx}/               component.yaml + component.meta.json + {TMFCxxx}.md (narrative, from the PDF spec -- 25 of 31 components have one, spec-components.md §3.1/§6)
knowledge/apis/{TMFxxx}/                      {TMFxxx}_v{version}.json + .meta.json (multiple versions coexist)
knowledge/index/                              the ID registry -- see below
```

Every artefact carries the same five-field envelope (`id`, `type`, `name`,
`version`, `status`) plus provenance (`source.origin`/`retrieved`/`sha256`)
and, for use cases, maturity/approval fields — spec.md §5.0/§5.4 explains
why, and it's what makes `check-usecase-maturity` (below) possible without
a network call.

## The ID registry — `knowledge/index/`

Every "what exists, and what links to what" question should be answerable
by reading one of these files:

| File | What it answers |
|---|---|
| `use-cases.json` / `components.json` / `apis.json` | the full corpus, one row per artefact, with forward and reverse links |
| `usecase-list.json` | every `TMFSxxx` id IG1228 knows about, including `planned`/`not available` ones with nothing converted yet |
| `usecase-component-matrix.json` | IG1228's own corpus-level "which use case touches which component" table |
| `matrix-discrepancies.md` | where a use case's own document disagrees with that matrix, logged to feedback to the use-case team (spec.md §5.4) — read **both** sources for a complete answer; |
| `gaps-backlog.md` | capability gaps TM Forum's own authors already flagged in use cases' "Lessons learned" sections — proposed components/APIs that don't exist yet, consolidated across every use case that raises each one (spec.md §11.2, `skills/feedback-harvest-gaps-from-lessons-learned/`) |
| `component-folder-map.json` / `api-samples-folder-map.json` | id → upstream GitHub folder lookups, internal to `tools/fetch_*.py` |

Regenerate all three main index files with `python tools/build_index.py`
(idempotent — safe to re-run any time, byte-identical output on unchanged
input).

## Running a refresh

TM Forum republishes on a rolling 8 week cadence. There are two
independent tracks — see [`spec/refresh-runbook.md`](spec/refresh-runbook.md)
for the full step-by-step, and `spec/spec.md` §6 for why they're split:

- **Assisted** (`spec/refresh-runbook.md`) — IG1228 and `TMFSxxx` use cases.
  Requires a logged-in TM Forum member session and a human to click
  through the download; cannot be scheduled.
- **Automated** (`python tools/fetch_component.py --all-referenced && python tools/fetch_api.py`) —
  ODA Component specs and Open API schemas. Fully public, unauthenticated,
  safe to run on a schedule; only rewrites files whose content actually
  changed. The human-readable Component Specification PDFs (`{TMFCxxx}.md`,
  `tools/pdf2md_component.py`) belong to this same track — no login gate
  either — but are heavier: each component's PDF link has to be resolved
  from a real directory-page load first (spec-components.md §3), not a
  tag-listing lookup, and that discovery+download half isn't yet its own
  checked-in script (done per-component via a driven browser so far,
  spec-components.md §7, spec/tasks-components.md Phase 8.4).

Either way, finish with `python tools/build_index.py` then
`python tools/refresh_report.py` to regenerate the index and append a
dated entry to `CHANGELOG.md` describing what changed — maturity/status
transitions (`Beta → GA`) called out explicitly, per spec.md §6.3's
finding that a newly-changed use case is very likely pre-GA.

## Skills

Built against `knowledge/`, read-only, no network calls needed at
skill-run time. Two audiences, packaged as two separate plugins
(`tm-forum-oda-consumer` / `tm-forum-oda-creator`, see
[`tools/build_plugin.py`](tools/build_plugin.py)) so each install's skill
list stays focused on what that audience actually invokes: **consumers**
build a product using ODA; **creators** extend ODA itself.

**Consumers** (`tm-forum-oda-consumer`)

Stage follows the Discover/Design/Build/Test/Run framing in
[`spec/spec-skills-consumer.md`](spec/spec-skills-consumer.md) §3 — a
documentation-only grouping, not a folder structure (§9 there explains
why `skills/` itself stays flat).

| Skill | Stage | Given | Produces |
|---|---|---|---|
| [`check-usecase-maturity`](skills/check-usecase-maturity/SKILL.md) | Discover | a `TMFSxxx` id | a plain-language "is this safe to build against" verdict from frontmatter alone |
| [`explain-etom-process`](skills/explain-etom-process/SKILL.md) | Discover | a `GB921` eTOM process id (e.g. `1.2.20`) | a plain-language explanation of the process and which ODA components implement it |
| [`recommend-oda-components-for-requirement`](skills/recommend-oda-components-for-requirement/SKILL.md) | Discover → Design | a plain-language requirement | the closest matching use case(s) and a starting component/API architecture |
| [`decompose-requirement-against-oda`](skills/decompose-requirement-against-oda/SKILL.md) | Discover | a requirement with no close use-case match | a structured ODA decomposition (intent, candidate processes/components/APIs/entities, open questions) |
| [`capture-requirements-from-usecase`](skills/capture-requirements-from-usecase/SKILL.md) | Design | a `TMFSxxx` id | user stories and acceptance criteria, citing real component/API ids |
| [`draft-architecture-diagram-from-usecase`](skills/draft-architecture-diagram-from-usecase/SKILL.md) | Design | a `TMFSxxx` id | a Mermaid diagram redrawn from the use case's own sequence diagrams |
| [`draft-event-design-for-component`](skills/draft-event-design-for-component/SKILL.md) | Design | a `TMFCxxx` id + the APIs it exposes/depends on | a drafted `eventNotification` entry grounded in the API's own schema and any existing sibling precedent |
| [`validate-design-against-oda`](skills/validate-design-against-oda/SKILL.md) | Design (pre-build gate) | a proposed component/API design | a drift report checking its claimed dependencies against the real cached specs |
| [`generate-api-mocks-from-usecase`](skills/generate-api-mocks-from-usecase/SKILL.md) | Build (enabling) | a `TMFSxxx` id | mock/fixture payloads for its linked APIs, from cached schemas and real sample payloads |
| [`generate-implementation-scaffold-from-usecase`](skills/generate-implementation-scaffold-from-usecase/SKILL.md) | Build | a `TMFSxxx` id + a target language | typed models and route/handler stubs from the linked APIs' cached schemas, `TODO`-marked, no business logic |
| [`implement-oda-component`](skills/implement-oda-component/SKILL.md) | Build + Deploy | a `TMFCxxx` id | ⚠ Builds & deploys — a complete Node.js reference implementation and Helm chart, TM Forum's own opinionated stack, builds/pushes images and can `helm install` |
| [`generate-test-cases-from-usecase`](skills/generate-test-cases-from-usecase/SKILL.md) | Test (authoring) | a `TMFSxxx` id | BDD/Gherkin test scenarios grounded in the use case's real linked components/APIs and cached schemas |
| [`generate-api-conformance-tests`](skills/generate-api-conformance-tests/SKILL.md) | Test | a `TMFxxx` id + version | conformance test assertions (required fields, enums, operations, status codes) from the cached schema, pass/fail if an implementation is supplied |
| [`audit-implementation-against-usecase`](skills/audit-implementation-against-usecase/SKILL.md) | Run (post-build) | a `TMFSxxx` id + an existing implementation | a drift report against what the use case actually specifies |
| [`audit-implementation-against-component`](skills/audit-implementation-against-component/SKILL.md) | Run (post-build) | a `TMFCxxx` id + an existing implementation | Core Function and Supporting Function conformance, reported as two separate dimensions |
| [`review-architecture-against-oda`](skills/review-architecture-against-oda/SKILL.md) | Run (also usable pre-build) | a proposed or existing multi-component architecture | duplicated-ownership, point-to-point coupling, and boundary-bypass findings against the real cached corpus |
| [`assess-change-impact`](skills/assess-change-impact/SKILL.md) | Run (change management) | a `TMFCxxx`/`TMFxxx`/`GB921` eTOM id + proposed change | every use case that depends on it (index reverse links; eTOM ids resolve via `etom-index.json`) and a maturity-weighted migration risk report |
| [`deliver-oda-requirement`](skills/deliver-oda-requirement/SKILL.md) | Discover → Run (orchestrator) | a plain-language requirement | the full chain above run end to end — orchestrates the other skills, no ODA reasoning of its own |

**Creators** (`tm-forum-oda-creator`)

| Skill | Given | Produces |
|---|---|---|
| [`feedback-harvest-gaps-from-lessons-learned`](skills/feedback-harvest-gaps-from-lessons-learned/SKILL.md) | the whole corpus | capability gaps TM Forum's own authors already flagged, consolidated in [`knowledge/index/gaps-backlog.md`](knowledge/index/gaps-backlog.md) |
| [`feedback-propose-matrix-correction`](skills/feedback-propose-matrix-correction/SKILL.md) | a `matrix-discrepancies.md` entry | a specific, submittable correction for the next IG1228 revision |
| [`draft-new-usecase-from-scenario`](skills/draft-new-usecase-from-scenario/SKILL.md) | a business scenario | a new use-case document in this corpus's own structure |
| [`propose-component-or-api-extension`](skills/propose-component-or-api-extension/SKILL.md) | a capability gap | a draft component skeleton (real IG1242 shape) or API schema extension |
| [`lint-usecase-draft`](skills/lint-usecase-draft/SKILL.md) | a draft use-case document | a pre-submission check against known conversion-breaking document shapes |

Using these skills from another repository? Install
[`tm-forum-oda-consumer`](dist/consumer/) and/or
[`tm-forum-oda-creator`](dist/creator/) as Claude Code plugins from the
marketplace — see [Using the marketplace in Claude Code](#using-the-marketplace-in-claude-code)
above. Each plugin bundles its own copy of `knowledge/`, so it works from
any project with zero manual clone/update management.

**Repo maintenance**

Two skills write to `knowledge/` instead of just reading it, and are
deliberately excluded from both `dist/consumer/` and `dist/creator/` — a
consumer or creator building against this corpus has no use for a skill
that edits it:

| Skill | Given | Produces |
|---|---|---|
| [`process-usecase-media`](skills/process-usecase-media/SKILL.md) | a `TMFSxxx` id | renames each of its raw extracted images descriptively, reverse-engineers UML sequence diagrams into PlantUML, and writes a text description for everything else — see spec.md §12 |
| [`process-component-media`](skills/process-component-media/SKILL.md) | a `TMFCxxx` id | renames each of its raw extracted images descriptively, reverse-engineers the component architecture/eTOM-SID-link/API-structure diagrams into PlantUML, and writes a text description for everything else — see spec-components.md §4.2 |

## Tools

Every script in `tools/` opens with a `Reads:`/`Writes:`/`Track:` header
stating what it touches and whether it belongs to the assisted or
automated refresh track (or is a shared helper/gating check used by both)
— check there before reading further into any one script's docstring for
the *why*.
