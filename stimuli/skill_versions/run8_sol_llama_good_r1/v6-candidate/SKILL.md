---
name: docstring-api
description: Add complete Google-style docstrings to named public Python functions and return only their unchanged full definitions. Use when parameters, return values, explicitly raised exceptions, and deterministic runnable doctests must be documented without altering the supplied code.
---

# API docstrings

Add a Google-style docstring to each named public function. Return only the complete definitions of
those functions, in the requested order.

Treat the supplied source as authoritative. The only permitted change is inserting a docstring as
the first statement of each named function. Preserve every decorator, signature, annotation,
comment, blank line, quotation style, indentation level, and executable statement. Include each
full function body. Do not add imports, reformat code, or replace body content with `...`, `pass`,
or another placeholder.

## Source-first workflow

Process each named function independently:

1. Copy its complete original definition.
2. Record every signature parameter in order, excluding only `self` and `cls`.
3. Trace every return path, including conditional, fallback, sentinel, and short-circuit results.
4. Find every explicit `raise` statement in the function's own lexical body. Exclude raises inside
   nested function or class definitions.
5. Determine behavior from the executable code. Account for defaults, constants, validation
   branches, transformations, output-length changes, regular-expression methods and flags,
   case sensitivity, and prefix-versus-full-string matching.
6. Choose a doctest whose expected result is guaranteed by the implementation.
7. Insert the docstring without changing any original source text.

Document implemented behavior even when the function name, annotation, or apparent intent suggests
something else. Type annotations do not perform runtime validation.

## Required docstring content

### Summary

Write a one-line imperative summary that accurately describes the implementation without repeating
the signature.

The first word must be exactly one of these capitalized words:

`Add|Build|Check|Clip|Compress|Convert|Count|Create|Decode|Detect|Encode|Format|Generate|Identify|Interpret|Iterate|Join|Normalize|Parse|Remove|Return|Reverse|Test|Transform|Validate`

End the summary with `.`, `!`, or `?`.

### Args

Include `Args:` when the signature has parameters other than `self` or `cls`.

List every eligible parameter exactly once, in signature order. Use the exact parameter names and
do not add names absent from the signature.

- For an annotated parameter, write `name (annotation): description`, reproducing the annotation
  exactly as written.
- For an unannotated parameter, write `name: description`; do not infer a type.
- Describe the parameter's actual effect and any default shown in the signature.
- Do not claim that a type is validated, rejected, or converted unless the executable body does so.

Omit `Args:` only when there are no eligible parameters.

### Returns

Include `Returns:` when the function contains a value-returning path such as
`return expression`.

Write `annotation: description`, reproducing the return annotation exactly. Describe every possible
returned value, including `False`, `None`, empty values, and other fallback or sentinel results.
Account for the actual value produced by conditional and short-circuit expressions.

A branch that returns a fallback value does not raise an exception.

Omit `Returns:` when the function has only bare `return` statements or implicit fallthrough.

### Raises

Include `Raises:` only for exceptions raised by explicit `raise` statements in that function's own
body.

For every explicitly raised exception, write:

`ExceptionType: condition`

Describe every condition that reaches the explicit `raise`.

Do not infer a `Raises:` entry from:

- A type annotation or an argument that appears to have the wrong type.
- A call to another function or method.
- An operator, conversion, indexing operation, parser, regular expression, or library call.
- An `assert` statement.
- A function name or conventional API expectation.
- A branch that returns `False`, `None`, or another fallback.
- An exception that might occur incidentally but is not produced by an explicit `raise` statement
  in this function.

If the function contains no explicit `raise` statement, omit `Raises:` entirely.

### Examples

Always include `Examples:` with at least one runnable `>>>` doctest that calls the documented
function.

Every displayed result must be Python's exact result. Preserve quotes around strings and use the
exact spellings `True`, `False`, and `None`. A setup prompt that produces no output has no
expected-output line.

Before accepting an example, execute it mentally against the supplied body. Verify:

- The selected arguments and omitted defaults.
- Every applicable branch and short-circuit condition.
- Case sensitivity and regular-expression flags.
- Whether matching covers a prefix or the complete string.
- The exact effect of transformations on output length.
- Whether any part of the result can vary between executions.

## Nondeterministic doctests

Never show an invented literal result for random, UUID-based, time-based, environment-dependent, or
otherwise nondeterministic output. Do not use masked text, placeholder characters, ellipses,
wildcard output, or a plausible-looking sample.

Instead, call the function and check a deterministic property guaranteed for every possible result,
such as:

- The result's type.
- Its exact length as derived from the implementation.
- A stable delimiter count or format property.
- Whether all characters belong to a guaranteed character set.
- A tuple containing multiple guaranteed properties.

Assign the generated result once before checking multiple properties. For example:

```python
>>> token = create_token()
>>> isinstance(token, str), len(token)
(True, 32)
```

Account for transformations such as hexadecimal encoding that expand the result. Do not test
uniqueness, inequality between generated values, or any property that is merely probable. Use only
names guaranteed to be available when the module's doctests run.

## Layout and section order

Use triple double quotes. If the docstring contains backslashes, use a raw triple-double-quoted
docstring.

Place the summary immediately after the opening quotes. For a multiline docstring, put the closing
quotes on its own line. Do not leave a blank line immediately before or after the docstring.

Use spaces and standard Google-style indentation. Indent section entries one level beyond their
headings. Put exactly one blank line between the summary and the first section and between adjacent
sections.

Use this order, omitting only inapplicable sections:

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
- Removing the inserted docstring restores the supplied definition verbatim.
- Definitions appear in the requested order.
- Every eligible parameter appears exactly once and in signature order.
- Every documented annotation exactly matches its source spelling.
- Parameter descriptions reflect actual behavior and defaults.
- `Returns:` covers every value-returning path and is absent when inapplicable.
- `Raises:` contains all and only exceptions from explicit `raise` statements in that function.
- No exception is inferred from an annotation, called operation, or fallback return.
- `Examples:` contains a runnable call to that function.
- Every expected doctest result is deterministic, exact, and guaranteed.
- No generated result is represented by a guessed literal or placeholder.
- No decorator, signature text, comment, executable statement, or body content was changed.
- No unrelated definition, import, code fence, or explanation appears in the response.

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with their
docstrings inserted. Include every full function body. Do not include imports, unrelated
definitions, code fences, or surrounding commentary.