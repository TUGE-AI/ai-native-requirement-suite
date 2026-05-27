# AI-native Requirement Suite

AI-native Requirement Suite is a portable skill suite for turning product ideas, requirement drafts, PRDs, and story-level specs into requirement assets that are easier for humans, AI coding agents, and AI testing agents to consume.

The suite focuses on three goals:

- Make requirements more complete, consistent, and reviewable.
- Preserve human-readable product intent while adding AI-friendly structure.
- Produce requirement assets with clear quality gates before downstream development and testing.

Current status: `v0.25-public-preview`.

This repository is prepared as a clean public release. It does not include private project workspaces, internal validation evidence, local machine paths, or company-specific requirement samples.

## What It Includes

- `requirement-router`: identifies the current requirement stage and recommends the next subskill.
- `idea-to-demand`: turns early ideas into a demand brief and clarification questions.
- `demand-to-prd-spec`: turns a confirmed demand brief into a human-readable PRD/spec.
- `ai-ready-spec`: converts PRD/spec material into a V3 requirement asset package.
- `requirement-quality-review`: reviews requirement assets for readiness, testability, and AI coding/testing consumption.
- Shared tools:
  - `requirement-asset-validator`
  - `requirement-wiki-generator`

## Typical Flow

```text
idea
  -> idea-to-demand
  -> demand brief
  -> demand-to-prd-spec
  -> PRD/spec
  -> ai-ready-spec
  -> V3 requirement asset package
  -> requirement-quality-review
  -> ready / need_revision / blocked
```

If you are not sure where to start, use `requirement-router`.

## Installation

The suite can be installed into a Codex skill directory with the included installer.

```powershell
$env:CODEX_HOME = '<your CODEX_HOME>'
$py = '<your Python executable>'
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --dry-run
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --install
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --verify
```

For upgrade:

```powershell
& $py tools\skill-installer\install_skill.py --manifest install-manifests\ai-native-requirement-suite.user.json --upgrade
```

## Tool Support

Validated:

- Codex skill installation flow.

Prepared but not formally validated in this public preview:

- Claude Code
- Cursor
- TRAE
- OpenClaw
- Hermes

The skill content is mostly Markdown plus Python standard-library scripts, so it is designed to be portable. Runtime adapters and tool-specific validation should be added before claiming support for additional tools.

## Third-Party Methodology References

The suite can reuse or emulate several external method styles when available:

- Superpowers `brainstorming`
- gstack `office-hours`, `plan-ceo-review`, `plan-eng-review`
- Matt Pocock agent skills `grill-me`, `grill-with-docs`

These are optional method references, not hard runtime dependencies. If a corresponding skill is unavailable, the suite should degrade to equivalent questioning or review patterns and should not claim that the external command was actually invoked.

## Documentation

- [OPEN-SOURCE-OPERATING-SCHEME.md](OPEN-SOURCE-OPERATING-SCHEME.md)
- [USER-GUIDE.md](USER-GUIDE.md)
- [ROADMAP.md](ROADMAP.md)
- [GITHUB-WORKFLOW.md](GITHUB-WORKFLOW.md)
- [skills/ai-native-requirement-suite/SKILL.md](skills/ai-native-requirement-suite/SKILL.md)

## License

MIT. See [LICENSE](LICENSE).
