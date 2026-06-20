# Typing

Types are a checked contract and the cheapest documentation you can write. A strict type checker
reads them on every change and refuses the build when the contract breaks. Annotate enough that the
checker can do that work for you.

## The baseline

- Annotate every function signature: each parameter and the return type. A function that returns
  nothing returns `None`, and you say so.
- Annotate every public attribute, including class-level and dataclass fields.
- Run `mypy --strict` or Pyright in strict mode in the toolchain and in CI. Strict mode is the point:
  it rejects untyped functions and implicit `Any`, which is where bugs hide.
- Local variables usually do not need annotations; the checker infers them. Annotate a local only
  when inference is wrong or unclear, or to narrow a broad inferred type.

## No bare suppressions

`# type: ignore` with no error code hides every error on that line forever, including ones you
introduce later. When a suppression is genuinely required, pin the specific code and state the
reason:

```python
result = legacy_api()  # type: ignore[no-any-return]  # third-party stub returns Any, validated below
```

Treat every suppression as a small debt with a note attached. The same rule applies to `# noqa`:
name the rule and the reason.

## Keep `Any` out

`Any` switches the checker off for that value and everything it touches. It spreads silently. Where
data enters from outside (a request body, a JSON payload, an environment variable, a deserialized
blob), validate it at the boundary and convert it to a precise type immediately, so the untyped
value never reaches your logic. Pydantic, dataclasses with explicit parsing, or `TypedDict` with a
runtime check are all ways to do this. Inside the boundary, everything is typed.

When you truly do not know or care about a type, prefer `object` over `Any`: `object` forces you to
narrow before use, `Any` lets anything through unchecked.

## Tools of the type system

- **Precise built-ins.** `list[int]`, `dict[str, User]`, `tuple[int, str]`. Annotate containers with
  their contents.
- **`X | None`** for an optional value, and handle the `None` case. The checker narrows the type
  inside an `if value is not None:` guard, so write the guard and let it narrow.
- **`Protocol`** for structural typing: depend on the shape you use (the methods you call), not on a
  concrete class or a shared base. This keeps callers decoupled and tests easy to fake. See PEP 544
  in `sources.md`.
- **Generics and `TypeVar`** to keep a relationship between input and output types instead of
  collapsing it to `Any`.
- **`Final`, `Literal`, and enums** to make illegal states unrepresentable: a `Literal["read", "write"]`
  is checked, a bare `str` is not.
- **`cast`** is a blunt instrument that asserts a type the checker cannot prove. Use it rarely, and
  only when you can see by hand that it holds. Prefer narrowing with a guard or an `assert` that also
  runs at runtime.

## Typing existing untyped code

Add types at the edges first: public functions and the boundaries data crosses. Turn strictness up
module by module rather than disabling the checker globally. A single broadly-typed boundary that
validates input is worth more than scattered annotations on internal helpers.

## When you are done

Every signature and public attribute is annotated. `mypy --strict` (or Pyright strict) passes with
no error. Every suppression carries a code and a reason. No stray `Any` leaks from a boundary into
your logic.
