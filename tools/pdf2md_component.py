"""Reads: references/components/{ID}/{ID}_{Name}_v{version}.pdf.
Writes: knowledge/components/{ID}/{ID}.md, knowledge/components/{ID}/media/*.
Track: automated (spec/spec-components.md 7) -- no login gate, but heavier
than fetch_component.py's tag-pinned discovery: the download URL has to be
resolved from a real TM Forum ODA directory page load per component first
(spec/spec-components.md 3), not assembled from a URL pattern. That
discovery+download step isn't done by this script, and as of
spec/tasks-components.md Phase 8 isn't yet its own checked-in tools/*.py
script either -- done per-component via a driven browser through Phases
1-6. This script only does the PDF -> Markdown half, once a URL and the
raw PDF are already in hand.

tools/pdf2md_component.py -- TM Forum Component Specification PDF ->
knowledge/components/<ID>/<ID>.md

Strips the fixed set of boilerplate sections documented in
spec/spec-components.md 4.1 (title page, Notice, Table of Contents,
References, Administrative Appendix and its children) using the same
mechanical, heading-name-driven approach as tools/docx2md.py (spec/spec.md
5.1.1) -- adapted for numbered PDF section headings ("2.3. Functional
Framework Functions") instead of Word paragraph styles, since these PDFs
carry no style/outline metadata pypdf or pdfplumber can read directly.

Tables are real GFM tables, not verbatim text. Per page: pdfplumber's
`find_tables()` gives each table's bounding box and cell grid directly (it
does its own line/rect-based structural detection -- this is not a text-
layout heuristic), and `page.filter()` then extracts the *prose* text with
every table's own bounding box excluded, so table content is never counted
twice. A table that continues onto the next page (TM Forum's own template
repeats the header row on each new page) is detected by comparing the new
page's first table's normalized header against the still-open table's, and
merged into one continuous table rather than emitted as several small ones.

Images are linked inline from the body, at the position they actually
appear (interleaved with prose and tables the same way, by vertical
position on the page -- not appended as a files-extracted-but-unlinked
footnote). Deduplicated by content hash before being saved -- every page
of these PDFs repeats the same TM Forum logo image, which would otherwise
flood media/ with dozens of copies of the same three logo bitmaps (see
spec/spec-components.md 4.2). Position comes from `pdfplumber` (`page.
images`, which gives each image's bounding box); the actual decoded bytes
come from `pypdf` (`page.images[i].data`, already a valid PNG/JPEG) rather
than from `pdfplumber` itself, since pdfplumber's image objects are a raw,
still-encoded content stream. The two libraries report a page's images in
the same order, confirmed directly against this component's real PDF, so
matching them up by index within a page is reliable.

Usage:
    python pdf2md_component.py <ID> <name> <version> <pdf_url> <src.pdf> <out.md> <media_dir_name> [status]

    <status> is the component's directory status (spec/spec-components.md 6)
    -- defaults to "specified" since that's true for most of the 25
    components with a PDF at all, but TMFC011 is "Pre-production", not
    "specified", and the envelope must say so rather than defaulting.

Example:
    python pdf2md_component.py TMFC039 "Agreement Management" 1.1.0 \
        https://oda-production.s3.eu-west-2.amazonaws.com/v1.0.0/TMFC039_Agreement_Management_v1.1.0.pdf \
        references/components/TMFC039/TMFC039_Agreement_Management_v1.1.0.pdf \
        knowledge/components/TMFC039/TMFC039.md media
"""
import datetime as _dt
import hashlib
import json
import os
import re
import sys

import pdfplumber
from pypdf import PdfReader

import _yaml_lite as yaml_lite

ID = sys.argv[1]
NAME = sys.argv[2]
VERSION = sys.argv[3]
PDF_URL = sys.argv[4]
SRC = sys.argv[5]
OUT = sys.argv[6]
MEDIA_DIR_NAME = sys.argv[7]
STATUS = sys.argv[8] if len(sys.argv) > 8 else "specified"
MEDIA_DIR = os.path.join(os.path.dirname(OUT), MEDIA_DIR_NAME)

