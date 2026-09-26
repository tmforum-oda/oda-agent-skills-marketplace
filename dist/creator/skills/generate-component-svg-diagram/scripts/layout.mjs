// Diagram model → SVG, drawn with D3 into a jsdom document. See spec §5.
import * as d3 from 'd3';
import { JSDOM } from 'jsdom';

const FONT = 'Arial, Helvetica, sans-serif';
const C = { box: '#404040', ink: '#000000', paper: '#ffffff', muted: '#666666', onBox: '#cfcfcf' };
// Subtle per-function tints: stroke for the connector, fill for the glyph head and label pill.
export const FN_COLOR = {
  core: { stroke: '#4c9a52', fill: '#e8f5e9', name: 'Core function' },
  management: { stroke: '#4a7fbf', fill: '#e7eff9', name: 'Management function' },
  security: { stroke: '#c0504d', fill: '#fbeaea', name: 'Security function' },
};

// Helvetica advance widths (1/1000 em) for ASCII 32..126 — no text metrics in Node.
const W = [278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584];
export function textWidth(s, size = 12, bold = false) {
  let w = 0;
  for (const ch of String(s)) { const c = ch.charCodeAt(0); w += (c >= 32 && c <= 126 ? W[c - 32] : 600); }
  return (w / 1000) * size * (bold ? 1.07 : 1);
}

// Greedy word wrap to at most `maxLines` lines within `maxW` px.
function wrap(s, maxW, size, maxLines = 2) {
  const words = String(s).split(' ');
  const lines = [];
  let cur = '';
  for (const w of words) {
    const next = cur ? `${cur} ${w}` : w;
    if (textWidth(next, size) <= maxW || !cur) cur = next;
    else { lines.push(cur); cur = w; }
  }
  if (cur) lines.push(cur);
  if (lines.length > maxLines) {
    const head = lines.slice(0, maxLines - 1);
    head.push(lines.slice(maxLines - 1).join(' '));
    return head;
  }
  return lines;
}

const L = {
  margin: 30, titleH: 50, fs: 12,
  boxPad: 30, rectH: 30, rectGap: 10, rectMinW: 560, emptyBoxW: 380,
  sidCols: 3, sidH: 38, sidGap: 16, sidTop: 40,
  apiPitch: 46, groupGap: 20, stub: 150, r: 10, labelGap: 24,
  noteH: 30, legendH: 64, legendGap: 30,
};

// Row offsets for one side: even pitch, with an extra gap wherever the function changes.
function rowOffsets(apis, boxH) {
  if (!apis.length) return [];
  const breaks = apis.reduce((n, a, i) => n + (i && a.fn !== apis[i - 1].fn ? 1 : 0), 0);
  const avail = boxH - L.boxPad * 2 - breaks * L.groupGap;
  const pitch = Math.min(L.apiPitch * 1.3, avail / apis.length);
  let y = L.boxPad, prev = null;
  return apis.map((a) => {
    if (prev && a.fn !== prev) y += L.groupGap;
    prev = a.fn;
    const at = y + pitch / 2;
    y += pitch;
    return at;
  });
}

