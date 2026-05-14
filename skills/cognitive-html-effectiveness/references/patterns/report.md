# Pattern: Report

Recurring structured documents — status updates, post-mortems, weekly summaries — where structure and color turn something people skim into something they actually read.

## When to use

- User asks for a "reporte semanal", "status update", "weekly report"
- User wants a "post-mortem", "incident report", "análisis de incidente"
- User says "hazme un resumen de la semana", "qué pasó esta semana"
- User references dates and metrics that need to be presented

## Two sub-patterns

### A) Status Report (weekly update)

```
┌──────────────────────────────────────────────────┐
│ Header                                            │
│   Title + auto-generated badge + date range       │
├──────────────────────────────────────────────────┤
│ Summary Band (4 stat cards)                        │
│   PRs merged | Deploys | Incidents | Tests       │
├──────────────────────────────────────────────────┤
│ Highlights                                        │
│   ● Bullet list with bold keywords                │
├──────────────────────────────────────────────────┤
│ Shipped table                                     │
│   PR# | Title | Author | Risk                    │
├──────────────────────────────────────────────────┤
│ Velocity chart (SVG bar chart)                    │
├──────────────────────────────────────────────────┤
│ Carryover                                         │
│   In review / Blocked / Slipped items            │
├──────────────────────────────────────────────────┤
│ Footer: sources, generation timestamp             │
└──────────────────────────────────────────────────┘
```

### B) Incident Report (post-mortem)

```
┌──────────────────────────────────────────────────┐
│ Header                                            │
│   Incident ID + title + severity/duration pills   │
├──────────────────────────────────────────────────┤
│ TL;DR Box (dark bg)                                │
│   What happened, impact, resolution in 2-3 lines  │
├──────────────────────────────────────────────────┤
│ Timeline                                          │
│   ●── Normal                                     │
│   ●── Impact starts (colored)                     │
│   ●── Diagnostic steps                            │
│   ●── Mitigated (green)                           │
│   ●── Resolved                                    │
├──────────────────────────────────────────────────┤
│ Root cause                                        │
│   Narrative + code diff panel                     │
├──────────────────────────────────────────────────┤
│ Impact table                                      │
│   Requests failed | Peak error | Users | Data loss│
├──────────────────────────────────────────────────┤
│ Action items (checklist with owners and dates)     │
├──────────────────────────────────────────────────┤
│ Footer: author, reviewers, timestamp              │
└──────────────────────────────────────────────────┘
```

## Component prescriptions

| For status report | Component |
|-------------------|-----------|
| Summary band | **Summary Band / Stat Cards** — `components.md` § 2 |
| Highlights | Custom bullet list with clay dots |
| Shipped table | **Data Table** — `components.md` § 11 |
| Chart | Inline SVG bar chart |
| Carryover | Custom card with tags (in review / blocked / slipped) |

| For incident report | Component |
|--------------------|-----------|
| TL;DR | **TL;DR Box** — `components.md` § 1 |
| Severity/duration pills | **Chip / Tag (pills)** — `components.md` § 4 |
| Timeline | **Timeline** — `components.md` § 5 |
| Root cause code | **Code Panel** — `components.md` § 7 |
| Impact | **Data Table** — `components.md` § 11 |
| Action items | **Action Items / Checklist** — `components.md` § 10 |

## Foundation shell

Use this page shell before adding status-report or incident-report content:

```html
<body>
  <div class="page report-page">
    <header class="page-header">...</header>
    <main class="page-main">...</main>
    <footer class="page-footer">...</footer>
  </div>
</body>
```

```css
body {
  margin: 0;
  background: var(--bg-page);
  color: var(--text-primary);
  font-family: var(--sans);
  font-size: var(--text-body);
  line-height: var(--lh-body);
}
.page {
  max-width: var(--container-page);
  margin: 0 auto;
  padding: var(--page-padding-block) var(--page-padding-inline) calc(var(--page-padding-block) * 1.5);
}
.page-main {
  display: grid;
  gap: var(--section-gap);
}
.page-header > * { margin-top: 0; }
.page-header {
  margin-bottom: var(--section-gap);
}
.page-footer {
  margin-top: var(--section-gap);
  padding-top: var(--space-5);
  border-top: 1px solid var(--gray-300);
  color: var(--text-muted);
  font-size: var(--text-small);
}
.measure {
  max-width: var(--container-reading);
}
```

## Status report — key details

### Auto-generated badge

```html
<span class="auto-pill">auto-generated</span>
```

```css
.auto-pill {
  font-family: var(--mono); font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text-muted); background: var(--bg-muted);
  border: var(--border); border-radius: var(--radius-pill);
  padding: 5px 11px; white-space: nowrap;
}
```

### Shipped table with risk dots

Each row has a risk indicator:

```html
<td><span class="risk"><span class="risk-dot low"></span>Low</span></td>
```

```css
.risk { display: inline-flex; align-items: center; gap: 7px; font-size: 12px; color: var(--text-muted); }
.risk-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
.risk-dot.low  { background: var(--color-success); }
.risk-dot.med  { background: var(--color-warning); }
.risk-dot.high { background: var(--color-danger); }
```

### Velocity chart

Use an SVG bar chart. Bars are `<rect>` elements. The peak bar gets the clay color, others get oat. Include gridlines, y-axis labels, x-axis labels, and value labels.

### Carryover section

```html
<div class="carryover">
  <div class="carry-item">
    <span class="carry-tag">In review</span>
    <div class="carry-body">Workspace export to CSV — waiting on pagination review.</div>
  </div>
</div>
```

```css
.carryover { background: var(--bg-accent); border-radius: var(--radius-panel); padding: 20px 22px; }
.carry-item { display: flex; align-items: baseline; gap: 14px; padding: 8px 0; }
.carry-item + .carry-item { border-top: 1px solid color-mix(in srgb, var(--slate) 8%, var(--white)); }
.carry-tag {
  font-family: var(--mono); font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--text-secondary); background: var(--ivory); border-radius: 4px; padding: 3px 7px; flex-shrink: 0;
}
```

## Incident report — key details

### Timeline with colored dots

The timeline is THE centerpiece of a post-mortem. Use `components.md` § 5 exactly as specified.

### Root cause: narrative + diff

Always pair a prose explanation with a code diff panel showing exactly what changed.

### Action items as a checklist

Every post-mortem ends with concrete, assigned, dated action items. Each item has: checkbox, owner avatar (initials), description, due date.

## Generating real content

These reports are most powerful when generated from real data:
- `git log` for PR lists and authors
- Deploy logs for incident timelines
- CI dashboards for test pass rates
- Alert history for severity and duration

When the user provides a date range, pull real data from these sources before generating the HTML.

## Styling rules specific to reports

- Keep narrative sections inside a `.measure` wrapper so post-mortem prose does not become a wall of text.
- Use the same heading rhythm on every report: title, section heading, body/meta.
- Status cards, tables, and action lists should reuse component spacing/radius/borders exactly as documented.
- Charts and timelines can extend wider than prose, but they still live inside the same page shell.
- Use warning/danger colors sparingly; if everything is loud, nothing is important.

## Full examples

- **Status report**: See `resources/11-status-report.html` in the project — Engineering Status Week 11 with summary band, shipped table, velocity chart, and carryover
- **Incident report**: See `resources/12-incident-report.html` in the project — INC-2025-0412 post-mortem with timeline, root cause diff, impact table, and action items