os.makedirs(MEDIA_DIR, exist_ok=True)

# --- boilerplate to strip, spec/spec-components.md 4.1 -- fixed heading-text list ---
DROP_HEADINGS = {
    "notice",
    "table of contents",
    "references",
    "administrative appendix",
    "document history",
    "version history",
    "release history",
    "acknowledgments",
    "acknowledgements",
}
# A numbered heading line, e.g. "2.3. Functional Framework Functions" or "1. Overview".
# Requires a literal ". " right after the number so table rows like "1026      Collaboration"
# (a Functional Framework Function ID, not a heading) never match -- confirmed against
# TMFC039's actual layout, where every genuine heading has this shape and no table-row
# leading number does.
HEADING_RE = re.compile(r"^\s*(\d+(?:\.\d+)*)\.\s+(\S.*\S|\S)\s*$")
# A Table-of-Contents entry ("1. Overview .......................... 5") uses the exact
# same numbered-heading shape as a real heading, and dot-leaders are the only reliable
# textual signal distinguishing it -- drop these lines outright, before heading
# detection ever sees them, or the *first* "1. Overview" match is the ToC line itself.
TOC_LEADER_RE = re.compile(r"\.{4,}")
# The optional lone "." before "Page N of M" handles a real rendering artifact
# (confirmed on TMFC003: "TM Forum 2025. All Rights Reserved. . Page 12 of 27" -- an
# extra stray period, likely a misplaced copyright-symbol glyph, that an exactly-one-
# optional-period pattern doesn't account for and would otherwise leak as a stray line).
# Both "All Rights Reserved" and the "of M" page-total are themselves optional -- some
# components use an older, shorter footer template with neither (confirmed on TMFC050,
# every single page: "TM Forum 2021. Page 3", no "All Rights Reserved" at all and no
# page total) which the previous, stricter pattern didn't match at all, leaking the
# whole footer as a stray paragraph on every page of that document.
FOOTER_RE = re.compile(
    r"^.{0,3}TM Forum \d{4}\.?(?: All Rights Reserved\.?)?\s*\.?\s*(Page \d+(?: of \d+)?)?\s*$", re.IGNORECASE
)
PAGE_NUM_RE = re.compile(r"^\s*Page \d+(?: of \d+)?\s*$", re.IGNORECASE)
# The running header/footer every page repeats ("TMFC039 Agreement Management v1.1.0"),
# built from ID/name/version rather than hardcoded so it matches regardless of component.
# Not anchored at the end -- some components append a trailing ticket reference after
# the version ("TMFC001 Product Catalog Management v2.1.2 (TAC-1172)"), which an
# end-anchored pattern misses entirely, leaking the whole running header as a stray
# body paragraph on every single page.
ID_FOOTER_RE = re.compile(rf"^{re.escape(ID)}\b.*v{re.escape(VERSION)}\b", re.IGNORECASE)


# --- images: dedup by content hash -- every page repeats the same header/footer logo,
# and a byte-size floor drops that logo's two colour variants even on their first
# occurrence (confirmed on TMFC039: the two logo bitmaps are 9043/9229 bytes, every
# real diagram is 26KB+) ---
MIN_IMAGE_BYTES = 15000
seen_image_hashes = set()
img_counter = 0


def save_image(data, ext):
    """Write a real (non-logo, not-yet-seen) image to media/ and return its filename,
    or None if it's a duplicate/too-small-to-be-a-real-diagram and should be skipped."""
    global img_counter
    if len(data) < MIN_IMAGE_BYTES:
        return None
    h = hashlib.sha256(data).hexdigest()
    if h in seen_image_hashes:
        return None
    seen_image_hashes.add(h)
    img_counter += 1
    fname = f"image{img_counter:02d}.{ext}"
    with open(os.path.join(MEDIA_DIR, fname), "wb") as f:
        f.write(data)
    return fname


