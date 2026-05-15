# Template-Script Generation — Specification

## Purpose

Separate PRESENTATION (templates) from CONTENT (per-run manifest data). The LLM reads ~150-line `catalog-summary.md` → writes `manifest.json` → `generate.py` validates + renders via `string.Template` → self-contained HTML. Zero pip install. Fully backward compatible with the existing direct-generation path.

---

## Requirements

### R1: Python Generation Script

The system MUST provide `generate.py` accepting `manifest.json` path and output HTML path as CLI arguments. MUST use only Python 3.6+ stdlib. MUST validate manifest against JSON schema before rendering. MUST exit non-zero with a clear error message on validation failure. Generated HTML MUST be self-contained and pass all quality checklist gates.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Valid manifest generates HTML | valid `manifest.json` with all required fields | `python generate.py manifest.json output.html` runs | `output.html` created as self-contained valid HTML passing all quality gates |
| Invalid manifest reports error | manifest missing a required field (e.g. `pattern`) | validation runs | non-zero exit + clear error identifying missing field and expected type |
| Stdlib-only operation | system with only Python 3.6+ stdlib | `generate.py` invoked | runs without any pip-installed packages |

### R2: Template Library

The system MUST include exactly 40 template files: `templates/base.html` (1), `templates/components/*.html` (29), `templates/patterns/*.html` (10). All templates MUST use `$PLACEHOLDER` syntax compatible with Python `string.Template`. Fragment templates (sub-component rows, items) MUST use column/key placeholders for collection rendering via `$JOIN{fragment-name}` markers. `base.html` MUST include all design tokens as CSS variables and the full HTML page shell (`<html>`, `<head>`, `<body>`, `<style>`, responsive viewport meta). Each component template MUST contain its own `<style>` block with scoped CSS. `base.html` MUST contain only shared/reset CSS — zero component-specific rules. `generate.py` MUST extract `<style>` blocks from rendered component HTML and concatenate them into `$COMPONENT_CSS`. `pyproject.toml` MUST specify `requires-python = ">=3.6"`.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Correct count and syntax | `templates/` directory exists | enumerating files | exactly 40 `.html` files exist, all using `$PLACEHOLDER` syntax |
| Base shell has tokens and shell | `templates/base.html` | reading content | includes all design tokens as CSS variables + complete HTML page shell with responsive `<meta>` |
| Templates are valid fragments | any template file | reading as text | parses as valid HTML (no rendering required) |
| Component CSS self-contained | any component template | reading content | `<style>` block present with scoped selectors |
| Base has no component CSS | all component CSS distributed to templates | reading `base.html` | only shared/reset CSS remains |
| CSS extracted and concatenated | component with embedded `<style>` | `generate.py` renders | `<style>` content included in `$COMPONENT_CSS` |
| CSS deduplication | same component rendered twice | `generate.py` renders | component `<style>` appears once in output |
| Python version | `pyproject.toml` | reading `requires-python` | set to `">=3.6"` |

### R3: Data Table Mobile Accordion

System MUST render tables with CSS-only dual-display using template-driven rendering. `data-table.html` MUST use `$JOIN{data-table-row}` and `$JOIN{data-table-accordion-row}` markers. `data-table-row.html` and `data-table-accordion-row.html` MUST exist as proper template fragments with column/key placeholders. `generate.py` MUST NOT use f-strings for HTML construction in the data-table pipeline — only template substitution via `process_joins()`. Zero JavaScript. Accordion MUST be expanded by default (`open` attribute).

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Desktop renders table | component `type: "table"` in manifest | viewport ≥768px | `<table>` with `<thead>` and `<tbody>` visible; header labels match manifest column definitions |
| Mobile renders accordion | component `type: "table"` in manifest | viewport <768px | each row as `<details open>` from `data-table-accordion-row.html` template |
| Template fragments load | both row fragment templates exist | `generate.py` processes data-table | loaded via `$JOIN` markers — no f-string HTML construction |
| No JavaScript required | any viewport | dual-render active | toggle driven solely by CSS `@media` queries — zero JS |

### R4: Manifest Schema

