---
name: docstring-api
description: How to write the Google-style docstrings this project expects for named public Python functions — required sections, summary-line wording, exact formatting, runnable doctests, and the rule that surrounding code is copied through unchanged.
---

# Docstrings for named public functions

## What you are producing

You are given a working module and a list of public function names. For each named function you add
one Google-style docstring and change nothing else. You then return those functions' complete
definitions, in the order the names were listed.

Do not document functions that were not named. Do not refactor, reformat, rename, reorder, or
"improve" any code. Signatures and every executable statement — including nested helpers, comments,
and decorators — come through byte-for-byte identical. Never abbreviate a body with `...` or
`# unchanged`.

## The four required parts (this is where entries usually fail)

For **every single named function**, the docstring must contain all of the following that apply, and
`Examples:` always applies:

| Section | Include it when | Skip it when |
| --- | --- | --- |
| summary line | always | never |
| `Args:` | the signature has at least one parameter (excluding `self`/`cls`) | the signature takes no parameters |
| `Returns:` | the body has a `return <value>` or a `yield` | the function only returns `None` implicitly |
| `Raises:` | the body contains an explicit `raise` statement | the body has no explicit `raise` |
| `Examples:` | **always — every named function needs one** | never |

A docstring that is only a summary plus a sentence or two of prose is wrong, no matter how well
written the prose is. A docstring with `Args:` and `Returns:` but no `Examples:` is wrong. Before you
finish, count: one `Examples:` block per named function, no exceptions.

Sections appear in exactly this order: `Args:` → `Returns:` → `Raises:` → `Examples:`.

## Exact layout

Follow this skeleton literally. The summary text starts on the same line as the opening `"""` — never
on the line below it.

```python
def example_name(first: str, second: int = 0) -> bool:
    """Validate one short imperative sentence here.

    Args:
        first (str): What this parameter is.
        second (int): What this parameter is.

    Returns:
        bool: What the result means.

    Raises:
        ValueError: When the condition that triggers it holds.

    Examples:
        >>> example_name('abc', 1)
        True
    """
    ...
```

Rules embodied above:

- `"""Summary…` — no newline and no space between the quotes and the first word.
- Exactly one blank line between the summary and the first section, and between each pair of
  sections. No blank line before the closing `"""`.
- Closing `"""` on its own line, indented to the function body's level.
- Section headers (`Args:`, `Returns:`, `Raises:`, `Examples:`) sit at the docstring's indent level;
  their entries are indented one further level. Spaces only, never tabs.
- No blank line between `def` and the docstring, or between the docstring and the first statement.
- If the docstring text contains a backslash, make it a raw string: `r"""…"""`.

## The summary line

One line, imperative mood, describing what the function does — not a restatement of the signature and
not a line copied out of the body.

- Capitalize the first word and end with `.`, `!`, or `?`.
- The first word must be one of:
  `add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.
  Pick the one that genuinely fits the function's behavior; capitalize it (`Check…`, `Generate…`).
- Do not repeat the function name or parameter list in it.

## `Args:`

- List every parameter in signature order. Omit `self` and `cls`. Add no name that is not in the
  signature, and drop none that is.
- Annotated parameter: `name (annotation): description`, where the annotation is copied **exactly**
  from the signature — including `bool`, `Any`, `int = 1` written as just `int`, `Generator`,
  `Optional[str]`, and so on. Do not translate a type into words.
- Unannotated parameter: `name: description`. Do not invent a type for it.
- Mention a default's effect in the description if it matters; keep the type field to the annotation.

## `Returns:`

- Format: `annotation: description`, with the annotation copied exactly from the signature's return
  annotation.
- For a generator function, use the declared return annotation and describe what is yielded.
- Omit the whole section for a function that returns nothing.

## `Raises:`

- One entry per exception class that the body raises with an explicit `raise`, including `raise`s
  inside nested helper functions and inside `except` blocks.
- Format: `ExceptionType: condition that triggers it.` Use the class name exactly as written in the
  code (project-specific error classes included).
- Do not list exceptions that merely propagate from a call, and do not invent plausible ones.

## `Examples:`

At least one `>>>` line per named function, inside that function's own docstring. An example that
lives in another function's docstring or elsewhere in the module does not count.

The doctest must actually run and its expected output must match character-for-character:

- Show the true `repr`. A string result prints as `'abc'` with quotes; use `print(...)` if you want
  bare text.
- A call that returns `None` produces **no** expected-output line at all.
- Never write an expected line you have not reasoned out precisely — avoid floats with long
  representations, unordered `set`/`dict` output, and objects whose repr contains a memory address.
- Consume a generator so the output is concrete, e.g. `>>> list(gen(...))` or `>>> next(gen(...))`.
- Multi-line setup is allowed with `...` continuation lines.

**When the result is not deterministic** — randomness, UUIDs, timestamps, secrets, environment,
hashing — do not print the value. Assert a stable property instead, so the expected line is fixed:

```
>>> value = nondeterministic_call(8)
>>> isinstance(value, str)
True
>>> len(value)
8
```

To demonstrate an error path, either call the function inside `try`/`except` and print something
fixed, or use the traceback form, whose final line must match the real message exactly:

```
>>> failing_call(-1)
Traceback (most recent call last):
    ...
ValueError: exact message text from the code
```

If you are not certain of the message text, use a passing call instead — a broken doctest is worse
than a modest one.

## Before you hand it back

Walk each named function once more and confirm:

1. Summary begins on the `"""` line, uses an approved capitalized first word, ends in `.`/`!`/`?`.
2. Every signature parameter appears in `Args:` in order, with the exact annotation.
3. `Returns:` present iff the function returns or yields a value, annotation copied exactly.
4. `Raises:` lists exactly the explicitly raised exception classes — no more, no fewer.
5. `Examples:` present with at least one `>>>` that would really pass.
6. Blank-line and indentation rules hold; body and signature are untouched.

Terms like "doc block," "API note," "function help," and "docstring" all mean this artifact. Derive
its contents from the actual signature and body, never from what the name suggests.

Output only the complete definitions of the named public functions, in the order listed, with the
docstrings inserted and full executable bodies retained. No code fence, no commentary.