# Testing

Test-driven development is the engine of this skill. You do not write code and then test it. You
write the test, watch it fail, then write the code that makes it pass. The test is the
specification of the behavior, captured before the behavior exists.

## The cycle

1. **Red.** Write one test for the smallest behavior you do not yet have. Run it. Confirm it fails,
   and that it fails for the reason you expect (the assertion, not an import error or a typo).
2. **Green.** Write the least code that makes the test pass. Nothing the test does not demand.
3. **Refactor.** With the suite green, remove duplication and sharpen names. Run the suite again.
4. Repeat for the next behavior.

A failing test that fails for the wrong reason is not a red test: it is a broken test. Read the
failure before you write any implementation.

## What to test

Test observable behavior through the public interface: inputs, outputs, side effects, raised
exceptions. Do not test private helpers directly or assert on internal state. If a private detail
is worth testing in isolation, that is a signal it should be its own unit with its own public
contract.

Cover the paths that matter:

- The happy path, stated as the simplest meaningful example.
- Boundaries: empty, single element, the limit, one past the limit.
- Error paths: the inputs that must raise, and that the right exception type is raised.
- Any branch in the code. Untested branches are unproven branches.

## Bug fixes start with a failing test

A bug means a behavior is unspecified or wrong. Before you fix it, write a test that reproduces it
and fails. Then fix the code until that test passes. The test now guards against the bug returning,
and it proves your fix addresses the real cause rather than a symptom.

## Structure and naming

Give each test one clear arrange, act, assert shape. Keep arrangement minimal. Assert one behavior
per test so a failure names the broken behavior precisely.

Name the test for the behavior it pins down, not the function it calls. `test_withdraw_more_than_balance_raises`
tells the next reader what broke. `test_withdraw_2` tells them nothing.

Put no logic in a test. A branch or loop inside a test is a second, untested program. When you need
to cover a range of inputs, use parametrization, not a loop.

## Tools

- **pytest** is the default. Plain functions, plain `assert`, fixtures for setup, `parametrize` for
  input tables. See the pytest docs in `sources.md`.
- **Fixtures** provide shared setup and teardown. Keep them small and composable. Scope them no
  wider than the tests that need them.
- **`pytest.mark.parametrize`** replaces copy-pasted near-identical tests and in-test loops with one
  test run across a table of cases. Each case reports as its own pass or fail.
- **Hypothesis** generates inputs to find the cases you did not think of. Reach for property-based
  testing when the input space is too wide to enumerate: assert an invariant that must hold for all
  valid inputs (a round trip, an ordering, a conservation) and let it search for a counterexample.
- **pytest-cov** measures which lines and branches ran. Use coverage to find untested code, not as a
  target to game. High coverage of weak assertions proves nothing.

A property-based test in practice: state an invariant and let Hypothesis search for a counterexample,
instead of hand-picking a few inputs.

```python
from hypothesis import given, strategies as st


@given(st.lists(st.integers()))
def test_sort_is_idempotent(items: list[int]) -> None:
    """Sorting an already sorted list changes nothing."""
    once = sorted(items)
    assert sorted(once) == once
```

## Tests must be deterministic

A test that passes or fails depending on the day, the machine, or the run order is worse than no
test, because it trains the team to ignore red.

- No real clock. Inject the time or freeze it. Do not assert on `datetime.now()`.
- No real network or filesystem in a unit test. Use a fake, a stub, or a temporary directory
  fixture. Integration tests that touch real systems are separate and marked as such.
- No randomness without a fixed seed.
- No dependence on test execution order or on shared mutable state between tests.

## Test doubles, used sparingly

Replace a real collaborator with a double only to cut a slow, non-deterministic, or unavailable
dependency, or to assert that an interaction happened. Prefer the lightest double that works: a
stub that returns a value over a mock that asserts calls. Mocking everything couples the test to the
implementation and lets it pass while the code is broken. If a unit needs a wall of mocks to test,
the design is telling you it has too many dependencies.

## When you are done

Every new behavior has a test. The bug fix has its regression test. The full suite passes, fast and
deterministic. If you cannot run the suite and watch it pass, the task is not done; say which gate
is red and why.