export function renderSvg(model) {
  const { document, XMLSerializer } = new JSDOM('<!DOCTYPE html><body></body>').window;
  const fs = L.fs;
  const isImpl = model.kind === 'implementation';
  const color = (d) => FN_COLOR[d.fn] ?? FN_COLOR.core;

  // ---- measure --------------------------------------------------------------
  const pillPad = 5;
  const labelW = (apis) => Math.max(0, ...apis.map((a) => textWidth(a.label, fs, a.required) + pillPad * 2));
  const leftGutter = Math.max(L.stub, labelW(model.dependent) + L.labelGap) + L.r * 2;
  const rightGutter = Math.max(L.stub, labelW(model.exposed) + L.labelGap) + L.r * 2;

  // A published spec with no eTOMs gets an explicit "none assigned" row; an implementation
  // simply doesn't carry eTOM/SID mappings, so its box is left compact instead.
  const etoms = model.etoms.length || isImpl ? model.etoms
    : [{ label: 'No eTOM business activities assigned', tooltip: 'componentMetadata.eTOMs is empty', placeholder: true }];
  const hasContent = etoms.length || model.sids.length;
  // Implementations: the box shows the chart's microservices instead of eTOM/SID content.
  const ms = isImpl && !hasContent && model.internals?.workloads.length
    ? measureInternals(model.internals, model.dependent.length > 0) : null;
  const rectW = hasContent ? Math.max(L.rectMinW, ...etoms.map((e) => textWidth(e.label, fs) + 16))
    : ms ? ms.width - L.boxPad * 2 : L.emptyBoxW - L.boxPad * 2;
  const boxW = rectW + L.boxPad * 2;
  const etomH = etoms.length ? etoms.length * (L.rectH + L.rectGap) - L.rectGap : 0;
  const sidRows = Math.ceil(model.sids.length / L.sidCols);
  const sidH = sidRows ? (etomH ? L.sidTop : 0) + sidRows * (L.sidH + L.sidGap) - L.sidGap : 0;
  const contentH = L.boxPad * 2 + etomH + sidH;
  const groupCount = (apis) => new Set(apis.map((a) => a.fn)).size;
  const apiH = (apis) => L.boxPad * 2 + apis.length * L.apiPitch + Math.max(0, groupCount(apis) - 1) * L.groupGap;
  let boxH = Math.max(contentH, apiH(model.dependent), apiH(model.exposed), ms?.height ?? 0, 200);
  let depY, expY, placed = null;
  // Microservice placement depends on API rows, which depend on box height: grow until it fits.
  for (let i = 0; i < 4; i++) {
    depY = rowOffsets(model.dependent, boxH);
    expY = rowOffsets(model.exposed, boxH);
    if (!ms) break;
    placed = placeInternals(model, ms, boxH, depY, expY);
    if (placed.overflow <= 0) break;
    boxH += Math.ceil(placed.overflow);
  }

  const fnsShown = Object.keys(FN_COLOR).filter((fn) =>
    [...model.exposed, ...model.dependent].some((a) => a.fn === fn));
  // Legend: shape key (eTOM/SID only when the diagram can contain them) + colour key when >1 function.
  const legend = {
    shapes: isImpl ? ['dependent', 'exposed', ...(etoms.length ? ['etom'] : []), ...(model.sids.length ? ['sid'] : []),
      ...(ms ? ['microservice', ...(model.internals.links.some((l) => l.type === 'internal') ? ['integration'] : [])] : [])]
      : ['etom', 'sid', 'dependent', 'exposed'],
    fns: fnsShown.length > 1 || isImpl ? fnsShown : [],
  };
  const rowW = (keys) => 140 + legendWidths(keys).reduce((a, b) => a + b, 0) + 30;

  const notes = [
    `Source: ${model.source}${model.functionalBlock ? ` · ${model.functionalBlock}` : ''} · bold API = required`,
    ...(model.sourceDetail ? [model.sourceDetail] : []),
  ];
  const noteW = Math.max(...notes.map((n) => textWidth(n, 11))) + leftGutter;
  const contentW = leftGutter + boxW + rightGutter;
  const titleW = textWidth(model.title, 16, true);
  // One legend row when it fits the diagram's width; otherwise shapes on one row, colours on a second.
  const bodyW = Math.max(contentW, titleW, noteW);
  legend.rows = rowW([...legend.shapes, ...legend.fns]) <= bodyW || !legend.fns.length
    ? [[...legend.shapes, ...legend.fns]] : [legend.shapes, legend.fns];
  const legendH = L.legendH + (legend.rows.length - 1) * 32;
  const pageW = L.margin * 2 + Math.max(bodyW, ...legend.rows.map(rowW));
  const originX = L.margin + Math.round((pageW - L.margin * 2 - contentW) / 2); // centre the diagram
  const boxX = Math.round(originX + leftGutter), boxY = L.margin + L.titleH;
  const legendY = boxY + boxH + L.noteH + (notes.length - 1) * 14 + L.legendGap;
  const pageH = legendY + legendH + L.margin;

  // ---- draw -----------------------------------------------------------------
  const svg = d3.select(document.body).append('svg')
    .attr('xmlns', 'http://www.w3.org/2000/svg')
    .attr('version', '1.1')
    .attr('width', Math.ceil(pageW)).attr('height', Math.ceil(pageH))
    .attr('viewBox', `0 0 ${Math.ceil(pageW)} ${Math.ceil(pageH)}`)
    .attr('font-family', FONT).attr('font-size', fs);
  svg.append('title').text(model.title);
  svg.append('desc').text(
    `ODA component architecture for ${model.id} (${model.source}, ${model.status}). ` +
    `Exposed APIs on the right, dependent APIs on the left; green = core, blue = management, red = security function. ` +
    `Generated by skills/svg-diagram.`);
  svg.append('rect').attr('width', '100%').attr('height', '100%').attr('fill', C.paper);

  svg.append('text').attr('x', L.margin).attr('y', L.margin + 10)
    .attr('font-size', 16).attr('font-weight', 'bold').attr('fill', C.ink).text(model.title);
  if (isImpl) {
    svg.append('text').attr('x', L.margin).attr('y', L.margin + 30).attr('fill', C.muted).text('Reference implementation');
  }

  // component box
  const box = svg.append('g').attr('id', 'component').attr('transform', `translate(${boxX},${boxY})`);
  box.append('rect').attr('width', boxW).attr('height', boxH).attr('fill', C.box).attr('stroke', C.ink);
  if (ms) {
    drawInternals(svg, box, model, ms, { boxW, boxH, placed });
  } else if (!hasContent) {
    box.append('text').attr('x', boxW / 2).attr('y', boxH / 2).attr('text-anchor', 'middle')
      .attr('font-style', 'italic').attr('fill', C.onBox)
      .text('No eTOM / SID mapping in implementation');
  }

  // eTOM activities
  const et = box.append('g').attr('id', 'etoms').selectAll('g').data(etoms).join('g')
    .attr('class', 'etom')
    .attr('transform', (_, i) => `translate(${L.boxPad},${L.boxPad + i * (L.rectH + L.rectGap)})`);
  et.append('title').text((d) => d.tooltip);
  et.append('rect').attr('width', rectW).attr('height', L.rectH).attr('fill', C.paper).attr('stroke', C.ink);
  et.append('text').attr('x', 6).attr('y', L.rectH / 2).attr('dy', '0.35em')
    .attr('fill', (d) => (d.placeholder ? C.muted : C.ink))
    .attr('font-style', (d) => (d.placeholder ? 'italic' : null))
    .text((d) => d.label);

  // SID entities as cylinders
  const colW = (rectW - (L.sidCols - 1) * L.sidGap) / L.sidCols;
  const cylW = Math.min(colW, 200), ry = 5;
  const sidY0 = L.boxPad + etomH + (etomH ? L.sidTop : 0);
  const sid = box.append('g').attr('id', 'sids').selectAll('g').data(model.sids).join('g')
    .attr('class', 'sid')
    .attr('transform', (_, i) => {
      const col = i % L.sidCols, row = Math.floor(i / L.sidCols);
      const x = L.boxPad + col * (colW + L.sidGap) + (colW - cylW) / 2;
      return `translate(${x},${sidY0 + row * (L.sidH + L.sidGap)})`;
    });
  sid.append('title').text((d) => d.tooltip);
  sid.append('path').attr('fill', C.paper).attr('stroke', C.ink)
    .attr('d', `M0,${ry} A${cylW / 2},${ry} 0 0 1 ${cylW},${ry} V${L.sidH - ry} A${cylW / 2},${ry} 0 0 1 0,${L.sidH - ry} Z`);
  sid.append('path').attr('fill', 'none').attr('stroke', C.ink)
    .attr('d', `M0,${ry} A${cylW / 2},${ry} 0 0 0 ${cylW},${ry}`);
  sid.each(function (d) {
    const lines = wrap(d.label, cylW - 10, fs);
    const t = d3.select(this).append('text').attr('text-anchor', 'middle').attr('fill', C.ink);
    const cy = ry + (L.sidH - ry) / 2 - ((lines.length - 1) * 13) / 2;
    lines.forEach((ln, i) => t.append('tspan').attr('x', cylW / 2).attr('y', cy + i * 13).attr('dy', '0.35em').text(ln));
  });

  // API label with a subtle function-coloured pill behind it, centred on cx.
  const label = (sel, cx) => {
    sel.append('rect')
      .attr('x', (d) => cx - (textWidth(d.label, fs, d.required) / 2 + pillPad)).attr('y', -23)
      .attr('width', (d) => textWidth(d.label, fs, d.required) + pillPad * 2).attr('height', 17).attr('rx', 3)
      .attr('fill', (d) => color(d).fill);
    sel.append('text').attr('x', cx).attr('y', -10).attr('text-anchor', 'middle')
      .attr('fill', C.ink).attr('font-weight', (d) => (d.required ? 'bold' : null)).text((d) => d.label);
  };

  // dependent (left): socket = half circle opening to the left, line into the box
  const dep = svg.append('g').attr('id', 'dependent-apis').selectAll('g').data(model.dependent).join('g')
    .attr('class', 'dependent-api').attr('data-api', (d) => d.id).attr('data-function', (d) => d.fn)
    .attr('transform', (_, i) => `translate(${originX},${boxY + depY[i]})`);
  dep.append('title').text((d) => d.tooltip);
  dep.append('path').attr('fill', 'none').attr('stroke', (d) => color(d).stroke).attr('stroke-width', 2.5)
    .attr('d', `M${L.r},${-L.r} A${L.r},${L.r} 0 0 1 ${L.r},${L.r}`);
  dep.append('line').attr('x1', L.r * 2).attr('x2', leftGutter).attr('y1', 0).attr('y2', 0)
    .attr('stroke', (d) => color(d).stroke).attr('stroke-width', 2);
  label(dep, L.r + leftGutter / 2);

  // exposed (right): lollipop = line out of the box ending in a circle
  const exp = svg.append('g').attr('id', 'exposed-apis').selectAll('g').data(model.exposed).join('g')
    .attr('class', 'exposed-api').attr('data-api', (d) => d.id).attr('data-function', (d) => d.fn)
    .attr('transform', (_, i) => `translate(${boxX + boxW},${boxY + expY[i]})`);
  exp.append('title').text((d) => d.tooltip);
  exp.append('line').attr('x1', 0).attr('x2', rightGutter - L.r * 2).attr('y1', 0).attr('y2', 0)
    .attr('stroke', (d) => color(d).stroke).attr('stroke-width', 2);
  exp.append('circle').attr('cx', rightGutter - L.r).attr('cy', 0).attr('r', L.r)
    .attr('fill', (d) => color(d).fill).attr('stroke', (d) => color(d).stroke).attr('stroke-width', 2);
  label(exp, (rightGutter - L.r) / 2);

  // note under the box
  notes.forEach((n, i) => svg.append('text').attr('x', boxX).attr('y', boxY + boxH + 20 + i * 14)
    .attr('font-style', 'italic').attr('font-size', 11).attr('fill', C.muted).text(n));

  drawLegend(svg, L.margin, legendY, pageW - L.margin * 2, legendH, legend);

  return new XMLSerializer().serializeToString(svg.node()) + '\n';
}

