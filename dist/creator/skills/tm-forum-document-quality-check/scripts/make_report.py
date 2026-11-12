"""Turn a run's Markdown report into a Word (.docx) report.

The skill writes each run's report as Markdown (the same text it shows in
chat) and this script renders it. It handles what the reports use:
# / ## / ### headings, "> " blockquotes (the disclaimer), "- " bullets
(nested by two-space indents), "1. " numbered items, pipe tables, "---"
rules, and inline **bold**, *italic*, `code` and [text](url) links.
Score cells are shaded by their class word (see CLASS_FILLS): red, amber
or green, or shades of grey for dependence, darker for heavy.

Usage: python -I make_report.py <report.md> <report.docx> [--title "..."]
Pages are always A4 portrait. A TM Forum-branded HTML copy is written beside
the .docx with the same name (make_html_report.py).
Needs python-docx.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import os
import re
import sys

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`|\[[^\]]+\]\([^)\s]+\))")
TABLE_SEP = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
BULLET = re.compile(r"^(\s*)[-*] (.*)$")
NUMBERED = re.compile(r"^(\s*)(\d+)\. (.*)$")
LINK_BLUE = RGBColor(0x05, 0x63, 0xC1)

RED, AMBER, GREEN = "FFC7CE", "FFEB9C", "C6EFCE"
# Column header (lower case, matched as a substring) -> class word -> cell fill. A cell is
# shaded by the first class word it contains; one without a class word ("none found") stays plain.
# Dependence is shaded grey, not red/amber/green: depending on another body's work isn't wrong in itself.
DEPENDENCE = {"heavy": "A6A6A6", "typical": "D9D9D9", "light": "F2F2F2"}
CLASS_FILLS = [
    ("ownership", {"bad": RED, "improving": AMBER, "good": GREEN}),
    ("automation", {"high": RED, "medium": AMBER, "low": GREEN}),
    ("pointers", DEPENDENCE),
    ("copied", DEPENDENCE),
    ("editorial", {"very inconsistent": RED, "inconsistent": RED, "improving": AMBER, "consistent": GREEN}),
    ("oda content", {"heavy": GREEN, "typical": AMBER, "light": RED}),
    ("overall", {"high": RED, "typical": AMBER, "low": GREEN}),
    ("project class", {"high": RED, "medium": AMBER, "low": GREEN, "too few to class": "F2F2F2"}),
]


# Project table (project_report.py): measure cells read "N of M" flagged documents and are shaded by the
# flagged share, with the project class lines; the project score is shaded by its class.
PROJECT_LINES = (0.10, 0.30)
COUNT_CELL = re.compile(r"^(\d+) of (\d+)$")


def project_fill(h, text):
    m = COUNT_CELL.match(text.strip())
    if m and h.endswith(")") and "(" in h and int(m.group(2)):
        share = int(m.group(1)) / int(m.group(2))
        tones = (DEPENDENCE["light"], DEPENDENCE["typical"], DEPENDENCE["heavy"]) \
            if ("pointers" in h or "copied" in h) else (GREEN, AMBER, RED)
        return tones[0] if share == 0 else tones[1] if share <= PROJECT_LINES[1] else tones[2]
    if h == "project score" and re.fullmatch(r"\d+\.\d+", text.strip()):
        v = float(text)
        return GREEN if v <= PROJECT_LINES[0] else AMBER if v <= PROJECT_LINES[1] else RED
    return None


def class_fill(header, text):
    h = re.sub(r"[*`]", "", header).lower().strip()
    fill = project_fill(h, text)
    if fill:
        return fill
    fills = next((f for key, f in CLASS_FILLS if key in h), None)
    if not fills:
        return None
    # Longest words first so "very inconsistent" wins over "inconsistent" at the same place.
    words = sorted(fills, key=len, reverse=True)
    m = re.search(r"\b(%s)\b" % "|".join(re.escape(w) for w in words), text.lower())
    return fills[m.group(1)] if m else None


def add_hyperlink(paragraph, text, url, size=None, bold=False, italic=False):
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
                          is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    colour = OxmlElement("w:color")
    colour.set(qn("w:val"), "0563C1")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    if bold:
        props.append(OxmlElement("w:b"))
    if italic:
        props.append(OxmlElement("w:i"))
    props.append(colour)
    if size:
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), str(int(size.pt * 2)))
        props.append(sz)
    props.append(underline)
    run.append(props)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def add_inline(paragraph, text, size=None, bold=False, italic=False):
    """Add text with **bold**, *italic*, `code` and [links](url) to a paragraph.

    Bold and italic spans are processed recursively, so code and links
    inside them render properly.
    """
    def run_of(t, code=False):
        r = paragraph.add_run(t)
        r.bold = bold or None
        r.italic = italic or None
        if code:
            r.font.name = "Consolas"
        if size:
            r.font.size = size
        return r

    for piece in INLINE.split(text):
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**") and len(piece) > 4:
            add_inline(paragraph, piece[2:-2], size, True, italic)
        elif piece.startswith("`") and piece.endswith("`"):
            run_of(piece[1:-1], code=True)
        elif piece.startswith("[") and "](" in piece:
            label, url = piece[1:-1].split("](", 1)
            add_hyperlink(paragraph, label, url, size, bold, italic)
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            add_inline(paragraph, piece[1:-1], size, bold, True)
        else:
            # Bare URLs become links too.
            for part in re.split(r"(https?://[^\s)|`]+)", piece):
                if re.match(r"https?://", part):
                    url = part.rstrip(".,;")
                    add_hyperlink(paragraph, url, url, size, bold, italic)
                    if len(url) < len(part):
                        run_of(part[len(url):])
                elif part:
                    run_of(part)


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def add_table(doc, rows):
    header, body = rows[0], rows[1:]
    table = doc.add_table(rows=1 + len(body), cols=len(header))
    table.style = "Table Grid"
    for r, row in enumerate([header] + body):
        for c in range(len(header)):
            cell = table.cell(r, c)
            cell.text = ""
            p = cell.paragraphs[0]
            add_inline(p, row[c] if c < len(row) else "", size=Pt(8.5), bold=(r == 0))
            if r == 0:
                shade(cell, "D9E2F3")
                p.paragraph_format.keep_with_next = True
            elif c < len(row):
                fill = class_fill(header[c], row[c])
                if fill:
                    shade(cell, fill)
        tr_pr = table.rows[r]._tr.get_or_add_trPr()
        tr_pr.append(OxmlElement("w:cantSplit"))
        if r == 0:
            tr_pr.append(OxmlElement("w:tblHeader"))
    doc.add_paragraph()


def add_quote(doc, lines):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.right_indent = Cm(0.5)
    p_pr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "FFF2CC")
    p_pr.append(shd)
    borders = OxmlElement("w:pBdr")
    for side in ("top", "left", "bottom", "right"):
        b = OxmlElement("w:%s" % side)
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "6")
        b.set(qn("w:space"), "4")
        b.set(qn("w:color"), "BF9000")
        borders.append(b)
    p_pr.append(borders)
    add_inline(p, " ".join(l.strip() for l in lines))


def render(md, out, title):
    doc = Document()
    section = doc.sections[0]
    # Every report is A4 portrait.
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width, section.page_height = Cm(21.0), Cm(29.7)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(section, side, Cm(1.8))
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(10)
    if title:
        doc.core_properties.title = title
        t = doc.add_paragraph()
        t.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = t.add_run(title)
        run.bold = True
        run.font.size = Pt(18)

    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            add_quote(doc, quote)
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1].strip()):
            rows = [split_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            add_table(doc, rows)
            continue
        heading = re.match(r"^(#{1,4}) (.*)$", stripped)
        if heading:
            doc.add_heading(re.sub(r"[*`]", "", heading.group(2)), level=min(len(heading.group(1)), 3))
            i += 1
            continue
        if re.match(r"^-{3,}$", stripped):
            doc.add_paragraph("_" * 40).alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1
            continue
        m = BULLET.match(line) or NUMBERED.match(line)
        if m:
            level = min(len(m.group(1).replace("\t", "  ")) // 2, 2)
            numbered = not BULLET.match(line)
            text = m.group(3) if numbered else m.group(2)
            i += 1
            # Continuation lines indented under the item.
            while i < len(lines) and lines[i].strip() and lines[i].startswith(" " * (len(m.group(1)) + 2)) \
                    and not BULLET.match(lines[i]) and not NUMBERED.match(lines[i]) \
                    and not lines[i].strip().startswith("|"):
                text += " " + lines[i].strip()
                i += 1
            if numbered:
                # Word's "List Number" style keeps counting across separate
                # lists, so write the Markdown's own number with a hanging indent.
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.75 * (level + 1))
                p.paragraph_format.first_line_indent = Cm(-0.75)
                p.add_run("%s.\t" % m.group(2))
                add_inline(p, text)
            else:
                style = "List Bullet" + (" %d" % (level + 1) if level else "")
                add_inline(doc.add_paragraph(style=style), text)
            continue
        para = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\||-{3,}$)", lines[i].strip()) \
                and not BULLET.match(lines[i]) and not NUMBERED.match(lines[i]):
            para.append(lines[i].strip())
            i += 1
        add_inline(doc.add_paragraph(), " ".join(para))
    doc.save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown")
    ap.add_argument("docx")
    ap.add_argument("--title")
    ap.add_argument("--portrait", action="store_true", help="accepted for compatibility; reports are always A4 portrait")
    a = ap.parse_args()
    with open(a.markdown, encoding="utf-8") as f:
        md = f.read()
    render(md, a.docx, a.title)
    print("Wrote %s" % a.docx)
    # Every report also gets a TM Forum-branded HTML copy beside it (see make_html_report.py).
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
    from make_html_report import render_html
    html_out = re.sub(r"\.docx$", "", a.docx, flags=re.I) + ".html"
    render_html(md, html_out, a.title)
    print("Wrote %s" % html_out)


if __name__ == "__main__":
    sys.exit(main())