def normalize_table(raw_rows):
    """(header_tuple, data_rows, leading_leftover) from a pdfplumber extract_tables()
    grid. `leading_leftover` is None, or a single row (already through the same
    column corrections as data_rows) that the caller should append onto the
    still-open table's own last row rather than treat as a new row of this table --
    see the comment where it's produced, below.

    Leading rows whose first cell is empty are header continuation fragments
    (a merged/split header cell rendered as extra rows, e.g. "Mandatory /"
    on one row and "Optional" directly below it in the same column) -- they
    get merged column-wise into a single header row rather than kept as
    blank-looking data rows.

    A header cell that needed this row-merge (i.e. its text is taller/wraps
    across the header's own multiple grid rows) throws off pdfplumber's
    column-boundary detection for the *data* rows beneath it: the data that
    actually belongs under that header lands one column to the left instead
    (confirmed on TMFC039's SID ABEs and Overview tables, and its Exposed/
    Dependent APIs tables -- every column whose header needed a row-merge
    has this exact one-column-left data shift; every column whose header
    didn't need one is already correctly aligned). Fixed by recording which
    column indices received a merge, then shifting that data back right
    before reading it as real content -- rather than a blanket "any
    blank-header column merges into its neighbour" rule, which would also
    fire on ordinary spacer columns that are never populated in the first
    place and don't need touching.

    Columns that are empty across the *entire* table (header and every data
    row, after the shift above) are merged-cell artifacts, not real
    columns, and are dropped.

    A table that continues onto a new page can have a leftover, still-
    wrapping line from the *previous* page's last data row appear as its
    own row at the very top of this page's grid, with an empty first cell
    just like a real header-continuation row (confirmed on the Functional
    Framework Functions table's page 2: `['', '', 'or group of products of
    the partner.', '', None, ...]`, the tail end of a Description cell that
    didn't fit on page 1). Treated as a real continuation, this both
    corrupts the header text (already handled by the caller always keeping
    the first clean header seen) and -- the bug this guard actually fixes
    -- wrongly marks that column as "shifted", so a *later* legitimate data
    row's Function Name then gets merged into Function Description instead
    of staying in its own column. Distinguished from a real continuation
    fragment ("Function", "Level 1", "(or set of BEs)") by shape: every
    genuine one seen across this whole document is a short label with no
    sentence-ending punctuation or comma; a leftover wrapped sentence or
    operation-list fragment is neither -- the comma check specifically was
    added after a second, shorter leftover fragment slipped past the length
    check alone (`TMFC002`'s Dependent APIs table: a lone `"Patch,\nDelete"`
    -- the tail of a wrapped Operations cell -- read as short and
    period-free, and wrongly flagged the *Operation* column as shifted,
    which then ate every subsequent row's *Resource* column value).

    Text shape alone still isn't enough -- a *third* leftover fragment
    (`TMFC005`'s Exposed APIs table: a lone `"hub"` / `"POST\nDELETE"` pair,
    the tail of a wrapped Resource/Operations row) is short and free of
    both period and comma, so it also passes the shape check. The check
    that actually catches this one is structural, not textual: every
    genuine multi-row header continuation seen in this whole document
    re-extends the *same* set of column positions on every continuation
    row (e.g. the Functional Framework Functions header's "Aggregate" /
    "Function" / "Level 1" continuation touches columns {4, 7} on both of
    its continuation rows) -- a leftover data row instead touches a
    *different* set of columns unrelated to whichever header cell was
    actually still incomplete (`hub`/`POST DELETE` touches the Resource/
    Operations columns, which round out fine from row 0 alone and were
    never part of any continuation). The first continuation row accepted
    establishes that column set; every later candidate row must match it
    exactly or the continuation loop stops there.
    """
    HEADER_FRAGMENT_MAXLEN = 20

    def looks_like_header_fragment(c):
        return len(c) <= HEADER_FRAGMENT_MAXLEN and "." not in c and "," not in c

    rows = [[(c or "").replace("\n", "<br>").strip() for c in row] for row in raw_rows]
    header = list(rows[0])
    data_start = 1
    shifted_cols = set()
    continuation_col_set = None
    for row in rows[1:]:
        non_empty_idx = [i for i, c in enumerate(row) if c.strip()]
        non_empty = [row[i] for i in non_empty_idx]
        col_set = frozenset(non_empty_idx)
        matches_pattern = continuation_col_set is None or col_set == continuation_col_set
        if non_empty and not row[0].strip() and matches_pattern and all(looks_like_header_fragment(c) for c in non_empty):
            continuation_col_set = col_set
            for i, c in enumerate(row):
                if c.strip():
                    header[i] = f"{header[i]} {c}".strip() if header[i] else c
                    shifted_cols.add(i)
            data_start += 1
        else:
            break
    data_rows = rows[data_start:]
    # A leftover wrapped-continuation-line row that failed the header-fragment check
    # above (see the docstring) still ends up here as a "data" row with only one real
    # cell and nothing else -- in every *wide* table seen in this document (3+ real
    # columns) a genuine data row always populates at least two of them (an id/name
    # plus something else), so requiring >=2 populated cells is a safe way to drop it
    # rather than emitting a near-blank junk row. But a genuinely narrow table (<=2
    # real columns, e.g. TMFC008's SID ABEs table: just "SID ABE Level 1" / "SID ABE
    # Level 2 (or set of BEs)") can have a perfectly legitimate data row that only
    # populates one of its two columns ("Service ABE" with no Level 2 entry) -- the
    # >=2 rule wrongly discarded that single real row down to zero, which silently
    # dropped the whole table (flush_table only emits a table with >=1 data row).
    # Scale the threshold to the header's own real (non-blank) column count instead
    # of hardcoding 2, so this only fires on tables wide enough for it to mean
    # anything.
    min_populated = 1 if sum(1 for c in header if c.strip()) <= 2 else 2
    # The *first* candidate data row on a page is a special case: if it fails the
    # threshold above, it isn't just noise to discard -- it's the tail of the
    # *previous* page's last row, wrapped across the page break, and dropping it
    # silently loses real content instead of merely a junk fragment. Confirmed on
    # TMFC039's own Functional Framework Functions table (the pilot document,
    # already committed): page 7's last row ends "...anomalies for single
    # products", page 8 opens with the leftover `['', '', 'or group of products of
    # the partner.', ...]` -- concatenated, that's the complete, correct sentence.
    # The caller re-attaches this to the still-open table's own last row rather
    # than losing it (see process_table). Only the *first* row gets this
    # treatment: a row failing the threshold deeper in the table is judged as
    # ordinary sparse data instead (the already-established rule right above).
    leading_leftover = None
    if data_rows and 0 < sum(1 for c in data_rows[0] if c.strip()) < min_populated:
        leading_leftover = data_rows[0]
        data_rows = data_rows[1:]
    data_rows = [row for row in data_rows if sum(1 for c in row if c.strip()) >= min_populated]
    # A single-row header (no continuation row at all, so `shifted_cols` above never
    # fires) can still have its own text split across grid columns that don't line up
    # with where pdfplumber puts the data below it -- confirmed on TMFC008's SID ABEs
    # table: header row is `['', 'SID ABE Level 1', '', '', 'SID ABE Level 2 ...', '']`
    # (real labels at columns 1 and 4), but its one data row is `['Service ABE', None,
    # None, '', None, None]` (value at column 0, one column left of the label it
    # belongs under). Detected generally: if a data row's populated columns share
    # nothing with the header's populated columns, but shifting every one of them
    # right by one column lines them up exactly with populated header columns, apply
    # that shift -- the same "one column left" pattern already established for
    # header-continuation rows above, just triggered by column-set mismatch instead
    # of by the continuation-merge bookkeeping (which only exists when the header
    # itself spans more than one grid row).
    # leading_leftover goes through the same column corrections as any other data
    # row (it's a real row, just returned separately) -- processed alongside
    # data_rows here so both end up in the same final column layout.
    shift_rows = data_rows + ([leading_leftover] if leading_leftover is not None else [])
    header_populated = frozenset(i for i, c in enumerate(header) if c.strip())
    for row in shift_rows:
        row_populated = frozenset(i for i, c in enumerate(row) if c.strip())
        if row_populated and not (row_populated & header_populated):
            shifted = frozenset(i + 1 for i in row_populated)
            if shifted <= header_populated:
                for i in sorted(row_populated, reverse=True):
                    row[i + 1] = row[i]
                    row[i] = ""
    for row in shift_rows:
        for i in sorted(shifted_cols):
            if i == 0 or i >= len(row):
                continue
            if row[i - 1].strip():
                row[i] = f"{row[i]} {row[i - 1]}".strip() if row[i] else row[i - 1]
                row[i - 1] = ""
    all_rows = [header] + shift_rows
    ncols = len(header)
    keep_cols = [i for i in range(ncols) if any((r[i] if i < len(r) else "").strip() for r in all_rows)]
    header = tuple(header[i] for i in keep_cols)
    data_rows = [[r[i] if i < len(r) else "" for i in keep_cols] for r in data_rows]
    if leading_leftover is not None:
        leading_leftover = [leading_leftover[i] if i < len(leading_leftover) else "" for i in keep_cols]
    return header, data_rows, leading_leftover


