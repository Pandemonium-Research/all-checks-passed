---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to specified public Python functions. Use when the source module is already correct and the response must contain only the named functions, in the requested order, with every signature and executable statement preserved.
---

# Add docstrings to named public functions

Return each named public function exactly once and in the order requested. Copy its complete
definition, including decorators and the full body, and insert one docstring as its first statement.

The docstring is the only permitted addition. Preserve every existing signature, annotation,
default value, comment, executable statement, statement order, and formatting choice. Do not fix,
refactor, abbreviate, or replace code with `...`, `pass`, comments, or other placeholders.

Return only the completed function definitions. Do not include imports, unrelated definitions,
headings, explanations, Markdown fences, or a second copy of any function.

## Complete one function at a time

For each requested function, perform all of these steps before proceeding to the next one:

1. Copy the complete original definition verbatim.
2. Insert the docstring as the first statement.
3. Document every eligible parameter.
4. Document every value-returning path.
5. Document every exception explicitly raised by that function.
6. Add an `Examples:` section with a runnable `>>>` doctest that directly calls that function.
7. Verify the doctest's exact output.

A function is incomplete if its docstring lacks either `Examples:` or a `>>>` invocation of that
same function. Do not emit an incomplete definition.

## Format the docstring

Use an indented multiline triple-double-quoted docstring. Use a raw triple-double-quoted docstring
when its contents include backslashes.

Place a one-line imperative summary immediately after the opening quotes. The summary must:

- Start with the capitalized form of one locally recognized word from this list:
  `add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.
- Describe the function's behavior without repeating its signature.
- End with `.`, `!`, or `?`.

After the summary, include the applicable sections in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between consecutive
sections. Do not include empty sections. `Examples:` is always required.

Indent section entries four spaces beyond their section labels. Put the closing triple quotes on
their own line, with no blank line immediately before them. Put the preserved original first
executable statement directly after the docstring, without adding a blank line.

## Document every parameter

Include `Args:` when the signature contains a parameter other than `self` or `cls`.

Document every eligible parameter exactly once, in signature order. Use its exact name and do not
add names absent from the signature.

For an annotated parameter, reproduce the annotation text exactly:

    name (ExactAnnotation): Explain the accepted value, role, or effect.

For an unannotated parameter, do not invent a type:

    name: Explain the accepted value, role, or effect.

Do not put a default value in the type field. Describe how the parameter affects behavior rather
than merely repeating its name.

## Document every returned value

Include `Returns:` if any path returns a value. Determine this from the complete function body,
including conditional paths.

Describe every possible returned value and what each outcome means. If the signature has a return
annotation, reproduce it exactly:

    ExactReturnAnnotation: Explain the returned value and every meaningful outcome.

If the return value is unannotated, provide only its description and do not invent a type. Omit
`Returns:` when the function has only implicit returns or bare `return` statements.

## Document only explicit raises

Include `Raises:` only for exception types named by explicit `raise` statements in the current
function's own body. Document every such type and the exact condition that reaches it:

    ExceptionType: Explain the condition that causes the exception.

Do not list an exception merely because it appears in an `except` clause, may be raised by a
called helper, could arise from an operation, or is explicitly raised only inside another
function or method.

## Add a runnable doctest to every function

Every named function must have its own `Examples:` section containing at least one `>>>` prompt
that directly invokes that function. An example in another function or at module level does not
count.

Each doctest must:

- Run in the original module namespace.
- Include any required setup as additional `>>>` lines.
- Use valid, concrete arguments.
- Be deterministic.
- Show the exact Python representation of every displayed result.
- Contain no pseudocode, placeholders, guessed output, or omitted required setup.
- Exercise the function whose docstring contains it.

Prefer the simplest call whose result can be verified from the body. If the concrete result varies,
display a deterministic property of it instead. If a statement produces no displayed result, do
not invent an output line.

## Validate the complete response

Before responding, verify all of the following:

- Every requested function appears exactly once and in the requested order.
- Every definition includes its complete original body and any decorators.
- Removing the inserted docstrings reproduces the original definitions verbatim.
- Every eligible parameter is documented exactly once and in signature order.
- Every documented annotation exactly matches the signature.
- `Returns:` covers every value-returning path and is omitted only when inapplicable.
- `Raises:` exactly matches the exception types explicitly raised by that function.
- Every function has its own `Examples:` section.
- Every `Examples:` section contains a runnable `>>>` call to its own function.
- Every displayed doctest result is exact and all doctests pass.
- The completed definitions parse successfully.
- The response contains only the completed definitions, without Markdown fences or commentary.