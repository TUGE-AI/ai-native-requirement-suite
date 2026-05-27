# GitHub Workflow

This repository uses GitHub as the public coordination layer.

## Public Repository

Use the public repository for:

- Public-safe bugs
- Public-safe feature requests
- Documentation improvements
- Release notes
- Contributor-facing workflow questions

## Internal Repository

Use the private repository for:

- Internal requirements
- Customer-specific examples
- Sensitive validation material
- Company-only roadmap items
- Private triage and review notes

## Standard Flow

```text
issue
  -> branch
  -> changes
  -> local verification
  -> commit
  -> push
  -> pull request
  -> review
  -> merge
```

## Linkage Rules

- Reference the issue number in the branch name or PR body.
- Use `Fixes #n` or `Closes #n` in the PR body when the PR should close the issue.
- Keep public issues and PRs free of internal paths, secrets, customer names, and private validation data.
