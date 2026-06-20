# Contributing

Thanks for considering a contribution. The bar for a change here is the same bar the skill itself
sets: a clear reason, a real improvement, and nothing that introduces copyrighted text from a
read-only source.

## What belongs here

This repository is a Claude Code skill that encodes Python engineering discipline. Good changes
sharpen the guidance, fix an inaccuracy, improve how reliably the skill triggers, or add a template
that makes the standards easier to enforce. Before opening a change, be able to say in one sentence
what it improves and why.

## Ground rules

- **Keep `SKILL.md` lean.** It is the procedure only. Depth lives in `references/` and loads on
  demand. If the body grows past roughly 150 lines, move detail into a reference file and point to
  it.
- **No em dashes or en dashes anywhere.** Use commas, colons, parentheses, or separate sentences.
  The CI dash scan will fail the build otherwise.
- **Respect the licensing rules.** All content is written in the project's own words. Only sources
  marked bundle-able in `skills/proven-python/references/sources.md` may be quoted, and only with the
  attribution their license requires. If you add a source, add a row to `sources.md`, and if it is
  CC BY, add an entry to `NOTICE`.
- **Preserve the layout.** Manifests live only in `.claude-plugin/`. The skill lives under
  `skills/proven-python/`. Copy-pasteable tooling templates live in `skills/proven-python/assets/`.
- **Dogfood.** Any Python added to this repo follows the proven-python skill itself: write the test
  first, type everything, and leave the toolchain green.

## Before you open a pull request

- Run the repo's own validation locally and confirm it passes (see `.github/workflows/validate.yml`
  for what CI checks: manifest validity, link resolution, the dash scan, and the markdown linter).
- Update `CHANGELOG.md` under the `Unreleased` heading with a short, user-facing description of the
  change.
- Keep the change focused. Unrelated edits belong in a separate pull request.

## Reporting a problem

Open an issue describing what you expected, what happened, and how to reproduce it. For a wording or
accuracy concern, point at the specific file and line.
