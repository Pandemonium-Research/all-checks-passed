---
name: docstring-api
description: Use this guide to add complete Google-style docstrings and runnable doctests to named public Python functions without changing their signatures, executable code, full bodies, or requested order.
---

# Add docstrings to named public functions

## Output contract

Return only the complete definitions of the named public functions, in the order listed in the request.

For each named function:

- Copy its decorators, signature, annotations, and entire body verbatim.
- Insert exactly one docstring as the first statement in the function body.
- Preserve every executable statement, including nested definitions, in its original order and form.
- Include the full body; never substitute `...`, `pass`, comments, or another placeholder.
- Do not correct, reformat, simplify, or otherwise improve the original code.
- Do not add docstrings to nested functions unless they are separately named in the request.

Do not output imports, unrelated definitions, Markdown code fences, headings, notes, or commentary. Removing the inserted docstrings from the response must reproduce the original requested definitions exactly.

## Docstring structure

Use an indented, multiline, triple-double-quoted Google-style docstring with these parts in order:

1. One-line summary
2. `Args:` when applicable
3. `Returns:` when applicable
4. `Raises:` when applicable
5. `Examples:`

Separate the summary and every included section with exactly one blank line. Put the closing triple quotes on their own line, immediately before the original first statement. Do not leave a blank line between them.

Use ordinary `"""` delimiters unless the docstring contains backslashes that Python would interpret as escapes. In that case, use `r"""`.

## Summary

Write one imperative sentence describing the function's behavior as implemented.

Begin with the capitalized form of exactly one approved verb:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

Derive the behavior from the signature and complete body, not merely the function's name. Do not repeat the signature, describe unsupported behavior, mention these instructions, or include review notes.

## Args section

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every eligible parameter exactly once and in signature order. Use its exact identifier and never invent a parameter.

For an annotated parameter, use:

    name (annotation): Description.

Copy the annotation text exactly as written in the signature. Do not simplify, expand, qualify, or infer another type.

For an unannotated parameter, use:

    name: Description.

Describe the parameter's actual role, supported values, relevant constraints, and any default that changes behavior. Follow the implementation rather than assumptions suggested by the parameter name. If invalid input returns `False`, `None`, or another sentinel, describe that behavior instead of claiming it raises an exception.

## Returns section

Include `Returns:` when the function returns a value, yields values, or returns a generator or iterator object.

For an annotated return, use:

    annotation: Description.

Copy the return annotation exactly from the signature. Describe the actual result, including parameter-controlled variants and sentinel results for invalid input.

For a generator or iterator, describe the values it produces, their order, and relevant endpoint behavior. Do not describe exceptions as return values.

Omit `Returns:` only when the function has no value-returning or yielding behavior.

## Raises section

Document all and only exceptions produced by explicit `raise` statements in the complete named function definition.

Inspect nested helpers defined inside the named function. Include an exception explicitly raised by a nested helper when the named function invokes that helper or exposes its execution through a returned generator or iterator.

For each applicable exception type, use:

    ExceptionType: Exact condition that triggers the explicit raise.

Document each exception type once. Combine all triggering conditions when multiple explicit branches raise the same type.

Do not infer a `Raises:` entry from:

- Parameter annotations, function names, or validation-like behavior.
- Calls to separately defined functions.
- Operators, conversions, parsing, regular expressions, or library calls.
- Exception types appearing only in `except` clauses.
- Invalid inputs handled by returning a sentinel.
- Incidental runtime errors that have no explicit `raise` statement.

Omit `Raises:` when there is no applicable explicit `raise`. Never add an entry such as “Not applicable.”

## Examples section

Every named function must have its own `Examples:` section containing at least one runnable `>>>` doctest that directly calls that function.

Construct and verify each function's examples independently. Every doctest must:

- Call the function whose docstring contains it.
- Use the function's exact name and pass only parameters accepted by its signature.
- Use inputs supported by the implementation.
- Run in the module's normal doctest namespace without imports, files, network access, user interaction, or unstated setup.
- Match Python's displayed output exactly, including capitalization, quoting, collection syntax, ordering, and exception formatting.
- Avoid duplicate calls unless they demonstrate meaningfully different behavior.

Use literal expected output only when the implementation guarantees that exact result.

For random, UUID-generating, time-dependent, environment-dependent, or otherwise variable results, call the function once, assign its result, and test deterministic properties guaranteed by the implementation, such as type, length, format, range, or character set. Never invent a particular variable result.

For example, use this pattern with the actual function and its guaranteed invariant:

    >>> result = function_name(valid_argument)
    >>> isinstance(result, str)
    True
    >>> len(result) == guaranteed_length
    True

For a generator or iterator, consume it with an operation such as `list(...)` only when the chosen inputs guarantee finite execution and an exactly predictable sequence.

Prefer a successful deterministic example. If an example intentionally raises, reproduce the complete doctest traceback output and exception message exactly.

## Final verification

Check each named function independently before returning the response:

- The complete original definition appears in the requested position.
- Its decorators, signature, annotations, nested definitions, indentation, quoting, and executable statements are unchanged.
- Its docstring is the first body statement and the only inserted content.
- Its summary starts with an approved capitalized verb and ends with valid punctuation.
- Every eligible parameter is documented once, in signature order.
- Every documented annotation exactly matches the signature.
- `Returns:` matches all value-returning, yielding, and generator-returning behavior.
- `Raises:` includes every applicable explicit raise and no inferred exception.
- `Examples:` directly calls the correct function using its real signature.
- Every doctest is runnable and every expected result is guaranteed by the implementation.
- No variable output is presented as a fixed value.
- Removing the docstrings leaves the original requested definitions verbatim.
- The response contains no imports, unrelated definitions, placeholders, code fences, or commentary.