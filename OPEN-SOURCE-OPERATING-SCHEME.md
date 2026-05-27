# AI-native Requirement Suite Open Source Operating Scheme

This document consolidates the product idea, Q&A, implementation scheme, and current operating model for turning `ai-native-requirement-suite` into a GitHub open source project under `TUGE-AI`.

It is written for two audiences:

- Public contributors and maintainers of `TUGE-AI/ai-native-requirement-suite`
- Internal maintainers who also manage `TUGE-AI/ai-native-requirement-suite-internal`

## 1. What This Project Is

`AI-native Requirement Suite` is a requirement skillsuite that helps transform product ideas, requirement briefs, PRDs, stories, and structured requirement assets into materials that are easier for humans, AI coding agents, and AI testing agents to consume.

The core product goal is to make requirement work:

- more complete
- more consistent
- more reviewable
- more AI-consumable

The suite is intentionally split into:

- a public repository for reusable, public-safe capabilities and documentation
- a private repository for internal requirements, sensitive samples, company-only triage, and private validation
- local workspaces for temporary analysis only

## 2. The Questions We Clarified

### 2.1 Is V3 about the full product, or only a MVP?

Answer: the PRD froze the full V3 scope, while the first delivery is V3.0 and later items are V3.1/V4 candidates. The implementation work should not keep reopening the PRD unless a blocker changes the release boundary.

### 2.2 Should requirements be human-readable and AI-readable at the same time?

Answer: yes. Markdown remains the source asset, while HTML wiki / human-view is the consumer view. Machine-friendly content stays available, but the default human view should emphasize narrative, flows, decision summaries, and gate results.

### 2.3 Should GEARS/GWT be mandatory everywhere?

Answer: GEARS/GWT help AI readability and testability, but they must not make the spec unreadable to humans. The rule is to keep the human view primary and expose machine-friendly structures in a controlled way.

### 2.4 Should internal and external work be separated?

Answer: yes. Public GitHub should only carry public-safe work. Private GitHub should carry internal requirements, sensitive validation, and company-specific feedback. Local workspace is not the source of truth for long-term collaboration.

### 2.5 Should Codex, GitHub CLI, and GitHub connector all be involved?

Answer: yes, but with different roles.

- GitHub CLI and git: operational path for repo creation, branch, commit, push, and PR
- Codex GitHub connector: issue/PR read-write integration when the app is installed on the target org
- Local workspace: code and doc editing

## 3. Current Verified Setup

The following has been verified in the current environment:

| Item | Status | Notes |
|---|---|---|
| Git installed | verified | `git` available locally |
| GitHub CLI installed | verified | `gh` available locally |
| GitHub CLI authenticated | verified | logged in as `winshipping` |
| `TUGE-AI` organization visible | verified | `gh api user/orgs` includes `TUGE-AI` |
| Codex connector installed at user level | verified | installed for `winshipping` |
| Codex connector installed at organization level | verified | installed for `TUGE-AI` |
| Public repo created | verified | `TUGE-AI/ai-native-requirement-suite` |
| Private repo created | verified | `TUGE-AI/ai-native-requirement-suite-internal` |
| Public repo pushed from local workspace | verified | `origin/main` created and updated |
| Issue creation/read via connector | verified | issue `#1` created and fetched |
| PR creation/merge/issue auto-close | verified | PR `#2` merged, issue `#1` closed |

## 4. What Still Needs Verification

The following are not yet treated as fully validated release capabilities:

- full public issue triage workflow at scale
- internal repo collaboration with multiple team members
- branch protection rules
- review assignment and reviewer routing
- labels, milestones, and project board conventions beyond the baseline set
- release tagging and changelog automation
- GitHub Actions usage for tests, packaging, and release publication
- external contributor onboarding
- more than one issue type and more than one PR pattern

## 5. Repository Split

### 5.1 Public Repository

`TUGE-AI/ai-native-requirement-suite`

Use this repository for:

- public-safe bug reports
- public-safe feature requests
- public documentation
- public release notes
- public examples and public fixtures
- GitHub issue and PR workflow documentation

Do not put the following here:

- company names
- customer names
- private paths
- private validation evidence
- internal business system names
- secrets, tokens, or credentials

### 5.2 Private Repository

`TUGE-AI/ai-native-requirement-suite-internal`

Use this repository for:

- internal requirements
- internal bugs
- private validation samples
- company-specific roadmap items
- internal review notes
- sensitive source material that cannot be published

### 5.3 Local Workspace

Use the local workspace only for:

- analysis
- editing
- temporary verification
- experiments

Do not treat the local workspace as the long-term source of truth for requirements or bugs.

## 6. Recommended Operating Model

### Public Flow

```text
public issue
  -> branch
  -> change
  -> local verification
  -> commit
  -> push
  -> pull request
  -> review
  -> merge
  -> release note
```

### Private Flow

```text
internal issue
  -> branch
  -> change
  -> local verification
  -> commit
  -> push
  -> pull request
  -> review
  -> merge
  -> internal release note or sync note
```

### Bridge Rule

If an internal issue can be generalized without leaking sensitive detail, create a public-safe derivative issue in the public repo. Otherwise keep it private.

## 7. Verified GitHub Usage Pattern

The verified pattern in this environment is:

1. Use GitHub CLI and git for repo creation, branch management, commit, push, and PR.
2. Use Codex connector for issue and PR read/write when the app is installed on the target org.
3. Use the public repo for public-safe issues and PRs.
4. Use the private repo for internal issues and PRs.

This pattern is already proven by:

- creating a public repo under `TUGE-AI`
- pushing the public local workspace to GitHub
- creating and reading a public issue through the Codex connector
- creating and merging a PR that closed that issue automatically

## 8. Future Validation Plan

The next validation targets should be:

- multiple public issues of different types
- internal private issue to PR flow
- branch protection and reviewer rules
- release tagging and release notes
- GitHub Actions for package verification
- public-safe issue template and private-safe triage rules

## 9. Internal Collaboration Doc

The private repository should carry its own internal collaboration notes. The recommended internal document should cover:

- who can open internal issues
- how to classify internal bug vs requirement vs release task
- how to redact material before bridging to public
- how to relate internal work to public issues or releases
- how to keep local workspace usage temporary

The private repo should remain more operational and less externally explanatory than the public repo.

## 10. Current Decision Record

- Public GitHub is the outward-facing collaboration surface.
- Private GitHub is the internal collaboration surface.
- Local workspace is only temporary working storage.
- Markdown is the source asset format.
- HTML/wiki is the human consumer view.
- GEARS/GWT and validator outputs support quality and AI consumption, but do not replace human-readable requirement structure.
- Codex, GitHub CLI, and GitHub connector are all part of the operating model, but they have different responsibilities.

