"""Put a document's pictures on contact sheets, many to a page, so they can
be looked at in a few views instead of one by one.

Use it for the images that image_scan.py did not flag and that have no
credit next to them. Flagged images, and ones with a credit, are looked at
one by one (or read from their credit); the rest go on the sheets. It
leaves out the flagged ones (image_flags.txt) and the credited ones (the
credit and source notes credit_check.py finds in images.txt) by itself. A sheet
shows each picture's file name and a thumbnail, so it is good for spotting
a picture whose style differs from its neighbours (generated artwork, a
screenshot, a slide cut from elsewhere). It is not good for reading labels
or credits, and it can't tell that a diagram in the document's own style
was adapted from a textbook: those need the picture itself and a label
search.

Reads <output-dir>/media (from extract_docx.py) and, to leave flagged
pictures out, <output-dir>/image_flags.txt. Writes
<output-dir>/sheets/sheet_1.png, sheet_2.png ...: 12 pictures to a sheet,
four across and three down.

Usage:
  python -I contact_sheets.py <output-dir> [--skip image3.png,image9.png]
         [--include-flagged] [--no-auto-skip] [--per-sheet 12]
--skip            more file names to leave out
--include-flagged also put the flagged pictures on the sheets
--no-auto-skip    don't leave out the credited pictures
Needs Pillow.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import glob
import os
import re
import sys

W, H, COLS = 400, 300, 4


def natural(p):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", os.path.basename(p))]


def flagged(outdir):
    names = set()
    path = os.path.join(outdir, "image_flags.txt")
    if os.path.isfile(path):
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.match(r"(\S+?):\s+FLAGGED", line)
                if m:
                    names.add(m.group(1))
    return names


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("--skip", default="")
    ap.add_argument("--include-flagged", action="store_true")
    ap.add_argument("--no-auto-skip", action="store_true", help="don't leave out credited pictures")
    ap.add_argument("--per-sheet", type=int, default=12)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit("contact_sheets.py needs Pillow (pip install pillow).")

    skip = {s.strip() for s in a.skip.split(",") if s.strip()}
    if not a.include_flagged:
        skip |= flagged(a.outdir)
    if not a.no_auto_skip:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import credit_check  # noqa: E402  (same folder; -I doesn't add it to sys.path)
        tmf, credited, _ = credit_check.classify_images(
            credit_check.read_images(os.path.join(a.outdir, "images.txt")))
        skip |= set(tmf) | {name for name, _ in credited}
    files = [p for p in sorted(glob.glob(os.path.join(a.outdir, "media", "*")), key=natural)
             if os.path.basename(p) not in skip]
    if not files:
        print("No pictures left for contact sheets (%d skipped)." % len(skip))
        return
    out = os.path.join(a.outdir, "sheets")
    os.makedirs(out, exist_ok=True)
    rows = -(-a.per_sheet // COLS)
    written = []
    for start in range(0, len(files), a.per_sheet):
        sheet = Image.new("RGB", (W * COLS, H * rows), "white")
        draw = ImageDraw.Draw(sheet)
        for i, path in enumerate(files[start:start + a.per_sheet]):
            x, y = (i % COLS) * W, (i // COLS) * H
            try:
                im = Image.open(path)
                im.load()
                if im.mode in ("RGBA", "LA", "P"):
                    im = im.convert("RGBA")
                    bg = Image.new("RGBA", im.size, "white")
                    bg.alpha_composite(im)
                    im = bg
                im = im.convert("RGB")
                im.thumbnail((W - 8, H - 28))
                sheet.paste(im, (x + 4, y + 24))
            except Exception:
                draw.text((x + 8, y + 40), "can't read this picture", fill="red")
            draw.text((x + 6, y + 6), os.path.basename(path), fill="black")
            draw.rectangle([x, y, x + W - 1, y + H - 1], outline="gray")
        name = os.path.join(out, "sheet_%d.png" % (start // a.per_sheet + 1))
        sheet.save(name)
        written.append(name)
    print("%d pictures on %d sheet(s); %d left out (flagged or skipped):" % (len(files), len(written), len(skip)))
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
