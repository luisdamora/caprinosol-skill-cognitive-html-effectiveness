# Pattern: Deck

A slide presentation as a single HTML file — arrow keys to navigate, no build step, no Keynote.

## When to use

- User asks for "presentación", "slides", "deck", "demo"
- User wants to present something in a meeting
- User says "prepara algo para exponer", "hazme unos slides"
- User references a Slack thread, design doc, or meeting notes they want turned into slides

## Structure blueprint

```
┌────────────────────────────────────────────────┐
│ Slide 1 — Title (optional: inverted)             │
│   Eyebrow + big title + subtitle + meta          │
├────────────────────────────────────────────────┤
│ Slide 2 — Content (shipped list, metrics, ...)   │
├────────────────────────────────────────────────┤
│ Slide 3 — Content                                │
├────────────────────────────────────────────────┤
│ Slide N — Decision needed (inverted)             │
├────────────────────────────────────────────────┤
│ Slide N+1 — Next steps / closing                  │
└────────────────────────────────────────────────┘
│ Fixed counter: "3 / 6" bottom-right               │
└────────────────────────────────────────────────┘
```

## Slide types

| Type | Visual | Best for |
|------|--------|----------|
| Title | Big serif headline, ornament, byline | Opening |
| List | Items with dots/icons, one-line descriptions | What shipped, what's next |
| Progress | Progress bars with percentages | In-progress updates |
| Metrics | Large numbers + delta indicators | KPIs, performance data |
| Decision | Inverted bg (dark), framed question card | Asking the room to decide |
| Closing | List + footnote | Next steps, Q&A prompt |

## Key CSS

```css
html { scroll-behavior: smooth; }
body {
  scroll-snap-type: y mandatory;
  overflow-x: hidden;
}
.slide {
  width: 100vw;
  height: 100vh;
  scroll-snap-align: start;
  scroll-snap-stop: always;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8vh 6vw;
}
.slide.invert {
  background: var(--slate);
  color: var(--ivory);
}
.slide.invert .eyebrow { color: var(--gray-300); }
.slide-inner {
  width: 100%;
  max-width: 780px;
}
```

## Navigation JS (standard, always include)

```js
const slides = Array.from(document.querySelectorAll('.slide'));
const counter = document.getElementById('counter');
let current = 0;

function go(i) {
  current = Math.max(0, Math.min(slides.length - 1, i));
  slides[current].scrollIntoView({ behavior: 'smooth' });
}

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { e.preventDefault(); go(current + 1); }
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')                     { e.preventDefault(); go(current - 1); }
});

const obs = new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (en.isIntersecting) {
      current = slides.indexOf(en.target);
      counter.textContent = (current + 1) + ' / ' + slides.length;
    }
  });
}, { threshold: 0.6 });

slides.forEach(s => obs.observe(s));
```

## Counter element

Always include at the bottom of `<body>`:

```html
<div id="counter">1 / 6</div>
```

```css
#counter {
  position: fixed;
  bottom: 22px; right: 28px;
  font-family: var(--mono);
  font-size: 12px;
  color: var(--gray-500);
  user-select: none;
  z-index: 10;
}
```

## Component prescriptions

| Slide content | Component |
|---------------|-----------|
| Shipped items | List with dots (custom) |
| Progress | **Progress Bar** — `components.md` § 12 |
| Metrics | Large metric blocks (custom) + sparkline SVG |
| Decision | **Decision Card** — `components.md` § 13 |
| Next steps | List with dash prefixes (custom) |

## Guidelines

- **5-8 slides maximum.** More than that and people stop paying attention.
- **One idea per slide.** Never cram two unrelated things on one slide.
- **Use the inverted slide sparingly.** It's for decisions and emphasis — 1 per deck max.
- **End with an action.** "Next week", "Decision needed", or "Questions?".
- **No bullets with sub-bullets.** If you need hierarchy, it's two slides.

## Full example

See `resources/09-slide-deck.html` in the project for a worked example: Platform Engineering weekly demo with 6 slides — title, shipped list, in-progress, metrics, decision card, and next steps.
