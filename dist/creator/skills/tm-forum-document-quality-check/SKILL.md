---
name: tm-forum-document-quality-check
description: Checks one TM Forum document at a time for IP and licence issues - undeclared copied text (word-for-word comparison against held sources, quoted web spot checks), weak credits (Title, Author, Source, Licence, Date), the publication date and age of each credited source and which one is core to the document, borrowed images, ownership, dependence on other standards bodies, Automation Indicators, ODA content, authors and, as a marked addition outside the IP references, editorial consistency - and saves the findings and scores in `work/documents/<key>/` (`report.md`, `entry.json`) without rendering a Word report. The report skill tm-forum-document-quality-individual (sibling folder `../tm-forum-document-quality-individual/`) runs it for a document that has no record yet, and reuses the record when it has one. Use it directly when the user asks only to check, scan or score a document without asking for a report, or to re-check a document that already has a record.
---

# TM Forum Document Quality: Check

> **Disclaimer:** Using this skill is not legal advice. It does not
> provide a valid legal defence for any infringement, misuse or other
> abuse of intellectual property or other rights. Responsibility for how
> material is used stays with the user. Get qualified legal advice where
> rights are in doubt.

## Where things live

This skill is the `${CLAUDE_PLUGIN_ROOT}/skills/tm-forum-document-quality-check/` folder (originally of the IP-scan-tool
repository). It holds every script and reference file the IP and licence
skills use: `scripts/` and `references/` (reference sets, the IPR Policy
copy, and two notes files read only when needed: `reference-citations.md`,
the citations of the six references, and `scoring-notes.md`, how the
reference sets and class rules were set). Run the commands below from
this folder (`python -I scripts/...`; the folder name has a space, so
quote it in a path). Everything else sits at the repository root:
`source/` (documents checked), `sdo-sources/` (held sources for the
copied-text check) and `work/documents/<key>/` (each document's working
files, its findings in `report.md` and its record in `entry.json`).
Scripts find their reference files relative to themselves, so the
repository works wherever it is checked out.

The report skill that runs this check:

- `tm-forum-document-quality-individual` (the sibling folder `../tm-forum-document-quality-individual/`): renders the document's full IP and
  licence check report from `report.md`.

## Running without the repository

The check runs without the rest of the IP-scan-tool repository, as long as
this whole folder (`scripts/` and `references/` together) is present. Create
the document's folder (`work/documents/<key>/` or any folder) yourself.

- **What still works:** every check on a single document, and its scores,
  which use the frozen reference sets in `references/`.
- **What needs the repository:** reusing an earlier record of the same
  document, the combined report (it reads every `work/documents/<key>/entry.json`)
  and rebuilding reference sets. Without the records, check the document
  afresh and say in the report that no earlier record was available.
- **No held sources:** without `sdo-sources/` (or another folder passed to
  `--sources`), the copied-text check can't run and the dependence and
  citation-date scripts say the folder wasn't found. Report the copied-text
  check and copying measures as **not checked**, never as "no matches", and
  list it under the report's coverage gaps.

When something the check needs is missing, the scripts stop with a one-line
`cannot run:` message naming the missing file, folder or Python package and
what to do, or print a `WARNING:` line and carry on with less. Read those
lines: a `cannot run:` means that step has no result, and a `WARNING:`
names a check that wasn't done. Each one is a coverage gap to state in the
report, never something to pass over or to fill in by guessing.

## Check once, reuse the record

A document is checked once. When `work/documents/<key>/` already holds
`entry.json` and `report.md` for the same document, the skills reuse them
and don't run this check again. Run it again only when the user asks to
re-check the document, or the document itself has changed (a new version
or draft); then replace the folder's contents.

**`report.md` is the one source of the report.** Every Word and HTML
report is rendered from `work/documents/<key>/report.md`, never edited
itself. To revise a report (a finding, a score after a rule change), edit
`report.md`, refresh its score block with `document_scores.py`, and render
again: the .docx and .html are replaced and always agree with each other.
Edits made in Word are lost at the next render.

All rates and scores are per 1,000 words of the document's text.

**Word counts.** The document's size is the `text.txt` word count: give
that in the report and use it for the ownership score. `dependence.py` and
`oda_score.py` print it beside their own count, because they leave out
contents lines or the document's own identifier before counting; their
rates use their own count and are quoted as printed. `ai_indicators.py`
uses the `text.txt` count. The counts differ by a few per cent; don't mix
one script's count with another script's rate.

## How to run this skill

These rules apply to every response this skill produces, from the first
to the last:

1. **The disclaimer is always visible.** Start every response with the
   disclaimer above, word for word, as a blockquote. Put it at the top of
   any file this skill writes too. Never shorten it, move it lower or
   leave it out, even in follow-up responses or ones that only answer a
   short question.
