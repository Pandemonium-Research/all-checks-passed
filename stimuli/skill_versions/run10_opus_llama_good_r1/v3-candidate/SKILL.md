---
name: docstring-api
description: Use this skill when adding Google-style API docstrings to named public Python functions, so the returned definitions document every parameter, return, and explicitly raised exception and carry doctests that actually pass, without changing any code.
---

# API docstrings

Add documentation under the Google docstring convention to the named public functions only.
Do not document unrelated functions. Do not modify executable code or signatures. Parameter and
return types belong in the docstrings even though the signatures already carry annotations.

## Required content

For every named public function:

1. Write a one-line imperative summary. Start it with a capital letter, end it with punctuation,
   specifically `.`, `!`, or `?`, and do not repeat the function signature there. Capitalize one
   locally recognized first word from this pipe-delimited set:
   `add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.
2. In `Args:`, document every parameter, in signature order, except `self` and `cls`. Use exactly
   the signature's parameter names and no extra names. An annotated entry is
   `name (annotation): description`; match the signature annotation exactly. For an unannotated
   parameter, use `name: description` rather than inventing a type.
3. When the body returns a value, document every return value in `Returns:` as
   `type: description`; match the return annotation exactly. Do not add `Returns:` for a function
   without a value return.
4. In `Raises:`, document every exception raised explicitly in the function body as
   `ExceptionType: condition`, and no exception that the body does not explicitly raise.
5. Add `Examples:` with at least one runnable `>>>` doctest per named public function. Every
   doctest must execute successfully and its expected output must match exactly. Stabilize
   nondeterministic results.

## Raises: one entry per literal `raise`

Scan the function's own body for `raise` statements. Each one, and only each one, becomes an entry,
using the exception class name exactly as written, including a project's own error classes. Do not
add an entry for:

- an exception the interpreter might produce on its own (`TypeError` for a wrong argument type,
  `ValueError`, `KeyError`, `AttributeError`) when no `raise` in this body produces it;
- an exception that a helper called by the body might raise;
- a rule you stated in `Args:` — describing a parameter as a boolean is not evidence that the body
  raises `TypeError` when it is not one;
- an exception raised in a neighbouring function.

A guard such as `if not isinstance(x, int) or x < 1: raise ValueError(...)` yields exactly one
entry: `ValueError`. A body containing no `raise` gets no `Raises:` section at all.

## Doctest output is traced from the body, never guessed

Do not predict output from the function's name, its summary, or what the code appears to intend.
For each example: pick a small concrete input, walk the body statement by statement with it —
including every guard clause and early return — and write the expected line as Python's `repr` of
the value the final `return` actually produces. If your input trips a guard such as
`if not <predicate>(value): return value`, the result is the unchanged input; either show that, or
pick an input that reaches the branch you meant to demonstrate. Apply the real semantics of every
call on the path: `''.join(parts)` inserts no separator, `str.title()` capitalizes each alphabetic
run, `[::-1]` reverses, hex encoding of *n* bytes yields *2n* characters. Keep the example
self-consistent — a length argument of `10` must not produce a result of a different length. An
expression evaluating to `None` prints nothing, so leave no expected-output line under it. Use
`...` to continue a multi-line statement, and put no blank line inside `Examples:`.

## Varying results are asserted, not printed

If the value depends on randomness, cryptographic entropy, the clock, process state, iteration
order, object identity, or a temporary path — `random`, `secrets`, `os.urandom`, `uuid`, `time`,
`datetime.now`, `id()`, `tempfile` — its literal output can never match on a later run. Never paste
a sample value such as a specific UUID or a specific random string as expected output, however
plausible it looks. Bind the result to a name and assert properties the code guarantees every run,
checking transformed sizes rather than the raw argument where the code transforms them:

```
Examples:
    >>> value = generate_token(8)
    >>> isinstance(value, str)
    True
    >>> len(value)
    16
    >>> set(value) <= set('0123456789abcdef')
    True
```

## Layout and order

Use triple double quotes, and use a raw triple-quoted docstring when it contains backslashes. Put
the summary immediately after the opening triple quotes, with no surrounding whitespace. For a
multiline docstring, put the closing triple quotes on their own line. Leave no blank line
immediately before or after the docstring. Use spaces and the standard indented Google layout:
indent the docstring to match the function body and indent section entries one additional level.
Put a blank line between the summary and each section, using exactly one blank line at each break.
Order applicable sections as
`Args:` → `Returns:` → `Raises:` → `Examples:`.

Resolve overlaps in this precedence: preserve source, limit scope to named functions, then trust
exact signature/body evidence over guesses. Omit inapplicable sections.

## Worked example

Before:

```python
def root(value: float) -> float:
    if value < 0:
        raise ValueError("value")
    return value ** 0.5
```

After:

```python
def root(value: float) -> float:
    """Return the square root of a value.

    Args:
        value (float): Number to process.

    Returns:
        float: The square root.

    Raises:
        ValueError: If value is negative.

    Examples:
        >>> root(9.0)
        3.0
    """
    if value < 0:
        raise ValueError("value")
    return value ** 0.5
```

## Final check before returning

- Every signature parameter appears in `Args:`, with no extras and no invented types.
- Every `Raises:` entry matches a literal `raise` in that function's own body, and every such
  `raise` has an entry.
- Every expected output was traced through the body, guards and early returns included.
- No doctest expects a value that could differ on the next run.

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with the
requested docstrings inserted. Keep their full executable bodies; do not replace them with `...`.
Include no code fence or surrounding explanation.