System MUST validate `manifest.json` against a defined JSON schema. Manifest MUST specify: `pattern`, `title`, `language`, `palette`, `components[]`. Each component MUST specify: `type` (from allowed enum), content data, optional mobile behavior. Schema MUST validate field types, required fields, and the component type enum.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Valid manifest passes | manifest with all required fields and correct types | validation runs | passes without errors |
| Invalid component type rejected | component with `type: "invalid_type"` (not in enum) | validation runs | non-zero exit + error listing allowed types |
| Missing required field | manifest without `components` array | validation runs | non-zero exit + error identifying `components` as required |

### R5: Catalog Summary

System MUST provide `catalog-summary.md` as the LLM's sole entry point for template generation. MUST contain: list of all 10 patterns with descriptions, list of all 15 components with descriptions, JSON manifest schema, and a quickstart example. File MUST be ≤200 lines. MUST contain zero CSS or HTML — only markdown, JSON snippets, and lists.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Catalog is complete | `catalog-summary.md` | LLM reads it | contains all 10 pattern descriptions, all 15 component descriptions, manifest schema, and quickstart |
| Catalog is under limit | `catalog-summary.md` | counting lines | ≤200 lines |
| No HTML/CSS in catalog | `catalog-summary.md` | scanning for HTML tags or CSS properties | contains zero HTML or CSS — only markdown, JSON, and lists |

### R6: Backward Compatibility

Existing SKILL.md direct-generation path MUST remain functional. Template generation MUST be additive — users MAY choose either workflow.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Direct path unchanged | existing SKILL.md with direct-generation instructions | invoked per original workflow | produces identical HTML output as before template system was added |
| Both workflows coexist | both SKILL.md and template system installed | user picks either path | both produce valid self-contained HTML; neither breaks the other |

### R7: Test Hardening

Test suite MUST verify all 7 placeholders in `base.html` (`$PAGE_LANG`, `$PALETTE_CSS`, `$COMPONENT_CSS`, `$EYEBROW`, `$PAGE_TITLE`, `$BODY_HTML`, `$EXPORT_JS`) exist and resolve to non-empty content after generation. Tests MUST use `html.parser.HTMLParser` to validate structural integrity of generated HTML fragments. Quality checklist MUST be parameterized across all 10 patterns.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| All placeholders verified | `base.html` with 7 placeholders | test suite runs | each resolves to non-empty content in generated output |
| HTML parser validates fragments | generated HTML fragment | `html.parser.HTMLParser` parses | no parse errors — valid HTML structure |
| All-pattern quality | quality checklist for all 10 patterns | parameterized test runs | each pattern passes all quality gates |

### R8: Pattern Semantic Slots

Pattern templates MUST define named semantic slot placeholders (e.g., `$HEADER_SECTION`, `$BODY_SECTION`). The manifest schema MUST support an optional `slots` object mapping component keys to pattern zone names. `generate.py` MUST resolve component output into named slots based on the `slots` mapping. When a manifest omits `slots`, `generate.py` SHALL fall back to `$COMPONENTS_HTML` for backward compatibility. Invalid slot reference (non-existent component key) MUST cause non-zero exit. Unmapped slots resolve to empty string.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Named slots populated | manifest with `slots` mapping | `generate.py` renders pattern | slot placeholders substituted with correct component output |
| Backward compat | manifest without `slots` key | `generate.py` renders pattern | components render into `$COMPONENTS_HTML` as before |
| Invalid slot reference | manifest `slots` references non-existent component key | `generate.py` renders | non-zero exit with error identifying the invalid key |
| Unmapped slot gets empty | pattern defines `$SIDEBAR_SECTION` but manifest `slots` omits it | `generate.py` renders | `$SIDEBAR_SECTION` resolves to empty string, no error |

---

## Coverage Summary

| Req | Happy Path | Edge Case | Error State |
|-----|-----------|-----------|-------------|
| R1 — Python Script | ✅ | ✅ | ✅ |
| R2 — Template Library | ✅ | ✅ | ✅ |
| R3 — Data Table Accordion | ✅ | ✅ | ✅ |
| R4 — Manifest Schema | ✅ | ❌ | ✅ |
| R5 — Catalog Summary | ✅ | ✅ | ✅ |
| R6 — Backward Compat | ✅ | ✅ | ✅ |
| R7 — Test Hardening | ✅ | ✅ | ✅ |
| R8 — Pattern Semantic Slots | ✅ | ✅ | ✅ |
