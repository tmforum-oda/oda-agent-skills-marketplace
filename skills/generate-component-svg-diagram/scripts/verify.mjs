#!/usr/bin/env node
// Check rendered SVGs against the YAML-derived model: element counts and API ids per side.
// Usage: node verify.mjs [--components-dir knowledge/components] [--diagrams-dir diagrams] [TMFCxxx ...]
//        node verify.mjs --chart <dir> [--svg diagrams/reference/<chart>-architecture.svg] [--set k=v]... [--strict]
// Chart mode runs two passes: the SVG against the model it was drawn from, then an independent
// audit (audit-chart.mjs) that re-derives expected links from the raw helm output. Audit warnings
// fail the run only with --strict.
import fs from 'node:fs';
import path from 'node:path';
import { JSDOM } from 'jsdom';
import { loadComponent, loadChart, helmTemplate, listComponentIds, DEFAULT_COMPONENTS_DIR } from './model.mjs';
import { auditChart } from './audit-chart.mjs';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args.splice(i, 2)[1] : d; };
const componentsDir = opt('--components-dir', DEFAULT_COMPONENTS_DIR);
const diagramsDir = opt('--diagrams-dir', 'diagrams');
const chartDir = opt('--chart', null);
const svgPath = opt('--svg', null);
const sets = [];
for (let s; (s = opt('--set', null)); ) sets.push(s);
const strict = args.includes('--strict') && !!args.splice(args.indexOf('--strict'), 1);
if (chartDir) process.exit(verifyChart());
const ids = args.length ? args : listComponentIds(componentsDir);

// Chart mode: APIs per function, microservices and every link drawn, against `helm template`.
function verifyChart() {
  const { chart, model } = loadChart(chartDir, { componentsDir, set: sets, include: ['management', 'security'] });
  const file = svgPath ?? path.join(diagramsDir, 'reference', `${chart.name}-architecture.svg`);
  const doc = new JSDOM(fs.readFileSync(file, 'utf8'), { contentType: 'image/svg+xml' }).window.document;
  const q = (sel) => [...doc.querySelectorAll(sel)];
  const sideIds = (sel) => q(sel).map((g) => `${g.getAttribute('data-function')}:${g.getAttribute('data-api')}`).join(',');
  const { workloads, links } = model.internals;
  const linkIds = (type) => links.filter((l) => l.type === type)
    .map((l) => `${workloads.find((w) => w.id === l.from).name}>${l.api ?? workloads.find((w) => w.id === l.to).name}`).sort().join(',');
  const got = {
    exposed: sideIds('.exposed-api'),
    dependent: sideIds('.dependent-api'),
    microservices: q('.microservice').map((g) => g.getAttribute('data-name')).join(','),
    apiLinks: q('.api-link').map((p) => `${p.getAttribute('data-from')}>${p.getAttribute('data-api')}`).sort().join(','),
    internalLinks: q('.internal-link').map((p) => `${p.getAttribute('data-from')}>${p.getAttribute('data-to')}`).sort().join(','),
  };
  const want = {
    exposed: model.exposed.map((a) => `${a.fn}:${a.id}`).join(','),
    dependent: model.dependent.map((a) => `${a.fn}:${a.id}`).join(','),
    microservices: workloads.map((w) => w.name).join(','),
    apiLinks: [linkIds('exposed'), linkIds('dependent')].filter(Boolean).join(',').split(',').filter(Boolean).sort().join(','),
    internalLinks: linkIds('internal'),
  };
  const bad = Object.keys(want).filter((k) => got[k] !== want[k]);
  for (const k of Object.keys(want)) console.log(`${bad.includes(k) ? 'FAIL' : 'ok  '} ${k}: ${got[k] || '(none)'}${bad.includes(k) ? `  want ${want[k]}` : ''}`);
  const { docs } = helmTemplate(chartDir, { set: sets });
  const findings = auditChart(docs, doc);
  const warnings = findings.filter((f) => f.level === 'warn');
  console.log(`independent audit (${warnings.length} warning${warnings.length === 1 ? '' : 's'}):`);
  for (const f of findings) console.log(`  ${f.level === 'warn' ? 'WARN' : 'info'} [${f.check}] ${f.message}`);
  const failed = bad.length || (strict && warnings.length);
  console.log(`${file}: ${failed ? 'FAILED' : 'passed'}`);
  return failed ? 1 : 0;
}

let failures = 0, checked = 0;
for (const id of ids) {
  const model = loadComponent(componentsDir, id);
  if (!model) continue;
  const file = path.join(diagramsDir, `${id}-architecture.svg`);
  if (!fs.existsSync(file)) { console.log(`MISSING ${file}`); failures++; continue; }
  const doc = new JSDOM(fs.readFileSync(file, 'utf8'), { contentType: 'image/svg+xml' }).window.document;
  const q = (sel) => [...doc.querySelectorAll(sel)];
  const got = {
    dependent: q('.dependent-api').map((g) => g.getAttribute('data-api')).join(','),
    exposed: q('.exposed-api').map((g) => g.getAttribute('data-api')).join(','),
    etoms: q('.etom').length,
    sids: q('.sid').length,
    title: doc.querySelector('svg > text')?.textContent,
    legend: !!doc.querySelector('#legend'),
  };
  const want = {
    dependent: model.dependent.map((a) => a.id).join(','),
    exposed: model.exposed.map((a) => a.id).join(','),
    etoms: Math.max(model.etoms.length, 1), // placeholder rect when none
    sids: model.sids.length,
    title: model.title,
    legend: true,
  };
  const bad = Object.keys(want).filter((k) => got[k] !== want[k]);
  checked++;
  if (bad.length) {
    failures++;
    console.log(`FAIL ${id}: ` + bad.map((k) => `${k} got=${got[k]} want=${want[k]}`).join('; '));
  } else {
    console.log(`ok   ${id}  dep=${model.dependent.length} exp=${model.exposed.length} etom=${got.etoms} sid=${got.sids}`);
  }
}
console.log(`${checked} checked, ${failures} failed`);
process.exit(failures ? 1 : 0);
