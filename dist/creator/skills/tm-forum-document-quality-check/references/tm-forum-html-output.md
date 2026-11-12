---
name: tm-forum-html-output
description: Generate consistent, accessible, responsive, self-contained HTML outputs for TM Forum agents. Use whenever an agent is asked to return a report, briefing, comparison, plan, dashboard, search result, recommendation, summary, or other content as HTML.
version: 1.0.0
owner: TM Forum
output-type: text/html
---

# TM Forum HTML output skill

## Purpose

Create polished HTML that feels like a TM Forum digital product rather than a generic AI response. Apply this skill to all agent-generated HTML unless a more specific product or event design system has been explicitly supplied.

The output must be:

- recognisably TM Forum
- accessible and keyboard-friendly
- responsive from mobile to desktop
- self-contained and safe to embed
- concise, scannable, and useful without additional explanation
- based only on supplied or retrieved facts, with no invented data

## Activation rules

Use this skill when the user asks for:

- HTML, a web page, a visual report, or a clickable prototype
- a briefing, summary, recommendation, comparison, plan, roadmap, or dashboard that would benefit from structured HTML
- an output intended for a TM Forum website, Copilot agent, internal portal, or downloadable HTML artefact

Do not use this skill when:

- the host application requires plain text, Markdown, Adaptive Cards, JSON, or another fixed schema
- an approved event-specific design system is supplied
- the user explicitly requests unstyled or fragment-only HTML

## Output contract

Return one complete HTML5 document by default. Begin with `<!doctype html>` and include `html`, `head`, and `body` elements.

If the host explicitly requests a fragment, return only one root `<section class="tmf-agent-output">` and include the same CSS in a scoped `<style>` block.

Unless explicitly requested, output only the HTML. Do not wrap it in Markdown fences and do not add commentary before or after it.

## Brand foundation

Use these core design tokens. They align with the TM Forum corporate palette and should be kept as CSS custom properties so a host application can override them.

```css
:root {
  --tmf-navy: #0d0b4d;
  --tmf-dark-red: #d91241;
  --tmf-bright-red: #ff004a;
  --tmf-orange: #ff5502;
  --tmf-green: #42b277;
  --tmf-blue: #39c5e5;
  --tmf-pink: #f4059d;
  --tmf-purple: #980bd9;

  --tmf-white: #ffffff;
  --tmf-off-white: #f7f7fa;
  --tmf-border: #d9d9e5;
  --tmf-muted: #5b5b73;
  --tmf-success-bg: #eaf7f0;
  --tmf-warning-bg: #fff4e8;
  --tmf-danger-bg: #fff0f3;
  --tmf-info-bg: #edf9fc;

  --tmf-gradient: linear-gradient(110deg, #0d0b4d 13%, #d91241 100%);
  --tmf-font: "DM Sans", Arial, sans-serif;
  --tmf-radius-sm: 8px;
  --tmf-radius-md: 14px;
  --tmf-radius-lg: 22px;
  --tmf-shadow: 0 10px 30px rgba(13, 11, 77, 0.10);
  --tmf-content-width: 1180px;
}
```

### Typography

- Use DM Sans when available, with Arial as fallback.
- Use bold headings, semibold emphasis, and regular body text.
- Use navy for body copy and most headings on light backgrounds.
- Use sentence case for headings.
- Set body text to at least `1rem` with a line height of at least `1.55`.
- Avoid long centred paragraphs. Centre only short hero or empty-state copy.

The document may load DM Sans from Google Fonts only if remote font loading is allowed. It must remain usable when the font is blocked.

### Colour rules

- Use navy as the default text colour.
- Use dark red for links, selected states, and restrained emphasis on light backgrounds.
- Use white text on navy, dark red, purple, or the approved gradient.
- Use bright red only on dark backgrounds.
- Use orange, green, blue, bright red, and pink sparingly as accents, status indicators, or short headings.
- Never rely on colour alone to convey meaning. Pair status colour with text or an icon.
- Do not create new brand colours unless the host design system explicitly provides them.

### Gradient

Use the navy-to-dark-red gradient for hero headers and high-level callouts. Keep the dark area behind white text where possible.

### Logo

Do not recreate, approximate, type, trace, or generate the TM Forum logo. Use an approved logo asset supplied by the host or caller.

