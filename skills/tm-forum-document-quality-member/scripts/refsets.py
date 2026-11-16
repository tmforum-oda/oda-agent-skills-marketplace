"""Which reference sets a document is scored against.

Word documents (and documents read from a PDF) are scored against the sets in
references/. Spreadsheets (.xlsx records, whose extract writes source_format.txt
"xlsx") are scored against the sets in references/spreadsheet/, built from the
spreadsheets alone, because per-1,000-word rates, AI-wording signs and
editorial findings in cell text aren't comparable with those of prose. A
spreadsheet set that hasn't been built falls back to the Word set of the same
name.

Scripts call use(kind) or use_for(doc_dir) before loading a set, and load it
with path(name).
"""

import json
import os

REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")
SPREADSHEET_DIR = os.path.join(REF, "spreadsheet")
KINDS = ("word", "xlsx")

_kind = ["word"]
_listeners = []


def use(kind):
    if kind not in KINDS:
        raise ValueError("unknown reference kind: %s" % kind)
    if _kind[0] != kind:
        _kind[0] = kind
        for f in _listeners:
            f()


def current():
    return _kind[0]


def on_change(f):
    """Call f() whenever the kind changes (for scripts that cache a loaded set)."""
    _listeners.append(f)


def path(name, kind=None, for_write=False):
    kind = kind or _kind[0]
    if kind == "xlsx":
        p = os.path.join(SPREADSHEET_DIR, name)
        if for_write or os.path.exists(p):
            return p
    return os.path.join(REF, name)


def has_own_set(name, kind=None):
    """Whether this kind has its own set of that name (not the Word fallback)."""
    kind = kind or _kind[0]
    return kind == "word" or os.path.exists(os.path.join(SPREADSHEET_DIR, name))


def kind_of_dir(doc_dir):
    """"xlsx" when the record's extract says its source was a spreadsheet, else "word".
    doc_dir is the record folder (with entry.json) or the extract folder itself."""
    d = doc_dir
    entry = os.path.join(doc_dir, "entry.json")
    if os.path.exists(entry):
        with open(entry, encoding="utf-8") as f:
            d = os.path.normpath(os.path.join(doc_dir, json.load(f).get("dir", ".")))
    marker = os.path.join(d, "source_format.txt")
    if os.path.exists(marker):
        with open(marker, encoding="utf-8") as f:
            if f.read().strip() == "xlsx":
                return "xlsx"
    return "word"


def use_for(doc_dir):
    use(kind_of_dir(doc_dir))
