# The six references

This file holds the citation for each of the six references the IP and
licence scan uses, and the central test of Reference 1. SKILL.md says when
to show a citation: under the heading of a reference that has findings.
Quote a document's own wording only where its terms allow it. The ISO/IEC
standards are paid, copyrighted texts: refer to them by clause, never
reproduce them.

## Which document to use

| Question | Document |
|---|---|
| Which licence mode or copyright notice applies to a TM Forum deliverable (spec, YAML, API)? Who owns a Contribution? | 1. TM Forum IPR Policy |
| What a licence compliance programme needs: policy, roles, scanning and review, notices, record keeping | 2. ISO/IEC 5230 |
| Checking open-source components for known vulnerabilities as part of the same programme | 3. ISO/IEC 18974 |
| How to label each file's licence and copyright, and the format for a software bill of materials (SBOM) | 4. SPDX and REUSE |
| How third-party text, images and figures in a document should be credited | 5. Creative Commons attribution practice |
| Whether a document declares its GenAI use, and who is responsible for AI-produced content | 6. COPE, Authorship and AI tools |

References 2–4 are for code and software; references 5 and 6 are their
counterparts for documents, text and images.

## 1. TM Forum Policy on Intellectual Property Rights

- **Author / publisher:** TM Forum (Board of Directors). By-laws Annex 1.
- **Version:** IPR Policy v6, January 2018 (By-laws version 7.2,
  November 2017). © TM Forum 2017.
- **Where:** [TMF-IPR-Policy-v6.md](TMF-IPR-Policy-v6.md),
  a Markdown conversion of the PDF `IPR_v6_Jan_2018_Final.pdf`. If the
  conversion and the PDF differ, the PDF is authoritative.
- **Relevant sections:**
  - §5 Contributions (§5.1.3 copyright holders identified, §5.1.5
    ability to grant, §5.2.1 licence of the Contributor's own copyright,
    §5.2.2 Copyright License Grant needed for non-Contributors' material,
    §5.3 trademarks); Appendix B, the Copyright License Grant form
  - §10 Licensing Requirements: §10.1 RAND, §10.2 RF, §10.3 FORUM
    Click-Through License (FCTL), §10.4 Apache 2.0
  - §14 Notices: §14.1 documents, §14.2 other deliverables, §14.4 the
    Apache 2.0 notice for TM Forum API Deliverables
- **Use it for:** the licence mode and notice that TM Forum material
  carries, such as `RAND licence mode: Notice` in this repository's
  generated files and YAML comments.
