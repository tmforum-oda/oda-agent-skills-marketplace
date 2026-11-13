"""Score the signs that a document, or parts of it, were produced with
GenAI. It measures indicators, not proof: AI-text detection is unreliable,
flags human writing (especially non-native English) and misses edited AI
text. Every point in the score is tied to evidence a reviewer can check.

Signs, strongest first:
  1. Leftover assistant text: chat-style lines such as "I hope this
     helps", "as an AI", "I have the ... from earlier", or chat citation
     artefacts ("oaicite", "turn0search", "【...】").           5 points each
  2. AI provenance in the file's metadata: in a picture file, C2PA /
     Content Credentials, the IPTC "trainedAlgorithmicMedia" source type,
     or a generator's name (DALL-E, Midjourney, Firefly, Stable Diffusion,
     Imagen, Napkin...); in the document's own properties (docProps
     core.xml, app.xml, custom.xml: creator, last modified by, application,
     custom properties), an AI tool's name (ChatGPT, OpenAI, Claude,
     Anthropic, Copilot, Gemini...).              5 points per picture, 5 for the properties
  3. Figures whose labels contradict the text (from the visual image
     check; pass --figure-mismatches N).        counted and reported, 0 points
     A label that contradicts the text shows that a figure and its text
     disagree, not who or what wrote them, so it is reported as its own
     measure (the Figure labels column of the reports), not scored here.
  4. Style shift: long paragraphs (40+ words) with at least two AI-typical
     words, at 4 or more per 100 words and three times the rest of the
     document's rate.                                             10 x share of long paragraphs
  5. Wording: AI-typical words and phrases per 1,000 words, and em dashes
     per 1,000 words.                                             1 x rate, 0.2 x rate
Signs 1 and 2 are capped at 4 occurrences each.

The score is classed by its rank against the reference set in
references/ai-indicators-reference.json (class_rule): low is at or below
the score that ends the reference set's bottom quarter, high at or above the
score that starts its top fifth, medium in between. (The scores pile up at
zero, so sigma is larger than the mean and mean +/- k*sigma said little.)
z against the mean and sigma is still given, for context and the author
table.
Any occurrence of sign 1 or sign 2 makes the class "high" whatever the
score, because those are close to direct evidence.

Usage:
  python -I ai_indicators.py <output-dir> [--docx <input.docx>] [--figure-mismatches N]
  python -I ai_indicators.py --reference
<output-dir> is the folder extract_docx.py wrote (text.txt, media/).
--docx also scans the picture files inside the .docx (same as media/) and
the document's properties; without it the properties aren't checked.
Writes <output-dir>/ai_indicators.txt and prints the same report.
"""

import os  # noqa: E402
import sys  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves the script's folder off the path
import graceful  # noqa: E402  (clear messages when files, folders or packages are missing)
graceful.install()
import argparse
import json
import math
import os
import re
import statistics
import struct
import sys
import zipfile
import zlib

REFERENCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "ai-indicators-reference.json")

ASSISTANT = re.compile("|".join([
    # Only the assistant's self-description: "as an AI Model Catalog" is ordinary text.
    r"\bas an ai(?: (?:language model|assistant)\b|,)", r"\bas a (large )?language model\b", r"\bi hope this helps\b",
    r"\blet me know if you\b", r"\bwould you like me to\b", r"\bfeel free to (ask|let me)\b",
    r"\bhere(?:'s| is) (?:a|an|the) (?:revised|updated|rewritten|draft|summary|version)\b",
    r"\b(?:certainly|sure|absolutely)[!,] here\b", r"\bgreat question\b",
    r"\bi (?:have|had) the .{1,60} from earlier\b", r"\bfrom (?:our|the) (?:earlier|previous) (?:conversation|chat)\b",
    r"\bi (?:can(?:no|')t|cannot|am unable to) (?:browse|access|verify)\b",
    r"\bmy (?:knowledge )?cut-?off\b", r"\bregenerate response\b",
    r"oaicite", r"contentreference\[", r"turn\d+(?:search|view|news)\d+", r"【[^】]{0,40}】",
]), re.I)

PROVENANCE = [b"c2pa", b"jumb", b"contentcredentials", b"trainedAlgorithmicMedia", b"compositeWithTrainedAlgorithmicMedia",
              b"DALL-E", b"DALL\xc2\xb7E", b"Midjourney", b"Adobe Firefly", b"Stable Diffusion", b"stability.ai",
              b"OpenAI", b"ChatGPT", b"Imagen", b"Gemini", b"SynthID", b"Napkin", b"Leonardo.Ai", b"Ideogram"]

