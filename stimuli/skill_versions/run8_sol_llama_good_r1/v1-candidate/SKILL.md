---
name: docstring-api
description: Use this skill to add complete Google-style docstrings to specified public Python functions while preserving their signatures and executable bodies exactly.
---

# API docstrings

Add Google-style docstrings to the named public functions only. Return each complete function
definition in the requested order. Apart from inserting its docstring, copy every signature and
executable statement verbatim.

Do not document unrelated functions, add decorators, reformat code, rename parameters, change
quoting in existing statements, or replace any part of a body with a placeholder.

## Source-first workflow

For each named function, inspect its exact signature and body before writing:

1. Record every parameter from the signature, in order, excluding only `self` and `cls`.
2. Determine whether the body returns a value.
3. Record only exceptions appearing in explicit `raise` statements in that function.
4. Trace the actual implementation, defaults, branches, patterns, and constants to determine
   behavior for the examples.
5. Choose a deterministic doctest whose expected output follows from the implementation.

Treat the source as authoritative. Do not document intended, conventional, or assumed behavior
when it differs from what the code actually does.

## Required content

For every named public function:

1. Write a one-line imperative summary. Start it with a capital letter, end it with `.`, `!`, or
   `?`, and do not repeat the function signature. Capitalize one locally recognized first word
   from this pipe-delimited set:
   `add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.
2. Add `Args:` and document every parameter in signature order, except `self` and `cls`. Use the
   exact parameter name and add no extra names. For an annotated parameter, write
   `name (annotation): description` and reproduce the annotation exactly. For an unannotated
   parameter, write `name: description`; do not infer a type. Describe defaults consistently with
   the signature.
3. If the function returns a value, add `Returns:` with `type: description`, reproducing the
   return annotation exactly. Make the description cover all value-returning branches. Omit
   `Returns:` when the function has no value return.
4. Add `Raises:` only when the function contains an explicit `raise` statement. Document every
   explicitly raised exception as `ExceptionType: condition`. Do not infer exceptions from type
   annotations, invalid-looking inputs, called functions, operators, library calls, or regular
   expressions. A function that returns `False` for invalid input does not raise an exception
   unless its body explicitly says `raise`.
5. Add `Examples:` containing at least one runnable `>>>` doctest. Each expected result must match
   the real implementation exactly.

## Doctest accuracy

Never represent generated output with invented sample text, placeholder characters, masked
patterns, or a guessed random value. For nondeterministic output, test a deterministic property of
one generated result, such as its type, length, prefix, character set, or format. Assign the result
once when multiple checks are needed.

For deterministic functions, select inputs whose result can be derived unambiguously from the
body. Respect signature defaults and actual branch, matching, and case-sensitivity behavior.
Do not write examples based only on the function name or summary. Mentally execute each prompt
against the supplied source and verify that every displayed value, string length, and Boolean is
exact.

Doctests may use setup prompts with no displayed output. Any prompt that produces output must be
followed by its exact expected representation.

## Layout and order

Use triple double quotes. Use a raw triple-quoted docstring when the docstring itself contains
backslashes. Put the summary immediately after the opening quotes, with no surrounding whitespace.
For a multiline docstring, put the closing quotes on their own line.

Leave no blank line immediately before or after the docstring. Use spaces and the standard
indented Google layout: indent the docstring to match the function body and indent section entries
one additional level. Put exactly one blank line between the summary and each section and between
adjacent sections.

Order applicable sections as:

`Args:` → `Returns:` → `Raises:` → `Examples:`

Omit only sections that are explicitly inapplicable. `Examples:` is always required.

When instructions overlap, use this precedence:

1. Preserve the source verbatim except for inserted docstrings.
2. Limit changes to the named functions.
3. Follow exact signature and body evidence.
4. Follow documentation style requirements.

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

## Final verification

Before returning the result, verify for every named function that:

- Its signature and executable statements are unchanged.
- Its full body is present.
- Every eligible parameter appears exactly once and in signature order.
- The return annotation is copied exactly when `Returns:` applies.
- `Raises:` contains all and only explicitly raised exceptions.
- At least one `>>>` prompt is present.
- Every doctest is executable and deterministic.
- No generated or random value is shown as guessed literal output.
- The definitions appear in the requested order.

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with the
requested docstrings inserted. Include no code fence, imports, surrounding explanation, or
unrelated definitions.