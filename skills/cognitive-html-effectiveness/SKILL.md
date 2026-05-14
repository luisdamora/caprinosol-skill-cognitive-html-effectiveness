---
name: cognitive-html-effectiveness
description: "Generate self-contained, beautiful HTML documents that replace walls of markdown. Use this skill whenever the user asks for a report, comparison, explainer, slide deck, diagram, post-mortem, status update, code walkthrough, design system showcase, prototype, or interactive editor — or mentions creating HTML outputs, dashboards, visual documentation, or \"instead of markdown\". Covers 10 battle-tested patterns: comparison, walkthrough, review, design-system, prototyping, diagram, deck, explainer, report, and editor."
---

# Cognitive HTML Effectiveness

Generate self-contained HTML files that people actually read — not walls of markdown they skim and ignore.

## When to use

This skill fires when the user asks for any of:

- "crea un reporte", "haz un status", "post-mortem", "incident report"
- "compara approaches", "tradeoffs", "qué opción es mejor"
- "explícame cómo funciona X", "recorrido del código", "walkthrough"
- "slides", "presentación", "deck", "demo"
- "diagrama", "flujo", "flowchart", "arquitectura"
- "prototipo", "animación", "transición"
- "design system", "colores", "tipografía", "componentes"
- "tablero", "triage", "kanban", "drag and drop"
- "revisa este PR", "analiza este diff"
- Or any request where the user would benefit from visual layout, color coding, interaction, or progressive disclosure instead of linear text.

## Core principles

These are non-negotiable. Every HTML file you produce must respect them.

| # | Principle | What it means |
|---|-----------|---------------|
| 1 | **Self-contained** | Zero external dependencies. All CSS in `<style>`, all JS in `<script>`, all SVG inline. The file opens directly in any browser — no server, no build step, no CDN. |
| 2 | **TL;DR first** | The most important information occupies the first viewport. Use a TL;DR box, summary band, or executive summary. Answer "what happened" or "what this is" before anything else. |
| 3 | **Progressive disclosure** | Show the big picture first, hide details behind collapsible sections, tabs, or scroll. The reader should never feel overwhelmed. |
| 4 | **Color has meaning** | Warm colors (clay, rust) = attention, warning, danger. Cool colors (olive) = success, safety, good. Grays = structure, metadata, neutral. Never use color as the ONLY signal — always pair with text or shape. |
| 5 | **Typography hierarchy** | Serif for headings (authority), sans for body (readability), mono for code and metadata. At least three levels of visual hierarchy on every page. |
| 6 | **Review empathy** | Design for the person who will read this Monday morning. They're busy, they're scanning, they need to know if this matters to them in 5 seconds. |
| 7 | **Export always** | Every interactive page ends with a button that exports the final state as markdown, JSON, or plain text. The artifact must leave the page. |

## Workflow

### Step 1: Detect palette

Read `references/palette-override.md` for the full protocol. In short:

1. Check if `AGENTS.md` exists in the project root.
2. Look for the block delimited by `<!-- cognitive-html:palette -->` and `<!-- /cognitive-html:palette -->`.
3. If found, parse the YAML inside. Merge overrides with defaults.
4. If not found, use the full default palette from `assets/design-tokens.css`.

### Step 2: Load the foundation system

Before choosing a pattern, establish one shared base for the whole page. Every HTML output starts from the same foundation layer:

- **Page shell**: `body` → `.page` → `.page-header` / `.page-main` / `.page-footer`
- **Type scale**: use the tokens from `assets/design-tokens.css` for display, headings, body, small text, and metadata
- **Spacing scale**: compose spacing from `--space-1` through `--space-8`; do not invent arbitrary paddings/margins
- **Reading width**: prose-heavy sections stay near `--container-reading`; dashboards and diagrams can expand toward `--container-page`
- **Shared components**: cards, callouts, code panels, tables, badges, and nav must reuse the documented component variants

Read `assets/design-tokens.css` as the source of truth for typography, spacing, borders, shadows, and semantic surfaces.

### Step 3: Choose pattern

Read `references/decision-tree.md` for the full table. Match the user's request to one of the 10 patterns:

| Pattern | File | For... |
|---------|------|--------|
| Comparison | `patterns/comparison.md` | Side-by-side tradeoff analysis |
| Walkthrough | `patterns/walkthrough.md` | Code flow, architecture tour |
| Review | `patterns/review.md` | Annotated diff, PR analysis |
| Design System | `patterns/design-system.md` | Colors, typography, spacing tokens |
| Prototyping | `patterns/prototyping.md` | Animation sandbox, clickable flow |
| Diagram | `patterns/diagram.md` | Flowchart, architecture diagram |
| Deck | `patterns/deck.md` | Slide presentation |
| Explainer | `patterns/explainer.md` | Feature explanation, concept teaching |
| Report | `patterns/report.md` | Status update, post-mortem |
| Editor | `patterns/editor.md` | Interactive board, triage, drag-drop |

### Step 4: Read the pattern file

Each pattern file in `references/patterns/` contains:
- **When to use** — signal phrases that match this pattern
- **Structure blueprint** — the exact HTML skeleton
- **Component prescriptions** — which components from `references/components.md` to use
- **Full worked example** — a complete, self-contained HTML file you can study

### Step 5: Compose from components

