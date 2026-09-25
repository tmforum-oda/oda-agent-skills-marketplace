# Refresh runbook — assisted track

Precise, step-by-step execution of spec.md §6.1. Written so someone other than
the original builder can run a refresh without re-deriving the TM Forum
search-URL trick, the download-modal quirk, or any of the judgment calls
Phase 1–4 already hit once. If you're only refreshing components/APIs
(no login needed), skip to "Automated track" near the bottom — you don't need
any of the browser steps above it.

Needs: a TM Forum website member login (a personal account with the free
member tier is enough — this is not a paid-tier gate), and a browser you can
drive interactively (this repo has been built by driving Chrome via the
`claude-in-chrome` MCP tools; a human clicking through manually works exactly
the same way).

## 1. Check for a new IG1228

1. Open `https://www.tmforum.org/resources/introductory-guide/how-to-use-oda-using-open-apis-to-realize-use-cases-v31-0-0-ig1228/`
   (or search `tmforum.org` for "IG1228" if that slug has moved — TM Forum's
   catalog URLs embed the version number, so a new version gets a new slug,
   not a redirect).
2. Read the version number and publish date off the page. Compare against
   `references/ig1228/IG1228_*.pdf`'s filename (it's version-stamped) and/or
   `knowledge/index/usecase-list.json`'s `generated_from` field.
3. If unchanged, stop here — nothing to refresh on the assisted track this
   cycle. (You may still want to run the automated track below; it's cheap
   and safe to run anyway.)
4. If changed, download **both** the DOCX and PDF of the new version to
   `references/ig1228/`, named the same way as the existing file
   (`IG1228_How_to_use_ODA_Using_Open_APIs_to_Realize_UseCases_v<X>.<Y>.<Z>.pdf`
   / `.docx`). Leave the old version's files in place — nothing currently
   depends on only one being present, and keeping the prior version is free
   provenance if a diff question ever comes up.

## 2. Regenerate the two IG1228-derived index files against the new PDF

```bash
python tools/extract_usecase_list.py references/ig1228/IG1228_..._v<X>.<Y>.<Z>.pdf
python tools/extract_usecase_matrix.py references/ig1228/IG1228_..._v<X>.<Y>.<Z>.pdf
```

Both scripts default to the *old* filename if you don't pass the new path
explicitly (`DEFAULT_PDF` near the top of each file) — always pass the new
path on a refresh, and update `DEFAULT_PDF` in both scripts afterward so the
next refresh's no-argument default points at the current version.

Both scripts fail loudly (an `assert` on header text, not a silent
misparse) if TM Forum has changed the table layout since v31.0.0 — see the
docstrings in `tools/extract_usecase_list.py` and
`tools/extract_usecase_matrix.py` for exactly what's being asserted. If one
trips, the table has genuinely moved and the per-part column config
(`PART_CONFIGS` in `extract_usecase_matrix.py`, `COL_*` constants in
`extract_usecase_list.py`) needs re-deriving by hand against the new PDF —
don't loosen the assertion to make it pass.

## 3. Diff the new roster against what's already converted

`tools/extract_usecase_list.py`'s output (`knowledge/index/usecase-list.json`)
is the full IG1228 roster including `planned`/`not available` rows;
`knowledge/index/use-cases.json` (from `build_index.py`) is what's actually
converted. There's no scripted diff for this step yet (task 5.2 built
`refresh_report.py` for the *index* diff, not this roster-vs-corpus one) —
compare by hand:

- Any id in `usecase-list.json` with `status_in_ig1228: "Available"` that
  has **no** matching directory under `knowledge/use-cases/` is new — needs
  a full first-time download (step 4 below).
- Any id already converted: check whether IG1228's chapter-2 matrix
  (`usecase-component-matrix.json`) or its own catalog page (step 4.3 below)
  shows a version bump since `knowledge/use-cases/<id>/<id>.md`'s own
  `version` field. If unchanged, skip it.
- A `status_in_ig1228` transition (`planned` → `Available`) is itself
  refresh-report-worthy even before you've downloaded anything — note it,
  `refresh_report.py` picks it up once the new document lands in
  `use-cases.json`.

## 4. Download each changed/new use case's DOCX

This is the step that cannot be scripted — TM Forum's download is a
JS-driven modal keyed to your logged-in session, not a stable direct URL
(confirmed while building the pilot, spec.md §6.1).

1. Go to `https://www.tmforum.org/?s=TMFSxxx&post_type=product` (substitute
   the real id — TM Forum's search does not do partial/fuzzy id matching
   reliably, use the exact id).
2. Sort results newest-first if not already.
3. **Prefer Production over Pre-production** when both appear for the same
   id. Exception, hit once already (TMFS019): a "Production" link can point
   at a stale, superseded document if TM Forum's own catalog hasn't been
   fully re-linked after a split or restructure. Tell-tale sign: the page
   title/URL slug doesn't match what you expected (e.g. missing a "Part II"
   that the search-result listing showed) — if that happens, go back and
   take the Pre-production/other listed link instead, and note the
   discrepancy in this cycle's refresh notes. Don't just trust the label.
4. On the document's page, click Download and save the DOCX (and PDF, if
   offered — not every catalog page offers both; TMFS019A/B only ever had a
   DOCX) to `references/use-cases/<ID>/<ID>_v<version>.docx`, matching the
   existing naming convention (see any existing file under
   `references/use-cases/` for the exact pattern).
