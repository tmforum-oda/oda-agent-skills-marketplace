"""Turn a .pdf into a minimal .docx package so the rest of the check runs unchanged.

Use it only when the document isn't available as .docx or .xlsx. The package holds
what the other scripts read, and nothing else:
  word/document.xml   body text as paragraphs (one per PDF text block), in reading
                      order, with each picture placed where it sits on the page and
                      each link wrapped round the text it covers
  word/header1.xml,   lines in the top or bottom band of the page that repeat on
  word/footer1.xml    three or more pages (running headers, footers, page numbers),
                      kept out of the body
  word/_rels/document.xml.rels   picture and external-link targets
  word/media/         the pictures (header and footer logos once each)
  docProps/core.xml, docProps/app.xml   the PDF's own metadata (author, title,
                      creator, producer, dates), for the AI-indicator check

Then run extract_docx.py, image_scan.py and ai_indicators.py --docx on the .docx
it writes, as for a Word document. Text from a PDF loses what Word keeps: content
controls, styles and footnote markup; tables come out cell by cell; a paragraph
split by a page break stays split. Say in the report that the document was read
from a PDF.

Usage: python -I pdf_to_docx.py <input.pdf> <output.docx>
Needs PyMuPDF (fitz).
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import hashlib
import re
import sys
import zipfile
from xml.sax.saxutils import escape

import fitz

BAND = 0.07          # top and bottom share of the page treated as header/footer zone
REPEAT_PAGES = 3     # a band line on this many pages is a running header or footer
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" ' \
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'


def norm(t):
    return re.sub(r"\d+", "#", t.strip())


def run(t):
    return '<w:r><w:t xml:space="preserve">%s</w:t></w:r>' % escape(t) if t else ""


def main(src, dst):
    doc = fitz.open(src)
    pages = []
    band_count = {}
    for page in doc:
        h = page.rect.height
        d = page.get_text("dict")
        items = []
        for b in d["blocks"]:
            y0, y1 = b["bbox"][1], b["bbox"][3]
            in_band = y1 < h * BAND or y0 > h * (1 - BAND)
            if b["type"] == 0:
                text = " ".join(" ".join(s["text"] for s in l["spans"]).strip() for l in b["lines"])
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    items.append(("text", b["bbox"], text, in_band))
                    if in_band:
                        band_count.setdefault(norm(text), set()).add(page.number)
            elif b["type"] == 1 and b.get("image"):
                items.append(("image", b["bbox"], (b["image"], b.get("ext", "png")), in_band))
        links = [(fitz.Rect(l["from"]), l["uri"]) for l in page.get_links() if l.get("uri")]
        pages.append((page, items, links))
    running = {k for k, v in band_count.items() if len(v) >= REPEAT_PAGES}

    body, headers, footers, rels, media = [], [], [], [], {}
    rid = 0
    for page, items, links in pages:
        h = page.rect.height
        for kind, bbox, data, in_band in sorted(items, key=lambda x: (round(x[1][1]), x[1][0])):
            if kind == "text":
                if in_band and norm(data) in running:
                    target = headers if bbox[1] < h * BAND else footers
                    if data not in target:
                        target.append(data)
                    continue
                done, rest, extra = [], data, []
                for rect, uri in links:
                    if not rect.intersects(fitz.Rect(bbox)):
                        continue
                    shown = re.sub(r"\s+", " ", page.get_textbox(rect)).strip()
                    rid += 1
                    rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                                'relationships/hyperlink" Target="%s" TargetMode="External"/>' % (rid, escape(uri, {'"': "&quot;"})))
                    if shown and shown in rest:
                        a, rest = rest.split(shown, 1)
                        done += [run(a), '<w:hyperlink r:id="rId%d">%s</w:hyperlink>' % (rid, run(shown))]
                    else:
                        extra.append('<w:hyperlink r:id="rId%d"/>' % rid)
                body.append("<w:p>%s</w:p>" % "".join(done + [run(rest)] + extra))
            else:
                img, ext = data
                key = hashlib.sha256(img).hexdigest()
                if in_band and key in media:
                    continue  # a logo repeated in every header or footer
                if key not in media:
                    media[key] = ("image%d.%s" % (len(media) + 1, ext), img)
                rid += 1
                rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                            'relationships/image" Target="media/%s"/>' % (rid, media[key][0]))
                body.append('<w:p><w:r><w:drawing><a:blip xmlns:a="x" r:embed="rId%d"/></w:drawing></w:r></w:p>' % rid)

    m = doc.metadata or {}
    core = ('<cp:coreProperties xmlns:cp="c" xmlns:dc="d" xmlns:dcterms="t">'
            + "".join("<%s>%s</%s>" % (tag, escape(m.get(key) or ""), tag)
                      for tag, key in (("dc:title", "title"), ("dc:creator", "author"), ("dc:subject", "subject"),
                                       ("cp:keywords", "keywords"), ("dcterms:created", "creationDate"),
                                       ("dcterms:modified", "modDate")) if m.get(key))
            + "</cp:coreProperties>")
    app = ('<Properties><Application>%s</Application><Producer>%s</Producer></Properties>'
           % (escape(m.get("creator") or ""), escape(m.get("producer") or "")))

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("word/document.xml", "<w:document %s><w:body>%s</w:body></w:document>" % (W, "".join(body)))
        z.writestr("word/_rels/document.xml.rels", "<Relationships>%s</Relationships>" % "".join(rels))
        z.writestr("word/header1.xml", "<w:hdr %s>%s</w:hdr>" % (W, "".join("<w:p>%s</w:p>" % run(t) for t in headers)))
        z.writestr("word/footer1.xml", "<w:ftr %s>%s</w:ftr>" % (W, "".join("<w:p>%s</w:p>" % run(t) for t in footers)))
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        for name, img in media.values():
            z.writestr("word/media/" + name, img)
    print("%s: %d pages, %d paragraphs, %d pictures, %d links, %d running header/footer lines"
          % (dst, len(pages), sum(1 for b in body if "w:drawing" not in b), len(media),
             sum(1 for r in rels if "hyperlink" in r), len(headers) + len(footers)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
