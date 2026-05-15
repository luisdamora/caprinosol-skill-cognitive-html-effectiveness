# Proposal: Template-Script Generation

## Intent

LLM reads ~3,200 lines of reference per invocation — ~95% boilerplate CSS/HTML that never varies. Template generation separates PRESENTATION (templates) from CONTENT (per-run data), cutting LLM read to ~150 lines via `catalog-summary.md`.

## Scope

**In**: 26 templates (1 base + 15 components + 10 patterns) • `generate.py` (stdlib only) • `catalog-summary.md` • `manifest.json` schema • Data Table dual-render (<table> ↔ <details>) • All 10 patterns + 15 components • Hybrid artifact store (engram + openspec)

**Out**: jinja2/mako • JS for table transform • Replacing existing SKILL.md direct path • Bundlers/WASM

## Capabilities

> No existing specs — all new.

| Capability | Description |
|------------|-------------|
| `template-generation-system` | LLM writes `manifest.json` → `generate.py` renders stdlib templates → HTML |
| `data-table-dual-render` | CSS `@media` toggle `<table>` >768px / `<details>` ≤768px. Zero JS |
| `template-catalog` | `catalog-summary.md` entry point documenting 26 templates |

## Approach + Key Decisions

1. **Manifest-first**: LLM reads ~150-line `catalog-summary.md` → writes `manifest.json`. `generate.py` validates + renders via `string.Template` (`$PLACEHOLDER`). Python stdlib only — zero-install on any 3.6+.
2. **Dual-render tables**: Both `<table>` + `<details>` emitted; CSS `display` toggle at 768px. No JS or reflow cost.
3. **Template tree**: `base.html` → 15 components → 10 patterns. `$JOIN` markers for repeated data (stdlib has no loops).
4. **Backward compatible**: Existing SKILL.md direct path untouched. Template path additive.

## Affected Areas

| Area | Impact |
|------|--------|
| `skills/.../SKILL.md` | Modified — add template workflow |
| `skills/.../references/` | Modified — boilerplate moves to templates |
| `generate.py` | New |
| `templates/` (26 files) | New |
| `catalog-summary.md` | New |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Template drift from SKILL.md | Med | CI: diff generated output per pattern |
| stdlib no-loop limitation | Low | `$JOIN` marker; Python pre-joins data |
| Invalid manifest.json | Low | Schema validation before render |
| Mobile accordion a11y | Low | `<details open>` is natively accessible |

## Rollback Plan

Revert `templates/`, `generate.py`, `catalog-summary.md` and SKILL.md changes via git. Direct path always works — no user-facing breakage.

## Dependencies

Python 3.6+ (stdlib only). Existing pattern + component references as content source.

## Success Criteria

- [ ] `python generate.py manifest.json` produces valid HTML for all 10 patterns
- [ ] 26 template files exist (1 base + 15 components + 10 patterns)
- [ ] `catalog-summary.md` ≤ 200 lines
- [ ] Data Table renders `<table>` >768px, `<details>` ≤768px (viewport test)
- [ ] Zero new pip packages
- [ ] 17 automatable quality items baked into templates
- [ ] Existing SKILL.md direct path still works