2. **Each reference gets its own section.** All six references always
   get a section headed `## Reference N: <title>`, numbered as in
   `references/reference-citations.md`, in that order. Put only that
   reference's findings in its section; never mix two references in one
   section or combine their headings. A reference that doesn't apply gets
   its heading and one line saying why (for example "Doesn't apply: the
   document contains no open-source software, code or SBOM."), nothing
   else. Anything that doesn't come from one of the six references goes in
   a separate section headed `## Not from the references`, after
   Reference 6. The one exception is `## Editorial consistency check`,
   which sits above Reference 1 (see rule 6).
3. **The reference is visible while it's in use.** Directly under the
   heading of each reference that has findings, before any findings, show
   that reference's citation from `references/reference-citations.md`
   (title, edition, publisher, link) and the sections or clauses you're
   relying on. Mark each finding with the clause it comes from (for
   example `IPR Policy §10.1`). Read that file for the citations and for
   the central test of Reference 1 (was the material the Contributor's to
   contribute?).
4. **Asking for provenance uses the template.** When the user needs to
   ask someone where third-party material came from or what rights apply
   to it, use
   [references/citation-request-template.md](references/citation-request-template.md)
   unchanged.
5. **Find issues; don't fix them.** This skill reports what it finds and
   the evidence for it: what the issue is, where it is, what it matches
   or breaks, and the clause or source it's judged against. It never
   suggests fixes or next steps: no "what to do", no recommended wording,
   corrected identifiers, suggested credits, rewrites, questions to put
   to the author, or "consider adding". Where a finding is uncertain,
   say what is uncertain and why, and stop there. Don't end the report
   with a list of fixes or an overall to-do list.
6. **Every run writes the findings to `report.md`.** Write the full
   findings, starting with the disclaimer, to `work/documents/<key>/report.md`. Directly after the
   disclaimer comes the title line `# IP and licence check: <document name>`,
   and directly under the title the document's score block from
   `document_scores.py` (see "Document score and entry.json"), unchanged,
   before anything else. Directly below the score block comes
   `## Editorial consistency check` (see "Editorial consistency"), then
   the reference sections. Don't render it to Word: the report skill
   that ran this check does that. When several documents are checked in
   one run, each gets its own folder and `report.md`.
7. **Hand back to the report skill.** When a report skill ran this check,
   go back to that skill's steps once `entry.json` and `report.md` are
   written. When the user ran it directly, the chat response is a
   summary: the disclaimer, one line for each of the six references (the
   number of findings, or "doesn't apply"), the scores with their classes
   in a small table, the worst findings in a sentence or two each, one
   line giving the editorial consistency score, class and counts (marked
   as an addition outside the IP references), and the folder's path.
8. **Check as deep as the evidence calls for.** Depth is stepped: a light
   floor for every document, doubled when the cheap first pass finds
   something, redoubled when what it finds is serious (see "Depth of
   check" below). Within a tier work in this order: extract and key
   extracts, credit check, images, held-source copy check, web check,
   scores, authors, editorial consistency, entry.json and document score,
   `report.md`. Don't read a whole file when a script's output
   or an extract answers the question.
9. **Report the current state only.** A report gives the findings and
   scores as they stand, as if checked once. It never describes how they
   were reached over time: no earlier runs, reruns, re-checks, cycles,
   addenda, before-and-after tables, earlier scores or classes, or what
   changed since a previous report. When a document is checked again,
   rewrite its report in full. Gaps are stated as they stand (what wasn't
   checked or confirmed), not as what a later pass added.

## Depth of check

How much work a document gets depends on what the cheap first pass finds.
Run the first pass (extract, key extracts, credit check, image scan and
the held-source copy check), then pick the tier:

```bash
python -I scripts/triage.py "<output-dir>" --sources "<sources-dir>" [--items <weight:cited,...>]
```

| Tier | Trigger | What it asks for |
|---|---|---|
| **Light** | Nothing found: no passage credited to a source outside TM Forum, no word-for-word copying from held sources, no judged ownership item | The floor: the credit check, contact sheets for the unflagged images, the figure-label check on figures whose caption or text names their parts, each credited source opened once, and batch 1 (7 sentences) of the web check, stopping if it is clean |
| **Doubled** | Something found, but the provisional poorly cited score isn't above 0.15 per 1,000 words | Every credited passage placed (compared with its source, or searched until found or each search has failed), all three web batches whatever the earlier ones found, flow-style, architecture and textbook-looking figures at full size one at a time, and the figure-label check on every figure that carries text |
| **Redoubled** | The provisional poorly cited score is above 0.15 per 1,000 words, or 10 or more words per 1,000 are copied word for word from held sources | The doubled work, plus the sections around each finding searched sentence by sentence, each credited source opened in full, every distinctive figure label set searched, and headers, footers and captions read for notice and credit problems |

The tier only goes up during a run. Run `triage.py` again with `--items`
each time items are judged, and when it rises, do the extra work. State
the final tier, what triggered it and which checks the tier left out, in
the report under `### Depth of check` in `## Not from the references`,
before `### Images`. A light tier is not a clean bill: it means the cheap
checks found nothing. The triggers come from the 38 reference documents
(`references/scoring-notes.md`); they are a guide to effort, not a score,
and have no class and no fixes.

## Reading a .docx

Don't read a Word file with python-docx or another paragraph reader:
TM Forum IG templates keep their text inside content controls, which
those readers skip, so the document looks empty. Use
`scripts/extract_docx.py` instead. It writes the body text, headers and
footers, footnotes, external hyperlinks, embedded images, the text
around each image (`images.txt`) and the text credited to outside
sources (`cited.txt`) to an output folder:

```bash
python -I scripts/extract_docx.py "<input.docx>" "<output-dir>"
python -I scripts/key_extracts.py "<output-dir>"
```

Put `<output-dir>` in `work/documents/<key>/` at the repository root,
where `<key>` is the document's short name (`IG1242`, `TAC-1012`). If the
folder already holds an earlier check of the same document, replace it.
`key_extracts.py` writes `key_extracts.txt` there: the notice and
licence lines, the Acknowledgements, the credited sources, the outside
links, any statements about AI use and the open-source and licence
mentions, each with its line number in `text.txt`. Use it to write the
reference sections, and open `text.txt` only at the lines an extract
points to or where a check needs more context. It is a guide to where to
look: a line its patterns miss isn't shown, so read further when the
document looks unusual (no notice found, no Acknowledgements section, a
document that discusses licences).

## Reading a .xlsx

A spreadsheet (for example a maturity-model workbook) is read with
`scripts/extract_xlsx.py` instead. It writes the same files to the same
folder, so every later step runs unchanged:

```bash
python -I scripts/extract_xlsx.py "<input.xlsx>" "<output-dir>"
python -I scripts/key_extracts.py "<output-dir>"
```

`text.txt` holds every cell with text (numbers are left out), sheet by
sheet, each sheet opening with a `Sheet: <name>` line. `cells.txt` gives the
same cells as `<sheet>!<cell>: <text>`: a workbook has no table of contents,
so give locations in the report as the sheet and cell (for example
"Customer (D1)!F23"). `notes.txt` holds cell comments, `headers.txt` the
sheets' page headers and footers, and `images.txt` each picture with its
sheet and anchor cell. A column headed "Source" ("Source of the
standard", "Standard source") credits its row in `cited.txt`: the text after
the source in the same cell, or else the row's longest text cell; a long cell
there that opens with no source is credited to "no source named", which
`credit_check.py` grades **none**. `image_scan.py` and `ai_indicators.py --docx` take
the .xlsx in place of a .docx; put the .xlsx path in `entry.json`'s
`docx` field.

The extract also writes `source_format.txt` ("xlsx"). From it,
`document_scores.py` and the combined report each add a note that the spreadsheet's scores aren't comparable with
those of the Word documents, because the reference sets, the per-1,000-word
rates and the editorial expectation were built from prose documents. Say
the same in `report.md` under `### Depth of check`. The rest of the check
is the same, with two points to state in the report: the web spot check
picks sentences of 10 to 40 words, so few cells qualify, and authors are
found only if the workbook has an Acknowledgements sheet.

## Reading a .pdf

Use a PDF only when the document isn't available as .docx or .xlsx. Turn it
into a minimal Word package first, then run every later step on that package
exactly as for a Word document (`extract_docx.py`, `image_scan.py`,
`ai_indicators.py --docx`, and the package's path in `entry.json`'s `docx`
field):

```bash
python -I scripts/pdf_to_docx.py "<input.pdf>" "<work/pdf/name.docx>"
python -I scripts/extract_docx.py "<work/pdf/name.docx>" "<output-dir>"
```

It keeps the text blocks in reading order, the pictures in place, the links
round the text they cover, running headers and footers (lines repeated in the
top or bottom band of three or more pages) out of the body, and the PDF's own
metadata (author, creator, producer, dates) as document properties. Say in the
report that the document was read from a PDF, and what that loses: Word's
structure, so tables and slides come out line by line (`authors.py` may miss
an Acknowledgements table; take the names from the page and write
`authors.json` by hand), and any text inside pictures or screenshots, which
has to be read from the rendered pages. For slide decks, view each page
whole as well as the contact sheets.

## Checking credits

```bash
python -I scripts/credit_check.py "<output-dir>" --sources "<sources-dir>"
```

From `cited.txt` and `images.txt` alone, with no web search, it grades each
credit on Title, Author, Source (a link) and Licence, the four parts
Creative Commons recommends (Reference 5), and on Date, a fifth part this
skill adds: the credit itself gives the work's publication date (a date
the skill finds only from a held copy or `citation-dates.json` doesn't
count, because the document's reader can't see it). Say in the report that
Date is this skill's addition, not part of the Creative Commons practice.
Passages are grouped by source,
so each source is judged once (a numbered reference-list entry counts as credited to its own link; links that wrap only a bare "[5]" marker or a blank are ignored, because some documents carry stale marker links to other entries' addresses, and if you see that, report it as a link observation); a credit is complete (all five),
complete with no date (Title, Author, Source and Licence only), partial
(any other one to four) or none. It also separates the images that have a credit to
a TM Forum deliverable, the images with another credit or source note, and
the images with nothing nearby. Report the grades under Reference 5. It
reports what a credit contains: it can't tell whether the credit points at
the right work or whether the text really comes from there. That needs the
source opened (see the web check).

### Citation dates and the core citation

The credit table has two more columns, **Published** and **Age (years)**,
and marks one source **(core)**. `credit_check.py` gets them from
`citation_dates.py`, which can also be run alone and writes
`citations.json` to the output folder:

```bash
python -I scripts/citation_dates.py "<output-dir>" --sources "<sources-dir>" [--core "<source>"]
```

- **Published.** Taken from the first of: a date in the credit itself
  (the source line, the reference-list entry a marker such as `[29]`
  points to, a `/2023/` path in the link, an arXiv identifier such as
  `2506.12469` for June 2025; "accessed" dates are skipped);
  the front page of a held copy in `<sources-dir>` whose file name
  carries a document number the credit names (`rfc6749.txt`,
  `28312-j50.docx`); or
  [references/citation-dates.json](references/citation-dates.json). The
  cell says which. A held copy's date is the date of the edition held,
  which may be later than the edition the document used: say so where
  the document names an edition.
- **Filling gaps.** When the web check opens a credited source (see
  "Credited passages"), note its publication date from the page or the
  document's front page, add it to `citation-dates.json` with its basis
  (the address opened), and rerun `credit_check.py` before writing the
  report. Don't search for a date on its own: a source the web check
  doesn't open stays "not found" unless the credit or a held copy dates
  it.
- **Age** is years from the publication date to the date of the run
  (`--as-of` sets another).
- **Core citation.** The outside source the document leans on most: the
  most credited passages, then the most mentions in the text of the
  document numbers its credit names. TM Forum's own sources (a TM Forum
  link or a TMF, TMFC, GB, IG or TR number) are left out. The automatic
  pick is a starting point: read the scope and introduction and, if the
  document plainly rests on another work (its declared base, or the
  specification it profiles), name that one with `--core` and say why.
  A work cited.txt doesn't list can be named too (for example
  `--core "A2A Protocol Agent Card specification v1.0"`); it is added as
  a row with 0 passages and dated the same way. A tool or site link (draw.io, a code host's home page) or a stray
  marker (such as `[0]` from `schemes[0]`) is never the core citation.

Report the table under Reference 5, and the core citation, its date, its
age and how it was chosen in one line under it.

### Outside works named with no citation

`credit_check.py` only sees text that carries a credit. A document can also
lean on outside works it only names. These are standards, protocols,
frameworks, runtimes, benchmarks and risk catalogues (for example "ODP-EL",
"REP (Ripple Effect Protocol)", "A2A JSON-RPC 2.0", "NIST AAI001",
"BIRD-SQL"), named as the basis of a field, rule or value with no citation
anywhere. Find them while reading `text.txt` for the editorial check: look at
acronyms and proper names in the normative sections, templates, tables and
code blocks. A named work counts when **all** of these hold:

- it isn't TM Forum's own (a TM Forum name, or a TMF, TMFC, GB, IG or TR
  number);
- the document relies on it, by saying a field, rule, value or design is
  based on, follows, maps to or is inspired by it, or by using it as a
  field's value; a passing mention doesn't count;
- it has no entry in the document's References or Abbreviations, no outside
  link next to it, and no `cited.txt` credit.

Under Reference 5, after the credit check, add a section headed
`### Outside works named with no citation`, with one row per work: **Work as
named**, **Where it is named** (section numbers from the table of contents),
**What the document attributes to it** (quote it), and **Citation given**
("none", or what partial pointer there is, such as a link styled in a figure
with no address). Say in one line that these works are named, not
reproduced, so they aren't ownership items and don't change any score. If
they are also an editorial "incomplete references" finding, say so in one
line: there they are an editorial finding, here a credit finding. When the
document names none, write "None found." under the heading. As everywhere
in this skill, report the finding without saying what the citation should
be.

## Checking images

Check every image listed in `images.txt`, plus any in `media/` that it
doesn't list (those sit in headers or footers, usually logos). Images
are where third-party material is easiest to miss, because no text
check sees inside them. Work down this ladder, so most pictures cost
little and the ones that need a real look get it:

1. **Credited images (from `credit_check.py`).** An image with a credit or
   source note next to it needs no search to find its origin: grade the
   credit and, if the weight of the item needs it, open the credited source
   once. An image whose credit names a TM Forum deliverable (TM Forum,
   TMF/GB/IG/TR numbers, SID, eTOM) is TM Forum's own, or a contributing
   Member's own, and needn't be looked at for outside origin. Only a credit
   counts here: a mention of ODA or TM Forum in the surrounding text is not
   a credit, and an image with one still has to be looked at.
2. **Flagged images.** Run the automatic scan, which flags clip-art, icons
   and other artwork of outside origin:

   ```bash
   python -I scripts/image_scan.py "<input.docx>" "<output-dir>"
   ```

   It writes `image_flags.txt` and checks every picture in the document for:

   - **Metadata:** Office icons inserted from Word's Insert > Icons, a
     picture whose name or alt text says icon, clip art, graphic or stock,
     WMF/EMF pictures (the Office clip-art format), and author, copyright,
     creator or software fields inside the picture file.
   - **Pictograms** (needs Pillow and numpy; it says so if they're
     missing): small, isolated, irregular shapes that aren't text, boxes,
     lines, arrows or circles. Each is reported with its size and position
     as **multi-colour** (typical of clip-art and illustrations) or
     **monochrome** (typical of icons).

   Known TM Forum images, such as the logo, are recognised and not flagged.
   The pictogram check is a heuristic: it can flag a shape that's the
   author's own (for example a stylised arrow) and can miss artwork. Every
   flag must be confirmed by looking at the image, one image at a time:
   say what each reported shape is (clip-art figure, icon set, photo, or a
   false alarm such as an arrow).
3. **The rest, on contact sheets.** Put the pictures that are neither
   flagged nor credited on contact sheets, twelve to a sheet:

   ```bash
   python -I scripts/contact_sheets.py "<output-dir>"
   ```

   It leaves out the flagged pictures (`image_flags.txt`) and the credited
   ones (the credits `credit_check.py` finds in `images.txt`) by itself;
   `--skip` adds more, `--include-flagged` and `--no-auto-skip` put them
   back.

   Look at each sheet once. They show a picture's style, so look for one
   that differs from its neighbours: generated-looking artwork, a
   screenshot, a slide cut from elsewhere, stock pictures inside a figure,
   blurred or low-resolution crops. Then look at each outlier on its own.
   Sheets can't show labels or credits and can't show that a diagram in the
   document's own style was adapted from a textbook or another well-known
   figure, so if a figure resembles one (a well-known agent, architecture
   or lifecycle diagram), look at it on its own as well.
4. **For each image that was looked at on its own**, in this order:
   1. **Note any text in it:** labels, titles, legends.
   2. **Read its context** in `images.txt`: the caption and the paragraphs
      either side. A "Source:" note, a citation or a link to an outside
      work there means the image may come from that work.
   3. **Compare it with any cited source.** Open the source (the paper,
      page or standard) and check whether the same figure is in it. If it
      is, the image is a reproduction, even if it's credited.
   4. **Search its distinctive labels,** only if the image has text and
      isn't plainly TM Forum's own. Search two or three of its most unusual
      labels together in quotation marks (for example `"User as an
      Operator" "User as a Collaborator"`). Matching labels on an outside
      page or paper means it was copied or adapted from there.
   5. **Look for signs of outside origin:** another organisation's logo or
      watermark, a visual style unlike the rest of the document, a
      resemblance to a well-known figure (such as a textbook diagram), or
      a screenshot of another product.

5. **Figure-label check (a named step; it feeds `--figure-mismatches`).**
   For each figure whose caption or surrounding text names its parts
   (stages, steps, roles, streams, layers, levels, flow names), view the
   figure at full size and compare its labels with that text. Each label
   that contradicts the text (a stage named differently, a step missing or
   added, a number that differs) is one mismatch: list it in the report
   with the figure, the label and the text it contradicts. A contact sheet
   can't show labels, so a figure seen only on a sheet hasn't had this
   check: don't record 0 mismatches for it. At the light tier do the check
   on figures whose caption or text names parts; at the doubled and
   redoubled tiers on every figure that carries text.

Report every image in a table under `## Not from the references` with
its file name, its figure number or caption, what `image_scan.py`
flagged (or "none"), whether its labels were compared with the text
(**compared**, with the number of mismatches, or **not compared**), and one of: **own work**
(TM Forum's, nothing suggesting otherwise; say "contact sheet" or
"credited to TM Forum" where that is how it was checked), **reproduced**
or **adapted** (name the source, and whether it's credited), or
**unknown** (say what makes it uncertain). Clip art and icons are listed
too, as **clip art/icons, excluded**.

## Checking for undeclared copied text

Run both checks on any draft the user asks about, especially one written
with GenAI help. Report the results under `## Not from the references`,
in two parts headed `### Copied-text check` and `### Web spot check`.
Neither check proves a passage was or wasn't copied: a person decides
each finding, using the citation request template where the source needs
to be asked.

### Check 1: copied-text check against held sources

Compares the draft with source documents the user holds and reports every
stretch of 12 or more words the draft shares word for word with one of
them.

```bash
python -I scripts/copy_check.py "<output-dir>/text.txt" "<sources-dir>"
```

- `<sources-dir>` is a folder of the documents the user is worried
  about: ISO/IEC standards, analyst reports, vendor papers, books. This
  repository keeps the free standards it holds in `sdo-sources/<body>/`;
  use that folder, or ask the user for another folder's path (don't
  guess it).
- It reads .txt, .md and .docx sources, and .pdf if PyMuPDF is
  installed. It lists any file it couldn't read under "Not checked";
  report those, because those sources weren't checked.
- Matches with TM Forum's own text (the §14.1 notice, other TM Forum
  deliverables) are expected and don't need declaring. Say so, rather
  than leaving them out.
- `--n` (run length, default 8) and `--min-words` (default 12) can be
  lowered to catch shorter copied phrases, at the cost of more false
  alarms.
- It only catches word-for-word copying. Close paraphrase, typical of
  GenAI output, needs a person to compare the passages.

### Check 2: web spot check

Searches the web for distinctive sentences in quotation marks, to catch
text copied from sources the user doesn't hold, and opens the sources the
draft credits.

```bash
python -I scripts/spot_check_candidates.py "<output-dir>/text.txt" --count 20
```

**Credited passages.** The script first lists every passage the draft
credits to an outside source, from `cited.txt` next to `text.txt`: text
holding or followed by a non-TM Forum link, a "(Source: …)" note, or a
numeric citation marker such as `[29]`, a "Source: …" note appended to the
end of a paragraph (with or without brackets), the block of paragraphs a
source line introduces, up to the next heading, and the rows under a
heading or table title that names a source (for example "… Component
Feature Source TR315") (a marker like `[29]` usually means text was lifted
from a paper, citations and all). They are grouped by source. Open each
credited source once (fetch its page or document) and compare all of its
passages with it, instead of searching each passage; compare every
credited passage, whatever its wording, because credited text is the
likeliest to be reproduced word for word and a credit alone doesn't make
reproduction allowed. Say whether each passage is word for word, close, or
not in the source (a credit to the wrong source scores 0). For each source
report its licence or terms where the source states them, or that they're
unknown, and note its publication date for `citation-dates.json` (see
"Citation dates and the core citation"). Don't sample credited passages. A passage that is not in its credited source (the page or document opened has no such text, or different wording) is reported as "not in the credited source": search its distinctive sentence, and if it is found on another page it is a credit to the wrong source (citation 0, with that page's owner); if it is found nowhere, say it is unplaced and leave it out of the ownership items unless its wording or form suggests it was copied. A credited source that can't be opened (a paywalled report, a news page instead of the work, a dead link) is reported as not opened, and its passages count as unconfirmed origin (weight 0.5). At the doubled and redoubled tiers, search distinctive sentences from every credited passage, not only the first, to find the work, and stop only when each passage is placed or each search has failed.

