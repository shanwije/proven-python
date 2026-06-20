# Human-readable output

Code, comments, and documentation should read as if a careful human wrote them: clear, natural, and
free of the tells that mark text as machine-generated. This is a quality and trust goal, not a trick
to fool a detector. Never degrade working code (scramble names, desync imports, manufacture
inconsistency) to look more human. The aim is output a thoughtful engineer would be glad to put
their name on.

## Code that reads as considered, not generated

- Comment for signal, not coverage. The clearest tell of generated code is a comment on every line
  restating what the line already says. Comment the non-obvious and delete the rest. See `style.md`.
- Keep messages terse and natural. An error or log line reads the way a person writes one: "Invalid
  email format", not "The provided email address is not in a valid format." Say what broke and what
  to do, without the formal padding.
- Resist needless ceremony. Generated code tends to over-scaffold: layers, options, and abstractions
  the task never asked for. Build what the requirement needs and nothing more. See `design.md`.
- Reach for the idiom a Python developer would use, not a verbose literal translation. See
  `style.md`.
- Consistency with the surrounding file beats a uniform generated style stamped on top of it.

## Prose that reads as written, not assembled

This covers docstrings, READMEs, commit messages, changelog entries, decision records, and comments.

- Write plain, direct sentences. Make the point and move on.
- Drop the AI vocabulary and filler. Words and tics that flag generated text include "delve",
  "tapestry", "testament", "landscape", "showcase", "crucial", "intricate", "seamless", and "robust"
  used as padding, plus openers like "In today's fast-paced world" and wrap-ups like "In
  conclusion".
- Cut the reflexes: sycophancy, hedging filler, the manufactured rule of three (three adjectives,
  three clauses), and "not just X, but Y" parallelisms.
- No em dashes or en dashes. Their overuse is one of the most common tells, which is why this
  project bans them outright and the build fails on one. Use commas, colons, parentheses, or
  separate sentences.
- Match the voice already in the file or project rather than switching to a generic register.

## Compose with focused companions

proven-python sets the standards and holds them. Two focused tools pair well with it, and neither
replaces the judgment here: they help you apply the standards, they do not decide them.

- For a clarity pass over code you just wrote or accepted, the official code-simplifier skill (run
  `/simplify`) is the better fit. It makes a behavior-preserving cleanup, flattening nesting,
  removing duplication, and sharpening names without changing what the code does, and it follows the
  project's own conventions. Reach for it when you want clarity work that touches only how the code
  reads, never what it does.
- For prose-heavy writing (a long README, an announcement, user-facing copy), the standalone
  humanizer skill rewrites text against a catalog of documented AI-writing patterns. It is narrow
  and optional: use it on the writing, not the code.

Both are listed in `sources.md`.

## When you are done

The output reads naturally and says what it means. No comment merely restates code, no message is
robotically formal, no prose leans on AI filler or banned dashes, and nothing was made worse just to
look human.
