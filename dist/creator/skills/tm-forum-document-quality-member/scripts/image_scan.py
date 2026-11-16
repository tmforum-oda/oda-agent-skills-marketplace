"""Flag images in a .docx that may contain clip-art, icons or other
artwork of outside origin.

Two kinds of signal, both automatic:

1. Metadata (always run, standard library only):
   - Office icons inserted from Word's Insert > Icons (an svgBlip), or a
     picture whose name or alt text says icon, clip art, graphic or stock.
   - WMF/EMF pictures, the format of Office clip art.
   - Author, copyright, creator or software fields in the picture file
     (PNG text chunks, JPEG EXIF/XMP).

2. Pictograms (needs Pillow and numpy; skipped with a note if missing):
   finds small, isolated, irregular shapes that aren't text, boxes,
   lines, arrows or circles, which is what icons and clip-art figures
   look like inside a diagram. Each is reported as:
   - "multi-colour": 12+ colours, typical of clip-art or illustrations;
   - "monochrome": fewer colours, typical of icons and pictograms.
   This is a heuristic. It points at images to look at; it doesn't prove
   anything was copied, and it can miss artwork or flag a shape that is
   the author's own.

Usage: python -I image_scan.py <input.docx> <output-dir>
Writes <output-dir>/image_flags.txt and prints the same report.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import hashlib
import os
import re
import struct
import sys
import zipfile
from collections import deque

NAME_HINT = re.compile(r"icon|clip ?art|clipart|graphic \d|stock|shutterstock|getty|istock|freepik|flaticon|vecteezy", re.I)
META_KEYS = re.compile(rb"(Artist|Copyright|Author|Creator|Software|Rights|Source|Credit)", re.I)
DOC_PR = re.compile(r'<(?:wp:docPr|xdr:cNvPr) ([^>]*)>.*?(?:r:embed="([^"]+)")', re.S)
ATTR = re.compile(r'(\w+)="([^"]*)"')
REL = re.compile(r'<Relationship [^>]*?Id="([^"]+)"[^>]*?Target="([^"]+)"')

# Pictogram detector settings (pixels refer to the picture as stored).
BG_DIFF = 48            # how far from the background colour counts as ink
MIN_H, MAX_H = 16, 160  # icon height range; smaller is text, larger is a panel
MIN_W, MAX_W = 14, 200
ASPECT = (0.5, 2.2)     # icons are roughly square
FILL = (0.15, 0.72)     # share of the bounding box inked: not a line, not a solid box
SOLIDITY = (0.42, 0.72) # share of the convex hull inked: arrows/circles are near 1
MULTI_COLOUR = 12       # distinct colours (in 32-level steps) for clip-art

# TM Forum's own images, by SHA-256 of the file, reported as such and not scanned.
KNOWN_OWN = {
    "b0777e4b69f9cae89d307e922e448db7de1fbe338b47ab262e5a7304e5000e9f": "TM Forum logo",
}


def metadata_flags(name, data):
    flags = []
    ext = os.path.splitext(name)[1].lower()
    if ext in (".wmf", ".emf"):
        flags.append("WMF/EMF picture (Office clip-art format)")
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        i = 8
        while i + 8 <= len(data):
            n, = struct.unpack(">I", data[i:i + 4])
            kind = data[i + 4:i + 8]
            if kind in (b"tEXt", b"iTXt", b"zTXt"):
                key = data[i + 8:i + 8 + n].split(b"\0", 1)[0]
                if META_KEYS.search(key) or key.startswith(b"XML:com.adobe.xmp"):
                    flags.append("PNG metadata: %s" % key.decode("latin-1"))
            if kind == b"IEND":
                break
            i += 12 + n
    elif data[:2] == b"\xff\xd8":
        head = data[:65536]
        for key in sorted(set(m.group(1).decode() for m in META_KEYS.finditer(head))):
            flags.append("JPEG metadata field: %s" % key)
    return flags


def components(mask):
    import numpy as np
    h, w = mask.shape
    label = np.zeros((h, w), np.int32)
    out, n = [], 0
    for y0, x0 in zip(*np.nonzero(mask)):
        if label[y0, x0]:
            continue
        n += 1
        label[y0, x0] = n
        queue, pts = deque([(y0, x0)]), []
        while queue:
            y, x = queue.popleft()
            pts.append((y, x))
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not label[yy, xx]:
                    label[yy, xx] = n
                    queue.append((yy, xx))
        out.append(np.array(pts))
    return out


def solidity(pts):
    p = sorted(set(map(tuple, pts[:, ::-1].tolist())))
    if len(p) < 3:
        return 1.0

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for q in p:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], q) <= 0:
            lower.pop()
        lower.append(q)
    for q in reversed(p):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], q) <= 0:
            upper.pop()
        upper.append(q)
    hull = lower[:-1] + upper[:-1]
    area = abs(sum(hull[i][0] * hull[(i + 1) % len(hull)][1] - hull[(i + 1) % len(hull)][0] * hull[i][1]
                   for i in range(len(hull)))) / 2 + len(hull) / 2 + 1
    return len(pts) / area


def pictograms(data):
    """Return a list of (x, y, w, h, colours) for icon-like shapes."""
    import io
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(io.BytesIO(data)).convert("RGB")).astype(int)
    vals, counts = np.unique((a // 8).reshape(-1, 3), axis=0, return_counts=True)
    background = vals[counts.argmax()] * 8 + 4
    mask = np.abs(a - background).max(axis=2) > BG_DIFF
    shapes = []
    for pts in components(mask):
        if len(pts) < 20:
            continue
        y0, x0 = pts.min(0)
        y1, x1 = pts.max(0)
        shapes.append((int(x0), int(y0), int(x1 - x0 + 1), int(y1 - y0 + 1), pts))
    found = []
    for i, (x, y, w, h, pts) in enumerate(shapes):
        if not (MIN_H <= h <= MAX_H and MIN_W <= w <= MAX_W and ASPECT[0] <= w / h <= ASPECT[1]):
            continue
        if not FILL[0] <= len(pts) / (w * h) <= FILL[1]:
            continue
        # Text: another shape of similar height sits next to it on the same line.
        if any(j != i and 0.6 * h <= h2 <= 1.6 * h
               and min(y + h, y2 + h2) - max(y, y2) >= 0.6 * min(h, h2)
               and max(x2 - (x + w), x - (x2 + w2)) < 0.8 * h
               for j, (x2, y2, w2, h2, _) in enumerate(shapes)):
            continue
        if not SOLIDITY[0] <= solidity(pts) <= SOLIDITY[1]:
            continue
        colours = len(np.unique(a[pts[:, 0], pts[:, 1]] // 32, axis=0))
        found.append((x, y, w, h, colours))
    return found


def main(src, dst):
    sys.stdout.reconfigure(encoding="utf-8")
    z = zipfile.ZipFile(src)
    names = [n for n in z.namelist() if not n.endswith("/")]  # skip folder entries ("word/media/")
    if "word/document.xml" in names:
        doc = z.read("word/document.xml").decode("utf-8")
        rels = dict(REL.findall(z.read("word/_rels/document.xml.rels").decode("utf-8")))
        media_dir = "word/media/"
    else:  # a .xlsx workbook: pictures sit in its drawings, each drawing with its own rels
        drawings = sorted(n for n in names if re.match(r"xl/drawings/drawing\d+\.xml$", n))
        doc = "".join(z.read(n).decode("utf-8") for n in drawings)
        rels = {}
        for n in drawings:
            r = "xl/drawings/_rels/%s.rels" % os.path.basename(n)
            if r in names:
                rels.update(REL.findall(z.read(r).decode("utf-8")))
        media_dir = "xl/media/"

    doc_flags = {}
    for attrs, rid in DOC_PR.findall(doc):
        a = dict(ATTR.findall(attrs))
        text = " ".join(filter(None, (a.get("name"), a.get("descr"), a.get("title"))))
        target = os.path.basename(rels.get(rid, ""))
        if target and NAME_HINT.search(text):
            doc_flags.setdefault(target, []).append('name/alt text: "%s"' % text[:120])
    if "svgBlip" in doc:
        doc_flags.setdefault("(document)", []).append(
            "%d Office icon(s) inserted as SVG (Insert > Icons)" % doc.count("svgBlip"))

    try:
        import numpy  # noqa: F401
        from PIL import Image  # noqa: F401
        pixel_ok = True
    except ImportError:
        pixel_ok = False

    lines = []
    if not pixel_ok:
        lines.append("NOTE: Pillow/numpy not installed - pictogram detection skipped; metadata checks only.")
    for target, flags in doc_flags.items():
        if target == "(document)":
            lines += ["(document): %s" % f for f in flags]
    for name in sorted((n for n in names if n.startswith(media_dir)),
                       key=lambda n: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", n)]):
        base = os.path.basename(name)
        data = z.read(name)
        known = KNOWN_OWN.get(hashlib.sha256(data).hexdigest())
        if known:
            lines.append("%s: known TM Forum image (%s)" % (base, known))
            continue
        flags =doc_flags.get(base, []) + metadata_flags(base, data)
        if pixel_ok and os.path.splitext(base)[1].lower() in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
            try:
                found = pictograms(data)
            except Exception as e:  # unreadable picture: say so rather than stop
                flags.append("pictogram check failed: %s" % e)
                found = []
            multi = [f for f in found if f[4] >= MULTI_COLOUR]
            mono = [f for f in found if f[4] < MULTI_COLOUR]
            for label, group in (("multi-colour (clip-art/illustration)", multi), ("monochrome (icon/pictogram)", mono)):
                if group:
                    where = ", ".join("%dx%d at (%d,%d)" % (w, h, x, y) for x, y, w, h, _ in group[:6])
                    flags.append("%d %s shape(s): %s%s" % (len(group), label, where, " ..." if len(group) > 6 else ""))
        lines.append("%s: %s" % (base, "FLAGGED - " + "; ".join(flags) if flags else "no signals"))

    os.makedirs(dst, exist_ok=True)
    with open(os.path.join(dst, "image_flags.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
