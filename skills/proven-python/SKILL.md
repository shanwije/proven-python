---
name: proven-python
description: >-
  Python engineering-discipline guardrails for writing, refactoring, testing, and reviewing
  Python code. Enforces test-driven development, full type coverage, small readable functions, PEP 257
  docstrings, configuration over hardcoding, deliberate design, and a green toolchain (ruff,
  mypy, pytest) before any task is treated as finished. Use this whenever you are about to
  write, change, debug, test, package, or review Python code, set up a Python project, or
  decide whether Python code is done, even if the user never says the words "best practices",
  "clean code", "TDD", "type hints", or "design patterns".
---

# proven-python

Operating discipline for producing Python that another engineer can read, trust, and change six
months later. Apply it whenever you touch Python. The goal is correctness you can prove, code
that explains itself, and changes that do not surprise the next reader.

This file is the procedure. The `references/` files hold the depth: load one only when the task
needs it. The `checklists/` are the gates: run them before you claim a task is complete.

## When to apply

Writing new Python, changing or refactoring existing Python, debugging, writing or fixing tests,
setting up a project or its tooling, packaging, or reviewing a diff. If you are unsure whether
code is finished, that is exactly when to run the Definition of Done below.

## Apply with judgment

This skill sharpens the work; it does not stand in its way. Two things keep it from turning into
ceremony:

- Scale the rigor to the code. Production code, shared libraries, and anything others will build on
  earn the full discipline. A throwaway script, a spike, or a quick exploration earns its spirit,
  not the whole gate: say which one you are writing.
- Defer to context. Explicit user instructions and the established conventions of the codebase you
  are in win over any default here. Match the surrounding code rather than imposing another style
  on it.
- Stay alongside the agent. This skill rides with a coding agent like Claude Code and shares its
  habits: give the work a check the tools can run, separate exploring from building, and prefer the
  smallest change that does the job. If you could describe the diff in one sentence (a typo, a log
  line, a rename), make it directly and skip the ceremony.

When a rule would genuinely get in the way of what the user actually asked for, name the tradeoff
and adapt instead of applying it on autopilot. The anti-patterns at the end are the one exception:
those are worth avoiding whatever the code is for.

## The non-negotiables

1. Test first for anything with logic. Write a failing test, watch it fail for the right reason,
   write the minimum code to pass, then refactor with the suite green. A bug fix starts with a
   test that reproduces the bug. See `references/testing.md`.
2. Type everything. Annotate every function signature and public attribute. Code passes a strict
   type checker with no ignore you cannot justify in a comment. See `references/typing.md`.
3. Keep units small and honestly named. One job per function. A name that needs a comment to
   explain what it does is the wrong name. See `references/style.md`.
4. Document the contract, not the mechanics. A PEP 257 docstring on every public module, class,
   and function: what it does, its arguments, what it returns, what it raises. See
   `references/documentation.md`.
5. Configuration over hardcoding. No literal for anything that varies by environment, secret, or
   deployment. Inject dependencies rather than reaching for globals or import-time side effects.
6. Design for change before reaching for a pattern. Introduce an abstraction to remove a real,
   present duplication or rigidity, never on speculation. See `references/design.md`.
7. Leave the toolchain green. Lint, format, type check, and tests all pass locally before the
   task is done. See the toolchain below.

## Workflow

Follow this order. Do not jump ahead to implementation.

1. Restate the requirement in one sentence and name the smallest behavior to build first.
2. Write the test for that behavior. Run it. Confirm it fails for the intended reason.
3. Write the least code that makes it pass. Resist anything the test does not demand.
4. Refactor: remove duplication, sharpen names, extract units, while the suite stays green.
5. Repeat for the next behavior.
6. Before declaring done, run the full toolchain and the Definition of Done checklist.

In an existing codebase, match its established conventions first: consistency beats personal
preference. If the conventions are absent or actively harmful, raise it rather than silently
diverging.

## Toolchain

Default to the modern stack and state which you used:

- Environment and packaging: `uv` for fast, reproducible installs and locking. `pip` with
  `venv` is the fallback.
- Lint and format: `ruff check` and `ruff format`, which replace flake8, isort, and Black in a
  single fast tool. Black plus isort plus flake8 is the fallback.
- Types: `mypy --strict` or Pyright in strict mode. No bare `# type: ignore`: pin the error
  code and state the reason.
- Tests: `pytest` with `pytest-cov`. Add `hypothesis` for property-based tests when the input
  space is too wide for examples to cover.
- Project metadata and tool config live in `pyproject.toml` (PEP 621), as one source of truth.
- Architecture and boundaries: `tach check` (or `import-linter`) to enforce module dependencies and
  no import cycles. Optional, for projects with real module boundaries; skip it on a small script.

A command that fails the build on a violation is worth more than a paragraph asking the model to
behave. Prefer the tool over the instruction wherever a tool exists.

Ready-to-copy templates for all of this live in `assets/`: a strict `pyproject.toml` (ruff, mypy,
pytest with coverage), a `.pre-commit-config.yaml`, and a GitHub Actions `ci.yml`. When setting up
or hardening a project, copy them into place rather than writing the config from memory.

## Definition of Done

Do not call a task complete until every item holds. The full version is
`checklists/pre-commit.md`.

- Every new behavior is covered by a test, and the whole suite passes.
- A bug fix ships with a test that fails without the fix.
- The type checker passes with no unexplained ignores.
- Lint and format pass with no suppression you cannot justify.
- Public API has docstrings stating arguments, return value, and exceptions raised.
- No secrets, no environment-specific literals, no dead code, no leftover debug prints.
- Names read clearly, functions are small, nesting is shallow.
- The change is the smallest one that satisfies the requirement.

## Reviewing code

When judging a diff rather than writing one, use `checklists/code-review.md` and the standards in
`references/review.md`. Review for correctness, then tests, then readability, then design risk,
in that priority order. State each finding as symptom, cause, consequence, and the specific fix,
and separate what blocks merge from what is a suggestion.

## Anti-patterns to refuse

- Writing implementation before a test exists for it.
- Adding a layer, abstraction, or design pattern with no present duplication to justify it.
- Catching exceptions broadly to make a test pass or a traceback disappear.
- `# type: ignore` or `# noqa` with no error code and no reason.
- Functions that do several jobs, deep nesting, names that lie about behavior.
- Comments that restate the code instead of explaining a non-obvious reason.
- Mutable default arguments, import-time side effects, hidden global state.
- Output that reads as machine-generated: comments that over-explain, robotically formal messages,
  or AI filler vocabulary. See `references/human-readable.md`.

## Sources

The principles here are distilled, in this skill's own words, from the canonical Python and
software-engineering literature. `references/sources.md` lists every source with its license,
marks which are permissively licensed and quotable with attribution, and which are read-only and
must be restated rather than copied. Consult it before pasting any external text into a project.
