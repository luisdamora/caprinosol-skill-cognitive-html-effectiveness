# Tasks: Template Generation Maturity

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 1800–2200 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 → PR 2 → PR 3 → PR 4 → PR 5 |
| Delivery strategy | ask-on-risk |
| Chain strategy | feature-branch-chain |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Structural fixes — `pyproject.toml`, dead stub cleanup | PR 1 | Base: `feat/template-generation-maturity`; ~30 lines |
| 2 | CSS distribution — extract CSS into 15 component templates, wire `_extract_css()` | PR 2 | Base: PR 1 branch; ~500 lines (large but mostly CSS moves) |
| 3 | Data-table refactor — template-driven pipeline, new fragments | PR 3 | Base: PR 2 branch; ~200 lines |
| 4 | Pattern slots — named slots in 10 patterns, schema, generate.py | PR 4 | Base: PR 3 branch; ~300 lines |
| 5 | Test hardening + spec sync — all-pattern fixtures, html.parser, spec R2/R7 | PR 5 | Base: PR 4 branch; ~250 lines |

## Phase 1: Structural Fixes

- [x] 1.1 Fix `pyproject.toml`: change `requires-python` to `">=3.6"`, update classifiers to include 3.6–3.12. **S** | `pyproject.toml`
- [x] 1.2 Delete dead `data-table-row.html` stub (hardcoded 6-col `$col0`–`$col5`); recreated in Phase 3. **S** | `templates/components/data-table-row.html`

## Phase 2: CSS Distribution

- [x] 2.1 Extract `.tldr` CSS (lines 130–158 of `base.html`) into `<style>` block in `tldr-box.html`. **S** | `templates/components/tldr-box.html`, `templates/base.html`
- [x] 2.2 Extract `.summary-band` + `.stat-*` CSS (lines 161–197) into `summary-band.html`. **S** | `templates/components/summary-band.html`, `templates/base.html`
- [x] 2.3 Extract `.tradeoffs` CSS (lines 200–237) into `tradeoff-table.html`. **S** | `templates/components/tradeoff-table.html`, `templates/base.html`
- [x] 2.4 Extract `.pill` + `.tag` CSS (lines 240–266) into `chips.html`. **S** | `templates/components/chips.html`, `templates/base.html`
- [x] 2.5 Extract `.timeline` CSS (lines 269–310) into `timeline.html`. **S** | `templates/components/timeline.html`, `templates/base.html`
- [x] 2.6 Extract `details.snippet` CSS (lines 313–345) into `collapsible.html`. **S** | `templates/components/collapsible.html`, `templates/base.html`
- [x] 2.7 Extract `.code-panel` CSS (lines 348–368) into `code-panel.html`. **S** | `templates/components/code-panel.html`, `templates/base.html`
- [x] 2.8 Extract `.tabs` CSS (lines 371–402) into `tabs.html`. **S** | `templates/components/tabs.html`, `templates/base.html`
- [x] 2.9 Extract `.callout` CSS (lines 405–416) into `callout.html`. **S** | `templates/components/callout.html`, `templates/base.html`
- [x] 2.10 Extract `.actions` + `.ai-*` CSS (lines 419–464) into `action-items.html`. **S** | `templates/components/action-items.html`, `templates/base.html`
- [x] 2.11 Extract `.data-table` + `.table-scroll` CSS (lines 467–498) into `data-table.html`. **S** | `templates/components/data-table.html`, `templates/base.html`
- [x] 2.12 Extract `.prog-*` CSS (lines 501–534) into `progress-bar.html`. **S** | `templates/components/progress-bar.html`, `templates/base.html`
- [x] 2.13 Extract `.decision-card` + `.chip` CSS (lines 537–572) into `decision-card.html`. **S** | `templates/components/decision-card.html`, `templates/base.html`
- [x] 2.14 Extract `dl.faq` CSS (lines 575–587) into `faq.html`. **S** | `templates/components/faq.html`, `templates/base.html`
- [x] 2.15 Extract `.side-nav` CSS (lines 590–626) into `sidebar-nav.html`. **S** | `templates/components/sidebar-nav.html`, `templates/base.html`
- [x] 2.16 Extract mobile accordion CSS (lines 670–733) into `data-table.html`. **S** | `templates/components/data-table.html`, `templates/base.html`
- [x] 2.17 Keep only shared/reset CSS + shell mobile responsive (lines 1–128, 629–667) in `base.html`. Verify ≤300 lines. **S** | `templates/base.html`
- [x] 2.18 Add `_extract_css()` method to `HTMLGenerator` — regex `<style>...</style>` extraction, returns `(html_without_styles, css_text)`. **M** | `scripts/generate.py`
- [x] 2.19 Wire `render_component()` to call `_extract_css()`, accumulate CSS per component. **M** | `scripts/generate.py`
- [x] 2.20 Update `generate()` to pass accumulated CSS as `$COMPONENT_CSS` (replace empty string). **S** | `scripts/generate.py`
- [x] 2.21 Add CSS deduplication: track seen component keys, skip duplicate `<style>` blocks. **S** | `scripts/generate.py`

