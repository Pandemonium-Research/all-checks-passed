---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to specified public Python functions without changing their existing source. Use when the response must contain only the full definitions of the named functions in the requested order.
---

# Add docstrings to named public functions

Document every function named in the request. Do not stop after documenting only some of them.

For each named function, copy its complete definition and insert one docstring as its first
statement. Return only those completed definitions, exactly once each and in the order listed.

## Preserve the original source verbatim

The inserted docstrings are the only permitted changes. Preserve every existing:

- Decorator.
- Function name and signature.
- Type annotation and default value.
- Comment and formatting choice.
- Executable statement.
- Complete function body.

Do not refactor, repair, abbreviate, or reorder the source. Never replace body content with `...`,
`pass`, a comment, or another placeholder. Removing the inserted docstrings must reproduce the
original named definitions verbatim.

Do not return imports, unrelated definitions, headings, explanations, Markdown code fences, or
duplicate copies of any function.

## Use the required docstring structure

Use an indented multiline triple-double-quoted docstring. Place its one-line summary immediately
after the opening quotes:

    """Check whether the value satisfies the required condition.

The summary must:

- Use imperative wording.
- Start with exactly one of these capitalized words: `Add`, `Build`, `Check`, `Clip`, `Compress`,
  `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`,
  `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`,
  `Transform`, or `Validate`.
- End with `.`, `!`, or `?`.
- Describe the function's behavior without repeating its signature.

After the summary, include applicable sections in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between consecutive
sections. Do not create empty sections. `Examples:` is mandatory for every named function,
regardless of which other sections apply.

Indent section entries four spaces beyond their labels. Put the closing triple quotes on their own
line, with no blank line immediately before them or between them and the original first executable
statement. Use a raw triple-double-quoted docstring when its content contains backslashes.

## Document every parameter

Include `Args:` whenever the signature contains a parameter other than `self` or `cls`.

Document every eligible parameter exactly once, in signature order. Use the exact parameter name
from the signature and add no other names.

For an annotated parameter, reproduce the annotation text exactly:

    parameter_name (ExactAnnotation): Explain the parameter's role, accepted values, or effect.

For an unannotated parameter, do not invent a type:

    parameter_name: Explain the parameter's role, accepted values, or effect.

Do not put a default value in the type field. The description must explain behavior rather than
merely restating the parameter name.

## Document every returned value

Include `Returns:` when any execution path returns a value. Describe every possible returned value
and what it means, including distinct conditional outcomes.

If the signature has a return annotation, reproduce it exactly:

    ExactReturnAnnotation: Explain the returned value and its meaning.

If the return value is unannotated, provide only a description; do not invent a type. Omit
`Returns:` when the function has only an implicit return or bare `return`.

Determine return behavior from the complete executable body, not from the function name alone.

## Document only direct explicit raises

Include `Raises:` only when the named function itself contains an explicit `raise` statement.
Document every exception type named by those statements and the exact condition that reaches each
one:

    ExceptionType: Explain the condition that causes the exception.

Do not list an exception merely because it:

- Appears in an `except` clause.
- May be raised by a called helper.
- Could arise from an operation.
- Is explicitly raised only inside another function or method.

## Add a runnable doctest to every function

Every named function must have its own `Examples:` section containing at least one `>>>` prompt.
A prose example is not sufficient, and an example in one function does not satisfy another
function.

Each doctest must:

- Directly call the function whose docstring contains it.
- Run in the original module namespace without omitted setup.
- Use valid, concrete arguments.
- Be deterministic.
- Show the exact Python representation of every displayed result.
- Contain no pseudocode, placeholders, guessed output, or ellipses for unknown output.

Prefer the simplest call whose result can be verified from the body. If a concrete result can
vary, display a deterministic property instead. Include any required setup as additional `>>>`
lines. If a statement displays no result, do not invent an output line.

Before moving to the next function, confirm that the current function contains both an
`Examples:` label and a direct `>>>` call to that function.

## Validate before responding

Do not return the result until every check passes:

- Every requested function appears exactly once and in the requested order.
- Every function includes its complete original definition and body.
- No original source text changed except for the inserted docstrings.
- Every eligible parameter appears exactly once in `Args:` and in signature order.
- Every documented annotation exactly matches the signature.
- `Returns:` covers all value-returning paths and is omitted only when inapplicable.
- `Raises:` exactly matches exception types explicitly raised by that function.
- Every function has its own `Examples:` section with a direct, runnable `>>>` doctest.
- Every doctest's displayed output is exact.
- The completed definitions parse successfully and their doctests pass.
- The response contains only the completed definitions, without Markdown fences or commentary.