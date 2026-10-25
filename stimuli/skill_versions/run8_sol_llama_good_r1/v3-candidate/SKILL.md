---
name: docstring-api
description: Add complete Google-style docstrings to named public Python functions and return only their unchanged full definitions. Use when every parameter, returned value, explicit exception, and deterministic runnable doctest must be documented without altering the supplied code.
---

# API docstrings

Add Google-style docstrings to the named public functions only. Return each complete definition in the requested order.

Treat the supplied source as authoritative. Apart from inserting a docstring as each function's first statement, copy its definition verbatim. Preserve existing decorators, signatures, annotations, indentation, comments, quoting, and executable statements. Do not add imports, reformat code, or replace any body content with a placeholder.

## Source-first workflow

For each named function:

1. Copy its complete definition.
2. Record every signature parameter in order, excluding only `self` and `cls`.
3. Identify every branch that returns a value.
4. Find every explicit `raise` statement written in that function.
5. Trace the implementation, including defaults, branches, constants, regular-expression behavior, and library calls.
6. Choose a doctest whose expected result is guaranteed by that implementation.
7. Insert the docstring without changing any original source text.

Document actual behavior, even when the function name, annotation, or apparent intent suggests something else. Type annotations do not perform runtime validation.

## Required content

Every named function must have:

1. A one-line imperative summary. Start with exactly one capitalized word from this list and end with `.`, `!`, or `?`:

   `Add|Build|Check|Clip|Compress|Convert|Count|Create|Decode|Detect|Encode|Format|Generate|Identify|Interpret|Iterate|Join|Normalize|Parse|Remove|Return|Reverse|Test|Transform|Validate`

   Describe what the implementation does without repeating the signature.

2. An `Args:` section listing every parameter in signature order except `self` and `cls.`
   
   - Use the exact parameter name and add no extra names.
   - For an annotated parameter, write `name (annotation): description` and reproduce the annotation exactly.
   - For an unannotated parameter, write `name: description`; do not invent a type.
   - Describe the parameter's actual effect and any default shown in the signature.

3. A `Returns:` section when the function returns a value.
   
   - Write `type: description` and reproduce the return annotation exactly.
   - Cover every returning branch, including fallback or sentinel results.
   - Omit `Returns:` only when the function has no value return.

4. A `Raises:` section only when the function contains an explicit `raise` statement.
   
   - Write `ExceptionType: condition` for every explicitly raised exception and cover every triggering condition.
   - Omit `Raises:` entirely when no explicit `raise` appears in that function.
   - Do not infer exceptions from annotations, invalid-looking inputs, called functions, operators, indexing, parsing, regular expressions, assertions, or library behavior.
   - Do not document an exception merely because a parameter has the wrong runtime type.
   - A function that returns `False`, `None`, or another fallback for invalid input does not raise unless its body explicitly executes `raise`.

5. An `Examples:` section containing at least one runnable `>>>` doctest that calls that function. Every displayed result must exactly match what Python produces.

## Doctest accuracy

Derive every example from the function body. Check the exact arguments used, including omitted defaults, branch conditions, case sensitivity, regular-expression flags, prefix-versus-full-string matching, and output-length calculations.

For random, UUID-based, time-based, environment-dependent, or otherwise nondeterministic output:

- Never display an invented, masked, placeholder, or plausible-looking generated value.
- Call the function and test a deterministic property guaranteed for every possible result, such as its type, exact length, stable format, or allowed character set.
- Assign the generated result once when checking multiple properties.
- Do not use an assertion that is merely likely to be true.

Use exact Python representations, including quotes around strings and the correct spelling of `True`, `False`, and `None`. A setup prompt that produces no output needs no expected-output line.

Mentally execute every prompt against the supplied implementation before accepting it. If the implementation does not guarantee the displayed result, choose another example.

## Layout and order

Use triple double quotes. Use a raw triple-double-quoted docstring when the docstring contains backslashes.

Place the summary immediately after the opening quotes. For a multiline docstring, place the closing quotes on its own line. Leave no blank line immediately before or after the docstring.

Use spaces and standard Google-style indentation. Indent section entries one level beyond their headings. Put exactly one blank line between the summary and the first section and between adjacent sections.

Order applicable sections as:

`Args:` → `Returns:` → `Raises:` → `Examples:`

`Examples:` is always required. Omit other sections only when explicitly inapplicable.

When requirements overlap, use this precedence:

1. Preserve the supplied definition verbatim except for the inserted docstring.
2. Limit output to the named functions.
3. Follow exact signature and body evidence.
4. Apply documentation style requirements.

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
- `Returns:` covers all value-returning branches and is absent when inapplicable.
- `Raises:` contains all and only explicitly raised exceptions from that function.
- `Examples:` contains a runnable call to that function.
- Every expected doctest result is deterministic and exact.
- No nondeterministic value is represented by a guessed literal.
- No unrelated definition, import, code fence, or explanation is included.

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with their docstrings inserted. Include every full function body. Do not include imports, unrelated definitions, code fences, or surrounding commentary.