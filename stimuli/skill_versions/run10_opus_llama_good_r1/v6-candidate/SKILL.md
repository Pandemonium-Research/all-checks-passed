---
name: docstring-api
description: Use this skill when adding Google-style API docstrings to named public Python functions — what each docstring section must contain, how to choose doctest examples that actually pass, and what to return.
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
   `type: description`; match the return annotation exactly. This applies even when the returned
   value is a generator or other object built inside the body. Do not add `Returns:` for a
   function without a value return.
4. In `Raises:`, document every exception raised explicitly in the function body as
   `ExceptionType: condition`, and no exception that the body does not explicitly raise. An
   exception counts as explicitly raised only when a `raise` statement appears in that function's
   own body, including inside a helper defined there; name the class exactly as written there,
   including a project's own error classes. A type described in `Args:` is not evidence of a
   `raise` — a `bool` parameter with no guard yields no `TypeError` entry. A body with no `raise`
   gets no `Raises:` section.
5. Add `Examples:` with at least one runnable `>>>` doctest per named public function. Every
   doctest must execute successfully, terminate, and produce expected output that matches
   character for character. The doctest is the part of this task that fails most often, so apply
   the following four checks to each example before keeping it.

   - **Trace it through the body.** Simulate the call statement by statement against the real
     source. Never infer the result from the function's name, its summary, or a sibling function
     that appears to invert it — a converse pair rarely round-trips on the same input. Follow
     guard clauses and early returns with your chosen input: if the input trips a guard such as
     `if not <predicate>(value): return value`, the result is the unchanged input, so either show
     that or choose an input that reaches the branch you meant to demonstrate. Apply the real
     semantics of each call on the path — `''.join(parts)` inserts no separator, `str.title()`
     capitalizes each alphabetic run, a substitution that inserts a separator leaves that
     separator in the result, hex encoding of *n* bytes yields *2n* characters.
   - **Check the arguments against the body's guards and loops.** Run the validation and bounds
     checks against your literal argument values first; an example that raises where you expected
     a value is a failed doctest. Then confirm every loop terminates for those values. A loop
     conditioned on an exact comparison, such as `while current != end`, terminates only when the
     step lands exactly on the endpoint; arguments that step past it hang forever. Prefer example
     arguments that walk a short, obviously terminating path.
   - **Write the expected line as Python's `repr` of the value actually returned**, and keep it
     self-consistent with the arguments — a length argument of `10` cannot produce a result of a
     different length. An expression evaluating to `None` prints nothing, so leave no expected
     line under it. Use `...` to continue a multi-line statement, and leave no blank line inside
     `Examples:`.
   - **Stabilize nondeterministic results.** When the value depends on randomness, entropy, the
     clock, process state, iteration order, object identity, or a temporary path — `random`,
     `secrets`, `os.urandom`, `uuid`, `time`, `datetime.now`, `id()`, `tempfile` — no literal
     expected value can match on a later run. Never write a sampled, invented, elided, or masked
     value: a specific UUID, a hand-typed random string, a made-up hex blob, or a placeholder such
     as `'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'` or `'a'` all fail the doctest. If you cannot
     compute the exact characters by hand from the source, do not write them as expected output.
     Bind the result to a name instead and assert properties the code guarantees every time:

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
     `.startswith(...)` and the varying tail by length. Membership, length, type, character-set,
     and prefix/suffix checks are the reliable tools here; equality against a literal is not.

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
requested docstrings inserted, separated by one blank line as in the source.

- The output begins with the first named function's `def` line, or with its decorators if it has
  any. Emit no import statements, no `__all__`, no module constants, no module docstring, and no
  other module-level code, even though you read them to trace the examples.
- Emit no module-level function that was not named. Nested functions defined inside a named
  function's body are part of that body: keep them exactly as written and add no docstring to them.
- Reproduce each named function verbatim apart from the inserted docstring. Keep the full
  executable body; do not replace it with `...` or a summary comment.
- Include no code fence, no preamble, and no explanation of what you changed.