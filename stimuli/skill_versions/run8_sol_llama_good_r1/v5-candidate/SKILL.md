---
name: docstring-api
description: Add complete Google-style docstrings to named public Python functions when signatures, executable code, output scope, and deterministic doctest behavior must remain unchanged.
---

# API docstrings

Add a Google-style docstring to each named public function. Return only the complete definitions of those functions, in the requested order.

Treat the supplied source as authoritative. The only permitted change is inserting a docstring as the first statement of each named function. Preserve every decorator, signature, annotation, comment, quotation style, indentation level, and executable statement. Include every function's full body. Do not add imports, reformat code, or substitute `...`, `pass`, or another placeholder.

## Source-first workflow

For each named function:

1. Copy its complete original definition.
2. Record every signature parameter in order, excluding only `self` and `cls`.
3. Trace every return path, including short-circuit expressions, fallback values, and sentinel values.
4. Find every explicit `raise` statement in the function's own body, excluding raises inside nested functions or classes.
5. Determine behavior from the executable statements, including defaults, constants, transformations, output-length calculations, regular-expression methods and flags, and prefix-versus-full-string matching.
6. Choose a doctest whose expected result is guaranteed by the implementation.
7. Insert the docstring without changing any original source text.

Document implemented behavior even when the function name, annotation, or apparent intent suggests otherwise. An annotation does not perform runtime validation.

## Required content

Every named function must contain the applicable sections below.

### Summary

Write a one-line imperative summary that describes the implementation without repeating the signature.

Start with exactly one capitalized word from this list:

`Add|Build|Check|Clip|Compress|Convert|Count|Create|Decode|Detect|Encode|Format|Generate|Identify|Interpret|Iterate|Join|Normalize|Parse|Remove|Return|Reverse|Test|Transform|Validate`

End the summary with `.`, `!`, or `?`.

### Args

Include `Args:` when the signature has parameters other than `self` or `cls`.

List every eligible parameter exactly once and in signature order.

- Use the exact parameter name from the signature.
- For an annotated parameter, write `name (annotation): description` and reproduce the annotation exactly.
- For an unannotated parameter, write `name: description`; do not invent a type.
- Describe the parameter's actual effect.
- State the default when one appears in the signature.
- Do not claim that the function rejects or validates a type unless its body performs that check.

### Returns

Include `Returns:` when the function has a value-returning path.

Write `annotation: description` and reproduce the return annotation exactly. Describe every possible returned value, including fallback values produced by conditionals or short-circuit expressions.

A function that returns `False`, `None`, an empty value, or another sentinel for invalid input is returning a value; it is not raising an exception.

Omit `Returns:` only when the function has no value return.

### Raises

Include `Raises:` only for exceptions produced by explicit `raise` statements in that function's own body.

For every such exception, write:

`ExceptionType: condition`

Cover every condition that reaches the explicit `raise`.

Do not infer a `Raises:` entry from:

- An annotation or an unexpected argument type.
- A called function or method.
- An operator, conversion, indexing operation, parser, regular expression, or library call.
- An `assert` statement.
- A function name or conventional expectation.
- A branch that returns a fallback value.

If the function contains no explicit `raise` statement, omit `Raises:` entirely.

### Examples

Always include `Examples:` with at least one runnable `>>>` doctest that calls the documented function.

Every displayed result must exactly equal Python's output. Use exact representations, including quotation marks for strings and the spellings `True`, `False`, and `None`. A setup prompt that produces no output does not need an expected-output line.

Before accepting an example, evaluate it against the supplied body. Check:

- The exact argument values and omitted defaults.
- Every branch and short-circuit condition.
- Case sensitivity.
- Regular-expression flags and whether the code performs prefix or full-string matching.
- The precise size effect of each transformation.
- Whether the result can vary between executions.

Do not add a `Raises:` section merely because a doctest uses unusual input.

## Nondeterministic results

Never show an invented literal for random, UUID-based, time-based, environment-dependent, or otherwise nondeterministic output. Do not use masked values, placeholder characters, ellipses, wildcard output, or plausible-looking samples.

Instead, call the function and test a deterministic property guaranteed for every possible result, such as its type, exact length, delimiter placement, or allowed character set. Derive expected lengths from the implementation; account for transformations that expand or shrink the output.

Assign the result once when checking multiple properties:

```python
>>> token = create_token()
>>> isinstance(token, str), len(token)
(True, 32)
```

Use only guaranteed properties. Do not test uniqueness, inequality between generated values, or anything merely likely to be true.

## Layout and order

Use triple double quotes. Use a raw triple-double-quoted docstring when its contents include backslashes.

Place the summary immediately after the opening quotes. Put the closing quotes of a multiline docstring on their own line. Leave no blank line immediately before or after the docstring.

Use spaces and standard Google-style indentation. Indent section entries one level beyond their headings. Put exactly one blank line between the summary and the first section and between adjacent sections.

Order applicable sections as:

`Args:` → `Returns:` → `Raises:` → `Examples:`

`Examples:` is always required. Omit another section only when it is inapplicable.

When requirements overlap, use this precedence:

1. Preserve the supplied definition verbatim except for its inserted docstring.
2. Return only the named functions in the requested order.
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
- `Returns:` covers every value-returning path.
- `Raises:` contains all and only exceptions from explicit `raise` statements in that function.
- `Examples:` contains a runnable call to that function.
- Every expected doctest result is deterministic, exact, and guaranteed.
- No generated result is represented by a guessed literal or placeholder.
- No unrelated definition, import, code fence, or explanation is included.

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with their docstrings inserted. Include every full function body. Do not include imports, unrelated definitions, code fences, or surrounding commentary.