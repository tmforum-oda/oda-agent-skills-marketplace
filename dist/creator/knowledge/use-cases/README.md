# knowledge/use-cases/

25 TM Forum ODA use cases (`TMFSxxx`), converted from the original,
member-gated use-case DOCX documents into agent-friendly Markdown.

If you're an AI agent, read [`AGENTS.md`](AGENTS.md) here first.

## Layout

```
TMFS001/
├── TMFS001.md      YAML frontmatter envelope + prose body (Introduction,
│                   Description, sequence-diagram walkthroughs, Lessons
│                   Learned, ...)
└── media/          diagrams referenced from the body -- PlantUML sources
                     (.puml) for sequence/information diagrams, and
                     .text-description.md sidecars for anything else
                     (UI mockups, block diagrams)
```

Every `TMFSxxx.md` carries the same envelope every artefact in this
corpus does (`id`/`type`/`name`/`version`/`status`/`source`), plus
use-case-specific maturity fields (`maturity`, `approval_status`,
`release_status`, `team_approved`, `published`) and its own curated
`links.components`/`links.apis` — see `spec/spec.md` §5.1/§5.4.

## What a use case is *for*

Each one documents a real business scenario end to end: the actors and
context, the ODA components and Open APIs it exercises, and (for many)
UML sequence diagrams showing exactly which API call happens when. It's
the layer above `components/`/`apis/` — those two answer "what does this
component/API do," a use case answers "here's a concrete scenario where
several of them work together."

## Not every use case IG1228 lists is here yet

[`knowledge/index/usecase-list.json`](../index/usecase-list.json) is the
full list TM Forum's own IG1228 index names, including ones not yet
converted (`planned`, `not available`). This folder only holds the ones
actually converted so far — check that file, not just this folder's
listing, for the complete picture.

## Regenerating

```bash
python tools/docx2md.py <TMFSxxx>
```

Requires the source DOCX already downloaded to `references/use-cases/`
via a logged-in TM Forum member session — see
[`spec/refresh-runbook.md`](../../spec/refresh-runbook.md) for the full
assisted-refresh procedure. Media enrichment (renaming raw images,
writing PlantUML) is a separate, explicit step:
[`skills/process-usecase-media/`](../../skills/process-usecase-media/SKILL.md).