const LEGEND_LABEL = { etom: 'eTOM Business Activity', sid: 'SID Data Entity', dependent: 'Dependent API', exposed: 'Exposed API',
  microservice: 'Microservice', integration: 'Internal integration' };
const legendLabel = (k) => LEGEND_LABEL[k] ?? FN_COLOR[k].name;
const legendWidths = (keys) => keys.map((k) => 60 + textWidth(legendLabel(k)) + 30);

function drawLegend(svg, x, y, w, h, { shapes, rows }) {
  if (shapes.includes('integration')) arrowMarker(svg, 'arrow-legend', C.muted);
  const g = svg.append('g').attr('id', 'legend').attr('transform', `translate(${x},${y})`);
  g.append('rect').attr('width', w).attr('height', h).attr('rx', h / 2)
    .attr('fill', C.paper).attr('stroke', C.ink).attr('stroke-width', 1.5);
  g.append('text').attr('x', 40).attr('y', h / 2).attr('dy', '0.35em').attr('font-weight', 'bold').text('LEGEND');

  const core = FN_COLOR.core;
  // Items sit at their natural widths, with each row's leftover space shared out evenly.
  const at = new Map();
  rows.forEach((keys, r) => {
    const widths = legendWidths(keys);
    const spare = Math.max(0, (w - 170 - widths.reduce((a, b) => a + b, 0)) / keys.length);
    const cy = rows.length === 1 ? h / 2 : 20 + r * 32 + (h - 40 - (rows.length - 1) * 32) / 2;
    keys.forEach((k, i) => at.set(k, [140 + widths.slice(0, i).reduce((a, b) => a + b + spare, 0), cy]));
  });
  const item = (key, label, draw) => {
    if (!at.has(key)) return;
    const [ix, iy] = at.get(key);
    const s = g.append('g').attr('transform', `translate(${ix},${iy})`);
    draw(s);
    s.append('text').attr('x', 60).attr('dy', '0.35em').attr('fill', C.ink).text(label);
  };
  item('etom', LEGEND_LABEL.etom, (s) =>
    s.append('rect').attr('x', 0).attr('y', -10).attr('width', 50).attr('height', 20).attr('fill', C.paper).attr('stroke', C.ink));
  item('sid', LEGEND_LABEL.sid, (s) => {
    s.append('path').attr('fill', C.paper).attr('stroke', C.ink)
      .attr('d', 'M0,-8 A25,4 0 0 1 50,-8 V8 A25,4 0 0 1 0,8 Z');
    s.append('path').attr('fill', 'none').attr('stroke', C.ink).attr('d', 'M0,-8 A25,4 0 0 0 50,-8');
  });
  item('dependent', LEGEND_LABEL.dependent, (s) => {
    s.append('path').attr('fill', 'none').attr('stroke', core.stroke).attr('stroke-width', 2.5).attr('d', 'M10,-10 A10,10 0 0 1 10,10');
    s.append('line').attr('x1', 20).attr('x2', 50).attr('stroke', core.stroke).attr('stroke-width', 2);
  });
  item('exposed', LEGEND_LABEL.exposed, (s) => {
    s.append('line').attr('x1', 0).attr('x2', 30).attr('stroke', core.stroke).attr('stroke-width', 2);
    s.append('circle').attr('cx', 40).attr('r', 10).attr('fill', core.fill).attr('stroke', core.stroke).attr('stroke-width', 2);
  });
  item('microservice', LEGEND_LABEL.microservice, (s) =>
    s.append('rect').attr('x', 0).attr('y', -11).attr('width', 50).attr('height', 22).attr('rx', MS.rx)
      .attr('fill', C.paper).attr('stroke', C.ink));
  item('integration', LEGEND_LABEL.integration, (s) =>
    s.append('line').attr('x1', 0).attr('x2', 46).attr('stroke', C.muted).attr('stroke-width', 1.5)
      .attr('marker-end', 'url(#arrow-legend)'));
  Object.keys(FN_COLOR).forEach((fn) => item(fn, FN_COLOR[fn].name, (s) =>
    s.append('rect').attr('x', 0).attr('y', -9).attr('width', 50).attr('height', 18).attr('rx', 3)
      .attr('fill', FN_COLOR[fn].fill).attr('stroke', FN_COLOR[fn].stroke).attr('stroke-width', 2)));
}

