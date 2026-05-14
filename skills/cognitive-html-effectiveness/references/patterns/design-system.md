# Pattern: Design System

Showcase the visual identity of a project — colors, typography, spacing, and component tokens — rendered as visual swatches and scales.

## When to use

- User asks to see "design system", "colores", "tipografía", "tokens"
- User wants to extract visual tokens from a codebase
- User asks "muéstrame los colores que usa este proyecto"
- User wants a living reference of design decisions

## Structure blueprint

```
┌──────────────────────────────────────────────────────────┐
│ Header                                                    │
│   Title: "[Project] Design System"                         │
│   Subtitle: "Extracted from [source]"                      │
├──────────────────────────────────────────────────────────┤
│ Section: Palette                                           │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │
│ │ #xxx │ │ #xxx │ │ #xxx │ │ #xxx │ │ #xxx │  ...       │
│ │ name │ │ name │ │ name │ │ name │ │ name │           │
│ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘           │
├──────────────────────────────────────────────────────────┤
│ Section: Typography                                       │
│   Scale showing each level rendered at its actual size     │
│   "Heading 1 — serif, 38px, 500 weight"                   │
│   "Body — sans, 15px, 400 weight"                         │
├──────────────────────────────────────────────────────────┤
│ Section: Spacing                                          │
│   Visual scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px   │
├──────────────────────────────────────────────────────────┤
│ Section: Shadows / Borders / Radius (if applicable)       │
└──────────────────────────────────────────────────────────┘
```

## Component prescriptions

All custom — no standard components needed beyond basic layout.

## Color swatch CSS

```css
.swatches {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
}
.swatch {
  background: var(--bg-card);
  border: var(--border);
  border-radius: var(--radius-panel);
  overflow: hidden;
}
.swatch-preview {
  height: 80px;
}
.swatch-info {
  padding: 12px 14px;
}
.swatch-name {
  font-family: var(--serif); font-size: 15px; font-weight: 500; color: var(--text-primary); margin-bottom: 4px;
}
.swatch-hex {
  font-family: var(--mono); font-size: 12px; color: var(--text-muted);
}
```

Usage — each swatch gets a `--bg` inline style with the actual color, and the hex is shown below:

```html
<div class="swatches">
  <div class="swatch">
    <div class="swatch-preview" style="background:var(--ivory)"></div>
    <div class="swatch-info">
      <div class="swatch-name">Ivory — Page bg</div>
      <div class="swatch-hex">#FAF9F5</div>
    </div>
  </div>
  <!-- repeat for each color -->
</div>
```

## Typography scale CSS

```css
.type-scale { display: flex; flex-direction: column; gap: 32px; }
.type-row {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 24px;
  align-items: baseline;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--gray-100);
}
.type-meta {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.6;
}
.type-meta .family { color: var(--text-primary); font-weight: 600; }
.type-sample { color: var(--text-primary); }
```

Usage — render each level at its actual size:

```html
<div class="type-scale">
  <div class="type-row">
    <div class="type-meta">
      <span class="family">Serif</span><br>38px / 500<br>Heading 1
    </div>
    <div class="type-sample" style="font-family:var(--serif);font-size:38px;font-weight:500;line-height:1.15">
      The quick brown fox
    </div>
  </div>
  <div class="type-row">
    <div class="type-meta">
      <span class="family">Sans</span><br>15px / 400<br>Body
    </div>
    <div class="type-sample" style="font-family:var(--sans);font-size:15px;line-height:1.6">
      The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs.
    </div>
  </div>
  <!-- ... -->
</div>
```

## Spacing scale

```css
.space-scale { display: flex; flex-direction: column; gap: 0; }
.space-row {
  display: grid;
  grid-template-columns: 60px 1fr 60px;
  gap: 18px;
  align-items: center;
  padding: 8px 0;
}
.space-label { font-family: var(--mono); font-size: 12px; color: var(--text-muted); text-align: right; }
.space-bar { height: 100%; min-height: 8px; background: var(--clay); border-radius: 2px; }
.space-px { font-family: var(--mono); font-size: 12px; color: var(--text-muted); }
```

## Full example

See `resources/05-design-system.html` in the project for a worked example: colors, type scale, spacing tokens, and shadows extracted from a codebase and rendered as visual references.
