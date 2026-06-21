# Code review checklist

Run this when reviewing a diff. Work top to bottom: the order is the priority order. Do not let a
style nit at the bottom block a change while a correctness hole at the top goes unchecked. State
each finding as symptom, cause, consequence, and fix, and mark whether it blocks merge.

## Correctness (blocks merge)

- [ ] The change does what it claims, and the claim matches the stated requirement.
- [ ] Edge cases are handled: empty, single, boundary, one past the boundary.
- [ ] Error paths are handled; no unhandled `None`, no off by one, no race.
- [ ] No exception is swallowed; every caught error is logged with context and recovered, surfaced,
      or re-raised (`raise ... from err` when translating). No `except Exception: pass`, no unused
      caught variable.
- [ ] No secret, credential, or environment-specific literal is introduced.

## Tests (blocks merge for new behavior)

- [ ] New behavior is covered by a test that would fail if the behavior broke.
- [ ] A bug fix includes a regression test that fails without the fix.
- [ ] Assertions check observable behavior, not internals, and are strong enough to catch a regression.
- [ ] Tests are deterministic: no real clock, network, randomness, or order dependence.

## Readability

- [ ] Names state intent; none needs a comment to explain what it refers to.
- [ ] Each function does one job; nesting is shallow; the main path is not buried.
- [ ] Comments explain why or clarify dense logic; no restated lines, commented-out code, or debug leftovers.
- [ ] The diff is a reviewable size; if not, the right ask is to split it.

## Design risk

- [ ] No abstraction or pattern is added without a present duplication or rigidity to justify it.
- [ ] Collaborators are injected, not constructed inside or pulled from globals.
- [ ] Decision logic is separated from I/O where it reasonably can be.
- [ ] The change fits the existing conventions; it does not paint the next change into a corner.

## Types and tooling

- [ ] Public signatures and attributes are annotated; strict type checking passes.
- [ ] Any suppression carries an error code and a reason.
- [ ] Lint and format are green; mechanical issues were left to the tools, not to review comments.

## Communication

- [ ] Each finding is symptom, cause, consequence, and fix, located precisely.
- [ ] Blocking issues are separated from suggestions; suggestions are labelled as such.
- [ ] The review judges the author's approach on its own terms, not against a rewrite.

## One-line gate

Approve only when correctness and tests are satisfied and every blocking finding is resolved. If the
build is not green, the change is not ready to review in depth; say so and stop.