5. Read the document's own catalog page for its General Information table —
   you'll need `status`, `maturity`, `approval_status`, `release_status`,
   `team_approved` date, `published` date, and IPR mode for step 4.3's
   metadata pass. Screenshot or copy these values now; the page is easy to
   navigate away from and re-finding it later costs another search.

## 4.1 Convert

```bash
python tools/docx2md.py references/use-cases/<ID>/<ID>_v<version>.docx
```

Writes/overwrites `knowledge/use-cases/<ID>/<ID>.md`. Check
`links.components`/`links.apis` came out non-empty if the source document has
a real References section — an empty result on a document that clearly lists
components is a parser miss, not a fact about the document (this is exactly
how the three bugs in Phase 4 were found; see tasks.md 4.2 for what they
were and how they were fixed — if a fourth document shape trips the parser
the same way, fix `docx2md.py` the same way: find the real cause in the raw
docx XML, don't work around it in the runbook).

## 4.2 Re-apply catalog metadata

```bash
python tools/add_usecase_metadata.py <ID>
```

Re-running `docx2md.py` always emits fresh `"TODO"` stubs for the
catalog-page-only fields (status/maturity/approval_status/release_status/
team_approved/published/source.origin/source.license) — this step is not
optional, even on a version-number-only bump. Use the values you captured in
step 4, step 5.

## 5. Regenerate the corpus-wide index and matrix cross-check

```bash
python tools/build_index.py
```

Runs `validate_envelope.py --strict` as its own last step and refuses to
finish if any artefact is still carrying a `TODO` stub — that's your signal
step 4.2 was skipped or incomplete for some id.

Re-check `knowledge/index/matrix-discrepancies.md` for the ids you touched
this cycle: does the new document's own References section still agree or
disagree with the matrix the same way it did last cycle? A disagreement that
flips (agreed last cycle, disagrees now, or vice versa) is worth a line in
this cycle's `CHANGELOG.md` entry, not just a silent table update — it's
exactly the kind of signal spec.md §5.4 keeps this file around to catch.

## 6. Automated track — components and APIs (no login needed)

Safe to run every cycle regardless of whether anything changed on the
assisted side above; components/APIs can gain new versions on their own
schedule.

```bash
python tools/fetch_component.py --refresh-map     # re-list the tagged component repo once
python tools/fetch_component.py --all-referenced   # every TMFCxxx any use case links to
python tools/fetch_api.py                          # every API any cached component.yaml references
python tools/fetch_api_samples.py                  # optional — best-effort, needs org GitHub access
```

See task 5.3 in `spec/tasks.md` for what "confirm nothing rewritten
unexpectedly" means in practice, and note the caveat recorded there: as of
this writing these two scripts always overwrite their output files on every
run (including bumping `source.retrieved` to today even when the fetched
bytes are byte-identical), so "nothing changed" currently has to be verified
via `git diff --stat` after the run, not by watching the scripts skip files.

## 6a. eTOM (`GB921`) — assisted, but on the Frameworx schedule

eTOM ships with TM Forum's **Frameworx release train (~2×/year)**, not
IG1228's 8-week cadence, so most cycles have nothing to do here. The workbook
is member-gated (same login as step 1).

1. Check the TM Forum Frameworx / `GB921` catalog page for a version newer
   than the `version` in `knowledge/etom/GB921.md`. If unchanged, skip the
   rest of this section.
2. Download the new **`GB921_..._Excel_v<ver>.xlsx`** (and the
   `etom_v<ver>.json` if still published) into `references/eTOM/`, replacing
   the old files. Rename nothing — `build_etom.py` hard-codes the v26.0
   filenames; update the constants in that script (and `spec-etom.md` §3/§4)
   when the version bumps.
3. Regenerate:

```bash
python tools/build_etom.py --retrieved <YYYY-MM-DD> [--origin <url>]
python tools/build_index.py     # also rebuilds knowledge/index/etom-index.json
```

4. Review `knowledge/index/etom-anomalies.md` — it's regenerated in full each
   run. A big swing in the "Build summary" counts, or the eTOM↔component
   resolution rate in `etom-index.json`'s `summary` moving sharply, is worth
   a line in this cycle's `CHANGELOG.md` (see step 7).

## 7. Generate the refresh report

```bash
python tools/refresh_report.py
```

Compares the just-regenerated `knowledge/index/*.json` against the last
git-committed version and appends a dated entry to `CHANGELOG.md` — see
`tools/refresh_report.py`'s own docstring for exactly what it diffs and how
it decides what counts as reportable. Run this **after** steps 5 and 6, not
before — it reads whatever is currently on disk, uncommitted changes
included, and diffs against `git show HEAD:...`.

Read the generated entry before committing. It's a draft, not
gospel — spec.md §6.3 specifically wants maturity/status transitions
(`Beta → GA`) called out; if the report's wording doesn't make a transition
you know happened this cycle obvious, edit `CHANGELOG.md` by hand before
committing rather than trusting the auto-generated phrasing blindly.

## 8. Commit

One commit for the cycle, following the existing `git log` pattern (one
commit per phase/refresh-cycle, not one per file). Stage `references/`,
`knowledge/`, and `CHANGELOG.md` together — see spec.md §10 for why
`references/` is committed at all (member-gated content, not independently
re-obtainable from a fresh clone without a login).
