# Validation Rules

## Severity

- `error`: structure or reference failure that blocks downstream consumption.
- `warning`: inconsistency or missing explanation that requires revision but may not block preflight.
- `info`: context useful for consumers.

## Required Files

The validator checks these files at package root:

- `feature-map.md`
- `prd.md`
- `quality-review.md`
- `human-view.md`
- `ai-coding-input.md`
- `ai-testing-input.md`

Missing root required files are `error`.

## Feature / Story Consistency

- Every `features/FEATURE-*` directory should include `feature-spec.md`, `story-map.md`, and `stories/`.
- Story files referenced from `feature-map.md` must exist.
- Story IDs listed in `story-map.md` should match `stories/STORY-*.md`.
- Feature IDs in file names and front matter should not contradict the directory name.

## Question Consistency

- `QUESTION-*` IDs should be visible in `prd.md`, `feature-map.md`, `human-view.md`, and `quality-review.md`.
- `quality-review.md` should cover questions listed in PRD or feature-map.
- Story open questions may be a subset, but questions used by stories should be covered by package-level question lists.

## Readiness Reason

- `need_revision`, `blocked`, and `ready_for_coding_only` require a visible `reason:` or linked `QUESTION-*`.
- `ready_for_coding_only` is not full release readiness.

## Human / AI Consumer Entrypoints

`human-view.md` should reference:

- Feature entry
- Story entry
- `ai-coding-input.md`
- `ai-testing-input.md`
- `quality-review.md`

Missing consumer entrypoints are `warning`.

## Source Mutation

Validation must be read-only. The validator records SHA-256 hashes before and after validation; any difference is an `error`.
