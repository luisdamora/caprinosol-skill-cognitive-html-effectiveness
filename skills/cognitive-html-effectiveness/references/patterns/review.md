# Pattern: Review

Annotated code review — a diff rendered with margin notes, severity tags, and visual cues that make it faster to scan than scrolling a terminal.

## When to use

- User says "revisa este PR", "code review", "analiza este diff"
- User wants to understand what changed and why
- User asks "qué hay que arreglar" or "is this safe to merge"
- User wants a writeup for reviewers: "escribe la descripción del PR"

## Two sub-patterns

### A) Annotated Diff (review from the reviewer's perspective)

Show the diff with inline annotations, severity tags, and a recommendation.

```
┌──────────────────────────────────────────────┐
│ Header                                         │
│   PR #, title, author, stats                   │
│   Severity summary pills                       │
├──────────────────────────────────────────────┤
│ TL;DR Box                                      │
│   "This PR [does X]. Key concern is [Y]."       │
├──────────────────────────────────────────────┤
│ File-by-file review                            │
│ ┌── src/auth.ts ─────────────────────────┐    │
│ │  ⚠ Medium · [annotation on line range]   │    │
│ │  + const session = await Store.get(id);   │    │
│ │  - const session = Store.getSync(id);     │    │
│ │  ✔ Good · [annotation]                    │    │
│ └──────────────────────────────────────────┘    │
├──────────────────────────────────────────────┤
│ Recommendation: Approve / Request Changes       │
└──────────────────────────────────────────────┘
```

### B) PR Writeup (from the author's perspective)

A document the PR author creates for reviewers.

```
┌──────────────────────────────────────────────┐
│ Header: PR title, branch, stats                │
├──────────────────────────────────────────────┤
│ Motivation: why this change exists             │
├──────────────────────────────────────────────┤
│ Before / After (side by side or visual)        │
├──────────────────────────────────────────────┤
│ File tour: what changed where, and why         │
├──────────────────────────────────────────────┤
│ Review focus: where to look first              │
├──────────────────────────────────────────────┤
│ Out of scope: what this PR does NOT do         │
├──────────────────────────────────────────────┤
│ Testing: how to verify                         │
└──────────────────────────────────────────────┘
```

## Component prescriptions

| For annotated diff | Component | From |
|-------------------|-----------|------|
| Severity pills | **Chip / Tag** (pill variant) | `components.md` § 4 |
| TL;DR | **TL;DR Box** | `components.md` § 1 |
| Diff display | **Code Panel** (with .diff-line) | `components.md` § 7 |
| Recommendation | custom card | see below |

| For PR writeup | Component | From |
|---------------|-----------|------|
| Stats | **Summary Band** / stat cards | `components.md` § 2 |
| Before/After | **Tabbed Interface** | `components.md` § 8 |
| Gotchas | **Callout** | `components.md` § 9 |

## Key CSS for severity tags in annotations

```css
.annotation {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 8px 0; margin: 4px 0;
  border-left: 3px solid transparent; padding-left: 14px;
}
.annotation.high   { border-color: var(--rust); background: var(--surface-danger-soft); }
.annotation.medium { border-color: var(--clay); background: var(--surface-warning-soft); }
.annotation.low    { border-color: var(--gray-300); }
.annotation.good   { border-color: var(--olive); background: var(--surface-success-soft); }
.annotation-tag {
  font-family: var(--mono); font-size: 10px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.04em;
  padding: 2px 8px; border-radius: var(--radius-pill);
  flex-shrink: 0; min-width: 60px; text-align: center;
}
.annotation.high .annotation-tag   { background: var(--rust); color: var(--white); }
.annotation.medium .annotation-tag { background: var(--clay); color: var(--white); }
.annotation.low .annotation-tag    { background: var(--bg-muted); color: var(--text-muted); }
.annotation.good .annotation-tag   { background: var(--olive); color: var(--white); }
.annotation-body { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }
```

## Severity guide

| Tag | When to use |
|-----|-------------|
| 🔴 High | Security issue, data loss risk, crash potential |
| 🟠 Medium | Logic error, missing edge case handling, race condition |
| ⚪ Low | Style nit, naming suggestion, minor improvement |
| 🟢 Good | Well-done pattern, good test, clean refactor |

## PR writeup key sections

```html
<section>
  <h2>Motivation</h2>
  <p>What problem does this solve? Link the issue.</p>
</section>

<section>
  <h2>What changed</h2>
  <div class="before-after">
    <!-- Tabbed Interface: Before / After -->
  </div>
</section>

<section>
  <h2>File-by-file tour</h2>
  <div class="file-tour">
    <div class="file-entry">
      <span class="file-path">src/auth/middleware.ts</span>
      <p>Extracted token validation into a shared helper. The logic is unchanged — just moved.</p>
    </div>
  </div>
</section>

<section>
  <h2>Where to focus review</h2>
  <ol>
    <li><strong>src/sessionStore.ts:42-68</strong> — the new LRU cache logic</li>
    <li><strong>config/limits.yaml</strong> — the new worker tier defaults</li>
  </ol>
</section>

<section>
  <h2>Out of scope</h2>
  <ul>
    <li>Session expiration TTL tuning (separate PR)</li>
    <li>Cache invalidation across workers (next sprint)</li>
  </ul>
</section>
```

## Full examples

- **Annotated diff**: See `resources/03-code-review-pr.html` in the project
- **PR writeup**: See `resources/17-pr-writeup.html` in the project
