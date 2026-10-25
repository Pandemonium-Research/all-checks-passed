---
name: docstring-api
description: Use this guide to add complete Google-style docstrings and runnable doctests to named public Python functions without changing their signatures, executable code, or requested order.
---

# Add docstrings to named public functions

## Required output

Return only the complete definitions of the named public functions, in the order requested.

For every named function:

- Copy its decorators, signature, annotations, and complete body verbatim.
- Insert exactly one docstring as the first statement in its body.
- Preserve every existing executable statement, including nested function definitions.
- Do not add docstrings to nested functions unless they are also named in the request.
- Do not add, remove, reorder, rewrite, or reformat executable code.
- Never replace any part of a body with `...`, `pass`, a comment, or another placeholder.

Do not output imports, unrelated definitions, Markdown code fences, headings, notes, or explanatory text.

## Docstring layout

Use an indented, multiline, triple-double-quoted Google-style docstring with these sections in this order when applicable:

1. One-line summary
2. `Args:`
3. `Returns:`
4. `Raises:`
5. `Examples:`

Separate the summary and every included section with exactly one blank line. Put the closing triple quotes on their own line, followed immediately by the function's original first statement with no intervening blank line.

Use ordinary `"""` delimiters unless the docstring itself contains backslashes that Python would interpret. In that case, use `r"""`.

## Summary

Write one imperative sentence describing the function's actual behavior.

Begin with the capitalized form of exactly one approved verb:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

Do not repeat the signature or include instructions, review notes, implementation details, or claims that the body does not support.

## Args section

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every such parameter exactly once and in signature order. Use the exact parameter name and no invented parameters.

For an annotated parameter, write:

    name (annotation): Description.

Copy the annotation text exactly from the signature. Do not simplify, expand, qualify, or infer another type.

For an unannotated parameter, write:

    name: Description.

Describe the parameter's role, accepted values, relevant constraints, and any default that changes behavior. Derive these details from the signature and body rather than assuming conventional behavior from the function's name.

## Returns section

Include `Returns:` if any path explicitly returns a value or the function returns a generator or other constructed value.

For an annotated return, write:

    annotation: Description.

Copy the return annotation exactly from the signature. Describe the actual result and any variations controlled by parameters.

Omit `Returns:` only when the function has no value-returning behavior. Do not describe raised exceptions as return values.

## Raises section

Include only exceptions produced by explicit `raise` statements in the named function's source, including explicit raises inside nested helpers defined and used by that function.

For each explicitly raised exception type, write:

    ExceptionType: Exact condition that triggers the explicit raise.

Document each exception type once. If several explicit branches raise the same type, combine all their triggering conditions in that entry.

Do not infer exceptions from type annotations, validation-like names, calls to other functions, operators, parsing operations, library behavior, or caught exceptions. A function that returns `False` for invalid input does not raise an exception unless its source contains a corresponding explicit `raise`.

Omit `Raises:` when there is no explicit raise statement. Never add entries such as “not applicable.”

## Examples section

Every named function must have its own `Examples:` section containing at least one runnable `>>>` doctest that directly calls that function.

Each doctest must:

- Use the function's real signature and pass only parameters it accepts.
- Use inputs permitted by the implementation.
- Run in the module's normal doctest namespace without imports, files, network access, user interaction, or unstated setup.
- Match Python's displayed values, capitalization, quoting, collection syntax, and exception formatting exactly.
- Avoid redundant duplicate calls unless separate calls demonstrate meaningfully different behavior.

Use direct expected output only for deterministic results.

Never invent or hard-code the output of random, UUID-generating, time-dependent, environment-dependent, or otherwise variable functions. Instead, test stable properties. For example:

    >>> result = function_name(valid_argument)
    >>> isinstance(result, str)
    True
    >>> len(result) == expected_length
    True

When testing a generator or iterator, consume it with a deterministic operation such as `list(...)` only when the resulting sequence is finite and exactly predictable.

## Final verification

Check every named function independently before returning the response:

- The complete original definition is present in the requested position.
- Its signature, decorators, annotations, and executable statements are unchanged.
- Its docstring is the first body statement and is the only inserted content.
- Its summary begins with an approved capitalized verb and ends with valid punctuation.
- Every eligible parameter appears once, in order, with its annotation copied exactly.
- `Returns:` matches the function's actual value-returning behavior.
- `Raises:` matches all and only explicit raise statements.
- Its doctest calls the correct function with the correct signature.
- Variable results are checked through deterministic properties rather than fabricated output.
- The response contains no code fences, imports, unrelated definitions, placeholders, or commentary.