# Wiki Output Contract

## Purpose

The generated HTML wiki is a human consumption view for V3 requirement asset packages. It helps PM, engineering and testing users quickly answer:

- What is this requirement about?
- Which Feature / Story items exist?
- Which items are ready, need revision or blocked?
- What are the open questions?
- Where should AI coding/testing agents start?

## Output Files

```text
human-view/
  index.html
  review-cockpit.html
  prd.html
  quality-review.html
  features/
    FEATURE-001.html
  assets/
    styles.css
  search-index.json
```

## Page Responsibilities

| Page | Responsibility |
|---|---|
| `index.html` | Human-readable overview, source file index and main navigation |
| `review-cockpit.html` | Gate summary, Story readiness, warnings and open questions |
| `prd.html` | Rendered PRD source |
| `quality-review.html` | Rendered quality review or incomplete warning |
| `features/FEATURE-*.html` | Feature-level overview and Story summary |
| `search-index.json` | Machine-readable page index for future search UI |

## Required Behavior

- Preserve stable IDs.
- Use relative links only.
- Do not modify input Markdown.
- Generate warnings for missing recommended files.
- Fail clearly for missing required files.
- Prefer readable summaries over dumping full GEARS/GWT/YAML details.

## Non-goals

- No SPA.
- No login or publishing.
- No Mermaid rendering.
- No search UI in iteration-1.
