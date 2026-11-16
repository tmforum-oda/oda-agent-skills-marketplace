"""Extract everything an IP and licence check needs from a .xlsx workbook.

The spreadsheet counterpart of extract_docx.py: it writes the same files, so
every later step of the check runs unchanged. Reads the raw workbook XML.

Usage: python -I extract_xlsx.py <input.xlsx> <output-dir>

Writes to <output-dir>:
  text.txt        the text of every cell that holds text, including IDs and
                  values typed as text ("1.1.1", "75-80%"), sheet by sheet in
                  workbook order, row by row; each sheet starts with a
                  "Sheet: <name>" line. Cells stored as numbers are left out,
                  so they don't count as words
  cells.txt       every cell as "<sheet>!<cell>: <text>", for giving
                  locations in the report (a workbook has no headings); cells
                  stored as numbers are listed too, marked "(number)", with
                  Excel's raw value (a date shows as its serial number)
  headers.txt     page header and footer text of each sheet
  notes.txt       cell comments and notes
  hyperlinks.txt  external link targets (one per line, duplicates removed)
  images.txt      each picture, with its sheet, the cell it is anchored at
                  and the two text cells before and after it
  cited.txt       text credited to an outside source, found with the same
                  patterns as extract_docx.py: a cell holding or linking to a
                  non-TM Forum address, "(Source: ...)", a trailing
                  "Source: ..." or a numeric citation marker like [29]. A short
                  source cell credits the text cell before it. A column headed
                  "Source" ("Source of the standard", "Standard source")
                  credits its row: the text after the source in the same
                  cell, or else the row's longest text cell.
                  Format: "<source> | <text>"
  media/          embedded pictures
  source_format.txt  "xlsx", so the reports say the scores aren't comparable
                  with the Word documents
Standard library only.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import os
import posixpath
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
from extract_docx import (CITE_MARK, OWN_HOST, OWN_WORDS, REF_ENTRY, SOURCE_NOTE,  # noqa: E402
                          SOURCE_TRAIL, URL, unescape)

NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
SI = re.compile(r"<si>(.*?)</si>", re.S)
T = re.compile(r"<t(?: [^>]*)?>([^<]*)</t>")
CELL = re.compile(r'<c ([^>]*?)(?:/>|>(.*?)</c>)', re.S)
ATTR = re.compile(r'(\w+(?::\w+)?)="([^"]*)"')
V = re.compile(r"<v>([^<]*)</v>")
SHEET = re.compile(r"<sheet ([^>]*?)/>")
REL = re.compile(r"<Relationship ([^>]*?)/>")
HYPERLINK = re.compile(r"<hyperlink ([^>]*?)/>")
HF = re.compile(r"<(odd|even|first)(Header|Footer)>([^<]*)</\1\2>")
HF_CODE = re.compile(r"&(?:\"[^\"]*\"|[LCRPNDTFAZGBIUSEXY]|\d+|K[0-9A-F]{6})")
COMMENT = re.compile(r'<comment ([^>]*?)>(.*?)</comment>', re.S)
ANCHOR = re.compile(r"<xdr:(?:twoCellAnchor|oneCellAnchor|absoluteAnchor)\b.*?</xdr:(?:twoCellAnchor|oneCellAnchor|absoluteAnchor)>", re.S)
FROM = re.compile(r"<xdr:from>\s*<xdr:col>(\d+)</xdr:col>.*?<xdr:row>(\d+)</xdr:row>", re.S)
EMBED = re.compile(r'r:embed="([^"]+)"')
XESC = re.compile(r"_x([0-9A-Fa-f]{4})_")  # Excel's escape for control characters: "_x000D_" is a carriage return
CONTEXT = 2  # text cells recorded either side of a picture
SOURCE_COLUMN = re.compile(r"\bsources?\b", re.I)  # a column header naming the source of each row
SOURCE_HEADER_ROWS = 3  # header rows searched for such a column
SOURCE_LINE_WORDS = 8  # a cell's first line this short, naming a body or a number, is its source
SOURCE_NAME = re.compile(r"\d|\b(?:3GPP|ETSI|IETF|ITU|IEEE|ISO|IEC|MEF|NIST|ONF|TM ?Forum|RFC|GSMA|O-RAN|W3C)\b", re.I)


def attrs(s):
    return dict(ATTR.findall(s))


def col_index(ref):
    """'C12' -> (12, 3): row, then column, both counted from 1."""
    m = re.match(r"([A-Z]+)(\d+)", ref)
    col = 0
    for ch in m.group(1):
        col = col * 26 + ord(ch) - 64
    return int(m.group(2)), col


def col_name(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def rels_of(z, part):
    """{rId: (target part, external?)} for a part's .rels file."""
    folder, name = posixpath.split(part)
    path = posixpath.join(folder, "_rels", name + ".rels")
    out = {}
    if path in z.namelist():
        for a in map(attrs, REL.findall(z.read(path).decode("utf-8"))):
            external = a.get("TargetMode") == "External"
            target = unescape(a["Target"]) if external else posixpath.normpath(posixpath.join(folder, a["Target"]))
            out[a["Id"]] = (target, external, a.get("Type", ""))
    return out


