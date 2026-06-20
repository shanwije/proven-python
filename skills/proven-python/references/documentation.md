# Documentation

Documentation records the contract and the reasoning that the code itself cannot show. The code says
how; the docstring says what and what for; the changelog and the decision record say why. Write the
minimum that a future reader (often you) needs, and keep it true, because documentation that has
drifted from the code is worse than none.

## Docstrings: the contract, not the mechanics

Every public module, class, and function gets a PEP 257 docstring. Document what the caller needs to
use it correctly, not a line-by-line account of the body.

- Start with a one-line summary in the imperative mood that fits on the first line: `"""Return the
  invoice total including tax."""`. Many tools and readers see only this line, so make it stand
  alone.
- If more is needed, leave a blank line after the summary, then expand: the arguments and their
  meaning, the return value, and the exceptions raised and when.
- Document behavior a caller cannot infer from the signature: units, valid ranges, side effects,
  what happens at the boundaries.
- Do not restate the type annotations in prose, and do not narrate the implementation. If the body
  changes but the contract holds, the docstring should not need to.

A consistent format helps. The Google docstring style (Args, Returns, Raises sections) reads well
and is widely tooled; pick one style and apply it everywhere. See the Google Python Style Guide in
`sources.md`.

```python
def withdraw(account: Account, amount: Decimal) -> Decimal:
    """Withdraw an amount and return the new balance.

    Args:
        account: The account to debit.
        amount: A positive amount to withdraw.

    Returns:
        The balance after the withdrawal.

    Raises:
        InsufficientFundsError: If amount exceeds the available balance.
    """
```

## Comments document reasons, docstrings document contracts

Keep the split clean. The docstring faces the caller and describes the interface. An inline comment
faces the maintainer and explains a non-obvious reason inside the body. Neither should narrate what
the code plainly says.

## README: how to start and how to use

A README orients a newcomer fast: what the project is and why it exists, how to install and run it,
the smallest example that does something real, and where to go next. Lead with the use, not the
internals. Keep it current as the public surface changes.

## Record decisions that were not obvious

When you make a choice with real trade-offs (a library, a boundary, a pattern, something you
deliberately did not do), write a short architecture decision record: the context, the decision, and
the consequences. It costs a few minutes and saves the next person from reopening a settled question
or unknowingly undoing a deliberate one.

## Changelog: what changed, for the people affected

Keep a human-readable changelog (see the Keep a Changelog format in `sources.md`). Group entries
under an `Unreleased` heading as you work, sorted into Added, Changed, Fixed, and Removed, and stamp
them with a version on release. Write entries for the reader who depends on the project, describing
the effect of the change, not the commit that made it. Pair this with semantic versioning so the
version number itself signals whether a change is breaking.

## Find the right shape

Different documentation answers different questions, and mixing them confuses the reader. A tutorial
teaches a beginner by doing; a how-to guide solves one specific problem for someone who already knows
the basics; reference describes the API precisely and exhaustively; an explanation gives background
and rationale. The Diátaxis framework (linked in `sources.md`) names these four and is worth keeping
in mind when a doc feels muddled: it usually means two of these are fighting in one page.

## When you are done

Every public module, class, and function has a docstring stating its arguments, return value, and
exceptions. The README reflects the current public surface. Decisions with real trade-offs are
recorded. The changelog has an entry for any change a user would notice.
