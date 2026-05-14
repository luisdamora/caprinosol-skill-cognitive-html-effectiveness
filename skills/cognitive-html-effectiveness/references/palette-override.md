# Palette Override — Customizing Theme Tokens per Project

The skill ships with a warm, earthy design system.
Projects can override color tokens, font stacks, and a few foundation tokens via a YAML block in the root `AGENTS.md`.

## How it works

1.  **At generation time**, look for a `AGENTS.md` file in the project root.
2.  If it exists, scan for the block delimited by `<!-- cognitive-html:palette -->` and `<!-- /cognitive-html:palette -->`.
3.  If the block exists, parse the YAML inside it. Each key maps to a CSS variable name.
4.  Any keys found **replace** the default value. Keys not found keep their default.

## Block format

```markdown
<!-- cognitive-html:palette -->
```yaml
# Custom theme overrides for cognitive-html-effectiveness
ivory: "#FEFEFE"
slate: "#1A1A2E"
clay:  "#E94560"
olive: "#0F3460"
oat:   "#E8E8E8"
rust:  "#C0392B"
font-display: '"Iowan Old Style", Georgia, serif'
font-body: 'Inter, system-ui, sans-serif'
radius-panel: "18px"
container-reading: "70ch"
```
<!-- /cognitive-html:palette -->
```

## Recommended override keys

| Key | CSS Variable | Role |
|-----|--------------|------|
| `ivory` | `--ivory` | Page background |
| `slate` | `--slate` | Primary text, dark surfaces |
| `clay` | `--clay` | Accent, warnings, highlights |
| `clay-d` | `--clay-d` | Darker accent (hover) |
| `oat` | `--oat` | Secondary surface, muted bg |
| `olive` | `--olive` | Success, positive indicators |
| `rust` | `--rust` | Danger, high severity |
| `gray-100` | `--gray-100` | Subtle background |
| `gray-200` | `--gray-200` | Light border |
| `gray-300` | `--gray-300` | Default border |
| `gray-500` | `--gray-500` | Secondary text |
| `gray-700` | `--gray-700` | Body text |
| `white` | `--white` | Card backgrounds |
| `font-display` | `--font-display` | Heading serif stack |
| `font-body` | `--font-body` | Body sans stack |
| `font-mono` | `--font-mono` | Code/metadata stack |
| `radius-panel` | `--radius-panel` | Card radius |
| `radius-row` | `--radius-row` | Dense row radius |
| `container-reading` | `--container-reading` | Long-form width |
| `container-page` | `--container-page` | Page width |

> Advanced users may override any token exposed by `assets/design-tokens.css`, but the keys above are the safest ones to customize without breaking visual balance.

## Fallback behavior

- **No AGENTS.md exists** → use full default palette.
- **AGENTS.md exists but no `cognitive-html:palette` block** → use full default palette.
- **Block exists with partial overrides** → merge: overridden keys win, rest stay default.

## Example: Corporate brand palette

```yaml
# A cooler, blue-toned corporate look
ivory: "#F5F7FA"
slate: "#1E293B"
clay:  "#3B82F6"
olive: "#10B981"
oat:   "#E2E8F0"
rust:  "#EF4444"
```

## Guardrails

- Keep overrides small — only change what needs to match your brand.
- Preserve semantic intent: warning colors should still feel warning-like, success colors should still feel positive.
- If you override font stacks, keep the three-role model: display/serif, body/sans, mono.
- If you override radii or widths, do it consistently across all related tokens.
- Overriding everything usually produces worse results than selective tweaks.
