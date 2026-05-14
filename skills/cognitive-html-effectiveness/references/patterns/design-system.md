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

## Foundation shell

The design-system pattern is the canonical place to show the whole foundation layer. Start from the same shared shell as the other patterns, then render swatches, type, spacing, radius, and shadows as sections.

## Mobile-first behavior

- This page should prove the system works on a phone, not just describe desktop tokens.
- Swatches stack naturally, typography rows collapse into one column, and spacing demos stay readable at `390px`.
- Include at least one section that explicitly shows touch target, page padding, and mobile reading width tokens.

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
.swatch-preview.ivory { background: var(--ivory); }
.swatch-preview.slate { background: var(--slate); }
.swatch-preview.clay { background: var(--clay); }
.swatch-preview.olive { background: var(--olive); }
.swatch-preview.oat { background: var(--oat); }
.swatch-info {
  padding: 12px 14px;
}
.swatch-name {
  font-family: var(--serif); font-size: 15px; font-weight: 500; color: var(--text-primary); margin-bottom: 4px;
}
.swatch-hex {
  font-family: var(--mono); font-size: 12px; color: var(--text-muted);
}
@media (max-width: 640px) {
  .swatches { grid-template-columns: 1fr 1fr; }
}
```

Usage — each swatch gets a `--bg` inline style with the actual color, and the hex is shown below:

```html
<div class="swatches">
  <div class="swatch">
    <div class="swatch-preview ivory"></div>
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
.type-sample.display { font-family: var(--serif); font-size: var(--text-display); font-weight: var(--weight-display); line-height: var(--lh-display); }
.type-sample.h1 { font-family: var(--serif); font-size: var(--text-h1); font-weight: var(--weight-heading); line-height: var(--lh-heading); }
.type-sample.body { font-family: var(--sans); font-size: var(--text-body); font-weight: var(--weight-body); line-height: var(--lh-body); }
@media (max-width: 640px) {
  .type-row { grid-template-columns: 1fr; gap: 10px; }
}
```

Usage — render each level at its actual size:

```html
<div class="type-scale">
  <div class="type-row">
    <div class="type-meta">
      <span class="family">Display serif</span><br>var(--text-display) / 600<br>Hero title
    </div>
    <div class="type-sample display">
      The quick brown fox
    </div>
  </div>
  <div class="type-row">
    <div class="type-meta">
      <span class="family">Body sans</span><br>var(--text-body) / 400<br>Body
    </div>
    <div class="type-sample body">
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
@media (max-width: 640px) {
  .space-row { grid-template-columns: 56px 1fr 56px; gap: 12px; }
}
```

## Include the rest of the system

Do not stop at colors and type. A strong design-system page should also show:

- the canonical page shell (`.page`, `.page-header`, `.page-main`, `.page-footer`)
- border radius tokens
- shadow levels
- semantic surfaces (page/card/muted/accent/inverse)
- example controls (button, pill, tab, callout) using the shared tokens

## Full example

See `resources/05-design-system.html` in the project for a worked example: colors, type scale, spacing tokens, and shadows extracted from a codebase and rendered as visual references.