# AI tool names in the document's properties. "Claude" counts only as the whole value (with an
# optional "Anthropic" and product words), so a person called "Claude Martin" isn't flagged.
PROPERTY_TOOLS = re.compile(r"\b(?:ChatGPT|OpenAI|GPT-?[345](?:\.\d)?o?|Anthropic|Copilot|Gemini|Google Bard|"
                            r"Perplexity|Mistral AI|DeepSeek|Grok|Jasper AI|Writesonic|Claude\.ai|"
                            # openpyxl, the Python library AI tools use to write workbooks, puts its own name in
                            # the creator field: the file was generated by a script, not saved from Excel.
                            r"openpyxl)\b", re.I)
PROPERTY_CLAUDE = re.compile(r"(?:Anthropic\s+)?Claude(?:\s+(?:AI|Code|Desktop|Opus|Sonnet|Haiku|Fable|\d[\w.]*))*",
                             re.I)
PROPERTY_PARTS = ("docProps/core.xml", "docProps/app.xml", "docProps/custom.xml")
PROPERTY_SHOWN = ("creator", "lastModifiedBy", "Application", "revision", "created", "modified")

AI_WORDS = re.compile(r"\b(" + "|".join([
    r"delve[sd]?", r"delving", r"seamless(?:ly)?", r"leverag(?:e|es|ed|ing)", r"robust(?:ness)?",
    r"streamlin(?:e|es|ed|ing)", r"comprehensive", r"pivotal", r"foster(?:s|ed|ing)?", r"holistic(?:ally)?",
    r"empower(?:s|ed|ing|ment)?", r"cutting-edge", r"game-?changer", r"transformative", r"synerg(?:y|ies|istic)",
    r"paradigm", r"unlock(?:s|ed|ing)?", r"harness(?:es|ed|ing)?", r"elevat(?:e|es|ed|ing)", r"tapestry",
    r"realm", r"intricate", r"underscor(?:e|es|ed|ing)", r"bolster(?:s|ed|ing)?", r"crucial", r"vital",
    r"meticulous(?:ly)?", r"nuanced?", r"multifaceted", r"ever-evolving", r"dynamic landscape",
    r"evolving landscape", r"plays? a (?:crucial|pivotal|key|vital) role", r"it is (?:important|worth) (?:to note|noting)",
    r"in today's", r"not (?:just|only) [^.]{1,40}? but (?:also )?", r"in conclusion", r"at its core",
    r"a testament to", r"navigat(?:e|es|ing) the complexit(?:y|ies)",
]) + r")\b", re.I)

LONG_PARA = 40          # words; shorter paragraphs are too short to judge style
SHIFT_RATIO = 3.0       # a paragraph's AI-wording rate this many times the document's ...
SHIFT_FLOOR = 0.04      # ... and at least this rate (4 per 100 words) ...
SHIFT_MIN_HITS = 2      # ... from at least this many AI-typical words is a style outlier (one word isn't a shift)
CAP = 4
FIGURE_POINTS = 0  # points per figure label contradicting the text (sign 3): reported, not scored


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


B64 = b"A-Za-z0-9+/"


def provenance_marker(marker, data):
    """Whether a provenance marker appears in a picture file as itself, not as chance letters inside encoded data.

    Short markers ("c2pa", "jumb") turn up by chance inside base64 runs (pictures embedded in an SVG) and
    compressed bytes. A real marker is followed or preceded by a byte outside the base64 alphabet: a NUL in a
    JUMBF box ("jumd" + "c2pa\\x00..."), a ":" or quote in XMP. A match with base64 characters on both sides
    is left out.
    """
    pattern = re.compile(b"(?<![" + B64 + b"])" + re.escape(marker) + b"|" + re.escape(marker) + b"(?![" + B64 + b"])",
                         re.I)
    return bool(pattern.search(data))


def metadata_bytes(data):
    """Return the parts of a picture file where provenance can live, leaving out the encoded pixels.

    Chance letters ("jUmb") turn up inside compressed pixel data, so the pixels aren't searched:
    - PNG: every chunk except IDAT; compressed text chunks (zTXt, compressed iTXt) are inflated.
    - JPEG: the segments before the first SOS marker (APP1 XMP, APP11 JUMBF/C2PA live there).
    - anything else (SVG, EMF, GIF, ...): the whole file, as before.
    """
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        parts, p = [], 8
        while p + 8 <= len(data):
            n = struct.unpack(">I", data[p:p + 4])[0]
            kind, body = data[p + 4:p + 8], data[p + 8:p + 8 + n]
            if kind != b"IDAT":
                parts.append(kind + body)
                try:
                    if kind == b"zTXt":
                        parts.append(zlib.decompress(body.split(b"\0", 1)[1][1:]))
                    elif kind == b"iTXt":
                        key, rest = body.split(b"\0", 1)
                        if rest[0]:
                            parts.append(zlib.decompress(rest[2:].split(b"\0", 2)[2]))
                except (zlib.error, IndexError, ValueError):
                    pass
            p += 12 + n
        return b"\n".join(parts)
    if data.startswith(b"\xff\xd8"):
        p = 2
        while p + 4 <= len(data) and data[p] == 0xFF:
            marker = data[p + 1]
            if marker == 0xDA:  # start of scan: entropy-coded pixels follow
                return data[:p]
            if marker in (0x01,) or 0xD0 <= marker <= 0xD7:
                p += 2
                continue
            p += 2 + struct.unpack(">H", data[p + 2:p + 4])[0]
        return data[:p]
    return data


