# Ontology & Cross-Reference Layer — Extension Spec

**Status:** Draft v2 — revised after explicit direction on both open questions
v1 raised. v1 recommended patching the disagreement in skill instructions and
not building an RDF/OWL export; both were overridden on request. §2/§3/§8/§9
below describe what was actually built instead; §4–§7's grounding analysis is
kept because the reasoning still holds — it's *why* the RDF/OWL export in §8.4
is built the way it is (a derived, secondary artifact, not a replacement for
the JSON lookups every skill uses).
**Owner:** Lester Thomas
**Extends:** [`spec.md`](./spec.md) §5.4 (Indexes) and §3 principles 6/7/9. Prompted by a
skill-creator review of `skills/assess-change-impact` that found its own matrix
cross-check instruction under-specified enough to produce a measured, real
undercount (§2) — this spec asks the broader question that finding raised: is
`knowledge/index/`'s current shape (plain JSON catalogs, one hand-maintained
discrepancy doc) still the right one at this corpus's current size, or does it
need a formal ontology (OWL) and/or RDF-graph representation instead? Answered
by checking both the actual data and the actual repository principles before
proposing anything, per the same discipline `spec-skills-consumer.md` §6
applies to its own backlog — an idea earns a place here only if it's grounded
in what `knowledge/` genuinely contains and genuinely needs, not speculative.

## 1. The question this answers

`assess-change-impact` answers "if we change `TMFC020`, which use cases
break?" by reading a reverse index (`used_by`) computed from forward links
every other artefact declares. That's a graph query — small, but a graph
query — over data assembled from two independent, sometimes-disagreeing
sources. Graph-shaped, multi-source, provenance-sensitive data is exactly the
kind of problem the Semantic Web stack (RDF triples, OWL classes/reasoning,
SPARQL) was built for, which is why it's worth asking directly rather than
assuming plain JSON is obviously sufficient forever. This spec answers that
question for the corpus as it exists today, and names the trigger for
revisiting it later rather than leaving the question permanently closed.

## 2. What prompted this — a measured bug, not a hypothetical

Before this session, `assess-change-impact`'s Step 2 caveat said to
"cross-check `knowledge/index/usecase-component-matrix.json` and
`knowledge/index/matrix-discrepancies.md` for the same id" without saying
*how* — and tested against a real id, that vagueness produced a real,
measured gap:

```
components.json's "used_by" for TMFC020      (frontmatter-derived): TMFS001, TMFS016            (2)
usecase-component-matrix.json's own reverse
  index, components["TMFC020"].used_by       (IG1228 ch.2-derived):  TMFS001, TMFS016, TMFS020, TMFS021  (4)
```

A change-impact report for TMFC020 that only read `used_by` — which is what
the previous instructions actually pointed the skill at — would have shipped
a 2-dependent report for something with 4 real dependents, missing half of
them, silently. The corpus-wide reason this isn't a one-off: per
`matrix-discrepancies.md`'s own Phase 4 finding, 14 of 24 use cases in the
whole corpus disagree between their own document and IG1228's matrix in one
direction or the other — this is the *normal* case, not an edge case.

**v1 of this spec fixed this in `skills/assess-change-impact/SKILL.md`'s own
instructions** — naming the exact reverse-index key to read and requiring the
union to be reported in three groups. **Overridden on request**: fixing the
*data* was preferred over fixing the *instructions* — "rather than have two
sources of truth and the need to reverse-lookup." §3/§8 below describe what
changed instead: `components.json`'s own `used_by` is now the reconciled
union, computed once in `tools/build_index.py`, not re-derived per skill
invocation. `assess-change-impact`'s Step 2 is simpler as a result — it now
just reads one field.

## 3. What the cross-reference layer looks like today

