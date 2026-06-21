# Pre-commit checklist

Run this before committing or declaring a task done. Every box must be true. If one cannot be,
say so explicitly rather than skipping it.

## Tests

- [ ] Every new behavior has a test, and the full suite passes.
- [ ] Any bug fix includes a test that fails without the fix.
- [ ] Tests assert observable behavior, not private internals.
- [ ] Tests are deterministic: no real clock, network, randomness, or order dependence.
- [ ] No logic (branches, loops) inside tests; wide input ranges use parametrize or Hypothesis.
- [ ] Error paths and edge cases are covered, not only the happy path.

## Types

- [ ] Every function signature and public attribute is annotated.
- [ ] `mypy --strict` (or Pyright strict) passes.
- [ ] No bare `# type: ignore`; any suppression has an error code and a reason.
- [ ] No stray `Any`; external input is validated at the boundary.

## Readability

- [ ] Names state intent; none needs a comment to explain what it refers to.
- [ ] Each function does one job; nesting is shallow; guard clauses replace deep conditionals.
- [ ] No commented-out code, no leftover debug prints or `breakpoint()`.
- [ ] Comments explain why, or clarify genuinely dense logic; none merely restates the code.

## Design

- [ ] No abstraction or design pattern added without a present duplication to justify it.
- [ ] Collaborators are injected, not constructed inside or pulled from globals.
- [ ] I/O is separated from decision logic where it reasonably can be.
- [ ] Exceptions are specific and raised at the point of contract violation; nothing is swallowed.
- [ ] Every caught error is logged with context and handled (recover, surface, or re-raise with
      `from`); no `except Exception: pass`, no unused caught variable.

## Configuration and safety

- [ ] No secrets, credentials, tokens, or environment-specific literals in the code.
- [ ] Values that vary by environment come from config, not hardcoded literals.
- [ ] No mutable default arguments, no import-time side effects, no hidden module state.

## Docs and hygiene

- [ ] Public modules, classes, and functions have PEP 257 docstrings with args, returns, raises.
- [ ] Public API changes are reflected in the README or changelog.
- [ ] `ruff check` and `ruff format` pass with no unjustified suppression.
- [ ] The change is the smallest one that satisfies the requirement; unrelated edits are removed.

## One-line gate

If you cannot run the suite, the type checker, and the linter and see them all green, the task is
not done. Report which gate is red and why.
