# Tasks: Template-Script Generation

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~2,150 (37 files: 1 pyproject + 1 generate.py + 26 templates + 1 schema + 1 catalog + 1 SKILL + 5 tests + 1 README) |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1: Foundation + validation tests → PR 2: 15 components + data-table tests → PR 3: 10 patterns + gen tests → PR 4: SKILL.md + README + verify |
| Delivery strategy | auto-chain |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Base |
|------|------|-----------|------|
| 1 | Foundation (generate.py, base.html, schema, catalog) + validation tests | PR 1 | `feat/template-script-generation` tracker |
| 2 | All 15 component templates + data-table accordion test + palette test | PR 2 | PR 1 branch |
| 3 | All 10 pattern templates + HTML generation tests | PR 3 | PR 2 branch |
| 4 | SKILL.md update + README + verify all 17 scenarios | PR 4 | PR 3 branch |

---

## Phase 1: Foundation (script + base template + manifest schema)

- **[x] T1.1** Create `pyproject.toml` — project metadata, pytest config, test discovery paths. Dep: none. Complexity: S
- **[x] T1.2** Create `generate.py` — CLI argparser, ManifestValidator (jsonschema), TemplateLoader (string.Template cache), HTMLGenerator (palette resolution, $JOIN preprocessing, bottom-up composition, file output). Dep: none. Complexity: L
- **[x] T1.3** Create `templates/base.html` — full HTML page shell with all design tokens as CSS variables in `<style>`, responsive viewport meta, `$TITLE`, `$LANG`, `$PALETTE_CSS`, `$BODY_HTML` placeholders. Dep: none. Complexity: M
- **[x] T1.4** Create `manifest-schema.json` — JSON Schema draft-07: pattern enum (10), title, lang, palette overrides, components object. Dep: none. Complexity: S
- **[x] T1.5** Create `catalog-summary.md` — ≤200 line LLM entry point: all 10 patterns + 15 components with descriptions, full manifest schema, quickstart example. Zero HTML/CSS. Dep: none. Complexity: M

## Phase 2: Component Templates (15 components)

Each depends on T1.3. Each template includes its CSS block as `$COMPONENT_CSS_PLACEHOLDER` (used by base.html composition). Data Table gets dual-render treatment.

- **[x] T2.1** `templates/components/tldr-box.html` — key-value TL;DR box. Dep: T1.3. Complexity: S
- **[x] T2.2** `templates/components/summary-band.html` — horizontal metric band. Dep: T1.3. Complexity: S
- **[x] T2.3** `templates/components/tradeoff-table.html` — pro/con comparison table. Dep: T1.3. Complexity: S
- **[x] T2.4** `templates/components/chips.html` — inline label/tag. Dep: T1.3. Complexity: S
- **[x] T2.5** `templates/components/timeline.html` — vertical timeline with items. Dep: T1.3. Complexity: M
- **[x] T2.6** `templates/components/collapsible.html` — `<details>` collapsible section. Dep: T1.3. Complexity: S
- **[x] T2.7** `templates/components/code-panel.html` — syntax-highlighted code block. Dep: T1.3. Complexity: S
- **[x] T2.8** `templates/components/tabs.html` — CSS-only tab container. Dep: T1.3. Complexity: M
- **[x] T2.9** `templates/components/callout.html` — colored callout/info box. Dep: T1.3. Complexity: S
- **[x] T2.10** `templates/components/action-items.html` — numbered action item list. Dep: T1.3. Complexity: S
- **[x] T2.11** `templates/components/data-table.html` — dual-render: `<table>` at ≥768px, `<details open>` accordion at <768px. CSS `@media` toggle, zero JS. Dep: T1.3. Complexity: L
- **[x] T2.12** `templates/components/progress-bar.html` — labeled progress bar. Dep: T1.3. Complexity: S
- **[x] T2.13** `templates/components/decision-card.html` — decision outcome card. Dep: T1.3. Complexity: S
- **[x] T2.14** `templates/components/faq.html` — Q&A accordion list. Dep: T1.3. Complexity: M
- **[x] T2.15** `templates/components/sidebar-nav.html` — sticky sidebar navigation. Dep: T1.3. Complexity: M

## Phase 3: Pattern Templates (10 patterns)

Each depends on Phase 2 (all components available). Each composes from component templates using `$JOIN` preprocessing. Each includes `$COMPONENT_CSS_PLACEHOLDER` to aggregate component CSS blocks.

