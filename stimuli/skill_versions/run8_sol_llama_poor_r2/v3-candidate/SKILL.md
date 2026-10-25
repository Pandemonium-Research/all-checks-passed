---
name: docstring-api
description: Use when adding complete Google-style docstrings and deterministic, runnable doctests to named public Python functions while preserving their signatures and executable source exactly.
---

# Add docstrings to selected public functions

## Required output

Return only the complete definitions of the named public functions, in the requested order.

For each named function:

1. Copy its decorators, signature, and full body from the supplied module.
2. Insert one docstring as the first statement in the body.
3. Preserve all original source outside the inserted docstring verbatim, including annotations, defaults, string literals, comments, nested definitions, executable statements, and control flow.
4. Include the complete body. Never substitute `...`, `pass`, or another placeholder.
5. Do not include imports, constants, unrelated functions, Markdown fences, or explanatory text.

The inserted docstring is the only permitted source change. Do not reformat, simplify, repair, or otherwise rewrite the supplied code.

## Docstring structure

Use one multiline, triple-double-quoted Google-style docstring. Keep the summary, section headings, entries, and doctests inside the same pair of triple quotes.

Indent the docstring at the function-body level. Indent every section entry by four additional spaces.

Use exactly one blank line between the summary and the first section and between consecutive sections. Do not insert a blank line between the closing triple quotes and the original first statement.

If the docstring contains a backslash, make it a raw docstring beginning with `r"""`.

Include only applicable sections, in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is required for every named function. Never emit an empty `Args:`, `Returns:`, or `Raises:` section.

Do not copy generic instructional wording into a docstring. Phrases such as “Explain its meaning,” “Describe the result,” or “Generate a deterministic description” are placeholders, not valid documentation. Every description must state concrete behavior derived from the supplied implementation.

## Summary

Begin immediately after the opening triple quotes with a one-line imperative summary.

The summary must:

- Start with one of these words, capitalized exactly as shown: `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.
- End with `.`, `!`, or `?`.
- State the function's actual observable purpose.
- Not repeat the signature.
- Not claim behavior absent from the implementation.

Any additional description must remain inside the docstring and agree with the implementation.

## Arguments

Add `Args:` when the signature contains parameters other than `self` or `cls`. Do not document `self` or `cls`.

Document every other parameter exactly once and in signature order:

- Annotated parameter: `name (annotation): description`
- Unannotated parameter: `name: description`

Copy each parameter name and annotation exactly from the signature. Do not simplify, expand, normalize, or invent types.

Describe what the parameter controls. Include defaults, accepted ranges, flag behavior, units, and other constraints when they are evident from the implementation. Distinguish input size from output size when the implementation transforms one into the other.

Do not document local variables or names that are not parameters.

## Return values

Add `Returns:` only when the function returns a value.

When a return annotation exists, format the entry as:

`annotation: description`

Copy the annotation exactly from the signature. When no return annotation exists, describe the returned value without inventing a type label.

Describe every possible returned result and the conditions selecting it:

- For `bool`, state both the condition producing `True` and the condition producing `False`.
- For a representation controlled by a flag, describe every representation and its corresponding flag value.
- For an iterator or generator, describe the yielded values, their order, step behavior, and endpoint behavior evident from the implementation.
- For generated data, describe guaranteed properties such as length, alphabet, encoding, or format.

Do not add `Returns:` when the function has no value return.

## Explicit exceptions

Add `Raises:` only if the supplied function definition contains an explicit `raise` statement, including a `raise` inside a local helper defined by that function.

Document every explicitly raised exception type exactly once:

`ExceptionType: precise condition`

Trace the branch that reaches each `raise` and state its complete condition. Include combined type, range, direction, and configuration checks when applicable.

Do not list an exception merely because:

- Its name appears in an `except` clause.
- The function catches it and returns, continues, or falls through.
- A called function or operation could raise it.
- The annotation or implementation makes it seem plausible.

Exceptions named only in `except` clauses do not belong in `Raises:`.

## Runnable doctests

Every named function must contain an `Examples:` section with at least one `>>>` doctest that calls that function.

Before including a doctest, determine exactly what the expression prints. Every expected-output line must match that output.

Each doctest must:

- Be valid in the supplied module's context without adding imports to the response.
- Complete successfully.
- Call the documented function.
- Show all output produced by the expression.
- Use stable inputs.
- Materialize an iterator or generator when verifying its yielded values.
- Avoid nonterminating or invalid control-flow paths.
- Avoid dependence on time, randomness, machine state, network access, memory addresses, or unspecified iteration order.

For a nondeterministic result, test a guaranteed deterministic invariant instead of showing the generated value. Suitable invariants include:

- The result's type.
- Its exact length.
- Its required punctuation or structural shape.
- Whether every character belongs to the implementation's alphabet.
- A combination of guaranteed properties.

The expected result of such a predicate is commonly `True`.

Never present a guessed, observed, illustrative, or placeholder random value as exact doctest output. Do not use repeated placeholder characters. Do not use ellipsis matching unless the supplied module explicitly enables it.

For deterministic functions, use inputs whose exact result follows from the implementation.

## Final verification

Before returning the definitions, verify every named function against both checklists.

### Source preservation

- The decorators and signature are unchanged.
- The docstring is the first body statement.
- Every original body line remains present and in the same order.
- No statement, literal, comment, nested definition, or control-flow branch was changed.
- The full body is included without placeholders.
- No import, constant, unrelated definition, Markdown fence, or explanation was added.

### Documentation completeness

- The summary uses an allowed opening word and required punctuation.
- All descriptions contain implementation-derived facts rather than generic placeholders.
- Every applicable parameter is documented once, in order, with its exact annotation.
- Every returned value is documented with the exact return annotation.
- Every explicit `raise` is documented exactly once.
- Exceptions appearing only in `except` clauses are omitted.
- Every named function has a deterministic, runnable doctest that calls it.
- Nondeterministic output is checked through guaranteed invariants rather than an invented value.
- All sections and examples remain inside the docstring.
- The final response contains only the requested complete function definitions, in the requested order.