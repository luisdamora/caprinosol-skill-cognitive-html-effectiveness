# Design: Template Generation Maturity

## Technical Approach

Five-part refactor of the template generation pipeline: (1) extract component CSS from the 752-line `base.html` monolith into per-component `<style>` blocks, (2) replace the 130-line `_render_data_table()` f-string method with template-driven `$JOIN` rendering, (3) replace generic `$COMPONENTS_HTML` in pattern templates with named semantic slots driven by a manifest `slots` object, (4) structural fixes (`pyproject.toml`, dead code elimination, `generate.py` location decision), and (5) test hardening (7/7 placeholders, `html.parser` validation, fixture manifests for all 10 patterns).

## Architecture Decisions

### Decision: CSS Distribution — Inline `<style>` extraction

**Choice**: Each component template gets a `<style>` block at the top. `generate.py` extracts all `<style>` blocks from rendered components, concatenates them into `$COMPONENT_CSS`.
**Alternatives**: (A) Separate `.css` files per component, (B) Single `components.css` generated file, (C) Keep monolithic.
**Rationale**: (A) adds file I/O for no gain — self-contained HTML is the project's core constraint. (B) breaks the "template IS the source of truth" model. (C) is the status quo debt. Inline `<style>` in the template keeps the template self-describing; extraction at generation time is a simple regex pass.

### Decision: Data-table — Template-driven via `$JOIN`

**Choice**: Replace `_render_data_table()` with `data-table.html` using `$JOIN{data-table-row}` + `$JOIN{data-table-accordion-row}`. New `data-table-accordion-row.html` fragment. Recreate `data-table-row.html` with dynamic column count.
**Alternatives**: (A) Keep f-string method, (B) Use a Jinja2 include, (C) Pre-render in `process_joins` only.
**Rationale**: (A) is the debt being fixed. (B) violates the zero-dependency constraint. (C) is what we're doing — but by wiring it through the template, not bypassing the pipeline. The `process_joins()` method already handles array-to-`colN` mapping (line 387-399); we extend it to support dynamic column headers.

### Decision: Pattern Slots — Manifest-driven mapping

**Choice**: Manifest gains optional `slots` object. `generate.py` resolves component output to named slots. Pattern templates use `$SLOT_NAME` placeholders. No `slots` → fallback to `$COMPONENTS_HTML`.
**Alternatives**: (A) Hard-coded slot names per pattern, (B) Pattern templates read component order positionally, (C) Keep `$COMPONENTS_HTML`.
**Rationale**: (A) couples manifest schema to pattern internals. (B) is fragile. (C) is the debt. Manifest-driven `slots` is declarative, backward-compatible (fallback path), and lets pattern authors name zones semantically.

### Decision: `generate.py` stays in `scripts/`

**Choice**: Keep `scripts/generate.py`. Update all design artifacts to match reality.
**Alternatives**: Move to skill root as `generate.py`.
**Rationale**: Moving adds a `git mv` that breaks import paths (`from scripts.generate import ...` in all test files). The `SKILL_DIR = Path(__file__).resolve().parent.parent` resolves correctly from `scripts/`. No functional gain from moving; significant churn cost.

### Decision: `data-table-row.html` dynamic columns

**Choice**: Row template uses `$cells` (pre-rendered `<td>` string) instead of hardcoded `$col0`–`$col5`. `process_joins` generates `$cells` from the row array length.
**Alternatives**: (A) Emit `$col0`..`$colN` with `safe_substitute`, (B) Separate `data-table-cell.html` fragment with `$JOIN`.
**Rationale**: (A) requires `safe_substitute` to avoid KeyError on variable column counts — fragile. (B) adds one more file for marginal gain. Pre-rendering `<td>` cells in `process_joins` and injecting as `$cells` is simpler, fewer templates, and matches the f-string output exactly.

## Data Flow