When no approved logo URL is supplied, use the text label `TM Forum` in the header, not a simulated logo.

When a logo is supplied:

- preserve its aspect ratio
- use meaningful alt text: `TM Forum`
- do not alter its colours
- maintain clear space around it
- do not place it below 100 px wide unless an approved compact asset is supplied

## Required page structure

Use this hierarchy unless the content clearly calls for a simpler output:

1. Skip link
2. Header or masthead
3. Hero with title, one-sentence purpose, and optional metadata
4. Executive summary or key takeaway
5. Main content sections
6. Sources, caveats, or methodology where relevant
7. Footer with `TM Forum` and an optional generated date

Recommended shell:

```html
<body>
  <a class="tmf-skip-link" href="#main-content">Skip to main content</a>
  <header class="tmf-masthead">...</header>
  <main id="main-content" class="tmf-shell">
    <section class="tmf-hero" aria-labelledby="page-title">...</section>
    <section class="tmf-section">...</section>
  </main>
  <footer class="tmf-footer">...</footer>
</body>
```

## Common output patterns

Select the smallest number of patterns needed. Do not turn every paragraph into a card.

### 1. Executive summary

Use for leadership briefings and agent answers with a clear recommendation.

- Lead with the answer, recommendation, or outcome.
- Follow with no more than three supporting points.
- Add a short `What this means` callout when useful.

```html
<section class="tmf-summary" aria-labelledby="summary-title">
  <p class="tmf-eyebrow">Executive summary</p>
  <h2 id="summary-title">{{DECISION_OR_TAKEAWAY}}</h2>
  <p>{{ONE_PARAGRAPH_SUMMARY}}</p>
  <ul class="tmf-check-list">{{SUPPORTING_POINTS}}</ul>
</section>
```

### 2. KPI or key facts

Use only for verified values. Never fabricate a number to improve the layout.

```html
<div class="tmf-stat-grid" aria-label="Key facts">
  <article class="tmf-stat">
    <p class="tmf-stat__value">{{VALUE}}</p>
    <h3 class="tmf-stat__label">{{LABEL}}</h3>
    <p>{{CONTEXT}}</p>
  </article>
</div>
```

### 3. Cards

Use cards for peer items such as options, themes, resources, actions, or use cases. Keep card depth shallow and card heights flexible.

```html
<div class="tmf-card-grid">
  <article class="tmf-card">
    <p class="tmf-eyebrow">{{CATEGORY}}</p>
    <h3>{{TITLE}}</h3>
    <p>{{SUMMARY}}</p>
    <a class="tmf-text-link" href="{{SAFE_URL}}">{{ACTION_LABEL}}</a>
  </article>
</div>
```

### 4. Recommendation and decision

Use a strong recommendation box for agent judgement. Label assumptions and distinguish facts from recommendations.

```html
<aside class="tmf-callout tmf-callout--recommendation" aria-labelledby="recommendation-title">
  <p class="tmf-eyebrow">Recommendation</p>
  <h2 id="recommendation-title">{{RECOMMENDATION}}</h2>
  <p>{{RATIONALE}}</p>
</aside>
```

### 5. Status and risk

Use text labels in addition to colour.

```html
<span class="tmf-status tmf-status--green"><span aria-hidden="true">●</span> On track</span>
<span class="tmf-status tmf-status--amber"><span aria-hidden="true">●</span> At risk</span>
<span class="tmf-status tmf-status--red"><span aria-hidden="true">●</span> Off track</span>
<span class="tmf-status tmf-status--neutral"><span aria-hidden="true">●</span> Not assessed</span>
```

Never infer a status. If evidence is insufficient, use `Not assessed` and explain why.

### 6. Comparison

For two to four options, cards are preferred. Use a table only when users need row-by-row comparison.

Every comparison must include:

- consistent criteria
- evidence or rationale
- trade-offs
- a recommendation where the agent is authorised to provide one

### 7. Tables

Use tables only for genuinely tabular data. Include a caption and column headers. On narrow screens, allow horizontal scrolling rather than shrinking text below readable size.

