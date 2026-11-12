"""Combine the scans of several documents into one report, with their authors
and a separate table scoring the authors.

For each document it runs the automatic scans (Automation Indicators, dependence, and
copied text if --sources is given), reads the authors from the
Acknowledgements (authors.py), and takes the poorly cited ownership score from
the ownership items a person judged, where the manifest gives them. Poorly cited ownership, copied words, editorial
consistency and the pointer rate's light class (documents without a declared
base) use fixed rules; the AI-indicator score is classed by rank against its
reference set; the other pointer classes use mean +/- 0.8 sigma.

Usage:
  python -I combined_report.py <manifest.json> <report.md> [--sources <dir>]

manifest.json:
  (Paths below are relative to the manifest's folder, or absolute.)
  {"title": "...",                      optional, the report's first heading line
   "scope": "...",                      optional sentence on what was checked
   "documents": [
     {"dir": "<output-dir from extract_docx.py>",
      "label": "IG1242 v26.0.0",
      "key": "IG1242",                   optional short name for the author table (default: first word of label)
      "docx": "<input.docx>",            optional, lets the AI check read pictures
      "figure_mismatches": 0,            optional, from the visual image check
      "declared_base": ["ETSI"],         optional, bases the script misses
      "cites_held_source": true,         optional, when it cites a held source the identifiers miss
      "exclude_own": "TMF44[345]",       optional regex, other names of the document itself, removed before the ODA count
      "core_citation": "<source>",       optional, the core citation as citation_dates.py prints it, when the
                                         automatic pick (most passages, then mentions) is wrong
      "ownership": {"words": 9603,       optional; without it ownership is "not scanned"
                    "items": [{"item": "...", "weight": 1.0, "cited": 0.5}]}}]}

Author scores: for each person named as an author or editor, the mean z of each
measure over their documents, how many of those documents were flagged (bad,
high or heavy), and an overall score (the mean of their measure scores).
Then render the report with make_report.py.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import datetime
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ai_indicators  # noqa: E402  (same folder; -I doesn't add it to sys.path)
import authors as authors_mod  # noqa: E402
import citation_dates  # noqa: E402
import dependence  # noqa: E402
import oda_score  # noqa: E402
import editorial_score  # noqa: E402
import ownership_score  # noqa: E402

REF = os.path.join(HERE, "..", "references")
DISCLAIMER = ("> **Disclaimer:** Using this skill is not legal advice. It does not provide a valid legal defence "
              "for any infringement, misuse or other abuse of intellectual property or other rights. "
              "Responsibility for how material is used stays with the user. Get qualified legal advice where "
              "rights are in doubt.\n")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def poorly_cited(words, items):
    return sum(i["weight"] * (1 - i["cited"]) for i in items) / words * 1e3


def reference_stats():
    own = load(os.path.join(REF, "ownership-reference.json"))
    poor = [poorly_cited(d["words"], d["items"]) for d in own["documents"]]
    _, ai_m, ai_sd, k = ai_indicators.reference_stats()
    dep, dstats = dependence.load_reference()
    return {"k": k, "poor": (statistics.mean(poor), statistics.pstdev(poor)), "poor_rule": own.get("class_rule"),
            "ai": (ai_m, ai_sd), "ai_cuts": ai_indicators.class_cuts(),
            "ptr": dstats, "copy": dstats.get("copied"), "dep": dep,
            "ed": editorial_score.reference()}


def poor_class(value, zv, s, k, items=()):
    """Poorly cited ownership: a fixed rule when the reference file has one, else the mean and sigma.
    items are the judged ownership items (dicts with weight and cited)."""
    rule = s.get("poor_rule")
    if rule:
        return ownership_score.fixed_poor_class(value, [(i["weight"], i["cited"]) for i in items], rule)
    return band(zv, k, ("good", "improving", "bad"))


def poor_text(p, s, k):
    rule = s.get("poor_rule")
    if rule:
        return ("The class is set by a fixed rule, not by comparison with the other documents: **good** is a "
                "score up to %.2f per 1,000 words%s, **bad** is a score above %.2f per 1,000 words (roughly "
                "one word-for-word passage with no credit for every 6,700 words), and **improving** is anything in "
                "between. For context, the mean across the reference set is %.3f and σ %.3f."
                % (rule["good_at_most"], ", as long as no whole figure or word-for-word passage is left with no "
                   "credit at all" if rule.get("good_needs_no_uncredited_whole_item") else "",
                   rule["bad_above"], p[0], p[1]))
    return ("Across the reference set the mean is %.2f and σ %.2f. A score below %.2f is **good**, above %.2f is "
            "**bad**, and anything between is **improving**." % (p[0], p[1], p[0] - k * p[1], p[0] + k * p[1]))


# The held-source helpers live in dependence.py, which also needs them.
held_names = dependence.held_names
cites_held = dependence.cites_held


def z(v, s):
    return (v - s[0]) / s[1] if s and s[1] else 0.0


def band(zv, k, words):
    return words[2] if zv > k else words[0] if zv < -k else words[1]


# Said wherever a spreadsheet's scores appear: the reference sets and class rules were built from prose documents.
SPREADSHEET_NOTE = ("This document is a spreadsheet (.xlsx), read cell by cell with extract_xlsx.py. Its scores "
                    "aren't comparable with those of the Word documents: the per-1,000-word rates, the AI-wording "
                    "signs, the editorial expectation for its length and every reference set were built from prose "
                    "documents, and short, repeated cell text shifts them in ways those sets don't allow for.")


def is_spreadsheet(entry):
    """A workbook checked with extract_xlsx.py: its input is a .xlsx, or its extract says so."""
    marker = os.path.join(entry["dir"], "source_format.txt")
    if (entry.get("docx") or "").lower().endswith(".xlsx"):
        return True
    if os.path.isfile(marker):
        with open(marker, encoding="utf-8") as f:
            return f.read().strip() == "xlsx"
    return False


def scan(entry, sources, held, s, as_of):
    d = {"label": entry["label"], "key": entry.get("key") or entry["label"].split()[0],
         "figure_checked": "figure_mismatches" in entry, "spreadsheet": is_spreadsheet(entry)}
    with open(os.path.join(entry["dir"], "text.txt"), encoding="utf-8") as f:
        raw = f.read()
    k = s["k"]
    people = authors_mod.people_in(raw)
    d["people"] = [(p["name"], p["company"]) for p in authors_mod.authors_of(people)]

    own = entry.get("ownership")
    if own is not None:
        d["poor"] = poorly_cited(own.get("words") or len(raw.split()), own["items"])
        d["z_poor"] = z(d["poor"], s["poor"])
        d["poor_cls"] = poor_class(d["poor"], d["z_poor"], s, k, own["items"])
        d["own_items"] = own["items"]
    else:
        d["poor"] = d["z_poor"] = d["poor_cls"] = None

    a = ai_indicators.measure(entry["dir"], entry.get("docx"), entry.get("figure_mismatches", 0))
    d["ai"] = a
    d["z_ai"] = z(a["score"], s["ai"])
    d["ai_cls"] = ai_indicators.class_of(a["score"], s["ai_cuts"], bool(a["assistant"] or a["provenance"]))

    text = "\n".join(l for l in raw.splitlines() if not dependence.CONTENTS_LINE.match(l.strip()))
    r = dependence.reference_measures(text)
    declared = sorted(set(r["declared"]) | set(entry.get("declared_base", [])))
    d.update(dep=r, declared=declared)
    group = "declared" if declared else "none"
    d["z_ptr"], d["ptr_cls"] = dependence.classify(r["pointer_rate"], r["pointers"], group, s["dep"], s["ptr"])
    m = r["mentions"]
    d["undeclared"] = r["top_body"] if r["top_body"] and r["concentration"] >= 0.5 \
        and sum(m.values()) >= dependence.MIN_BASE_MENTIONS and r["top_body"] not in declared else None

    ed = entry.get("editorial")  # {"words": n, "counts": {category: n}}, from the document's editorial.json
    d["ed"] = d["z_ed"] = d["ed_cls"] = None
    if ed:
        d["ed"] = editorial_score.evaluate(ed["counts"], ed["words"], s.get("ed"))
        if d["ed"]["score"] is not None:
            d["z_ed"], d["ed_cls"] = d["ed"]["z"], d["ed"]["class"]

    d["oda"] = oda_score.measure(raw, entry.get("exclude_own"))
    d["web"] = entry.get("web_check")  # {"searched": n, "outside": n}, counted from the document's own report
    cites = citation_dates.citations(entry["dir"], sources, as_of, entry.get("core_citation"))["citations"]
    d["core"] = next((c for c in cites if c["core"]), None)
    d["copy"] = d["z_copy"] = d["copy_cls"] = None
    if sources:
        c = dependence.copy_measures(text, sources, declared, 8, 12)
        d["copy"] = c
        d["copied"] = (1 - c["original"]) * 1000  # copied words per 1,000 words
        # Held: the document names a held source's number, or the manifest says so (for a document that
        # cites its sources in a way the identifiers don't catch, such as TR255's "NFV IFA011").
        d["cites_held"] = bool(entry.get("cites_held_source", cites_held(r["doc_ids"], held)))
        if d["cites_held"] and s["copy"]:
            d["z_copy"] = z(d["copied"], s["copy"])
            d["copy_cls"] = dependence.copy_class(d["copied"], s["dep"])
    return d


FLAGGED = {"z_poor": lambda d: d["poor_cls"] == "bad", "z_ai": lambda d: d["ai_cls"].startswith("high"),
           "z_ptr": lambda d: d["ptr_cls"] == "heavy", "z_copy": lambda d: d["copy_cls"] == "heavy",
           "z_ed": lambda d: d["ed_cls"] in editorial_score.FLAGGED}


MIN_AUTHOR_DOCS = 2  # people named on fewer documents than this aren't in the author table


def author_people(docs):
    """Every person named as an author or editor, with the number of documents they're named on."""
    by = {}
    for d in docs:
        for n, _ in d["people"]:
            by[n] = by.get(n, 0) + 1
    return by


