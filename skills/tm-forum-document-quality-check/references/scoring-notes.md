# Scoring notes: reference sets and how classes were set

SKILL.md says how to run each measure. This file records what the
reference sets contain and why each class rule is what it is. Read it when
a score needs explaining or a reference set is being changed. Only change
a reference set, a σ multiplier or a class rule when the user asks.

All rates are per 1,000 words of the document's text. (The ownership
scores and the copied share used to be per 10,000 words and a percentage;
they were restated per 1,000 words on 2026-10-22, with the same classes.)

The reference set is the 38 documents checked on 2026-10-20 and
2026-10-21 (drafts still being written are left out), listed in
`ownership-reference.json`, `dependence-reference.json`,
`ai-indicators-reference.json` and `oda-reference.json`. Their files are
in `source/`. To rebuild the first three after more documents are checked,
run `scripts/build_reference_sets.py <manifest.json> --sources
<sources-dir>`; it rewrites them from the same manifest and prints how
classes change.

## Ownership scores

- Ownership: mean 0.176, σ 0.247 per 1,000 words (not classed).
- Poorly cited ownership: mean 0.119, σ 0.160, shown for context only.
- The class is a fixed rule, not a comparison with the mean: classing at
  mean ± 0.8σ put the "good" threshold below zero (−0.009) once the set
  grew to 38, so no document could be good (a few large scores make σ
  large), and the classes moved whenever documents were added.
- **good** is a score up to 0.05 per 1,000 words, as long as no whole
  figure or word-for-word passage (weight 1.0) has no credit at all;
  **bad** is above 0.15 per 1,000 words (roughly one word-for-word passage
  with no credit per 6,700 words); **improving** is in between. Hugo
  Vaughan set the bad threshold on 2026-10-21 at 0.2 per 1,000 words (it
  was 2.0 per 10,000 words, the same line) and lowered it to 0.15 on
  2026-10-23.
- Good was a score of exactly 0 until 2026-11-05, when Hugo Vaughan widened
  it: under that rule every good document was short (13 of the 14 under
  7,000 words), because a long document almost never scores exactly 0, so
  the class said more about length than about care.
- Under it, 10 of the 38 reference documents are bad (IG1526A, GB1059,
  GB1082, GB998, IG1330, IG1412, IG1453, IG1245, IG1251 and TMF444), 11 are
  improving and 17 are good, on their 2026-10-21 scores. IG1351 (0.027),
  GB1022 (0.041) and IG1251C (0.048) moved from improving to good. With
  good = 0 it was 14 improving and 14 good; at a bad line of 0.2 it was 8
  bad.
  `ownership_score.py --reference` prints the table.

## Dependence on outside sources

- The pointer rate is classed separately for documents with and without a
  declared base, at 0.8σ: **heavy** above mean + 0.8σ (and at least three
  pointers, because most documents without a base have none, so one or two
  in a short document would otherwise class as heavy), **light** below
  mean − 0.8σ, **typical** in between. For documents without a declared
  base, **light** is no pointers at all (`pointer_light_at_zero`, set by
  Hugo Vaughan on 2026-11-05): 23 of the 32 have none, so mean − 0.8σ was
  below zero (−0.08) and light was impossible. Under it 23 are light, 8
  typical and 1 heavy.
- Six documents have a declared base (mean 0.56, σ 0.54 per 1,000 words,
  so light < 0.13, heavy > 0.99): the TM Forum inception form for SMIC
  (IETF), IG1280 (3GPP), IG1251 and TR255 (ETSI), IG1453 (Linux Foundation)
  and IG1330 (IETF). The other 32 have none (mean 0.08, σ 0.20, so heavy >
  0.25). Six is few, so treat that group's class with care.
