# Pattern: Editor

An interactive tool page — drag to reorder, click to filter, toggle to configure — with a mandatory export button that turns the result back into portable text.

## When to use

- User asks for a "tablero", "triage", "kanban", "drag and drop"
- User wants to "ordenar tickets", "categorizar", "filtrar y organizar"
- User asks for a "prompt tuner", "feature flag editor", "configurator"
- User says "dame una UI para..." followed by an interactive task
- User needs to manipulate data visually and export the result

## The golden rule

**Every editor ends with an export button.** The user interacts in the UI, then copies the result back into markdown, JSON, or plain text. Without export, the interaction is a dead end.

## Sub-patterns

### A) Triage Board (kanban-style)

Drag cards across columns. Click a tag to filter. Export as markdown.

### B) Feature Flag Editor

Toggle rows grouped by area. Warnings when prerequisites are off. Export changed keys as diff.

### C) Prompt Tuner

Editable template with variable slots highlighted. Sample inputs re-render live as you type.

## Triage board — structure

```
┌──────────────────────────────────────────────────┐
│ Header: title, description, hints                  │
├──────────────────────────────────────────────────┤
│ Toolbar (sticky):                                   │
│   Summary · filter badge · [Reset] [Copy md]       │
├──────────────────────────────────────────────────┤
│ Board (4 columns grid):                            │
│ ┌─ Now ───┐ ┌─ Next ──┐ ┌─ Later ─┐ ┌─ Cut ──┐ │
│ │ ┌──────┐ │ │ ┌──────┐│ │         │ │         │ │
│ │ │ticket│ │ │ │ticket││ │         │ │         │ │
│ │ └──────┘ │ │ └──────┘│ │         │ │         │ │
│ │ ┌──────┐ │ │         │ │         │ │         │ │
│ │ │ticket│ │ │         │ │         │ │         │ │
│ │ └──────┘ │ │         │ │         │ │         │ │
│ │ 5 · 8pt  │ │ 7 · 11pt│ │ 8 · 14pt│ │ 4 · 10pt│ │
│ └──────────┘ └─────────┘ └─────────┘ └─────────┘ │
└──────────────────────────────────────────────────┘
```

## Triage board — key CSS

```css
.board {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  align-items: start;
}
.col {
  background: var(--bg-card);
  border: var(--border);
  border-radius: var(--radius-panel);
  overflow: hidden;
  display: flex; flex-direction: column;
  min-height: 200px;
}
.col[data-col="now"]   { border-top: 3px solid var(--clay); }
.col[data-col="next"]  { border-top: 3px solid var(--olive); }
.col[data-col="later"] { border-top: 3px solid var(--gray-500); }
.col[data-col="cut"]   { border-top: 3px solid var(--gray-200); }
.col.dragover { outline: 2px dashed var(--clay); outline-offset: -6px; background: var(--surface-warning-soft); }
```

## Ticket card CSS

```css
.ticket {
  background: var(--bg-card);
  border: 1.5px solid var(--gray-200);
  border-radius: 8px;
  padding: 10px 11px 9px;
  cursor: grab;
  user-select: none;
  transition: border-color 120ms, box-shadow 120ms, opacity 120ms;
}
.ticket:hover { border-color: var(--gray-500); box-shadow: var(--shadow-1); }
.ticket:active { cursor: grabbing; }
.ticket.dragging { opacity: .4; }
.ticket.dim { opacity: .25; }
```

## Drag-and-drop JS pattern

```js
let dragId = null;

// On each card:
card.addEventListener('dragstart', e => {
  dragId = ticket.id;
  card.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
});

card.addEventListener('dragend', () => {
  dragId = null;
  card.classList.remove('dragging');
});

// On each column:
col.addEventListener('dragover', e => {
  e.preventDefault();
  col.classList.add('dragover');
});
col.addEventListener('dragleave', e => {
  if (!col.contains(e.relatedTarget)) col.classList.remove('dragover');
});
col.addEventListener('drop', e => {
  e.preventDefault();
  col.classList.remove('dragover');
  if (!dragId) return;
  const t = tickets.find(x => x.id === dragId);
  if (t && t.col !== columnKey) { t.col = columnKey; render(); }
});
```

## Export to markdown

```js
function buildMarkdown() {
  const lines = [];
  lines.push('# [Title]');
  lines.push('');
  columns.forEach(col => {
    const rows = tickets.filter(t => t.col === col.key);
    lines.push('## ' + col.label + ' (' + rows.length + ')');
    lines.push('');
    rows.forEach(t => {
      lines.push('- **' + t.id + '** ' + t.title + ' — ' + t.tag);
    });
    lines.push('');
  });
  return lines.join('\n');
}

copyBtn.addEventListener('click', () => {
  const md = buildMarkdown();
  navigator.clipboard.writeText(md).then(() => {
    copyBtn.textContent = 'Copied ✓';
    setTimeout(() => { copyBtn.textContent = 'Copy as markdown'; }, 1200);
  });
});
```

## Feature flag editor pattern

For toggle-based config editors:

```html
<div class="flag-group">
  <h3>Authentication</h3>
  <div class="flag-row">
    <span class="flag-name">sso_login</span>
    <span class="flag-desc">Enable SSO for enterprise workspaces</span>
    <label class="toggle">
      <input type="checkbox" checked>
      <span class="slider"></span>
    </label>
  </div>
</div>
```

Include dependency warnings: if a flag is turned on but its prerequisite is off, show a warning callout.

## Prompt tuner pattern

Left side: editable textarea with `{{variables}}` highlighted. Right side: 3 sample inputs rendered with the current template.

```html
<textarea id="template">You are a {{role}}. Help me {{task}}.</textarea>
<div class="samples" id="samples">
  <!-- re-rendered on every keystroke -->
</div>
```

## Export formats by editor type

| Editor | Export format | Button label |
|--------|---------------|--------------|
| Triage board | Markdown list | "Copy as markdown" |
| Feature flags | Diff of changed keys | "Copy diff" |
| Prompt tuner | Final prompt text | "Copy prompt" |
| Any data editor | JSON | "Copy as JSON" |

## Mobile consideration

All editors degrade gracefully on mobile:
- Triage board: 4 columns → 2 columns → 1 column via media queries
- Drag-and-drop: provide a dropdown alternative for mobile
- Buttons: ensure touch target size ≥ 44px

## Full examples

- **Triage board**: See `resources/18-editor-triage-board.html` in the project — 24 tickets, 4 columns, drag-drop, tag filter, export to markdown
- **Feature flags**: See `resources/19-editor-feature-flags.html` in the project
- **Prompt tuner**: See `resources/20-editor-prompt-tuner.html` in the project
