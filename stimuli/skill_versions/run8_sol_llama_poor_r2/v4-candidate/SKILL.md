---
name: docstring-api
description: Use when adding complete Google-style docstrings and runnable doctests to specified public Python functions while preserving all supplied source except the inserted docstrings.
---

# Add docstrings to selected public functions

## Required output

Return only the complete definitions of the named public functions, in the requested order.

For each named function:

1. Copy every attached decorator, the signature, and the full body from the supplied module.
2. Insert one docstring as the first statement in the function body.
3. Preserve all other source verbatim, including annotations, defaults, comments, string literals, nested definitions, executable statements, and control flow.
4. Include the complete function body. Never replace code with `...`, `pass`, or another placeholder.
5. Exclude imports, constants, unrelated definitions, Markdown fences, and explanatory text.

The inserted docstring is the only permitted change. Do not repair, simplify, reformat, or otherwise rewrite the supplied code.

## Docstring structure

Use one multiline, triple-double-quoted Google-style docstring. Keep the summary, section headings, entries, and doctests inside the same pair of triple quotes.

Indent the docstring at the function-body level and each section entry by four additional spaces. Use exactly one blank line between the summary and the first section and between consecutive sections. Do not add a blank line between the closing triple quotes and the original source that follows it.

If the docstring contains a backslash, use a raw docstring beginning with `r"""`.

Include only applicable sections, in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is required for every named function. Never emit an empty `Args:`, `Returns:`, or `Raises:` section.

Write concrete documentation directly from the implementation. Never emit instructional or placeholder text such as “Explain its meaning,” “Describe the result,” “expected output,” or “Generate a deterministic description.”

## Summary

Begin immediately after the opening triple quotes with a one-line imperative summary.

The summary must:

- Start with one of these words, capitalized exactly as shown: `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.
- End with `.`, `!`, or `?`.
- State the function's observable purpose.
- Not repeat the signature.
- Not claim behavior absent from the implementation.

Any additional description must remain inside the docstring and agree with the implementation.

## Arguments

Add `Args:` when the signature contains parameters other than `self` or `cls`. Do not document `self` or `cls`.

Document every other parameter exactly once and in signature order:

- Annotated parameter: `name (annotation): description`
- Unannotated parameter: `name: description`

Copy the parameter name and annotation text exactly from the signature. A default does not change the annotation: for example, a parameter annotated `bool` must be labeled `(bool)`, not `(bool, optional)`. Describe its default in prose instead.

Explain what each parameter controls. Include default behavior, accepted ranges, units, flag behavior, and other constraints when the implementation establishes them. Preserve distinctions such as input bytes versus output characters. Do not document local variables or invent constraints that the code does not enforce.

## Return values

Add `Returns:` when the function returns a value.

If a return annotation exists, format the entry as:

`annotation: description`

Copy the return annotation exactly from the signature. If no return annotation exists, describe the value without inventing a type label.

Trace every return path and describe:

- Every possible result and the conditions selecting it.
- Both the `True` and `False` conditions for a Boolean result.
- Each representation selected by a flag.
- Guaranteed length, alphabet, encoding, or format for generated data.
- The values, order, step behavior, and endpoint behavior of an iterator or generator.

Do not add `Returns:` to a function that has no value return. Do not describe a caught exception or fall-through path as a raised error.

## Explicit exceptions

Add `Raises:` only when the supplied definition contains an explicit `raise` statement, including one inside a local helper defined by the named function.

Document every explicitly raised exception type exactly once:

`ExceptionType: precise condition`

For each explicit `raise`, trace the complete Boolean condition that can reach it. Preserve distinctions involving type checks, inclusive or exclusive bounds, absolute values, step direction, and combinations of conditions.

An exception does not belong in `Raises:` merely because:

- Its name appears in an `except` clause.
- The function catches it and returns, continues, or falls through.
- A called function or operation could raise it.
- Its annotation or surrounding code makes it seem plausible.

Before finishing, compare the listed exception types with the function's actual `raise` statements. Types found only after `except` must be omitted.

## Runnable doctests

Every named function must have an `Examples:` section containing at least one `>>>` line that calls that function, either directly or inside a deterministic expression.

Determine the exact result of each doctest before including it. Every expected-output line must match Python's displayed output exactly.

Each doctest must:

- Be valid in the supplied module's context without adding imports to the response.
- Finish successfully.
- Call the documented function.
- Show all output produced by the expression.
- Use stable inputs.
- Avoid time, machine state, network access, memory addresses, and unspecified iteration order.
- Materialize an iterator or generator when checking its yielded values.
- Avoid a generator configuration that skips its stopping value or otherwise fails to terminate.

For a nondeterministic function, never show the generated value itself as exact expected output. This prohibition includes observed samples, plausible UUIDs or tokens, repeated placeholder characters, and guessed random strings.

Instead, call the function inside an expression that checks a property guaranteed by its implementation, such as:

- The returned type.
- The exact output length.
- Required separators or structural shape.
- Whether every character belongs to the implemented alphabet.
- A conjunction of guaranteed properties.

Use the actual relationship established by the code; for example, distinguish the number of source bytes from the number of encoded output characters. The predicate's expected result is usually `True`.

If several properties require storing one generated result, the assignment may call the function without expected output, followed by a predicate whose output is shown. Do not use ellipsis matching unless the supplied module explicitly enables it.

For deterministic functions, choose inputs whose exact displayed result follows directly from the implementation.

## Final verification

Perform both checks before returning the answer.

### Source preservation

Remove only the inserted docstrings mentally and confirm that the supplied definitions are recovered verbatim:

- Every decorator and signature is unchanged.
- Every original body line remains present and in the same order.
- No statement, literal, comment, nested definition, or control-flow branch was changed.
- Each full body is present without placeholders.
- No import, constant, unrelated definition, Markdown fence, or explanation was added.
- The definitions appear in the requested order.

### Documentation completeness

For every named function, confirm that:

- The summary uses an allowed opening word and required punctuation.
- No placeholder or generic instructional wording remains.
- Every applicable parameter appears once, in order, with its exact annotation text.
- Defaults and constraints are described in prose rather than added to annotation labels.
- Every return path is documented with the exact return annotation.
- Every explicit `raise` is documented exactly once with its complete condition.
- Exceptions appearing only in `except` clauses are omitted.
- At least one deterministic, runnable doctest calls the function.
- No nondeterministic value is presented as exact output.
- Every iterator doctest terminates and materializes the returned values.
- All sections and examples remain inside the docstring.
- The final response contains only the requested complete function definitions.