- **Three flat catalogs**, one row per artefact: `use-cases.json`,
  `components.json`, `apis.json` (§5.4). Every row carries the shared
  envelope (§5.0) plus **forward** links (`links.components`/`links.apis`,
  authored from each use case's own document) and, on the component/API
  side only, a **reverse** `used_by` — computed once by `build_index.py`.
  **As of this revision, the two catalogs compute it differently, and
  deliberately so**: `apis.json`'s `used_by` stays a plain frontmatter-only
  id list (there's no second source to reconcile against — see below);
  `components.json`'s `used_by` is now the *reconciled union* of the
  frontmatter side and the matrix side, each entry tagged `confirmed` /
  `frontmatter_only` / `matrix_only` (§8.2). The original design (v1 of this
  file, and `build_index.py`'s own prior docstring) deliberately left these
  unmerged, reasoning that blending them would silently erase the
  disagreement signal `matrix-discrepancies.md` exists to preserve —
  overridden on request: tagging each entry's source preserves that signal
  just as well as keeping the files separate does, while removing the need
  for every reader to redo the merge itself.
- **One independently-sourced bipartite graph**,
  `usecase-component-matrix.json`, extracted mechanically from IG1228
  chapter 2. Unlike the catalogs above, it's already dual-keyed —
  `use_cases: {TMFSxxx: [TMFCxxx...]}` **and** `components: {TMFCxxx:
  {used_by: [TMFSxxx...]}}` — i.e. it already carries its own reverse index;
  nothing needed to be added to read it in reverse. This is the file
  `assess-change-impact`'s bug (§2) was in front of the whole time.
- **One hand-maintained prose log**, `matrix-discrepancies.md`, narrating
  *why* the catalogs and the matrix disagree per use case, not just *that*
  they do — deliberately kept as prose rather than folded into a
  machine-only structure, because the "why" (TMFS029's References section
  is a literature bibliography, not a component list; IG1228's chapter 2
  lagging behind individual document edits) is exactly the part a bare list
  of mismatched ids would lose.
- **Corpus scale, measured directly**: 24 use cases, 31 components, 51
  cached `(id, version)` API rows. `use-cases.json` + `components.json` +
  `apis.json` + `usecase-component-matrix.json` together are under 90KB.
  Every lookup any shipped skill performs today is either "read one row by
  id" or "read one row's array field" — nothing in the current skill set
  scans the corpus or joins across more than two files.
- **Only one skill reads a reverse index at all.** `grep -r used_by
  skills/` returns exactly `assess-change-impact/SKILL.md` — every other
  skill that touches the matrix (`generate-test-cases-from-usecase`,
  `audit-implementation-against-usecase`, `feedback-propose-matrix-correction`) goes
  forward, use case → components, which the matrix's own `use_cases[id]`
  key already answers unambiguously (there's only one place that id can be
  keyed). The reverse direction is structurally the harder one — a
  component id could in principle appear in the matrix's `components` key,
  the catalog's `used_by`, or a use case's un-indexed body prose — and
  `assess-change-impact` is, today, the only skill that has to reconcile
  that.

## 4. What OWL/RDF would actually add, if adopted

Keeping the two apart, since the question named both and they're different
tools:

- **RDF** is a generic graph data model — everything is a `(subject,
  predicate, object)` triple, queried with SPARQL. Applied here, an edge
  like "TMFS020 references TMFC020" becomes a triple instead of an array
  entry; the genuine advantage over an array is that the *predicate* itself
  becomes a first-class, queryable thing (`references` vs. `matrix_credits`
  vs. `mentions_in_body` could each be distinct predicates), and provenance
  can be attached per-triple (RDF reification, or named graphs) rather than
  bolted on as an extra object field.
- **OWL** sits on top of RDF and adds a *schema* layer with teeth: class
  hierarchies (`ODAComponent rdfs:subClassOf Artefact`), property
  restrictions, and — the actual reason to reach for OWL specifically, not
  just RDF — a **reasoner** that can infer new triples from the schema
  (transitive closure across chained relationships, automatic consistency
  flags when two asserted facts contradict the schema's constraints).

Where either would map onto something real in this corpus: the
frontmatter-vs-matrix disagreement (§2, §3) is genuinely a multi-source,
provenance-tagged graph problem — that part of the pitch is not imaginary.
The open question is whether *this specific implementation* — a full
Semantic Web stack, a reasoner, SPARQL — is the right-sized way to get that,
or whether the graph-shaped part of the problem can be had without it.

## 5. Grounding check — does this corpus and skill set actually need it?

| Capability OWL/RDF would bring | Genuinely needed here? | Why |
|---|---|---|
| Formal class subsumption / inference over types | **No** | Three flat artefact types (`use-case`/`component`/`api`), §5.0's envelope — no subtype hierarchy exists anywhere in the source data (TM Forum's own component/API catalogs are flat lists, not taxonomies) for a reasoner to classify over. |
| Transitive/chained impact queries (e.g. "use cases affected by an API exposed by a component that itself depends on this API") | **Marginally, and already answerable** | Every such chain in this corpus is one or two hops, and both hops are already fully materialized as plain arrays in the existing catalogs — reading two JSON files answers it exactly as completely as a SPARQL `property-path` query would, for a corpus this size. |
| Automatic consistency checking between frontmatter and the matrix | **Partially — and the repo already chose prose over automation here, deliberately** | `matrix-discrepancies.md` narrates *why* each disagreement exists (a bibliography-only References section, a matrix that lags a document's own edits), not just that ids differ. An OWL reasoner would surface the *that* — an inferred inconsistency triple — not the *why*, which is exactly the part this repo's own design (spec.md §5.4) treats as the valuable half. |
| Reverse/multi-directional lookups without per-skill, hand-written reconciliation logic | **Yes, this was real** — didn't require RDF to fix; resolved directly in `components.json` (§8.2). |
| Standard interchange with an external semantic-web consumer | **No current consumer** | Nothing outside this repo's own skills reads `knowledge/` today. spec.md §7's own forward-looking note about external reach is an MCP server — a thin read-only wrapper over the existing JSON index files, explicitly, not a SPARQL endpoint. |

## 6. Does TM Forum itself publish an OWL/RDF form of any of this?

No. Checked directly rather than assumed: TM Forum's SID/eTOM models are
distributed as a Sparx Enterprise Architect (UML) model with XMI export —
the same source `spec.md` §7 already plans to pipe through **"XMI →
structured YAML → Markdown,"** not through OWL. Searching for an official
OWL/RDF distribution of SID or the Open API catalog turns up academic
ontology-matching research that *converts* TM Forum's published UML/XML
models into OWL for the researchers' own network-ontology-matching
experiments — a third party doing the conversion for a different purpose,
not something TM Forum authors, versions, or maintains as a first-class
deliverable the way it maintains the YAML component specs and Swagger API
schemas this repo already caches (§5.2/§5.3). No JSON-LD or comparable
semantic annotation was found on TM Forum's own published Open API schemas
either.

This matters directly against principle 3 (`references/` is the raw cache;
`knowledge/` is regeneratable from it plus public sources — nothing is
hand-authored knowledge). Every other artefact type this repo caches mirrors
a real upstream TM Forum publication and can be diffed against it on refresh
(§6). An OWL ontology here would have no such upstream counterpart to mirror
— it would be a freestanding modeling effort this repo would own and
maintain forever, a fundamentally different kind of work than the
caching-and-converting every `tools/*.py` script currently does.

## 7. Cost side, weighed against this repo's own stated principles

- **Principle 6** ("optimize for a skill doing a single lookup… not a corpus
  scan") — a SPARQL query layer is a step *away* from "one JSON file read,"
  the thing every shipped skill's instructions are already written around.
- **Principle 7** (idempotent, byte-identical regeneration, enforced today
  by `validate_envelope.py` gating `build_index.py`'s own successful exit) —
  an OWL reasoner's inferred triples are a function of the reasoner
  implementation and version, not just the input data; keeping generated
  output byte-identical and diffable gets materially harder the moment
  inference (as opposed to plain materialization) is in the loop.
- **A new class of runtime dependency, with no existing precedent in this
  repo.** `tools/_yaml_lite.py` already hand-rolls a *deterministic* YAML
  emitter specifically to avoid PyYAML's non-deterministic-formatting
  default — this repo is already visibly careful about exactly the kind of
  determinism risk an OWL reasoner (`owlready2`, or an external triple
  store + SPARQL engine) would reintroduce, for a capability §5's table just
  found nothing in the current skill set actually exercises.
- **Corpus scale.** 24 use cases, 31 components, 51 API rows (§3). This is
  not a "not yet, but it will be" scale problem — even at 5–10× today's size
  it would still comfortably fit the "read one JSON file" model every skill
  here is built around.

## 8. What was actually built

§§4–7 still stand as the reason **skills keep reading plain JSON, not
SPARQL, at query time** — that recommendation wasn't overridden, and §8.4's
RDF/OWL export is built as a secondary, derived artifact specifically so it
doesn't disturb that. Two things *were* overridden, both on explicit
direction, and both are built:

### 8.1 Name the relationship vocabulary explicitly

"Ontology," in the modest sense that actually helped here, just means: give
each relationship type a name and track its provenance instead of collapsing
everything into one undifferentiated list. That's the design principle
behind both §8.2 and §8.4 below — `confirmed` / `frontmatter_only` /
`matrix_only` as three explicitly named states, carried all the way through
from the JSON index to the RDF export.

### 8.2 The reconciliation moved into the data — built

v1 of this spec logged a generated reverse cross-reference file as a
deferred, speculative idea, on the reasoning that only one skill needed it.
**Overridden**: the underlying data was fixed directly rather than kept as
two files a reader has to reconcile. `tools/build_index.py`'s
`add_reconciled_component_used_by` now computes `components.json`'s
`used_by` as the union of each use case's forward `links.components` and
`usecase-component-matrix.json`'s own reverse index, tagging every entry:

```json
{
  "id": "TMFC020",
  "...": "...",
  "used_by": [
    {"use_case": "TMFS001", "source": "confirmed"},
    {"use_case": "TMFS016", "source": "confirmed"},
    {"use_case": "TMFS020", "source": "matrix_only"},
    {"use_case": "TMFS021", "source": "matrix_only"}
  ]
}
```

Verified against the §2 numbers directly: TMFC020's `used_by` now has all 4
real dependents, 2 `confirmed` and 2 `matrix_only`, in one field, one read.
`apis.json`'s `used_by` is deliberately unchanged (plain id list) — the
matrix has no API-level data, so there is nothing to reconcile for an API id;
this is a real structural asymmetry between the two artefact types (§3), not
an inconsistency to fix later. Regenerating both is still one command
(`python tools/build_index.py`), still verified idempotent (byte-identical
across two consecutive runs on unchanged input). The forward direction (one
use case → its components, `matrix-discrepancies.md`'s original subject) is
untouched by this — that direction still has no single "correct" merged
answer for the ambiguous both-direction cases (`matrix-discrepancies.md`'s
own TMFS020 note), which is a different kind of disagreement than the
reverse direction's completeness gap this fixes.

### 8.3 Revisit trigger for OWL's *own* strength — unchanged

The one place OWL's actual strength — subsumption over a real type hierarchy
— would first apply to this corpus is `knowledge/etom/`/`knowledge/sid/`
(spec.md §7). eTOM **has now landed** (`GB921` v26.0, `spec-etom.md`) and
`processes.json` carries genuine subtype structure (`parent`/`children`, a
7-level process hierarchy); SID is still reserved. The revisit trigger is
therefore now half-met on the *data* side — what's still missing is the
second half: a skill that genuinely needs "a query about a parent process
should match its children" reasoning. `explain-etom-process` deliberately
does **not** — it reports the immediate `parent`/`children` and stops
(spec-etom.md §8). Until a skill actually needs transitive hierarchy
queries over `processes.json`, a reasoner still isn't earning its keep;
plain `parent`/`children` traversal in the consuming skill covers it.

### 8.4 A derived RDF/OWL export — built, on request, as a secondary artifact

`tools/build_ontology.py` reads the same three JSON catalogs (specifically
`components.json`'s now-reconciled `used_by`, §8.2 — not a second, separate
extraction from the matrix) and emits `knowledge/index/ontology.ttl`: one
Turtle file that is simultaneously a small OWL ontology and its RDF instance
data.

**What it models** — deliberately scoped to the cross-reference layer this
spec is about, not a re-encoding of every document's content (§6's point
about not hand-authoring a freestanding ontology still applies to *content*,
just not to *this* graph, which already exists as materialized JSON and is
only being re-expressed):

- Three disjoint classes (`owl:disjointWith`, pairwise) under a common
  `:Artefact` superclass — `:UseCase`, `:Component`, `:API` — mirroring
  spec.md §5.0's envelope typing exactly, nothing invented beyond it.
- Envelope + use-case-extension fields as datatype properties (`:id`,
  `:version`, `:status`, `:path`, `:maturity`, `:approvalStatus`,
  `:releaseStatus`), plus `:apiFamily` since `apis.json` mints one
  individual per `(id, version)` row and `:id` alone doesn't group a
  family's versions.
- The cross-reference graph as named object properties, not RDF reification:
  `:dependsOnComponent` (asserted whenever either source says so) with two
  `rdfs:subPropertyOf` sub-properties, `:documentReferencesComponent` and
  `:matrixCreditsComponent`, carrying exactly the `frontmatter_only` /
  `matrix_only` / `confirmed` distinction from §8.2's JSON — and
  `:dependsOnAPI`, with no sub-properties, since there's nothing to
  distinguish for an API. Inverse properties (`:componentUsedByUseCase`,
  `:apiUsedByUseCase`) are declared with `owl:inverseOf` *and* asserted as
  explicit triples in both directions — consistent with §7's determinism
  concern: nothing in this file requires a reasoner to query correctly.

**Verified, not just generated**: parsed clean with `rdflib` (installed
temporarily for this check only, not added as a project dependency —
consistent with §7's point about not introducing a reasoner/RDF-store
dependency the generator itself doesn't need, since it hand-emits Turtle
with no library). Round-tripped the exact §2/§8.2 example back out of the
`.ttl`: `id:TMFC020 :componentUsedByUseCase` returns all 4 use cases, and
`id:TMFS020 ?p id:TMFC020` returns `:dependsOnComponent` and
`:matrixCreditsComponent` (not `:documentReferencesComponent`) — the
provenance survived the RDF conversion correctly. Confirmed idempotent the
same way `build_index.py` is: byte-identical `.ttl` output across two
consecutive runs on unchanged input.

**Why this doesn't reopen §§4–7's conclusion**: this file is generated,
git-committed alongside the JSON it's derived from, and read by nothing in
`skills/` — no skill's instructions were changed to depend on it, no
reasoner or SPARQL engine was added anywhere in the dependency chain a skill
invocation runs through. It exists for a reader who specifically wants an
RDF/OWL view of this corpus (Protégé, a graph tool, a linked-data
experiment) — exactly the audience named in the request — without moving
that requirement onto the JSON-reading path every skill's instructions
assume. If a skill ever did need to *query* this file rather than a human
opening it, that would be a new, separate decision — SPARQL over a
100-artefact corpus is still not obviously better than the direct JSON
lookups already in place — but nothing here forces that decision now.

## 9. Decision

Both open questions from v1 were revisited and resolved the opposite way, on
explicit direction, and both are built and verified:

- **The frontmatter/matrix disagreement is now reconciled in the data
  itself** — `components.json`'s `used_by` (§8.2), not left as an
  instruction for each skill to re-derive. `assess-change-impact`'s Step 2
  is simplified accordingly.
- **A derived RDF/OWL export exists** — `tools/build_ontology.py` →
  `knowledge/index/ontology.ttl` (§8.4), regenerate any time after
  `build_index.py` with `python tools/build_ontology.py`.

What v1's grounding analysis (§§4–7) still settles, and what remains true
after both overrides: `knowledge/index/`'s **primary**, skill-facing lookup
path stays plain JSON, one file read, no reasoner and no SPARQL engine in
any skill's dependency chain — the RDF/OWL export is additive, not a
replacement, and nothing here reopens that question unless a real consumer
of the `.ttl` file's own query capabilities shows up (§8.4's closing note).