// ---- implementation internals ------------------------------------------------------------
// Microservices (chart workloads) as rounded rectangles inside the component box. Services that
// implement an API sit in the right-hand column, aligned with the API they serve; everything
// else (databases, jobs, helpers) sits in the left-hand column next to what uses it.

const MS = { h: 46, gap: 18, rx: 9, colGap: 110, apiRoom: 56, minW: 170, maxW: 270, sub: 10 };
const INTEGRATION = '#d9d9d9';

const msSubline = (w) => [w.images.join(', '), w.ports.length ? `:${w.ports.join(', :')}` : '', w.role === 'job' ? w.kind : '']
  .filter(Boolean).join('  ');

function measureInternals(internals, hasDependent) {
  const { workloads, links } = internals;
  const apiLinked = new Set(links.filter((l) => l.type !== 'internal').map((l) => l.from));
  const colB = workloads.filter((w) => apiLinked.has(w.id));
  const colA = workloads.filter((w) => !apiLinked.has(w.id));
  const w = Math.min(MS.maxW, Math.max(MS.minW,
    ...workloads.map((x) => Math.max(textWidth(x.name, 12, true) + 34, textWidth(msSubline(x), MS.sub) + 20))));
  const xA = L.boxPad + (hasDependent ? MS.apiRoom : 0);
  const xB = colB.length && colA.length ? xA + w + MS.colGap : xA;
  const width = xB + w + (colB.length ? MS.apiRoom : 0) + L.boxPad;
  const rows = Math.max(colA.length, colB.length);
  return { w, xA, xB, colA, colB, width, height: L.boxPad * 2 + rows * (MS.h + MS.gap) - MS.gap };
}