def table_to_markdown(header, data_rows):
    def esc(c):
        return c.replace("|", "\\|") or " "

    lines = ["| " + " | ".join(esc(c) for c in header) + " |"]
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in data_rows:
        lines.append("| " + " | ".join(esc(c) for c in row) + " |")
    return "\n".join(lines)


# --- main pass: page by page, prose (heading/paragraph state machine) interleaved
# with structurally-extracted tables ---
out_lines = []
seen_first_heading = False  # everything before the real "Overview" heading is the title/cover page
drop_until_level = None
max_top_seen = 0  # highest top-level (depth-1) section number accepted as a real heading so far
para_buf = []
open_table = None  # {"header": tuple, "rows": [...]} -- a table that may still continue on the next page
pending_heading = None  # (level, number, title, dropped) -- a heading whose title may wrap onto the next line
# A single bare word, letters/hyphens only, no digits or punctuation -- deliberately
# narrow. A heading title occasionally wraps onto a second physical line as exactly
# one more word ("6. Administrative" / "Appendix" -- confirmed on TMFC005/TMFC006's
# real Administrative Appendix heading, still true even under pdfplumber's extraction,
# which mostly avoids this but not always). A broader "any short line" version of this
# check was tried first and rejected: it also matched genuine short *sentences*
# immediately following a heading (confirmed corrupting TMFC006's "SID ABEs" heading
# with "SID ABEs this component is responsible for are:"). A bare single word is safe
# because a real sentence essentially never reduces to exactly one bare word.
CONTINUATION_WORD_RE = re.compile(r"^[A-Za-z][A-Za-z-]*$")

