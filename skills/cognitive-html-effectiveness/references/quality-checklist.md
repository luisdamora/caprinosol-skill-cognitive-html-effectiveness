# Quality Checklist — Before Delivering Any HTML

Run through this checklist before returning a generated HTML file to the user.
Every item is a gate; if any fails, fix it before delivering.

## Structural gates

- [ ] **Self-contained**: zero external dependencies. No CDN links, no `<link>`, no `<script src="...">`. All CSS is in a `<style>` block. All JS (if any) is in a `<script>` block. All SVG is inline.
- [ ] **Opens in any browser**: the file works when opened directly (`file://`) — no server needed.
- [ ] **Responsive**: has `viewport` meta tag. Uses media queries or fluid units (`clamp`, `%`, `vw`) so it works on mobile. Test mentally at 375px and 1200px widths.
- [ ] **No build step**: the HTML is the artifact. No npm, no bundler, no TypeScript compilation needed.

## Content gates

- [ ] **Language matches prompt**: ALL visible text (headings, labels, descriptions, TL;DR, captions, button text, tooltips) is in the same language as the user's prompt. Code, file paths, and technical identifiers stay in English.
- [ ] **TL;DR first**: the most important information appears in the first 3 seconds of scanning. Use a TL;DR box, summary band, or executive summary at the top.
- [ ] **Progressive disclosure**: details are hidden behind collapsible elements, tabs, or scroll-triggered reveals. The reader sees the big picture first, then drills in.

## Visual gates

- [ ] **Palette respected**: uses the CSS variables from the default palette OR the project's AGENTS.md overrides. No hardcoded colors.
- [ ] **Typography hierarchy**: serif for headings (authority), sans for body (readability), mono for code. At least 3 levels of visual hierarchy (title → section heading → body).
- [ ] **Color has meaning**: red/warning colors signal problems, green/success colors signal good news, neutral colors are for structure. Never use color as the ONLY signal — pair with text or icons.
- [ ] **Whitespace is generous**: sections have breathing room. Dense walls of text are broken up. Cards have padding. Line-height is ≥ 1.5 for body text.

## Interaction gates (if interactive)

- [ ] **Export button exists**: every interactive editor/page has a way to export the final state as markdown, JSON, or plain text. Label: "Copy as markdown", "Copy as JSON", or "Export".
- [ ] **Keyboard accessible**: interactive elements work with Tab, Enter, Escape. Drag-drop has a keyboard fallback or is clearly labeled as mouse-only.
- [ ] **State is visible**: filters show what's active, drag targets highlight, copied buttons flash feedback.

## Final sanity check

- [ ] **Would I read this?** — If this document landed in your inbox Monday morning, would you actually read it or skim and archive? If the answer is "skim and archive", restructure until the answer changes.
- [ ] **Does it replace a wall of markdown?** — If the same information could have been a .md file with no loss of comprehension, you didn't use HTML's strengths. Add spatial layout, color coding, interaction, or progressive disclosure.
