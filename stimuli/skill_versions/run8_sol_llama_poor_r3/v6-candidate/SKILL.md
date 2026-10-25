---
name: docstring-api
description: Use this guide to add complete Google-style docstrings and runnable doctests to specified public Python functions while preserving their definitions verbatim except for the inserted docstrings.
---

# Add docstrings to named public functions

## Required output

Return only the complete definitions of the named public functions, in the requested order.

For each named function:

- Preserve its decorators, signature, annotations, and complete executable body exactly as provided.
- Insert only one docstring, as the first statement in the function body.
- Preserve all nested definitions and executable statements in their original order and form.
- Never correct, reformat, simplify, or omit original code.
- Never replace body content with `...`, `pass`, comments, or another placeholder.
- Do not add docstrings to nested functions unless they are separately named in the request.

Do not include imports, unrelated definitions, Markdown code fences, headings, separators, or explanatory text. Do not place code fences between function definitions. Removing the inserted docstrings from the response must reproduce the requested definitions verbatim.

## Docstring structure

Use an indented, multiline, triple-double-quoted Google-style docstring with these parts in order:

1. One-line summary
2. `Args:` when the function has documentable parameters
3. `Returns:` when the function returns or yields a value
4. `Raises:` when the named function explicitly raises an exception
5. `Examples:` in every named function

Separate the summary and each included section with exactly one blank line. Put the closing triple quotes on their own line immediately before the original first statement, with no blank line between them.

Use ordinary `"""` delimiters. Use `r"""` only when the docstring itself contains backslashes that Python would otherwise interpret as escape sequences.

## Summary

Write one imperative sentence describing the function's actual behavior.

The first word must be the capitalized form of exactly one of these approved verbs:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

Derive the behavior from the complete implementation, not only from the function name. Do not claim that invalid input raises when the implementation instead returns `False`, `None`, or another normal result. Do not copy the signature into the summary or include process instructions, review notes, or unsupported behavior.

## Args section

Document every signature parameter exactly once and in signature order, except `self` and `cls. Use the exact parameter names from the signature and add no others.

For an annotated parameter, use:

    name (annotation): Description.

Copy the annotation exactly as written in the signature. Do not simplify, expand, qualify, or infer a different type.

For an unannotated parameter, use:

    name: Description.

Describe the parameter's actual purpose, accepted values, relevant constraints, and any default that materially changes behavior. Distinguish invalid input that produces a normal return value from invalid input handled by an explicit `raise`.

Omit `Args:` only when there are no parameters to document.

## Returns section

Include `Returns:` whenever the function returns a value, yields values, or returns a generator or iterator object.

For an annotated return value, use:

    annotation: Description.

Copy the return annotation exactly as written in the signature. Describe every meaningful result represented by the implementation, including parameter-controlled variants and sentinel values such as `False` or `None`.

For a generator or iterator, describe the values it produces and any relevant ordering or endpoint behavior. Do not describe exceptions as return values.

Omit `Returns:` only when the function has no value-returning or yielding behavior.

## Raises section

Document all and only exceptions produced by explicit `raise` statements within the complete named function definition:

    ExceptionType: Exact condition that triggers the exception.

Inspect nested helpers defined inside the named function. Include an exception explicitly raised by such a helper when the named function invokes that helper as part of its behavior.

Document each exception type once. If several explicit branches raise the same type, combine their triggering conditions in one entry.

Do not infer a `Raises:` entry from:

- A parameter annotation, function name, or validation purpose.
- A call to a separately defined function.
- An operator, conversion, parser, regular expression, or library operation.
- An exception type appearing only in an `except` clause.
- Invalid input handled by returning a normal value.
- A possible incidental runtime error without an explicit `raise`.

Omit `Raises:` when there is no applicable explicit `raise`. Never add entries such as `Not applicable`.

## Examples section

Every named function must have its own `Examples:` section containing at least one runnable `>>>` doctest that directly calls that function.

Build and verify each function's examples independently. Before writing an example, confirm the function's exact name, parameters, defaults, and behavior from its definition.

Each doctest must:

- Call the function whose docstring contains it.
- Pass only arguments accepted by that function's signature.
- Use inputs supported by the implementation.
- Run in the module's normal doctest namespace without imports, files, network access, user interaction, or unstated setup.
- Match Python's displayed output exactly, including type, capitalization, quoting, collection syntax, and ordering.
- Avoid duplicate calls unless they demonstrate meaningfully different behavior.

Do not copy an example from another function without rechecking its function name and arguments.

Use literal expected output only when the implementation guarantees that exact result. For random, UUID-generating, time-dependent, environment-dependent, or otherwise variable results, call the function once, assign the result, and test stable properties guaranteed by the implementation, such as its type, length, format, range, or character set. Never invent a particular variable result.

For a finite generator or iterator, consume it with a deterministic operation such as `list(...)` only when the chosen inputs guarantee finite execution and an exactly predictable sequence.

Prefer a successful deterministic example. If an example intentionally raises, reproduce the complete doctest traceback and exception message exactly.

## Final verification

Before returning the definitions, verify every named function independently:

- The complete original definition appears in the requested position.
- Its decorators, signature, annotations, nested definitions, and executable statements are unchanged.
- Its docstring is the first body statement and the only inserted content.
- Its summary starts with an approved capitalized verb and ends with valid punctuation.
- Every eligible parameter is documented once, in signature order.
- Every documented annotation exactly matches the signature.
- `Returns:` covers the actual value-returning, yielding, or generator-returning behavior.
- `Raises:` includes every applicable explicit raise and no inferred exception.
- `Examples:` directly calls the correct function using only its accepted arguments.
- Every doctest is runnable and every expected result is guaranteed by the implementation.
- No variable output is presented as a fixed value.
- Removing the docstrings leaves the requested definitions verbatim.
- The response contains no imports, unrelated definitions, placeholders, code fences, headings, separators, or commentary.