**Other sentences, in batches.** After those, it lists up to 20 other
sentences of 10 to 40 words, choosing the ones least about this project,
because those are what gets copied in from outside, in three batches: 7,
then 8, then the rest (`--batches 7,8`). Search batch 1. Search batch 2
only if a batch 1 sentence matched a page outside TM Forum, and batch 3
only if a batch 2 sentence did. Say which batches were searched and why
the later ones weren't. At the doubled and redoubled tiers run all three batches whether or not an earlier one matched. Run the searches of a batch together, not one at
a time. It skips sentences that are TM Forum's own text, meaning at
least half of the sentence is found in TM Forum's own text: by default
the IPR Policy copy in this skill's `references/` folder, plus anything
named with `--exclude`. It never uses the whole repository, because the
repository holds the checked documents and their reports, which quote
the draft. It ranks the rest by two signals added together:

- **Project-specific terms:** the share of words that look like code,
  paths, IDs, acronyms or names (`component-specification-studio`,
  `TMFC001`, `YAML`, `GitHub`).
- **The document's own vocabulary:** the share of words the draft uses
  five or more times. Text copied in from elsewhere tends to use words
  the rest of the document doesn't, such as "hyphens", "lowercase" and
  "prefix" in a section on branch naming.

Ties go to definitions (at most two per defining phrase, so a document
written to one template doesn't fill the list), then to longer sentences.
These signals only roughly order the sentences: across 587 sentences
searched they did little better than chance at predicting a match, which
is why the batches, not the ranking, limit the work. Report the "Skipped N
sentences" line it prints. To exclude other TM Forum text, pass
`--exclude <folder>`; to skip nothing, pass `--no-exclude`. To recognise
TM Forum's component specs too, pass `--exclude <local clone of
TMForum-ODA-Component_Development>`. Search for each sentence in
quotation marks, exactly as printed. For each result report the sentence,
whether it matched, and the URL and owner of any matching page. A match on
a TM Forum page is expected; a match anywhere else is a finding. Say that
no match only means the text isn't on the indexed public web: paywalled
standards and reports aren't searched this way, which is what check 1 is
for.

## Ownership scores

Every report ends with two scores, in a section headed
`### Ownership scores` under `## Not from the references`. Only the
poorly cited ownership score is classed good, improving or bad; the
ownership score is reported with its z for context:

- **Ownership score:** how much material owned by non-Contributors the
  document contains, however well it's cited.
- **Poorly cited ownership score:** the same material, counted only to
  the extent its credit is missing or wrong.

1. List each item of material owned by a non-Contributor (see "The
   central test" under Reference 1 in `references/reference-citations.md`),
   with:
   - a **weight**: **1.0** for a whole figure, a word-for-word passage, a
     close paraphrase, or a reworded idea, structure or convention taken
     from an identifiable outside work (for example a named level scheme,
     metric or model restated in the document's own words); **0.5** for an
     adapted figure or an item of unconfirmed origin;
   - a **citation** value: **1.0** for a complete credit (Title, Author,
     Source and Licence, per Reference 5, and Date), **0.75** for a credit
     complete but for the date, **0.5** for a partial credit (the right
     source, but no licence, author or quotation marks),
     **0** for no credit or a credit to the wrong source (a credit whose number or title doesn't match the work that was found, such as "RFC1616" for the HTTP specification, is a wrong source). `credit_check.py`
     gives the credit's parts; whether the source is the right one comes
     from opening it.

   Don't count clip art and icons, or contributing Members' own material.
   An idea or convention common across a field, with no single
   identifiable source, isn't an item either. The reference set in
   `references/ownership-reference.json` was weighted before close
   paraphrase and reworded ideas counted 1.0, so z against it overstates
   a document's score; the class rule is fixed thresholds and still
   applies. Say so in the report when an item uses the 1.0 rewording
   weight.
2. Count the document's words (`text.txt`; use that count for the ownership score and say so, because the other scripts count words a little differently: they drop contents lines or the document's own identifier), then run:

   ```bash
   python -I scripts/ownership_score.py --words <words> --items <weight:citation,...>
   ```

   The ownership score is the total weight per 1,000 words; the poorly
   cited ownership score is the total of weight × (1 − citation) per 1,000
   words. The poorly cited ownership score is classed by a fixed rule held
   in [references/ownership-reference.json](references/ownership-reference.json):
   **good** is a score up to 0.05 per 1,000 words, as long as no whole
   figure or word-for-word passage is left with no credit at all, **bad**
   is above 0.15 per 1,000 words (roughly one word-for-word passage with
   no credit per 6,700 words), **improving** is in between. `--reference` prints the
   reference table.
3. Report the items with their weights and citation values, both scores
   with their z (σ from the reference mean), and the class of the poorly
   cited ownership score. The class is a finding like any other: no
   fixes follow from it.

## Dependence on outside sources

Every report says how far the document depends on other bodies' work, in
a section headed `### Dependence on outside sources` under
`## Not from the references`, after `### Ownership scores`. Dependence
isn't an IP finding by itself: a document can depend heavily on a
standard it credits properly. It's reported so a reader can see whether
the document stands on its own.

Some documents, especially in the network space, say they expand on
another standards body's work (3GPP, ETSI, MEF, IETF and so on). For
those, depending on that body is expected and is the point of the
document. So the script first finds the **declared base** and then
judges the document against others like it.

```bash
python -I scripts/dependence.py "<output-dir>" [--sources "<sources-dir>"] [--declared-base 3GPP,ETSI]
```

- **Declared base:** bodies the title or the first 15% of the text
  (scope, introduction) says the document builds on ("based on",
  "extends", "expands on", "aligned with", "bridging", "mapped to" ...).
  The script quotes the sentence it relied on. It only knows standards
  bodies by name, so a base named only by its specification (for
  example "A2A" for the Linux Foundation's Agent2Agent protocol, or
  "ETSI NFV" concepts adopted without a declaring sentence) is missed:
  read the scope and introduction, and pass any it misses with
  `--declared-base`. Report which bases were found and which were added.
- **By reference** (always): body mentions per 1,000 words, the top
  body's share of them, distinct outside document identifiers
  (3GPP TS 28.531, MEF 55, RFC 6749 ...), and **pointers per 1,000
  words**: phrases like "as defined in", "see" or "according to"
  followed within ten words by a body or identifier. Pointers are the
  stand-alone test: each one sends the reader elsewhere to understand
  the text. Contents and figure-list lines are left out.
- **Possible undeclared base:** printed when one body has half or more
  of five or more mentions but isn't declared. Report it as a finding.
- **By copying** (only with `--sources`, the same folder as the
  copied-text check): each matching source's words, its words per 1,000
  words of the document, longest run and words in normative text
  (sentences with shall, must, should, required), with its role. **base**
  means the file's name or folder names a declared base, so file sources
  under a folder per body (`<sources-dir>/3GPP/...`). **cited** means the
  document names the source. **TM Forum (expected)** means a file named
  IG..., GB..., TR... or TMF.... **undeclared** means any other source.
  Then the **original** words per 1,000: the document's text, and its
  normative text, that matches no outside source. TM Forum's own text
  counts as original. For a document with a declared base, a thin
  original share of normative text is the finding that matters, since that
  means the requirements restate the base rather than adding to it. A
  cited source is recognised by its number in the file name
  (`28312-j50.docx` for TS 28.312, `gs_zsm002v010101p.pdf` for ZSM 002,
  `rfc6749.txt`).

The pointer rate is classed against
[references/dependence-reference.json](references/dependence-reference.json),
separately for documents with and without a declared base, at 0.8σ:
**heavy** above mean + 0.8σ (and at least three pointers), **light**
below mean − 0.8σ, **typical** in between. For documents without a
declared base **light** means no pointers at all: most of them have none,
so mean − 0.8σ is below zero. Report the class, z, the group
it was judged against, every measure in the script's table and, with
`--sources`, the copying table. As with the other scores, no fixes follow
from the class.

**Copied words.** With `--sources`, the words copied word for word from
outside sources (base, cited and undeclared together), per 1,000 words of
the document, are classed too, by a fixed rule held in the reference
file (`copied_class_rule`): **light** below 1 per 1,000 words, **heavy**
above 20, **typical** in between. Only documents
that cite a held source (they name one of the specifications held in
`sdo-sources/` by its number, or `entry.json` says so) are classed:
for any other a result of 0 only means there was nothing to compare it
with. Report it as "none found; sources not held", or, if a match turns up
anyway, as its figure "not classed (cites no held source)". TM Forum's
§14.1 notice is masked out first. Any copied normative text is a finding:
none of the 38 reference documents copied any. Use `sdo-sources/` as
`--sources` for SDO-based documents and add to it as needed (.docx, .pdf,
.txt or .md). `--reference` prints the reference table.

## AI-indicator score

Every report gives a likelihood that the document, or parts of it, were
produced with GenAI, under `## Reference 6` (COPE), next to whether the
document declares AI use. It measures **indicators, not proof**: AI-text
detection is unreliable, flags human writing (especially non-native
English) and misses edited AI text. Say so in the report, and always list
the evidence behind the score.

```bash
python -I scripts/ai_indicators.py "<output-dir>" --docx "<input.docx>" --figure-mismatches <N>
```

`<N>` is the number of figure labels that contradict the document's text,
found during the visual image check (0 if none). The script writes
`ai_indicators.txt` and lists five signs, strongest first. Sign 3 is counted
and reported but scores nothing: a label that contradicts the text shows that
a figure and its text disagree, not who or what wrote them, so the reports
give it its own **Figure labels** column (no class, no z), and the reference
set's scores are recomputed without it:

| Sign | Points |
|---|---|
| 1. Leftover assistant text: chat-style lines ("I hope this helps", "as an AI", "I have the … from earlier") or chat citation artefacts ("oaicite", "turn0search") | 5 each |
| 2. AI provenance in the file's metadata: in a picture file, C2PA / Content Credentials, the IPTC "trainedAlgorithmicMedia" type, or a generator's name; in the document's own properties (creator, last modified by, application, custom properties), an AI tool's name | 5 per picture; 5 for the document properties |
| 3. Figure labels that contradict the text (from the visual check) | 0 (reported in the Figure labels column) |
| 4. Style shift: long paragraphs (40+ words) with at least two AI-typical words, at 4 or more per 100 words and three times the rest of the document's rate | 10 × share of long paragraphs |
| 5. Wording: AI-typical words and phrases per 1,000 words; em dashes per 1,000 words | 1 × rate; 0.2 × rate |

Signs 1 and 2 are capped at four occurrences each and are absolute points,
not scaled by the document's length: one leftover assistant line is
direct evidence in a short document and a long one alike. Signs 4 and 5
are rates. The script prints the two parts of the score apart (the
evidence points, and the wording rate per 1,000 words). The score is
classed against
[references/ai-indicators-reference.json](references/ai-indicators-reference.json)
by rank (`class_rule`): **low** is a score at or below the one that ends
the reference set's bottom quarter, **high** at or above the one that
starts its top fifth, **medium** in between. The scores pile up at zero,
so σ is larger than the mean and mean ± 0.8σ said little; z is still
given for context. Any occurrence of sign 1 or 2 makes the class **high (direct
evidence)** whatever the score. Report the score, z, class and every piece
of evidence the script lists (quote leftover assistant text exactly).
Pictures exported from Confluence usually lose their metadata, so no
provenance found doesn't mean none existed.

**Document properties.** With `--docx`, sign 2 also reads the document's
own properties (`docProps/core.xml`, `app.xml`, `custom.xml`) and counts
them once if any value names an AI tool (ChatGPT, OpenAI, Claude,
Anthropic, Copilot, Gemini ...). "Claude" counts only as the whole value,
so a person called Claude isn't flagged. The script prints the creator,
last modified by, application, revision and dates whether or not they
name a tool: report them under Reference 6 next to the score. A value
naming an AI tool is direct evidence that a tool wrote the file, but any
program can set these fields, and Word keeps the creator of the file a
document was started from, so it isn't proof the text is AI-written.
Without `--docx` the properties aren't checked; say so. This is the one
use of the file's metadata: it still doesn't identify the authors (see
"Authors").

## ODA content

Every report says how much of the document is about ODA, in a section
headed `### ODA content` under `## Not from the references`, after
`### Dependence on outside sources`.

```bash
python -I scripts/oda_score.py "<output-dir>" [--exclude-own "<regex>"]
```

It counts, per 1,000 words, the terms for TM Forum's items in seven parts
of ODA: components (TMFC numbers, "ODA Component"), canvas ("ODA Canvas",
Canvas CTK), APIs (TMF Open API numbers, "TM Forum Open API"), frameworks
(eTOM, SID, Frameworx, the Business Process, Information, Application and
Functional Frameworks, Open Digital Architecture), use cases, HVS
(high-value scenarios) and solution packages. Only TM Forum's items count:

- A name that is TM Forum's own (eTOM, Frameworx, ODA Component, ODA
  Canvas, Open Digital Architecture) always counts.
- A TMFC or TMF number counts only if TM Forum has published it: a
  component in the component inventory or component specifications, or a
  TM Forum Open API. The list is
  [references/tmforum-identifiers.json](references/tmforum-identifiers.json).
  TM Forum's other TMF-numbered documents (TMF630, TMF443) aren't APIs and
  don't count as APIs.
- A generic term (use case, UC numbers, SID, TAM, Open API, Information
  Framework, Technical Architecture, component specification, solution
  package, HVS) counts only in TM Forum context: its paragraph, or the
  paragraph either side, names TM Forum, ODA, eTOM, Frameworx, a TMF or
  TMFC number, or a TM Forum document (GBnnn, IGnnnn, TRnnn). "OpenAPI"
  and "Open API Specification" never count.

The score is the sum of the seven rates, with equal weights. A fixed rule
classes it: **light** below 5, **typical** 5 to 20, **heavy** above 20.
Report the table the script prints (TM Forum terms, rate and terms left
out for each part), any unpublished TMF or TMFC numbers it lists, the
score, the class and how many of the seven parts have at least one term
per 1,000 words.

- It removes the document's own number (read from the cover) before
  counting, so a document isn't scored for naming itself. Pass
  `--exclude-own` for other names of the document: documents that cite
  their sister documents' numbers (`TMF ?44[345]` for TMF443, TMF444 and
  TMF445) or a title that is itself ODA vocabulary
  (`(?:ODA )?Functional Architecture` for GB1022). Say what was passed.
- It counts mentions only. It doesn't use the title or document type, and
  it doesn't show whether the document defines, implements or only cites
  what it names. A document that is part of ODA but rarely uses the
  vocabulary in its body (the AN L4 solution-package guides) is light. Say
  so where it applies. It isn't a risk score: it has no z, and no fixes
  follow from the class.

`--reference` prints the reference table for the 38 reference documents.

## Authors

Every report names the document's authors, from its Acknowledgements:

```bash
python -I scripts/authors.py "<output-dir>"
```

It reads `text.txt` and writes `authors.json`. An author is anyone whose
role names an author (Lead Author, Co-Author, "Project Chair, Author"),
or an editor who isn't TM Forum's reviewing editor ("Reviewer, Editor").
Contributors, key contributors and reviewers aren't authors. It handles
the layouts in published deliverables: "Name, Title, Company - Role"
lines, Team Member / Company / Role tables (with or without a Title
column), and an "Authors" or "Guide Editors and Authors" heading over a
list. It merges spellings of one person ("Dave Millham", "David Milham")
and fixes all-capital or all-lower-case names. Don't use the file's own
metadata: TM Forum documents carry the publishing staff's name there,
not the authors'. Check the result against the Acknowledgements and say
when a document names no author or editor (some list only project
members, and an unfilled inception form lists no one). Put the authors
in the report under `## Not from the references`, before
`### Ownership scores`, in a section headed `### Authors`.

## Editorial consistency (this skill's addition, not an IP check)

Every report gives a reading of the document against itself, in a
section headed `## Editorial consistency check` placed directly below
the document score block and above `## Reference 1`. It answers a
reviewer's usual complaint about drafts built up in pieces (with or
without GenAI): the parts were never reconciled with each other. It
isn't an IP or licence finding and doesn't come from the six references.
It has its own score (see "Editorial consistency score" below), which
also appears as a column of the document score block and of the combined
report. `editorial_score.py` writes the whole section, starting with this
marker:

