---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to named public Python functions. Use when the source code is already correct and the response must contain only the requested full function definitions, unchanged except for inserted docstrings.
---

# Add API docstrings to named functions

Document every function named in the request, exactly once and in the order listed.

For each named function:

1. Copy its complete definition, including any decorators and its full body.
2. Insert one docstring as the first statement in the body.
3. Preserve all existing source text exactly.
4. Add and verify a runnable doctest that directly calls that function.

Return only the completed definitions. Do not include imports, unrelated definitions, explanations,
headings, Markdown fences, or duplicate copies.

## Preserve the source exactly

The docstrings are the only additions permitted. Do not alter any existing:

- Decorator.
- Signature, annotation, or default value.
- Executable statement.
- Comment.
- Formatting or statement order.

Do not fix, refactor, shorten, or complete the code. Never replace any part of a body with `...`,
`pass`, a comment, or another placeholder. Removing the inserted docstrings from the response must
reproduce the original requested definitions verbatim.

## Format each docstring

Use an indented multiline triple-double-quoted docstring. Use `r"""` when the docstring contains
backslashes.

Start with a one-line imperative summary immediately after the opening quotes. The summary must:

- Begin with one capitalized word from this list: `Add`, `Build`, `Check`, `Clip`, `Compress`,
  `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`,
  `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`,
  `Transform`, or `Validate`.
- Describe the function's behavior without repeating its signature.
- End with `.`, `!`, or `?`.

After the summary, include applicable sections in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line before each section. Do not include an empty section. `Examples:` is
required for every named function.

Indent section entries four spaces beyond their labels. Put the closing triple quotes on their own
line immediately after the final example output, with no blank line before the closing quotes.
Place the preserved original first statement on the next line.

## Document all parameters

Include `Args:` when the signature has any parameter other than `self` or `cls`.

Document every eligible parameter exactly once and in signature order. Use its exact name. Do not
document names absent from the signature.

For an annotated parameter, copy the annotation text exactly:

    parameter_name (ExactAnnotation): Explain its accepted value, role, or effect.

For an unannotated parameter, do not invent a type:

    parameter_name: Explain its accepted value, role, or effect.

Do not put default values in the type field. Descriptions must explain behavior rather than merely
repeat the parameter name.

## Document all return values

Include `Returns:` when any execution path returns a value. Describe every possible returned value
and what each outcome means.

When the signature has a return annotation, copy it exactly:

    ExactReturnAnnotation: Explain the returned value and the meaning of each possible outcome.

For an unannotated return value, provide only the description; do not invent a type. Omit
`Returns:` only when the function has no value-returning path. A bare `return` or implicit return
does not require the section.

Determine return behavior from the complete body, including every conditional path.

## Document explicit raises

Include `Raises:` only when the named function's own body contains an explicit `raise` statement.
Document every exception type explicitly raised there and the exact condition that reaches it:

    ExceptionType: Explain the condition that causes the exception.

Do not list exceptions merely because they appear in an `except` clause, may be raised by a called
helper, or could arise from an operation.

## Add a runnable doctest to every function

Every function must have its own `Examples:` section containing at least one `>>>` prompt that
directly calls that function.

Each doctest must:

- Run in the original module namespace without omitted setup.
- Use concrete, valid arguments.
- Be deterministic.
- Show the exact Python representation of every displayed result.
- Contain no pseudocode, placeholders, guessed output, or ellipses for unknown output.

Prefer the simplest successful call whose result follows directly from the body. If the concrete
result varies, display a deterministic property of it. Add required setup as preceding `>>>`
lines. Do not invent an output line for a statement that displays no value.

An example for one function does not satisfy any other function. Before proceeding to the next
definition, confirm that the current docstring contains both `Examples:` and a direct `>>>` call
to the current function.

## Final verification

Before responding, verify all of the following:

- The number of definitions equals the number of requested function names.
- The definitions occur exactly once and in the requested order.
- Every definition contains its complete original body.
- No original source text changed.
- Every eligible parameter is documented exactly once and in signature order.
- Every documented annotation exactly matches the signature.
- Every value-returning path is covered by `Returns:`.
- `Raises:` exactly matches the function's explicit `raise` statements.
- Every function has its own runnable, deterministic doctest with exact output.
- The completed definitions parse and all doctests pass.
- The response contains only the completed definitions, with no Markdown fence or commentary.