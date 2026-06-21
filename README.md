# proven-python

[![validate](https://github.com/shanwije/proven-python/actions/workflows/validate.yml/badge.svg)](https://github.com/shanwije/proven-python/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) ![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-8A2BE2) [![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> Your AI agent says "done" and hands you a pile of Python: untested, loosely typed, sloppy in the places nobody looked. You find out when you read it.
> proven-python holds the agent to the standards you would have checked in review, so the code arrives already at your bar instead of arriving as work you have to prove from scratch.

**proven-python** exists because an AI agent writes a lot of code fast and nothing holds it to your
team's quality bar. The agent declares "done" on code that no failing test drove, that types
loosely, that reads fine on the surface and breaks under the cases nobody wrote, and a human cleans
it up later. This skill points the agent at the standards your team already trusts, the Google
Python Style Guide, PEP 8, PEP 257, PEP 484, test-driven development, and full type coverage, and
tells it to meet them before reporting back: write the failing test first, type every signature,
keep functions small and readable, and document the contract. The skill guides; the deterministic
enforcement comes from the toolchain the skill runs, ruff, mypy, and pytest, which stay red until
the work actually clears the bar. So "looks done" never gets to pass for "proven done", and the
Python an agent hands you reads like the Python your team writes by hand.

It ships as a [Claude Code](https://claude.com/claude-code) skill, but the discipline is
agent-agnostic: the procedure is plain Markdown, so it works just as well dropped into Codex,
Cursor, or any agent that reads a skill or an instructions file.

Skills are model-invoked: the agent consults this one when it is about to touch Python, and
follows the procedure instead of producing plausible-looking code that nobody tested. The skill
body is short on purpose; the depth lives in `references/` and is loaded only when a task needs
it, and the gates live in `checklists/`.

## Quickstart

Install the plugin:
/plugin marketplace add shanwije/proven-python
/plugin install proven-python

Then ask your agent to write something in Python, for example:
Write a function that validates a US phone number and returns it in E.164 format.

Instead of handing back code straight away, the agent writes a failing test first, types the
function signature fully, implements it, then runs ruff, mypy, and pytest before reporting
done. You see the test, the type hints, and a green toolchain, not just a function that looks
right.

## Why

proven-python has the agent work the way a disciplined engineer does: write the failing test first,
type everything, keep units small and honestly named, document the contract, and refuse to call a
task finished while ruff, mypy, or pytest is red. None of the rules are invented here. They are the
established, industry-standard ones your team already follows, drawn from the canonical Python and
software-engineering literature: the Google Python Style Guide, Google's Code Review Developer
Guide, PEP 8, PEP 257, and PEP 484. Each is distilled in the skill's own words, with every source
and its license listed in `skills/proven-python/references/sources.md`. The payoff is code an agent
writes that clears the same bar as the code you write by hand, so your review confirms quality
instead of supplying it.

## What it enforces

- Test-first development and regression tests for bug fixes (`references/testing.md`)
- Strict typing with no unexplained ignores (`references/typing.md`)
- Readable names, small functions, idiomatic Python per the Google Python Style Guide and PEP 8 (`references/style.md`)
- Design for change, SOLID, composition, I/O separated from logic, module boundaries kept cycle-free with Tach (`references/design.md`)
- PEP 257 docstrings in Google docstring style, READMEs, ADRs, changelogs (`references/documentation.md`)
- Code review with prioritized, actionable findings, drawn from Google's Code Review Developer Guide (`references/review.md`)
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
- `tach check` (or `import-linter`) to keep module boundaries and the import graph cycle-free on a multi-module project
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