# A wrapped Operations-cell tail (e.g. "resourceSpecification\n- GET\n- GET/id") can
# land entirely outside its own table's detected bbox when it's the very last row of
# a table that closes at the bottom of a page -- confirmed on TMFC009's Dependent
# APIs table: `find_tables()`'s bbox for the table's last page stops above this
# fragment, so it's never part of the table grid at all (unlike the leftover-header-
# row variant of this same underlying issue, which *is* caught by
# `normalize_table`'s continuation-column-set guard because it's still inside the
# table's own grid). Because it lands in the *prose* stream instead, and the table
# it belongs to is still "open" (accumulating rows across pages, not flushed until
# the next heading/table/image), it also surfaces in the wrong place in `out_lines`
# -- `flush_para()` always runs before `flush_table()` at a heading boundary, so
# this trailing fragment prints *before* the table it trails, not after. Fixing the
# ordering would need buffering table flushes relative to interleaved prose, which
# is a bigger change for no real benefit: the fragment is never legitimate prose in
# either position, only ever the tail of an Operations list. Recognized structurally
# (a "paragraph" that reduces to nothing but bullet + HTTP-verb tokens) and dropped
# outright, the same way a header-continuation fragment is recognized by shape
# elsewhere in this file -- a real sentence never reduces to just this.
OPERATION_FRAGMENT_RE = re.compile(
    r"^(?:[•\-*]?\s*(?:GET|POST|PATCH|PUT|DELETE)(?:\s*/\s*id)?\s*)+$", re.IGNORECASE
)


