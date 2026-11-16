"""Pull out the parts of an extracted document that the six references need,
so the whole text doesn't have to be read.

Reads the files extract_docx.py wrote to <output-dir> and writes
<output-dir>/key_extracts.txt (and prints it):

  1. Notice and licence lines: copyright, "All Rights Reserved", IPR mode,
     licence names (IPR Policy §14; also where a file label would sit).
  2. The Acknowledgements and contributors section (who the authors and
     contributors are, which companies contributed).
  3. Credited text: each source in cited.txt with how many passages cite it.
  4. Outside links: external hyperlinks grouped by host, TM Forum's own
     hosts counted apart.
  5. Statements about AI use: generative AI, chat assistants, "AI-assisted".
  6. Open-source and licence mentions: software, code, SBOM, licence names
     (relevant to the OpenChain, SPDX and REUSE references).

Each extract carries the line number in text.txt, so a reader can open the
context when an extract isn't enough. This is a guide to where to look, not
a check: a line the patterns miss is not shown. Read the full text only
where an extract points to something that needs it.

Usage:
  python -I key_extracts.py <output-dir>
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
from urllib.parse import urlparse

NOTICE = re.compile(r"©|\(c\)\s*\d{4}|copyright|all rights reserved|IPR\s*mode|RAND|royalty|licen[cs]e|"
                    r"apache|FORUM click|FCTL", re.I)
ACK = re.compile(r"^\s*(?:\d+(?:\.\d+)*\.?\s*)?(acknowledg(?:e)?ments?|contributors?|authors?)\b", re.I)
AI = re.compile(r"generative\s+ai|\bgenai\b|chatgpt|\bgpt-?\d|claude|copilot|gemini|\bllm\b|large language model|"
                r"ai[- ]assisted|ai[- ]generated|prepared with the help of|drafted (?:with|using)", re.I)
OSS = re.compile(r"open[- ]source|\bSBOM\b|\bSPDX\b|\bREUSE\b|\bGPL\b|\bMIT licen|apache[- ]2|github\.com|"
                 r"\bsoftware component|source code|third[- ]party (?:software|librar)", re.I)
TMF_HOSTS = ("tmforum.org", "projects.tmforum.org", "github.com/tmforum", "tmforum-oda")


def lines_of(path):
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read().splitlines()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("--max", type=int, default=25, help="most lines shown per extract")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    text = lines_of(os.path.join(a.outdir, "text.txt"))
    headers = lines_of(os.path.join(a.outdir, "headers.txt"))
    out = []

    def section(title, rows, note=""):
        out.append("## %s" % title)
        if note:
            out.append(note)
        out.extend(rows if rows else ["(none found)"])
        out.append("")

    def first(pattern, source, label=None):
        rows, seen = [], set()
        for n, l in enumerate(source, 1):
            if pattern.search(l):
                key = re.sub(r"\s+", " ", l.strip())[:120]
                if key in seen:
                    continue
                seen.add(key)
                rows.append("%s%d: %s" % (label or "text.txt:", n, re.sub(r"\s+", " ", l.strip())[:220]))
        return rows

    rows = first(NOTICE, headers, "headers.txt:")[:8] + first(NOTICE, text)[:a.max]
    section("1. Notice and licence lines", rows)

    ack = []
    for n, l in enumerate(text):
        if ACK.match(l) and len(l.split()) <= 6 and n > len(text) * 0.5:
            ack = ["text.txt:%d: %s" % (n + i + 1, re.sub(r"\s+", " ", t.strip())[:200])
                   for i, t in enumerate(text[n:n + 70]) if t.strip()]
            break
    section("2. Acknowledgements and contributors (first 70 lines of the section, from the second half of the text)",
            ack[:70])

    cited = {}
    for l in lines_of(os.path.join(a.outdir, "cited.txt")):
        if " | " in l:
            src = l.split(" | ", 1)[0].strip()
            cited[src] = cited.get(src, 0) + 1
    section("3. Credited text (from cited.txt)", ["%d passage(s) credited to %s" % (n, s[:150]) for s, n in cited.items()])

    hosts_out, hosts_tmf = {}, 0
    for l in lines_of(os.path.join(a.outdir, "hyperlinks.txt")):
        u = l.strip()
        if not u.lower().startswith("http"):
            continue
        host = urlparse(u).netloc.lower()
        if any(t in (host + urlparse(u).path.lower()) for t in TMF_HOSTS):
            hosts_tmf += 1
        else:
            hosts_out[host] = hosts_out.get(host, 0) + 1
    rows = ["%d link(s) to %s" % (n, h) for h, n in sorted(hosts_out.items(), key=lambda kv: -kv[1])]
    section("4. Outside links (TM Forum's own hosts: %d link(s), not listed)" % hosts_tmf, rows[:a.max])

    section("5. Statements about AI use", first(AI, text)[:a.max])
    section("6. Open-source and licence mentions", first(OSS, text)[:a.max])

    body = "\n".join(out)
    with open(os.path.join(a.outdir, "key_extracts.txt"), "w", encoding="utf-8") as f:
        f.write(body + "\n")
    print(body)


if __name__ == "__main__":
    main()
