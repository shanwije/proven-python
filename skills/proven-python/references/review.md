# Review

A review is a second engineer taking responsibility for the change with you. The goal is a healthy
codebase over time, not a perfect change today. Reviewing is a distinct skill from writing: you are
judging whether the code is correct, tested, readable, and safe to change, and saying so clearly
enough to act on. The same standards in this skill are the bar you review against.

## Review in priority order

Spend your attention where the risk is. Work down this order, and do not let a style nit distract
from a correctness hole.

1. **Correctness.** Does it do what it claims, including the edges and the error paths? Look for off
   by one errors, wrong boundaries, races, unhandled `None`, swallowed exceptions, and the input the
   author did not consider.
2. **Tests.** Is the new behavior actually covered, and would the tests fail if the behavior broke?
   A bug fix without a regression test is incomplete. Weak assertions that pass regardless prove
   nothing.
3. **Readability.** Will the next reader understand this without the author in the room? Names,
   function size, nesting, and clarity of intent.
4. **Design risk.** Does the change fit the system, or does it add an abstraction with no
   justification, couple things that should be separate, or paint a corner the next change will have
   to fight? Flag speculative complexity as readily as missing structure.

## State a finding so it can be acted on

A finding the author cannot act on is wasted. Give each one four parts:

- **Symptom:** what you observed, with the specific location.
- **Cause:** why it is a problem.
- **Consequence:** what it will cost if it ships (a crash, a security hole, a maintenance trap).
- **Fix:** the concrete change you are asking for, or a clear question if you are not sure.

"This is fragile" helps no one. "If `items` is empty this divides by zero (line 40); guard it and add
a test for the empty case" can be acted on in a minute.

## Separate what blocks merge from what does not

Be explicit about the weight of each comment, so the author knows what they must address and what is
optional. A correctness bug, a missing test for new behavior, or a security issue blocks merge. A
preference, a possible future cleanup, or a "consider this" is a suggestion; label it as one (a
"nit:" prefix works). Do not hold a change hostage over taste.

## Review the change, at a reviewable size

Review what the diff does, against what it set out to do, not the code you would have written. If two
solutions are equally good, the author's stands. A large diff hides bugs and exhausts the reviewer;
when a change is too big to review well, the right feedback is to split it.

## Automate the mechanical, review the judgment

Formatting, lint, type errors, and coverage are the build's job, not a human's. When the tools
already enforce a rule, do not spend review comments on it. That frees the review for the things only
a person can judge: is this correct, is it tested, is it clear, will it age well.

## Tone

Review the code, not the author. Critique is about the change; assume competence and good intent, ask
rather than accuse, and give credit where the work is good. The aim is a better change and a
colleague who still wants to send you the next one. See the Google code review guides in
`sources.md`.

## When you are done

You have read the whole diff, checked correctness and tests before style, stated each finding as
symptom, cause, consequence, and fix, and separated what blocks merge from what is a suggestion.
