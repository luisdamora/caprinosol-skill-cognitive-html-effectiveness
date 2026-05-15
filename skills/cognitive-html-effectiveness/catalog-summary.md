# Cognitive HTML — Template Catalog

LLM entry point for template-based HTML generation. Write manifest.json → generate.py → output.html.

## Quickstart

1. Write `manifest.json` (see schema below)
2. Run: `python scripts/generate.py manifest.json --output output.html`
3. Open `output.html` in any browser

## Patterns (10)

| Pattern | Template | Description |
|---------|----------|-------------|
| comparison | `templates/patterns/comparison.html` | Side-by-side tradeoff analysis with approach cards and recommendation |
| walkthrough | `templates/patterns/walkthrough.html` | Step-by-step code flow or architecture tour with collapsible steps |
| review | `templates/patterns/review.html` | Annotated diff/PR analysis with severity tags and file-by-file breakdown |
| design-system | `templates/patterns/design-system.html` | Color swatches, typography scale, spacing tokens, component showcase |
| prototyping | `templates/patterns/prototyping.html` | Animation sandbox with CSS controls and live preview |
| diagram | `templates/patterns/diagram.html` | Flowchart or architecture diagram with SVG and clickable nodes |
| deck | `templates/patterns/deck.html` | Slide presentation with arrow-key navigation, no Keynote needed |
| explainer | `templates/patterns/explainer.html` | Feature/concept explanation with collapsible steps, tabs, and FAQ |
| report | `templates/patterns/report.html` | Status update or post-mortem with summary band, timeline, action items |
| editor | `templates/patterns/editor.html` | Interactive board, triage table, or drag-drop with export |

## Components (15)

| Component | Template | Description |
|-----------|----------|-------------|
| tldr | `templates/components/tldr-box.html` | Dark-background TL;DR box: what happened, impact, resolution |
| summary-band | `templates/components/summary-band.html` | Horizontal row of stat cards for KPIs and metrics |
| tradeoff-table | `templates/components/tradeoff-table.html` | Pro/con comparison table, 2-col grid, mobile stacks |
| chips | `templates/components/chips.html` | Inline pills (severity) and tags (bug/feat/chore) for metadata |
| timeline | `templates/components/timeline.html` | Vertical timeline with dots, timestamps, and color-coded states |
| collapsible | `templates/components/collapsible.html` | `<details>/<summary>` progressive disclosure snippet |
| code-panel | `templates/components/code-panel.html` | Dark-background code block, inline diff support (`+`/`-` lines) |
| tabs | `templates/components/tabs.html` | CSS-only tab container, zero JS, monospace tab labels |
| callout | `templates/components/callout.html` | Accent-colored info/tip/warning callout box |
| action-items | `templates/components/action-items.html` | Checklist rows with checkbox, avatar, description, due date |
| data-table | `templates/components/data-table.html` | Dual-render: `<table>` on desktop, `<details>` accordion on mobile |
| progress-bar | `templates/components/progress-bar.html` | Labeled progress bar with title, percentage, note |
| decision-card | `templates/components/decision-card.html` | Framed decision with question, context, and choice chips |
| faq | `templates/components/faq.html` | `<dl>` Q&A list: question as `<dt>`, answer as `<dd>` |
| sidebar-nav | `templates/components/sidebar-nav.html` | Sticky "On this page" nav with anchor links and file list |

## Manifest JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["pattern", "title", "lang", "components"],
  "properties": {
    "pattern": {
      "type": "string",
      "enum": ["comparison", "walkthrough", "review", "design-system",
               "prototyping", "diagram", "deck", "explainer", "report", "editor"]
    },
    "title": { "type": "string", "maxLength": 120 },
    "lang": { "type": "string", "enum": ["en", "es"] },
    "palette": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "Optional: override CSS variable values"
    },
    "exportJs": {
      "type": "string",
      "description": "Optional: custom export JavaScript"
    },
    "components": {
      "type": "object",
      "minProperties": 1,
      "additionalProperties": {
        "type": "object",
        "required": ["type"],
        "properties": {
          "type": {
            "type": "string",
            "enum": ["tldr", "summary-band", "tradeoff-table", "chips",
                     "timeline", "collapsible", "code-panel", "tabs",
                     "callout", "action-items", "data-table", "progress-bar",
                     "decision-card", "faq", "sidebar-nav"]
          },
          "mobile_behavior": {
            "type": "string",
            "enum": ["stack", "scroll", "collapse", "accordion", "hide"]
          }
        }
      }
    }
  }
}
```

## Example manifest.json (report)

```json
{
  "pattern": "report",
  "title": "Engineering Status — Week 14",
  "lang": "en",
  "components": {
    "summaryBand": {
      "type": "summary-band",
      "items": [
        { "num": "14", "label": "PRs merged", "delta": "+3" },
        { "num": "1", "label": "Incidents", "delta": "SEV-2 · 47m" },
        { "num": "89%", "label": "Tests passing", "delta": "+2%" },
        { "num": "3", "label": "Deploys", "delta": "1 prod · 2 staging" }
      ]
    },
    "tldrBox": {
      "type": "tldr",
      "content": "<strong>What happened</strong> — Week 14 focused on the bulk edit toolbar feature and the N+1 query fix. <strong>Impact</strong> — Query performance improved ~40% on the dashboard. <strong>Risk</strong> — The config change in production caused a brief queue spike."
    },
    "dataTable": {
      "type": "data-table",
      "columns": ["PR", "Title", "Author", "Risk"],
      "rows": [
        ["#4871", "Bulk edit toolbar", "Mira Okafor", "med"],
        ["#4892", "Fix N+1 query", "Dan Park", "low"],
        ["#4899", "Config change", "Sam Lee", "high"]
      ],
      "rowFieldLabels": {"PR": "PR #", "Title": "Title", "Author": "Author", "Risk": "Risk"},
      "primaryColumn": "PR"
    }
  }
}
```

## Example manifest.json (comparison)

```json
{
  "pattern": "comparison",
  "title": "Debounce approaches compared",
  "lang": "en",
  "components": {
    "tradeoffTable": {
      "type": "tradeoff-table",
      "rows": [
        { "pro": "Simple, no deps", "con": "Logic duplicated" },
        { "pro": "Easy to debug", "con": "Two state sources" }
      ]
    },
    "chips": { "type": "chips" }
  }
}
```

## Output

`generate.py` produces a fully self-contained HTML file:
- All CSS in `<style>` block (design tokens + component styles)
- All JS in `<script>` block
- All SVG inline
- Responsive viewport meta tag
- Mobile-first layout (single-column at 390px)
- Desktop enhancements via media queries
