# Design: Template-Script Generation

## Technical Approach

Python 3.6+ stdlib pipeline: LLM writes `manifest.json` → `generate.py` validates against JSON Schema → resolves palette overrides from AGENTS.md → composes HTML from 26 `string.Template` files (1 base + 15 components + 10 patterns). Repeated sections use a `$JOIN` pre-processing step since `string.Template` has no loop construct. Data Table emits dual HTML blocks (`<table>` desktop / `<details>` mobile) toggled by a CSS `@media` query at 768px — zero JS, zero reflow.

## Data Flow

```
                    AGENTS.md (palette)
                         │
LLM ──writes──→ catalog-summary.md (~150 lines)
                         │ reads
                         ▼
                   manifest.json ──validates──→ manifest-schema.json
                         │
                         ▼
                   generate.py ──reads──→ templates/
                         │         base.html + 15 components + 10 patterns
                         │         │
                         │         ▼
                         │    string.Template.substitute()
                         │    $JOIN preprocessing for arrays
                         │         │
                         ▼         ▼
                   output.html (self-contained, all CSS/JS inline)
```

## Architecture Decisions

| Decision | Choice | Alternatives | Rationale |
|----------|--------|-------------|-----------|
| Template engine | `string.Template` | jinja2/mako | Zero install on any Python 3.6+. The project must work with `pip install` never called. `$PLACEHOLDER` syntax is PEP 624 compatible. |
| Table mobile transform | CSS dual-render | JS DOM transform | Zero JS dependency. No reflow cost at load. `<details open>` is natively accessible. Both DOM trees exist; CSS toggles `display` at breakpoint. |
| Mobile breakpoint | 768px | 640px, 480px, 390px | 768px is the standard tablet-to-mobile boundary. The `<details>` accordion fits content poorly above 768px (too wide for card layout). 640px (SKILL.md convention) is for component internal collapse — tables need a wider cutoff because column count varies. |
| Placeholder convention | `$PLACEHOLDER` | `${placeholder}`, `{{placeholder}}` | `$PLACEHOLDER` is PEP 624 default, visually distinct from HTML, and `string.Template` native. No delimiter escaping needed since HTML uses `{` `}` extensively. |
| Repeated sections | `$JOIN` preprocessing | `string.Template` safe_substitute with dict | stdlib has no loop. Python pre-renders each row/item fragment and joins with `\n` before substituting into parent template. The marker `$JOIN` is a sentinel that the generator replaces with pre-joined content. |
| Palette resolution | YAML block in AGENTS.md | Separate palette.json | Follows existing skill convention. `generate.py` searches for `<!-- cognitive-html:palette -->` block, parses YAML, merges with defaults, emits CSS `:root` vars as `$CSS_TOKENS`. |

## File Organization

```
skills/cognitive-html-effectiveness/
├── assets/                          # Static assets
│   └── design-tokens.css            # ← Source of truth for palette defaults
├── references/                      # Reference docs (unchanged)
│   ├── components.md
│   ├── decision-tree.md
│   ├── palette-override.md
│   ├── quality-checklist.md
│   └── patterns/
│       ├── comparison.md
│       ├── review.md
│       ├── walkthrough.md
│       ├── explainer.md
│       ├── diagram.md
│       ├── deck.md
│       ├── report.md
│       ├── design-system.md
│       ├── prototyping.md
│       └── editor.md
├── SKILL.md                         # Modified: add template workflow section
├── templates/                       # NEW — template files
│   ├── base.html                    # Page shell with placeholders
│   ├── components/                  # 15 component fragments
│   │   ├── tldr-box.html
│   │   ├── summary-band.html
│   │   ├── tradeoff-table.html
│   │   ├── chip.html
│   │   ├── timeline.html
│   │   ├── collapsible.html
│   │   ├── code-panel.html
│   │   ├── tabs.html
│   │   ├── callout.html
│   │   ├── action-items.html
│   │   ├── data-table.html          # Dual-render: <table> + <details> blocks
│   │   ├── data-table-row.html      # Single <tr> fragment (used by $JOIN)
│   │   ├── data-table-accordion-row.html  # Single <details> fragment (used by $JOIN)
│   │   ├── progress-bar.html
│   │   ├── decision-card.html
│   │   ├── faq.html
│   │   └── sidebar-nav.html
│   └── patterns/                    # 10 pattern composers
│       ├── comparison.html
│       ├── walkthrough.html
│       ├── review.html
│       ├── explainer.html
│       ├── diagram.html
│       ├── deck.html
│       ├── report.html
│       ├── design-system.html
│       ├── prototyping.html
│       └── editor.html
├── generate.py                      # NEW — CLI entry point
├── manifest-schema.json             # NEW — JSON Schema (draft-07)
└── catalog-summary.md               # NEW — LLM-readable template index (~150 lines)
```

The script finds templates relative to `generate.py` location: `Path(__file__).parent / "templates"`. No env vars or config files needed.

## generate.py Class Design

| Class | Responsibility |
|-------|---------------|
| `ManifestValidator` | Loads `manifest-schema.json`, validates input manifest via `jsonschema.validate()`. Fails fast with line-precise error messages. |
| `TemplateLoader` | Reads `.html` files from `templates/` dir tree. Caches parsed `string.Template` objects. Resolves template paths by component/pattern name. |
| `HTMLGenerator` | Orchestrates generation: resolve palette → validate manifest → load templates → pre-process `$JOIN` arrays → compose bottom-up (fragments → components → pattern → base) → write output. |

