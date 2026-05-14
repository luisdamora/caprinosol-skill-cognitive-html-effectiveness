# Component Catalog — Reusable UI Building Blocks

Every pattern in this skill composes from this catalog. When generating HTML,
use these components as templates — copy the HTML structure and CSS, fill in
the content. Do NOT invent new component patterns unless the user's request
genuinely demands something beyond this catalog.

## Table of Contents

1.  [TL;DR Box](#1-tldr-box)
2.  [Summary Band / Stat Cards](#2-summary-band--stat-cards)
3.  [Tradeoff Table](#3-tradeoff-table)
4.  [Chip / Tag](#4-chip--tag)
5.  [Timeline](#5-timeline)
6.  [Collapsible (Details/Summary)](#6-collapsible-detailssummary)
7.  [Code Panel](#7-code-panel)
8.  [Tabbed Interface](#8-tabbed-interface)
9.  [Callout / Note](#9-callout--note)
10. [Action Items / Checklist](#10-action-items--checklist)
11. [Data Table](#11-data-table)
12. [Progress Bar](#12-progress-bar)
13. [Decision Card](#13-decision-card)
14. [FAQ Section](#14-faq-section)
15. [Sidebar Navigation](#15-sidebar-navigation)

---

## 1. TL;DR Box

The first thing a reader sees. Dark background, high contrast, answers "what happened" in 2-3 sentences.

```html
<div class="tldr">
  <div class="tldr-label">TL;DR</div>
  <p>
    <strong>What happened</strong> — concise explanation.
    <strong>Impact</strong> — what it affected.
    <strong>Resolution</strong> — how it was fixed or what to do next.
  </p>
</div>
```

```css
.tldr {
  background: var(--slate);
  color: var(--ivory);
  border-radius: var(--radius-panel);
  padding: 22px 26px;
  margin-bottom: 48px;
}
.tldr-label {
  font-family: var(--mono);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--oat);
  margin-bottom: 10px;
}
.tldr p { margin: 0; font-size: 15.5px; line-height: 1.65; }
.tldr code {
  font-family: var(--mono);
  font-size: 13.5px;
  background: rgba(250,249,245,0.12);
  padding: 1px 5px;
  border-radius: 4px;
}
```

---

## 2. Summary Band / Stat Cards

A horizontal row of metric cards. Use for dashboards, status reports, KPIs.

```html
<div class="summary-band">
  <div class="stat-card">
    <div class="stat-num">14</div>
    <div class="stat-label">PRs merged</div>
    <div class="stat-delta up">+3 vs last week</div>
  </div>
  <div class="stat-card warn">
    <div class="stat-num">1</div>
    <div class="stat-label">Incidents</div>
    <div class="stat-delta flat">SEV-2 · 47m</div>
  </div>
</div>
```

```css
.summary-band {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px;
}
.stat-card {
  background: var(--bg-card);
  border: var(--border);
  border-radius: var(--radius-panel);
  padding: 20px 22px 18px;
}
.stat-card.warn { border-left: 4px solid var(--color-warning); padding-left: 19px; }
.stat-num {
  font-family: var(--serif);
  font-size: 44px;
  font-weight: 500;
  line-height: 1;
  color: var(--text-primary);
  margin-bottom: 8px;
}
.stat-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}
.stat-delta { font-family: var(--mono); font-size: 11px; margin-top: 6px; }
.stat-delta.up   { color: var(--color-success); }
.stat-delta.down { color: var(--color-success); }
.stat-delta.flat { color: var(--text-muted); }
```

---

## 3. Tradeoff Table

Side-by-side pros and cons. Use for comparison patterns.

```html
<div class="tradeoffs">
  <div class="row head">
    <div class="cell">Pro</div>
    <div class="cell">Con</div>
  </div>
  <div class="row">
    <div class="cell pro">Simple, no new dependencies</div>
    <div class="cell con">Logic duplicated everywhere</div>
  </div>
  <div class="row">
    <div class="cell pro">Easy to step through in devtools</div>
    <div class="cell con">Two pieces of state for one value</div>
  </div>
</div>
```

```css
.tradeoffs {
  border: var(--border);
  border-radius: var(--radius-row);
  overflow: hidden;
  font-size: 13px;
}
.tradeoffs .row {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
.tradeoffs .row + .row { border-top: var(--border); }
.tradeoffs .cell { padding: 10px 14px; }
.tradeoffs .cell:first-child { border-right: var(--border); }
.tradeoffs .head {
  background: var(--bg-muted);
  font-weight: 600;
  color: var(--text-primary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.tradeoffs .pro::before,
.tradeoffs .con::before {
  content: '';
  display: inline-block;
  width: 6px; height: 6px;
  border-radius: 50%;
  margin-right: 8px;
  vertical-align: 2px;
}
.tradeoffs .pro::before { background: var(--color-success); }
.tradeoffs .con::before { background: var(--color-warning); }
```

---

## 4. Chip / Tag

Small label for metadata: severity, type, status, estimate.

```html
<!-- severity pills -->
<span class="pill sev">SEV-2</span>
<span class="pill resolved">Resolved</span>
<span class="pill neutral"><span class="k">Duration</span> 47 min</span>

<!-- feature/bug tags -->
<span class="tag tag-bug">bug</span>
<span class="tag tag-feat">feature</span>
<span class="tag tag-chore">chore</span>
<span class="tag tag-debt">tech debt</span>
```

```css
.pill {
  display: inline-flex;
  align-items: baseline;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  border-radius: var(--radius-pill);
  padding: 5px 12px;
  line-height: 1;
}
.pill.sev      { background: var(--color-warning); color: var(--white); }
.pill.resolved { background: var(--color-success); color: var(--white); }
.pill.neutral  { background: var(--bg-muted); color: var(--text-secondary); border: var(--border); }

.tag {
  font-family: var(--mono);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: var(--radius-pill);
  padding: 1px 7px 2px;
  border: 1px solid transparent;
}
.tag-bug   { background: #F5E2D8; color: var(--clay-d); border-color: #E8C9BA; }
.tag-feat  { background: #E8EDE0; color: #5C6F44; border-color: #CFDAC0; }
.tag-chore { background: var(--bg-muted); color: var(--text-secondary); border-color: var(--gray-200); }
.tag-debt  { background: var(--bg-muted); color: var(--text-secondary); border-color: var(--gray-200); }
```

---

## 5. Timeline

Vertical timeline with dots and timestamps. Use for incident reports, project plans, changelogs.

```html
<div class="timeline">
  <div class="tl-entry">
    <span class="tl-dot"></span>
    <span class="tl-time">14:02</span>
    <div class="tl-body">Config change promoted to production.</div>
  </div>
  <div class="tl-entry">
    <span class="tl-dot impact"></span>
    <span class="tl-time">14:06</span>
    <div class="tl-body"><strong>Impact starts.</strong> Workers begin queueing.</div>
  </div>
  <div class="tl-entry">
    <span class="tl-dot mitigated"></span>
    <span class="tl-time">14:44</span>
    <div class="tl-body"><strong>Mitigated.</strong> Config reverted.</div>
  </div>
</div>
```

```css
.timeline {
  position: relative;
  padding: 4px 0 4px 16px;
}
.timeline::before {
  content: "";
  position: absolute;
  left: 16px; top: 8px; bottom: 8px;
  width: 2px;
  background: var(--gray-300);
}
.tl-entry {
  position: relative;
  padding: 0 0 22px 28px;
}
.tl-entry:last-child { padding-bottom: 0; }
.tl-dot {
  position: absolute;
  left: -5px; top: 6px;
  width: 12px; height: 12px;
  border-radius: 50%;
  background: var(--gray-500);
  border: 2px solid var(--ivory);
  box-sizing: content-box;
}
.tl-dot.impact    { background: var(--color-warning); }
.tl-dot.mitigated { background: var(--color-success); }
.tl-time {
  display: inline-block;
  font-family: var(--mono);
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-muted);
  border: 1px solid var(--gray-300);
  border-radius: 6px;
  padding: 2px 8px;
  margin-bottom: 6px;
}
.tl-body { font-size: 14px; color: var(--text-secondary); }
.tl-body strong { color: var(--text-primary); font-weight: 600; }
```

---

## 6. Collapsible (Details/Summary)

Progressive disclosure. Use for step-by-step walkthroughs, optional details, "show source" blocks.

```html
<details class="snippet">
  <summary>1 · Identify the caller <span class="where">middleware/ratelimit.ts:21</span></summary>
  <div class="body">
    <p>The middleware reduces the request to a bucket key...</p>
  </div>
</details>
```

```css
details.snippet {
  border: var(--border);
  border-radius: 10px;
  background: var(--bg-card);
  margin: 14px 0;
  overflow: hidden;
}
details.snippet summary {
  list-style: none;
  cursor: pointer;
  padding: 14px 16px;
  font-family: var(--serif);
  font-size: 16px;
  color: var(--text-primary);
  display: flex;
  align-items: baseline;
  gap: 10px;
}
details.snippet summary::-webkit-details-marker { display: none; }
details.snippet summary::before {
  content: "▸";
  color: var(--clay);
  font-size: 12px;
  transition: transform 120ms;
}
details.snippet[open] summary::before { transform: rotate(90deg); }
details.snippet summary .where {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-muted);
  margin-left: auto;
}
details.snippet .body { padding: 0 16px 16px; }
```

**"At most one open" JS** (for walkthroughs where too many open snippets break scanning):

```js
document.querySelectorAll('details.snippet').forEach(d => {
  d.addEventListener('toggle', () => {
    if (!d.open) return;
    document.querySelectorAll('details.snippet').forEach(other => {
      if (other !== d) other.open = false;
    });
  });
});
```

---

## 7. Code Panel

Dark background code block. Use for diffs, config snippets, source code.

```html
<div class="code-panel">
  <span class="path">infra/config/workers.yaml</span>
  <div class="diff-line ctx">   pool:</div>
  <div class="diff-line del">-      max_connections: 64</div>
  <div class="diff-line add">+      max_connections: 8   # debug, do not ship</div>
</div>
```

```css
.code-panel {
  background: var(--slate);
  color: var(--gray-100);
  border-radius: var(--radius-panel);
  padding: 18px 20px;
  font-family: var(--mono);
  font-size: 13px;
  line-height: 1.7;
  overflow-x: auto;
  margin: 8px 0 4px;
}
.code-panel .path {
  color: var(--gray-500);
  font-size: 12px;
  margin-bottom: 10px;
  display: block;
}
.diff-line { white-space: pre; }
.diff-line.ctx { color: var(--gray-300); }
.diff-line.del { color: #E0897A; }
.diff-line.add { color: #A3B88A; }
```

---

## 8. Tabbed Interface

Multiple views in a single space. Use for config examples, language variants, before/after.

```html
<div class="tabs">
  <div class="tabbar">
    <button class="on" data-t="0">limits.yaml</button>
    <button data-t="1">route.ts</button>
    <button data-t="2">client response</button>
  </div>
  <pre class="on"><code># config/limits.yaml ...</code></pre>
  <pre><code>// routes/search.ts ...</code></pre>
  <pre><code>HTTP/1.1 429 Too Many Requests ...</code></pre>
</div>
```

```css
.tabs {
  border: var(--border);
  border-radius: 10px;
  background: var(--bg-card);
  margin: 16px 0 8px;
  overflow: hidden;
}
.tabbar {
  display: flex;
  border-bottom: 1px solid var(--gray-300);
  background: var(--bg-muted);
}
.tabbar button {
  appearance: none; border: none; background: none;
  font-family: var(--mono);
  font-size: 12px;
  color: var(--text-muted);
  padding: 10px 16px;
  cursor: pointer;
  border-right: 1px solid var(--gray-300);
}
.tabbar button.on {
  background: var(--bg-card);
  color: var(--text-primary);
  border-bottom: 2px solid var(--clay);
  margin-bottom: -1px;
}
.tabs pre { display: none; margin: 0; padding: 16px 18px; }
.tabs pre.on { display: block; }
```

```js
document.querySelectorAll("[data-tabs]").forEach(box => {
  const btns = box.querySelectorAll("button");
  const panes = box.querySelectorAll("pre");
  btns.forEach(b => b.addEventListener("click", () => {
    btns.forEach(x => x.classList.remove("on"));
    panes.forEach(x => x.classList.remove("on"));
    b.classList.add("on");
    panes[+b.dataset.t].classList.add("on");
  }));
});
```

---

## 9. Callout / Note

Highlighted sidebar note. Use for tips, warnings, "heads up" messages.

```html
<div class="callout">
  <span class="ico">★</span>
  <div>If you only need the default tier, you don't need a YAML entry at all.</div>
</div>
```

```css
.callout {
  display: flex;
  gap: 12px;
  border: 1.5px solid var(--oat);
  background: rgba(227,218,204,0.35);
  border-radius: 10px;
  padding: 14px 16px;
  margin: 18px 0;
  font-size: 14px;
}
.callout .ico { color: var(--clay); font-weight: 600; flex-shrink: 0; }
```

---

## 10. Action Items / Checklist

Trackable tasks with checkboxes and owners. Use for post-mortem follow-ups, implementation plans.

```html
<div class="actions">
  <div class="ai-row done">
    <span class="ai-check"></span>
    <span class="ai-avatar">DP</span>
    <span class="ai-desc">Revert config and restore pool limit</span>
    <span class="ai-due">Apr 12</span>
  </div>
  <div class="ai-row">
    <span class="ai-check"></span>
    <span class="ai-avatar">MO</span>
    <span class="ai-desc">Add config-linter range check</span>
    <span class="ai-due">Apr 18</span>
  </div>
</div>
```

```css
.actions {
  background: var(--bg-card);
  border: var(--border);
  border-radius: var(--radius-panel);
  overflow: hidden;
}
.ai-row {
  display: grid;
  grid-template-columns: 36px 36px 1fr 96px;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  border-bottom: 1px solid var(--gray-100);
}
.ai-row:last-child { border-bottom: none; }
.ai-row.done .ai-desc {
  color: var(--text-muted);
  text-decoration: line-through;
  text-decoration-color: var(--gray-300);
}
.ai-check {
  width: 18px; height: 18px;
  border: 1.5px solid var(--gray-300);
  border-radius: 5px;
}
.ai-row.done .ai-check { background: var(--color-success); border-color: var(--color-success); }
.ai-row.done .ai-check::after {
  content: ""; position: absolute;
  left: 4px; top: 1px;
  width: 5px; height: 9px;
  border: solid var(--white);
  border-width: 0 2px 2px 0;
  transform: rotate(40deg);
}
.ai-avatar {
  width: 30px; height: 30px;
  border-radius: 50%;
  background: var(--oat);
  font-size: 11px; font-weight: 600;
  display: flex; align-items: center; justify-content: center;
}
.ai-due { font-family: var(--mono); font-size: 12px; color: var(--text-muted); text-align: right; }
```

---

## 11. Data Table

Structured data with headers. Use for PR lists, comparison data, specs.

```html
<table class="data-table">
  <thead>
    <tr>
      <th>PR</th><th>Title</th><th>Author</th><th style="width:100px">Risk</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="#">#4871</a></td>
      <td>Bulk edit toolbar</td>
      <td>Mira Okafor</td>
      <td><span class="risk"><span class="risk-dot med"></span>Med</span></td>
    </tr>
  </tbody>
</table>
```

```css
table.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: var(--bg-card);
  border: var(--border);
  border-radius: var(--radius-panel);
  overflow: hidden;
}
table.data-table thead th {
  text-align: left;
  font-size: 11px; font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  background: var(--bg-muted);
  padding: 12px 16px;
  border-bottom: 1px solid var(--gray-300);
}
table.data-table tbody td {
  padding: 13px 16px;
  border-bottom: 1px solid var(--gray-100);
  font-size: 14px;
  vertical-align: middle;
}
table.data-table tbody tr:last-child td { border-bottom: none; }
table.data-table tbody tr:hover { background: var(--ivory); }
```

---

## 12. Progress Bar

Visual progress indicator. Use for project status, completion percentages.

```html
<div class="prog-item">
  <div class="prog-head">
    <span class="prog-title">Recurring tasks engine</span>
    <span class="prog-pct">~70%</span>
  </div>
  <div class="prog-track"><div class="prog-fill" style="width:70%"></div></div>
  <p class="prog-note">Scheduler and RRULE parsing are done; remaining: timezone edge cases.</p>
</div>
```

```css
.prog-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px; }
.prog-title { font-family: var(--serif); font-size: 20px; font-weight: 500; }
.prog-pct { font-family: var(--mono); font-size: 12px; color: var(--text-muted); }
.prog-track { width: 100%; height: 5px; background: var(--bg-muted); border-radius: 3px; overflow: hidden; }
.prog-fill { height: 100%; background: var(--clay); border-radius: 3px; }
.prog-note { font-size: 13px; line-height: 1.55; color: var(--text-secondary); }
```

---

## 13. Decision Card

A framed question for the reader to decide. Use for slide decks, planning docs.

```html
<div class="decision-card">
  <p class="decision-q">Do we ship behind a flag in 2.4, or hold for timezone fixes?</p>
  <p class="decision-context">Flagged gets it to partners Friday but means two code paths for ~2 weeks.</p>
  <div class="options">
    <span class="chip lean">A — Flag it, ship Friday</span>
    <span class="chip">B — Hold for 2.5</span>
  </div>
</div>
```

```css
.decision-card {
  border: 1.5px solid var(--clay);
  border-radius: 14px;
  padding: 36px 38px;
  background: rgba(217,119,87,0.06);
}
.decision-q { font-family: var(--serif); font-size: 24px; line-height: 1.4; margin-bottom: 12px; }
.decision-context { font-size: 14px; line-height: 1.6; color: var(--gray-300); }
.options { display: flex; gap: 14px; margin-top: 32px; flex-wrap: wrap; }
.chip {
  font-family: var(--mono); font-size: 12px;
  padding: 10px 18px; border-radius: var(--radius-pill);
  border: 1px solid var(--gray-700);
  color: var(--ivory); background: transparent;
}
.chip.lean { border-color: var(--clay); color: var(--clay); }
```

---

## 14. FAQ Section

Question/answer pairs. Use at the end of explainers, docs, incident reports.

```html
<dl class="faq">
  <dt>How do I exempt internal traffic?</dt>
  <dd>Set <code>x-acme-internal: 1</code> from the caller; the middleware skips the bucket.</dd>

  <dt>Where do I see who's getting limited?</dt>
  <dd>Every <code>429</code> emits a <code>ratelimit.rejected</code> metric.</dd>
</dl>
```

```css
dl.faq dt {
  font-family: var(--serif);
  font-size: 16px;
  color: var(--text-primary);
  margin-top: 18px;
}
dl.faq dd { font-size: 14px; margin: 4px 0 0; max-width: 640px; color: var(--text-secondary); }
```

---

## 15. Sidebar Navigation

Sticky sidebar with "On this page" links. Use for long documents.

```html
<nav class="side-nav">
  <div class="label">On this page</div>
  <a href="#tldr">TL;DR</a>
  <a href="#timeline">Timeline</a>
  <a href="#root-cause">Root cause</a>
  <a href="#actions">Action items</a>
  <div class="files">
    <div class="label">Files read</div>
    <code>middleware/auth.ts</code>
    <code>lib/sessionStore.ts</code>
  </div>
</nav>
```

```css
.side-nav {
  position: sticky;
  top: 32px;
  align-self: start;
  font-size: 13px;
}
.side-nav .label {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 12px;
}
.side-nav a {
  display: block;
  padding: 5px 0 5px 12px;
  border-left: 2px solid var(--gray-300);
  color: var(--text-secondary);
  text-decoration: none;
}
.side-nav a:hover { color: var(--text-primary); border-color: var(--text-primary); }
.side-nav .files { margin-top: 28px; border-top: 1px solid var(--gray-300); padding-top: 16px; }
.side-nav .files code { display: block; font-family: var(--mono); font-size: 11px; color: var(--text-muted); padding: 3px 0; }
```

---

## Composition rules

1.  **Start with TL;DR or Summary Band** — every page needs a "why should I care" signal in the first viewport.
2.  **Use at most 4-5 component types per page** — too many different visual patterns create cognitive noise.
3.  **Consistent spacing** — 48-56px between main sections, 14-22px between items within a section.
4.  **Color has meaning** — warm colors (clay, rust) signal attention/warning; cool colors (olive) signal success/safety; grays are structure.
5.  **Every interactive page needs an export button** — "Copy as markdown" or "Copy as JSON". The artifact must leave the page.
