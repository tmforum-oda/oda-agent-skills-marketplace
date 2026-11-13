"""Extract everything an IP and licence check needs from a .docx file.

Reads the raw document XML rather than using python-docx, which skips text
held inside Word content controls (as in TM Forum IG templates).

Usage: python -I extract_docx.py <input.docx> <output-dir>

Writes to <output-dir>:
  text.txt        body paragraphs, including content controls and tables
  headers.txt     header and footer text
  notes.txt       footnote and endnote text
  hyperlinks.txt  external link targets (one per line, duplicates removed)
  images.txt      each image in the body, in document order, with the two
                  paragraphs before and after it (captions, "Source:" notes)
  cited.txt       text credited to an outside source: a paragraph holding a
                  non-TM Forum link, "(Source: ...)", a trailing unbracketed
                  "Source: ..." or a numeric citation marker like [29]. When a
                  paragraph is only a link or source line, the paragraph
                  before it is credited; a source line also credits the
                  paragraphs after it, up to the next heading. A heading or
                  table title naming a source ("... Source TR315") credits
                  the section under it, joining descriptions wrapped over
                  several lines. Format: "<source> | <text>"
  media/          embedded images, for checking logos and diagrams
Standard library only.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import os
import re
import sys
import zipfile

PARA = re.compile(r"<w:p[ >].*?</w:p>", re.S)
TEXT = re.compile(r"<w:t(?: [^>]*)?>([^<]*)</w:t>")
LINK = re.compile(r'Target="([^"]+)"[^>]*TargetMode="External"|TargetMode="External"[^>]*Target="([^"]+)"')
ENTITIES = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&apos;": "'"}
EMBED = re.compile(r'r:embed="([^"]+)"')
REL = re.compile(r'<Relationship [^>]*?Id="([^"]+)"[^>]*?Target="([^"]+)"')
CONTEXT = 2  # paragraphs of text recorded either side of an image
HLINK = re.compile(r'<w:hyperlink [^>]*?r:id="([^"]+)"')
SOURCE_NOTE = re.compile(r"\(Source:\s*([^)]*)\)", re.I)
# "Source: X" appended to the end of a paragraph, with no brackets, possibly
# with no space after the full stop: "...utilization.Source: Int handler 1/4/2024"
# Case-sensitive "Source:" with no word-boundary test, so a stray character
# before it ("support.VSource: ...") still matches but "resource:" doesn't.
SOURCE_TRAIL = re.compile(r"Source:\s*([^()]{2,120}?)\s*$")
# A source named in a heading or table title that covers what follows:
# "...Component Feature Source TR315", "...source TR311 BP01 thru BP04".
# Needs an identifier with a digit, so ordinary words after "source" don't match.
SOURCE_HEADING = re.compile(r"\bsource:?\s+((?=\S*\d)[A-Za-z0-9][\w.-]*(?:\s+\S+){0,5})\s*$", re.I)
SECTION_MAX = 120  # most lines scanned under a heading's source
SECTION_STOP_WORDS = 7  # a section title this long ends a heading's section
HLINK_FULL = re.compile(r'<w:hyperlink [^>]*?r:id="([^"]+)"[^>]*?(?:/>|>(.*?)</w:hyperlink>)', re.S)
REF_ENTRY = re.compile(r"^\[\s*\d+\s*\]")  # a numbered reference-list entry: "[5] Title ..."
LABEL_WORDS = 4  # in a section, a shorter line is a cell label (ID, name), not text
# Template placeholders: "<insert ...>", or "insert ..." once the brackets are lost.
PLACEHOLDER = re.compile(r"^(<[^>]*>|insert\b.*)$", re.I)
# Words a wrapped line can end on mid-sentence; such a line isn't a title.
CONTINUES = re.compile(r"\b(the|a|an|and|or|of|to|in|for|with|that|on|by|as|at|from|is|are)$", re.I)


def section_title(t):
    """A line that starts a new section: long enough, starts with a capital,
    and doesn't look like a description wrapped mid-sentence."""
    return (len(t.split()) >= SECTION_STOP_WORDS and t[:1].isupper()
            and looks_like_heading(t, 20) and not t.endswith(",") and not CONTINUES.search(t))
