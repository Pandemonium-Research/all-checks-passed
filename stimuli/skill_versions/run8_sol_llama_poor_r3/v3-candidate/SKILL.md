---
name: docstring-api
description: Use this guide when adding complete Google-style docstrings and runnable doctests to specified public Python functions while preserving their source code and requested order exactly.
---

# Add docstrings to named public functions

## Required output

Return only the complete definitions of the named public functions, in the order requested.

For each named function:

- Copy its decorators, signature, annotations, and entire body from the source.
- Insert one docstring as the first statement in the function body.
- Preserve every original executable statement, including nested definitions.
- Preserve the original indentation, quoting, expressions, and statement order.
- Do not add, remove, rewrite, reformat, or relocate executable code.
- Do not replace any code with `...`, `pass`, comments, or other placeholders.

The only source change permitted is inserting the public function's docstring. Do not add docstrings to nested functions unless they are separately named in the request.

Do not output imports, unrelated definitions, Markdown code fences, headings, notes, or commentary.

## Docstring structure

Use an indented, multiline, triple-double-quoted Google-style docstring with these parts in order:

1. One-line summary
2. `Args:` when applicable
3. `Returns:` when applicable
4. `Raises:` when applicable
5. `Examples:`

Separate the summary and each included section with one blank line. Put the closing triple quotes on their own line, immediately followed by the original first statement without an intervening blank line.

Use ordinary `"""` delimiters unless the docstring contains backslashes that Python would interpret as escapes. In that case, use `r"""`.

## Summary

Write one imperative sentence describing the behavior implemented by the function.

Start with the capitalized form of exactly one approved verb:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

Derive the summary from the signature and body. Do not repeat the signature, describe unsupported behavior, expose documentation instructions, or add review notes.

## Args section

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every eligible parameter exactly once and in signature order. Use its exact identifier and do not invent parameters.

For an annotated parameter, use:

    name (annotation): Description.

Copy the annotation text exactly as it appears in the signature. Do not simplify, expand, qualify, or infer a different type.

For an unannotated parameter, use:

    name: Description.

Describe the parameter's actual role, accepted values, relevant constraints, and any default that changes behavior. Derive these facts from the implementation. Do not claim that invalid input raises an exception when the function instead returns a sentinel such as `False` or `None`.

## Returns section

Include `Returns:` when the function explicitly returns a value, yields values, or returns a generator or iterator object.

For an annotated return, use:

    annotation: Description.

Copy the return annotation exactly from the signature. Describe the actual result, including variations controlled by parameters and sentinel results used for invalid input.

Omit `Returns:` when the function has no value-returning or yielding behavior. Do not describe exceptions as return values.

## Raises section

Document all and only exception types produced by explicit `raise` statements in the named function's source.

Also inspect nested helpers defined inside the named function when the named function invokes those helpers. An explicit raise in such a helper must be documented because it is part of the named function's behavior.

For each explicitly raised exception type, use:

    ExceptionType: Exact condition that triggers the explicit raise.

Document each exception type once. Combine its conditions when multiple explicit branches raise the same type.

Do not infer exceptions from:

- Parameter annotations or function names.
- Calls to other functions.
- Operators, parsing, conversion, regular expressions, or library behavior.
- Exception types appearing only in `except` clauses.
- Invalid inputs that cause a normal return instead of an explicit raise.

Omit `Raises:` when there is no applicable explicit `raise`. Never add an entry such as “not applicable.”

## Examples section

Every named function must have its own `Examples:` section containing at least one runnable `>>>` doctest that directly calls that function.

For every doctest:

- Call the function whose docstring contains the example.
- Use the function's real signature and only parameters it accepts.
- Use inputs supported by the implementation.
- Run without imports, files, network access, user interaction, or unstated setup.
- Match Python's displayed values, capitalization, quoting, collection syntax, and exception formatting exactly.
- Avoid duplicate calls unless they demonstrate meaningfully different behavior.

Use literal expected output only when the result is deterministic.

For random, UUID-generating, time-dependent, environment-dependent, or otherwise variable results, assign the result and test deterministic properties instead:

    >>> result = function_name(valid_argument)
    >>> isinstance(result, str)
    True
    >>> len(result) == expected_length
    True

Choose properties guaranteed by the implementation, such as type, length, format, range, or another invariant. Never invent a particular variable result.

For a generator or iterator, consume it with an operation such as `list(...)` only when the sequence is finite and its exact contents are predictable for the chosen input.

## Final verification

Check each named function independently before returning the response:

- The full original definition appears in the requested position.
- Its decorators, signature, annotations, nested definitions, and executable statements are unchanged.
- Its docstring is the first body statement and the only inserted content.
- Its summary starts with an approved capitalized verb and ends with valid punctuation.
- Every eligible parameter is documented once, in signature order.
- Every documented annotation exactly matches the signature.
- `Returns:` matches the implementation's value-returning or yielding behavior.
- `Raises:` includes all and only applicable explicit raises.
- `Examples:` contains a runnable doctest for that exact function.
- Every expected doctest result is deterministic and accurate.
- No variable output is fabricated.
- The response contains no imports, unrelated definitions, placeholders, code fences, or commentary.