---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to specified public Python functions while preserving their signatures and executable bodies exactly. Use when a correct module has named public functions without docstrings and the response must contain only those full updated definitions.
---

# Add docstrings to named public functions

Process only the function names specified in the request. Use their requested order, even if the
source module uses a different order.

For each named function:

1. Copy its complete source definition, including attached decorators and the entire body.
2. Inspect its signature and body.
3. Insert one docstring as its first statement.
4. Verify that function's documentation before processing the next function.

## Preserve the source

The inserted docstrings are the only permitted changes. Preserve verbatim every existing:

- Decorator.
- Function name and signature.
- Annotation and default value.
- Comment and formatting choice.
- Executable statement.

Do not fix, refactor, abbreviate, or reorder the code. Do not replace any body content with `...`,
`pass`, or another placeholder. Removing the inserted docstrings from the response must reproduce
the original named definitions exactly.

Return each requested definition exactly once. Do not include imports, unrelated functions,
headings, explanations, Markdown fences, or duplicate definitions.

## Write the docstring

Use an indented, multiline, triple-double-quoted docstring. Put the one-line summary immediately
after the opening quotes:

    """Check whether the value satisfies the required condition.

The summary must:

- Use imperative wording.
- Start with exactly one capitalized word from:
  `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`,
  `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`,
  `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.
- End with `.`, `!`, or `?`.
- Describe behavior without repeating the function signature.

After the summary, include applicable sections in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between sections. Do not
include an empty section. `Examples:` is never optional.

Indent section entries four spaces beyond their labels. Put the closing triple quotes on their own
line, immediately after the final entry, and put the original first statement on the next line
without an intervening blank line. Use `r"""` instead of `"""` when the docstring contains
backslashes.

## Inventory the arguments

Include `Args:` when the signature has any parameter other than `self` or `cls`.

Document every eligible parameter exactly once, in signature order. Use its exact name and do not
add names absent from the signature.

For an annotated parameter, copy its annotation text exactly:

    parameter_name (ExactAnnotation): Explain its role, accepted value, or effect.

For an unannotated parameter, do not invent a type:

    parameter_name: Explain its role, accepted value, or effect.

Do not add a default value to the type field. Write a meaningful description rather than merely
rephrasing the parameter name.

## Describe returned values

Include `Returns:` if any execution path returns a value. Cover every possible returned value and
explain what each value means.

When the signature has a return annotation, copy it exactly:

    ExactReturnAnnotation: Explain the returned value and its meaning.

For an unannotated return value, write only the description and do not invent a type. Omit
`Returns:` when the function has no value-returning path; an implicit return or bare `return` does
not require it.

Determine return behavior from the complete body, including conditional paths, rather than from
the function name.

## List explicit exceptions

Include `Raises:` only if the named function itself contains an explicit `raise` statement.
Document every exception type named by such statements and the precise condition that reaches
each one:

    ExceptionType: Explain the condition that causes the exception.

Do not document exceptions merely because they appear in an `except` clause, may come from a
called helper, or could arise from an operation. Do not omit any exception type explicitly raised
by the function.

## Add a doctest to every function

Every named function must contain its own `Examples:` section with at least one `>>>` prompt.
Before moving to the next function, confirm that the current function has both `Examples:` and a
direct call to that function.

Each doctest must:

- Run in the original module namespace without omitted setup.
- Directly call the function whose docstring contains it.
- Use valid concrete arguments.
- Be deterministic.
- Show the exact Python representation of every displayed result.
- Include no pseudocode, placeholders, guessed output, or ellipses for unknown output.

Prefer a simple successful call. If the concrete result varies, display a deterministic property
of the result. Include setup as additional `>>>` lines when required. If a statement produces no
displayed value, do not invent an output line. An example in one function never satisfies another
function's requirement.

## Validate the response

Do not respond until every check passes:

- The number of returned definitions equals the number of requested names.
- The definitions appear exactly once and in the requested order.
- Every definition contains its complete original body.
- Removing the docstrings reproduces the original definitions verbatim.
- Every eligible parameter appears once in `Args:` and in signature order.
- Every documented annotation exactly matches the signature.
- `Returns:` covers all value-returning paths and is absent only when inapplicable.
- `Raises:` exactly matches exception types explicitly raised by that function.
- The number of `Examples:` sections equals the number of returned functions.
- Every function has at least one direct, runnable `>>>` doctest with exact output.
- The completed definitions parse successfully and all doctests pass.
- The response contains only the completed definitions, with no Markdown fence or commentary.