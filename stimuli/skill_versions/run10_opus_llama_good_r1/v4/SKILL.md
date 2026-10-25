---
name: docstring-api
description: Use this skill when adding API docstrings to named public Python functions, so the returned definitions follow the project's Google-style documentation contract without changing code.
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
   `ExceptionType: condition`, and no exception that the body does not explicitly raise. An
   exception counts as explicitly raised only when a `raise` statement appears in that function's
   own body; name the class exactly as written there, including a project's own error classes. A
   type described in `Args:` is not evidence of a `raise` — a `bool` parameter with no guard yields
   no `TypeError` entry. A body with no `raise` gets no `Raises:` section.
5. Add `Examples:` with at least one runnable `>>>` doctest per named public function. Every
   doctest must execute successfully and its expected output must match exactly.
   - Trace each example through the body rather than predicting it from the summary or the
     function name. Follow guard clauses and early returns with your chosen input: if the input
     trips a guard such as `if not <predicate>(value): return value`, the result is the unchanged
     input, so either show that or choose an input that reaches the branch you meant to
     demonstrate. Apply the real semantics of each call on the path — `''.join(parts)` inserts no
     separator, `str.title()` capitalizes each alphabetic run, hex encoding of *n* bytes yields
     *2n* characters.
   - Write the expected line as Python's `repr` of the value actually returned, and keep it
     self-consistent with the arguments — a length argument of `10` cannot produce a result of a
     different length. An expression evaluating to `None` prints nothing, so leave no expected
     line under it. Use `...` to continue a multi-line statement, and leave no blank line inside
     `Examples:`.
   - Stabilize nondeterministic results. When the value depends on randomness, entropy, the clock,
     process state, iteration order, object identity, or a temporary path — `random`, `secrets`,
     `os.urandom`, `uuid`, `time`, `datetime.now`, `id()`, `tempfile` — a pasted sample such as a
     specific UUID or random string can never match on a later run. Bind the result to a name and
     assert properties the code guarantees every time:

     ```
     Examples:
         >>> value = generate_token(8)
         >>> isinstance(value, str)
         True
         >>> len(value)
         8
         >>> set(value) <= set('0123456789abcdef')
         True
     ```

     Assert the size the code actually produces, not the raw argument, wherever the body
     transforms it. A result that varies only in part may assert the fixed part with
     `.startswith(...)` and the varying tail by length.

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

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with the
requested docstrings inserted. Keep their full executable bodies; do not replace them with `...`.
Include no code fence or surrounding explanation.