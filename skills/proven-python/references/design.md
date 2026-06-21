# Design

Design is the work of arranging code so the change you cannot yet see is cheap when it arrives. You
do not get there by adding structure up front. You get there by keeping the code simple, removing
duplication when it is real, and introducing an abstraction only when a concrete pressure demands
it.

## Design for change, not for everything

The future is uncertain, so do not pay today for flexibility you may never use. An abstraction added
on speculation is a guess that usually costs more to carry and to remove than it ever saves. This is
YAGNI: build what the current requirement needs, and trust that good, simple code is easy to extend
when the real need shows up.

The signal to abstract is duplication or rigidity you can point at right now, not one you imagine.
A useful rule: write it once, copy it a second time, and extract the shared abstraction on the third
occurrence, when you can finally see what actually varies.

## Separate decisions from I/O

The logic that decides (the rules, the calculations, the policy) should not be tangled with the code
that talks to the outside world (files, network, database, clock, console). Keep the core logic
pure: it takes values in and returns values out, with no hidden side effects. Push the I/O to the
edges and pass its results into the core.

This is the single highest-leverage design move available to you. Pure logic is trivial to test
(no mocks, no setup), easy to reason about, and reusable in a context the original I/O never
anticipated. Ports and adapters, hexagonal architecture, and functional core / imperative shell are
all names for this same separation.

## Inject collaborators, do not reach for them

A unit should receive what it depends on, as a parameter or a constructor argument, rather than
constructing it inside or pulling it from a global or a module-level singleton. Injected
dependencies make the unit's needs explicit in its signature, let a test pass a fake, and let you
swap an implementation without editing the unit. Depend on the narrow interface you use (a
`Protocol` of the methods you call), not on a concrete class, so callers stay decoupled.

## The SOLID ideas, briefly

These are concepts, useful as a vocabulary, not rules to apply mechanically:

- **Single responsibility.** A unit has one reason to change. Mixing unrelated reasons means an
  edit for one forces a risk on the other.
- **Open to extension, closed to modification.** Add behavior by adding code (a new implementation
  of an interface), not by editing a working unit and risking what already passes.
- **Substitutability.** A subtype must honor the contract of its base: a caller written against the
  base must not break when handed the subtype.
- **Small, focused interfaces.** A client should not be forced to depend on methods it never calls.
  Many narrow interfaces beat one wide one.
- **Depend on abstractions.** High-level policy should not import low-level detail directly; both
  should meet at an interface, so the detail can change without disturbing the policy.

## Composition over inheritance

Inheritance couples a subclass to the internals of its parent and locks behavior at definition time.
Prefer composing small objects and injecting collaborators: it is more flexible, easier to test, and
avoids deep fragile hierarchies. Use inheritance for a genuine, stable "is a" relationship, not to
share a few helper methods. A `Protocol` or a passed-in function is often the lighter answer.

## Errors are part of the design

- Raise a specific exception at the point a contract is violated, with a message that names what was
  expected and what was received. Do not return `None` or a sentinel to signal an error a caller
  must remember to check.
- Define your own exception types for your own failure modes, so callers can catch precisely.
- Never catch broadly to silence a traceback or make a test pass. A bare `except:` or `except
  Exception:` that swallows the error hides the bug and the next one after it. Catch the narrowest
  exception you can actually handle, and let the rest propagate.

## Prefer immutable, prefer explicit

Use `dataclass(frozen=True)`, tuples, and plain values for data that should not change after it is
built. Immutable data cannot be corrupted by a distant caller and is safe to share. Avoid hidden
state: no mutable default arguments, no import-time side effects, no module-level mutable globals
standing in for parameters.

## Enforce boundaries with a tool

Prose keeps module boundaries honest only as long as everyone remembers them. On a codebase with
real modules (a modular monolith, a multi-package app, a monorepo), make a boundary violation fail
the build the way ruff fails on style. [Tach](https://github.com/tach-org/tach) checks that imports
come only from declared dependencies, that cross-module calls go through a declared public interface,
and that the dependency graph stays free of cycles.
[import-linter](https://github.com/seddonym/import-linter) is the established, pure-Python
alternative.

This is optional, and it scales with the code: a single-module script has no boundaries to enforce,
so skip it there. Reach for it once an accidental import across a boundary would be a real problem.
Both tools are listed in `sources.md`.

## When you are done

No abstraction exists without a present duplication or rigidity to justify it. Decisions are
separated from I/O. Collaborators are injected. Exceptions are specific and raised at the point of
violation, and nothing is silently swallowed. The design is the simplest one that meets the
requirement.