**CLI**: `python generate.py <manifest.json> [--output output.html] [--lang es|en]`

**Error handling**: Validate manifest schema BEFORE any template loading. If `--lang` given, override manifest `lang`. Fail with exit code 1 and `json.dumps` formatted error on: missing manifest, schema violation, missing template, template substitution KeyError.

**`$JOIN` algorithm** (core of repeated-section handling):

```
1. Scan template for $JOIN markers → extract fragment template name + data key
2. For each array entry in manifest[data_key]:
   a. Create string.Template from fragment file  
   b. .substitute() with entry fields
3. '\n'.join(rendered_fragments)
4. Substitute joined result into parent template at $JOIN position
5. Recurse upward until base.html
```

## Data Table Dual-Render — Detailed Design

**Desktop block** (shown >768px):
```html
<div class="table-scroll table-desktop">
  <table class="data-table"><!-- standard table --></table>
</div>
```

**Mobile block** (shown ≤768px):
```html
<div class="table-mobile-accordion">
  <details class="accordion-row" open>
    <summary class="accordion-summary">
      <span class="accordion-primary">$PRIMARY_VALUE</span>
    </summary>
    <div class="accordion-body">
      <div class="accordion-field">
        <span class="accordion-label">Column Name</span>
        <span class="accordion-value">$VALUE</span>
      </div>
      <!-- one .accordion-field per column -->
    </div>
  </details>
  <!-- one <details> per row -->
</div>
```

**CSS toggle**:
```css
.table-mobile-accordion { display: none; }
@media (max-width: 768px) {
  .table-desktop { display: none; }
  .table-mobile-accordion { display: block; }
}
```

**Card styling**: Accordion rows use `--surface-card` background, `--border` stroke, `--radius-row` rounding. Labels use `--text-muted`/`--font-mono`, values use `--text-primary`/`--font-sans`.

**Edge cases**: Empty table → render only header row with "No data" `<td>` / `<details>` body. Single row → `<details open>` (not collapsed). Cells with `<a>` or badges → pass HTML directly into `$VALUE` (no escaping — trusted manifest content).

## Manifest Schema (draft-07)

```
openspec/changes/template-script-generation/
├── design.md        ← this file
├── proposal.md      ← from sdd-propose
├── specs/           ← from sdd-spec (future)
└── manifest-schema.json  ← NEW — placed in skills/cognitive-html-effectiveness/
```

**Top-level shape**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["pattern", "title", "lang"],
  "properties": {
    "pattern": { "type": "string", "enum": ["comparison","walkthrough","review","design-system","prototyping","diagram","deck","explainer","report","editor"] },
    "title": { "type": "string", "maxLength": 120 },
    "lang": { "type": "string", "enum": ["en", "es"] },
    "palette": { "type": "object", "additionalProperties": { "type": "string" } },
    "exportJs": { "type": "string" },
    "components": { "type": "object" }
  }
}
```

Each component type in `components` has its own required/optional fields. Example **report** pattern manifest:
```json
{
  "pattern": "report",
  "title": "Engineering Status — Week 14",
  "lang": "en",
  "components": {
    "summaryBand": {
      "items": [
        { "num": "14", "label": "PRs merged", "delta": "+3" }
      ]
    },
    "dataTable": {
      "columns": ["PR", "Title", "Author", "Risk"],
      "rows": [
        ["#4871", "Bulk edit toolbar", "Mira Okafor", "med"],
        ["#4892", "Fix N+1 query", "Dan Park", "low"]
      ],
      "rowFieldLabels": {"PR": "PR #", "Title": "Title", "Author": "Author", "Risk": "Risk"},
      "primaryColumn": "PR"
    }
  }
}
```

The `dataTable` component uses `columns` array for headers, `rows` as 2D arrays (matches existing component.md pattern), `rowFieldLabels` for accordion card labels, and `primaryColumn` to determine which field goes in the `<summary>` bar.

## Testing Strategy

| Layer | What | How |
|-------|------|-----|
| Manifest validation | Schema rejects invalid manifests | `pytest` with `jsonschema`, fixture files for each violation type |
| Template loading | All 26 templates parse without error | `pytest` loads each template, verifies `string.Template` pattern count matches expected |
| HTML generation | Output matches expected structure | Generate from fixture manifests, verify `DOCTYPE`, title, lang attr, palette CSS |
| Data Table dual-render | Both table + accordion present in output | Generated HTML contains both `.table-desktop` and `.table-mobile-accordion` |
| Palette resolution | AGENTS.md override merged correctly | Temp dir with mock AGENTS.md, verify CSS vars |

**Fixtures**: `tests/fixtures/manifests/` — valid report, valid comparison, empty table, single row, palette override, missing field. `tests/fixtures/AGENTS-palette.md` for palette tests.

**Coverage target**: 90%+ on `generate.py` logic (validation, loading, generation). Template files not measured (HTML/CSS).

Test file at `skills/cognitive-html-effectiveness/tests/test_generate.py`.

## Open Questions

- None. All decisions documented above.

## Rollout

Template directory is purely additive. Existing SKILL.md direct path untouched. `generate.py` is standalone — no hooks, no imports changed. Rollback: `git revert` templates/, generate.py, catalog-summary.md.
