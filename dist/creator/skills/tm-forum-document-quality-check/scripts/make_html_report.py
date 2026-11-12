"""Turn a run's Markdown report into a TM Forum-branded HTML report.

The page follows references/tm-forum-html-output.md: masthead, gradient
hero, disclaimer callout, contents, one section per ## heading, accessible
tables and the TM Forum footer. It reads the same Markdown make_report.py
reads and uses its parsing and class-word shading (CLASS_FILLS), so the
HTML and Word reports always agree. A document score table (one row,
headed "Poorly cited ownership", "Automation Indicators" ...) becomes score
cards whose numbers are coloured red, amber or green by class (grey for
dependence); a core citation card shows the citation's age, not the source.
Score cells show the score and its class only; bracketed z values are left out.

make_report.py writes this HTML next to every .docx it writes. To render
only the HTML:

Usage: python -I make_html_report.py <report.md> <report.html> [--title "..."]
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import datetime
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_report import AMBER, BULLET, GREEN, INLINE, NUMBERED, RED, TABLE_SEP, class_fill, split_row  # noqa: E402

TONES = {RED: "red", AMBER: "amber", GREEN: "green", "A6A6A6": "grey-dark", "D9D9D9": "grey", "F2F2F2": "grey-light"}
SCORE_HEADERS = ("poorly cited ownership", "automation indicators")

CSS = r"""
:root {
  --tmf-navy: #0d0b4d; --tmf-dark-red: #d91241; --tmf-bright-red: #ff004a; --tmf-orange: #ff5502;
  --tmf-green: #42b277; --tmf-blue: #39c5e5; --tmf-pink: #f4059d; --tmf-purple: #980bd9;
  --tmf-white: #ffffff; --tmf-off-white: #f7f7fa; --tmf-border: #d9d9e5; --tmf-muted: #5b5b73;
  --tmf-success-bg: #eaf7f0; --tmf-warning-bg: #fff4e8; --tmf-danger-bg: #fff0f3; --tmf-info-bg: #edf9fc;
  --tmf-gradient: linear-gradient(110deg, #0d0b4d 13%, #d91241 100%);
  --tmf-font: "DM Sans", Arial, sans-serif;
  --tmf-radius-sm: 8px; --tmf-radius-md: 14px; --tmf-radius-lg: 22px;
  --tmf-shadow: 0 10px 30px rgba(13, 11, 77, 0.10);
  --tmf-content-width: 1180px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--tmf-off-white); color: var(--tmf-navy); font-family: var(--tmf-font); font-size: 16px; line-height: 1.6; }
