# Changelog

All notable changes to this project are documented here. The format follows Keep a Changelog, and
the project aims to follow Semantic Versioning.

## [Unreleased]

### Added

- Initial proven-python skill: `SKILL.md` procedure with non-negotiables, an apply-with-judgment
  section that scales the rigor to the task and keeps the skill from obstructing a host agent like
  Claude Code, a workflow, toolchain, Definition of Done, and anti-patterns.
- Reference files loaded on demand: `testing.md`, `typing.md`, `style.md`, `design.md`,
  `documentation.md`, `review.md`, `human-readable.md`, and `sources.md` with every source and its
  license.
- Guidance on human-readable, AI-tell-free output, pointing to the official code-simplifier skill
  for code clarity and the humanizer skill for prose (`references/human-readable.md`).
- Gate checklists: `checklists/pre-commit.md` and `checklists/code-review.md`.
- Copy-pasteable tooling templates under `skills/proven-python/assets/`: `pyproject.toml`
  (ruff, mypy strict, pytest with coverage), `.pre-commit-config.yaml`, and a GitHub Actions
  `ci.yml` running the full toolchain across a Python version matrix.
- Plugin packaging: `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` so the repo
  can be added as a one-plugin marketplace.
- Repository CI in `.github/workflows/validate.yml` that validates the manifests, checks internal
  links resolve, fails on em dashes or en dashes, and lints the markdown.
- A typed, tested validation script under `scripts/` supporting the repository CI.
- Project docs: `README.md`, `LICENSE` (MIT), `NOTICE` (CC BY attributions), and `CONTRIBUTING.md`.

[Unreleased]: https://github.com/shanwije/proven-python
