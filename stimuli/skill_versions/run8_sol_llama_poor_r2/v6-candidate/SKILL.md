---
name: docstring-api
description: Use when adding complete Google-style docstrings and deterministic, runnable doctests to named public Python functions while preserving their signatures and executable code exactly.
---

# Add docstrings to selected public functions

## Required output

Return only the complete definitions of the named public functions, in the requested order.

For each function:

1. Copy every attached decorator, the signature, and the complete body verbatim.
2. Insert one docstring as the first statement in the body.
3. Preserve every original annotation, default, statement, literal, comment, nested definition, indentation level, and control-flow branch.
4. Include the full body; never substitute `...`, `pass`, or another placeholder.
5. Exclude imports, constants, unrelated definitions, Markdown fences, and explanatory text.

The inserted docstrings are the only permitted changes. Do not repair, reformat, simplify, or otherwise rewrite the supplied source.

## Docstring structure

Use one multiline, triple-double-quoted Google-style docstring. Keep the summary, sections, and doctests inside the same pair of triple quotes.

Indent the docstring at the function-body level and section entries one additional level. Use one blank line between the summary and the first section and between consecutive sections. Do not add a blank line between the closing triple quotes and the original first statement. If the docstring contains a backslash, use a raw docstring beginning with `r"""`.

Include only applicable sections, in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is required for every named function. Never include an empty `Args:`, `Returns:`, or `Raises:` section.

Write concrete documentation derived from the implementation. Never emit instructions or placeholders such as “Explain its meaning,” “Describe the result,” “expected output,” or “Generate a deterministic description.”

## Summary

Begin immediately after the opening triple quotes with a one-line imperative summary.

The summary must:

- Start with one of these words, capitalized exactly as shown: `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.
- End with `.`, `!`, or `?`.
- State the function’s observable purpose.
- Not repeat the signature.
- Not claim behavior absent from the implementation.

Any additional description must remain inside the docstring and agree with the implementation.

## Arguments

Add `Args:` when the signature contains parameters other than `self` or `cls`. Do not document `self` or `cls`.

Document every other parameter exactly once and in signature order:

- Annotated: `name (annotation): description`
- Unannotated: `name: description`

Copy each parameter name and annotation exactly from the signature. A default value does not change the annotation: for example, document a parameter annotated `bool` as `(bool)`, never `(bool, optional)`. Describe its default in prose.

Explain what the parameter controls and any default behavior, bounds, units, flag behavior, or other constraints established by the code. Do not invent constraints or document local variables.

## Return values

Add `Returns:` whenever the function returns a value.

When a return annotation exists, format the entry as:

`annotation: description`

Copy the annotation exactly from the signature. If no return annotation exists, describe the value without inventing a type label.

Trace every return path and document all possible results and the conditions selecting them. In particular:

- For a Boolean result, state both the `True` and `False` conditions.
- For formats selected by a flag, describe each format and its corresponding flag value.
- For generated data, state guaranteed properties such as length, alphabet, encoding, or separators.
- For an iterator or generator, describe the yielded values, order, step behavior, and endpoint behavior.

Do not add `Returns:` when the function has no value return.

## Explicit exceptions

Add `Raises:` only for explicit `raise` statements in the supplied definition, including explicit raises inside local helper functions.

Document each explicitly raised exception type exactly once:

`ExceptionType: precise condition`

Trace the complete condition that reaches each `raise`, including relevant type checks, bounds, sign handling, direction, and combined conditions.

Do not list an exception merely because:

- It appears in an `except` clause.
- The function catches it and returns or falls through.
- A called function or operation could raise it.
- It appears plausible from the surrounding code.

Before finishing, compare the `Raises:` entries directly with the function’s explicit `raise` statements. An exception named only in `except` must be omitted.

## Runnable doctests

Every named function must have an `Examples:` section with at least one `>>>` line that calls that function, directly or within a deterministic expression.

Every doctest must:

- Run successfully in the supplied module context without adding imports to the response.
- Show all output produced by the expression.
- Use expected output that matches Python’s displayed output exactly.
- Avoid dependence on time, randomness, machine state, network access, memory addresses, or unspecified iteration order.
- Materialize iterators and generators when checking their values.
- Use terminating inputs when testing a generator.

Never present a generated random, secure, UUID-like, or otherwise nondeterministic value as exact expected output. This includes guessed samples and repeated placeholder characters.

Instead, call the function in an expression that checks an invariant guaranteed by the implementation, such as the returned type, exact length, structural shape, separators, or character alphabet. If several checks require one result, assign it on a `>>>` line and test its properties on following lines. Account precisely for transformations such as bytes encoded into a different number of output characters.

Do not use ellipsis matching unless the supplied module explicitly enables it.

## Final verification

Before returning the answer, verify that:

- Removing only the inserted docstrings recovers the supplied definitions verbatim.
- Every decorator, signature, full body, nested definition, and original line remains unchanged and in order.
- Every summary follows the required opening-word and punctuation rules.
- No placeholder or generic instructional wording remains.
- Every applicable parameter appears once, in signature order, with its exact annotation.
- Every return path is documented with the exact return annotation.
- Every explicit `raise` is documented exactly once, and caught exceptions are not listed.
- Every function has a deterministic, runnable doctest that calls it.
- No nondeterministic value is shown as exact output.
- Every iterator doctest terminates and materializes its values.
- All docstring sections and examples remain inside the triple quotes.
- The response contains only the requested complete function definitions, without Markdown fences or explanation.