```
manifest.json
     │
     ▼
  validate ─── resolve palette ──→ $PALETTE_CSS
     │
     ▼
  render_component() per component
     ├── load component template
     ├── extract <style> ──→ accumulate CSS blocks
     ├── process_joins()
     │     ├── data-table-row:     array → $cells → <tr>...$cells...</tr>
     │     └── data-table-accordion-row: array → $primary, $fields → <details>...
     └── substitute → component HTML
     │
     ▼
  render_pattern() with slot mapping
     ├── has manifest.slots? → resolve component output → $SLOT_NAME
     └── no slots?           → $COMPONENTS_HTML fallback
     │
     ▼
  compose base.html
     ├── $PALETTE_CSS    (palette vars)
     ├── $COMPONENT_CSS  (concatenated <style> blocks from components)
     ├── $BODY_HTML      (pattern-wrapped content)
     └── $PAGE_TITLE, $PAGE_LANG, $EYEBROW, $EXPORT_JS
     │
     ▼
  output.html
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `templates/base.html` | Modify | Strip lines 129–733 (component CSS). Keep lines 1–128 (shell + reset + typography + shared utilities + mobile responsive for shell). Add mobile accordion CSS to `data-table.html` instead. |
| `templates/components/data-table.html` | Modify | Replace 2-line stub with full template: `<style>` block (table + accordion CSS), `$JOIN{data-table-row}` for desktop, `$JOIN{data-table-accordion-row}` for mobile, `$DATA_TABLE_HEADERS` for `<thead>` |
| `templates/components/data-table-row.html` | Modify | Replace hardcoded 6-column stub with `<tr>$cells</tr>` using `$cells` placeholder |
| `templates/components/data-table-accordion-row.html` | Create | Accordion `<details>` fragment with `$primary_value`, `$fields` placeholders |
| `templates/components/tldr-box.html` | Modify | Add `<style>.tldr{...}</style>` block extracted from base.html |
| `templates/components/summary-band.html` | Modify | Add `<style>.summary-band{...}.stat-card{...}</style>` |
| `templates/components/tradeoff-table.html` | Modify | Add `<style>.tradeoffs{...}</style>` |
| `templates/components/chips.html` | Modify | Add `<style>.pill{...}.tag{...}</style>` |
| `templates/components/timeline.html` | Modify | Add `<style>.timeline{...}</style>` |
| `templates/components/collapsible.html` | Modify | Add `<style>details.snippet{...}</style>` |
| `templates/components/code-panel.html` | Modify | Add `<style>.code-panel{...}</style>` |
| `templates/components/tabs.html` | Modify | Add `<style>.tabs{...}</style>` |
| `templates/components/callout.html` | Modify | Add `<style>.callout{...}</style>` |
| `templates/components/action-items.html` | Modify | Add `<style>.actions{...}</style>` |
| `templates/components/progress-bar.html` | Modify | Add `<style>.prog-head{...}</style>` |
| `templates/components/decision-card.html` | Modify | Add `<style>.decision-card{...}</style>` |
| `templates/components/faq.html` | Modify | Add `<style>dl.faq{...}</style>` |
| `templates/components/sidebar-nav.html` | Modify | Add `<style>.side-nav{...}</style>` |
| `templates/patterns/report.html` | Modify | Replace `$COMPONENTS_HTML` with `$SUMMARY_SECTION`, `$BODY_SECTION`, `$ACTION_SECTION` |
| `templates/patterns/comparison.html` | Modify | Replace `$COMPONENTS_HTML` with `$APPROACHES_SECTION` |
| `templates/patterns/review.html` | Modify | Replace `$COMPONENTS_HTML` with `$FINDINGS_SECTION` |
| `templates/patterns/walkthrough.html` | Modify | Replace `$COMPONENTS_HTML` with `$MAIN_CONTENT`, keep `$FLOW_DIAGRAM`, `$SIDEBAR_HTML` |
| `templates/patterns/explainer.html` | Modify | Replace `$COMPONENTS_HTML` with `$MAIN_CONTENT`, keep `$SIDEBAR_HTML` |
| `templates/patterns/diagram.html` | Modify | Replace `$COMPONENTS_HTML` with `$NOTES_SECTION` |
| `templates/patterns/deck.html` | Modify | Replace `$COMPONENTS_HTML` with `$SLIDES_CONTENT` |
| `templates/patterns/editor.html` | Modify | Replace `$COMPONENTS_HTML` with `$EDITOR_CONTENT` |
| `templates/patterns/prototyping.html` | Modify | Replace `$COMPONENTS_HTML` with `$EXTRAS_CONTENT` |
| `templates/patterns/design-system.html` | Modify | Replace `$COMPONENTS_HTML` with `$CUSTOM_SECTIONS` |
| `scripts/generate.py` | Modify | Add `_extract_css()` method. Rewrite `_render_data_table()` to use template pipeline. Add slot resolution in `render_pattern()`. Change `COMPONENT_CSS=""` to aggregated CSS. Keep `generate.py` in `scripts/`. |
| `manifest-schema.json` | Modify | Add optional `slots` property (`type: object`, `additionalProperties: {type: string}`) |
| `pyproject.toml` | Modify | Change `requires-python` from `">=3.12"` to `">=3.6"`, update classifiers |
| `tests/test_template_loading.py` | Modify | Extend `test_base_template_has_placeholders` to verify all 7. Add `html.parser` validation in `test_all_templates_are_html_strings`. Add `data-table-accordion-row` to fragment list. |
| `tests/test_html_generation.py` | Modify | Add `test_component_css_populated` verifying `$COMPONENT_CSS` is non-empty. Add quality checklist parameterized test across all 10 patterns. |
| `tests/fixtures/manifests/valid-comparison.json` | Modify | Add `slots` field for testing |
| `tests/fixtures/manifests/valid-report.json` | Modify | Add `slots` field for testing |

## Interfaces / Contracts

### CSS Extraction Contract

```python
_STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.DOTALL)