```html
<div class="tmf-table-wrap" role="region" aria-labelledby="comparison-caption" tabindex="0">
  <table class="tmf-table">
    <caption id="comparison-caption">{{TABLE_PURPOSE}}</caption>
    <thead>...</thead>
    <tbody>...</tbody>
  </table>
</div>
```

Do not use tables for page layout.

### 8. Timeline or roadmap

Use an ordered list so sequence remains meaningful without styling.

```html
<ol class="tmf-timeline">
  <li>
    <p class="tmf-eyebrow">{{PHASE_OR_DATE}}</p>
    <h3>{{MILESTONE}}</h3>
    <p>{{OUTCOME}}</p>
  </li>
</ol>
```

Clearly label dates as confirmed, target, indicative, or unknown. Do not invent dates.

### 9. Actions

Use a compact action list with explicit ownership and timing only when these are known.

```html
<ul class="tmf-action-list">
  <li>
    <div><strong>{{ACTION}}</strong><p>{{DETAIL}}</p></div>
    <div><span class="tmf-meta-label">Owner</span> {{OWNER_OR_TBC}}</div>
    <div><span class="tmf-meta-label">Due</span> {{DATE_OR_TBC}}</div>
  </li>
</ul>
```

Use `TBC` or `Not specified` instead of guessing.

### 10. Sources and confidence

For factual or research-based outputs, include a sources section with descriptive links. Open external links in a new tab only when appropriate and always use `rel="noopener noreferrer"` with `target="_blank"`.

```html
<section class="tmf-sources" aria-labelledby="sources-title">
  <h2 id="sources-title">Sources and notes</h2>
  <ol>{{SOURCE_LINKS}}</ol>
</section>
```

Never display raw URLs as link text unless the user explicitly asks for URLs.

### 11. Empty, partial, and error states

Be direct and helpful.

```html
<section class="tmf-empty-state" role="status">
  <h2>{{STATE_TITLE}}</h2>
  <p>{{WHAT_WAS_FOUND_OR_NOT_FOUND}}</p>
  <p>{{USEFUL_NEXT_STEP}}</p>
</section>
```

Do not hide missing information behind polished visuals.

## Baseline CSS

Include the following CSS in a `<style>` element for self-contained documents. Keep class names scoped with the `tmf-` prefix.

