"""List sentences from a draft that are worth a quoted web search.

Skips sentences that are TM Forum's own text, because a web search for
them only finds TM Forum's pages again. A sentence counts as TM Forum's
own when at least half of its 8-word runs appear in the exclude folders
(by default, the skill's own references folder, which holds the IPR
Policy copy; pass --exclude for more, such as a clone of
TMForum-ODA-Component_Development). Files that are versions of the draft
itself, such as earlier IG1242 releases, are not used for excluding, or
every sentence would be skipped. The default is never the whole
repository this skill sits in: its source documents, reports and working
files quote the drafts being checked, and would hide every sentence.

From what is left it prefers general-purpose prose, because that is
what gets copied from outside: a sentence full of project-specific
terms (file paths, tool and repo names like component-specification-
studio, IDs like TMFC001, acronyms, product names) describes this
project and won't be found elsewhere. Sentences are ranked by how few
such terms they have, then definitions ("X is a ...", "refers to", "is
defined as", "means") ahead of other sentences, then longest first.
Each line is ready to paste into a search engine in quotation marks.

The other candidates come in batches, so a clean document costs fewer
searches: search batch 1 (7 sentences by default); only if one of them
matches, search batch 2 (8 more); only if one of those matches, search the
rest (up to --count in all). Matches cluster in some documents and most
documents have none, so a first batch with no match is a reason to stop.

Before those, it lists every passage in cited.txt (written by
extract_docx.py next to text.txt): text the draft credits to an outside
source. They are grouped by source: open each credited source once (fetch
its page or document) and compare all of its passages with it, instead of
searching each passage. Credited text is the likeliest to be reproduced
from its source, so every credited passage is compared, whatever its
wording; they don't count towards --count.

Usage:
  python -I spot_check_candidates.py <draft.txt> [--count 20] [--batches 7,8]
         [--exclude <dir-or-file> ...] [--no-exclude] [--cited <file>]

--exclude     folder or file of TM Forum's own text; repeatable. Replaces
              the default (the skill's references folder).
--no-exclude  don't skip anything; pick from every sentence.
--batches     sizes of the first batches of other candidates (default 7,8);
              what is left of --count follows in a last batch.
--cited       cited-text file; default cited.txt next to the draft, if any.
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

N = 8
DEFINITION = re.compile(r"\b(is an?|is the|refers to|is defined as|means|is responsible for)\b", re.I)
SENTENCE = re.compile(r"(?<=[.!?])\s+")
WORD = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")
TEXT_EXT = (".yaml", ".yml", ".md", ".txt")
SKIP_DIRS = {".git", "node_modules"}
DRAFT_COPY = 0.25  # a file sharing this share of the draft's runs is a version of it
PER_PHRASE = 2  # most definitions picked per defining phrase
MIN_WORDS, MAX_WORDS = 10, 40
MAX_SENTENCES = 6  # most sentences listed from one credited passage
# A word is project-specific if it looks like code or a path (has - _ / .
# < > @ or a digit), is camelCase or mixed-case (TMForum, GitHub), or is an
# acronym (YAML, CTK). A capitalised word mid-sentence (a product or team
# name) counts half, since ordinary prose has some of those.
CODE_LIKE = re.compile(r"[-_/.<>@\\]|\d|[a-z][A-Z]|^[A-Z]{2,}$")
EDGE = "\"'()[]{},;:!?“”‘’"


STOP = set("""a an the and or but if of to in on at by for with from as into onto than then
so that this these those it its is are was were be been being has have had do does did not no
can could will would should may might must shall which who whom whose what when where why how
all any each every both either neither other such only own same very more most also just there
their they them we our you your he she his her one two three via per before after once while
""".split())
DOC_TERM_MIN = 5  # a word used this often in the draft is the document's own vocabulary


def content_words(text):
    return [w for w in WORD.findall(text.lower().replace("’", "'")) if len(w) > 2 and w not in STOP]


def specificity(sentence, doc_terms=frozenset()):
    """How much the sentence is about this project, 0.0 (general) upwards.

    Adds the share of words that look like code, paths, IDs or names to the
    share of content words that are the document's own vocabulary (used
    DOC_TERM_MIN+ times in the draft). Text copied in from elsewhere tends
    to use words the rest of the document doesn't.
    """
    words = sentence.split()
    score = 0.0
    for i, raw in enumerate(words):
        w = raw.strip(EDGE).rstrip(".")
        if not w:
            continue
        if CODE_LIKE.search(w):
            score += 1
        elif i > 0 and w[0].isupper():
            score += 0.5
    content = content_words(sentence)
    own = sum(w in doc_terms for w in content) / len(content) if content else 1.0
    return score / len(words) + own


def runs(text):
    w = WORD.findall(text.lower().replace("’", "'"))
    return [hash(tuple(w[i:i + N])) for i in range(len(w) - N + 1)]


def default_exclude():
    """The skill's own references (the IPR Policy copy): TM Forum text that ships with the skill."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")


