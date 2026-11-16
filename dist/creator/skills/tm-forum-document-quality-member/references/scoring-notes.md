# Scoring notes: reference sets and class rules

SKILL.md says how to run each measure. This file says what the reference
sets contain and why each class rule is what it is. Read it when a score
needs explaining or a reference set is being changed. Only change a
reference set, a σ multiplier or a class rule when the user asks.

All rates are per 1,000 words of the document's text.

## Reference sets

There are two groups of reference sets, each with the same five sets and
the same class rules:

- **Word sets**, in `references/`: the same 95 Word records in
  `work/documents/` (including documents read from a PDF), listed in each
  file. Word records checked since (IG1552 v1.2.1, IG1579A and IG1579B)
  are scored against them but aren't part of them.
- **Spreadsheet sets**, in `references/spreadsheet/`: the 19 spreadsheet
  (.xlsx) records. Per-1,000-word rates, AI-wording signs and editorial
  findings behave differently in short, repeated cell text than in prose,
  so a spreadsheet is compared with other spreadsheets only.

`scripts/refsets.py` picks the group from a record's `source_format.txt`.

| Set | File (in both folders) |
|---|---|
| Ownership | `ownership-reference.json` |
| Automation Indicators | `ai-indicators-reference.json` |
| Dependence | `dependence-reference.json` |
| ODA content | `oda-reference.json` |
| Editorial consistency | `editorial-reference.json` |

`scripts/build_reference_sets.py <manifest.json> --sources <sources-dir>`
rebuilds the first four from a manifest of the Word records, and with
`--spreadsheets` from a manifest of the spreadsheet records;
`editorial_score.py --build-reference work/documents --refit` rebuilds the
editorial set from the Word records, and with `--spreadsheets` from the
spreadsheet records. SKILL.md says how to update existing reports after a
rebuild. The sections below give the Word sets' figures; the last section
gives the spreadsheet sets'.

## Ownership scores

- Ownership: mean 0.149, σ 0.243 per 1,000 words (not classed).
- Poorly cited ownership: mean 0.099, σ 0.170, shown for context only.
- The class is a fixed rule, not a comparison with the mean: mean − 0.8σ
  is below zero, so classing at mean ± 0.8σ could never give good (a few
  large scores make σ large), and the classes would move whenever
  documents were added.
- **good** is a score up to 0.05 per 1,000 words, as long as no whole
  figure or word-for-word passage (weight 1.0) has no credit at all;
  **bad** is above 0.15 per 1,000 words (roughly one word-for-word passage
  with no credit per 6,700 words); **improving** is in between. Good isn't
  limited to exactly 0, because a long document almost never scores
  exactly 0, so that rule would make good a measure of length rather than
  of care.
- In the reference set, 58 documents are good, 16 improving and 21 bad.
  `ownership_score.py --reference` prints the table.
- The set takes each document's items as its record holds them. Some
  records weight close paraphrase 0.5 and leave out reworded ideas; others
  weight close paraphrase and reworded ideas from an identifiable work
  1.0. So z against the set is approximate. The class rule is fixed and
  isn't affected.

## Dependence on outside sources

- The pointer rate is classed separately for documents with and without a
  declared base, at 0.8σ: **heavy** above mean + 0.8σ (and at least three
  pointers, because most documents without a base have none, so one or two
  in a short document would otherwise class as heavy), **light** below
  mean − 0.8σ, **typical** in between. For documents without a declared
  base, **light** is no pointers at all (`pointer_light_at_zero`): 70 of
  the 84 have none, so mean − 0.8σ is below zero and could never give
  light.
- Eleven documents have a declared base (mean 0.39, σ 0.45 per 1,000
  words, so light < 0.03, heavy > 0.75). The other 84 have none (mean
  0.05, σ 0.15, so heavy > 0.18). Eleven is few, so treat that group's
  class with care. The groups are separate because a document that says
  it builds on another body's work is expected to point to it often.
- Across the 95: 72 light, 16 typical and 7 heavy (IG1339, IG1343,
  IG1218F, TMFS026, IG1280, GB1059 and IG1330).