// Place boxes at their ideal y, pushed apart to avoid overlap and kept inside [top, bottom].
function sweep(items, top, bottom) {
  const sorted = [...items].sort((a, b) => a.ideal - b.ideal || a.order - b.order);
  let y = top;
  for (const it of sorted) { it.y = Math.max(Number.isFinite(it.ideal) ? it.ideal : y, y); y = it.y + MS.h + MS.gap; }
  let limit = bottom;
  for (const it of sorted.reverse()) { it.y = Math.min(it.y, limit - MS.h); limit = it.y - MS.gap; }
  for (const it of sorted.reverse()) it.y = Math.max(it.y, top);
}

function arrowMarker(svg, id, fill) {
  let defs = svg.select('defs');
  if (defs.empty()) defs = svg.insert('defs', ':first-child');
  defs.append('marker').attr('id', id).attr('viewBox', '0 0 10 10').attr('refX', 9).attr('refY', 5)
    .attr('markerWidth', 7).attr('markerHeight', 7).attr('orient', 'auto-start-reverse')
    .append('path').attr('d', 'M0,0 L10,5 L0,10 Z').attr('fill', fill);
}

// Positions for every microservice. Right column: at the mean y of its APIs. Left column: beside
// the services it integrates with, but kept off the rows that dependent-API lines run along to
// reach the right column (so a line never appears to end at the wrong box). `overflow` > 0 means
// the box must grow by that much.
function placeInternals(model, ms, boxH, depY, expY) {
  const { links, apiKey } = model.internals;
  const apiY = new Map([
    ...model.exposed.map((a, i) => [apiKey('exposed', a), expY[i]]),
    ...model.dependent.map((a, i) => [apiKey('dependent', a), depY[i]]),
  ]);
  const top = L.boxPad, bottom = boxH - L.boxPad;
  const pos = new Map(); // workload id → {x, y}
  const mean = (ys) => (ys.length ? ys.reduce((a, b) => a + b, 0) / ys.length : Infinity);

  const colB = ms.colB.map((w, order) => ({ w, order,
    ideal: mean(links.filter((l) => l.from === w.id && l.api).map((l) => apiY.get(l.api)).filter((y) => y != null)) - MS.h / 2 }));
  sweep(colB, top, bottom);
  colB.forEach((it) => pos.set(it.w.id, { x: ms.xB, y: it.y }));

  const inB = new Set(ms.colB.map((w) => w.id));
  const bands = ms.colA.length
    ? [...new Set(links.filter((l) => l.type === 'dependent' && inB.has(l.from)).map((l) => apiY.get(l.api)))]
      .filter((y) => y != null).sort((a, b) => a - b)
    : [];
  const clear = 8;
  const colA = ms.colA.map((w, order) => {
    const peers = links.filter((l) => l.type === 'internal' && (l.to === w.id || l.from === w.id))
      .map((l) => pos.get(l.to === w.id ? l.from : l.to)).filter(Boolean).map((p) => p.y);
    return { w, order, ideal: w.role === 'job' ? Infinity : mean(peers) };
  }).sort((a, b) => a.ideal - b.ideal || a.order - b.order);
  let cursor = top, overflow = 0;
  for (const it of colA) {
    let y = Math.max(Number.isFinite(it.ideal) ? it.ideal : cursor, cursor);
    for (let moved = true; moved; ) {
      moved = false;
      for (const b of bands) {
        if (y < b + clear && y + MS.h > b - clear) { y = b + clear; moved = true; }
      }
    }
    pos.set(it.w.id, { x: ms.xA, y });
    cursor = y + MS.h + MS.gap;
    overflow = Math.max(overflow, y + MS.h - bottom);
  }
  return { pos, apiY, overflow };
}

