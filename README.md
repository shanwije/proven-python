# proven-python

[![validate](https://github.com/shanwije/proven-python/actions/workflows/validate.yml/badge.svg)](https://github.com/shanwije/proven-python/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) ![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-8A2BE2) [![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> The code looks done. It compiles, it reads well, it probably works.
> proven-python runs it red until a test proves it.

**proven-python** holds an AI coding agent to real engineering discipline on Python. "Looks done" is not
done: a change is done when a failing test drove it, every signature is typed, the linter is quiet,
and the whole bar is green. Until then the bar is red, and so is the task. It enforces test-driven
development, full type coverage, small readable functions, PEP 257 docstrings, configuration over
hardcoding, deliberate design, and a green toolchain before anything is called done.

It ships as a [Claude Code](https://claude.com/claude-code) skill, but the discipline is
agent-agnostic: the procedure is plain Markdown, so it works just as well dropped into Codex,
Cursor, or any agent that reads a skill or an instructions file.

Skills are model-invoked: the agent consults this one when it is about to touch Python, and
follows the procedure instead of producing plausible-looking code that nobody tested. The skill
body is short on purpose; the depth lives in `references/` and is loaded only when a task needs
it, and the gates live in `checklists/`.

## Why

Most code an AI agent writes looks right and is never proven right. This skill makes the agent
work the way a disciplined engineer does: write the failing test first, type everything, keep
units small and honest, document the contract, and refuse to declare a task finished while the
linter, the type checker, or the suite is red. It is grounded in the canonical Python and
software-engineering literature, distilled in the skill's own words, with every source and its
license listed in `skills/proven-python/references/sources.md`.

## What it enforces

- Test-first development and regression tests for bug fixes (`references/testing.md`)
- Strict typing with no unexplained ignores (`references/typing.md`)
- Readable names, small functions, idiomatic Python (`references/style.md`)
- Design for change, SOLID, composition, I/O separated from logic (`references/design.md`)
- PEP 257 docstrings, READMEs, ADRs, changelogs (`references/documentation.md`)
- Code review with prioritized, actionable findings (`references/review.md`)
- Output that reads as human-crafted, not machine-generated (`references/human-readable.md`)
- A definition-of-done gate and a review gate (`checklists/`)

## Install

### As a Claude Code plugin (recommended)

```
/plugin marketplace add shanwije/proven-python
/plugin install proven-python
```

### As a project skill, checked into your repo

Copy the skill folder into your project so every collaborator who clones it gets the skill:

```
mkdir -p .claude/skills
cp -r skills/proven-python .claude/skills/proven-python
```

### As a personal skill

```
mkdir -p ~/.claude/skills
cp -r skills/proven-python ~/.claude/skills/proven-python
```

### In Claude.ai or Cowork

Upload the `skills/proven-python` folder as a skill.

The skill is invoked by name (`proven-python`), set in the SKILL.md frontmatter, so the invocation
name is stable across updates.

## Pair it with tools, not just prose

A skill guides the agent; it does not replace deterministic enforcement. Wire the same standards
into your project so the build fails on a violation regardless of what any model does:

- `ruff check` and `ruff format` for lint and format
- `mypy --strict` or Pyright for types
- `pytest` with `pytest-cov` for tests, and `hypothesis` for property-based tests
- a pre-commit hook and a CI gate running all of the above

The skill points the agent at these. The tools are what actually hold the line.

Copy-pasteable templates for the config above (a strict `pyproject.toml`, a
`.pre-commit-config.yaml`, and a GitHub Actions `ci.yml`) ship in
`skills/proven-python/assets/`. Copy them into a new or existing project to wire the standards in
minutes instead of assembling the config from memory.

## Repository layout

```
proven-python/
├── .claude-plugin/
│   ├── plugin.json          plugin manifest
│   └── marketplace.json     so the repo can be added as a one-plugin marketplace
├── skills/
│   └── proven-python/
│       ├── SKILL.md         the procedure (short, always loaded when triggered)
│       ├── references/      depth, loaded on demand
│       │   ├── sources.md   every source with its license and reuse rule
│       │   ├── testing.md
│       │   ├── typing.md
│       │   ├── style.md
│       │   ├── design.md
│       │   ├── documentation.md
│       │   └── review.md
│       ├── checklists/
│       │   ├── pre-commit.md
│       │   └── code-review.md
│       └── assets/          copy-pasteable tooling templates
│           ├── pyproject.toml
│           ├── .pre-commit-config.yaml
│           └── ci.yml
├── LICENSE                  MIT (this project's own content)
├── NOTICE                   attribution for the CC BY sources drawn on
├── CONTRIBUTING.md
└── CHANGELOG.md
```

## Sources and licensing

This project's content is MIT licensed. The principles are distilled in the skill's own words
from public references. `skills/proven-python/references/sources.md` marks which sources are
permissively licensed (and quotable with attribution) and which are read-only (learn from, then
restate). The `NOTICE` file carries the required attributions for the CC BY 3.0 sources.

## Contributing

See `CONTRIBUTING.md`. The bar for a change is the same bar the skill sets: a clear reason, a
real improvement, and nothing that introduces copyrighted text from a read-only source.

## License

MIT. See `LICENSE`.
