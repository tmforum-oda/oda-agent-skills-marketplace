#!/usr/bin/env node
// Build a single self-contained HTML page with every rendered diagram inlined (for review).
// Usage: node gallery.mjs [--diagrams-dir diagrams] [--out diagrams/index.html]
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const dir = opt('--diagrams-dir', 'diagrams');
const out = opt('--out', path.join(dir, 'index.html'));

const files = fs.readdirSync(dir).filter((f) => /^TMFC\d+-architecture\.svg$/.test(f)).sort();
const figures = files.map((f) => {
  const id = f.split('-')[0];
  // Make each inline SVG scale to the figure width.
  const svg = fs.readFileSync(path.join(dir, f), 'utf8')
    .replace(/<svg([^>]*?) width="\d+" height="\d+"/, '<svg$1 width="100%"');
  return `<figure id="${id}"><figcaption><a href="${f}">${id}</a></figcaption>${svg}</figure>`;
});

fs.writeFileSync(out, `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>ODA Component Diagrams</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial,Helvetica,sans-serif;margin:16px;background:#f4f4f4;color:#000}
figure{background:#fff;margin:0 0 24px;padding:8px;border:1px solid #ccc}
figcaption{font-weight:bold;margin-bottom:6px}
figure svg{display:block;height:auto;max-width:100%}
</style></head><body>
<h1>ODA Component Diagrams (${files.length})</h1>
${figures.join('\n')}
</body></html>
`, 'utf8');
console.log(`wrote ${out} (${files.length} diagrams)`);