def _extract_css(self, component_html: str) -> tuple:
    """Returns (html_without_style_blocks, extracted_css_string)."""
```

Called in `render_component()` after template substitution. Accumulated CSS passed to `generate()` for `$COMPONENT_CSS`.

### Data-Table Template Contract

**`data-table.html`** receives these substitution variables:
- `$DATA_TABLE_HEADERS`: pre-rendered `<th>` cells from `columns` array
- `$JOIN{data-table-row}`: iterates `rows` array
- `$JOIN{data-table-accordion-row}`: iterates `rows` array
- `$columns_json`: JSON-encoded columns array (for accordion field mapping)

**`data-table-row.html`**:
```html
      <tr>
$cells
      </tr>
```

**`data-table-accordion-row.html`**:
```html
  <details open>
    <summary class="accordion-summary">
      <span class="accordion-primary">$primary_value</span>
    </summary>
    <div class="accordion-body">
$fields
    </div>
  </details>
```

Where `$cells` and `$fields` are pre-rendered by `process_joins` before substitution.

### Slot Resolution Contract

```python
def render_pattern(self, pattern_name: str, components_html: str,
                   slot_map: Optional[Dict[str, str]] = None) -> str:
    """
    If slot_map provided: substitute each $SLOT_NAME with its component HTML.
    If not: fall back to $COMPONENTS_HTML for backward compat.
    """
```

Manifest `slots` shape:
```json
{
  "slots": {
    "SUMMARY_SECTION": "summaryBand",
    "BODY_SECTION": "dataTable",
    "ACTION_SECTION": "actionItems"
  }
}
```

Value is a component key; `generate.py` resolves to that component's rendered HTML.

## Testing Strategy

| Layer | What | Approach |
|-------|------|----------|
| Unit — Placeholders | All 7 base.html placeholders present | Extend `test_base_template_has_placeholders` to include `PAGE_LANG`, `EYEBROW`, `EXPORT_JS` |
| Unit — HTML validity | Templates produce parseable HTML | `html.parser.HTMLParser` subclass in `test_all_templates_are_html_strings` that validates tag balance on rendered output |
| Unit — CSS extraction | Component CSS extracted correctly | Test `_extract_css()` returns stripped HTML + CSS; verify `$COMPONENT_CSS` non-empty in generated output |
| Unit — Data-table template | Rows + accordion rendered via template | Replace `_render_data_table()` call path; assert DOM structure matches existing test expectations (all 12 existing data-table tests must pass unchanged) |
| Unit — Slot resolution | Named slots substitute correctly | Test `render_pattern` with slot_map; test fallback without slot_map |
| Integration — Pattern fixtures | All 10 patterns generate valid HTML | Parameterized pytest fixture: one manifest per pattern, each validates DOCTYPE, title, lang, palette, self-containment |
| Integration — Quality checklist | Generated output passes quality checks | Parameterized test verifying: CSS vars present, mobile breakpoint present, no external refs, semantic HTML structure |

## Migration / Rollout

No data migration required. Chained PR delivery recommended (high review surface):

1. **PR1**: Structural fixes — `pyproject.toml`, delete dead `data-table-row.html` stub (but don't recreate yet)
2. **PR2**: CSS distribution — extract CSS from `base.html` into component templates, wire `_extract_css()` + `$COMPONENT_CSS`
3. **PR3**: Data-table refactor — new `data-table-row.html`, `data-table-accordion-row.html`, rewrite `data-table.html`, remove `_render_data_table()`
4. **PR4**: Pattern slots — add `slots` to schema, update all 10 pattern templates, wire slot resolution
5. **PR5**: Test hardening — extend placeholder test, add `html.parser` validation, add all-pattern fixture manifests

## Open Questions

- [ ] Confirm slot names per pattern — the names above (`$SUMMARY_SECTION`, `$BODY_SECTION`, etc.) are proposed; may need adjustment per pattern author preference
- [ ] Should base.html keep the `@media (max-width: 640px)` mobile rules for the page shell, or should those also migrate to a `shell.css` concept? Current design keeps them in base.html.