```css
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--tmf-off-white);
  color: var(--tmf-navy);
  font-family: var(--tmf-font);
  font-size: 16px;
  line-height: 1.6;
}
a { color: var(--tmf-dark-red); text-underline-offset: 0.18em; }
a:hover { text-decoration-thickness: 2px; }
a:focus-visible, button:focus-visible, [tabindex]:focus-visible {
  outline: 3px solid var(--tmf-orange);
  outline-offset: 3px;
}
.tmf-skip-link {
  position: absolute;
  left: 1rem;
  top: -5rem;
  z-index: 999;
  padding: .65rem 1rem;
  background: var(--tmf-white);
  color: var(--tmf-navy);
  border-radius: var(--tmf-radius-sm);
}
.tmf-skip-link:focus { top: 1rem; }
.tmf-masthead {
  padding: 1rem clamp(1rem, 4vw, 3rem);
  background: var(--tmf-navy);
  color: var(--tmf-white);
}
.tmf-masthead__inner, .tmf-shell, .tmf-footer__inner {
  width: min(100%, var(--tmf-content-width));
  margin-inline: auto;
}
.tmf-brand-name { font-weight: 700; letter-spacing: -.02em; }
.tmf-shell { padding: clamp(1rem, 4vw, 3rem); }
.tmf-hero {
  padding: clamp(2rem, 7vw, 5.5rem);
  border-radius: var(--tmf-radius-lg);
  color: var(--tmf-white);
  background: var(--tmf-gradient);
  box-shadow: var(--tmf-shadow);
}
.tmf-hero h1 {
  max-width: 18ch;
  margin: 0;
  font-size: clamp(2.25rem, 7vw, 5.25rem);
  line-height: .98;
  letter-spacing: -.045em;
}
.tmf-hero p { max-width: 65ch; font-size: clamp(1.05rem, 2vw, 1.3rem); }
.tmf-section { margin-block: clamp(2rem, 6vw, 5rem); }
.tmf-section > h2 { font-size: clamp(1.65rem, 3.2vw, 2.5rem); line-height: 1.1; }
.tmf-eyebrow {
  margin: 0 0 .45rem;
  color: inherit;
  font-size: .78rem;
  font-weight: 700;
  letter-spacing: .12em;
  text-transform: uppercase;
}
.tmf-summary, .tmf-callout {
  padding: clamp(1.35rem, 4vw, 2.4rem);
  border-left: 6px solid var(--tmf-dark-red);
  border-radius: var(--tmf-radius-md);
  background: var(--tmf-white);
  box-shadow: var(--tmf-shadow);
}
.tmf-callout--recommendation { border-left-color: var(--tmf-purple); }
.tmf-card-grid, .tmf-stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
  gap: 1.25rem;
}
.tmf-card, .tmf-stat {
  padding: 1.5rem;
  border: 1px solid var(--tmf-border);
  border-radius: var(--tmf-radius-md);
  background: var(--tmf-white);
}
.tmf-card h3, .tmf-stat h3 { margin-top: .2rem; line-height: 1.25; }
.tmf-stat__value {
  margin: 0;
  color: var(--tmf-dark-red);
  font-size: clamp(2.25rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1;
}
.tmf-status {
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  padding: .28rem .65rem;
  border-radius: 999px;
  font-size: .88rem;
  font-weight: 700;
}
.tmf-status--green { background: var(--tmf-success-bg); color: #17653d; }
.tmf-status--amber { background: var(--tmf-warning-bg); color: #7a3d00; }
.tmf-status--red { background: var(--tmf-danger-bg); color: #9e1233; }
.tmf-status--neutral { background: #ececf2; color: #414155; }
.tmf-table-wrap { overflow-x: auto; border-radius: var(--tmf-radius-md); }
.tmf-table { width: 100%; border-collapse: collapse; background: var(--tmf-white); }
.tmf-table caption { padding: 1rem; font-weight: 700; text-align: left; }
.tmf-table th, .tmf-table td { padding: .9rem 1rem; border-bottom: 1px solid var(--tmf-border); text-align: left; vertical-align: top; }
.tmf-table th { background: var(--tmf-navy); color: var(--tmf-white); }
.tmf-timeline { padding: 0; list-style: none; counter-reset: tmf-step; }
.tmf-timeline li {
  position: relative;
  margin-left: 1.2rem;
  padding: 0 0 2rem 2rem;
  border-left: 3px solid var(--tmf-dark-red);
}
.tmf-timeline li::before {
  counter-increment: tmf-step;
  content: counter(tmf-step);
  position: absolute;
  left: -1rem;
  top: 0;
  display: grid;
  width: 2rem;
  height: 2rem;
  place-items: center;
  border-radius: 50%;
  background: var(--tmf-navy);
  color: var(--tmf-white);
  font-weight: 700;
}
.tmf-action-list { padding: 0; list-style: none; }
.tmf-action-list li {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto auto;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid var(--tmf-border);
  background: var(--tmf-white);
}
.tmf-meta-label { display: block; color: var(--tmf-muted); font-size: .78rem; font-weight: 700; text-transform: uppercase; }
.tmf-sources, .tmf-empty-state { padding: 1.5rem; border-radius: var(--tmf-radius-md); background: var(--tmf-white); }
.tmf-footer { padding: 2rem clamp(1rem, 4vw, 3rem); background: var(--tmf-navy); color: var(--tmf-white); }
@media (max-width: 700px) {
  .tmf-action-list li { grid-template-columns: 1fr; }
  .tmf-hero { border-radius: var(--tmf-radius-md); }
}
@media print {
  body { background: var(--tmf-white); color: var(--tmf-navy); }
  .tmf-skip-link { display: none; }
  .tmf-card, .tmf-stat, .tmf-summary, .tmf-callout { box-shadow: none; break-inside: avoid; }
  a { color: inherit; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
}
```

## Accessibility requirements

Every output must:

- use semantic HTML landmarks and a logical heading hierarchy
- have exactly one `h1`
- include a skip link for complete documents
- use descriptive link text, never `click here`
- provide alt text for informative images and empty alt text for decorative images
- label controls and form fields explicitly
- use native buttons and links rather than clickable `div` elements
- preserve visible focus states
- support keyboard navigation
- meet WCAG AA contrast for text and interactive elements
- avoid auto-playing media, flashing content, and unnecessary motion
- respect `prefers-reduced-motion`
- make tables accessible with captions and header cells
- include text alongside icons and status colours