## Phase 3: Data-table Refactor

- [x] 3.1 Create `data-table-accordion-row.html` with `<details open>` template: `$primary_value`, `$fields` placeholders. **S** | `templates/components/data-table-accordion-row.html`
- [x] 3.2 Create new `data-table-row.html` with `<tr>$cells</tr>` using `$cells` placeholder. **S** | `templates/components/data-table-row.html`
- [x] 3.3 Rewrite `data-table.html`: add `$DATA_TABLE_HEADERS`, `$JOIN{data-table-row}`, `$JOIN{data-table-accordion-row}` markers. **M** | `templates/components/data-table.html`
- [x] 3.4 Extend `process_joins()` to generate `$cells` (pre-rendered `<td>` cells) from row array length. **M** | `scripts/generate.py`
- [x] 3.5 Extend `process_joins()` to generate `$primary_value` + `$fields` for accordion rows using `columns` + `rowFieldLabels`. **M** | `scripts/generate.py`
- [x] 3.6 Add `$DATA_TABLE_HEADERS` generation: pre-render `<th>` cells from `columns` array. **S** | `scripts/generate.py`
- [x] 3.7 Remove `render_component()` data-table special case — route through template pipeline. **M** | `scripts/generate.py`
- [x] 3.8 Delete `_render_data_table()` method entirely. **S** | `scripts/generate.py`
- [x] 3.9 Add `data-table-accordion-row` to fragment template existence test. **S** | `tests/test_template_loading.py`

## Phase 4: Pattern Slots

- [x] 4.1 Update `report.html`: replace `$COMPONENTS_HTML` with `$SUMMARY_SECTION`, `$BODY_SECTION`, `$ACTION_SECTION`. **S** | `templates/patterns/report.html`
- [x] 4.2 Update `comparison.html`: replace `$COMPONENTS_HTML` with `$APPROACHES_SECTION`. **S** | `templates/patterns/comparison.html`
- [x] 4.3 Update `review.html`: replace `$COMPONENTS_HTML` with `$FINDINGS_SECTION`. **S** | `templates/patterns/review.html`
- [x] 4.4 Update `walkthrough.html`: replace `$COMPONENTS_HTML` with `$MAIN_CONTENT` (keep `$FLOW_DIAGRAM`, `$SIDEBAR_HTML`). **S** | `templates/patterns/walkthrough.html`
- [x] 4.5 Update `explainer.html`: replace `$COMPONENTS_HTML` with `$MAIN_CONTENT` (keep `$SIDEBAR_HTML`). **S** | `templates/patterns/explainer.html`
- [x] 4.6 Update `diagram.html`: replace `$COMPONENTS_HTML` with `$NOTES_SECTION`. **S** | `templates/patterns/diagram.html`
- [x] 4.7 Update `deck.html`: replace `$COMPONENTS_HTML` with `$SLIDES_CONTENT`. **S** | `templates/patterns/deck.html`
- [x] 4.8 Update `editor.html`: replace `$COMPONENTS_HTML` with `$EDITOR_CONTENT`. **S** | `templates/patterns/editor.html`
- [x] 4.9 Update `prototyping.html`: replace `$COMPONENTS_HTML` with `$EXTRAS_CONTENT`. **S** | `templates/patterns/prototyping.html`
- [x] 4.10 Update `design-system.html`: replace `$COMPONENTS_HTML` with `$CUSTOM_SECTIONS`. **S** | `templates/patterns/design-system.html`
- [x] 4.11 Add `slots` property to `manifest-schema.json`: `type: object`, `additionalProperties: {type: string}`, optional. **S** | `manifest-schema.json`
- [x] 4.12 Update `render_pattern()` to accept `slot_map: Optional[Dict[str, str]]`, resolve component keys to rendered HTML, substitute `$SLOT_NAME`. **M** | `scripts/generate.py`
- [x] 4.13 Add backward-compat fallback in `render_pattern()`: no `slots` → use `$COMPONENTS_HTML`. **S** | `scripts/generate.py`
- [x] 4.14 Update `generate()` to extract `manifest.get("slots")` and pass to `render_pattern()`. **S** | `scripts/generate.py`
- [x] 4.15 Add error handling: invalid slot reference (non-existent component key) → non-zero exit. **S** | `scripts/generate.py`
- [x] 4.16 Unmapped slot resolves to empty string (no error). **S** | `scripts/generate.py`

