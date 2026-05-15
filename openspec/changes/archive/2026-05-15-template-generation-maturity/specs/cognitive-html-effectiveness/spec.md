# Delta for cognitive-html-effectiveness

## MODIFIED Requirements

### R2: Template Library

The system MUST include exactly 39 template files: `templates/base.html` (1), `templates/components/*.html` (28), `templates/patterns/*.html` (10). All templates MUST use `$PLACEHOLDER` syntax compatible with Python `string.Template`. Fragment templates (sub-component rows, items) MUST use column/key placeholders for collection rendering via `$JOIN{fragment-name}` markers. `base.html` MUST include all design tokens as CSS variables and the full HTML page shell. `pyproject.toml` MUST specify `requires-python = ">=3.6"`.

(Previously: required exactly 26 templates with 15 components; no fragment template concept; no pyproject.toml reference)

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Correct count | `templates/` directory | enumerating files | exactly 39 `.html` files |
| Base shell complete | `templates/base.html` | reading content | all design tokens as CSS vars + HTML shell + responsive `<meta>` |
| Fragments use placeholders | fragment template like `data-table-row.html` | reading content | column placeholders (`$col0`–`$colN`) present |
| Python version | `pyproject.toml` | reading `requires-python` | set to `">=3.6"` |

### R3: Data Table Mobile Accordion

System MUST render tables with CSS-only dual-display using template-driven rendering. `data-table.html` MUST use `$JOIN{data-table-row}` and `$JOIN{data-table-accordion-row}` markers. `data-table-row.html` and `data-table-accordion-row.html` MUST exist as proper template fragments with column/key placeholders. `generate.py` MUST NOT use f-strings for HTML construction in the data-table pipeline — only template substitution via `process_joins()`. Zero JavaScript. Accordion MUST be expanded by default (`open` attribute).

(Previously: described visual dual-display but did not mandate template-driven rendering or restrict f-strings; `data-table.html` was a stub with `$DATA_TABLE_HTML`; no accordion fragment template existed)

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Desktop table | component `type: "table"` in manifest | viewport ≥768px | `<table>` with `<thead>`/`<tbody>` visible; headers match manifest columns |
| Mobile accordion from template | component `type: "table"` in manifest | viewport <768px | each row as `<details open>` from `data-table-accordion-row.html` template |
| Template fragments load | both row fragment templates exist | `generate.py` processes data-table | loaded via `$JOIN` markers — no f-string HTML construction |
| No JavaScript | any viewport | dual-render active | CSS `@media` only — zero JS |

## ADDED Requirements

### R7: Test Hardening

Test suite MUST verify all 7 placeholders in `base.html` (`$PAGE_LANG`, `$PALETTE_CSS`, `$COMPONENT_CSS`, `$EYEBROW`, `$PAGE_TITLE`, `$BODY_HTML`, `$EXPORT_JS`) exist and resolve to non-empty content after generation. Tests MUST use `html.parser.HTMLParser` to validate structural integrity of generated HTML fragments. Quality checklist MUST be parameterized across all 10 patterns.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| All placeholders verified | `base.html` with 7 placeholders | test suite runs | each resolves to non-empty content in generated output |
| HTML parser validates fragments | generated HTML fragment | `html.parser.HTMLParser` parses | no parse errors — valid HTML structure |
| All-pattern quality | quality checklist for all 10 patterns | parameterized test runs | each pattern passes all quality gates |
