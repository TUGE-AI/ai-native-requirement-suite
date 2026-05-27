---
name: requirement-asset-validator
description: Use when checking a V3 requirement asset package for structure, stable IDs, Story/Feature references, Gate readiness, open-question coverage, or downstream AI coding/testing/wiki consumability.
---

# Requirement Asset Validator

## Overview

This skill validates a V3 requirement asset package before downstream coding, testing, review, or wiki generation. It is a code-backed skill: use the deterministic validator script and interpret the generated report.

## When to Use

Use when the user asks to:

- validate a V3 requirement asset package
- check Feature / Story / Question ID consistency
- run preflight before `requirement-wiki-generator`
- verify whether AI coding/testing inputs are consumable
- identify missing files, broken Story references, or unclear Gate reasons

Do not use for:

- judging whether the business requirement is correct
- converting V2 requirements into V3 assets
- rendering HTML wiki output
- editing the source asset package

## Inputs

Required input is a directory containing:

- `feature-map.md`
- `prd.md`
- `quality-review.md`
- `human-view.md`
- `ai-coding-input.md`
- `ai-testing-input.md`
- `features/FEATURE-*/feature-spec.md`
- `features/FEATURE-*/story-map.md`
- `features/FEATURE-*/stories/STORY-*.md`

## Command

```bash
python scripts/validate_requirement_asset.py --input <requirement-asset-dir> --output <output-dir> --title <case-title>
```

Outputs:

```text
validation-report.md
validation-report.json
source-inventory.json
```

## Severity

| Severity | Meaning |
|---|---|
| `error` | Blocks downstream consumption, such as missing required files or broken Story references. |
| `warning` | Needs revision or human attention, such as inconsistent question coverage or missing readiness reason. |
| `info` | Useful context or improvement note. |

## Interpretation Rules

- Treat `error_count > 0` as not ready for downstream wiki/coding/testing consumption.
- Treat `warning_count > 0` as consumable only if the downstream task explicitly accepts known gaps.
- Do not treat generated reports as source of truth; source Markdown remains authoritative.
- Do not modify the input package while validating.
- Use Chinese by default for user-facing summaries in this project.
