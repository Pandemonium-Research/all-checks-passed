---
name: docstring-api
description: Use when adding complete Google-style docstrings and runnable doctests to specified public Python functions without changing their signatures or executable code.
---

# Add docstrings to selected public functions

## Required output

Return only the complete definitions of the named public functions, in the order requested.

For each named function:

1. Copy its signature and full body verbatim.
2. Insert one docstring as the first statement in the body.
3. Preserve every executable statement, comment, annotation, default value, and line of control flow.
4. Include any decorator attached to the function.
5. Do not include imports, constants, unrelated functions, code fences, explanations, or placeholder bodies such as `...` or `pass`.

The added docstring is the only permitted change.

## Docstring structure

Use one multiline, triple-double-quoted Google-style docstring. The summary, all section headings, all entries, and all doctests must remain inside the same pair of triple quotes. Do not close the docstring before the sections.

Indent the docstring to the function-body level. Indent section entries one additional level:

    """Generate a deterministic description of the result.

    Args:
        parameter (annotation): Explain its meaning and behavior.

    Returns:
        annotation: Explain the returned value.

    Raises:
        ExceptionType: Explain the exact condition that raises it.

    Examples:
        >>> expression_using_the_function()
        expected_output
    """

Treat this only as a layout pattern. Replace every placeholder with facts derived from the actual function.

Use exactly one blank line between the summary and each section and between consecutive sections. Do not insert a blank line between the closing triple quotes and the first executable statement. If the docstring contains a backslash, use a raw docstring beginning with `r"""`.

Include only applicable sections, in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is always required. Do not emit an empty `Args:`, `Returns:`, or `Raises:` section.

## Summary

Begin immediately after the opening triple quotes with a one-line imperative summary.

The summary must:

- Start with one of these words, capitalized exactly as shown: `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.
- End with `.`, `!`, or `?`.
- Describe the function's observable purpose accurately.
- Not repeat the function signature.
- Not claim behavior that is absent from the implementation.

Any additional description must also remain inside the docstring and must agree with the function body.

## Arguments

Add `Args:` when the signature has parameters other than `self` or `cls`.

Document every applicable parameter exactly once and in signature order. Use the parameter name and annotation exactly as written in the signature:

- Annotated parameter: `name (annotation): description`
- Unannotated parameter: `name: description`

Do not simplify, expand, or invent a type. For example, preserve annotation text such as `Any`, `Optional[List[str]]`, or `Generator` exactly rather than substituting another spelling.

Each description must explain what the parameter controls, including relevant default behavior, accepted ranges, or special flag behavior that is evident from the code. Do not document names that are not parameters.

## Return values

Add `Returns:` when the function returns a value. Use:

`annotation: description`

The type text must match the return annotation exactly. If no return annotation exists, describe the return value without inventing an annotated type.

Describe all possible returned values and the conditions that distinguish them. For Boolean results, state what makes the result true and what makes it false. For a returned iterator or generator, describe the values it yields. Do not add `Returns:` to a function that has no value return.

## Explicit exceptions

Add `Raises:` only when the supplied function definition contains an explicit `raise` statement.

Document every explicitly raised exception type exactly once:

`ExceptionType: condition`

State the precise condition that reaches the corresponding `raise`. Inspect the entire function body, including local helper functions defined within it. Do not list exceptions merely because an operation or called function could raise them, and do not treat exceptions named only in an `except` clause as explicitly raised.

## Runnable doctests

Every named function must have an `Examples:` section containing at least one `>>>` doctest that directly calls that function.

Each doctest must:

- Be valid in the function's module context.
- Finish successfully.
- Show every output line produced by the expression.
- Have expected output that matches exactly.
- Avoid relying on time, randomness, machine state, network access, memory addresses, or iteration order that is not guaranteed.

For nondeterministic results, test a deterministic property such as the result's type, length, shape, alphabet, or other invariant. Do not invent a sample random value and present it as exact output. Materialize iterators when necessary so their values, rather than an unstable object representation, are checked.

## Final verification

Before returning the definitions, verify for every named function that:

- Its signature is unchanged.
- Its entire executable body is present and unchanged.
- The docstring is the first body statement.
- The summary follows the required wording and punctuation rules.
- Every parameter is documented once, in order, with its exact annotation.
- Every returned value is documented with the exact return annotation.
- Every explicit `raise` is documented, with no speculative exceptions added.
- At least one deterministic, runnable doctest calls the function.
- All sections and examples are inside the docstring.
- No unrelated source or surrounding explanation is included.