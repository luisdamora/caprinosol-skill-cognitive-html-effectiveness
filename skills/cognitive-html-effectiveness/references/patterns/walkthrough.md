# Pattern: Walkthrough

Step-by-step exploration of how something works in the codebase — a system flow, an architecture component, or a request path.

## When to use

- User asks to understand how code works: "explícame cómo funciona X", "recorrido de código"
- User wants a tour of a module or architecture: "how does auth flow", "walk me through the pipeline"
- User says "qué pasa cuando alguien hace X" (trace a request, event, or process)
- User is onboarding to an unfamiliar part of the codebase

## Structure blueprint

```
┌──────────────────────────────────────────────────────┐
│ Header                                                │
│   Repo/context line                                    │
│   Title: "How [thing] flows through [codebase]"         │
│   Summary paragraph: what, trust boundary, key insight  │
├──────────────────────────────────────────────────────┤
│ Two-column layout (main + sidebar)                     │
│                                                        │
│ ┌─ Main ────────────────────────┬─ Sidebar ─────────┐ │
│ │                               │                    │ │
│ │ Flow Diagram (SVG)            │ Key Files          │ │
│ │ (boxes + arrows)              │  path/to/a.ts      │ │
│ │                               │  path/to/b.ts      │ │
│ │ Walkthrough steps             │                    │ │
│ │ ┌── Step 1 ──────────────┐   │ Gotchas            │ │
│ │ │  ● File:line             │   │  • edge case 1     │ │
│ │ │  Description             │   │  • edge case 2     │ │
│ │ │  ▸ show source           │   │                    │ │
│ │ └──────────────────────────┘   │                    │ │
│ │ ┌── Step 2 (hot path) ────┐   │                    │ │
│ │ │  ● File:line             │   │                    │ │
│ │ │  Description             │   │                    │ │
│ │ └──────────────────────────┘   │                    │ │
│ └───────────────────────────────┴────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

## Component prescriptions

| Position | Component | From |
|----------|-----------|------|
| Flow diagram | **Inline SVG** | draw manually (see CSS below) |
| Each step | custom step row with badge | see CSS below |
| Code within step | **Collapsible snippet** | `components.md` § 6 |
| Sidebar - key files | **Sidebar Navigation** (files section) | `components.md` § 15 |
| Sidebar - gotchas | custom gotchas panel | see CSS below |

## Page layout

```html
<div class="page">
  <header>
    <div class="repo-line">[repo] · architecture note</div>
    <h1>How [thing] flows through the codebase</h1>
    <p class="summary">[2-3 sentence overview: what it does, the trust boundary, the key insight.]</p>
  </header>

  <main>
    <h2>Flow diagram</h2>
    <div class="diagram-panel">
      <svg class="flow" viewBox="0 0 720 280">...</svg>
    </div>

    <h2>Walkthrough</h2>
    <!-- Step 1 -->
    <div class="step">
      <div class="badge">1</div>
      <div class="step-body">
        <div class="step-loc">path/to/file.ts<span class="range"> :22-48</span></div>
        <p>Description of what happens at this step.</p>
        <details class="snippet">
          <summary>show source</summary>
          <pre class="code">...</pre>
        </details>
      </div>
    </div>
    <!-- Step 2 (hot path) -->
    <div class="step hot">
      <div class="badge">2</div>
      <div class="step-body">...</div>
    </div>
    <!-- ... more steps -->
  </main>

  <aside>
    <div class="panel">
      <h3>Key files</h3>
      <ul class="key-files">
        <li><span class="path">path/to/file.ts</span><span class="desc">What it does.</span></li>
      </ul>
    </div>
    <div class="gotchas">
      <h3>Gotchas</h3>
      <ul>
        <li>Edge case or surprising behavior.</li>
      </ul>
    </div>
  </aside>
