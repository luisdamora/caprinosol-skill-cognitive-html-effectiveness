# Pattern Semantic Slots Specification

## Purpose

Pattern templates use named semantic slot placeholders instead of a single generic `$COMPONENTS_HTML`. This enables structured composition where components map to specific zones within a pattern.

## Requirements

### R1: Named Semantic Slots

Pattern templates MUST define named semantic slot placeholders (e.g., `$HEADER_SECTION`, `$BODY_SECTION`, `$SIDEBAR_SECTION`). The manifest schema MUST support an optional `slots` object mapping component keys to pattern zone names. `generate.py` MUST resolve component output into named slots based on the `slots` mapping. When a manifest omits `slots`, `generate.py` SHALL fall back to `$COMPONENTS_HTML` for backward compatibility.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Named slots populated | manifest with `slots: {"header": ["tldr-box"], "body": ["data-table"]}` | `generate.py` renders pattern | `$HEADER_SECTION` contains tldr-box output; `$BODY_SECTION` contains data-table output |
| Backward compat | manifest without `slots` key | `generate.py` renders pattern | components render into `$COMPONENTS_HTML` as before |
| All patterns have slots | any of the 10 pattern templates | reading template | at least one named semantic slot placeholder present |
| Invalid slot reference | manifest `slots` references non-existent component key | `generate.py` renders | non-zero exit with error identifying the invalid key |
| Unmapped slot gets empty | pattern defines `$SIDEBAR_SECTION` but manifest `slots` omits it | `generate.py` renders | `$SIDEBAR_SECTION` resolves to empty string, no error |
