"""Pull named authors and editors from a TM Forum document's Acknowledgements.

Layouts seen in published deliverables:
  "Name, Title, Company - Lead Author"             one line
  "Name, Company, Editor and ... co-leader"        one line, role in a later part
  Name / Company / Role                            table rows, one cell per line
  "Authors" or "Guide Editors and Authors" heading, then "Name, Title, Company"
  lines or Member / Title / Company rows, until a contributors heading
Authors are those whose role names an author, or an editor who isn't TM Forum's
reviewing editor ("Reviewer, Editor"). Contributors and reviewers aren't authors.
The file's own metadata isn't used: it names TM Forum publishing staff.

Usage: python -I authors.py <output-dir>
Reads <output-dir>/text.txt (from extract_docx.py), writes authors.json there
({"authors": [...], "all": [...]}, each {"name", "company", "role"}) and prints
the authors.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import json
import os
import re
import sys

ROLE_WORD = re.compile(r"\b(?:author|co-author|editor|contributor|reviewer|chair|co-chair|lead|co-lead|leader)\b", re.I)
AUTHORISH = re.compile(r"author|editor", re.I)
START = re.compile(r"^(?:\d+(?:\.\d+)*\.?\s*)?Acknowledge?ments?\b", re.I)
STOP = re.compile(r"^(?:\d+(?:\.\d+)*\.?\s*)?(?:Glossary|Terminology|Appendix|Annex|Document History|References|"
                  r"Release History|Terms and Abbreviations|Notice|Administrative Appendix)\b", re.I)
HEADER = re.compile(r"^(?:team member|company|role\*?|name|member|title|organi[sz]ation|"
                    r"team member \(@mention\)|•|-)$", re.I)
AUTHOR_HEAD = re.compile(r"^(?:\d+(?:\.\d+)*\.?\s*)?(?:guide |main |lead )?(?:authors?|editors?)"
                         r"(?: and (?:authors?|editors?))?$", re.I)
OTHER_HEAD = re.compile(r"^(?:\d+(?:\.\d+)*\.?\s*)?(?:main |additional |other |key )?(?:contributors?|reviewers?|"
                        r"additional inputs?)\b.{0,30}$", re.I)


def clean(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ").replace("(@mention)", "").replace("@", "")).strip(" ,;•")


def is_role(s):
    return bool(ROLE_WORD.search(s)) and len(s.split()) <= 8


def parse(lines):
    starts = [i for i, l in enumerate(lines) if START.match(l.strip()) and len(l.split()) < 6
              and not re.search(r"\d+$", l.strip())]  # not a contents line ("9.Acknowledgements58")
    if not starts:
        return []
    block = []
    for l in lines[starts[-1] + 1:starts[-1] + 300]:
        if STOP.match(l.strip()) and len(l.split()) < 8:
            break
        block.append(clean(l))
    kept, preamble = [], False
    for b in block:
        # "This document was prepared by ... project team." can wrap over lines (PDFs).
        if re.match(r"^this (?:document|whitepaper|guide|report) (?:was|is|has been) (?:prepared|written)", b, re.I):
            preamble = True
        if preamble and HEADER.match(b):  # the table header ends a preamble with no full stop
            preamble = False
        if preamble:
            preamble = not re.search(r"[.:]$", b)
            continue
        if b and not HEADER.match(b) and not re.match(r"^\d+(?:\.\d+)+\.?\s+(?!.*(?:author|editor))", b, re.I):
            kept.append(b)
    block = kept
    people, section, i = [], None, 0
    while i < len(block):
        b = block[i]
        if AUTHOR_HEAD.match(b):
            section, i = "Author", i + 1
            continue
        if OTHER_HEAD.match(b):
            section, i = "Contributor", i + 1
            continue
        m = re.match(r"^(.+?)\s+[-–]\s+(.*\b(?:author|editor)\b.*)$", b, re.I)
        if m:  # "Name, Title, Company - Role"
            parts = [p.strip() for p in m.group(1).split(",")]
            people.append({"name": parts[0], "company": parts[-1] if len(parts) > 1 else "", "role": m.group(2)})
            i += 1
            continue
        parts = [p.strip() for p in b.split(",")]
        if len(parts) >= 3 and AUTHORISH.search(", ".join(parts[2:])) and len(parts[0].split()) <= 5:
            # "Name, Company, Editor and ... co-leader"
            people.append({"name": parts[0], "company": parts[1], "role": ", ".join(parts[2:])})
            i += 1
            continue
        if i + 2 < len(block) and is_role(block[i + 2]) and not is_role(b) and not is_role(block[i + 1]) \
                and len(b.split()) <= 5 and "," not in b:
            people.append({"name": b, "company": block[i + 1], "role": block[i + 2].rstrip("*")})
            i += 3
            continue
        if i + 3 < len(block) and is_role(block[i + 3]) and not is_role(b) and not is_role(block[i + 2]) \
                and len(b.split()) <= 5 and "," not in b:
            # Team Member / Title / Company / Role rows
            people.append({"name": b, "company": block[i + 2], "role": block[i + 3].rstrip("*")})
            i += 4
            continue
        if section == "Author" and "," not in b and i + 2 < len(block) and len(b.split()) <= 5 \
                and not AUTHOR_HEAD.match(block[i + 1]) and not OTHER_HEAD.match(block[i + 1]):
            # Member / Title / Company rows under an authors heading
            people.append({"name": b, "company": block[i + 2], "role": "Author"})
            i += 3
            continue
        if section and len(parts) >= 2 and len(b.split()) <= 16 and len(parts[0].split()) <= 5:
            people.append({"name": parts[0], "company": parts[-1], "role": section})
        elif len(parts) == 2 and len(parts[0].split()) <= 5 and len(b.split()) <= 10:
            people.append({"name": parts[0], "company": parts[1], "role": "Member"})
        i += 1
    return people


# Spellings of one person or company seen across documents.
ALIAS = {"dave millham": "Dave Milham", "david milham": "Dave Milham"}
COMPANY = {"cmcc": "China Mobile", "telefonica": "Telefónica"}


def normalise(p):
    """Strip "(TM Forum)" or e-mail suffixes, fix all-caps or all-lower names, and merge known aliases."""
    name = re.sub(r"\s*\([^)]*\)", "", p["name"]).strip()
    if name.isupper() or name.islower() or re.search(r"\b[A-Z]{2,}\b", name):
        name = " ".join(w if len(w) <= 1 else w[0].upper() + w[1:].lower() for w in name.split())
    return {"name": ALIAS.get(name.lower(), name), "company": COMPANY.get(p["company"].lower(), p["company"]),
            "role": p["role"]}


def people_in(text):
    """Every named team member, once each, normalised."""
    seen, out = set(), []
    for p in map(normalise, parse(text.splitlines())):
        if "select from" in p["name"].lower() or p["name"].lower() in seen:  # template guidance, repeats
            continue
        seen.add(p["name"].lower())
        out.append(p)
    return out


def authors_of(people):
    """A role naming an author, or an editor who isn't TM Forum's reviewing editor ("Reviewer, Editor")."""
    return [p for p in people if re.search(r"author", p["role"], re.I)
            or (re.search(r"editor", p["role"], re.I) and not re.search(r"reviewer", p["role"], re.I))]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python -I authors.py <output-dir>   (the folder extract_docx.py wrote)")
    sys.stdout.reconfigure(encoding="utf-8")
    with open(os.path.join(sys.argv[1], "text.txt"), encoding="utf-8") as f:
        people = people_in(f.read())
    result = {"authors": authors_of(people), "all": people}
    with open(os.path.join(sys.argv[1], "authors.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Authors and editors: " + ("; ".join("%s (%s, %s)" % (p["name"], p["company"], p["role"])
                                               for p in result["authors"]) or "none named"))
    print("Team members named: %d" % len(people))
