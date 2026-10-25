---
name: docstring-api
description: Use when adding complete Google-style docstrings and deterministic, runnable doctests to specified public Python functions while preserving their signatures and executable source exactly.
---

# Add docstrings to selected public functions

## Required output

Return only the complete definitions of the named public functions, in the requested order.

For each named function:

1. Copy its decorator, signature, and full body from the supplied module.
2. Insert one docstring as the first statement in the body.
3. Preserve every existing executable statement, nested definition, comment, annotation, default value, string literal, and control-flow branch verbatim.
4. Include the complete body. Never replace code with `...`, `pass`, or another placeholder.
5. Do not include imports, constants, unrelated functions, Markdown fences, or explanatory text.

The added docstring is the only permitted source change.

## Docstring format

Use one multiline, triple-double-quoted Google-style docstring. Keep the summary, descriptions, section headings, entries, and doctests inside the same pair of triple quotes.

Indent the docstring at the function-body level and section contents by four additional spaces:

    """Describe the observable operation.

    Args:
        parameter (annotation): Describe what the parameter controls.

    Returns:
        annotation: Describe the returned value.

    Raises:
        ExceptionType: Describe the exact condition reaching the raise.

    Examples:
        >>> expression_that_calls_the_function()
        expected_output
    """

This is a layout template only. Never copy its placeholder wording into an answer.

Use exactly one blank line between the summary and the first section and between consecutive sections. Do not add a blank line between the closing triple quotes and the original first statement.

If the docstring contains a backslash, use a raw docstring beginning with `r"""`.

Include only applicable sections, in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is required for every named function. Never emit an empty `Args:`, `Returns:`, or `Raises:` section.

## Summary

Begin immediately after the opening triple quotes with a one-line imperative summary.

The summary must:

- Start with one of these words, capitalized exactly as shown: `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.
- End with `.`, `!`, or `?`.
- State the function's actual observable purpose.
- Not repeat the signature.
- Not claim behavior absent from the implementation.

Do not use generic wording such as “Explain its meaning,” “Describe the result,” or “Generate a deterministic description.” Every sentence must contain concrete facts derived from the function.

## Arguments

Add `Args:` when the signature has parameters other than `self` or `cls`.

Document every applicable parameter exactly once, in signature order:

- Annotated parameter: `name (annotation): description`
- Unannotated parameter: `name: description`

Copy each parameter name and annotation text exactly from the signature. Do not simplify, expand, normalize, or invent types.

Describe what each parameter controls. Include defaults, accepted ranges, flag behavior, and other constraints when they are evident from the implementation. State those facts in prose; do not alter the parameter label by adding default syntax.

Do not document local variables or other names that are not parameters.

## Return values

Add `Returns:` only when the function returns a value.

For an annotated return, use:

`annotation: description`

Copy the return annotation exactly from the signature. If there is no return annotation, describe the value without inventing a type label.

Describe every possible returned result and the conditions selecting it:

- For `bool`, state both what produces `True` and what produces `False`.
- For an iterator or generator, describe the values it yields, their order, and endpoint behavior evident from the code.
- For output whose representation depends on a flag, describe each representation and the corresponding flag value.

Do not add `Returns:` to a function with no value return.

## Explicit exceptions

Add `Raises:` only if the supplied function definition contains an explicit `raise` statement, including one inside a local helper defined in that function.

Document every explicitly raised exception type exactly once:

`ExceptionType: precise condition`

Trace the actual branch leading to each `raise` and state its complete condition, including combined type and range checks where applicable.

Do not list an exception merely because:

- It appears in an `except` clause.
- It could be raised by an imported or called operation.
- Its type seems plausible from the annotations.
- The function catches it and returns or continues instead.

An exception named only in `except (...)` is not an explicitly raised exception.

## Runnable doctests

Every named function must contain an `Examples:` section with at least one `>>>` doctest that calls that function.

Before including a doctest, evaluate what its expression prints and ensure every expected-output line matches exactly.

Each doctest must:

- Be valid in the supplied module's context.
- Complete successfully.
- Call the documented function.
- Show all output produced by the expression.
- Use stable inputs.
- Avoid dependence on time, randomness, machine state, network access, memory addresses, or unspecified iteration order.
- Materialize an iterator or generator when checking its yielded values.
- Avoid invoking a nonterminating or invalid control-flow path.

Never invent exact output for a random or otherwise nondeterministic function. Instead, call it inside an expression that checks a deterministic invariant, such as:

- `isinstance(...)`
- `len(...) == expected_length`
- membership in a documented alphabet
- structural punctuation or shape
- a stable combination of such checks

The expected output for an invariant check is normally `True`. Ensure the invariant is guaranteed by the implementation for every successful run; a merely likely property is not acceptable.

Do not use placeholder output such as repeated `x` characters, an illustrative UUID, a guessed token, or one observed random result. Do not use ellipsis matching unless the module's doctest configuration explicitly enables it.

For deterministic functions, choose inputs whose exact result follows directly from the implementation. If a function returns an iterator or generator, convert it to a deterministic container such as `list(...)` when appropriate.

## Source-preservation check

After writing each docstring, compare the output definition with the supplied definition while ignoring only the inserted docstring. Confirm that:

- The decorator and signature are unchanged.
- All original body lines remain present and in the same order.
- No executable expression, literal, comment, or formatting-sensitive construct was rewritten.
- No import, constant, or unrelated definition was added.
- The docstring is the first body statement.
- The complete function body is included.

## Documentation check

For every named function, confirm that:

- The summary uses an allowed opening word and required punctuation.
- All descriptions contain concrete, implementation-derived facts rather than placeholders.
- Every parameter is documented once, in order, with its exact annotation.
- Every returned value is documented with the exact return annotation.
- Every explicit `raise` is documented exactly once.
- Exceptions appearing only in `except` clauses are omitted.
- At least one deterministic, runnable doctest calls the function.
- Nondeterministic output is tested through a guaranteed invariant rather than an invented value.
- All sections and examples remain inside the docstring.
- The final response contains only the requested complete function definitions.