def flush_para():
    if para_buf:
        joined = " ".join(x for x in para_buf if x)
        if joined and not OPERATION_FRAGMENT_RE.match(joined):
            out_lines.append(joined)
            out_lines.append("")
        para_buf.clear()


def flush_table():
    global open_table
    if open_table and open_table["rows"] and len(open_table["header"]) >= 2:
        out_lines.append(table_to_markdown(open_table["header"], open_table["rows"]))
        out_lines.append("")
    open_table = None


def process_prose_line(raw):
    global seen_first_heading, drop_until_level, max_top_seen, pending_heading
    stripped = raw.strip()
    m = HEADING_RE.match(raw) if stripped else None

    if not seen_first_heading:
        # The "Overview" section is always the first substantive content, but its number
        # isn't fixed -- most components number it "1." (Table of Contents sits outside
        # the numbering), but at least one (TMFC006) numbers Table of Contents itself as
        # "1." and Overview as "2.". Match on the title, not the number, for this reason.
        if m and m.group(2).strip().lower().rstrip(".") == "overview":
            seen_first_heading = True
        else:
            return

    if pending_heading is not None:
        level, number, title, dropped = pending_heading
        pending_heading = None
        if stripped and not m and CONTINUATION_WORD_RE.match(stripped):
            title = f"{title} {stripped}"
            name_key = title.lower().strip(" .")
            if not dropped and name_key in DROP_HEADINGS:
                # The drop/keep decision was made on the first line's title alone --
                # now that the wrap completes it into an actual boilerplate name
                # ("Administrative" + "Appendix"), reverse that decision: un-emit the
                # heading already appended and start dropping from here.
                del out_lines[-2:]
                drop_until_level = level
            elif not dropped:
                out_lines[-2] = f"{'#' * min(level, 6)} {number}. {title}"
            return

    if m and m.group(1).count(".") == 0 and int(m.group(1)) <= max_top_seen:
        # A top-level-shaped line ("1. IG1228: please refer to...") whose number does NOT
        # continue the document's own top-level sequence -- confirmed real on TMFC006,
        # whose References section contains its own restarted "1./2." enumerated list,
        # textually indistinguishable from a genuine heading by HEADING_RE alone.
        m = None

    if m:
        # Table first, then paragraph -- not the other way round. A still-"open" table
        # (accumulating rows across pages, not yet written to out_lines because no
        # incompatible table/image has closed it) can have genuine trailing prose
        # positioned *after* its last row but *before* this heading (confirmed on
        # TMFC003's SID ABEs section: a "Note:" paragraph sits below the SID ABEs
        # table, both on the same page, well before "2.3 eTOM L2 - SID ABEs links";
        # also on TMFC009's Dependent APIs table, where the trailing prose is itself
        # a leftover Operations-cell fragment). That prose is already sitting in
        # `para_buf` by the time this heading is reached, while the table it trails is
        # still waiting in `open_table` -- flushing para before table would print the
        # trailing prose *before* the table it structurally follows, inverting real
        # reading order. Flushing the table first restores it.
        flush_table()
        flush_para()
        level = m.group(1).count(".") + 1
        if level == 1:
            max_top_seen = int(m.group(1))
        title = m.group(2).strip()
        name_key = title.lower().strip(" .")
        if drop_until_level is not None and level <= drop_until_level:
            drop_until_level = None
        if drop_until_level is None and name_key in DROP_HEADINGS:
            drop_until_level = level
            pending_heading = (level, m.group(1), title, True)
            return
        if drop_until_level is not None:
            return
        out_lines.append(f"{'#' * min(level, 6)} {m.group(1)}. {title}")
        out_lines.append("")
        pending_heading = (level, m.group(1), title, False)
        return

    if drop_until_level is not None:
        return

    if not stripped:
        flush_para()
        return

    para_buf.append(stripped)