function drawInternals(svg, box, model, ms, { boxW, boxH, placed }) {
  const { workloads, links, external } = model.internals;
  const { pos, apiY } = placed;

  const g = box.append('g').attr('id', 'microservices');
  arrowMarker(svg, 'arrow-internal', INTEGRATION);
  const curve = (x1, y1, x2, y2) => {
    const mx = (x1 + x2) / 2;
    return `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`;
  };
  const byId = new Map(workloads.map((w) => [w.id, w]));

  // faint links from API edge-points to the microservice that implements / consumes them
  const apiLinks = links.filter((l) => l.api && pos.has(l.from) && apiY.has(l.api));
  g.append('g').attr('id', 'api-links').selectAll('path').data(apiLinks).join('path')
    .attr('class', 'api-link').attr('data-api', (l) => l.api).attr('data-from', (l) => byId.get(l.from).name)
    .attr('fill', 'none').attr('stroke', (l) => (FN_COLOR[l.fn] ?? FN_COLOR.core).stroke)
    .attr('stroke-opacity', 0.85).attr('stroke-width', 1.5).attr('stroke-dasharray', '5 4')
    .attr('d', (l) => {
      const p = pos.get(l.from), cy = p.y + MS.h / 2;
      if (l.type === 'exposed') return curve(p.x + ms.w, cy, boxW, apiY.get(l.api));
      // Dependent: run level with the API row across the left column, turn in the gap before
      // the right column.
      const y1 = apiY.get(l.api);
      const turn = p.x > ms.xA ? ms.xA + ms.w + 20 : 0;
      if (!turn) return curve(0, y1, p.x, cy);
      const mx = (turn + p.x) / 2;
      return `M0,${y1} H${turn} C${mx},${y1} ${mx},${cy} ${p.x},${cy}`;
    })
    .append('title').text((l) => `${byId.get(l.from).name} ${l.type === 'exposed' ? 'implements' : 'consumes'} ${l.api.split(':').pop()}${l.via ? ` (via ${l.via})` : ''}`);

  // internal integrations between microservices
  const internal = links.filter((l) => l.type === 'internal' && pos.has(l.from) && pos.has(l.to));
  g.append('g').attr('id', 'internal-links').selectAll('path').data(internal).join('path')
    .attr('class', 'internal-link').attr('data-from', (l) => byId.get(l.from).name).attr('data-to', (l) => byId.get(l.to).name)
    .attr('fill', 'none').attr('stroke', INTEGRATION).attr('stroke-width', 1.5).attr('marker-end', 'url(#arrow-internal)')
    .attr('d', (l) => {
      const a = pos.get(l.from), b = pos.get(l.to);
      if (a.x === b.x) { // same column: loop out to the side
        const down = b.y > a.y, x = a.x + ms.w - 16;
        return `M${x},${down ? a.y + MS.h : a.y} L${x},${down ? b.y : b.y + MS.h}`;
      }
      const leftward = b.x < a.x;
      return curve(leftward ? a.x : a.x + ms.w, a.y + MS.h / 2, leftward ? b.x + ms.w : b.x, b.y + MS.h / 2);
    })
    .append('title').text((l) => `${byId.get(l.from).name} → ${byId.get(l.to).name}\n${l.via.join('\n')}`);

  // microservice boxes
  const node = g.append('g').attr('id', 'workloads').selectAll('g').data(workloads.filter((w) => pos.has(w.id))).join('g')
    .attr('class', 'microservice').attr('data-name', (w) => w.name).attr('data-role', (w) => w.role)
    .attr('transform', (w) => `translate(${pos.get(w.id).x},${pos.get(w.id).y})`);
  node.append('title').text((w) => [
    `${w.name} (${w.kind}${w.role === 'database' ? ', database' : ''})`,
    ...w.images.map((i) => `image: ${i}`),
    ...w.services.map((sv) => `service: ${sv.name}:${sv.ports.join(',')}`),
    ...links.filter((l) => l.from === w.id && l.type !== 'internal').map((l) => `${l.type} API: ${l.api.split(':').pop()}`),
  ].join('\n'));
  node.append('rect').attr('width', ms.w).attr('height', MS.h).attr('rx', MS.rx)
    .attr('fill', (w) => (w.role === 'job' ? '#ececec' : C.paper)).attr('stroke', C.ink)
    .attr('stroke-dasharray', (w) => (w.role === 'job' ? '4 3' : null));
  node.append('text').attr('x', 10).attr('y', 19).attr('font-weight', 'bold').attr('fill', C.ink).text((w) => w.name);
  node.append('text').attr('x', 10).attr('y', 35).attr('font-size', MS.sub).attr('fill', C.muted).text((w) => msSubline(w));
  // small cylinder marks databases
  node.filter((w) => w.role === 'database').append('path')
    .attr('transform', `translate(${ms.w - 24},9)`).attr('fill', 'none').attr('stroke', C.muted)
    .attr('d', 'M0,3 A7,3 0 0 1 14,3 V13 A7,3 0 0 1 0,13 Z M0,3 A7,3 0 0 0 14,3');

  if (external.length) {
    box.append('text').attr('x', L.boxPad).attr('y', boxH - 10).attr('font-size', MS.sub).attr('fill', C.onBox)
      .attr('font-style', 'italic').text(`Platform services used: ${external.join(', ')}`)
      .append('title').text('Hosts referenced by microservice environment variables that are not part of this chart');
  }
}