def author_rows(docs):
    by = {}
    for d in docs:
        for n, c in d["people"]:
            e = by.setdefault(n, {"companies": [], "docs": []})
            if c and c not in e["companies"]:
                e["companies"].append(c)
            e["docs"].append(d)
    rows = []
    for n, e in by.items():
        if len(e["docs"]) < MIN_AUTHOR_DOCS:
            continue  # one document's score is that document's own score, already in the document table
        cols = []
        for field in ("z_poor", "z_ai", "z_ptr", "z_copy", "z_ed"):
            v = [x for x in e["docs"] if x[field] is not None]
            cols.append((statistics.mean(x[field] for x in v), len(v), sum(1 for x in v if FLAGGED[field](x)))
                        if v else (None, 0, 0))
        # The editorial column shows the plain average of the documents' editorial scores, classed with the
        # documents' own fixed bands; the overall score still uses the editorial z.
        ed = [x["ed"]["score"] for x in e["docs"] if x["ed"] and x["ed"]["score"] is not None]
        e["ed_avg"] = statistics.mean(ed) if ed else None
        rows.append((statistics.mean(c[0] for c in cols if c[0] is not None), n, e, cols))
    return sorted(rows, key=lambda r: (-r[0], r[1]))


def report(manifest, docs, s, sources, as_of, core_age_only=True):
    """core_age_only: the core citation cell gives only the age (the combined report); document_scores.py
    passes False so a document's own score row also names the citation."""
    k = s["k"]
    out = []
    w = out.append
    w(DISCLAIMER)
    if manifest.get("scope"):
        w("**Scope:** " + manifest["scope"] + "\n")
    w("Each score's class is set as its section below says: by a fixed rule, by rank against a reference set, "
      "or against a reference set at ±%.1fσ. z is the number of standard deviations from the reference mean, "
      "given for context; on every measure a higher z means more of what the measure looks for.\n" % k)

    p, a, ptr, cp = s["poor"], s["ai"], s["ptr"], s["copy"]
    w("## Document scores\n")
    w("**Poorly cited ownership.** Material in a document that belongs to someone who isn't a Contributor to it. "
      "TM Forum's IPR Policy (§5.2.1, §5.2.2) lets a Contributor license only what it owns, so outside material "
      "needs its owner's permission and a proper credit. A person judges each item (a copied passage, or a "
      "reproduced or adapted figure) and gives it a weight: 1.0 for a whole figure or a word-for-word passage, "
      "0.5 for an adapted figure, a close paraphrase or an item of unconfirmed origin. Each item also gets a "
      "credit value: 1.0 for a complete credit (title, author, source, licence and the work's publication date), "
      "0.75 for one complete but for the date, 0.5 for a partial credit, "
      "0 for none or a credit to the wrong source. The score is each item's weight times (1 minus its credit "
      "value), added up and expressed per 1,000 words, so a word-for-word passage with no credit adds 1.0 and "
      "one with a complete credit adds nothing. Clip art and icons, material owned by a contributing Member, and "
      "reworded ideas aren't counted. %s A bad score means credits are missing or wrong "
      "for outside material; it doesn't by itself show that anything was taken in bad faith.\n"
      % (poor_text(p, s, k),))
    w("**Automation Indicators.** How many signs there are that a document, or parts of it, were produced with "
      "generative AI. It adds up five signs: leftover assistant text such as \"as an AI language model\" (5 "
      "points each), AI provenance metadata inside pictures (5 each) or an AI tool named in the document's own "
      "properties, such as its creator (5), a shift in style between paragraphs (up to 10), and AI-typical words "
      "and em dashes per 1,000 words. Figure labels that contradict the text aren't part of it: they have their "
      "own column. The class is set by rank against the reference set: **low** is a score up to %.2f (the "
      "bottom quarter), **high** a score of %.2f or more (the top fifth), and **medium** in between; for "
      "context the mean is %.2f and σ %.2f. Any leftover assistant text or AI provenance makes the class "
      "**high (direct evidence)** whatever the score. These are indicators, not proof: AI-text detection is "
      "unreliable, flags human writing (especially by non-native English speakers) and misses AI text that was "
      "edited.\n"
      % (s["ai_cuts"][0], s["ai_cuts"][1], a[0], a[1]))
    w("**Figure labels.** How many of a document's figures carry a label (a stage, step, role, layer or number) "
      "that contradicts the text around it, from a person's (or model's) comparison of each figure at full size "
      "with its caption and text. A contradiction shows that a figure and its text disagree, often because one was "
      "carried over from another document or changed without the other. It doesn't show who or what wrote either, "
      "so it isn't scored as an AI sign. \"Not compared\" means no figure was compared, for example because the "
      "document's only pictures are logos. It has no class and no z, and isn't used in the author scores.\n")
    w("**Dependence: pointers.** How often the document sends the reader to another standards body's documents "
      "in order to understand it. It counts phrases such as \"as defined in\", \"see\" or \"according to\" that "
      "are followed within ten words by a standards body (3GPP, ETSI, IETF and others) or an outside document "
      "number, per 1,000 words. A document that says it builds on another body's work (its declared base, found "
      "in its title, scope or introduction) is expected to point to that body, so it is judged only against "
      "other documents that declare a base (mean %.2f, σ %.2f); other documents are judged against those that "
      "don't (mean %.2f, σ %.2f). **Heavy** is above the mean plus %.1fσ and needs at least %d pointers; "
      "**light** is below the mean minus %.1fσ for documents with a declared base, and no pointers at all for "
      "documents without one (most of them have none, so the mean minus %.1fσ is below zero); **typical** is "
      "in between. \"Possible undeclared base\" means one "
      "body accounts for half or more of the mentions of outside bodies, but the document doesn't say it builds "
      "on that body. This measures reliance by reference, not copying.\n"
      % (ptr["declared"][0], ptr["declared"][1], ptr["none"][0], ptr["none"][1], k,
         s["dep"]["min_heavy_pointers"], k, k))
    if cp:
        w("**Dependence: copied.** How many of every 1,000 words of the document sit in runs of 12 or more words "
          "identical to an outside source held in `%s` (free 3GPP, ETSI, IETF, OpenID Foundation and A2A "
          "specifications). TM Forum's own §14.1 notice, adapted from the ISOC statement in older RFCs, is masked "
          "out first. The class is set by a fixed rule: **light** is below %g per 1,000 words, **heavy** above %g, "
          "and **typical** in between (for context, the reference documents that cite a held source have a mean "
          "of %.1f per 1,000 and σ %.1f). A document \"cites a held source\" when it names a specification we hold, by "
          "its document number (for example 3GPP TS 28.312 or RFC 6749). Only those documents are classed, "
          "because for a document that cites none of the held specifications a result of 0 only means there was "
          "nothing to compare it with; it doesn't show the document is clean. Its cell says \"none found; "
          "sources not held\", or, if a match with a held specification turns up anyway, shows the figure and "
          "\"not classed (cites no held source)\". The check finds word-for-word copying only, not paraphrase; the "
          "evidence table below names the source and how many words matched.\n"
          % (os.path.basename(os.path.normpath(sources)) if sources else "the sources folder",
             s["dep"]["copied_class_rule"]["light_below"], s["dep"]["copied_class_rule"]["heavy_above"], cp[0], cp[1]))
    if s.get("ed"):
        er = s["ed"]
        e_m, e_sd = er["mean"], er["sigma"]
        w("**Editorial consistency.** This skill's addition, not an IP or licence measure: how far the document "
          "is consistent with itself. A reader goes through the whole document and records findings in five "
          "categories, each weighted by how far it stops a reader relying on the document: internally "
          "inconsistent rules (3), unsupported specificity (2), implementation detail given more normative weight "
          "than its evidence (2), incomplete references and cross-references (1) and duplicate concepts (1). "
          "Findings don't grow in proportion to length (some faults, such as an empty section, happen once per "
          "document), so the score compares the document's weighted findings with the number expected for a "
          "document of its length, fitted across the reference set as %.2f × (words ÷ 1,000)^%.2f: 1.00 is typical "
          "for its length, 1.50 is half as many again. The class is set by a fixed rule, not by comparison with "
          "the other documents: **consistent** up to %.2f, **improving** up to %.2f, **inconsistent** up to %.2f, "
          "and **very inconsistent** above %.2f. For context, the mean score across the reference set (the %d "
          "documents checked this way) is %.2f and σ %.2f, which gives the z. The cell gives the score and its "
          "class. It rests on one reading per document, so it is a judgement, not a count a script repeats; "
          "each document's own report lists every finding with its location.\n"
          % (er["a"], er["b"], editorial_score.CLASS_RULE[0][0], editorial_score.CLASS_RULE[1][0],
             editorial_score.CLASS_RULE[2][0], editorial_score.CLASS_RULE[2][0], er["n"], e_m, e_sd))
    w("**Web check.** What the web search found for the passages of the document that were searched. Each "
      "passage the document credits to an outside source, and about 20 further sentences chosen as the most "
      "likely to have come from outside, is searched in quotation marks on the public web. The cell gives how "
      "many passages were searched and how many turned up, word for word or nearly, on a page outside TM Forum. "
      "A match on a TM Forum page is expected and isn't counted, and neither is a credited source's own title. "
      "The count comes from the web-check table in each document's own report; it isn't a score and has no "
      "class. It also feeds the ownership score indirectly, because a match makes that passage an item to judge. "
      "A search that finds nothing only means the text isn't on the indexed public web; paywalled and "
      "member-only sources aren't searched this way, and the search tool summarises results rather than "
      "matching exact strings. The matches themselves, with their addresses, are in each document's report.\n")
    w("**Core citation.** The outside source the document leans on most, and how old it is. Among the sources "
      "the document credits (leaving out TM Forum's own), it is the one with the most credited passages, then "
      "the most mentions of its document number in the text; where a person judged that pick wrong, the "
      "manifest names it instead. Its publication date comes from the credit itself, else from the front page "
      "of a held copy in the sources folder, else from the skill's citation-dates list (dates read from the "
      "source's own page when the web check opened it); \"date not found\" means none of these dates it. Age "
      "is in years to %s. It isn't a score and has no class or z; an old core citation only says the document "
      "rests on older work.%s\n" % (as_of.isoformat(), " The cell gives the age only; each document's own report "
                                    "names the citation and its date." if core_age_only else ""))
    w("**ODA content.** How much of the document is about TM Forum's ODA, counted by term density: the terms for "
      "TM Forum's ODA components, canvas, Open APIs, frameworks, use cases, HVS and solution packages, per 1,000 "
      "words, added up with equal weights, after removing the document's own identifier. Only TM Forum's items "
      "count. Names that are TM Forum's own (eTOM, ODA Canvas, ODA Component, Frameworx) always count; component "
      "and API numbers count only if TM Forum has published them (a TMFC number in the component inventory or "
      "component specifications, a TMF number of a TM Forum Open API); generic terms (use case, SID, Open API, "
      "Information Framework, solution package, high-value scenario) count only in a paragraph that names TM Forum, "
      "ODA, eTOM, a TMF or TMFC number or a TM Forum document, or in the paragraph either side. \"OpenAPI\" and "
      "\"Open API Specification\" never count. **Light** is below 5, **typical** 5 to 20 and **heavy** above 20, a "
      "fixed rule. The cell also gives how many of the seven parts appear at least once per 1,000 words. It counts "
      "mentions only, not the title or document type, and it isn't a risk score: it has no z and isn't used in the "
      "author scores.\n")
    w("Documents are listed by risk: highest poorly cited ownership first, and within equal ownership (most are "
      "0.00) highest Automation Indicator score first.\n")
    w("| Document | Authors | Poorly cited ownership | Automation Indicators | Dependence: pointers | Dependence: copied "
      "| Editorial consistency | Web check | Figure labels | %s | ODA content |"
      % ("Core citation age" if core_age_only else "Core citation (age)"))
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for d in sorted(docs, key=lambda d: (-(d["z_poor"] if d["z_poor"] is not None else -99), -d["z_ai"], d["key"])):
        names = "; ".join("%s (%s)" % p for p in d["people"]) or "none named"
        own = "%.3f %s" % (d["poor"], d["poor_cls"]) if d["poor"] is not None else "not scanned"
        ai = "%.2f %s" % (d["ai"]["score"], d["ai_cls"])
        ptr = "%.2f %s" % (d["dep"]["pointer_rate"], d["ptr_cls"])
        if d["declared"]:
            ptr += "; base %s" % ", ".join(d["declared"])
        if d["undeclared"]:
            ptr += "; possible undeclared base %s" % d["undeclared"]
        if d["copy"] is None:
            cp = "not checked"
        elif d["copy_cls"] is None:
            # No class, because the document cites no held source. A match with a held source is still
            # shown: the share is real even though it can't be compared with the reference set.
            cp = ("%.1f per 1,000 found, not classed (cites no held source)" % d["copied"]) if d["copied"] > 0 \
                else "none found; sources not held"
        else:
            cp = "%.1f per 1,000 %s" % (d["copied"], d["copy_cls"])
        wc = d["web"]
        web = ("%d searched; %s outside TM Forum" % (wc["searched"], "none" if not wc["outside"] else wc["outside"])
               if wc else "not recorded")
        fig = "%d contradicting the text" % d["ai"]["mismatches"] if d["figure_checked"] else "not compared"
        c = d["core"]
        if core_age_only:
            core = "none outside TM Forum" if not c else "date not found" if not c["published"] else \
                "%.1f years" % c["age"]
        else:
            core = ("none outside TM Forum" if not c else "%s; date not found" % c["label"][:80].replace("|", "/")
                    if not c["published"] else "%s; published %s; %.1f years" % (
                        c["label"][:80].replace("|", "/"), c["published"], c["age"]))
        oda = "%.1f per 1,000 (%s), %d of 7 parts" % (d["oda"]["score"], d["oda"]["class"], d["oda"]["categories"])
        if d["ed"] is None:
            ed = "not checked"
        elif d["z_ed"] is None:
            ed = "%d weighted findings, not classed (no reference set)" % d["ed"]["weighted"]
        else:
            ed = "%.2f %s" % (d["ed"]["score"], d["ed_cls"])
        w("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
          % (d["label"] + (" (spreadsheet; not comparable)" if d["spreadsheet"] else ""), names, own, ai, ptr,
             cp, ed, web, fig, core, oda))
    note = "\nCells give the score and its class."
    if any(d["poor"] is None for d in docs):
        note += (" Poorly cited ownership needs a person to judge each item, so it's \"not scanned\" where no "
                 "one has.")
    w(note + "\n")

    w("## Author scores\n")
    w("**Author and Company.** The name and company as the document's Acknowledgements give them, with spellings "
      "of one person merged. A person is counted as an author if they're named as an author, co-author, lead "
      "author or editor. Contributors, key contributors, reviewers and TM Forum's reviewing editors aren't "
      "counted. Only people named on %d or more documents are listed: for someone named on one document, the "
      "scores would only repeat that document's row in the table above. A person named on documents for more "
      "than one company shows each company. Authors are listed from the highest overall score.\n"
      % MIN_AUTHOR_DOCS)
    w("**Documents.** The documents the person is named on as an author or editor, by short name. The same "
      "document appears against every author named on it, and each of them is given the document's scores in "
      "full, however many authors it has.\n")
    w("**The five score columns.** The first four show the author's average z-score across their documents (Editorial shows a plain average; see below), with the "
      "number of those documents that were flagged in brackets. A z-score says how many standard deviations a "
      "document sits from the reference average for that measure: 0 is average, and a positive score means more "
      "of what the measure looks for. In the brackets, \"1 of 3\" means one of the three documents that have "
      "the measure was classed bad, high, heavy or (very) inconsistent. A dash means none of the author's documents has the "
      "measure.\n")
    w("**Poorly cited ownership.** The average of the poorly cited ownership z-scores (explained above) across "
      "the author's documents. A high figure means their documents tend to carry outside material with missing or "
      "wrong credit. The bracket counts documents classed **bad**. In this report every document has this "
      "score; a document whose ownership items weren't judged would show a dash.\n")
    w("**Automation Indicators.** The average of the Automation Indicator z-scores. A high figure means their documents tend to "
      "show more of the signs of generative-AI text: leftover assistant text, AI provenance in pictures or document properties, "
      "style shifts and AI-typical wording. The bracket counts documents classed **high**.\n")
    w("**Pointers.** The average of the dependence-by-pointers z-scores. A high figure means their documents "
      "tend to send the reader to other standards bodies' documents more than similar documents do (documents "
      "that declare a base are compared with others that declare one). The bracket counts documents classed "
      "**heavy**.\n")
    w("**Copied.** The average of the copied-text z-scores, using only the author's documents that cite a source "
      "held in the sources folder. A high figure means more of their documents' words match an outside "
      "specification word for word. The bracket counts documents classed **heavy**. A dash means none of their "
      "documents cites a held source, so nothing could be compared.\n")
    w("**Editorial.** Unlike the four columns before it, this is a plain average, not a z-score: the average "
      "editorial consistency score (this skill's addition, explained above) of the author's documents, classed "
      "with the same fixed bands as a document: **consistent** up to %.2f, **improving** up to %.2f, "
      "**inconsistent** up to %.2f, **very inconsistent** above %.2f. 1.00 means their documents have, on "
      "average, the number of findings expected for their length; 1.30 means 30%% more. The bracket counts "
      "documents classed **inconsistent** or **very inconsistent**.\n"
      % (editorial_score.CLASS_RULE[0][0], editorial_score.CLASS_RULE[1][0], editorial_score.CLASS_RULE[2][0],
         editorial_score.CLASS_RULE[2][0]))
    w("**Overall.** The average of the author's z-scores on the five measures above (leaving out any with a "
      "dash; for editorial it uses the z behind the average shown, so all five are on one scale), "
      "classed at ±%.1f: **high** above +%.1f, **low** below −%.1f, and **typical** in between. It is a "
      "single figure for sorting the table, not a verdict on a person: it describes the documents they are named "
      "on, many authors are named on only two or three documents, and an author on a document with many authors "
      "carries its scores in full.\n" % (k, k, k))
    w("| Author | Company | Documents | Poorly cited ownership | Automation Indicators | Pointers | Copied | Editorial "
      "| Overall |")
    w("|---|---|---|---|---|---|---|---|---|")

    def cell(c):
        return "-" if c[0] is None else "%+.2f (%d of %d)" % (c[0], c[2], c[1])

    def ed_cell(e, c):
        if e["ed_avg"] is None:
            return "-"
        return "%.2f %s (%d of %d)" % (e["ed_avg"], editorial_score.class_of(e["ed_avg"]), c[2], c[1])

    for overall, n, e, cols in author_rows(docs):
        w("| %s | %s | %s | %s | %s | %s | %s | %s | %+.2f %s |" % (
            n, ", ".join(e["companies"]), ", ".join(d["key"] for d in e["docs"]),
            *(cell(c) for c in cols[:4]), ed_cell(e, cols[4]), overall, band(overall, k, ("low", "typical", "high"))))
    people = author_people(docs)
    once = sum(1 for v in people.values() if v < MIN_AUTHOR_DOCS)
    if once:
        w("\n%d of the %d people named as an author or editor are named on only one document and aren't in the "
          "author table.\n" % (once, len(people)))
    unnamed = [d["key"] for d in docs if not d["people"]]
    if unnamed:
        w("\nDocuments with no named author or editor (%s) aren't in the author table.\n" % ", ".join(unnamed))

    w("## Evidence behind bad, high, heavy and inconsistent results\n")
    w("| Document | Measure | Evidence |")
    w("|---|---|---|")
    for d in docs:
        if d["poor_cls"] == "bad":
            w("| %s | Poorly cited ownership | %s |" % (d["label"], "; ".join(
                "%s (weight %g, cited %g)" % (i["item"], i["weight"], i["cited"]) for i in d["own_items"])))
        if d["ai_cls"].startswith("high"):
            a, ev = d["ai"], []
            if a["assistant"]:
                ev.append("leftover assistant text: %s" % ", ".join('"%s"' % t for t in a["assistant"]))
            if a["provenance"]:
                ev.append("AI provenance in metadata: %s"
                          % "; ".join("%s (%s)" % (n, ", ".join(h)) for n, h in a["provenance"]))
            ev.append("AI-typical wording %.1f per 1,000 words (%s)" % (
                a["wording_rate"], ", ".join('"%s" ×%d' % t for t in a["top_words"][:4]) or "none"))
            if a["dash_rate"]:
                ev.append("em dashes %.1f per 1,000 words" % a["dash_rate"])
            if a["shift"]:
                ev.append("%.0f%% of long paragraphs shifted" % (a["shift"] * 100))
            w("| %s | Automation Indicators | %s; %d words |" % (d["label"], "; ".join(ev), a["words"]))
        if d["ptr_cls"] == "heavy":
            w("| %s | Dependence, pointers | %d pointers in %d words; mentions %s |" % (
                d["label"], d["dep"]["pointers"], d["dep"]["words"], ", ".join(
                    "%s %d" % kv for kv in sorted(d["dep"]["mentions"].items(), key=lambda kv: -kv[1]))))
        if d["copy_cls"] == "heavy":
            w("| %s | Dependence, copied | %s |" % (d["label"], "; ".join(
                "%d words from %s (%s)" % (r["words"], os.path.basename(r["source"]), r["role"])
                for r in d["copy"]["rows"])))
        if d["ed_cls"] in editorial_score.FLAGGED:
            names = {c: t for c, t, _ in editorial_score.CATEGORIES}
            w("| %s | Editorial consistency | %s; %d weighted findings against %.1f expected for %s words; every "
              "finding is in the document's own report |" % (d["label"], "; ".join(
                  "%s %d" % (names[c], n) for c, n in d["ed"]["counts"].items() if n), d["ed"]["weighted"],
                  d["ed"]["expected"], format(d["ed"]["words"], ",")))
    w("")

    w("## Limits\n")
    sheets = [d["label"] for d in docs if d["spreadsheet"]]
    if sheets:
        why = SPREADSHEET_NOTE.split(". ", 1)[1]
        w("- %s %s, so %s" % (", ".join(sheets), "is a spreadsheet" if len(sheets) == 1 else "are spreadsheets",
                              why[0].lower() + why[1:].replace("Its scores", "its scores")))
    w("- Authors come from each document's Acknowledgements; roles follow the document's own wording. A "
      "document's scores are attributed in full to every author named on it, so an author's score describes the "
      "documents they are named on, not their personal conduct or contribution.")
    w("- An author named on one or two documents has a score resting on very few data points.")
    no_fig = [d["key"] for d in docs if not d["figure_checked"]]
    if no_fig:
        w("- No figure check was recorded for %s, so their Figure labels cell says \"not compared\"."
          % ", ".join(no_fig))
    if not sources:
        w("- No sources folder was given, so copied text wasn't checked.")
    w("- The web-check counts are read from each document's own report, with near matches counted as matches.")
    no_ed = [d["key"] for d in docs if d["ed"] is None]
    if no_ed:
        w("- No editorial consistency check was recorded for %s." % ", ".join(no_ed))
    if any(d["ed"] is not None for d in docs):
        w("- Editorial consistency rests on one reading of each document, and the documents were read by "
          "different readers to one written method, so a difference of a few findings between two documents is "
          "within the reading's own variation. It doesn't judge whether the domain content is technically correct.")
    w("- A core citation dated from a held copy carries the date of the edition held, which may be later than "
      "the edition the document used.")
    w("- A core citation's date comes only from its credit, a held copy or the skill's citation-dates list; "
      "\"date not found\" means none of those dates it, not that the source is undated.")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest")
    ap.add_argument("report")
    ap.add_argument("--sources")
    ap.add_argument("--as-of", type=datetime.date.fromisoformat, default=datetime.date.today(),
                    help="date the core citation's age is counted to (default today)")
    a = ap.parse_args()
    a.sources = graceful.sources(a.sources)
    sys.stdout.reconfigure(encoding="utf-8")
    manifest = load(a.manifest)
    # Paths in the manifest are relative to the manifest's own folder (or absolute), so a checkout
    # of the repository works wherever it sits.
    base = os.path.dirname(os.path.abspath(a.manifest))
    for e in manifest["documents"]:
        for field in ("dir", "docx"):
            if e.get(field) and not os.path.isabs(e[field]):
                e[field] = os.path.normpath(os.path.join(base, e[field]))
    s = reference_stats()
    held = held_names(a.sources)
    docs = [scan(e, a.sources, held, s, a.as_of) for e in manifest["documents"]]
    text = report(manifest, docs, s, a.sources, a.as_of)
    with open(a.report, "w", encoding="utf-8") as f:
        f.write(text)
    print("Wrote %s: %d documents, %d authors (%d in the author table)"
          % (a.report, len(docs), len(author_people(docs)), len(author_rows(docs))))


if __name__ == "__main__":
    main()