Build the page using the component catalog in `references/components.md`. Do not invent new component patterns unless absolutely necessary. The catalog has 15 proven components: TL;DR box, summary band, tradeoff table, chips, timeline, collapsible snippets, code panels, tabs, callouts, action items, data tables, progress bars, decision cards, FAQ, and sidebar navigation.

All components must inherit from the same visual language:
- serif/display for headings, sans for prose, mono for metadata and code
- semantic surfaces and borders from tokens only
- consistent padding, radius, and shadow levels
- accessible focus states on interactive controls
- no ad hoc color math inside component CSS unless it is tokenized first

### Step 6: Apply quality checklist

Before delivering, run through `references/quality-checklist.md`. Every item is a gate:
- Self-contained? Opens in any browser? Responsive?
- Language matches the prompt?
- TL;DR visible in first viewport?
- Palette respected (no hardcoded colors)?
- Interactive? → has export button?

### Step 7: Deliver

Return the HTML file. The filename should be descriptive and kebab-case (e.g., `incident-report-sync-502.html`, `comparison-debounce-approaches.html`). If the user asked for multiple things, generate one file per pattern — each self-contained.

## Language rule

**Detect the language of the user's prompt and generate ALL visible text in that same language.** This includes: headings, labels, descriptions, TL;DR content, button text, captions, tooltips, alt text, chart labels, placeholder text, and navigation labels.

Code, file paths, technical identifiers, CSS class names, and variable names remain in English.

Example:
- Prompt in Spanish → "Informe de incidente", "Línea de tiempo", "Elementos de acción"
- Prompt in English → "Incident Report", "Timeline", "Action Items"
- Prompt in Portuguese → "Relatório de incidente", "Linha do tempo", "Itens de ação"

## File naming

Generated HTML files use descriptive kebab-case names in the language of the content:

- `informe-incidente-502.html`
- `comparacion-enfoques-busqueda.html`
- `status-engineering-semana-11.html`
- `como-funciona-rate-limiting.html`

Place files in the current working directory unless the user specifies otherwise.

## The default design system

These are the default design tokens. They define the visual identity. Every generated file embeds them in a `<style>` block. Reference components by semantic variable name, never by raw hex value.

```
--ivory:    #FAF9F5   ← page background
--slate:    #141413   ← primary text
--clay:     #D97757   ← accent, warnings
--oat:      #E3DACC   ← secondary surfaces
--olive:    #788C5D   ← success, positive
--rust:     #B04A3F   ← danger, high severity
--gray-100: #F0EEE6   ← subtle backgrounds
--gray-300: #D1CFC5   ← borders
--gray-500: #87867F   ← secondary text
--gray-700: #3D3D3A   ← body text
--white:    #FFFFFF   ← card backgrounds
--serif: ui-serif, Georgia, serif
--sans:  system-ui, sans-serif
--mono:  ui-monospace, monospace
```

In addition, generated files should expose:

```
--text-display / --text-h1 / --text-h2 / --text-h3 / --text-body / --text-small
--space-1 through --space-8
--container-reading / --container-page
--shadow-1 / --shadow-2 / --focus-ring
--surface-page / --surface-card / --surface-muted / --surface-accent / --surface-inverse
```

Use these tokens to create a recognizably consistent visual system across every pattern.

## Anti-patterns

- **Do NOT** link to external CSS frameworks (Bootstrap, Tailwind CDN, etc.). The file must work offline.
- **Do NOT** use external JavaScript libraries. If you need interaction, write vanilla JS.
- **Do NOT** generate markdown files with "HTML-like" formatting. The output must be valid HTML.
- **Do NOT** use inline styles (`style="..."` attributes) for static presentation. Keep styles in the `<style>` block. Data-driven SVG geometry and narrowly scoped CSS custom properties are acceptable only when they encode runtime data rather than visual decoration.
- **Do NOT** hardcode hex colors. Always use CSS variables from the palette.
- **Do NOT** skip the TL;DR. Every page needs a "why should I care" signal at the top.
- **Do NOT** create pages without an export mechanism if they are interactive.
- **Do NOT** mix multiple patterns in one file unless the pattern explicitly supports it (e.g., report pattern can include a timeline). When in doubt, one file per intent.

## Foundation rules

- Start every page from one shell: a centered `.page` container with generous top/bottom spacing and section gaps from the spacing scale.
- Keep long-form paragraphs near `--container-reading`; only data-heavy zones should span the full page width.
- Use at least 3 levels of hierarchy on every page: page title, section title, body/meta.
- Use one of the documented surface levels for every block: page, card, muted, accent, or inverse.
- Interactive controls need visible hover, focus, and active states.
- Tables, code panels, pills, and callouts should look like members of the same family, not mini one-off designs.

## Reference files

This skill uses progressive disclosure. Read reference files only as needed:

- `references/decision-tree.md` — full pattern selection guide with examples
- `references/components.md` — catalog of 15 reusable UI components with HTML + CSS
- `references/palette-override.md` — how to customize colors and core theme tokens per project via AGENTS.md
- `references/quality-checklist.md` — pre-delivery validation checklist
- `references/patterns/*.md` — one file per pattern, each with structure blueprint + worked example

When you need a specific pattern, read that one file — not all of them. When you need a component, reference `components.md` — do not guess the CSS.
