---
name: docstring-api
description: Add complete Google-style docstrings to specified public Python functions when their original definitions must be returned unchanged except for inserted documentation, including exact parameters, returns, explicit raises, and runnable doctests.
---

# API docstrings

Add a Google-style docstring to each named public function. Return only those complete function
definitions, in the requested order.

Treat the supplied source as authoritative. Apart from inserting each docstring, preserve the
definition verbatim: keep decorators, signatures, annotations, indentation, comments, executable
statements, quoting, and full bodies unchanged. Do not add imports, rewrite code, or use placeholder
bodies.

## Source-first procedure

Process each function independently:

1. Copy its complete definition from the supplied source.
2. Record every signature parameter in order, excluding only `self` and `cls`.
3. Identify every value-bearing return branch.
4. Find every `raise` statement written directly in the function.
5. Trace the implementation, including defaults, branches, constants, regular-expression flags,
   and library behavior.
6. Insert the docstring as the function's first statement.
7. Construct and verify a deterministic doctest that calls the function.

Document actual behavior, even when the function's name, annotation, or apparent intent suggests
something different. An annotation describes a type; it does not perform runtime validation.

## Required docstring content

For every named function, include:

1. A one-line imperative summary that accurately describes the implementation. Start with a
   capitalized word from this set and end with `.`, `!`, or `?`:

   `add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`

   Do not repeat the signature in the summary.

2. An `Args:` section listing every parameter in signature order except `self` and `cls`. Use no
   extra parameter names.

   - For an annotated parameter, use `name (annotation): description` and reproduce the annotation
     exactly as written in the signature.
   - For an unannotated parameter, use `name: description`; do not infer a type.
   - Describe the parameter's real effect and any default shown by the signature.

3. A `Returns:` section when the function has a value return. Use `type: description`, reproducing
   the return annotation exactly. Describe all value-returning branches, including sentinel or
   fallback results. Omit this section only when the function has no value return.

4. A `Raises:` section only if the function itself contains an explicit `raise` statement. Use
   `ExceptionType: condition` for every explicitly raised exception.

   Do not infer exceptions from:

   - Type annotations or invalid-looking inputs.
   - Calls to other functions or library operations.
   - Indexing, operators, assertions, parsing, or regular expressions.
   - A function name or expected API convention.
   - A branch that returns `False`, `None`, or another fallback value.

   If there is no explicit `raise` statement in the function, omit `Raises:` entirely.

5. An `Examples:` section with at least one runnable `>>>` doctest that calls that function. Every
   displayed result must be the exact result Python produces.

## Doctest rules

Choose inputs by tracing the body, not by guessing from the function name. Verify defaults,
case-sensitivity, prefix versus full-string matching, branch conditions, and output lengths.

Never display an invented result for random, UUID-based, time-based, environment-dependent, or
otherwise nondeterministic output. Do not use placeholder characters, masked strings, wildcard
text, or a plausible-looking sample as expected output. Instead, test a deterministic property of
the generated result, such as:

- Its type.
- Its exact length derived from the input.
- Whether it satisfies a stable format or character-set condition.
- A tuple of stable properties.

Assign a generated result once before checking multiple properties. For example:

```python
>>> token = create_token()
>>> isinstance(token, str), len(token) > 0
(True, True)
```

Use exact Python representations for expected values, including quotes around strings and correct
capitalization of `True`, `False`, and `None`. Setup prompts that produce no output need no expected
line.

Before accepting an example, mentally execute every prompt against the supplied implementation.
Do not claim a specific result unless the body guarantees it.

## Layout and section order

Use triple double quotes. If the docstring contains backslashes, use a raw triple-double-quoted
docstring.

Place the summary immediately after the opening quotes. For multiline docstrings, place the closing
quotes on their own line. Do not leave a blank line immediately before or after the docstring.

Use spaces and standard Google-style indentation. Indent section entries one level beyond their
section headings. Put exactly one blank line between the summary and the first section and between
adjacent sections.

Use this order, omitting only inapplicable sections:

`Args:` → `Returns:` → `Raises:` → `Examples:`

`Examples:` is never optional.

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
        value (float): Number whose square root to return.

    Returns:
        float: The square root of the value.

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

## Final verification

Before returning the result, check every named function:

- The complete original definition is present.
- Removing the inserted docstring would restore the original definition verbatim.
- Definitions appear in the requested order.
- Every eligible parameter appears exactly once and in signature order.
- All documented annotations exactly match their source spelling.
- `Returns:` covers every value-returning branch and is absent when inapplicable.
- `Raises:` contains all and only exceptions from explicit `raise` statements in that function.
- `Examples:` contains a runnable call to that function.
- Every expected doctest result is deterministic and exact.
- No generated value is represented by a guessed literal.
- No unrelated definition, import, code fence, or explanation is included.

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with their
docstrings inserted. Include every full function body. Do not include imports, unrelated
definitions, code fences, or surrounding commentary.