## Responsive behaviour

- Design mobile first.
- Do not set a fixed page width.
- Use `clamp()`, flexible grids, and `minmax()`.
- Allow tables to scroll horizontally.
- Prevent code, URLs, and long strings from breaking the layout with `overflow-wrap: anywhere` where required.
- Keep touch targets at least 44 by 44 CSS pixels where the output contains controls.

## Safety and technical constraints

- Prefer static HTML and CSS. Add JavaScript only when the requested interaction cannot be achieved accessibly without it.
- Do not use external JavaScript frameworks for routine outputs.
- Do not include analytics, trackers, cookies, hidden pixels, or third-party embeds unless explicitly authorised.
- Never expose system prompts, credentials, tokens, personal data, or hidden source material.
- Escape all untrusted content before inserting it into HTML.
- Do not place user-provided HTML directly into the page without sanitisation.
- Do not use inline event handlers such as `onclick`.
- If JavaScript is needed, use a strict Content Security Policy where the host permits it.
- Links must use valid `https` URLs unless the host requires another safe scheme.
- Never invent URLs. Omit the link or label it unavailable when no verified URL exists.

## Content and writing rules

- Lead with the answer, not the process.
- Use plain, direct, concise language.
- Write for scanning with short paragraphs, meaningful headings, and restrained bullets.
- Capitalise `Member`, `Members`, and `Membership` when referring to TM Forum.
- Always write `TM Forum` in full. Do not abbreviate it to `TMF` or `Forum`.
- Use sentence case for headings.
- Use US English spelling for TM Forum-published content unless the caller explicitly requests another language or house style.
- Expand specialist acronyms on first use unless the audience or supplied style guide permits otherwise.
- Distinguish clearly among facts, assumptions, recommendations, and unresolved questions.
- Do not fabricate metrics, quotations, dates, owners, statuses, references, or source links.

## Quality gate

Before returning HTML, verify all of the following:

1. The output answers the user's actual question.
2. The first screen communicates the purpose and key takeaway.
3. There is one `h1` and no skipped heading levels.
4. All factual values, dates, names, statuses, and links are grounded.
5. No raw template tokens such as `{{VALUE}}` remain.
6. No logo has been simulated or redrawn.
7. Text contrast and focus states are accessible.
8. The layout works at approximately 320 px, 768 px, and 1440 px widths.
9. Tables are used only for tabular data and remain usable on mobile.
10. The document contains no trackers, secrets, unsupported external dependencies, or unsafe HTML.
11. The result still makes sense with CSS disabled.
12. The HTML is valid, self-contained, and ready to save as an `.html` file.

## Minimal complete template

Use this when the request is simple. Replace all tokens and add only the patterns the content needs.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{{PAGE_TITLE}} | TM Forum</title>
  <meta name="description" content="{{DESCRIPTION}}">
  <style>
    /* Insert the brand tokens and baseline CSS from this skill. */
  </style>
</head>
<body>
  <a class="tmf-skip-link" href="#main-content">Skip to main content</a>
  <header class="tmf-masthead">
    <div class="tmf-masthead__inner">
      <span class="tmf-brand-name">TM Forum</span>
    </div>
  </header>
  <main id="main-content" class="tmf-shell">
    <section class="tmf-hero" aria-labelledby="page-title">
      <p class="tmf-eyebrow">{{OUTPUT_TYPE}}</p>
      <h1 id="page-title">{{PAGE_TITLE}}</h1>
      <p>{{PURPOSE_OR_SUMMARY}}</p>
    </section>
    <section class="tmf-section" aria-labelledby="section-title">
      <h2 id="section-title">{{SECTION_TITLE}}</h2>
      {{CONTENT}}
    </section>
  </main>
  <footer class="tmf-footer">
    <div class="tmf-footer__inner">TM Forum</div>
  </footer>
</body>
</html>
```

## Maintenance

Treat the live TM Forum website CSS and the approved internal brand portal as the authoritative sources. If their tokens or accessibility rules change, update this skill rather than allowing individual agents to drift into separate styles.