CITE_MARK = re.compile(r"\[\d+(?:\s*[,–-]\s*\d+)*\]")
URL = re.compile(r"https?://\S+")
OWN_HOST = re.compile(r"^https?://([^/]*\.)?tmforum\.org", re.I)
OWN_WORDS = 10  # a paragraph with fewer words than this is just a source line
FOLLOW_MAX = 12  # most paragraphs credited after a "(Source: ...)" line
HEADING_WORDS = 12  # a shorter line without closing punctuation ends the block


def unescape(s):
    for k, v in ENTITIES.items():
        s = s.replace(k, v)
    return s


def paragraphs(xml):
    out = []
    for p in PARA.findall(xml):
        t = unescape("".join(TEXT.findall(p)))
        if t.strip():
            out.append(t)
    return out


def image_context(doc, rels):
    """List each body image with the text around it, in document order."""
    targets = dict(REL.findall(rels))
    paras = PARA.findall(doc)
    texts = [unescape("".join(TEXT.findall(p))).strip() for p in paras]
    out = []
    for i, p in enumerate(paras):
        for rid in EMBED.findall(p):
            target = targets.get(rid, "")
            if not target.startswith("media/"):
                continue
            before = [t for t in texts[:i] if t][-CONTEXT:]
            after = [t for t in texts[i + 1:] if t][:CONTEXT]
            out.append("== %s" % os.path.basename(target))
            out += ["  before: %s" % t[:300] for t in before]
            if texts[i]:
                out.append("  same paragraph: %s" % texts[i][:300])
            out += ["  after: %s" % t[:300] for t in after]
    return out


def hyperlink_targets(p, targets):
    """External link targets in a paragraph, leaving out links that wrap only a bare marker
    ("[5]") or a blank. Stale links pile up on reference-list markers in some documents,
    each carrying the target of an entry above it; they would otherwise be read as the
    source of the entry."""
    out = []
    for rid, inner in HLINK_FULL.findall(p):
        shown = unescape("".join(TEXT.findall(inner or ""))).replace(" ", " ")
        if re.fullmatch(r"\s*(\[\s*\d+\s*\])?\s*", shown):
            continue
        out.append(targets.get(rid, ""))
    return out


def cited_text(doc, rels):
    """Return "<source> | <text>" lines for text credited to an outside source."""
    targets = dict(REL.findall(rels))
    paras = PARA.findall(doc)
    texts = [unescape("".join(TEXT.findall(p))).strip() for p in paras]
    out, seen = [], set()

    def own_link(i):
        """Whether paragraph i holds a non-TM Forum link of its own."""
        links = hyperlink_targets(paras[i], targets) + URL.findall(texts[i])
        return any(u.startswith("http") and not OWN_HOST.match(unescape(u)) for u in links)
    for i, p in enumerate(paras):
        links = hyperlink_targets(p, targets)
        links += URL.findall(texts[i])
        sources = [unescape(u) for u in links if u.startswith("http") and not OWN_HOST.match(u)]
        sources += ["Source: " + s for s in SOURCE_NOTE.findall(texts[i])]
        trail = SOURCE_TRAIL.search(texts[i])
        if trail:
            sources.append("Source: " + trail.group(1))
        heading = SOURCE_HEADING.search(texts[i]) if looks_like_heading(texts[i], 20) else None
        if heading:
            sources.append("Source: " + heading.group(1))
        if CITE_MARK.search(texts[i]):
            sources.append("citation marker " + CITE_MARK.search(texts[i]).group())
        if not sources:
            continue
        stripped = SOURCE_NOTE.sub("", texts[i])
        if trail:
            stripped = stripped[:trail.start()]
        own = URL.sub("", stripped).split()
        if heading:
            # A heading's source covers the section under it (often table rows).
            candidates = section_block(texts, i)
        elif REF_ENTRY.match(texts[i]):
            # A numbered reference-list entry ("[5] Title - https://...") is credited
            # with its own link, not the link of the entry that follows it.
            candidates = [texts[i]]
        elif len(own) >= OWN_WORDS:
            candidates = [stripped.strip() if trail else texts[i]]
        else:
            # A bare link or source line credits the paragraph before it, unless
            # that is a reference-list entry that carries its own link.
            prev_i = [k for k in range(i) if texts[k]]
            candidates = []
            if prev_i and not (REF_ENTRY.match(texts[prev_i[-1]]) and own_link(prev_i[-1])):
                candidates = [texts[prev_i[-1]]]
            # A "(Source: ...)" line can also introduce the block that follows
            # it (e.g. a field insight credited to a named person), so the
            # paragraphs after it are credited too, up to the next heading.
            if SOURCE_NOTE.search(texts[i]) or trail:
                candidates += following_block(texts, i)
        for text in candidates:
            # Skip text that only explains the link itself ("https://... – the root URL").
            explains_link = any(text.lstrip("\"'“ ").startswith(s) for s in sources)
            if len(text.split()) >= OWN_WORDS and text not in seen and not explains_link:
                seen.add(text)
                out.append("%s | %s" % (sources[0], text))
    return out


