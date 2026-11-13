"""Clear failures when the skill runs without the IP-scan-tool repository.

Every script in this folder imports this module first and calls install().
It replaces Python's traceback, for the errors a missing or partial copy
causes, with one line saying what is missing and what to do:

  - a file or folder that isn't there (the document, an extract file such as
    text.txt, entry.json, editorial.json, or the skill's own references/);
  - a Python package that isn't installed;
  - a .docx or .xlsx that isn't a valid Office file, or a JSON file that
    can't be read.

Other errors keep their normal traceback, since they are bugs, not setup.

sources() checks a --sources folder. A missing folder is reported, never
treated as a folder with nothing in it: "no matches" and "not checked" are
different findings, and the report must say which.
"""

import json
import os
import sys
import zipfile

SKILL_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REFERENCES = os.path.join(SKILL_DIR, "references")

PACKAGES = {"docx": "python-docx", "PIL": "Pillow", "fitz": "PyMuPDF", "numpy": "numpy",
            "openpyxl": "openpyxl"}

EXTRACT_FILES = {"text.txt", "cited.txt", "images.txt", "hyperlinks.txt", "headers.txt",
                 "notes.txt", "key_extracts.txt", "image_flags.txt"}


def _script():
    return os.path.basename(sys.argv[0]) if sys.argv and sys.argv[0] else "script"


def _hint(path):
    full = os.path.normpath(os.path.abspath(path))
    name = os.path.basename(full)
    if full.startswith(REFERENCES + os.sep) or full == REFERENCES:
        return ("The skill's references/ folder is missing or incomplete. Copy the whole "
                "'%s' folder (scripts/ and references/ together); the scripts need "
                "the reference files to score." % os.path.basename(SKILL_DIR))
    if name in EXTRACT_FILES:
        return ("Run extract_docx.py (or extract_xlsx.py, or pdf_to_docx.py then extract_docx.py) "
                "on the document into this output folder first.")
    if name == "entry.json":
        return "Write entry.json in the document's folder first (see 'Document score and entry.json' in SKILL.md)."
    if name == "editorial.json":
        return "Write editorial.json in the document's folder first (see 'Editorial consistency' in SKILL.md)."
    if name.lower().endswith((".docx", ".xlsx", ".pdf")):
        return ("Check the document's path. In entry.json, 'docx' is relative to the folder entry.json is in; "
                "outside the IP-scan-tool repository it may need changing.")
    return "Check the path; outside the IP-scan-tool repository, folders such as work/documents/ may not exist yet."


def describe(etype, e):
    """One-line explanation for a setup error, or None for anything else."""
    if issubclass(etype, FileNotFoundError):
        path = os.path.normpath(e.filename) if e.filename else ""
        return "not found: %s. %s" % (path, _hint(path))
    if issubclass(etype, NotADirectoryError):
        return "expected a folder, got a file: %s." % (e.filename or "")
    if issubclass(etype, PermissionError):
        return "no permission to read or write %s (is it open in another program?)." % (e.filename or "")
    if issubclass(etype, ModuleNotFoundError):
        mod = (e.name or "").split(".")[0]
        pkg = PACKAGES.get(mod, mod)
        return "needs the Python package '%s' (pip install %s)." % (pkg, pkg)
    if issubclass(etype, zipfile.BadZipFile):
        return "the file is not a valid .docx or .xlsx (Office files are zip packages): %s." % e
    if issubclass(etype, json.JSONDecodeError):
        return "a JSON file can't be read (%s). If it is entry.json or editorial.json, check its syntax." % e
    return None


def _hook(etype, e, tb):
    msg = describe(etype, e)
    if msg is None:
        sys.__excepthook__(etype, e, tb)
        return
    print("%s: cannot run: %s" % (_script(), msg), file=sys.stderr)


def install():
    sys.excepthook = _hook


def sources(path):
    """Return path when it is a folder; otherwise say so and return None."""
    if not path:
        return None
    if os.path.isdir(path):
        return path
    print("%s: WARNING: held-sources folder not found: %s. Nothing is compared word for word with held "
          "sources, and publication dates aren't read from them. Report those checks as not done, not "
          "as 'no matches'." % (_script(), path), file=sys.stderr)
    return None


def warn(message):
    print("%s: WARNING: %s" % (_script(), message), file=sys.stderr)