- **[x] T3.1** `templates/patterns/comparison.html`. Dep: Phase 2. Complexity: M
- **[x] T3.2** `templates/patterns/walkthrough.html`. Dep: Phase 2. Complexity: M
- **[x] T3.3** `templates/patterns/review.html`. Dep: Phase 2. Complexity: M
- **[x] T3.4** `templates/patterns/explainer.html`. Dep: Phase 2. Complexity: M
- **[x] T3.5** `templates/patterns/diagram.html`. Dep: Phase 2. Complexity: M
- **[x] T3.6** `templates/patterns/deck.html`. Dep: Phase 2. Complexity: M
- **[x] T3.7** `templates/patterns/report.html`. Dep: Phase 2. Complexity: M
- **[x] T3.8** `templates/patterns/design-system.html`. Dep: Phase 2. Complexity: M
- **[x] T3.9** `templates/patterns/prototyping.html`. Dep: Phase 2. Complexity: M
- **[x] T3.10** `templates/patterns/editor.html`. Dep: Phase 2. Complexity: M

## Phase 4: SKILL.md Update

- **[x] T4.1** Add template-generation workflow section to `SKILL.md`: document `generate.py` CLI usage, manifest workflow (catalog-summary.md → manifest.json → generate.py → output.html), and template file structure. Keep existing direct-generation path fully intact. Dep: T3.x. Complexity: M

## Phase 5: Tests (5 test files)

All tests go in `skills/cognitive-html-effectiveness/tests/`. Each uses `pytest` with fixture manifests in `tests/fixtures/manifests/`.

- **[x] T5.1** `test_manifest_validation.py` — ManifestValidator rejects invalid manifests (missing fields, wrong types, invalid component enum). Fixtures: valid manifest, missing field, invalid type. Dep: T1.4. Complexity: M
- **[x] T5.2** `test_template_loading.py` — TemplateLoader loads all 26+ templates, verifies `string.Template` pattern count matches expected, reports parse errors. Dep: T1.2. Complexity: M
- **[x] T5.3** `test_html_generation.py` — HTMLGenerator outputs valid HTML with correct DOCTYPE, title, lang attribute, palette CSS vars. Generate from fixture manifests, verify structure. Dep: T2.x, T3.x. Complexity: M
- **[x] T5.4** `test_data_table_accordion.py` — Rendered HTML contains both `.table-desktop` and `.table-mobile-accordion` CSS classes. Verify empty table (no-data row), single row, primaryColumn in `<summary>`, rowFieldLabels in card body. Dep: T2.11. Complexity: M
- **[x] T5.5** `test_palette_resolution.py` — AGENTS.md palette override merges correctly with defaults. Temp dir with mock AGENTS.md, verify output CSS vars. Dep: T1.2. Complexity: S

## Phase 6: Verify & Documentation

- **[x] T6.1** Run quality checklist validation (`references/quality-checklist.md`) on generated output from each pattern. Fix any gate failures. Dep: T5.x. Complexity: S
- **[x] T6.2** Verify all 17 spec scenarios pass (R1–R6, every happy/edge/error path). Dep: T6.1. Complexity: M
- **[x] T6.3** Update `README.md` with new template-generation workflow overview and usage instructions. Dep: T6.2. Complexity: S

---

### Phase Dependency Graph

```
Phase 1 (Foundation) ───→ Phase 2 (Components) ───→ Phase 3 (Patterns) ───→ Phase 4 (SKILL.md)
       │                         │                         │                        │
       │                         │                         │                        │
       ├── T1.4 ─→ T5.1         ├── T2.11 ─→ T5.4         └─────────→ T5.3        │
       └── T1.2 ─→ T5.2, T5.5                                          │           │
                                                                       ▼           ▼
                                                                   Phase 6 (Verify & Docs)
```

### Implementation Order

1. **Start with Phase 1** — everything depends on generate.py, base.html, and the JSON schema
2. **Phase 2 then Phase 3** — components before the patterns that compose them
3. **Phase 4** — SKILL.md update after all templates exist
4. **Phase 5** — tests can start early (T5.1/T5.2 after T1.2/T1.4, T5.4 after T2.11) but need full implementation to complete (T5.3 needs Phase 3)
5. **Phase 6** — final verification after everything else passes