- **Copied words** (with `--sources`): the words copied word for word from
  outside sources (base, cited and undeclared together), per 1,000 words
  of the document, classed by a fixed rule (`copied_class_rule` in
  `dependence-reference.json`): **light** below 1, **typical** 1 to 20,
  **heavy** above 20. Mean − 0.8σ (mean 9.0, σ 15.2) is below zero, so
  classing at mean ± 0.8σ could never give light.
- TM Forum's §14.1 notice is adapted from the ISOC copyright statement in
  older RFCs, so the script masks any text matching the IPR Policy copy
  before comparing; otherwise every TM Forum document matches RFC 2753 and
  RFC 3198.
- The held sources are 17 free specifications the sample cites, kept in
  `sdo-sources/<body>/` at the repository root (3GPP TS 28.100, 28.111,
  28.310, 28.312, 28.530, 28.531 and 28.541; ETSI GS ZSM 002 and NFV-IFA
  011, 013 and 014; RFC 2753, 3198, 6749 and 7519; OpenID Connect Core 1.0;
  the A2A specification). Add to the folder as needed. It needs .docx,
  .pdf, .txt or .md: unpack 3GPP zips, save legacy .doc files as .docx,
  and convert HTML pages to text.
- A document **cites a held source** when it names a specification we hold
  by its document number (for example 3GPP TS 28.312 or RFC 6749), or the
  manifest says so for a citation the numbers miss (TR255's "NFV IFA011").
  Only those documents are classed, because for a document that cites none
  of the held specifications a result of 0 only means there was nothing to
  compare it with, not that it is clean. Such a document is reported as
  "none found; sources not held", or, if a match turns up anyway (IG1252
  shares 58 words with TS 28.100, which it doesn't cite), as its figure
  "not classed (cites no held source)".
- Eighteen of the 95 documents cite a held source. Three are heavy:
  IG1526A (62 per 1,000), IG1453 v2.0.0 (25) and IG1453 v2.1.0 (20.3).
  Nine copy nothing and are light; the other six are typical.
- Published TM Forum deliverables add to the SDO work they build on
  rather than restating it, so any copied normative text is a finding.

## Automation Indicators

- Classed by rank (`class_rule`): **low** at or below the score that ends
  the bottom quarter of the reference set, **high** at or above the score
  that starts its top fifth, **medium** in between. On the 95 documents
  that is low ≤ 0.30 and high ≥ 3.59: 24 low, 52 medium, 19 high (3 of
  them direct evidence). Any occurrence of sign 1 or 2 makes the class
  high (direct evidence) whatever the score.
- Mean 2.04, σ 2.41. The scores pile up at zero (13 documents score
  exactly 0) and σ is larger than the mean, so bands at mean ± 0.8σ would
  say little; z is given for context and the author table.
- Style shift (sign 4): a long paragraph (40+ words) counts only with at
  least 2 AI-typical words, at 4 or more per 100 words and three times the
  document's rate, so a single AI-typical word in a short paragraph isn't
  enough.
- Figure labels that contradict the text (sign 3) are counted but score 0:
  a mismatch shows that a figure and its text disagree, not who or what
  wrote them. They are reported in their own Figure labels column.
- Signs 1 and 2 are absolute points (up to four occurrences each), not
  rates: one leftover assistant line is direct evidence in a short document
  and a long one alike. Signs 4 and 5 are rates (a share of long
  paragraphs; AI words and em dashes per 1,000 words). The script prints
  the two parts of the score apart. `ai_indicators.py --reference` prints
  every reference document's score.
- Sign 2 reads the document's own properties (creator, last modified by,
  application, custom properties naming an AI tool) only when the record
  has a .docx path. IG1251C, TR255 and IG1351 have none, so their
  properties aren't checked.
- Pictures exported from Confluence usually lose their metadata, so no
  provenance found doesn't mean none existed.

## ODA content

- Fixed rule: **light** below 5, **typical** 5 to 20, **heavy** above 20,
  per 1,000 words, equal weights over seven parts (components, canvas,
  APIs, frameworks, use cases, HVS, solution packages).
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
- Of the 95 documents, 10 are heavy (IG1242 v26.0.0 and v24.0.0,
  TAC-1012, IG1228, IG1330, TMFS033, IG1222, GB1022, IG1171 and TMFS020),
  25 typical and 60 light. The AN L4 solution-package guides are mostly
  light, because the score uses term density only, not the title or
  document type, and their text rarely names ODA or TM Forum next to
  "solution package" or "HVS". `oda_score.py --reference` prints the
  table.
- TMF443, TMF444 and TMF445 cite each other's numbers and GB1022's title
  is "ODA Functional Architecture": their scores are counted with those
  names removed (`excluded_own` in the reference file; `--exclude-own` on
  the command line).

## Depth of check (tiers)

`scripts/triage.py` picks a provisional tier from the cheap first pass:
**light** (nothing found), **doubled** (something found, provisional poorly
cited score not above 0.15 per 1,000 words) or **redoubled** (that score
above 0.15, or 10 or more words per 1,000 copied from held sources).

- The trigger is "a passage credited to a source outside TM Forum, or any
  word-for-word match to a held source". Image-scan flags aren't part of
  it: most flags on text-heavy diagrams are false alarms.
- The deeper tiers ask for the steps the light floor leaves out and that
  find what a light check misses: placing every credited passage, not
  only the first; looking at adapted figures at full size, not only on a
  contact sheet; and comparing figure labels with the text.
- The tier is a guide to effort, not a score: it has no class and no z.
- The 10-per-1,000 copied-words line: of the six reference documents at
  or above it (IG1526A, IG1453 v2.0.0 and v2.1.0, IG1572, IG1330 and
  IG1339), five are bad on poorly cited ownership; IG1339 isn't. It is
  half the heavy line for copied words (20), because the tier is a guide
  to effort, so a typical document can still be redoubled.

## Editorial consistency

- Expected weighted findings for a document's length are fitted across the
  95 documents as `a × (words ÷ 1,000)^b`, with a = 11.2269 and b = 0.3903.
  The score is the document's weighted findings divided by that number.
  Across the set the scores have mean 1.37, median 1.31 and σ 0.89.
- Classed by rank (`class_rule` in `editorial-reference.json`):
  **consistent** is the bottom 40% of the reference scores, and
  **improving**, **inconsistent** and **very inconsistent** 20% each. On
  the 95 that is consistent up to 0.920, improving up to 1.575,
  inconsistent up to 2.121 and very inconsistent above: 38, 19, 19 and 19
  documents. `editorial_score.py` reads the cut-offs from the reference
  file, so a rebuild moves them.
- Classing by rank gives each class a fixed share whatever the reading
  standard of a batch of documents, because documents read by different
  readers, or at different times, can differ in how many findings they
  record.
- `--build-reference` keeps `a` and `b` unless `--refit` is given; rebuild
  with `--refit` so the expected-findings curve and the cut-offs come from
  the same documents.

## Spreadsheet sets

The 19 spreadsheets, in `references/spreadsheet/`, with the same class
rules as the Word sets. Nineteen is few, so a class rests on few
comparisons and the rank cut-offs move noticeably when a workbook is
added.

- **Poorly cited ownership:** mean 0.075, σ 0.139 (ownership: mean 0.103,
  σ 0.172). 13 good, 2 improving, 4 bad.
- **Automation Indicators:** mean 1.04, σ 2.83. 14 of the 19 score
  exactly 0, so the bottom quarter ends at 0 and all 14 are low; high is
  0.49 or more. 14 low, 1 medium, 4 high (1 of them direct evidence).
- **Pointer rate:** six spreadsheets have a declared base (mean 1.30, σ
  0.77, so light < 0.68, heavy > 1.92) and 13 have none (mean 0.54, σ
  0.44, so heavy > 0.89). For those without a base, light is no pointers
  at all, as in the Word set (4 of the 13 have none); here mean − 0.8σ is
  0.20, and no spreadsheet without a base has a rate between 0 and 0.20,
  so classing at mean ± 0.8σ would give the same classes. 5 light, 10
  typical, 4 heavy.
- **Copied words:** ten spreadsheets cite a held source (mean 23.2, σ
  35.5, for context). The fixed rule (light below 1, heavy above 20)
  applies as for Word documents.
- **ODA content:** all 19 are light under the fixed rule.
- **Editorial consistency:** fitted as `a × (words ÷ 1,000)^b` with
  a = 6.7456 and b = 0.1475; findings in a workbook barely grow with its
  word count. Scores have mean 1.81, σ 1.61. By rank: consistent up to
  1.074, improving up to 2.186, inconsistent up to 3.768, very
  inconsistent above: 8, 4, 4 and 3 spreadsheets.
