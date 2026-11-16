"""Find passages a draft shares word for word with a set of source documents.

Breaks the draft and every source into overlapping runs of N words
(default 8), after lower-casing and stripping punctuation, and reports each
stretch of the draft that shares runs with a source. Overlapping and
adjacent runs are merged, so one copied paragraph is one finding.

Usage:
  python -I copy_check.py <draft> <sources-dir> [--n 8] [--min-words 12]

<draft>        a .txt or .md file, e.g. text.txt from extract_docx.py
<sources-dir>  folder of source documents: .txt, .md, .docx, and .pdf if
               PyMuPDF is installed. Searched recursively.
--n            run length in words (default 8)
--min-words    only report stretches at least this long (default 12)

Prints a Markdown report: one entry per matched stretch, longest first,
with the source file, the length in words and the draft text.
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
import zipfile

WORD = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")
FOLD = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                      "–": "-", "—": "-", " ": " "})


def docx_text(path):
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
    return "\n".join("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p)) for p in paras)


def pdf_text(path):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None
    with fitz.open(path) as d:
        return "\n".join(page.get_text() for page in d)


def read_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".txt", ".md"):
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    if ext == ".docx":
        return docx_text(path)
    if ext == ".pdf":
        return pdf_text(path)
    return None


def tokens(text):
    """Return (normalised words, character offset of each word in text)."""
    folded = text.translate(FOLD).lower()
    words, offsets = [], []
    for m in WORD.finditer(folded):
        words.append(m.group())
        offsets.append((m.start(), m.end()))
    return words, offsets


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("sources")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--min-words", type=int, default=12)
    a = ap.parse_args()
    if not os.path.isdir(a.sources):
        sys.exit("copy_check.py: cannot run: held-sources folder not found: %s. The copied-text check is not "
                 "done; report it as not checked, not as 'no shared stretches'." % a.sources)
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to a legacy code page

    draft_text = read_text(a.draft)
    if draft_text is None:
        sys.exit("Can't read the draft: %s" % a.draft)
    dwords, doffs = tokens(draft_text)

    # Index the draft's runs: run -> list of start positions.
    index = {}
    for i in range(len(dwords) - a.n + 1):
        index.setdefault(tuple(dwords[i:i + a.n]), []).append(i)

    skipped, findings = [], []
    for root, _, files in os.walk(a.sources):
        for name in sorted(files):
            path = os.path.join(root, name)
            text = read_text(path)
            if text is None:
                skipped.append(os.path.relpath(path, a.sources))
                continue
            swords, _ = tokens(text)
            hit = [False] * len(dwords)
            for j in range(len(swords) - a.n + 1):
                for i in index.get(tuple(swords[j:j + a.n]), ()):
                    for k in range(i, i + a.n):
                        hit[k] = True
            i = 0
            while i < len(dwords):
                if not hit[i]:
                    i += 1
                    continue
                start = i
                while i < len(dwords) and hit[i]:
                    i += 1
                if i - start >= a.min_words:
                    findings.append((i - start, os.path.relpath(path, a.sources),
                                     draft_text[doffs[start][0]:doffs[i - 1][1]]))

    findings.sort(key=lambda f: -f[0])
    print("# Copied-text check\n")
    print("Draft: `%s`  \nSources: `%s`  \nRun length: %d words; reporting stretches of %d+ words.\n"
          % (a.draft, a.sources, a.n, a.min_words))
    if not findings:
        print("No shared stretches found.\n")
    for n, (length, src, text) in enumerate(findings, 1):
        print("## %d. %d words shared with `%s`\n" % (n, length, src))
        print("> " + " ".join(text.split()) + "\n")
    if skipped:
        print("## Not checked\n")
        print("These source files couldn't be read (unsupported type, or a PDF without PyMuPDF installed):\n")
        for s in skipped:
            print("- `%s`" % s)


if __name__ == "__main__":
    main()