- **The central test: was it theirs to contribute?** Content enters a
  TM Forum document as Members' Contributions. §5.2.1 licenses to TM Forum
  only what a Contributor itself holds copyright in. For anything owned
  by someone who isn't a Contributor (a non-contributing Member, a
  publisher, an author, a vendor, an open-source project, a clip-art or
  icon library), §5.2.2 requires a signed Copyright License Grant
  (Appendix B) from each such owner, and §5.1.3 and §5.1.5 make the
  Contributor represent that those holders are identified and that
  nothing limits its ability to grant. So for every item of material the
  checks find that originated outside the document, report:
  - **Owner:** who holds the rights, as far as can be identified, or
    "unknown".
  - **Contributor or not:** whether that owner is a Contributor to this
    document (its company appears in the Acknowledgements).
  - **Grant recorded:** whether the document records a §5.2.2 grant or
    other permission (it almost never does: say "not recorded in the
    document").

  Material owned by a non-Contributor is the main finding of this skill,
  whatever the credit: a correct credit doesn't make it the
  Contributor's to contribute.
- **Clip art and icons are excluded.** Clip art and icons are made to be
  reused by their users, so they aren't non-Contributor material for this
  test and aren't counted in any ownership finding or score. Still list
  them in the image table (result: **clip art/icons, excluded**) so the
  reader can see what the scan flagged. This covers the individual clip-art
  figures and icons only: if a whole figure appears to be copied from
  another work (for example a diagram matching a published one, or a
  figure whose blur or style suggests it was lifted from elsewhere),
  report that figure as usual.
- **A contributing Member's own material meets the policy.** When a
  document credits material to a Member that is itself a Contributor to
  that document, for example a field insight credited to a named
  contributor, or a company's own practices described under that
  company's name, treat it as intentional and compliant (§5.1.4, §5.2.1,
  §5.3.3). Report it as a contributing Member's own material, not as a
  finding, and count it as correctly cited. This covers only what the
  Member itself owns: third-party material a Member passes on (another
  company's figure, a paper, stock art) is still owned by a
  non-Contributor and is a finding under §5.2.2.

## 2. ISO/IEC 5230 — OpenChain Specification

- **Title:** ISO/IEC 5230:2020, *Information technology — OpenChain
  Specification*.
- **Publisher:** ISO/IEC, 2020. Developed by the OpenChain Project
  (Linux Foundation).
- **Where:** https://www.iso.org/standard/81039.html and
  https://openchainproject.org/license-compliance
- **Use it for:** the requirements of an open-source licence compliance
  programme: identifying open-source components, reviewing their
  licences, producing the required notices, and keeping records.

## 3. ISO/IEC 18974 — OpenChain Security Assurance Specification

- **Title:** ISO/IEC 18974:2023, *Information technology — OpenChain
  security assurance specification*.
- **Publisher:** ISO/IEC, 2023. Developed by the OpenChain Project
  (Linux Foundation).
- **Where:** https://www.iso.org/standard/86450.html and
  https://openchainproject.org/security-assurance
- **Use it for:** the security side of the same programme: tracking the
  open-source components in a deliverable and handling their known
  vulnerabilities.

## 4. SPDX (ISO/IEC 5962) and the REUSE specification

- **SPDX:** ISO/IEC 5962:2021, *Information technology — SPDX®
  Specification V2.2.1*. ISO/IEC, 2021. Maintained by the SPDX project
  (Linux Foundation). https://www.iso.org/standard/81870.html and
  https://spdx.dev. The SPDX License List
  (https://spdx.org/licenses/) gives the standard licence identifiers.
- **REUSE:** *REUSE Specification – Version 3.3*, Free Software
  Foundation Europe. https://reuse.software/spec-3.3/ (the latest version
  is always at https://reuse.software/spec/)
- **Use them for:** per-file `SPDX-License-Identifier` and
  `SPDX-FileCopyrightText` headers, machine-readable SBOMs, and the
  licence identifiers that scanning tools report.

## 5. Creative Commons — Recommended practices for attribution

- **Title:** *Recommended practices for attribution*.
- **Publisher:** Creative Commons, wiki page, last edited 4 December
  2024. Licensed CC BY 4.0.
- **Where:** https://wiki.creativecommons.org/wiki/Recommended_practices_for_attribution
- **Use it for:** checking how third-party material in a document is
  credited. Every reuse of CC-licensed material should give its
  **T**itle, **A**uthor, **S**ource and **L**icence (TASL), and say
  if the material was changed. The page has worked examples for images,
  text, adaptations and material from several sources. Apply TASL to
  every reproduced or adapted image and passage; a credit that gives
  only a title (as in "(Source: …)") doesn't meet it.

## 6. COPE — Authorship and AI tools

- **Title:** *COPE position – Authorship and AI tools*.
- **Publisher:** COPE (Committee on Publication Ethics) Council, 13
  February 2023 (last reviewed date). DOI
  https://doi.org/10.24318/cCVRZBms. © 2024 COPE, licensed
  CC BY-NC-ND 4.0, so cite or link it rather than adapting its text.
- **Where:** https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools
- **Use it for:** GenAI-assisted documents. COPE's position is that AI
  tools can't be listed as authors, because they can't take
  responsibility for the work or manage copyright; that authors must
  disclose which AI tool they used and how, including for images; and
  that authors remain fully responsible for everything in the document,
  including the parts an AI tool produced. Use it to judge whether a
  document declares its AI use.

## Checking a document's details

Before you cite one of these, check its current edition at the link
given. ISO standards are revised, the REUSE and SPDX specifications have
versioned releases, the Creative Commons and COPE pages can be updated,
and the TM Forum Board can amend the IPR Policy (§1).
