#!/usr/bin/env node
// CLI:
//   node render.mjs <TMFCxxx|all> [--components-dir DIR (default: the bundled knowledge/components)] [--out PATH] [--include security,management] [--etom-levels 2|all]
//   node render.mjs --chart <helm-chart-dir> [--release r1] [--set k=v]... [--values f.yaml]... [--include ...] [--out PATH]
import fs from 'node:fs';
import path from 'node:path';
import { loadComponent, loadChart, listComponentIds, DEFAULT_COMPONENTS_DIR } from './model.mjs';
import { renderSvg } from './layout.mjs';

function parseArgs(argv) {
  const opts = { target: null, componentsDir: DEFAULT_COMPONENTS_DIR, out: null, include: null, etomLevels: '2',
    chart: null, release: 'r1', set: [], values: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--components-dir') opts.componentsDir = argv[++i];
    else if (a === '--out') opts.out = argv[++i];
    else if (a === '--include') opts.include = argv[++i].split(',').map((s) => s.trim()).filter((s) => s && s !== 'none');
    else if (a === '--etom-levels') opts.etomLevels = argv[++i];
    else if (a === '--chart') opts.chart = argv[++i];
    else if (a === '--release') opts.release = argv[++i];
    else if (a === '--set') opts.set.push(argv[++i]);
    else if (a === '--values' || a === '-f') opts.values.push(argv[++i]);
    else if (a === '--help' || a === '-h') opts.help = true;
    else if (!opts.target) opts.target = a;
    else throw new Error(`Unexpected argument: ${a}`);
  }
  return opts;
}

const usage = `Usage:
  node render.mjs <TMFCxxx|all> [--components-dir knowledge/components] [--out diagrams/X.svg|dir] [--include security,management] [--etom-levels 2|all]
  node render.mjs --chart <helm-chart-dir> [--release r1] [--set key=value]... [--values file.yaml]... [--include none|security,management] [--out file.svg|dir]`;

const summary = (m) =>
  `dependent ${m.dependent.length}, exposed ${m.exposed.length}, eTOM ${m.etoms.length}, SID ${m.sids.length}` +
  ` | by function: ${m.functions.map((fn) => `${fn} ${[...m.exposed, ...m.dependent].filter((a) => a.fn === fn).length}`).join(', ')}`;

function write(file, model) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, renderSvg(model), 'utf8');
  console.log(`wrote ${file}  (${summary(model)})`);
}

function renderChart(opts) {
  // Implementations deploy all three functions, so show them all unless told otherwise.
  const include = opts.include ?? ['management', 'security'];
  const { chart, model } = loadChart(opts.chart, { ...opts, include });
  const def = `${chart.name}-architecture.svg`;
  const file = !opts.out ? path.join('diagrams', 'reference', def)
    : opts.out.toLowerCase().endsWith('.svg') ? opts.out : path.join(opts.out, def);
  write(file, model);
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help || (!opts.target && !opts.chart)) { console.log(usage); process.exit(opts.help ? 0 : 1); }
  for (const f of opts.include ?? []) {
    if (!['security', 'management'].includes(f)) throw new Error(`--include accepts none or security,management (got ${f})`);
  }
  if (opts.chart) {
    if (!fs.existsSync(path.join(opts.chart, 'Chart.yaml'))) throw new Error(`No Chart.yaml in ${opts.chart}`);
    renderChart(opts);
    return;
  }
  if (!fs.existsSync(opts.componentsDir)) throw new Error(`Components dir not found: ${opts.componentsDir}`);
  const include = opts.include ?? [];

  const batch = opts.target.toLowerCase() === 'all';
  const ids = batch ? listComponentIds(opts.componentsDir) : [opts.target.toUpperCase()];
  // In batch mode --out is a directory; for a single id it may be a file or directory.
  const outFor = (id) => {
    const def = `${id}-architecture.svg`;
    if (!opts.out) return path.join('diagrams', def);
    return batch || !opts.out.toLowerCase().endsWith('.svg') ? path.join(opts.out, def) : opts.out;
  };

  let ok = 0, skipped = 0, failed = 0;
  for (const id of ids) {
    try {
      const model = loadComponent(opts.componentsDir, id, { ...opts, include });
      if (!model) {
        console.warn(`skip ${id}: no component.yaml`);
        skipped++;
        if (!batch) process.exit(2);
        continue;
      }
      write(outFor(id), model);
      ok++;
    } catch (e) {
      console.error(`fail ${id}: ${e.message}`);
      failed++;
      if (!batch) process.exit(1);
    }
  }
  if (batch) console.log(`done: ${ok} rendered, ${skipped} skipped, ${failed} failed`);
  process.exit(failed ? 1 : 0);
}

try { main(); } catch (e) { console.error(e.message); process.exit(1); }