</div>
```

## CSS (add to page <style>)

```css
.page { max-width: var(--container-page); margin: 0 auto; display: grid; grid-template-columns: minmax(0, 1fr) 280px; gap: 40px; }
@media (max-width: 960px) { .page { grid-template-columns: 1fr; } }
header { grid-column: 1 / -1; margin-bottom: 8px; }
.repo-line { font-family: var(--mono); font-size: 12.5px; color: var(--text-muted); margin-bottom: 10px; }
h1 { font-family: var(--serif); font-weight: var(--weight-heading); font-size: var(--text-h1); line-height: var(--lh-heading); color: var(--text-primary); margin-bottom: var(--space-4); }
.summary { max-width: var(--container-reading); font-size: var(--text-lead); color: var(--text-secondary); }
.summary code { font-family: var(--mono); font-size: 13px; }

/* diagram */
.diagram-panel { border: var(--border); border-radius: var(--radius-panel); background: var(--bg-card); padding: 20px; overflow-x: auto; }
svg.flow { display: block; max-width: 100%; }
.flow text { font-family: var(--mono); font-size: 12px; fill: var(--text-primary); }
.flow .sub { font-size: 10px; fill: var(--text-muted); }
.flow .box { fill: var(--bg-card); stroke: var(--gray-300); stroke-width: 1.5; }
.flow .box.hot { fill: color-mix(in srgb, var(--clay) 12%, var(--white)); stroke: var(--clay); }
.flow .arrow { stroke: var(--gray-500); stroke-width: 1.5; fill: none; }

/* steps */
.step { display: grid; grid-template-columns: 44px 1fr; gap: 18px; padding: 20px 0; border-bottom: 1.5px solid var(--bg-muted); }
.step:last-of-type { border-bottom: none; }
.badge {
  width: 34px; height: 34px; border-radius: 50%;
  background: var(--bg-accent); border: 1.5px solid var(--gray-300);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--mono); font-weight: 600; color: var(--text-primary); font-size: 14px;
}
.step.hot .badge { background: color-mix(in srgb, var(--clay) 16%, var(--white)); border-color: var(--clay); color: var(--clay); }
.step-loc { font-family: var(--mono); font-size: 13px; color: var(--text-primary); margin-bottom: 6px; }
.step-loc .range { color: var(--text-muted); }
.step-body p { margin-bottom: 10px; color: var(--text-secondary); }

/* sidebar */
aside { position: sticky; top: 24px; align-self: start; }
.panel { border: var(--border); border-radius: var(--radius-panel); background: var(--bg-card); padding: 18px 20px; margin-bottom: 20px; }
.panel h3 { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 12px; }
.key-files { list-style: none; padding: 0; }
.key-files li { margin-bottom: 12px; }
.key-files .path { font-family: var(--mono); font-size: 12px; color: var(--text-primary); display: block; margin-bottom: 2px; word-break: break-all; }
.key-files .desc { font-size: 12.5px; color: var(--text-muted); line-height: 1.45; }
.gotchas { border: 1.5px solid var(--clay); border-radius: var(--radius-panel); background: color-mix(in srgb, var(--clay) 8%, var(--white)); padding: 18px 20px; }
.gotchas h3 { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--clay); margin-bottom: 10px; }
.gotchas ul { list-style: none; padding: 0; }
.gotchas li { position: relative; padding-left: 16px; font-size: 13px; margin-bottom: 8px; color: var(--text-secondary); }
.gotchas li::before { content: ""; position: absolute; left: 0; top: 8px; width: 5px; height: 5px; background: var(--clay); border-radius: 2px; }
.gotchas code { font-family: var(--mono); font-size: 11.5px; }

/* code panels in steps */
pre.code { background: var(--slate); color: var(--gray-100); font-family: var(--mono); font-size: 12.5px; line-height: 1.7; border-radius: 8px; padding: 14px 16px; overflow-x: auto; margin-top: 10px; }
```

## "At most one open" JS

Add this at the bottom to keep the walkthrough scannable:

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

## Tip: marking the hot path

Use `.step.hot` on the step that is the trust boundary or the most important step. This gives it a clay-tinted badge and draws the reader's eye to the critical decision point.

## Full example

See `resources/04-code-understanding.html` in the project for a worked example: authentication flow through a web codebase, with SVG diagram, 5 walkthrough steps, key files sidebar, and gotchas panel.
