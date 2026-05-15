# Proposal: Template Generation Maturity

## Intent

The template-script-generation change shipped a working pipeline but left three tiers of debt: (1) structural drift between design docs and code (`generate.py` location, `pyproject.toml` Python version, dead/missing templates), (2) the core separation promise is hollow — all component CSS sits monolithically in `base.html` (752 lines) while `$COMPONENT_CSS` is always `""`, and (3) spec/tests/verify warnings were archived unresolved. This change closes that gap — making components truly self-contained, data-table template-driven, patterns semantically structured, and SDD artifacts truthful.

## Scope

### In Scope
- **CSS distribution**: Extract each component's CSS from `base.html` into its own `<style>` block in the component template; `generate.py` concatenates into `$COMPONENT_CSS`
- **Data-table template refactor**: Replace 130-line `_render_data_table()` with template-based rendering using `data-table.html` + `$JOIN{data-table-row}` + `$JOIN{data-table-accordion-row}`. Delete dead `data-table-row.html`, recreate it properly, create missing `data-table-accordion-row.html`
- **Pattern slot enrichment**: Replace generic `$COMPONENTS_HTML` with named semantic slots (`$HEADER_SECTION`, `$BODY_SECTION`, etc.). Manifest gains a `slots` layer mapping component keys to pattern zones
- **Structural fixes**: Reconcile `generate.py` location (scripts/ vs root), fix `pyproject.toml` to `>=3.6`, normalize file naming
- **Spec/design sync**: Update `openspec/specs/cognitive-html-effectiveness/spec.md` to reflect 39 templates, fix R2 count, update design.md to match reality
- **Test hardening**: Extend placeholder test to all 7, add `html.parser` validation, validate quality checklist on all 10 patterns

### Out of Scope
- `--validate-only` CLI flag
- Palette extraction to `design-tokens.css`
- e2e subprocess tests
- Naming normalization (`chip` vs `chips`)
- `mobile_behavior` field implementation

## Capabilities

### New Capabilities
- `component-css-distribution`: Each component template carries its own `<style>` block; `generate.py` extracts and concatenates them into `$COMPONENT_CSS`, making components truly self-contained and composable
- `pattern-semantic-slots`: Pattern templates use named slots (`$HEADER_SECTION`, `$BODY_SECTION`, `$SIDEBAR_SECTION`) instead of generic `$COMPONENTS_HTML`. Manifest `slots` layer maps component keys to pattern zones

### Modified Capabilities
- `template-generation-system`: R2 template count corrected from 26 to 39. Data-table rendering moves from programmatic f-strings to template-based `$JOIN`. Structural fixes (file locations, Python version). Test coverage expanded.
- `data-table-dual-render`: `_render_data_table()` refactored from programmatic 130-line f-string builder to template-driven pipeline using `data-table-row.html` and new `data-table-accordion-row.html` fragments

## Approach

1. **CSS extraction** — Parse `base.html` to identify component-scoped CSS blocks. Move each block into its corresponding component template wrapped in `<style>`. `generate.py` scans component templates for `<style>` blocks, concatenates into `$COMPONENT_CSS`. `base.html` keeps only shared/reset CSS.
2. **Data-table refactor** — Replace `_render_data_table()` with a `process_joins()`-based pipeline. New `data-table-row.html` and `data-table-accordion-row.html` fragments define `<tr>` and `<details>` templates. `data-table.html` uses `$JOIN` markers for both.
3. **Pattern slots** — Each pattern template defines named placeholders. Manifest schema adds optional `slots` object. `generate.py` maps component output to slots; patterns without slot config fall back to `$COMPONENTS_HTML` for backward compatibility.
4. **Structural fixes** — Decide: keep `scripts/generate.py` and update all design artifacts to match, OR move to skill root. Fix `pyproject.toml`. Update spec R2 count.
5. **Test hardening** — Extend existing `test_base_template_has_placeholders` to all 7. Add `html.parser.HTMLParser`-based validation for template fragments. Parameterize quality checklist test across all 10 patterns.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `templates/base.html` | Modified | Strip component CSS (keep shared/reset only); `COMPONENT_CSS` becomes populated |
| `templates/components/*.html` | Modified | Each gains its own `<style>` block |
| `templates/components/data-table-row.html` | Removed + Recreated | Delete dead stub; recreate as proper `$col0`–`$colN` fragment |
| `templates/components/data-table-accordion-row.html` | New | Accordion fragment for mobile rows |
| `templates/components/data-table.html` | Modified | Replace `$DATA_TABLE_HTML` with `$JOIN{data-table-row}` + `$JOIN{data-table-accordion-row}` |
| `templates/patterns/*.html` | Modified | Replace `$COMPONENTS_HTML` with named semantic slots |
| `scripts/generate.py` | Modified | CSS extraction, data-table refactor, slot mapping, structural fixes |
| `pyproject.toml` | Modified | `requires-python = ">=3.6"` |
| `manifest-schema.json` | Modified | Add `slots` object definition |
| `openspec/specs/cognitive-html-effectiveness/spec.md` | Modified | R2 count → 39, add component CSS + slot requirements |
| `tests/` | Modified | Expanded placeholder test, html.parser validation, all-pattern quality tests |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| CSS extraction breaks existing styles | Medium | Extract per-component; visual regression test via `html.parser` structure checks before/after |
| Data-table refactor changes output HTML structure | Medium | Snapshot test current output before refactor; compare DOM structure after |
| Pattern slot migration breaks backward compat | Low | Fallback: if no `slots` in manifest, use `$COMPONENTS_HTML` path |
| Large change surface (39 files) overwhelms review | High | Chain into focused PRs: CSS distribution → data-table → slots → structural → tests |

## Rollback Plan

All changes are in `templates/`, `scripts/generate.py`, `tests/`, and `manifest-schema.json`. `git revert` the change commit(s). Existing direct-generation SKILL.md path is untouched. Template path falls back to pre-change state.

## Dependencies

- Python 3.6+ stdlib (already satisfied)
- Existing 46 tests as regression baseline
- `html.parser` from stdlib (already available)

## Success Criteria

- [ ] `$COMPONENT_CSS` populated with component-scoped CSS (not empty string)
- [ ] `base.html` contains only shared/reset CSS (≤300 lines from 752)
- [ ] `_render_data_table()` uses template fragments, not f-strings
- [ ] `data-table-accordion-row.html` exists and is loaded by code path
- [ ] All 10 patterns have named slots (not just `$COMPONENTS_HTML`)
- [ ] `pyproject.toml` says `>=3.6`
- [ ] Spec R2 says 39 templates (or distinguishes core vs fragment count)
- [ ] All 7 base.html placeholders tested
- [ ] All 10 patterns pass quality checklist validation
- [ ] All existing 46 tests still pass after refactor
