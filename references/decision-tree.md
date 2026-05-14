# Decision Tree — Which Pattern to Use

When the user asks for something, use this table to select the right pattern.
If multiple patterns could apply, pick the one that best matches the **primary intent**.

## Quick-lookup table

| User says (signal phrases)                                           | Pattern file              | What it produces                             |
|----------------------------------------------------------------------|---------------------------|----------------------------------------------|
| "compara", "tradeoffs", "qué approach", "ventajas y desventajas", "cuál es mejor" | `comparison.md`           | Side-by-side grid + tradeoff table + recommendation |
| "explica cómo funciona en el código", "recorrido", "cómo fluye X", "walkthrough"   | `walkthrough.md`          | Diagram + numbered steps + collapsible code  |
| "revisa este PR", "analiza este diff", "code review", "qué cambió"   | `review.md`               | Annotated diff + severity tags + margin notes  |
| "design system", "colores", "tipografía", "tokens", "swatches"       | `design-system.md`        | Color swatches + type scale + spacing table  |
| "prototipo", "animación", "transición", "efecto", "interacción"       | `prototyping.md`          | Animation sandbox with sliders / clickable flow |
| "diagrama", "flujo", "flowchart", "arquitectura", "dibuja"            | `diagram.md`              | SVG inline flowchart or architecture diagram  |
| "presentación", "slides", "deck", "exponer", "demo"                  | `deck.md`                 | Full-viewport slide deck with keyboard nav   |
| "explícame", "cómo funciona", "feature explainer", "concepto", "qué es X" | `explainer.md`            | Collapsible steps + tabs + FAQ + callouts    |
| "reporte", "status", "semanal", "post-mortem", "incidente", "on-call"  | `report.md`               | Summary band + chart + table + timeline + actions |
| "editor", "tablero", "triage", "kanban", "drag and drop", "ordenar"   | `editor.md`               | Interactive board + filters + export button  |

## Ambiguity resolution

When the user's request hits multiple categories, apply this priority:

1.  **Interaction over static** — if they want to *do* something (triage, reorder), choose `editor.md`.
2.  **Presentation over document** — if they'll *present* it (meeting, demo), choose `deck.md`.
3.  **Report over explainer** — if it has numbers, dates, or status, choose `report.md`.
4.  **Explainer over walkthrough** — if the goal is *understanding a concept*, choose `explainer.md`.
5.  **Walkthrough over comparison** — if the goal is *following a process*, choose `walkthrough.md`.
6.  **Comparison over review** — if the goal is *choosing between options*, choose `comparison.md`.

## Compound requests

If the user asks for two things in one prompt (e.g., "explícame la arquitectura y dame un reporte de status"), generate separate HTML files — one per pattern. Each file stays self-contained. Link them from each other if it helps the reader, but never sacrifice self-containment.

## Examples

| Prompt                                                                 | Pattern(s)              |
|------------------------------------------------------------------------|--------------------------|
| "Compara React Query vs SWR para mi codebase"                          | `comparison.md`          |
| "Hazme un post-mortem del incidente del martes"                        | `report.md`              |
| "Explícame cómo funciona el rate limiting en este repo"                | `explainer.md`           |
| "Muéstrame el flujo de autenticación paso a paso"                      | `walkthrough.md`         |
| "Crea un slide deck para la demo del viernes"                          | `deck.md`                |
| "Quiero un tablero drag-drop para hacer triage de estos 20 tickets"    | `editor.md`              |
| "Revisa este PR y dime qué hay que arreglar"                           | `review.md`              |
| "Dame tres approaches para implementar búsqueda con debounce"          | `comparison.md`          |
| "Haz un diagrama del pipeline de deploy"                               | `diagram.md`             |
| "Prototipo de la animación del modal de confirmación"                  | `prototyping.md`         |
| "Muéstrame los colores y la tipografía que usa este proyecto"          | `design-system.md`       |