def not_in_any_table(obj, bboxes):
    x0, top, x1, bottom = obj["x0"], obj["top"], obj["x1"], obj["bottom"]
    for (bx0, btop, bx1, bbottom) in bboxes:
        if x0 >= bx0 - 3 and x1 <= bx1 + 3 and top >= btop - 3 and bottom <= bbottom + 3:
            return False
    return True


def headers_compatible(a, b):
    """True if two page-local header rows are "the same table's header" -- allows for
    one being a prefix/superset of the other's cell text rather than requiring exact
    equality. A table that continues onto a new page re-states its header row, but a
    wrapped data row straddling the page break can bleed leftover text into that
    restated header's last cell (confirmed on TMFC039's Functional Framework Functions
    table: "Function Description" arrives on page 2 as "Function Description or group
    of products of the partner."). Treating these as the same table -- and keeping only
    the *first* (clean) header seen, never the later possibly-corrupted one, see the
    caller -- avoids both fragmenting one logical table into several and ever emitting
    the corrupted version.
    """
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if not x or not y or x == y or x.startswith(y) or y.startswith(x):
            continue
        return False
    return True


def process_prose_text(text):
    for raw in text.split("\n"):
        s = raw.strip()
        if FOOTER_RE.match(s) or PAGE_NUM_RE.match(s) or ID_FOOTER_RE.match(s) or TOC_LEADER_RE.search(raw):
            continue
        process_prose_line(raw)
    flush_para()


def process_table(t):
    global open_table
    # A table on the title/cover page (before "Overview") or inside a dropped section
    # (References' own tables, etc.) is skipped the same way its surrounding prose
    # already is -- table extraction is independent of the prose state machine, so it
    # needs the same two gates applied explicitly.
    if not seen_first_heading or drop_until_level is not None:
        return
    header, data_rows, leading_leftover = normalize_table(t.extract())
    if len(header) < 2:
        # A degenerate single-column "table" -- pdfplumber's find_tables() occasionally
        # detects a stray fragment of wrapped cell text as its own tiny table (confirmed
        # on TMFC039: a spurious one-cell ["Function"] table alongside the real
        # 9-column one, on every page of the Functional Framework Functions section).
        # Never emitted anyway (flush_table's own >=2-column guard), but if not skipped
        # here first it still resets open_table as a side effect, breaking the real
        # table's cross-page continuity every single page.
        return
    if open_table is not None and headers_compatible(open_table["header"], header):
        if leading_leftover is not None and open_table["rows"]:
            # The wrapped tail of the still-open table's own last row, carried
            # across this page break -- append onto that row's cells rather than
            # start a new one (see normalize_table's docstring for why).
            last = open_table["rows"][-1]
            for i, val in enumerate(leading_leftover):
                if val.strip() and i < len(last):
                    last[i] = f"{last[i]}<br>{val}" if last[i] else val
        open_table["rows"].extend(data_rows)  # keep the first (clean) header, not this one
    else:
        flush_table()
        open_table = {"header": header, "rows": data_rows}
        # leading_leftover with no still-open compatible table to attach to is a
        # genuinely orphaned fragment (e.g. the very first table in the document) --
        # nothing to recover it into, so it's dropped, same as before this fix.


def process_image(data, ext):
    # Same two gates as process_table -- a title-page logo or an image sitting inside a
    # dropped section shouldn't be linked into the body just because it happened to
    # survive the hash/size filter.
    if not seen_first_heading or drop_until_level is not None:
        return
    # save_image() is called *before* touching para/table state, not after -- every
    # page carries two logo images that save_image() always filters out (too small /
    # already seen), and flushing the open table for one of those on every single page
    # was silently fragmenting a real multi-page table into one piece per page (found
    # by checking why the Functional Framework Functions table stopped merging after
    # an unrelated fix elsewhere -- this was already broken before that, just masked).
    fname = save_image(data, ext)
    if fname:
        flush_para()
        flush_table()  # a *real* image never sits inside an open table's own row span
        out_lines.append(f"![]({MEDIA_DIR_NAME}/{fname})")
        out_lines.append("")