def xunescape(s):
    return XESC.sub(lambda m: " " if int(m.group(1), 16) < 32 else chr(int(m.group(1), 16)), unescape(s))


def cell_text(body, a, shared):
    kind = a.get("t")
    if kind == "s":
        v = V.search(body or "")
        return shared[int(v.group(1))] if v else ""
    if kind == "inlineStr":
        return xunescape("".join(T.findall(body or "")))
    if kind in ("str", "e"):
        v = V.search(body or "")
        return xunescape(v.group(1)) if v else ""
    return ""  # numbers, dates and booleans hold no text


def main(src, dst):
    os.makedirs(os.path.join(dst, "media"), exist_ok=True)
    z = zipfile.ZipFile(src)
    names = [n for n in z.namelist() if not n.endswith("/")]

    def read(name):
        return z.read(name).decode("utf-8")

    def write(fname, lines):
        with open(os.path.join(dst, fname), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    shared = []
    if "xl/sharedStrings.xml" in names:
        shared = [xunescape("".join(T.findall(si))) for si in SI.findall(read("xl/sharedStrings.xml"))]
    book_rels = rels_of(z, "xl/workbook.xml")

    text, cells, hf, notes, links, images, cited, seen = [], [], [], [], [], [], [], set()
    media_count = 0
    for sh in map(attrs, SHEET.findall(read("xl/workbook.xml"))):
        sheet_name = unescape(sh["name"])
        part = book_rels[sh["r:id"]][0]
        xml = read(part)
        rels = rels_of(z, part)
        link_at = {}
        for h in map(attrs, HYPERLINK.findall(xml)):
            rid = h.get("r:id")
            if rid in rels and rels[rid][1]:
                target = rels[rid][0]
                link_at[h["ref"].split(":")[0]] = target
                if target not in links:
                    links.append(target)
        rows = []  # (row, col, ref, text) for every text cell, in row-major order
        values = []  # (row, col, ref, value) for cells holding a number, date or boolean
        for a_s, body in CELL.findall(xml):
            a = attrs(a_s)
            r, c = col_index(a["r"])
            t = cell_text(body, a, shared).strip()
            if t:
                rows.append((r, c, a["r"], t))
            elif a.get("t", "n") in ("n", "b", "d") and V.search(body or ""):
                values.append((r, c, a["r"], V.search(body).group(1)))
        rows.sort()
        text.append("Sheet: %s" % sheet_name)
        text += [t for _, _, _, t in rows]
        # Numbers go to cells.txt only, so the reader sees weights and targets without them counting as words.
        cells += ["%s!%s: %s" % (sheet_name, ref, t) if kind == "t" else "%s!%s: %s (number)" % (sheet_name, ref, t)
                  for _, _, ref, t, kind in sorted([x + ("t",) for x in rows] + [x + ("n",) for x in values])]

        for kind, which, value in HF.findall(xml):
            value = re.sub(r"\s+", " ", HF_CODE.sub(" ", xunescape(value))).strip()
            if value:
                hf.append("[%s %s %s] %s" % (sheet_name, kind, which.lower(), value))

        # A short source cell (a bare link, "Source: ...") credits the text cell before it.
        for i, (_, _, ref, t) in enumerate(rows):
            sources = [u for u in URL.findall(t) + ([link_at[ref]] if ref in link_at else [])
                       if u.startswith("http") and not OWN_HOST.match(u)]
            sources += ["Source: " + s for s in SOURCE_NOTE.findall(t)]
            trail = SOURCE_TRAIL.search(t)
            if trail:
                sources.append("Source: " + trail.group(1))
            if CITE_MARK.search(t):
                sources.append("citation marker " + CITE_MARK.search(t).group())
            if not sources:
                continue
            own = URL.sub("", SOURCE_NOTE.sub("", t[:trail.start()] if trail else t)).split()
            if len(own) >= OWN_WORDS or REF_ENTRY.match(t):
                candidate = t
            elif i:
                candidate = rows[i - 1][3]
            else:
                continue
            candidate = " ".join(candidate.split())  # cited.txt holds one passage per line
            if len(candidate.split()) >= OWN_WORDS and candidate not in seen:
                seen.add(candidate)
                cited.append("%s | %s" % (sources[0], candidate))

        # A column headed "Source", "Source of the standard", "Standard source" ... credits its row.
        # A cell in it often opens with the source ("3GPP TS 28.100 7.1.1") and goes on with text taken
        # from it, which is the passage; a cell with only the source credits the row's longest text cell.
        # A long cell there that opens with no source is credited to "no source named".
        for hr, hc, _, head in rows:
            head = head.strip().splitlines()[0].strip()  # "Standard source\n(3GPP/ETSI standards are ...)"
            if hr > SOURCE_HEADER_ROWS or not SOURCE_COLUMN.search(head) or len(head.split()) > 6:
                continue
            for r, c, ref, t in rows:
                if c != hc or r <= hr:
                    continue
                lines = [l.strip().strip('"“”') for l in t.splitlines() if l.strip().strip('"“”')]
                first, rest = lines[0], " ".join(lines[1:])
                if len(first.split()) <= SOURCE_LINE_WORDS and SOURCE_NAME.search(first):
                    source = "Source: " + first
                    passage = rest
                    if len(passage.split()) < OWN_WORDS:
                        passage = max((x for rr, cc, _, x in rows if rr == r and cc != c), key=lambda x: len(x.split()),
                                      default="")
                else:
                    source, passage = 'Source column "%s": no source named' % head, t
                passage = " ".join(passage.split())
                if len(passage.split()) >= OWN_WORDS and passage not in seen:
                    seen.add(passage)
                    cited.append("%s | %s" % (source, passage))

        for rid, (target, external, kind) in rels.items():
            if kind.endswith("/comments") and target in names:
                for c_a, c_body in COMMENT.findall(read(target)):
                    note = re.sub(r"\s+", " ", xunescape("".join(T.findall(c_body)))).strip()
                    if note:
                        notes.append("[%s!%s] %s" % (sheet_name, attrs(c_a).get("ref", "?"), note))
            if kind.endswith("/drawing") and target in names:
                d_xml, d_rels = read(target), rels_of(z, target)
                for anchor in ANCHOR.findall(d_xml):
                    at = FROM.search(anchor)
                    r, c = (int(at.group(2)) + 1, int(at.group(1)) + 1) if at else (1, 1)
                    for e in EMBED.findall(anchor):
                        media = d_rels.get(e, ("",))[0]
                        if not media.startswith("xl/media/"):
                            continue
                        before = [t for rr, cc, _, t in rows if (rr, cc) < (r, c)][-CONTEXT:]
                        after = [t for rr, cc, _, t in rows if (rr, cc) >= (r, c)][:CONTEXT]
                        images.append("== %s" % posixpath.basename(media))
                        images.append("  sheet: %s, anchored at %s%d" % (sheet_name, col_name(c), r))
                        images += ["  before: %s" % t[:300] for t in before]
                        images += ["  after: %s" % t[:300] for t in after]

    for n in (x for x in names if x.startswith("xl/media/")):
        with open(os.path.join(dst, "media", posixpath.basename(n)), "wb") as f:
            f.write(z.read(n))
        media_count += 1

    write("text.txt", text)
    write("cells.txt", cells)
    write("headers.txt", hf)
    write("notes.txt", notes)
    write("hyperlinks.txt", links)
    write("images.txt", images)
    write("cited.txt", cited)
    write("source_format.txt", ["xlsx"])
    print("text: %d cells (incl. numbers) on %d sheets, headers/footers: %d, notes: %d, hyperlinks: %d, media: %d"
          % (len(cells), sum(1 for t in text if t.startswith("Sheet: ")), len(hf), len(notes), len(links),
             media_count))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
