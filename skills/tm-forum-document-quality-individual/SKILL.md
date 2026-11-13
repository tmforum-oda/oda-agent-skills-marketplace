---
name: tm-forum-document-quality-individual
description: Writes the full IP and licence check report, one Word report per TM Forum document, covering undeclared copied text (word-for-word comparison against held sources, quoted web spot checks), weak credits (Title, Author, Source, Licence), the publication date and age of each credited source and which one is core to the document, and borrowed images, against the six reference documents for IP and licence scanning of TM Forum ODA component material - the TM Forum IPR Policy (licence modes, copyright notices), OpenChain ISO/IEC 5230 (open-source licence compliance), OpenChain ISO/IEC 18974 (open-source security assurance), SPDX (ISO/IEC 5962) with the REUSE specification (per-file licence labelling and bills of materials), Creative Commons recommended practices for attribution (crediting third-party text and images) and COPE's position on authorship and AI tools (declaring GenAI use). Use whenever the user asks which document covers IP or licence scans, how to check the licence or provenance of third-party material, which copyright notice or licence mode applies to a TMFCnnn deliverable, how to label files with licences, what an SBOM should follow, whether a document (including GenAI-assisted text) copies prose from a source without declaring it, how far a deliverable depends on other standards bodies' work (allowing for documents that say they expand on another SDO's content), how much of a document is about ODA (components, canvas, APIs, frameworks, use cases, HVS, solution packages), and, as a marked addition outside the IP references, whether the document is consistent with itself (duplicate concepts, internally inconsistent rules, incomplete references, unsupported specificity, implementation detail given more normative weight than its evidence). The check itself is the shared tm-forum-document-quality-check skill (sibling folder `../tm-forum-document-quality-check/`), run first when the document has no record.
---

# TM Forum Document Quality: Individual Report

> **Disclaimer:** Using this skill is not legal advice. It does not
> provide a valid legal defence for any infringement, misuse or other
> abuse of intellectual property or other rights. Responsibility for how
> material is used stays with the user. Get qualified legal advice where
> rights are in doubt.

## Where things live

This skill is the `skills/tm-forum-document-quality-individual/` folder (originally of the
IP-scan-tool repository). To use it, tell your GenAI tool something like
"Read `skills/tm-forum-document-quality-individual/SKILL.md` and follow it to check
`<document>`". The check itself, and every script and reference file, is
in the shared skill `tm-forum-document-quality-check`, the sibling folder `../tm-forum-document-quality-check/`
(written below as `skills/tm-forum-document-quality-individual/../tm-forum-document-quality-check/`, which resolves in a repository
clone and in an installed plugin alike). Run the commands below
from the repository root. Everything else sits at the repository root: `source/`
(documents checked), `Document Quality reports/` (every report),
`sdo-sources/` (held sources) and `work/documents/<key>/` (each
document's findings in `report.md` and its record in `entry.json`).

## How to run this skill

1. **The disclaimer is always visible.** Start every response with the
   disclaimer above, word for word, as a blockquote. Never shorten it,
   move it lower or leave it out, even in follow-up responses or ones
   that only answer a short question.
2. **Check once.** If `work/documents/<key>/` has no `entry.json` and
   `report.md` for the document, run the check: read
   `skills/tm-forum-document-quality-individual/../tm-forum-document-quality-check/SKILL.md` and follow it, then come back here.
   If both are there, reuse them and don't check again, unless the user
   asks for a re-check or the document has changed. All the check's rules
   (the six reference sections, find issues and don't fix them, depth of
   check, current state only) are in that skill and apply to the report.
3. **Every run produces a Word report and a branded HTML copy.** Render the document's
   `report.md`:

   ```bash
   python -I "skills/tm-forum-document-quality-individual/../tm-forum-document-quality-check/scripts/make_report.py" "work/documents/<key>/report.md" "<report.docx>" --title "IP and licence check: <document name>"
   ```

   Name the file `<checked document's name without extension>_IP-licence-check_<YYYY-MM-DD>.docx`
   and save it in the folder the user names, or, if they don't name
   one, in `Document Quality reports/` at the root of the IP-scan-tool repository. When
   several documents are checked in one run, write one report per
   document. `make_report.py` needs python-docx; it renders headings, the
   disclaimer box, bullets, tables and links, and shades score cells red, amber or
   green by class (grey for dependence). Every report is A4 portrait;
   don't produce landscape or Letter-size reports.
   It also writes a TM Forum-branded HTML copy beside the .docx, with the
   same name ending `.html` (`make_html_report.py`, styled by
   `skills/tm-forum-document-quality-individual/../tm-forum-document-quality-check/references/tm-forum-html-output.md`): score numbers are coloured
   red, amber or green by class (grey for dependence) and the core
   citation card shows the citation's age. Keep both files.
   Both are rendered from `report.md` and are never edited themselves: to
   change a report, edit `report.md` and render again.
4. **The chat response is a summary, not the report.** In chat give the
   disclaimer, then one line for each of the six references (the number
   of findings, or "doesn't apply"), the scores with their classes in a
   small table, the worst findings in a sentence or two each, one line
   giving the editorial consistency score, class and counts (marked as
   an addition outside the IP references), and the report's path. Paste
   the full report into chat only if the user asks for it.

## What this skill covers

For which of the six reference documents answers a given IP or licence
question, and how each is cited, see "What this skill covers" in
`skills/tm-forum-document-quality-individual/../tm-forum-document-quality-check/SKILL.md` and
`skills/tm-forum-document-quality-individual/../tm-forum-document-quality-check/references/reference-citations.md`.