> **This skill's addition, not an IP or licence finding.** This is a
> reading of the document against itself. It doesn't come from the six
> references and isn't part of the document score block or the IP
> scores; it has its own score, below. Locations are given as the
> section number and heading from the document's table of contents.

Read `text.txt` in full (this check can't be done from extracts). Give
every location as the section number and heading from the document's
table of contents (for example "§5.2 The Mapping to Gates", "Appendix B.6
Gate Catalog"), never a `text.txt` line number, because readers look for
findings in Word. Quote the conflicting wording on both sides. Record
each finding in `work/documents/<key>/editorial.json` under one of five
categories (the section shows each as a `###` sub-heading with a
two-column table, Location and Finding):

1. **Duplicate concepts.** A term, rule or passage defined or stated more
   than once, where the versions differ or repeat each other: the main
   concept's definition in the summary, body and glossary; a glossary
   term defined twice (Terminology and Abbreviations); a paragraph
   restated right after itself; a heading repeating another section's.
2. **Internally inconsistent rules.** Two statements that can't both
   hold: a principle against the tables that apply it (a taxonomy said to
   be independent of gating but used to gate); a definition against the
   glossary; a category count against the list it introduces; lists of
   the same thing that differ (lifecycle states, ID or version formats);
   a template against its worked instances (missing columns, fewer rows
   than the text claims, sections the instance maps to but doesn't
   contain); a cross-flow or cross-table reference to an ID that isn't
   there; code beside a table giving a different value.
3. **Incomplete references and cross-references.** Section references
   checked against the table of contents; placeholder numbers
   (`GB NNNN`); a source given differently in two places; vague
   attributions ("Industry Standard", a company name with no work);
   quotations or news items with no link or date; empty sections and
   headings; reference-table rows with no source; terms and acronyms
   used but never defined; drafting notes and dangling asterisks.
4. **Unsupported specificity.** Precise numbers, counts or thresholds
   with no basis in the document or a cited source ("eight reconstruction
   questions" where none are listed; mandated durations or percentages);
   figures describing content that isn't there; claims that the document
   contains something it doesn't ("complete template instances").
5. **Implementation detail given more normative weight than its
   evidence.** Mandatory or binding language (must, shall, not optional,
   authoritative, binding, invalid) set against what the document says
   about itself (maturity level, "RFC", "working model", "not
   normative"); a specific implementation (a language, code with concrete
   values) placed in the normative template; platform-wide rules
   resting only on worked examples; comparisons with standards or laws
   that cite no clause.

As with every other part of the report, give the finding and its
evidence only: no rewrites, no suggested wording and no list of what to
change. Apply the same standard to every document so scores compare:
record only findings the text evidences, and don't pad a clean
document. `work/documents/GB1096/editorial.json` is a worked example.

`editorial.json`:

```json
{"key": "GB1096", "words": 9238,
 "not_checked": "whether the domain content is technically correct",
 "findings": [{"category": "inconsistent", "location": "§5.2 The Mapping to Gates", "finding": "..."}]}
```

`category` is one of `duplicate`, `inconsistent`, `reference`,
`specificity`, `normative` (in the order of the list above: 1, 2, 3, 4,
5). `words` is the `text.txt` word count. `not_checked` says what the
reading didn't judge.

### Editorial consistency score

Each finding is weighted by how far it stops a reader relying on the
document:

| Category | Weight | Why |
|---|---|---|
| Internally inconsistent rules | 3 | The document can't be followed as written: two of its rules can't both hold |
| Unsupported specificity | 2 | A reader may act on a number or claim the document doesn't support |
| Implementation detail given more normative weight than its evidence | 2 | A reader may treat an example or a draft as binding |
| Incomplete references and cross-references | 1 | A reader can't follow up a point, but the content itself holds |
| Duplicate concepts | 1 | Repetition that diverges or adds nothing; usually a sign of the other categories |

Weighted findings don't grow in proportion to length: some faults happen
once per document whatever its size (an empty section, a missing
glossary), so across the 39 documents first checked, weighted findings
grew with about the 0.65 power of the word count, and a plain rate per
1,000 words made short documents look worse (correlation −0.71 with
length). The score therefore compares the document's weighted findings
with the number expected for a document of its length, fitted across
the reference set as `a × (words ÷ 1,000)^b` (13.73 and 0.649 for the
first 39): **1.00** is typical for its length, 1.50 is half as many
again. On the first 39 its correlation with length is 0.01. The fit
(`a`, `b`, frozen: `--build-reference` keeps them unless `--refit` is
given) and the scores' mean and σ are held in
[references/editorial-reference.json](references/editorial-reference.json)
(in this skill's folder: every document in `work/documents/` with an
`editorial.json`). The class is a fixed rule on the score, set by the
user and held as `CLASS_RULE` in `editorial_score.py`:

| Score | Class |
|---|---|
| up to 1.15 | **consistent** |
| above 1.15, up to 1.3 | **improving** |
| above 1.3, up to 1.5 | **inconsistent** |
| above 1.5 | **very inconsistent** |

The z against the reference set is given for context only. The report
also gives the weighted findings per 1,000 words, for context only.
It rests on one reading, so it is a judgement, not a count a script
repeats; a difference of a few findings between two documents is within
the reading's own variation. As with the other scores, no fixes follow
from the class.

```bash
python -I scripts/editorial_score.py "<output-dir>" --update-entry --md "<output-dir>/editorial.md"
```

It checks `editorial.json`, prints the counts, score, z and class, writes
the section (marker, score table, the five tables and what wasn't
checked) to `editorial.md`, and with `--update-entry` copies the counts
into `entry.json` as `"editorial": {"words": ..., "counts": {...}}`, so
the document score block and the combined report carry the score. Run it
before `document_scores.py`, and paste `editorial.md` directly below the
score block. Only rebuild the reference set when the user asks:
`editorial_score.py --build-reference ../../work/documents` (from
this folder).

## Document score and entry.json

Every run ends by saving the document's record and scoring it from that
record, so the score under the report's title and the document's row in
any later combined report are the same figures.

1. **Write `entry.json`** in the document's folder
   (`work/documents/<key>/entry.json`), with paths relative to that folder:

   ```json
   {"key": "IG1242", "label": "IG1242 v26.0.0", "dir": ".",
    "docx": "../../../source/IG1242_ODA_Component_Inventory_v26.0.0.docx",
    "figure_mismatches": 0,
    "ownership": {"words": 9603, "items": [{"item": "...", "weight": 1.0, "cited": 0.5}]},
    "web_check": {"searched": 20, "outside": 0}}
   ```

   `ownership` holds the same items, weights and citation values as
   `### Ownership scores` and the `text.txt` word count;
   `figure_mismatches` the figure-label check's count (leave it out if no
   figure was compared); `web_check` the passages searched on the web and
   how many turned up word for word or nearly on a page outside TM Forum.
   `editorial` is written by `editorial_score.py --update-entry` (see
   "Editorial consistency score"); don't edit it by hand.
   Add `declared_base`, `cites_held_source`, `exclude_own` and
   `core_citation` when this run passed `--declared-base`, judged that the
   document cites a held source the identifiers miss, passed
   `--exclude-own` or `--core` (`core_citation` is the source line as
   `citation_dates.py` prints it).
2. **Score it:**

   ```bash
   python -I scripts/document_scores.py "<output-dir>/entry.json" --sources "<sources-dir>"
   ```

   It runs the automatic scans again from `entry.json` and prints a
   **Document score** block: one row giving poorly cited ownership,
   Automation Indicators, dependence by pointers, dependence by copying,
   editorial consistency (each as score and class), the web check, the core citation (age)
   and ODA content. Use the same `--sources` as the copied-text check.
   Paste the block, unchanged, directly under the report's title (rule 6).
   Its figures must agree with the sections below it; if they don't,
   `entry.json` is wrong: fix it and run again.

The per-document reports are rendered by the `tm-forum-document-quality-individual` skill (sibling folder `../tm-forum-document-quality-individual/`).

For how the reference sets were built and why each class rule is what it
is, read `references/scoring-notes.md`. Only change a reference set, the σ
multiplier or a class rule when the user asks.

## What this skill covers

Apart from the copying checks, the credit check, the image checks, the
scores and the dependence and ODA measures above, this skill doesn't scan
anything. It tells you which of six documents to use for a given IP or
licence question (the table in `references/reference-citations.md`), and
cites each one. Quote the document's own wording only where its terms
allow it. The ISO/IEC standards are paid, copyrighted texts: refer to them
by clause, never reproduce them. Before you cite one of the six, check its
current edition at the link given there.
