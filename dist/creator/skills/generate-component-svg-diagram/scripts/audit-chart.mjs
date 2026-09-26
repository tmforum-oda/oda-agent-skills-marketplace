// Independent audit of a chart diagram: re-derives what *should* be linked straight from the raw
// `helm template` documents and checks the SVG, without using model.mjs's link logic
// (buildInternals). The SVG's data-* attributes are the only contract shared with the renderer.
// Findings are warnings (probable gaps) or info (worth knowing, often expected).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const PLACEHOLDER = /^(exposed|dependent)API_/;
const WORKLOADS = ['Deployment', 'StatefulSet', 'DaemonSet', 'Job', 'CronJob'];
const FUNCS = ['core', 'management', 'security'];
const PLATFORM = JSON.parse(fs.readFileSync(
  path.join(path.dirname(fileURLToPath(import.meta.url)), 'platform-apis.json'), 'utf8')).apis;

const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
// Does env value `v` refer to host `h`? Whole value, URL host, host:port, or h.<namespace>…
const refersTo = (v, h) => new RegExp(`(^|://|@)${esc(h)}(?=$|[:/.])`, 'i').test(v);

function hostsOf(v) {
  const url = v.match(/^[a-z][a-z0-9+.-]*:\/\/([^/:?#\s]+)/i);
  const host = url ? url[1] : (v.match(/^([a-z0-9-]+(?:\.[a-z0-9-]+)+)(?::\d+)?$/i) ?? [])[1];
  return host && /[a-z]/i.test(host) ? [host] : [];
}

export function auditChart(docs, svg, { release = 'r1' } = {}) {
  const out = [];
  const warn = (check, message) => out.push({ level: 'warn', check, message });
  const info = (check, message) => out.push({ level: 'info', check, message });
  const short = (n) => (String(n).startsWith(`${release}-`) ? String(n).slice(release.length + 1) : String(n));
  const q = (sel) => [...svg.querySelectorAll(sel)];

  // ---- what the SVG shows
  const drawnMs = new Set(q('.microservice').map((g) => g.getAttribute('data-name')));
  const apiLinks = q('.api-link').map((p) => ({ api: p.getAttribute('data-api'), from: p.getAttribute('data-from') }));
  const internal = q('.internal-link').map((p) => `${p.getAttribute('data-from')}>${p.getAttribute('data-to')}`);
  const drawnApi = (side, fn, id) => q(`.${side}-api`).some((g) => g.getAttribute('data-api') === id && g.getAttribute('data-function') === fn);
  const linked = (side, fn, id, from) => apiLinks.some((l) => l.api === `${side}:${fn}:${id}` && (!from || l.from === from));

  // ---- what the chart declares
  const comp = docs.find((d) => d.kind === 'Component');
  const workloads = docs.filter((d) => WORKLOADS.includes(d.kind)).map((w) => {
    const tpl = w.kind === 'CronJob' ? w.spec?.jobTemplate?.spec?.template : w.spec?.template;
    return {
      name: short(w.metadata.name), full: w.metadata.name, kind: w.kind,
      labels: tpl?.metadata?.labels ?? {},
      env: (tpl?.spec?.containers ?? []).flatMap((c) => c.env ?? []).filter((e) => e.value != null).map((e) => ({ k: e.name, v: String(e.value) })),
    };
  });
  const services = docs.filter((d) => d.kind === 'Service').map((s) => {
    const sel = s.spec?.selector ?? {};
    const targets = Object.keys(sel).length
      ? workloads.filter((w) => Object.entries(sel).every(([k, v]) => w.labels[k] === v)) : [];
    return { name: s.metadata.name, targets };
  });
  const svcByName = new Map(services.map((s) => [s.name, s]));

  for (const w of workloads) if (!drawnMs.has(w.name)) warn('microservice-drawn', `${w.kind} ${w.name} is in the chart but not drawn`);
  for (const s of services) if (!s.targets.length) warn('service-selects', `Service ${s.name} selects no workload in the chart`);

  const apis = (key) => FUNCS.flatMap((fn) => (comp?.spec?.[`${fn}Function`]?.[key] ?? [])
    .filter((a) => a.name && !PLACEHOLDER.test(String(a.name)))
    .map((a) => ({ ...a, fn, key: /^TMF\d+$/.test(String(a.id ?? '')) ? String(a.id) : String(a.name) })));

  // A. every exposed API resolves to a workload, and the diagram links that workload to it
  for (const a of apis('exposedAPIs')) {
    const tag = `${a.fn} ${a.key}`;
    if (!drawnApi('exposed', a.fn, a.key)) { warn('exposed-drawn', `${tag} is declared but not drawn`); continue; }
    if (!a.implementation) { warn('exposed-implementation', `${tag} has no implementation field`); continue; }
    const impl = svcByName.get(a.implementation)?.targets ?? workloads.filter((w) => w.full === a.implementation);
    if (!impl.length) { warn('exposed-implementation', `${tag} implementation ${a.implementation} matches no Service/workload in the chart`); continue; }
    for (const w of impl) {
      if (!linked('exposed', a.fn, a.key, w.name)) warn('exposed-linked', `${tag} is implemented by ${w.name} (via ${a.implementation}) but the diagram has no link`);
    }
  }

  // B. every declared dependent API has at least one consuming microservice
  for (const a of apis('dependentAPIs')) {
    const tag = `${a.fn} ${a.key}`;
    if (!drawnApi('dependent', a.fn, a.key)) { warn('dependent-drawn', `${tag} is declared but not drawn`); continue; }
    if (!linked('dependent', a.fn, a.key)) {
      warn('dependent-linked', `${tag} (${a.name}) is declared but no microservice is linked to it`);
      continue;
    }
    const byEnv = workloads.filter((w) => w.env.some((e) => e.v.toLowerCase() === String(a.name).toLowerCase()));
    info('dependent-linked', `${tag} linked to ${apiLinks.filter((l) => l.api === `dependent:${a.fn}:${a.key}`).map((l) => l.from).join(', ')}` +
      (byEnv.length ? ` (named in env of ${byEnv.map((w) => w.name).join(', ')})` : ' (no env names it — wired by Canvas discovery)'));
  }

  // C. env vars that name another in-chart Service should appear as internal integrations
  for (const w of workloads) {
    for (const s of services) {
      const hits = w.env.filter((e) => refersTo(e.v, s.name));
      for (const t of hits.length ? s.targets : []) {
        if (t.name === w.name) continue;
        if (!internal.includes(`${w.name}>${t.name}`)) {
          warn('internal-linked', `${w.name} → ${t.name} (${hits.map((e) => `${e.k}=${e.v}`).join(', ')}) is not drawn`);
        }
      }
    }
  }

  // D. hosts outside the chart: known platform APIs must be drawn and linked; unknown ones flagged
  for (const w of workloads) {
    for (const e of w.env) {
      for (const h of hostsOf(e.v)) {
        if (services.some((s) => h === s.name || h.startsWith(`${s.name}.`))) continue;
        const p = PLATFORM.find((x) => x.hosts.some((ph) => ph.toLowerCase() === h.toLowerCase()));
        if (!p) { warn('platform-mapped', `${w.name} ${e.k} → ${h} is not in platform-apis.json (shown only as a note)`); continue; }
        const id = p.id ?? p.name;
        if (!drawnApi('dependent', p.function, id)) warn('platform-drawn', `${h} → ${p.function} ${id} is not drawn`);
        else if (!linked('dependent', p.function, id, w.name)) warn('platform-linked', `${w.name} uses ${h} (${e.k}) but is not linked to ${id}`);
      }
    }
  }

  // E. Services nothing points at, and microservices with no lines at all
  const implNames = new Set(apis('exposedAPIs').map((a) => a.implementation).filter(Boolean));
  for (const s of services) {
    if (!implNames.has(s.name) && !workloads.some((w) => w.env.some((e) => refersTo(e.v, s.name)))) {
      info('service-used', `Service ${s.name} is not an API implementation and no env var refers to it`);
    }
  }
  for (const w of workloads) {
    const any = apiLinks.some((l) => l.from === w.name) || internal.some((k) => k.split('>').includes(w.name));
    if (!any) info('isolated', `${w.name} (${w.kind}) has no lines${w.kind === 'Job' || w.kind === 'CronJob' ? ' — expected for an init job unless it calls an API' : ''}`);
  }
  return out;
}
