# Sources

Every principle in this skill is distilled in the skill's own words from the references below.
This file exists so that anyone reusing or extending the skill can do so without an IP problem.

There are two buckets. Read the rule for each before pasting any external text into a project.

## How to use this list

- **Bundle-able**: permissively licensed. You may quote or adapt the text inside a project or a
  derived skill, provided you keep the required attribution. These are the only sources whose
  wording you may carry across verbatim.
- **Read-only**: free to read and link, but the text is copyrighted and may not be redistributed.
  Learn from it, then restate the idea in your own words and cite the source. Never paste it.

When in doubt, restate and link. A principle (for example "depend on abstractions, not
concretions") is not copyrightable; a specific author's phrasing of it is.

---

## Bundle-able (permissive, attribution required)

| Source | Covers | License | Link |
| --- | --- | --- | --- |
| PEP 8 | Style guide for Python code | Public domain (see PEP Copyright) | peps.python.org/pep-0008 |
| PEP 20 | The Zen of Python | Public domain | peps.python.org/pep-0020 |
| PEP 257 | Docstring conventions | Public domain | peps.python.org/pep-0257 |
| PEP 484 / 526 / 544 | Type hints, variable annotations, Protocols | Public domain | peps.python.org |
| PEP 621 | Project metadata in pyproject.toml | Public domain | peps.python.org/pep-0621 |
| Python official docs | Language and standard library reference | PSF License (retain notice) | docs.python.org |
| Google Python Style Guide | Idiomatic Python style and docstring format | CC BY 3.0 | google.github.io/styleguide/pyguide.html |
| Google Engineering Practices (Code Review Developer Guide) | What to look for in review, author and reviewer guides | CC BY 3.0 | google.github.io/eng-practices |
| pytest docs | Test framework usage, fixtures, parametrization | MIT | docs.pytest.org |
| FastAPI docs | API design, dependency injection, typed request handling | MIT | fastapi.tiangolo.com |
| Hypothesis docs | Property-based testing | MPL 2.0 (docs), retain notice | hypothesis.readthedocs.io |
| Ruff docs | Linting and formatting rules and rationale | MIT | docs.astral.sh/ruff |
| Twelve-Factor App | Config, dependencies, dev/prod parity | Free to read and link | 12factor.net |
| Semantic Versioning | Version numbering contract | CC BY 3.0 | semver.org |
| Conventional Commits | Structured commit messages | CC BY 3.0 | conventionalcommits.org |
| Keep a Changelog | Changelog format | MIT | keepachangelog.com |
| Diátaxis | Documentation structure framework | CC BY-SA 4.0 (share-alike) | diataxis.fr |
| Claude Code best practices (Anthropic) | How an agentic coding assistant works, so this skill complements it | Free to read and link | code.claude.com/docs/en/best-practices |
| Wikipedia: Signs of AI writing | Catalog of AI-writing tells in prose | CC BY-SA 4.0 (share-alike) | en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing |

Notes:

- Most PEPs declare "This document has been placed in the public domain" in their Copyright
  section. Confirm in the specific PEP before relying on it.
- CC BY 3.0 requires visible attribution to the author when you reuse the text. The NOTICE file
  in this repo carries the attributions for the CC BY sources this skill draws on.
- Diátaxis is CC BY-SA: if you redistribute its text, your derivative must use the same license.
  Safer to restate and link.

## Read-only (free to read, do not redistribute, restate in your own words)

| Source | Covers | Link |
| --- | --- | --- |
| Refactoring catalog (Martin Fowler) | Named refactorings and when to apply them | refactoring.com |
| python-patterns.guide (Brandon Rhodes) | Gang of Four patterns reconsidered for Python | python-patterns.guide |
| Refactoring.Guru | Design patterns and refactorings with Python examples | refactoring.guru |
| Architecture Patterns with Python (Percival, Gregory) | DDD, ports and adapters, TDD in Python. Free to read online; license restricts redistribution | cosmicpython.com |
| The Hitchhiker's Guide to Python | Project layout and tooling conventions | docs.python-guide.org |
| Real Python | Tutorials across the ecosystem | realpython.com |

## Open-source code (verify the repo license before reusing code)

| Source | Covers | Link |
| --- | --- | --- |
| faif/python-patterns | Worked implementations of design patterns in Python | github.com/faif/python-patterns |

## Companion skills (recommended tools, not bundled here)

These are separate skills this one points to, not sources it quotes. Install and load them
alongside proven-python when their narrower job fits the task. See `human-readable.md`.

| Skill | Covers | License | Link |
| --- | --- | --- | --- |
| code-simplifier (Anthropic) | Behavior-preserving clarity pass over code, run as `/simplify` | See repo | github.com/anthropics/claude-plugins-official |
| humanizer | Rewriting prose to remove AI-writing tells | MIT | github.com/blader/humanizer |

## Books (read and distill; text is copyrighted, do not embed)

- Test-Driven Development by Example, Kent Beck
- Refactoring, second edition, Martin Fowler
- Clean Code, Robert C. Martin
- Working Effectively with Legacy Code, Michael Feathers
- The Pragmatic Programmer, Andrew Hunt and David Thomas
- Code Complete, second edition, Steve McConnell
- Domain-Driven Design, Eric Evans
- Fluent Python, second edition, Luciano Ramalho
- Effective Python, second edition, Brett Slatkin
- Robust Python, Patrick Viafore
- Python Testing with pytest, second edition, Brian Okken

The SOLID principles, YAGNI, composition over inheritance, and the rest of the named principles
are concepts, not text. Describe them freely. Only an author's specific wording is protected.
