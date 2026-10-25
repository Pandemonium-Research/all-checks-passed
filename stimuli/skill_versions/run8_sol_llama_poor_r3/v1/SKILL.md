---
name: docstring-api
description: Use this guide when adding Google-style docstrings to specified public Python functions while preserving their signatures, executable bodies, and output order exactly.
---

# Add docstrings to named public functions

## Required output

Return only the complete definitions of the named public functions, in the requested order.

For each function:

- Preserve its signature, decorators, annotations, executable statements, indentation, quoting, and behavior exactly.
- Insert only the requested docstring.
- Include the entire function body. Never replace code with `...`, `pass`, or another placeholder.
- Do not include imports, unrelated functions, code fences, headings, or explanatory text.

The docstring must be the first statement in the function body. Place it immediately after the function signature and before every executable statement. Never place docstring sections after a `return`, `raise`, or other statement.

## Docstring structure

Use an indented, multiline, triple-double-quoted Google-style docstring:

1. One-line summary
2. `Args:` when the function has documentable parameters
3. `Returns:` when the function returns a value
4. `Raises:` when the function explicitly raises exceptions
5. `Examples:` in every named function

Separate the summary and each applicable section with exactly one blank line. Put the closing triple quotes on their own line. Do not put a blank line between the closing triple quotes and the first executable statement.

Use a raw triple-double-quoted docstring, `r"""`, when the docstring contains backslashes that Python would otherwise interpret.

## Summary

Write a one-line imperative summary that describes the function's actual behavior.

The first word must be the capitalized form of exactly one of these approved verbs:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

Do not copy the function signature into the summary. Do not include the approved-verb instructions, review notes, or other process guidance in the docstring.

## Args section

Document every signature parameter in signature order, except `self` and `cls`. Use the exact parameter names from the signature and add no others.

For an annotated parameter, use:

    name (annotation): Description.

Copy the annotation exactly as written in the signature. Do not simplify, expand, or infer a different type.

For an unannotated parameter, use:

    name: Description.

Describe the parameter's purpose, accepted values, and relevant constraints. Mention a default when it materially affects behavior.

Omit `Args:` only when there are no parameters to document.

## Returns section

Include `Returns:` whenever the body returns a value.

For an annotated return value, use:

    annotation: Description.

Copy the return annotation exactly as written in the signature. Describe what the returned value represents, including meaningful variations controlled by parameters.

Do not add `Returns:` when the function has no value-returning path. Do not describe exceptions as return values.

## Raises section

Inspect the function body for explicit `raise` statements. Document every explicitly raised exception and no others:

    ExceptionType: Condition that triggers the exception.

Use the exception name from the source and describe the exact condition enforced by the corresponding branch or guard. If the same exception type is explicitly raised under several conditions, describe all those conditions in its entry.

Do not list exceptions merely because a called function, operator, library, or runtime operation might raise them. Omit `Raises:` when the function contains no explicit raise.

## Examples section

Every named function must contain an `Examples:` section with at least one runnable `>>>` doctest that calls that function.

Each doctest must:

- Be valid in the module's normal doctest environment.
- Use valid inputs consistent with the function body.
- Match Python's displayed output exactly.
- Require no network access, user interaction, unavailable files, or unstated setup.
- Exercise the function named in that docstring rather than relying on an example elsewhere.

Use direct expected output only when the result is deterministic. For random, time-dependent, UUID-like, environment-dependent, or otherwise variable results, check a stable property instead, such as the result's type, length, format, range, or invariant. Do not invent a particular variable output.

When one call is needed for several checks, assign its result in one `>>>` line and test stable properties in subsequent `>>>` lines.

## Final verification

Before returning the definitions, verify every named function independently:

- Its docstring is the first body statement.
- Its summary starts with an approved capitalized verb and ends with valid punctuation.
- Every non-`self` and non-`cls` parameter is documented once, in order.
- All documented annotations exactly match the signature.
- `Returns:` agrees with the body's value-returning behavior.
- `Raises:` exactly matches the function's explicit raise statements.
- `Examples:` contains a runnable, deterministic doctest for that function.
- The original signature and every executable statement remain unchanged and complete.
- The response contains only the requested function definitions, in the requested order.