def picture_files(out_dir, docx):
    files = []
    if docx:
        z = zipfile.ZipFile(docx)
        files += [(os.path.basename(n), z.read(n)) for n in z.namelist()
                  if n.startswith(("word/media/", "xl/media/")) and not n.endswith("/")]
    elif os.path.isdir(os.path.join(out_dir, "media")):
        for n in sorted(os.listdir(os.path.join(out_dir, "media"))):
            with open(os.path.join(out_dir, "media", n), "rb") as f:
                files.append((n, f.read()))
    return files


def document_properties(docx):
    """Return ([(part field, value)], [(part field, value) naming an AI tool]) from the .docx's docProps."""
    fields, hits = [], []
    z = zipfile.ZipFile(docx)
    for part in PROPERTY_PARTS:
        if part not in z.namelist():
            continue
        xml = z.read(part).decode("utf-8", "replace")
        short = part.split("/")[1]
        # custom.xml keeps the name in an attribute and the value in a child element
        for name, value in re.findall(r'<property\b[^>]*\bname="([^"]*)"[^>]*>\s*<[^>]+>([^<]*)<', xml):
            fields.append(("%s %s" % (short, name), value.strip()))
        for tag, value in re.findall(r"<(?:\w+:)?(\w+)\b[^>]*>([^<]+)</", xml):
            if tag not in ("property",) and not re.match(r"lpw?str|i4|bool|filetime", tag):
                fields.append(("%s %s" % (short, tag), value.strip()))
    for label, value in fields:
        if PROPERTY_TOOLS.search(value) or PROPERTY_CLAUDE.fullmatch(value):
            hits.append((label, value))
    return fields, hits


def measure(out_dir, docx=None, mismatches=0):
    text = read(os.path.join(out_dir, "text.txt"))
    words = len(text.split()) or 1
    paras = [p for p in text.splitlines() if p.strip()]

    assistant = [m.group(0) for m in ASSISTANT.finditer(text)]
    assistant_lines = [p for p in paras if ASSISTANT.search(p)]

    provenance = []
    for name, data in picture_files(out_dir, docx):
        hits = sorted({k.decode("latin-1") for k in PROVENANCE if provenance_marker(k, metadata_bytes(data))})
        if hits:
            provenance.append((name, hits))
    properties, property_hits = document_properties(docx) if docx else (None, [])
    if property_hits:
        # one entry for the whole set of properties, scored like one picture
        provenance.append(("document properties", ["%s = %s" % h for h in property_hits]))

    ai_hits = AI_WORDS.findall(text)
    wording_rate = len(ai_hits) / words * 1000
    dash_rate = text.count("—") / words * 1000

    doc_rate = len(ai_hits) / words
    long_paras = [p for p in paras if len(p.split()) >= LONG_PARA]
    outliers = []
    for p in long_paras:
        hits = len(AI_WORDS.findall(p))
        r = hits / len(p.split())
        if hits >= SHIFT_MIN_HITS and r >= SHIFT_FLOOR and r >= SHIFT_RATIO * doc_rate:
            outliers.append((r, p))
    shift = len(outliers) / len(long_paras) if long_paras else 0.0

    score = (5 * min(len(assistant), CAP) + 5 * min(len(provenance), CAP) + FIGURE_POINTS * min(mismatches, CAP)
             + 10 * shift + 1.0 * wording_rate + 0.2 * dash_rate)
    top_words = {}
    for h in ai_hits:
        top_words[h.lower()] = top_words.get(h.lower(), 0) + 1
    return {
        "words": words, "assistant": assistant, "assistant_lines": assistant_lines, "provenance": provenance,
        "properties": properties,
        "mismatches": mismatches, "shift": shift, "long_paras": len(long_paras), "outliers": outliers,
        "wording_rate": wording_rate, "dash_rate": dash_rate, "score": score,
        "top_words": sorted(top_words.items(), key=lambda x: -x[1])[:8],
    }