## Phase 5: Test Hardening + Spec Sync

- [x] 5.1 Extend `test_base_template_has_placeholders` to verify all 7: `PAGE_LANG`, `PALETTE_CSS`, `COMPONENT_CSS`, `EYEBROW`, `PAGE_TITLE`, `BODY_HTML`, `EXPORT_JS`. **S** | `tests/test_template_loading.py`
- [x] 5.2 Add `html.parser.HTMLParser` subclass in `test_all_templates_are_html_strings` for tag-balance validation on rendered output. **M** | `tests/test_template_loading.py`
- [x] 5.3 Add `test_component_css_populated` verifying `$COMPONENT_CSS` is non-empty in generated output. **S** | `tests/test_html_generation.py`
- [x] 5.4 Create fixture manifests for remaining 8 patterns (comparison, walkthrough, review, design-system, prototyping, diagram, deck, editor). **M** | `tests/fixtures/manifests/`
- [x] 5.5 Add parameterized quality checklist test across all 10 patterns: CSS vars, mobile breakpoint, no external refs, semantic HTML. **M** | `tests/test_html_generation.py`
- [x] 5.6 Add `test_slot_resolution_works`: manifest with `slots` → named slots substituted correctly. **S** | `tests/test_html_generation.py`
- [x] 5.7 Add `test_slot_backward_compat`: manifest without `slots` → `$COMPONENTS_HTML` fallback. **S** | `tests/test_html_generation.py`
- [x] 5.8 Update `valid-comparison.json` and `valid-report.json` fixtures with `slots` field. **S** | `tests/fixtures/manifests/`
- [x] 5.9 Update main spec `openspec/specs/cognitive-html-effectiveness/spec.md`: R2 count → 40, add CSS distribution + slot requirements. **M** | `openspec/specs/cognitive-html-effectiveness/spec.md`

## Phase Dependency Graph

```
Phase 1 ──→ Phase 2 ──→ Phase 3 ──→ Phase 4 ──→ Phase 5
  (fix)      (CSS)      (table)     (slots)     (tests+spec)
```

- Phase 1 is independent foundation
- Phase 2 depends on Phase 1 (base.html must be stable before CSS extraction)
- Phase 3 depends on Phase 2 (data-table.html gets its CSS in Phase 2)
- Phase 4 depends on Phase 3 (slot resolution needs stable component pipeline)
- Phase 5 depends on Phase 4 (tests validate all prior work; spec reflects final state)

## Implementation Order

Execute phases strictly sequentially. Within each phase, tasks with no cross-dependency (e.g., individual CSS extractions 2.1–2.17) can be done in parallel. Generate.py wiring tasks (2.18–2.21, 3.4–3.8, 4.12–4.16) are sequential within their phase. Run `pytest` after each phase to catch regressions early.
