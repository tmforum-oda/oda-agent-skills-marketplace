# knowledge/

The agent-facing corpus of this repository: a machine-readable knowledge
base built from TM Forum's Open Digital Architecture (ODA) — use cases,
ODA Components, and Open APIs — organized so Agent Skills can query it
directly, without re-parsing the original DOCX/PDF documents.

If you're an AI agent working in this repository, read [`AGENTS.md`](AGENTS.md)
in this folder (and the one in whichever subfolder you're working in) first.

## What's here

| Folder | What it holds | How many |
|---|---|---|
| [`use-cases/`](use-cases/) | `TMFSxxx` — narrative ODA use cases | 24 converted |
| [`components/`](components/) | `TMFCxxx` — ODA Component specs (machine-readable + narrative) | 31 (25 with a narrative PDF) |
| [`apis/`](apis/) | `TMFxxx` — Open API (Swagger/OpenAPI) schemas + sample payloads | 51+ API versions |
| [`index/`](index/) | Cross-references, ID registry, gap tracking | — |
| [`etom/`](etom/) | `GB921` — Business Process Framework (eTOM) process corpus | v26.0 (2,915 processes) |
| [`sid/`](sid/) | Reserved for a future SID data-model export | not populated in v1 |

## Where things come from

`references/` (a sibling of this folder) holds the raw, unmodified source
documents — DOCX/PDF/YAML — for provenance and re-conversion. Everything
under `knowledge/` is generated from `references/` plus public TM Forum
GitHub/S3 sources by the scripts in [`tools/`](../tools/); skills should
never need to touch `references/` directly, and this folder should never
be hand-edited except for the handful of files each subfolder's own
README calls out as static.

Every artefact — regardless of type — carries the same five-field
envelope (`id`, `type`, `name`, `version`, `status`) plus provenance
(`source.origin`/`retrieved`/`sha256`). The full rationale for this shape
lives in [`spec/spec.md`](../spec/spec.md) §5.0 (and, for the
Component-Specification-PDF layer specifically,
[`spec/spec-components.md`](../spec/spec-components.md)).

## Keeping this up to date

TM Forum republishes on a rolling ~8 week cadence. See the root
[`README.md`](../README.md#running-a-refresh) for the full refresh
commands — in short:

```bash
python tools/fetch_component.py --all-referenced && python tools/fetch_api.py   # automated track, no login needed
python tools/build_index.py                                                     # regenerate knowledge/index/
python tools/validate_envelope.py --strict                                      # gate: every envelope well-formed
```

Use-case DOCX files require a logged-in TM Forum member session and
follow the separate, human-assisted track documented in
[`spec/refresh-runbook.md`](../spec/refresh-runbook.md).

## Consuming this knowledge base

Query it through the Agent Skills built against it — see the root
[`README.md`](../README.md#skills) for the full catalog (what each skill
takes as input and produces). Using this corpus from another repository?
Install the plugins from the marketplace — see
[`README.md`](../README.md#using-the-marketplace-in-claude-code).