def following_block(texts, i):
    """Paragraphs after a source line, up to the next heading-like line."""
    block = []
    for t in texts[i + 1:]:
        if not t:
            continue
        if len(block) >= FOLLOW_MAX or looks_like_heading(t) or SOURCE_NOTE.search(t) or SOURCE_TRAIL.search(t):
            break
        block.append(t)
    return block


def section_block(texts, i):
    """Paragraphs under a heading that names a source, e.g. the rows of a
    table titled "... Source TR315". Short cells (IDs, names) are skipped
    rather than ending the section; it ends at the next section title
    (see section_title), at another source, or after SECTION_MAX lines.

    Descriptions wrapped over several short lines are joined: consecutive
    lines of LABEL_WORDS or more words form one passage, and a shorter
    line (an ID or a name cell) closes it."""
    block, current, seen_lines = [], [], 0
    for t in texts[i + 1:]:
        t = t.strip()
        if not t or PLACEHOLDER.match(t):
            continue
        words = len(t.split())
        if seen_lines >= SECTION_MAX or SOURCE_HEADING.search(t) and looks_like_heading(t, 20) \
                or SOURCE_NOTE.search(t) or SOURCE_TRAIL.search(t) or section_title(t):
            break
        seen_lines += 1
        if words >= LABEL_WORDS:
            current.append(t)
        elif current:
            block.append(" ".join(current))
            current = []
    if current:
        block.append(" ".join(current))
    return block


def looks_like_heading(t, max_words=HEADING_WORDS):
    """A short line with no closing punctuation, e.g. "Field Insight: Telefónica's COE"."""
    return len(t.split()) < max_words and not re.search(r"[.:;!?\"”)]$", t)


def main(src, dst):
    os.makedirs(os.path.join(dst, "media"), exist_ok=True)
    z = zipfile.ZipFile(src)
    # Some generators write folder entries ("word/media/") into the zip; they hold no file.
    names = [n for n in z.namelist() if not n.endswith("/")]

    def read(name):
        return z.read(name).decode("utf-8")

    def write(fname, lines):
        with open(os.path.join(dst, fname), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    doc = read("word/document.xml")
    write("text.txt", paragraphs(doc))
    rels = read("word/_rels/document.xml.rels")
    write("images.txt", image_context(doc, rels))
    write("cited.txt", cited_text(doc, rels))

    hf = []
    for n in sorted(x for x in names if re.match(r"word/(header|footer)\d*\.xml$", x)):
        hf += ["[%s] %s" % (n.split("/")[1], t) for t in paragraphs(read(n))]
    write("headers.txt", hf)

    notes = []
    for n in ("word/footnotes.xml", "word/endnotes.xml"):
        if n in names:
            notes += paragraphs(read(n))
    write("notes.txt", notes)

    links = []
    for n in (x for x in names if x.startswith("word/_rels/") and x.endswith(".rels")):
        for a, b in LINK.findall(read(n)):
            target = unescape(a or b)
            if target not in links:
                links.append(target)
    write("hyperlinks.txt", links)

    media = [x for x in names if x.startswith("word/media/")]
    for n in media:
        with open(os.path.join(dst, "media", os.path.basename(n)), "wb") as f:
            f.write(z.read(n))

    print("text: %d paragraphs, headers/footers: %d, notes: %d, hyperlinks: %d, media: %d"
          % (len(paragraphs(read("word/document.xml"))), len(hf), len(notes), len(links), len(media)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
