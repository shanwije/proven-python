# Security Policy

## Supported versions

This project ships a Claude Code skill plus a small validation script. Security
fixes are applied to the latest commit on the `main` branch. There are no
long-lived release branches to back port to.

## Reporting a vulnerability

Please do not open a public issue for a security problem.

Report it privately through GitHub's private vulnerability reporting:

1. Open the **Security** tab of this repository.
2. Click **Report a vulnerability**.
3. Describe the issue, the affected files, and the steps to reproduce it.

Expect an acknowledgement within a few days. Once the report is confirmed and a
fix is ready, the advisory is published and the reporter is credited unless they
ask to stay anonymous.

## Scope

The areas worth the most scrutiny are the GitHub Actions workflow under
`.github/workflows/` and the validation script under `scripts/`. The skill
content itself is plain Markdown and carries no executable code.
