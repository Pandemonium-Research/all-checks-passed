---
name: docstring-api
description: Add complete Google-style docstrings to named public Python functions and return only their unchanged full definitions. Use when every parameter, return value, explicitly raised exception, and deterministic runnable doctest must be documented without altering the supplied code.
---

# API docstrings

Add a Google-style docstring to each named public function. Return only the complete definitions of
those functions, in the requested order.

Treat the supplied source as authoritative. The only permitted change is inserting a docstring as
the first statement of each named function. Preserve every decorator, signature, annotation,
indentation level, comment, blank line, string quote, and executable statement. Include each full
body. Do not add imports, reformat code, or replace body content with `...`, `pass`, or another
placeholder.

## Source-first workflow

Process each named function independently:

1. Copy its complete original definition.
2. Record every signature parameter in order, excluding only `self` and `cls`.
3. Identify every branch containing `return expression`. Distinguish these from bare `return`
   statements and implicit fallthrough.
4. Find every explicit `raise` statement in the function's own lexical body, including its branches
   and exception handlers but excluding nested function or class definitions.
5. Trace the implementation exactly. Account for defaults, short-circuiting, fallback returns,
   constants, output transformations, regular-expression methods and flags, prefix-versus-full
   matching, and relevant library behavior.
6. Choose a doctest whose result is guaranteed for every execution with the selected input.
7. Insert the docstring without changing any original source text.

Document implemented behavior, even when the function's name, annotation, or apparent intent
suggests something else. Type annotations describe types; they do not perform runtime validation.

## Required docstring content

### Summary

Write a one-line imperative summary that accurately describes the implementation without repeating
the signature.

The first word must be exactly one of these capitalized words:

`Add|Build|Check|Clip|Compress|Convert|Count|Create|Decode|Detect|Encode|Format|Generate|Identify|Interpret|Iterate|Join|Normalize|Parse|Remove|Return|Reverse|Test|Transform|Validate`

End the summary with `.`, `!`, or `?`.

### Args

Include `Args:` when the signature has parameters other than `self` or `cls`.

List every eligible parameter exactly once, in signature order. Use the parameter's exact name and
add no names that are not in the signature.

- For an annotated parameter, write `name (annotation): description`, reproducing the annotation
  exactly as written.
- For an unannotated parameter, write `name: description`; do not infer a type.
- Describe the parameter's actual effect, including any default shown in the signature.
- Do not claim that a type is validated unless the executable body performs that validation.

Omit `Args:` only when there are no eligible parameters.

### Returns

Include `Returns:` when the function explicitly returns a value with `return expression`.

Write `annotation: description`, reproducing the return annotation exactly. Describe every
value-returning branch, including `False`, `None`, empty values, or other fallback and sentinel
results. A short-circuited expression that returns a fallback value must be documented as a return,
not as an exception.

Omit `Returns:` when the function has only bare `return` statements or implicit fallthrough and
therefore returns no documented value.

### Raises

Include `Raises:` only when the function's own body contains an explicit `raise` statement. For each
explicitly raised exception, write:

`ExceptionType: condition`

Describe every condition that reaches that `raise`.

Do not infer a `Raises:` entry from:

- A type annotation or an input that appears to have the wrong type.
- A call to another function or method.
- An operator, indexing operation, conversion, parser, regular expression, or library call.
- An `assert` statement.
- A function name or expected API convention.
- A branch that returns `False`, `None`, or another fallback.
- An exception that could occur incidentally but is not raised by an explicit `raise` statement in
  this function.

If no explicit `raise` statement appears in the function, omit `Raises:` entirely.

### Examples

Always include `Examples:` with at least one runnable `>>>` doctest that calls the documented
function.

Every displayed result must be the exact Python result. Use exact representations, including quotes
around strings and the correct capitalization of `True`, `False`, and `None`. A setup prompt that
produces no output has no expected-output line.

Before accepting an example, mentally execute every prompt against the supplied body. Verify the
selected arguments, omitted defaults, branch conditions, short-circuit behavior, case sensitivity,
regular-expression flags, matching method, and output-length calculations.

## Nondeterministic doctests

Never show an invented literal result for random, UUID-based, time-based, environment-dependent, or
otherwise nondeterministic output. Do not use masked text, placeholder characters, wildcard output,
or a plausible-looking sample.

Instead, call the function and check a deterministic property guaranteed by the implementation,
such as:

- The result's type.
- Its exact length derived from the input and transformations.
- A stable delimiter count or format property.
- Whether all characters belong to a guaranteed character set.
- A tuple of multiple guaranteed properties.

Assign the generated result once before testing multiple properties. For example, when the body
guarantees a string of a known length:

```python
>>> token = create_token()
>>> isinstance(token, str), len(token)
(True, 32)
```

Do not test uniqueness, inequality between generated values, or any other property that is merely
probable. Prefer built-ins and names guaranteed to be available when the module's doctests run.

## Layout and section order

Use triple double quotes. If the docstring contains backslashes, use a raw triple-double-quoted
docstring.

Place the summary immediately after the opening quotes. For a multiline docstring, put the closing
quotes on its own line. Do not leave a blank line immediately before or after the docstring.

Use spaces and standard Google-style indentation. Indent section entries one level beyond their
headings. Put exactly one blank line between the summary and the first section and between adjacent
sections.

Use this order, omitting only sections that are inapplicable:

`Args:` → `Returns:` → `Raises:` → `Examples:`

`Examples:` is never optional.

When requirements overlap, use this precedence:

1. Preserve the supplied definition verbatim except for the inserted docstring.
2. Limit the output to the named functions in the requested order.
3. Trust exact signature and body evidence over names, annotations, or assumptions.
4. Apply the documentation style requirements.

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

Before returning the result, verify every named function:

- Its complete original definition is present.
- Removing the inserted docstring restores the original definition verbatim.
- Definitions appear in the requested order.
- Every eligible parameter appears exactly once and in signature order.
- Every documented annotation exactly matches its source spelling.
- Parameter descriptions reflect actual behavior and defaults.
- `Returns:` covers every value-returning branch and is absent when inapplicable.
- `Raises:` contains all and only exceptions from explicit `raise` statements in that function.
- No exception is inferred from an annotation, called operation, or fallback return.
- `Examples:` contains a runnable call to that function.
- Every expected doctest result is deterministic, guaranteed, and exact.
- No generated value is represented by a guessed literal or placeholder.
- No decorator, signature text, comment, executable statement, or body content was changed.
- No unrelated definition, import, code fence, or explanation appears in the response.

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with their
docstrings inserted. Include every full function body. Do not include imports, unrelated
definitions, code fences, or surrounding commentary.