- Two documents are heavy: GB1059 (a 3GPP base it doesn't declare) and
  IG1330. IG1251 is light. All others are typical. IG1280 shows why the
  groups are separate: judged against documents without a base it would be
  heavy (z above +3), but for a document that says it bridges to 3GPP its
  rate is typical.
- **Copied words** (with `--sources`): the words copied word for word from
  outside sources (base, cited and undeclared together), per 1,000 words
  of the document. **Heavy** above mean + 0.8σ, **light** below mean −
  0.8σ, **typical** in between was the rule until 2026-11-05: with mean 10.0 and σ 18.0 per
  1,000 words, light was below −4.4, so no document could be light. Hugo
  Vaughan replaced it on 2026-11-05 with a fixed rule (`copied_class_rule`
  in `dependence-reference.json`): **light** below 1 per 1,000 words,
  **typical** 1 to 20, **heavy** above 20.
- TM Forum's §14.1 notice is adapted from the ISOC copyright statement in
  older RFCs, so the script masks any text matching the IPR Policy copy
  before comparing; otherwise every TM Forum document matches RFC 2753 and
  RFC 3198.
- The held sources are 17 free specs the sample cites, kept in
  `sdo-sources/<body>/` at the repository root (3GPP TS 28.100, 28.111,
  28.310, 28.312, 28.530, 28.531 and 28.541; ETSI GS ZSM 002 and NFV-IFA
  011, 013 and 014; RFC 2753, 3198, 6749 and 7519; OpenID Connect Core 1.0;
  the A2A specification), downloaded 2026-10-21. Add to the folder as
  needed. It needs .docx, .pdf, .txt or .md: unpack 3GPP zips, save legacy
  .doc files as .docx, and convert HTML pages to text.
- A document **cites a held source** when it names a specification we hold
  by its document number (for example 3GPP TS 28.312 or RFC 6749), or the
  manifest says so for a citation the numbers miss (TR255's "NFV IFA011").
  Only those documents are classed, because for a document that cites none
  of the held specifications a result of 0 only means there was nothing to
  compare it with, not that it is clean. Such a document is reported as
  "none found; sources not held", or, if a match turns up anyway (IG1252
  shares 58 words with TS 28.100, which it doesn't cite), as its figure
  "not classed (cites no held source)".
- Eleven of the 38 documents cite a held source (mean 10.0, σ 18.0 per
  1,000 words, for context). Two are heavy: IG1526A (62 per 1,000, from
  TS 28.312, TS 28.310 and TS 28.530) and IG1453 (25, from TS 28.312).
  Five copied nothing and are light (TMF445, IG1251, IG1523D, IG1523E and
  TR255); the other four are typical. The heavy pair is the same as under
  the old line of 24.4.
- None of the 38 documents copied any of its normative text: every
  original share of normative text was 100%. Published TM Forum
  deliverables add to the SDO work they build on rather than restating it,
  so any copied normative text is unusual and is a finding.

## AI-indicator score

- The AI-indicator reference set is its own: the 60 Word documents checked
  from 2026-10-20 to 2026-11-05 (every record except the 8 spreadsheets,
  whose scores aren't comparable), rebuilt on 2026-11-05. The other
  reference sets still use the 38 documents above.
- Classed by rank (`class_rule`, set by Hugo Vaughan on 2026-11-05):
  **low** at or below the score that ends the bottom quarter of the
  reference set, **high** at or above the score that starts its top fifth,
  **medium** in between. On the 60 documents that is low ≤ 0.16 and high
  ≥ 2.89: 15 low, 33 medium, 12 high (one of them direct evidence). Any
  occurrence of sign 1 or 2 makes the class high (direct evidence)
  whatever the score.
- Until 2026-11-05 it was classed at 0.8σ (mean 1.97, σ 2.28, so low <
  0.14 and high > 3.80). The scores pile up at zero (11 documents score
  exactly 0) and σ was larger than the mean, so the bands said little; z
  is still given for context and the author table.
- The style-shift trigger was tightened on 2026-11-05: a long paragraph
  (40+ words) now needs at least 2 AI-typical words, at 4 or more per 100
  words (it was 2) and three times the document's rate. Before, one AI
  word in a 40 to 50-word paragraph was enough: 38 of the 86 outlier
  paragraphs in the 60 reference documents rested on a single word; now 14
  paragraphs count. The reference set's style_shift values were
  recomputed (25 of the 60 changed), which lowered the mean to 1.75 and
  σ to 2.08.
- Figure labels that contradict the text (sign 3) are counted but score 0,
  from 2026-11-05. With 2 points each, 26 of the 38 documents classed high
  across the first 68 records were high only because of figure labels: a
  mismatch shows that a figure and its text disagree, not who or what wrote
  them. They are reported in their own Figure labels column instead.
- Signs 1 and 2 are absolute points (up to four occurrences each), not
  rates: one leftover assistant line is direct evidence in a short document
  and a long one alike. Signs 4 and 5 are rates (a share of long
  paragraphs; AI words and em dashes per 1,000 words). The script prints
  the two parts of the score apart.
- Across the 68 records, 13 are high, 2 of them direct evidence (TMF443:
  leftover assistant text; GB1090A: written by openpyxl), 38 medium and 17
  low. `ai_indicators.py --reference` prints every reference document's
  score.
- Pictures exported from Confluence usually lose their metadata, so no
  provenance found doesn't mean none existed.
- Sign 2 was extended on 2026-10-23 to the document's own properties
  (creator, last modified by, application, custom properties naming an AI
  tool). The reference set wasn't rebuilt: none of the 35 reference
  documents with a .docx names an AI tool in its properties (their
  creators are TM Forum staff or blank, last modified by TM Forum staff or
  Scroll Word Exporter, application Microsoft Office Word), so their
  scores don't change. IG1251C, TR255 and IG1351 have no .docx in the
  manifest and weren't checked.

## ODA content

- Fixed rule set by Hugo Vaughan on 2026-10-22: **light** below 5,
  **typical** 5 to 20, **heavy** above 20, per 1,000 words, equal weights
  over seven parts (components, canvas, APIs, frameworks, use cases, HVS,
  solution packages).
- Only TM Forum's items count. Names that are TM Forum's own (eTOM,
  Frameworx, ODA Component, ODA Canvas, Open Digital Architecture) always
  count. TMFC and TMF numbers count only if TM Forum has published them
  as a component or an Open API (`tmforum-identifiers.json`: the TMFC
  numbers in IG1242 v26.0.0 and the TMForum-ODA-Component_Development
  specifications; the TMF numbers of the tmforum-apis GitHub organisation,
  that repository's `apiIndex.json` and IG1242). Generic terms (use case,
  SID, TAM, Open API, Information Framework, solution package, HVS and the
  like) count only when their paragraph, or one either side, names TM
  Forum, ODA, eTOM, Frameworx, a TMF or TMFC number or a TM Forum
  document number. "OpenAPI" and "Open API Specification" never count.
- Under it, of the 38 documents 7 are heavy (IG1242, TAC-1012, IG1228,
  IG1330, IG1222, GB1022 and IG1171), 13 typical and 18 light. The AN L4
  solution-package guides are all light, because the score uses term
  density only, not the title or document type, and their text rarely
  names ODA or TM Forum next to "solution package" or "HVS".
  `oda_score.py --reference` prints the table.
- TMF443, TMF444 and TMF445 cite each other's numbers and GB1022's title
  is "ODA Functional Architecture": their scores are counted with those
  names removed (`excluded_own` in the reference file; `--exclude-own` on
  the command line).

## Depth of check (tiers)

`scripts/triage.py` picks a provisional tier from the cheap first pass:
**light** (nothing found), **doubled** (something found, provisional poorly
cited score not above 0.15 per 1,000 words) or **redoubled** (that score
above 0.15, or 10 or more words per 1,000 copied from held sources).

- The trigger "a passage credited to a source outside TM Forum, or any
  word-for-word match to a held source" was tried on the 38 reference
  documents against their poorly cited class. It fired on 7 of the 8 bad
  documents (the miss is IG1245, which turned up through a web search of
  one of the other sentences), 12 of the 16 improving documents and 3 of
  the 14 good ones. Scan flags were left out of the trigger: adding "3 or
  more flags" caught one more improving document but raised the good ones
  that fire from 3 to 5, and most flags on text-heavy diagrams are false
  alarms.
- Why it was added: in the 2026-10-22 cycle (IG1330, GB1082, IG1412,
  TAC-1012, IG1526A) the three documents that missed findings the
  2026-10-21 reports had caught were all ones the trigger fires on (7 to
  16 outside-credited passages each). The missed findings were a credited
  passage that wasn't placed because only the first one was searched, an
  adapted figure seen only on a contact sheet, and figure labels that were
  never compared with the text. The deeper tiers ask for exactly those
  steps.
- The tier is a guide to effort, not a score: it has no class and no z.
  About 60% of the reference documents fire the trigger, so the stepped
  approach moves effort towards them more than it saves overall; the
  saving is on the documents that stay light.
- The 10-per-1,000 copied-words line comes from the reference set: every
  document at or above it was bad (IG1526A 62, IG1453 25, IG1330 11). It is
  deliberately lower than the heavy line for copied words (20): the tier is
  a guide to effort, so a typical document like IG1330 can still be
  redoubled. It is also half the heavy line. Check it again whenever the
  reference set grows past its three supporting documents.

## Editorial consistency

- Fixed rule (`CLASS_RULE` in `editorial_score.py`), widened by Hugo
  Vaughan on 2026-11-05: **consistent** up to 1.15, **improving** up to
  1.3, **inconsistent** up to 1.5, **very inconsistent** above 1.5.
- The old bands (1.04, 1.1, 1.2) sat on a score that averages about 1.0
  by design (mean 1.036, σ 0.265), so "consistent" meant at or below
  average. The improving band was 0.06 wide, under a quarter of σ, and one
  weight-3 finding moves a 3,000-word document's score by about 0.11. Only
  2 of the 39 documents were improving and 15 were flagged.
- Under the new bands: 26 consistent, 7 improving, 3 inconsistent and 3
  very inconsistent (6 flagged). Each band is wider than one weight-3
  finding for documents of 3,000 words or more; below about 1,700 words a
  single weight-3 finding can still cross the improving band.
- The curve (`a` 13.7253, `b` 0.6494) is frozen: `--build-reference` keeps
  it unless `--refit` is given, so a rebuild doesn't move every score.

## Script notes (2026-10-22 fixes)

Problems the five-document cycle turned up, and how each was dealt with:

- **Word counts differ between scripts** (`text.txt`, `dependence.py`,
  `oda_score.py`): `dependence.py` leaves out contents lines and
  `oda_score.py` removes the document's own identifier, which can also split
  a token such as "IG1330-GUC0001". Both now print the `text.txt` count
  beside their own, and SKILL.md says which to quote.
- **Copied-words class with no held source:** `dependence.py` classed copied
  words even when the document cited no held source. It now classes only
  when the document names a held source (or `--cites-held` says so), like
  the combined report; the held-source helpers live in `dependence.py` and
  `combined_report.py` uses them.
- **`cited.txt` attached reference entries to the wrong links:** some
  documents carry stale hyperlinks on the "[5]" markers of their reference
  lists (IG1330's references [5] to [13] each carried the address of an entry
  above). `extract_docx.py` now ignores links that wrap only a bare marker
  or a blank, and a numbered reference entry is credited with its own link.
- **One sentence of a copied block listed:** `spot_check_candidates.py` now
  lists every sentence of a credited passage (up to 6).
- **Contact sheets needed `--skip` typed in:** `contact_sheets.py` now leaves
  out the flagged and the credited pictures itself.
- **Credited passage not on the credited page, and an unretrievable
  credited source:** rules added to SKILL.md (wrong source, unplaced,
  unconfirmed origin).
