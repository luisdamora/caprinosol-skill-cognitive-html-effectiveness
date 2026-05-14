# Palette Override — Customizing Colors per Project

The skill ships with a warm, earthy default palette (ivory / slate / clay / olive / oat).
Projects can override any token via a YAML block in the root `AGENTS.md`.

## How it works

1.  **At generation time**, look for a `AGENTS.md` file in the project root.
2.  If it exists, scan for the block delimited by `<!-- cognitive-html:palette -->` and `<!-- /cognitive-html:palette -->`.
3.  If the block exists, parse the YAML inside it. Each key maps to a CSS variable name.
4.  Any keys found **replace** the default value. Keys not found keep their default.

## Block format

```markdown
<!-- cognitive-html:palette -->
```yaml
# Custom color overrides for cognitive-html-effectiveness
ivory: "#FEFEFE"
slate: "#1A1A2E"
clay:  "#E94560"
olive: "#0F3460"
oat:   "#E8E8E8"
rust:  "#C0392B"
```
<!-- /cognitive-html:palette -->
```

## Supported override keys

| Key     | CSS Variable | Role                         |
|---------|--------------|------------------------------|
| `ivory`   | `--ivory`     | Page background              |
| `slate`   | `--slate`     | Primary text, dark surfaces  |
| `clay`    | `--clay`      | Accent, warnings, highlights |
| `clay-d`  | `--clay-d`    | Darker accent (hover)        |
| `oat`     | `--oat`       | Secondary surface, muted bg  |
| `olive`   | `--olive`     | Success, positive indicators |
| `rust`    | `--rust`      | Danger, high severity        |
| `gray-100`| `--gray-100`  | Subtle background            |
| `gray-200`| `--gray-200`  | Light border                 |
| `gray-300`| `--gray-300`  | Default border               |
| `gray-500`| `--gray-500`  | Secondary text               |
| `gray-700`| `--gray-700`  | Body text                    |
| `white`   | `--white`     | Card backgrounds             |

> You can also override `serif`, `sans`, and `mono` if you want to change the font stack.
> Format: `sans: "Inter, system-ui, sans-serif"`

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

## Tip

Keep the overrides small — only change what needs to match your brand.
The default palette is carefully balanced for readability and information hierarchy.
Overriding everything usually produces worse results than selective tweaks.
