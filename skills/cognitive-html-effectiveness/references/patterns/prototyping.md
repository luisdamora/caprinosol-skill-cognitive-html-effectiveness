# Pattern: Prototyping

A throwaway interactive page for feeling motion, interaction, or behavior — things that can't be described in prose.

## When to use

- User asks for "prototipo", "animación", "transición", "efecto"
- User wants to tune a CSS animation before wiring it into code
- User asks for a clickable flow or screen mockup
- User says "muéstrame cómo se vería", "let me feel it"

## Two sub-patterns

### A) Animation Sandbox

Isolate a transition/animation with live controls (duration, easing curve, trigger button).

```
┌──────────────────────────────────────────┐
│ Header: what we're prototyping             │
├──────────────────────────────────────────┤
│ Controls                                    │
│   Duration: [====slider====] 300ms          │
│   Easing:   [dropdown: ease/ease-in/...]    │
│   [Trigger] button                          │
├──────────────────────────────────────────┤
│ Preview area                                │
│   ┌──────────────────────────┐            │
│   │  The animated element     │            │
│   │  moves/transforms here    │            │
│   └──────────────────────────┘            │
├──────────────────────────────────────────┤
│ Copy CSS button                            │
└──────────────────────────────────────────┘
```

### B) Clickable Flow

Linked screens that simulate a user journey through an interface.

```
┌──────────────────────────────────────────┐
│ Screen 1 ──→ Screen 2 ──→ Screen 3 ──→ S4│
├──────────────────────────────────────────┤
│ ┌────────────────────────────────┐       │
│ │  [Header bar]                   │       │
│ │  [Content area]                 │       │
│ │  [Button → next]                │       │
│ └────────────────────────────────┘       │
├──────────────────────────────────────────┤
│ Step indicator: ● ○ ○ ○                   │
└──────────────────────────────────────────┘
```

## Animation sandbox — key CSS/JS

```html
<div class="sandbox">
  <div class="controls">
    <label>Duration: <span id="durVal">300</span>ms</label>
    <input type="range" id="duration" min="50" max="2000" value="300" step="10">

    <label>Easing:
      <select id="easing">
        <option value="ease">ease</option>
        <option value="ease-in">ease-in</option>
        <option value="ease-out">ease-out</option>
        <option value="ease-in-out">ease-in-out</option>
        <option value="cubic-bezier(0.34,1.56,0.64,1)">spring</option>
      </select>
    </label>

    <button id="trigger">Animate</button>
  </div>

  <div class="preview" id="preview">
    <div class="stage">
      <div class="ball" id="ball"></div>
    </div>
  </div>
</div>
```

```js
const ball = document.getElementById('ball');
const trigger = document.getElementById('trigger');
const durationSlider = document.getElementById('duration');
const easingSelect = document.getElementById('easing');
const durVal = document.getElementById('durVal');

durationSlider.addEventListener('input', () => {
  durVal.textContent = durationSlider.value;
});

trigger.addEventListener('click', () => {
  ball.style.transition = 'none';
  ball.style.transform = 'translateX(0)';
  ball.offsetHeight; // force reflow

  const dur = durationSlider.value + 'ms';
  const ease = easingSelect.value;
  ball.style.transition = `transform ${dur} ${ease}`;
  ball.style.transform = 'translateX(calc(100% - 50px))';
});
```

## Clickable flow — key JS

Use a simple screen stack with visibility toggling:

```js
const screens = document.querySelectorAll('.screen');
let current = 0;

function show(i) {
  screens.forEach((s, idx) => { s.style.display = idx === i ? 'flex' : 'none'; });
  current = i;
  updateIndicator();
}

document.querySelectorAll('.next-btn').forEach(btn => {
  btn.addEventListener('click', () => { if (current < screens.length - 1) show(current + 1); });
});
document.querySelectorAll('.prev-btn').forEach(btn => {
  btn.addEventListener('click', () => { if (current > 0) show(current - 1); });
});

show(0);
```

## Export

For animation sandbox: "Copy CSS" button that copies the current transition rule.  
For clickable flow: "Copy screens as HTML" or export each screen description.

## Mobile-first behavior

- Controls stack vertically on phone; sliders, selects, and buttons should be easy to manipulate with a thumb.
- The preview area must still communicate the behavior when narrow; if needed, reduce ornament before shrinking the interaction.
- Clickable flows should show one screen at a time on mobile, with obvious next/back controls.
- If the prototype depends on motion, include a reduced-motion fallback for readers who disable animation.

## Full examples

- **Animation sandbox**: See `resources/07-prototype-animation.html` in the project
- **Clickable flow**: See `resources/08-prototype-interaction.html` in the project
