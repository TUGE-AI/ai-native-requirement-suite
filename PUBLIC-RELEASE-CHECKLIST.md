# Public Release Checklist

Use this checklist before publishing a new public release.

## Repository Contents

- Do not include private `workspaces/` evidence.
- Do not include handoff notes, internal review transcripts, or local validation logs.
- Do not include generated release archives unless they were built from the public tree.
- Do not include company-specific requirement samples.

## Sensitive Information Scan

Search for:

- Company names and internal project names.
- Personal names, local usernames, emails, and phone numbers.
- Local paths such as user home directories, mapped drives, or network-share paths.
- Internal hostnames, IP addresses, and network shares.
- API keys, tokens, secrets, and passwords.
- Customer names, supplier names, contract names, and system IDs.

Recommended command shape:

```powershell
rg -n --hidden --glob '!**/.git/**' "<company-or-personal-keywords>|<local-path-patterns>|<credential-patterns>" .
```

## Compatibility Claims

- Claim only validated runtimes.
- Mark prepared but untested runtimes as `prepared_not_validated`.
- Keep optional third-party skills optional.
- If a fallback style is used, do not claim that the external command was invoked.

## Packaging

- Build release archives from this public tree only.
- Extract the archive into a temporary directory.
- Run installer `--dry-run`, `--install`, and `--verify`.
- Re-run the sensitive information scan on the extracted archive.