with pdfplumber.open(SRC) as pdf, open(SRC, "rb") as _f:
    pypdf_pages = PdfReader(_f).pages
    for page, pypdf_page in zip(pdf.pages, pypdf_pages):
        tables = [("table", t.bbox[1], t.bbox[3], t) for t in page.find_tables()]
        # Matched to pypdf's page.images by index -- both libraries walk the same page
        # resource dictionary in the same order (confirmed directly against this
        # component's real PDF); pdfplumber supplies the position, pypdf the already-
        # decoded bytes (see the module docstring for why the split).
        #
        # Pre-filtered by size here, not just later in save_image() -- a logo image's
        # bounding box can vertically overlap real heading/body text above or below it
        # (confirmed on TMFC006 page 4: a 9KB header logo's bbox runs from y=6 to
        # y=79, overlapping the "2. Overview" heading that starts at y=78). Including
        # it in the interleaving cursor still advances the cursor past the heading's
        # own start position even though the image itself is never saved, and
        # `within_bbox`'s strict containment then silently drops that heading's text
        # entirely from every subsequent slice -- corrupting the whole document (empty
        # body, since "seen_first_heading" then never becomes true). A discarded logo
        # should never affect prose slicing at all, so it's excluded before the sort,
        # not just before being written to media/.
        images = [
            ("image", im["top"], im["bottom"], pypdf_page.images[i])
            for i, im in enumerate(page.images)
            if i < len(pypdf_page.images) and len(pypdf_page.images[i].data) >= MIN_IMAGE_BYTES
        ]
        items = sorted(tables + images, key=lambda it: it[1])
        bboxes = [it[3].bbox for it in items if it[0] == "table"]
        filtered = page.filter(lambda obj: not_in_any_table(obj, bboxes)) if bboxes else page

        # Interleave in true top-to-bottom reading order, not "all this page's prose,
        # then all its tables/images" -- a table (or image) and a section-transition
        # heading can share one page (confirmed on TMFC039: "3.1 Exposed APIs"'s own
        # continuation table and the "3.2 Dependent APIs" heading both fall on page 13)
        # and processing them out of order silently attaches content to the wrong
        # section. Slice the page at each item's vertical extent and process
        # prose-then-item-then-prose... in that order.
        cursor = 0.0
        for kind, top, bottom, obj in items:
            if top > cursor:
                process_prose_text(filtered.within_bbox((0, cursor, page.width, top)).extract_text() or "")
            if kind == "table":
                process_table(obj)
            else:
                ext = os.path.splitext(obj.name)[1].lstrip(".") or "png"
                process_image(obj.data, ext)
            cursor = max(cursor, bottom)
        if cursor < page.height:
            process_prose_text(filtered.within_bbox((0, cursor, page.width, page.height)).extract_text() or "")

flush_para()
flush_table()

body_md = "\n".join(out_lines)
body_md = re.sub(r"\n{3,}", "\n\n", body_md).strip() + "\n"

envelope = {
    "id": ID,
    "type": "component",
    "name": NAME,
    "version": VERSION,
    "status": STATUS,
    "source": {
        "origin": PDF_URL,
        "license": "RAND",
        "retrieved": _dt.date.today().isoformat(),
        "sha256": hashlib.sha256(open(SRC, "rb").read()).hexdigest(),
        "raw_path": SRC.replace("\\", "/"),
    },
    "links": {"apis": [], "use_cases": []},  # filled in by build_index.py's sync_component_links() -- spec/spec-components.md 4
}

meta_path = os.path.join(os.path.dirname(OUT), "component.meta.json")
yaml_spec_version = None
if os.path.exists(meta_path):
    with open(meta_path, encoding="utf-8") as f:
        yaml_spec_version = json.load(f).get("version")

extension = {"yaml_spec_version": yaml_spec_version or "TODO"}

frontmatter_data = {**envelope, **extension}
yaml_lite.write(OUT, frontmatter_data, body_md)

print(f"Wrote {OUT} ({len(body_md)} chars body, {img_counter} unique images)")
if yaml_spec_version and yaml_spec_version != VERSION:
    print(f"NOTE: version drift -- component.yaml is v{yaml_spec_version}, this PDF is v{VERSION} (expected, see spec/spec-components.md 5)")
