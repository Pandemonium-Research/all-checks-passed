---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to specified public Python functions while preserving their signatures, executable code, and output order. Use when a correct module has named public functions without docstrings and the response must contain only their full updated definitions.
---

# Add API docstrings

Inspect every named function in the source module before writing the response. For each function,
record its parameters in signature order, return behavior, explicit `raise` statements, and a
deterministic call suitable for a doctest.

## Preserve the source

Return exactly one complete definition for each named public function, in the order requested.
Include any attached decorators and the entire function body. Copy all existing source text
verbatim and make exactly one change: insert the docstring as the first statement in the function
body.

Do not change signatures, annotations, defaults, decorators, comments, executable statements, or
formatting. Do not fix or refactor the code. Never replace any part of a body with `...`, a new
`pass`, or another placeholder.

Return only the function definitions. Do not include imports, unrelated definitions, Markdown
fences, explanatory text, or a second copy of any function.

## Format each docstring

Use an indented, multiline, triple-double-quoted Google-style docstring. Put the summary on the
same line as the opening quotes:

    """Check whether the value satisfies the condition.

Put the closing quotes on their own line. Do not leave a blank line between the closing quotes and
the original first executable statement. Use a raw triple-double-quoted docstring when its text
contains backslashes.

Write a one-line imperative summary that:

- Starts with exactly one of these capitalized words: `Add`, `Build`, `Check`, `Clip`, `Compress`,
  `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`,
  `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`,
  `Transform`, or `Validate`.
- Ends with `.`, `!`, or `?`.
- Describes the function's behavior without repeating its signature.

After the summary, include applicable sections in exactly this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between consecutive
sections. Indent section entries four spaces beyond their labels. Never insert an empty or
inapplicable section. `Examples:` is always applicable and therefore mandatory for every named
function.

## Document arguments exactly

In `Args:`, document every parameter except `self` and `cls`, in signature order. Use each
parameter's exact name and add no other names.

For an annotated parameter, use:

    name (annotation): Description.

Copy the annotation text exactly from the signature; do not simplify, normalize, or infer it.
For an unannotated parameter, use:

    name: Description.

Do not include the default value in the type. Make each description explain the parameter's role
or accepted meaning rather than merely restating its name. Omit `Args:` only when the function has
no parameters other than `self` or `cls`.

## Document returns from body evidence

Include `Returns:` when the function returns a value. Describe all possible returned values and
what they mean.

For an annotated return value, use:

    annotation: Description.

Copy the return annotation exactly from the signature. If the return value is unannotated, write
only its description and do not invent a type. Omit `Returns:` when the function has no
value-returning path; a bare `return` does not return a documented value.

## Document only explicit raises

In `Raises:`, list every exception type explicitly raised by a `raise` statement in that
function's own body. Use:

    ExceptionType: Condition that causes the exception.

Do not list exceptions merely caught by `except`, exceptions that called helpers might raise, or
exceptions inferred from operations. Omit `Raises:` if the function contains no explicit raise.

## Add a runnable doctest to every function

Every named function must have its own `Examples:` section containing at least one `>>>` prompt.
A section containing only prose does not satisfy this requirement.

The doctest must directly exercise the function whose docstring contains it and must run in the
original module's namespace. Supply valid arguments, and include the exact expected output for
every expression that displays a result. Prefer a simple deterministic call. If the concrete
result varies, test a deterministic property of the result instead. Do not use pseudocode,
placeholders, omitted setup, or output that only looks plausible.

## Validate before responding

Do not return the result until all checks pass:

- Every requested function appears exactly once and in the requested order.
- Every definition includes its full original body.
- Removing the added docstrings would reproduce the original definitions verbatim.
- Every parameter except `self` and `cls` appears once in `Args:` and in signature order.
- `Returns:` agrees with the function's value-returning behavior.
- `Raises:` exactly matches the function's explicit `raise` statements.
- Every function has `Examples:` with at least one runnable `>>>` doctest.
- The definitions parse successfully and every doctest passes with exact output.
- The response contains only the completed definitions, with no Markdown fence or commentary.