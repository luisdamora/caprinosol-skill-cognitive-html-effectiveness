# Pattern: Comparison

Side-by-side analysis of multiple approaches or options with tradeoffs and a recommendation.

## When to use

- User asks to compare approaches, frameworks, libraries, or strategies
- User says "tradeoffs", "ventajas y desventajas", "qué approach es mejor"
- User wants to choose between options
- User asks "show me different ways to solve X"

## Structure blueprint

```
┌─────────────────────────────────────────────────────┐
│ Header                                               │
│   Eyebrow: category + context                         │
│   Title: "N ways to [solve problem]"                  │
│   Prompt box: what the user asked (optional)           │
├─────────────────────────────────────────────────────┤
│ Grid of approach cards (2-4 columns)                  │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│ │ #1 Title  │ │ #2 Title  │ │ #3 Title  │              │
│ │ One-liner │ │ One-liner │ │ One-liner │              │
│ │ Code      │ │ Code      │ │ Code      │              │
│ │ Tradeoffs │ │ Tradeoffs │ │ Tradeoffs │              │
│ │ Chips     │ │ Chips     │ │ Chips     │              │
│ └──────────┘ └──────────┘ └──────────┘              │
├─────────────────────────────────────────────────────┤
│ Recommendation panel                                  │
│   "Go with approach #N because..."                     │
│   "Revisit #M if you later need..."                    │
└─────────────────────────────────────────────────────┘
```

## Component prescriptions

| Position | Component | From |
|----------|-----------|------|
| Header - eyebrow | text only | — |
| Header - prompt | code block (optional) | `components.md` § prompt-box pattern |
| Each approach card | custom grid card | see CSS below |
| Within card - code | **Code Panel** | `components.md` § 7 |
| Within card - pros/cons | **Tradeoff Table** | `components.md` § 3 |
| Within card - metadata | **Chips** | `components.md` § 4 |
| Footer | custom recommendation panel | see CSS below |

## Page layout

```html
<div class="page">
  <header class="page-head">
    <div class="eyebrow">Exploration · [project context]</div>
    <h1>[N] ways to [solve problem]</h1>
    <!-- optional prompt box -->
  </header>

  <section class="approaches">
    <article class="approach">
      <header class="approach-head">
        <h2><span class="num">01</span> [Approach name]</h2>
        <p>[One-line description]</p>
      </header>
      <!-- Code Panel component -->
      <!-- Tradeoff Table component -->
      <!-- Chips row -->
    </article>
    <!-- repeat for each approach -->
  </section>

  <aside class="reco">
    <h2>Recommendation</h2>
    <p>Go with <strong>approach [N]</strong>. [Rationale].</p>
    <p>Revisit approach [M] only if [condition].</p>
  </aside>
</div>
```

## CSS

```css
.page { max-width: 1360px; margin: 0 auto; }
.page-head { margin-bottom: 48px; max-width: 760px; }
.eyebrow {
  font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--text-muted); margin-bottom: 12px;
}
h1 {
  font-family: var(--serif); font-weight: 500; font-size: 38px;
  line-height: 1.15; color: var(--text-primary); margin-bottom: 18px;
  letter-spacing: -0.01em;
}

/* approach grid */
.approaches {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 28px;
  margin-bottom: 56px;
}
.approach {
  background: var(--bg-card);
  border: var(--border);
  border-radius: var(--radius-panel);
  padding: 24px;
  display: flex; flex-direction: column; gap: 20px;
}
.approach-head h2 { font-family: var(--serif); font-weight: 500; font-size: 21px; color: var(--text-primary); margin-bottom: 6px; }
.approach-head .num {
  display: inline-block;
  font-family: var(--mono); font-size: 12px;
  background: var(--bg-accent); color: var(--text-primary);
  padding: 2px 8px; border-radius: 8px;
  margin-right: 8px; vertical-align: 3px;
}
.approach-head p { font-size: 14px; color: var(--text-muted); }

/* recommendation */
.reco {
  border-left: 4px solid var(--clay);
  background: var(--bg-card);
  border-radius: 0 var(--radius-panel) var(--radius-panel) 0;
  padding: 24px 28px;
  max-width: 860px;
}
.reco h2 { font-family: var(--serif); font-weight: 500; font-size: 22px; color: var(--text-primary); margin-bottom: 10px; }
.reco p { font-size: 15px; margin-bottom: 8px; color: var(--text-secondary); }
.reco code { font-family: var(--mono); font-size: 0.92em; background: var(--bg-muted); padding: 1px 6px; border-radius: 4px; }
```

## Language adaptation

The endorsement style changes by language:
- English: "Go with approach N. Revisit M only if..."
- Spanish: "Ve con el approach N. Revisita M solo si..."
- Portuguese: "Vá com o approach N. Revisite M apenas se..."

## Full example

See `resources/01-exploration-code-approaches.html` in the project for a worked example: three React debounce approaches compared side-by-side with tradeoff tables and a recommendation.
