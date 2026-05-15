# cognitive-html-effectiveness

> A skill for AI agents that generates self-contained, beautiful HTML documents — replacing walls of markdown with pages people actually read.

[![skills.sh](https://skills.sh/b/luisdamora/caprinosol-skill-cognitive-html-effectiveness)](https://skills.sh/luisdamora/caprinosol-skill-cognitive-html-effectiveness)

## What it does

This skill teaches AI agents to produce rich HTML outputs instead of linear markdown for developer-facing documents. It combines **cognitive documentation design** principles (progressive disclosure, chunking, signposting) with **10 battle-tested patterns** from the [Unreasonable Effectiveness of HTML](https://thariqs.github.io/html-effectiveness/) collection.

The agent generates a single `.html` file that:
- Opens directly in any browser — no server, no build step, no dependencies
- Uses a warm, professional design system with semantic color coding, shared typography, and token-based spacing/layout
- Is designed mobile-first so the first-class experience still works beautifully on a phone
- Shows the TL;DR first, details behind collapsible sections
- Exports back to markdown when interactive
- Can optionally publish the generated HTML to a **secret GitHub Gist** and return a ready-to-share `htmlpreview.github.io` URL

## Optional share mode

If you ask for it, the skill can:

1. Create a **secret GitHub Gist** from the generated `.html`
2. Resolve the file's **raw URL**
3. Return a browser-friendly preview URL using `htmlpreview.github.io`

Expected links:

- **Gist**
- **Raw**
- **Preview**

By default the gist should stay secret (omit `--public`). Public visibility should only be used when explicitly requested.

## Install

```bash
npx skills add luisdamora/caprinosol-skill-cognitive-html-effectiveness --skill cognitive-html-effectiveness
```

```bash
bunx skills add luisdamora/caprinosol-skill-cognitive-html-effectiveness --skill cognitive-html-effectiveness
```

Works with OpenCode, Claude Code, Cursor, Windsurf, and other AI coding agents.

## What agents learn to build

| Pattern | When the user asks... | Example |
|---------|-----------------------|---------|
| **Comparison** | "compara approaches", "tradeoffs" | Side-by-side code with pros/cons table |
| **Walkthrough** | "explícame cómo funciona X" | Flow diagram + numbered steps with code |
| **Review** | "revisa este PR" | Annotated diff + severity tags |
| **Explainer** | "cómo funciona rate limiting" | Collapsible steps + tabs + FAQ |
| **Report** | "reporte semanal", "post-mortem" | Summary band + chart + timeline |
| **Deck** | "slides para la demo" | Arrow-key slides, no Keynote needed |
| **Diagram** | "dibuja el pipeline" | SVG flowchart with clickable nodes |
| **Editor** | "tablero de triage" | Drag-drop board + export to markdown |
| **Design System** | "muéstrame los colores" | Color swatches + type scale |
| **Prototyping** | "prototipo de animación" | Animation sandbox with sliders |

## Customize colors

Add this block to your project's `AGENTS.md` to override the default palette:

~~~markdown
<!-- cognitive-html:palette -->
```yaml
ivory: "#FEFEFE"
slate: "#1A1A2E"
clay:  "#E94560"
olive: "#0F3460"
oat:   "#E8E8E8"
```
<!-- /cognitive-html:palette -->
~~~

## Language support

The agent detects the prompt language and generates all visible text in that language — English, Spanish, Portuguese, French, and more.

## Based on

The 10 patterns are derived from the [HTML Effectiveness](https://thariqs.github.io/html-effectiveness/) collection by the Claude Code team — 20 self-contained HTML files demonstrating what agents can produce when they think in HTML instead of markdown.

## Structure

```
├── SKILL.md                  ← Agent instruction (trigger + workflow)
├── catalog-summary.md        ← LLM entry point for template mode
├── manifest-schema.json      ← JSON Schema for manifest validation
├── scripts/
│   └── generate.py           ← CLI: manifest → self-contained HTML
├── templates/
│   ├── base.html             ← Page shell with design tokens
│   ├── components/           ← 15 reusable component fragments
│   └── patterns/             ← 10 pattern composers
├── assets/
│   └── design-tokens.css     ← Default palette (CSS variables)
├── references/
│   ├── components.md         ← 15 reusable UI components
│   ├── decision-tree.md      ← Pattern selection guide
│   ├── palette-override.md   ← Color customization protocol
│   ├── quality-checklist.md  ← Pre-delivery validation
│   └── patterns/             ← 10 pattern blueprints
├── tests/
│   ├── conftest.py           ← Pytest fixtures
│   ├── test_manifest_validation.py
│   ├── test_template_loading.py
│   ├── test_html_generation.py
│   ├── test_data_table_accordion.py
│   └── test_palette_resolution.py
└── pyproject.toml            ← Project metadata + pytest config
```

## Template Generation Mode

For recurring output shapes (weekly reports, comparisons, incident templates), use the template mode instead of hand-writing HTML each time:

1. **Read** `catalog-summary.md` — the LLM entry point listing all patterns, components, and the manifest schema
2. **Write** `manifest.json` — a JSON file with pattern name, title, language, and component data
3. **Run** `python scripts/generate.py manifest.json --output output.html`
4. **Open** `output.html` in any browser

The generator validates your manifest against `manifest-schema.json`, resolves palette overrides from `AGENTS.md`, and composes the final HTML from 26 `string.Template` files — all with **zero pip install** required.

### Quick example

```bash
# Create a manifest.json, then:
python scripts/generate.py manifest.json --output report.html --lang en
```

See `catalog-summary.md` for the full manifest schema and component/pattern reference.

## License

MIT — see the original repo for details.