def files_under(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if f.lower().endswith(TEXT_EXT):
                    yield os.path.join(root, f)


def own_runs(draft_runs, paths):
    """Return the draft's runs found in the exclude files, and the draft copies skipped."""
    found, copies = set(), []
    for path in files_under(paths):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                shared = draft_runs.intersection(runs(f.read()))
        except OSError:
            continue
        if draft_runs and len(shared) / len(draft_runs) >= DRAFT_COPY:
            copies.append(path)
        else:
            found |= shared
    return found, copies


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--exclude", action="append")
    ap.add_argument("--no-exclude", action="store_true")
    ap.add_argument("--cited")
    ap.add_argument("--batches", default="7,8", help="sizes of the first batches of other candidates")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to a legacy code page

    cited = a.cited or os.path.join(os.path.dirname(os.path.abspath(a.draft)), "cited.txt")
    if os.path.isfile(cited):
        with open(cited, encoding="utf-8") as f:
            entries = [l.rstrip("\n").split(" | ", 1) for l in f if " | " in l]
        by_source = {}
        for source, passage in entries:
            by_source.setdefault(source.strip(), []).append(passage)
        print("# Credited to an outside source: %d passages from %d sources (from %s)."
              " Open each source once and compare all its passages with it:" % (len(entries), len(by_source), cited))
        for source, passages in by_source.items():
            print("## %s (%d passage%s)" % (source, len(passages), "" if len(passages) == 1 else "s"))
            for passage in passages:
                # Every sentence of the passage is listed (up to MAX_SENTENCES), not only the
                # first: a credited block of several copied sentences needs each compared.
                chunks, cur = [], ""
                for sent in SENTENCE.split(passage):
                    cur = (cur + " " + sent).strip()
                    if len(cur.split()) >= MIN_WORDS:
                        chunks.append(cur)
                        cur = ""
                if cur:
                    chunks.append(cur) if not chunks else chunks.__setitem__(-1, chunks[-1] + " " + cur)
                for chunk in chunks[:MAX_SENTENCES]:
                    print('"%s"' % " ".join(chunk.split()[:32]))
                if len(chunks) > MAX_SENTENCES:
                    print("(+%d more sentence(s) in this passage)" % (len(chunks) - MAX_SENTENCES))
        print("# Other candidates, in batches:")

    with open(a.draft, encoding="utf-8", errors="replace") as f:
        text = f.read()
    seen, sentences = set(), []
    for line in text.splitlines():
        for s in SENTENCE.split(line.strip()):
            s = " ".join(s.split())
            if MIN_WORDS <= len(s.split()) <= MAX_WORDS and s.lower() not in seen:
                seen.add(s.lower())
                sentences.append(s)

    skipped = 0
    if not a.no_exclude:
        paths = a.exclude or [default_exclude()]
        for p in paths:
            if not os.path.exists(p):
                graceful.warn("exclude path not found: %s. Sentences from TM Forum's own text there are not "
                              "skipped, so the list may include them." % p)
        if not a.exclude:
            print("# Only the skill's references are used as TM Forum's own text."
                  " Pass --exclude <folder> (for example a clone of TMForum-ODA-Component_Development) to skip more.")
        found, copies = own_runs(set(runs(text)), paths)
        kept = []
        for s in sentences:
            r = runs(s)
            if r and sum(x in found for x in r) / len(r) >= 0.5:
                skipped += 1
            else:
                kept.append(s)
        sentences = kept
        print("# Skipped %d sentences found in TM Forum's own text (%s)." % (skipped, "; ".join(paths)))
        for c in copies:
            print("# Not used for excluding (a version of the draft): %s" % c)

    # Most general first (specificity in steps of 0.1, so a sentence isn't
    # passed over for a tiny difference), then definitions, then longest.
    # At most PER_PHRASE definitions per defining phrase count as
    # definitions, so a document built from one template ("X component is
    # responsible for") doesn't fill the list.
    counts = {}
    for w in content_words(text):
        counts[w] = counts.get(w, 0) + 1
    doc_terms = frozenset(w for w, c in counts.items() if c >= DOC_TERM_MIN)
    per_phrase, ranked = {}, []
    for s in sentences:
        m = DEFINITION.search(s)
        phrase = m.group(1).lower() if m else None
        is_def = bool(phrase) and per_phrase.get(phrase, 0) < PER_PHRASE
        if is_def:
            per_phrase[phrase] = per_phrase.get(phrase, 0) + 1
        ranked.append((int(specificity(s, doc_terms) * 10), not is_def, -len(s), s))
    ranked.sort()
    picked = [r[3] for r in ranked[:a.count]]
    if not picked:
        print("# No sentences left to check.")
    sizes = [int(x) for x in a.batches.split(",") if x.strip()]
    sizes.append(max(0, len(picked) - sum(sizes)))
    pos = 0
    for n, size in enumerate(sizes, 1):
        batch = picked[pos:pos + size]
        pos += size
        if not batch:
            continue
        rule = ("search these first" if n == 1 else
                "search only if batch %d had a match" % (n - 1))
        print("# Batch %d (%d sentences; %s):" % (n, len(batch), rule))
        for s in batch:
            # Search engines cap query length; the first 32 words are enough to match.
            print('"%s"' % " ".join(s.split()[:32]))


if __name__ == "__main__":
    main()