def reference_score(d):
    """A reference document's score under the current weights, from the measurements the reference set records."""
    return (5 * min(d.get("assistant", 0), CAP) + 5 * min(d.get("provenance", 0), CAP)
            + FIGURE_POINTS * min(d.get("figure_mismatches", 0), CAP) + 10 * d.get("style_shift", 0)
            + d.get("wording_per_1000", 0) + 0.2 * d.get("em_dash_per_1000", 0))


def reference_stats():
    with open(REFERENCE, encoding="utf-8") as f:
        ref = json.load(f)
    scores = [reference_score(d) for d in ref["documents"]]
    m, sd = statistics.mean(scores), statistics.pstdev(scores)
    k = ref["sigma_multiplier"]
    return ref, m, sd, k


def class_cuts(ref=None):
    """(low_at_most, high_from): the reference scores that end the bottom low_share and start the top high_share."""
    if ref is None:
        ref = reference_stats()[0]
    rule = ref["class_rule"]
    s = sorted(reference_score(d) for d in ref["documents"])
    n = len(s)
    return s[math.ceil(n * rule["low_share"]) - 1], s[n - math.ceil(n * rule["high_share"])]


def class_of(score, cuts, direct=False):
    if direct:
        return "high (direct evidence)"
    low, high = cuts
    return "high" if score >= high else "low" if score <= low else "medium"


def classify(r, cuts):
    return class_of(r["score"], cuts, bool(r["assistant"] or r["provenance"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out_dir", nargs="?")
    ap.add_argument("--docx")
    ap.add_argument("--figure-mismatches", type=int, default=0)
    ap.add_argument("--reference", action="store_true")
    ap.add_argument("--json", action="store_true", help="print the raw measurements as JSON")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    ref, m, sd, k = reference_stats()
    cuts = class_cuts(ref)
    lines = ["AI-indicator reference: %d documents, mean %.2f, sigma %.2f; by rank (bottom %d%%, top %d%%) -> "
             "low <= %.2f, high >= %.2f"
             % (len(ref["documents"]), m, sd, 100 * ref["class_rule"]["low_share"],
                100 * ref["class_rule"]["high_share"], cuts[0], cuts[1])]
    if a.reference:
        for d in sorted(ref["documents"], key=reference_score):
            direct = bool(d.get("assistant", 0) or d.get("provenance", 0))
            cls = class_of(reference_score(d), cuts, direct)
            lines.append("  %-55s score %5.2f  z %+.2f  %s" % (d["name"], reference_score(d),
                                                                (reference_score(d) - m) / sd, cls))
    if a.out_dir:
        r = measure(a.out_dir, a.docx, a.figure_mismatches)
        if a.json:
            print(json.dumps({k2: v for k2, v in r.items() if k2 not in ("outliers", "assistant_lines")}, default=str))
            return
        lines += [
            "This document: score %.2f, z %+.2f -> %s" % (r["score"], (r["score"] - m) / sd, classify(r, cuts)),
            "  1. Leftover assistant text: %d" % len(r["assistant"]),
        ]
        lines += ["       \"%s\"" % p[:200] for p in r["assistant_lines"][:CAP]]
        lines.append("  2. AI provenance in metadata (pictures, document properties): %d" % len(r["provenance"]))
        lines += ["       %s: %s" % (n, ", ".join(h)) for n, h in r["provenance"]]
        if r["properties"] is None:
            lines.append("       document properties: not checked (no --docx)")
        else:
            shown = [(l, v) for l, v in r["properties"] if l.split(" ", 1)[1] in PROPERTY_SHOWN]
            lines.append("       properties recorded: %s"
                         % ("; ".join("%s = %s" % lv for lv in shown) or "none recorded"))
        lines.append("  3. Figure/text mismatches (from the visual check): %d (reported as its own measure, not scored)"
                     % r["mismatches"])
        lines.append("  4. Style shift: %d of %d long paragraphs (%.0f%%) far above the document's AI-typical wording"
                     % (len(r["outliers"]), r["long_paras"], 100 * r["shift"]))
        lines += ["       \"%s...\"" % p[:160] for _, p in sorted(r["outliers"], reverse=True)[:3]]
        lines.append("  5. AI-typical wording: %.2f per 1,000 words (most frequent: %s); em dashes %.2f per 1,000 words"
                     % (r["wording_rate"], ", ".join("%s %d" % w for w in r["top_words"]) or "none", r["dash_rate"]))
        evidence = 5 * min(len(r["assistant"]), CAP) + 5 * min(len(r["provenance"]), CAP)
        lines.append("  Score split: evidence counts (signs 1 and 2, absolute points, not scaled by length): %d; "
                     "wording and em-dash rates (sign 5, per 1,000 words): %.2f"
                     % (evidence, r["wording_rate"] + 0.2 * r["dash_rate"]))
        with open(os.path.join(a.out_dir, "ai_indicators.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    elif not a.reference:
        ap.error("give an output dir, or --reference")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
