# Style

Code is read far more often than it is written, usually by someone who is not you and does not have
your context. Style is not decoration; it is how you lower the cost of that reading. The formatter
settles the mechanical questions so you can spend your attention on the ones that matter: names,
size, and shape.

## Let the tool own formatting

Whitespace, quotes, import order, and line length are not worth a human decision or a review
comment. `ruff format` (and `ruff check` for lint) settles them the same way every time. Adopt PEP 8
through the tool, not by hand. A diff should show changed behavior, not reshuffled blank lines.

## Names carry the intent

A name is the comment you do not have to write. Spend the effort here.

- Name for what the thing means, not its type or its mechanics: `unpaid_invoices`, not `list2`.
- A name that needs a comment to explain what it refers to is the wrong name. Rename until the
  comment is redundant, then delete the comment.
- Functions are verbs (`charge_card`, `parse_header`); values and collections are nouns. A boolean
  reads as a yes or no question: `is_active`, `has_access`.
- Match the established vocabulary of the codebase and the domain. Do not invent a second word for an
  idea that already has one.
- Length tracks scope: a loop index can be `i`, a module-level constant earns a full descriptive
  name. Avoid abbreviations a newcomer would have to decode.

## One function, one job

A function should do one thing at one level of abstraction. When you cannot name it without "and",
it is doing too much; split it. Small functions are easier to name, test, and reuse, and a good
name turns the call site into prose.

Keep nesting shallow. Replace a deep `if` pyramid with guard clauses that handle the edge cases and
return early, so the main path stays flat and unindented:

```python
def price(order: Order) -> Decimal:
    if not order.items:
        raise EmptyOrderError(order.id)
    if order.is_cancelled:
        return Decimal(0)
    return sum((line.total for line in order.items), Decimal(0))
```

## Write idiomatic Python

Idiomatic code is shorter, clearer, and less buggy than a transliteration from another language.

- Iterate over things, not indices: `for user in users`, and `enumerate` when you need the index,
  `zip` to walk two sequences together.
- Use comprehensions for a simple map or filter; fall back to a loop when the logic is non-trivial,
  because a comprehension you have to puzzle over has lost its purpose.
- Manage resources with `with`: files, locks, connections close themselves even on an exception.
- Prefer asking forgiveness (try the operation, catch the specific failure) over checking first when
  the check would race or duplicate the work.
- Reach for the standard library before writing your own: `pathlib` for paths, `dataclasses` for
  plain data, `collections` and `itertools` for the common shapes.

## Comments explain why, not what

The code already says what it does. A comment earns its place by explaining the reason the reader
cannot see: a non-obvious constraint, a workaround for a known bug, a deliberate choice that looks
wrong but is not. A comment that restates the next line is noise that goes stale; delete it and let
the code and its names speak.

The real line is not why versus what, it is signal versus noise. A short note on top of genuinely
dense logic, a subtle algorithm, or an opaque regular expression is worth keeping, because it tells
the reader something the code does not make obvious. Restating an obvious line is the noise to cut.
When in doubt, match the comment density of the surrounding file rather than adding or stripping
comments to suit your own taste.

## Leave nothing dead behind

No commented-out code, no `print` debugging, no stray `breakpoint()`, no unused import or variable.
Version control remembers the old code; the file should show only what runs now. `ruff check` flags
most of this, so let it.

## When you are done

`ruff format` and `ruff check` pass with no unjustified suppression. Names read clearly without
their comments. Functions are small and single-purpose, nesting is shallow, and nothing dead is left
in the file.
