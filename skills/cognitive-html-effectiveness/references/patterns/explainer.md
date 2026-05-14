# Pattern: Explainer

A document that teaches a feature, concept, or system — designed for someone who needs to understand it, not just reference it.

## When to use

- User asks "explícame cómo funciona X en el código"
- User says "cómo funciona", "concept explainer", "feature explainer"
- User wants to understand a specific part of the codebase
- User asks "qué es X" or "how does X work in this repo"

## Structure blueprint

```
┌──────────────────────────────────────────────────────────┐
│ Sidebar (sticky, left)                   │ Main content   │
│ ┌─────────────────────┐                  │                │
│ │ On this page         │                  │ Header         │
│ │  TL;DR               │                  │  Eyebrow       │
│ │  Request path        │                  │  Title         │
│ │   1. Identify        │                  │  TL;DR box     │
│ │   2. Bucket lookup   │                  │                │
│ │   3. Consume         │                  │ Step-by-step   │
│ │   4. Reject          │                  │  ┌──────────┐ │
│ │  Configuring a route │                  │  │ 1. Step   │ │
│ │  Gotchas             │                  │  │  details  │ │
│ │  FAQ                 │                  │  └──────────┘ │
│ │                      │                  │  ┌──────────┐ │
│ │ Files read           │                  │  │ 2. Step   │ │
│ │  middleware/x.ts     │                  │  │  details  │ │
│ │  lib/y.ts            │                  │  └──────────┘ │
│ └─────────────────────┘                  │                │
│                                          │ Config section │
│                                          │  Tabbed code   │
│                                          │  samples        │
│                                          │                │
│                                          │ Gotchas list   │
│                                          │ FAQ            │
└──────────────────────────────────────────┘
```

## Component prescriptions

| Position | Component |
|----------|-----------|
| Sidebar nav | **Sidebar Navigation** — `components.md` § 15 |
| TL;DR | **TL;DR Box** — `components.md` § 1 |
| Steps | **Collapsible snippet** — `components.md` § 6 |
| Config samples | **Tabbed Interface** — `components.md` § 8 |
| Tips | **Callout / Note** — `components.md` § 9 |
| Gotchas | Custom list with bold + code |
| FAQ | **FAQ Section** — `components.md` § 14 |

## Page layout CSS

```css
.page {
  max-width: var(--container-page); margin: 0 auto;
  display: grid;
  grid-template-columns: 200px minmax(0, 1fr);
  gap: 48px;
}
@media (max-width: 920px) { .page { grid-template-columns: 1fr; } .page nav { display: none; } }
```

## Content writing rules for explainers

1. **Start with the TL;DR.** The first thing the reader sees should be a 2-3 sentence summary of what the feature does, where it lives, and the key insight.
2. **Show the request path / flow.** Most explainers benefit from a step-by-step walkthrough with collapsible sections.
3. **Show how to configure it.** Include a tabbed interface with the config file, the code that reads it, and the resulting behavior.
4. **Surface gotchas.** Anything that surprised you when you read the code goes here.
5. **End with FAQ.** Anticipate the 2-3 most common questions and answer them.

## Detailed steps structure

Each step has:
- **Number** (in sidebar, the step is collapsible)
- **What it does** — one sentence
- **Where it lives** — file:line in mono font
- **The relevant code** — inside the collapsible body
- Optional: **Why it matters** — if non-obvious

## FAQ format

```html
<h2>FAQ</h2>
<dl class="faq">
  <dt>How do I exempt internal traffic?</dt>
  <dd>Set <code>x-acme-internal: 1</code> from the caller.</dd>
  <dt>Where do I see who's getting limited?</dt>
  <dd>Every <code>429</code> emits a <code>ratelimit.rejected</code> metric.</dd>
</dl>
```

## Key insight

The explainer pattern is THE most important pattern for codebase understanding. Its power comes from the combination of:
- **Spatial layout** (sidebar tells you where you are)
- **Collapsible steps** (don't overwhelm, let the reader choose depth)
- **Tabbed config** (see the config, the code, and the result in one place)
- **Gotchas + FAQ** (the stuff you'd only know from reading the code)

## Full examples

- **Feature explainer**: See `resources/14-research-feature-explainer.html` in the project — rate limiting explained with collapsible steps, tabbed config, and FAQ
- **Concept explainer**: See `resources/15-research-concept-explainer.html` in the project — consistent hashing with interactive ring visualization
