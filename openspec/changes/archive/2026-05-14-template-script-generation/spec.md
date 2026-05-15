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

The system MUST include exactly 26 template files: `templates/base.html` (1), `templates/components/*.html` (15), `templates/patterns/*.html` (10). All templates MUST use `$PLACEHOLDER` syntax compatible with Python `string.Template`. `base.html` MUST include all design tokens as CSS variables and the full HTML page shell (`<html>`, `<head>`, `<body>`, `<style>`, responsive viewport meta). Templates MUST be valid HTML fragments readable as text.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Correct count and syntax | `templates/` directory exists | enumerating files | exactly 26 `.html` files exist, all using `$PLACEHOLDER` syntax |
| Base shell has tokens and shell | `templates/base.html` | reading content | includes all design tokens as CSS variables + complete HTML page shell with responsive `<meta>` |
| Templates are valid fragments | any template file | reading as text | parses as valid HTML (no rendering required) |

### R3: Data Table Mobile Accordion

System MUST render tables with CSS-only dual-display: standard `<table>` with `<thead>`/`<tbody>` at ≥768px, `<details open>` accordion cards at <768px. Zero JavaScript. `<summary>` shows key identifying columns; card body shows remaining columns as labeled rows. Accordion MUST be expanded by default (`open` attribute).

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Desktop renders table | component `type: "table"` in manifest | viewport ≥768px | `<table>` with `<thead>` and `<tbody>` visible; header labels match manifest column definitions |
| Mobile renders accordion | component `type: "table"` in manifest | viewport <768px | `<table>` hidden via `display: none`; each row rendered as `<details open>` with `<summary>` (key columns) + labeled body (remaining columns) |
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

---

## Coverage Summary

| Req | Happy Path | Edge Case | Error State |
|-----|-----------|-----------|-------------|
| R1 — Python Script | ✅ | ✅ | ✅ |
| R2 — Template Library | ✅ | ✅ | ❌ |
| R3 — Data Table Accordion | ✅ | ✅ | ✅ |
| R4 — Manifest Schema | ✅ | ❌ | ✅ |
| R5 — Catalog Summary | ✅ | ✅ | ✅ |
| R6 — Backward Compat | ✅ | ✅ | ❌ |
