# knowledge/ — Agent Instructions

This directory is a provenance-tracked, agent-facing knowledge base of TM
Forum's Open Digital Architecture (ODA): use cases, ODA Components, and
Open APIs. It exists so a skill or agent can answer ODA questions by
reading structured local files, never by re-parsing a DOCX/PDF or
guessing at what TM Forum publishes. Full design rationale: `spec/spec.md`
and `spec/spec-components.md`. Build history and every real bug/decision
found along the way: `spec/tasks.md` and `spec/tasks-components.md`.

## Subfolders

| Folder | Contents | Own AGENTS.md |
|---|---|---|
| `use-cases/` | `TMFSxxx` — narrative use cases | [use-cases/AGENTS.md](use-cases/AGENTS.md) |
| `components/` | `TMFCxxx` — ODA Component specs (machine + narrative) | [components/AGENTS.md](components/AGENTS.md) |
| `apis/` | `TMFxxx` — Open API schemas + sample payloads | [apis/AGENTS.md](apis/AGENTS.md) |
| `index/` | Cross-references, ID registry, backlog | [index/AGENTS.md](index/AGENTS.md) |
| `etom/` | `GB921` — Business Process Framework (eTOM) v26.0 (`processes.json`, `deleted.json`) | [etom/AGENTS.md](etom/AGENTS.md) |
| `sid/` | Reserved — not populated in v1 | [sid/AGENTS.md](sid/AGENTS.md) |

## Rules that apply everywhere under `knowledge/`

1. **Every artefact carries the same envelope** — `id`, `type`, `name`,
   `version`, `status`, plus `source.origin`/`retrieved`/`sha256`
   (`spec.md` §5.0). Read it before trusting the body. `status` is a real
   maturity signal (e.g. `Pre-production`, `not_yet_specified`,
   `specified`) — never treat a document as production-ready without
   checking it first.
2. **Absence is meaningful, not a gap to fill in.** If an id has no
   `.md`/`.yaml` — a use case not yet converted, a component with no
   published PDF, an id in `Planned`/`Future` status — that is real,
   surveyed information (see each subfolder's own notes). Never fabricate
   content to stand in for a document that doesn't exist. Say so instead.
3. **Cross-references live only in `knowledge/index/*.json`** (forward
   links in each artefact's own `links:` block, reverse links computed
   into the index). Don't hand-maintain a link anywhere else, and don't
   trust a link you find some other way without checking the index.
4. **This whole tree is generated output, not hand-authored content** —
   it's regenerated from `references/` (raw source documents) and public
   GitHub/S3 sources by `tools/*.py`. Don't hand-edit a generated file
   (`component.yaml`, `*.meta.json`, `*.json` index files, `TMFSxxx.md`/
   `TMFCxxx.md` bodies) — re-run the tool that produces it instead, or the
   next refresh will silently overwrite your edit. A small number of files
   are deliberately static and hand-maintained instead (each subfolder's
   own AGENTS.md says which) — those are the exception, not the norm.
5. **Two independent version numbers can exist for the same nominal
   artefact** (most concretely: an ODA Component's `component.yaml`
   version vs. its PDF specification's own version — `spec-components.md`
   §5). Don't normalize or reconcile them; report both.
6. **This corpus is refreshed on TM Forum's ~8-week publication cadence**,
   not continuously — treat `source.retrieved` as "true as of this date,"
   not "true right now." See `README.md` (this folder) for the refresh
   commands if you need to trigger one.

## Finding things

- Don't guess a file path from an id — look it up in
  `knowledge/index/id-registry.md` (which prefix means what) and
  `knowledge/index/{use-cases,components,apis}.json` (the actual
  `path`/`meta_path` for a given id, plus forward/reverse links).
- A skill already built against this data may already do what you need —
  check `skills/` (each one's `SKILL.md` states what id type it takes and
  what it produces) before reading raw files yourself.
