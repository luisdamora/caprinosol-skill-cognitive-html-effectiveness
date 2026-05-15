# Component CSS Distribution Specification

## Purpose

Each component template is self-contained: it carries its own `<style>` block. The generator extracts and concatenates component CSS into `$COMPONENT_CSS`, making `base.html` a pure shell with only shared/reset styles.

## Requirements

### R1: Component `<style>` Blocks

Each component template MUST contain a `<style>` block with CSS scoped to that component. `generate.py` MUST scan all loaded component templates for `<style>` blocks, extract their content, and concatenate into the `$COMPONENT_CSS` placeholder in `base.html`. `base.html` MUST contain only shared/reset CSS — zero component-specific rules.

| Scenario | Given | When | Then |
|----------|-------|------|------|
| CSS extracted from component | `callout.html` with embedded `<style>` | `generate.py` processes it | `<style>` content included in `$COMPONENT_CSS` |
| Base has no component CSS | all component CSS distributed to templates | reading `base.html` | only shared/reset CSS remains (≤300 lines) |
| Empty manifest valid | manifest with no CSS-bearing components | `generate.py` renders | `$COMPONENT_CSS` resolves to empty string, no error |
| All components carry styles | any component template | reading content | `<style>` block present with scoped selectors |
| CSS deduplication | same component loaded twice via manifest | `generate.py` concatenates | component `<style>` appears once in output |

---

## Coverage Summary

| Req | Happy Path | Edge Case | Error State |
|-----|-----------|-----------|-------------|
| R1 — Component `<style>` Blocks | ✅ | ✅ | ✅ |
