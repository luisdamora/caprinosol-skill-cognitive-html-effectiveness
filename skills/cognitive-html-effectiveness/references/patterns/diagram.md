# Pattern: Diagram

Visual diagrams rendered as inline SVG — flowcharts, architecture maps, sequence diagrams, and system topologies.

## When to use

- User asks for "diagrama", "flujo", "flowchart", "arquitectura visual"
- User wants to see how components connect: "dibuja el pipeline", "show me the architecture"
- User asks for a visual representation of a process or system
- User says "grafica", "mapa de módulos", "system diagram"

## Structure blueprint

```
┌──────────────────────────────────────────────────────────┐
│ Header                                                    │
│   Title: "[System/Process] Diagram"                        │
│   Subtitle: context or one-line description                │
├──────────────────────────────────────────────────────────┤
│ Diagram panel (white card with SVG inside)                 │
│   ┌────────────────────────────────────────┐             │
│   │  ┌───┐     ┌───┐     ┌───┐            │             │
│   │  │ A │ ──→ │ B │ ──→ │ C │            │             │
│   │  └───┘     └───┘     └───┘            │             │
│   │              │                          │             │
│   │              ▼                          │             │
│   │           ┌───┐                        │             │
│   │           │ D │                        │             │
│   │           └───┘                        │             │
│   └────────────────────────────────────────┘             │
├──────────────────────────────────────────────────────────┤
│ Legend / annotations (optional)                           │
│   ● Hot path   ○ Cold path   ──→ Data flow               │
├──────────────────────────────────────────────────────────┤
│ Step details below (if flowchart)                         │
│   Click any box to see what runs there                    │
└──────────────────────────────────────────────────────────┘
```

## Component prescriptions

| Position | Component | From |
|----------|-----------|------|
| Diagram panel | white card | see CSS below |
| SVG elements | inline SVG (hand-drawn) | see patterns below |
| Step details | **Collapsible snippet** | `components.md` § 6 |
| Legend | custom | see CSS below |

## SVG patterns to use

### Box with label (standard node)

```svg
<rect class="box" x="30" y="40" width="150" height="64" rx="10"/>
<text x="105" y="68" text-anchor="middle">Service Name</text>
<text class="sub" x="105" y="84" text-anchor="middle">details here</text>
```

### Hot path box (highlighted)

```svg
<rect class="box hot" x="460" y="40" width="180" height="64" rx="10"/>
```

### Arrow with marker

```svg
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path class="arrow-head" d="M 0 0 L 10 5 L 0 10 z"/>
  </marker>
</defs>
<line class="arrow" x1="180" y1="72" x2="245" y2="72" marker-end="url(#arrow)"/>
```

### Diamond (decision node)

```svg
<polygon class="box" points="60,28 100,10 140,28 100,46"/>
<text x="100" y="32" text-anchor="middle">Decision?</text>
```

### Dashed arrow (optional path)

```svg
<line class="arrow da" x1="180" y1="72" x2="245" y2="72" marker-end="url(#arrow)"/>
```

```css
.arrow.da { stroke-dasharray: 4 4; }
```

## Diagram CSS

```css
.diagram-panel {
  border: var(--border);
  border-radius: var(--radius-panel);
  background: var(--bg-card);
  padding: 28px 20px;
  overflow-x: auto;
  margin-bottom: 32px;
}
svg.diagram { display: block; max-width: 100%; }
svg.diagram text {
  font-family: var(--mono);
  font-size: 12px;
  fill: var(--text-primary);
}
svg.diagram .sub { font-size: 10px; fill: var(--text-muted); }
svg.diagram .arrow-head { fill: var(--gray-500); }
svg.diagram .box {
  fill: var(--bg-card);
  stroke: var(--gray-300);
  stroke-width: 1.5;
}
svg.diagram .box.hot {
  fill: color-mix(in srgb, var(--clay) 12%, var(--white));
  stroke: var(--clay);
}
svg.diagram .arrow {
  stroke: var(--gray-500);
  stroke-width: 1.5;
  fill: none;
}
svg.diagram .arrow.hot {
  stroke: var(--clay);
  stroke-width: 2;
}
@media (max-width: 640px) {
  .diagram-panel { padding: 18px 14px; }
  svg.diagram { min-width: 560px; }
}
```

## Mobile-first behavior

- Every diagram must still make sense at `390px` wide.
- If the SVG is wider than the phone, allow horizontal scroll inside the diagram panel — never on the full page.
- Add a short text summary or ordered list under the diagram so the reader can understand the main path without panning.
- Keep labels large enough to read on a phone; if you need too many nodes, break the diagram apart.

## Interactivity: click a node to see details

Add lightweight JS that connects SVG nodes to detail sections:

```js
document.querySelectorAll('svg .box[data-step]').forEach(box => {
  box.style.cursor = 'pointer';
  box.addEventListener('click', () => {
    const stepId = box.dataset.step;
    const detail = document.getElementById(stepId);
    if (detail) detail.scrollIntoView({ behavior: 'smooth' });
  });
});
```

Then in SVG, tag nodes: `<rect class="box" data-step="step-3" .../>`

And detail sections: `<div id="step-3" class="step-detail">...</div>`

## Legend

```html
<div class="legend">
  <span class="legend-item"><span class="swatch critical"></span> Critical path</span>
  <span class="legend-item"><span class="swatch normal"></span> Normal flow</span>
  <span class="legend-item"><span class="swatch store"></span> Data store</span>
</div>
```

```css
.legend {
  display: flex; gap: 20px; flex-wrap: wrap;
  padding: 12px 0; margin-bottom: 20px;
}
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-secondary); }
.swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
.swatch.critical { background: var(--clay); }
.swatch.normal { background: var(--gray-300); }
.swatch.store { background: var(--oat); }
```

## Tip: Keep the SVG simple

Don't try to fit every detail in the diagram. The diagram shows structure and flow. Put details in collapsible sections below. A diagram with more than 12-15 boxes is too complex — break it into sub-diagrams.

## Full examples

- **Flowchart**: See `resources/13-flowchart-diagram.html` in the project — deploy pipeline with clickable steps
- **Architecture diagram**: See `resources/04-code-understanding.html` — auth flow with boxes and arrows
