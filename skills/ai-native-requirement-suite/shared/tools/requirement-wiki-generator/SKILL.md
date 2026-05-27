---
name: requirement-wiki-generator
description: Use when converting a V3 requirement asset package into a static HTML wiki, human-view, review cockpit, or requirements manual for PM, engineering, testing, or review consumption.
---

# requirement-wiki-generator

## Overview

`requirement-wiki-generator` consumes a V3 requirement asset package and generates a static HTML human-view. Markdown remains the source of truth; HTML is a read-only consumption view.

## When to Use

Use this skill when the user asks to:

- Generate an HTML wiki from a `requirement-asset/` directory.
- Build a review cockpit for Feature / Story readiness.
- Turn `human-view.md`, `quality-review.md`, Feature files and Story files into a human-readable static site.
- Check whether a requirement asset package is ready for wiki generation.

Do not use it when the user asks to:

- Generate or revise the requirement spec itself.
- Produce AI coding or AI testing input.
- Build a full documentation platform with login, search UI, publishing, or permissions.

## Input Contract

Required:

- `feature-map.md`
- `human-view.md`
- `prd.md`

Recommended:

- `quality-review.md`
- `features/*/feature-spec.md`
- `features/*/story-map.md`
- `features/*/stories/STORY-*.md`

If `feature-map.md` or `human-view.md` is missing, stop and report the missing file. If `quality-review.md` is missing, generate the wiki with an incomplete review cockpit warning.

## Workflow

1. Inspect the input directory.
2. Confirm it is a V3 requirement asset package.
3. Run:

```bash
python scripts/build_wiki.py --input <requirement-asset-dir> --output <output-dir> --title <wiki-title>
```

If the local `python` command is unavailable, use any Python 3 interpreter with the same arguments. The script uses only the Python standard library.

4. Verify the output contains:

```text
index.html
review-cockpit.html
prd.html
quality-review.html
features/FEATURE-*.html
assets/styles.css
search-index.json
```

5. Report warnings and incomplete sections.

## Quality Rules

- Do not modify the input Markdown asset package.
- Preserve stable IDs such as `FEATURE-*`, `STORY-*`, `RULE-*`, `GWT-*`, `QUESTION-*`.
- Default generated UI text is Chinese unless the input is clearly English-only.
- Keep GEARS/GWT/YAML details out of the default reading flow; summarize or link instead.
- Make `need_revision` / `blocked` visible in `review-cockpit.html`.
- Treat missing required files as failure, not silent success.

## References

- `references/wiki-output-contract.md`

## Script

- `scripts/build_wiki.py`
