# ODA ID Registry

A static glossary, not generated — see `spec/spec.md` §4.1. If an ID prefix shows up that isn't
listed here, that's a sign the scope of this repo has grown and this file needs an entry added,
not that the ID is invalid.

| Prefix | Means | Example | Where it lives |
|---|---|---|---|
| `IGxxxx` | Introductory Guide (often an index/inventory doc) | `IG1228` | not vendored in full; only its extracted matrix is (`knowledge/index/usecase-component-matrix.json`) |
| `TMFSxxx` | Standalone Use Case | `TMFS001` | `knowledge/use-cases/TMFSxxx/` |
| `TMFCxxx` | ODA Component | `TMFC020` | `knowledge/components/TMFCxxx/` |
| `TMFxxx` | TM Forum Open API | `TMF632` | `knowledge/apis/TMFxxx/` |
| `GBxxx` | Guidebook (eTOM = GB921, SID = GB922) | `GB921` | `GB921` (eTOM) → `knowledge/etom/` (spec-etom.md); `GB922` (SID) still reserved, spec.md §7 |

Note the `TMFCxxx` / `TMFxxx` distinction: a Component ID always has the `C` (`TMFC020`); an API ID
never does (`TMF632`). `tools/docx2md.py`'s reference parser relies on exactly this to tell them
apart in prose that names both (`API_ID_RE` uses a negative lookahead, `TMF(?!C)\d+`, for this
reason — see the comment there).
