---
name: docstring-api
description: Use when adding complete Google-style docstrings and deterministic, runnable doctests to specified public Python functions while preserving their signatures and all existing source.
---

# Add docstrings to selected public functions

## Required output

Return only the complete definitions of the named public functions, in the requested order.

For each named function:

1. Copy every attached decorator, the signature, and the complete function body from the supplied module.
2. Insert one docstring as the first statement in the function body.
3. Preserve all original source outside the inserted docstring verbatim, including annotations, defaults, comments, string literals, nested definitions, executable statements, indentation, and control flow.
4. Include the full body. Never replace code with `...`, `pass`, or another placeholder.
5. Exclude imports, constants, unrelated definitions, Markdown fences, and explanatory text.

The inserted docstring is the only permitted source change. Do not reformat, simplify, repair, or otherwise rewrite the supplied code.

## Docstring structure

Use one multiline, triple-double-quoted Google-style docstring. Keep the summary, section headings, entries, and doctests inside the same pair of triple quotes.

Indent the docstring at the function-body level and each section entry by four additional spaces. Use exactly one blank line between the summary and the first section and between consecutive sections. Do not insert a blank line between the closing triple quotes and the original first statement.

If the docstring contains a backslash, make it a raw docstring beginning with `r"""`.

Include only applicable sections, in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is required for every named function. Never emit an empty `Args:`, `Returns:`, or `Raises:` section.

Write every description from facts established by the implementation. Do not copy instructional phrases into the result. Text such as “Explain its meaning,” “Describe the result,” “expected output,” or “Generate a deterministic description” is a placeholder, not documentation.

## Summary

Begin immediately after the opening triple quotes with a one-line imperative summary.

The summary must:

- Start with one of these words, capitalized exactly as shown: `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.
- End with `.`, `!`, or `?`.
- Describe the function's observable purpose accurately.
- Not repeat the function signature.
- Not claim behavior absent from the implementation.

Any additional description must remain inside the docstring and agree with the function body.

## Arguments

Add `Args:` when the signature contains parameters other than `self` or `cls`. Do not document `self` or `cls`.

Document every other parameter exactly once and in signature order:

- Annotated parameter: `name (annotation): description`
- Unannotated parameter: `name: description`

Copy each parameter name and annotation exactly from the signature. Do not simplify, expand, normalize, or invent type text. A default value does not alter the annotation: describe the default in prose instead of adding labels such as `optional` to the type.

Explain what each parameter controls. Include default behavior, accepted ranges, units, flag behavior, and other constraints when the implementation establishes them. Distinguish input quantities from output quantities when an encoding or transformation changes the size.

Do not document local variables or names that are not parameters.

## Return values

Add `Returns:` when the function returns a value.

When a return annotation exists, use:

`annotation: description`

Copy the annotation exactly from the signature. When no return annotation exists, describe the returned value without inventing a type label.

Trace every return path and describe all possible results and the conditions selecting them. In particular:

- For `bool`, state both what produces `True` and what produces `False`.
- For a representation selected by a flag, describe each representation and the corresponding flag value.
- For generated data, state guaranteed properties such as length, alphabet, encoding, separators, or format.
- For an iterator or generator, describe the yielded values, their order, step behavior, and endpoint behavior established by the code.

Do not add `Returns:` when the function has no value return.

## Explicit exceptions

Add `Raises:` only when the supplied function definition contains an explicit `raise` statement, including a `raise` inside a local helper defined by that function.

Document every explicitly raised exception type exactly once:

`ExceptionType: precise condition`

Trace the branch leading to each `raise` and state its complete condition, including relevant type checks, bounds, sign handling, direction, and combinations of conditions.

Do not list an exception merely because:

- Its name appears in an `except` clause.
- The function catches it and returns, continues, or falls through.
- A called function or operation could raise it.
- Its annotation or surrounding code makes it seem possible.

Before finishing, compare the `Raises:` entries directly with the explicit `raise` statements. An exception type found only in an `except` clause must be omitted.

## Runnable doctests

Every named function must have an `Examples:` section containing at least one `>>>` doctest that calls that function.

Determine exactly what each doctest expression displays before including it. Every expected-output line must match Python's displayed output exactly.

Each doctest must:

- Run in the supplied module's context without requiring imports in the response.
- Complete successfully.
- Call the documented function.
- Show every output line produced by the expression.
- Use stable inputs.
- Avoid dependence on time, randomness, machine state, network access, memory addresses, or unspecified iteration order.
- Materialize an iterator or generator when checking yielded values.
- Use a terminating generator configuration whose endpoint is reachable.

Never display a generated random, secure, UUID-like, or otherwise nondeterministic value as exact expected output. This includes guessed samples, values observed during one run, and repeated placeholder characters.

Instead, call the function in a deterministic property check. Check only invariants guaranteed by the implementation, such as:

- The returned type.
- The exact length.
- Required separators or structural shape.
- Membership of every character in the implemented alphabet.
- A conjunction of guaranteed properties.

If one generated result must be checked more than once, assign the function result on a `>>>` line, which produces no output, and then display the result of deterministic predicates on subsequent lines. Account for transformations precisely, such as the relationship between source bytes and encoded output characters.

Do not use ellipsis matching unless the supplied module explicitly enables it.

For deterministic functions, choose inputs whose exact displayed result follows directly from the implementation.

## Final verification

Before returning the definitions, perform both checks.

### Source preservation

Remove only the inserted docstrings mentally and confirm that the supplied definitions are recovered verbatim:

- Every decorator and signature is unchanged.
- Every original body line remains present and in the same order.
- No statement, literal, comment, nested definition, or control-flow branch was changed.
- Every complete body is present without placeholders.
- No import, constant, unrelated definition, Markdown fence, or explanation was added.
- The definitions appear in the requested order.

### Documentation completeness

For every named function, confirm that:

- The summary uses an allowed opening word and required punctuation.
- No generic instructional or placeholder wording remains.
- Every applicable parameter appears once, in signature order, with its exact annotation.
- Defaults and constraints are described in prose rather than added to annotation labels.
- Every returned result is documented with the exact return annotation.
- Every explicit `raise` is documented exactly once with its complete condition.
- Exceptions appearing only in `except` clauses are omitted.
- At least one deterministic, runnable doctest calls the function.
- No nondeterministic value is presented as exact output.
- Every iterator doctest terminates and materializes the yielded values.
- All sections and examples remain inside the docstring.
- The final response contains only the requested complete function definitions.