a { color: var(--tmf-dark-red); text-underline-offset: 0.18em; }
a:hover { text-decoration-thickness: 2px; }
a:focus-visible, button:focus-visible, [tabindex]:focus-visible { outline: 3px solid var(--tmf-orange); outline-offset: 3px; }
.tmf-skip-link { position: absolute; left: 1rem; top: -5rem; z-index: 999; padding: .65rem 1rem; background: var(--tmf-white); color: var(--tmf-navy); border-radius: var(--tmf-radius-sm); }
.tmf-skip-link:focus { top: 1rem; }
.tmf-masthead { padding: 1rem clamp(1rem, 4vw, 3rem); background: var(--tmf-navy); color: var(--tmf-white); }
.tmf-masthead__inner, .tmf-shell, .tmf-footer__inner { width: min(100%, var(--tmf-content-width)); margin-inline: auto; }
.tmf-brand-name { font-weight: 700; letter-spacing: -.02em; }
.tmf-shell { padding: clamp(1rem, 4vw, 3rem); }
.tmf-hero { padding: clamp(2rem, 7vw, 5.5rem); border-radius: var(--tmf-radius-lg); color: var(--tmf-white); background: var(--tmf-gradient); box-shadow: var(--tmf-shadow); }
.tmf-hero h1 { max-width: 18ch; margin: 0; font-size: clamp(2.25rem, 7vw, 5.25rem); line-height: .98; letter-spacing: -.045em; }
.tmf-hero p { max-width: 65ch; font-size: clamp(1.05rem, 2vw, 1.3rem); }
.tmf-section { margin-block: clamp(2rem, 6vw, 5rem); }
.tmf-section > h2 { font-size: clamp(1.65rem, 3.2vw, 2.5rem); line-height: 1.1; }
.tmf-eyebrow { margin: 0 0 .45rem; color: inherit; font-size: .78rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
.tmf-summary, .tmf-callout { padding: clamp(1.35rem, 4vw, 2.4rem); border-left: 6px solid var(--tmf-dark-red); border-radius: var(--tmf-radius-md); background: var(--tmf-white); box-shadow: var(--tmf-shadow); }
.tmf-card-grid, .tmf-stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr)); gap: 1.25rem; }
.tmf-card, .tmf-stat { padding: 1.5rem; border: 1px solid var(--tmf-border); border-radius: var(--tmf-radius-md); background: var(--tmf-white); }
.tmf-card h3, .tmf-stat h3 { margin-top: .2rem; line-height: 1.25; }
.tmf-stat__value { margin: 0; color: var(--tmf-dark-red); font-size: clamp(2.25rem, 5vw, 4rem); font-weight: 700; line-height: 1; }
.tmf-status { display: inline-flex; align-items: center; gap: .45rem; padding: .28rem .65rem; border-radius: 999px; font-size: .88rem; font-weight: 700; }
.tmf-status--green { background: var(--tmf-success-bg); color: #17653d; }
.tmf-status--amber { background: var(--tmf-warning-bg); color: #7a3d00; }
.tmf-status--red { background: var(--tmf-danger-bg); color: #9e1233; }
.tmf-status--neutral { background: #ececf2; color: #414155; }
.tmf-table-wrap { overflow-x: auto; border-radius: var(--tmf-radius-md); }
.tmf-table { width: 100%; border-collapse: collapse; background: var(--tmf-white); }
.tmf-table caption { padding: 1rem; font-weight: 700; text-align: left; }
.tmf-table th, .tmf-table td { padding: .9rem 1rem; border-bottom: 1px solid var(--tmf-border); text-align: left; vertical-align: top; }
.tmf-table th { background: var(--tmf-navy); color: var(--tmf-white); }
.tmf-footer { padding: 2rem clamp(1rem, 4vw, 3rem); background: var(--tmf-navy); color: var(--tmf-white); }
@media (max-width: 700px) { .tmf-hero { border-radius: var(--tmf-radius-md); } }
@media print {
  body { background: var(--tmf-white); color: var(--tmf-navy); }
  .tmf-skip-link { display: none; }
  .tmf-card, .tmf-stat, .tmf-summary, .tmf-callout { box-shadow: none; break-inside: avoid; }
  a { color: inherit; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
}
/* Report additions */
.tmf-hero h1.tmf-hero__title--long { max-width: 32ch; font-size: clamp(1.75rem, 4.5vw, 3.25rem); line-height: 1.08; letter-spacing: -.03em; }
.tmf-hero__meta { margin: 1.25rem 0 0; font-size: 1rem !important; opacity: .92; }
.tmf-shell p, .tmf-shell li, .tmf-table td { overflow-wrap: anywhere; }
.tmf-callout { margin-top: clamp(1.5rem, 4vw, 2.5rem); }
.tmf-callout p { margin: 0; }
.tmf-callout p + p { margin-top: .75rem; }
.tmf-toc { margin-top: clamp(1.5rem, 4vw, 2.5rem); padding: 1.25rem 1.5rem; border: 1px solid var(--tmf-border); border-radius: var(--tmf-radius-md); background: var(--tmf-white); }
.tmf-toc ol { margin: 0; padding-left: 1.4rem; columns: 2 18rem; column-gap: 2rem; }
.tmf-toc li { break-inside: avoid; padding-block: .15rem; }
.tmf-section h3 { margin-top: 2rem; font-size: 1.3rem; line-height: 1.25; }
.tmf-section h4 { margin: 1.5rem 0 .5rem; font-size: 1.05rem; }
.tmf-section .tmf-table-wrap { margin-block: 1rem 1.5rem; border: 1px solid var(--tmf-border); }
.tmf-section hr { border: 0; border-top: 1px solid var(--tmf-border); margin-block: 2rem; }
.tmf-section code { font-size: .9em; padding: .05em .3em; border-radius: 4px; background: #ececf2; }
.tmf-table { font-size: .95rem; }
.tmf-table caption { color: var(--tmf-navy); }
.tmf-table tbody tr:nth-child(even) td { background: var(--tmf-off-white); }
.tmf-stat-grid { margin-block: 1rem 1.25rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr)); }
.tmf-stat { display: flex; flex-direction: column; gap: .35rem; }
.tmf-stat h3 { order: -1; margin: 0; font-size: .82rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--tmf-muted); }
.tmf-stat p { margin: 0; }
.tmf-stat__value { color: var(--tmf-navy); }
.tmf-stat__value--text { font-size: 1.15rem; line-height: 1.3; overflow-wrap: anywhere; }
.tmf-stat__value--green { color: #17653d; }
.tmf-stat__value--amber { color: #7a3d00; }
.tmf-stat__value--red { color: #9e1233; }
.tmf-stat__value--grey-light, .tmf-stat__value--grey, .tmf-stat__value--grey-dark { color: #414155; }
.tmf-status--grey-light, .tmf-status--grey, .tmf-status--grey-dark { background: #ececf2; color: #414155; }
.tmf-table tbody tr td.tmf-cell--green { background: var(--tmf-success-bg); }
.tmf-table tbody tr td.tmf-cell--amber { background: var(--tmf-warning-bg); }
.tmf-table tbody tr td.tmf-cell--red { background: var(--tmf-danger-bg); }
.tmf-table tbody tr td.tmf-cell--grey-light { background: #f7f7fa; }
.tmf-table tbody tr td.tmf-cell--grey { background: #ececf2; }
.tmf-table tbody tr td.tmf-cell--grey-dark { background: #d9d9e5; }
.tmf-footer__inner { display: flex; flex-wrap: wrap; gap: .5rem 2rem; justify-content: space-between; }
"""


def esc(s):
    return html.escape(s, quote=True)


def inline(text):
    """**bold**, *italic*, `code` and [links](url). Only https links are linked; bare URLs stay text."""
    out = []
    for piece in INLINE.split(text):
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**") and len(piece) > 4:
            out.append("<strong>%s</strong>" % inline(piece[2:-2]))
        elif piece.startswith("`") and piece.endswith("`"):
            out.append("<code>%s</code>" % esc(piece[1:-1]))
        elif piece.startswith("[") and "](" in piece:
            label, url = piece[1:-1].split("](", 1)
            out.append('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (esc(url), inline(label))
                       if url.startswith("https://") else inline(label))
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            out.append("<em>%s</em>" % inline(piece[1:-1]))
        else:
            out.append(esc(piece.replace("\\|", "|")))
    return "".join(out)


def plain(text):
    return re.sub(r"[*`]", "", text).strip()


def tone(header, text):
    return TONES.get(class_fill(header, text))


def is_score_table(rows):
    header = " ".join(rows[0]).lower()
    return len(rows) == 2 and all(h in header for h in SCORE_HEADERS)


def score_cards(rows):
    cards = []
    for h, v in zip(rows[0], rows[1]):
        h, v = plain(h), plain(v)
        t = tone(h, v)
        if h.lower().startswith("core citation"):
            age = re.search(r";\s*(\d[\d.]*)\s+years?\s*$", v)
            pub = re.search(r"published\s+([\w-]+)", v)
            if age:
                value, ctx, cls = "%s years" % age.group(1), ("published %s" % pub.group(1) if pub else ""), ""
            elif "date not found" in v:
                value, ctx, cls = "Age not known", "publication date not found", " tmf-stat__value--text"
            else:
                value, ctx, cls = v, "", " tmf-stat__value--text"
        else:
            m = re.match(r"^([+\-−]?\d[\d.,]*)\s*(.*)$", v)
            if not m:
                value, ctx, cls = v, "", " tmf-stat__value--text"
            else:
                value, rest = m.group(1), m.group(2)
                cls = " tmf-stat__value--%s" % t if t else ""
                ctx = esc(rest)
                if t:
                    word = re.search(r"very inconsistent|\b(bad|improving|good|high|medium|low|heavy|typical|light|inconsistent|consistent)\b",
                                     rest, re.I).group(0)
                    other = re.sub(r"\s*\(?%s\)?" % re.escape(word), "", rest, count=1).strip(" ,;")
                    ctx = '<span class="tmf-status tmf-status--%s">%s</span>%s' % (t, esc(word), " " + esc(other) if other else "")
                cards.append('<article class="tmf-stat"><p class="tmf-stat__value%s">%s</p><h3>%s</h3><p>%s</p></article>'
                             % (cls, esc(value), esc(h), ctx))
                continue
        cards.append('<article class="tmf-stat"><p class="tmf-stat__value%s">%s</p><h3>%s</h3>%s</article>'
                     % (cls, esc(value), esc(h), "<p>%s</p>" % esc(ctx) if ctx else ""))
    return '<div class="tmf-stat-grid" aria-label="Document score">%s</div>' % "".join(cards)


def table(rows, caption, tid):
    header, body = rows[0], rows[1:]
    head = "".join('<th scope="col">%s</th>' % inline(h) for h in header)
    trs = []
    for row in body:
        tds = []
        for c, h in enumerate(header):
            cell = row[c] if c < len(row) else ""
            t = tone(plain(h), plain(cell))
            tds.append('<td%s>%s</td>' % (' class="tmf-cell--%s"' % t if t else "", inline(cell)))
        trs.append("<tr>%s</tr>" % "".join(tds))
    width = ' style="min-width:%dpx"' % (len(header) * 150) if len(header) > 4 else ""
    return ('<div class="tmf-table-wrap" role="region" aria-labelledby="%s" tabindex="0"><table class="tmf-table"%s>'
            '<caption id="%s">%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % (tid, width, tid, esc(caption), head, "".join(trs)))


def drop_z(md):
    """Score cells show the score and its class only: drop the bracketed z, e.g. "0.271 (+0.95) bad"."""
    md = re.sub(r",\s*its z in brackets(?:\s*\([^)]*\))?,\s*and its class", " and its class", md)
    return "\n".join(re.sub(r"\s\([+\-−]\d[\d.]*\)", "", l) if l.lstrip().startswith("|") else l
                     for l in md.splitlines())


def render_html(md, out, title=None):
    lines = drop_z(md).splitlines()
    used = set()

    def slug(text):
        base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "section"
        s, n = base, 2
        while s in used:
            s, n = "%s-%d" % (base, n), n + 1
        used.add(s)
        return s

    md_title = next((plain(l[2:]) for l in lines if l.startswith("# ")), None)
    title = title or md_title or "Report"
    eyebrow, h1 = (title.split(": ", 1) + [""])[:2] if ": " in title else ("Report", title)
    h1 = h1[:1].upper() + h1[1:]

    callouts, sections, cur = [], [], None
    state = {"level": 2, "caption": "", "tables": 0}

    def section(heading):
        nonlocal cur
        cur = {"id": slug(heading), "title": heading, "body": []}
        sections.append(cur)
        state["level"] = 2

    i = 0
    while i < len(lines):
        line, stripped = lines[i], lines[i].strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            box = "<p>%s</p>" % inline(" ".join(quote))
            if cur is None:
                callouts.append(box)
            else:
                cur["body"].append('<aside class="tmf-callout">%s</aside>' % box)
            continue
        heading = re.match(r"^(#{1,4}) (.*)$", stripped)
        if heading:
            text, level = plain(heading.group(2)), len(heading.group(1))
            i += 1
            if level == 1 and text == md_title:
                continue
            if level <= 2:
                section(text)
            else:
                if cur is None:
                    section("Overview")
                lv = min(level, state["level"] + 1, 4)
                cur["body"].append('<h%d id="%s">%s</h%d>' % (lv, slug(text), esc(text), lv))
                state["level"] = lv
            state["caption"] = text
            continue
        if cur is None:
            # Content before the first ## heading: the score block, or a note above it.
            if stripped.startswith("|") or stripped == "**Document score.**":
                section("Document score")
            else:
                callouts.append("<p>%s</p>" % inline(stripped))
                i += 1
                while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\|)", lines[i].strip()):
                    callouts[-1] = callouts[-1][:-4] + " " + inline(lines[i].strip()) + "</p>"
                    i += 1
                continue
        if stripped == "**Document score.**" and cur["title"] == "Document score":
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1].strip()):
            rows = [split_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            state["tables"] += 1
            if cur["title"] == "Document score" and is_score_table(rows):
                cur["body"].append(score_cards(rows))
            else:
                cur["body"].append(table(rows, state["caption"] or "Table %d" % state["tables"], "tbl-%d" % state["tables"]))
            continue
        if re.match(r"^-{3,}$", stripped):
            cur["body"].append("<hr>")
            i += 1
            continue
        if BULLET.match(line) or NUMBERED.match(line):
            stack = []  # (tag, indent)
            while i < len(lines) and (BULLET.match(lines[i]) or NUMBERED.match(lines[i])):
                m = BULLET.match(lines[i]) or NUMBERED.match(lines[i])
                numbered = not BULLET.match(lines[i])
                indent = len(m.group(1).replace("\t", "  "))
                text = m.group(3) if numbered else m.group(2)
                i += 1
                while i < len(lines) and lines[i].strip() and lines[i].startswith(" " * (indent + 2)) \
                        and not BULLET.match(lines[i]) and not NUMBERED.match(lines[i]) and not lines[i].strip().startswith("|"):
                    text += " " + lines[i].strip()
                    i += 1
                tag = "ol" if numbered else "ul"
                while stack and stack[-1][1] > indent:
                    cur["body"].append("</li></%s>" % stack.pop()[0])
                if stack and stack[-1][1] == indent:
                    cur["body"].append("</li><li>")
                else:
                    start = ' start="%s"' % m.group(2) if numbered and m.group(2) != "1" else ""
                    cur["body"].append("<%s%s><li>" % (tag, start))
                    stack.append((tag, indent))
                cur["body"].append(inline(text))
            while stack:
                cur["body"].append("</li></%s>" % stack.pop()[0])
            continue
        para = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\||-{3,}$)", lines[i].strip()) \
                and not BULLET.match(lines[i]) and not NUMBERED.match(lines[i]):
            para.append(lines[i].strip())
            i += 1
        text = " ".join(para)
        if re.fullmatch(r"\*\*[^*]+\*\*", text) and len(text) < 160:
            lv = min(state["level"] + 1, 4)
            cur["body"].append("<h%d>%s</h%d>" % (lv, esc(plain(text)), lv))
            state["caption"] = plain(text).rstrip(".")
        else:
            cur["body"].append("<p>%s</p>" % inline(text))

    today = datetime.date.today().isoformat()
    toc = "".join('<li><a href="#%s">%s</a></li>' % (s["id"], esc(s["title"])) for s in sections)
    body = "".join('<section class="tmf-section" aria-labelledby="%s"><h2 id="%s">%s</h2>%s</section>'
                   % (s["id"], s["id"], esc(s["title"]), "".join(s["body"])) for s in sections)
    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{h1} | TM Forum</title>
<meta name="description" content="{title}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&amp;display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<a class="tmf-skip-link" href="#main-content">Skip to main content</a>
<header class="tmf-masthead"><div class="tmf-masthead__inner"><span class="tmf-brand-name">TM Forum</span></div></header>
<main id="main-content" class="tmf-shell">
<section class="tmf-hero" aria-labelledby="page-title">
<p class="tmf-eyebrow">{eyebrow}</p>
<h1 id="page-title"{long}>{h1}</h1>
<p class="tmf-hero__meta">Report dated {today}.</p>
</section>
{callouts}
<nav class="tmf-toc" aria-labelledby="toc-title"><p class="tmf-eyebrow" id="toc-title">Contents</p><ol>{toc}</ol></nav>
{body}
</main>
<footer class="tmf-footer"><div class="tmf-footer__inner"><span class="tmf-brand-name">TM Forum</span><span>Generated {today}</span></div></footer>
</body>
</html>
""".format(h1=esc(h1), title=esc(title), css=CSS, eyebrow=esc(eyebrow), today=today, toc=toc, body=body,
           long=' class="tmf-hero__title--long"' if len(h1) > 40 else "",
           callouts='<aside class="tmf-callout" aria-label="Notes">%s</aside>' % "".join(callouts) if callouts else "")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown")
    ap.add_argument("html")
    ap.add_argument("--title")
    a = ap.parse_args()
    with open(a.markdown, encoding="utf-8") as f:
        md = f.read()
    render_html(md, a.html, a.title)
    print("Wrote %s" % a.html)


if __name__ == "__main__":
    sys.exit(main())
