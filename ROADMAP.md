# Roadmap

status: `v0.25-public-preview`

This roadmap describes public project direction. It intentionally excludes private validation workspaces, internal sample names, local paths, and company-specific evidence.

## Current Preview

The current public preview includes the first complete suite shape:

- A suite-level entry skill.
- Five user-facing subskills:
  - `requirement-router`
  - `idea-to-demand`
  - `demand-to-prd-spec`
  - `ai-ready-spec`
  - `requirement-quality-review`
- Shared schema, template, validator, and wiki generation assets.
- Optional methodology orchestration for brainstorming, review, challenge, and planning styles.
- A Codex installer manifest and a portable Python installer.

## Near-Term Goals

### V0.26 Public Preview Hardening

- Improve public examples so they are domain-neutral and safe to reuse.
- Add a minimal public regression fixture that does not depend on private project history.
- Tighten installation and verification instructions.
- Add a public release checklist for sensitive information scanning.

### V0.27 Cross-Tool Adapter Validation

- Prepare and validate adapter instructions for additional coding-agent environments.
- Keep tool support labels conservative:
  - `validated`
  - `prepared_not_validated`
  - `not_validated`
- Do not claim support for a runtime until it has been installed and smoke-tested there.

### V0.28 Requirement Asset Examples

- Add a full fictional example that covers:
  - demand brief
  - PRD/spec
  - feature map
  - story map
  - story-level GEARS/GWT examples
  - quality review
  - validator report

### V0.29 Documentation and Publishing

- Add English documentation for core usage.
- Add generated HTML documentation examples.
- Clarify contribution rules for new subskills, templates, and validators.

### V0.30 Release Candidate

- Freeze the public asset package contract.
- Add public smoke tests.
- Publish a signed release archive.
- Document compatibility expectations for supported agent runtimes.

## Scope Boundaries

The suite should not:

- Generate implementation design, database design, or API design in early requirement stages.
- Treat validator output as a substitute for product, engineering, or testing review.
- Hide `need_revision` or `blocked` results to make requirements appear ready.
- Require optional third-party skills as hard dependencies.
- Claim runtime compatibility that has not been verified.

## Contribution Direction

Useful contributions include:

- Better public examples.
- More precise quality gates.
- Safer templates for DFX and non-functional requirements.
- Additional runtime adapters with evidence.
- Better HTML/wiki human-view generation.
