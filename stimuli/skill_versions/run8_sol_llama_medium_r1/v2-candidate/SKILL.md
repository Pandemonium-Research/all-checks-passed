---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to specified public Python functions while preserving every signature, executable statement, and function body. Use when the response must contain only the named functions with documentation inserted.
---

# Add docstrings to named public functions

Read the complete source definition of every named function before writing. For each function,
identify:

- Every parameter in signature order.
- Every value the function can return.
- Every exception type named in an explicit `raise` statement in that function.
- At least one deterministic call whose exact doctest result is known.

Apply the following rules to each named function independently.

## Preserve the source exactly

Return each named public function exactly once, in the order listed in the request. Include its
complete definition and full body.

The only permitted source change is inserting a docstring as the first statement of each named
function. Preserve all existing text, including:

- Decorators.
- Function names and signatures.
- Type annotations and default values.
- Comments and formatting.
- Every executable statement.

Do not refactor, correct, abbreviate, or reorder the source. Never replace any part of a function
body with `...`, `pass`, or another placeholder. Removing the inserted docstrings from the response
must reproduce the original named definitions verbatim.

Return only the completed definitions. Do not include imports, unrelated definitions, Markdown
code fences, explanations, headings, or duplicate copies.

## Use the required docstring layout

Use an indented multiline triple-double-quoted docstring. Put the one-line summary immediately
after the opening quotes:

    """Check whether the value satisfies the required condition.

The summary must:

- Be imperative.
- Begin with a capitalized form of one locally recognized word from
  `add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.
- End with `.`, `!`, or `?`.
- Describe the behavior without repeating the function signature.

After the summary, include applicable sections in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between consecutive
sections. Do not include an empty section. `Examples:` is mandatory for every named function.

Indent section entries four spaces beyond their labels. Put the closing triple quotes on their own
line. Do not place a blank line immediately before the closing quotes or between the closing quotes
and the original first executable statement. If the docstring text contains backslashes, use a raw
triple-double-quoted docstring.

## Inventory every argument

Include `Args:` unless the function has no parameters other than `self` or `cls`.

Document every parameter except `self` and `cls`, exactly once and in signature order. Use the
parameter's exact name and add no names that are absent from the signature.

For an annotated parameter, copy the annotation text exactly:

    parameter_name (ExactAnnotation): Explain the parameter's role or accepted value.

For an unannotated parameter, do not invent a type:

    parameter_name: Explain the parameter's role or accepted value.

Do not put a default value in the type field. A description must explain how the parameter affects
the function rather than merely restating its name.

## Describe all returned values

Include `Returns:` if the function has any value-returning path. Describe every possible returned
value and what each value means.

If the signature has a return annotation, copy it exactly:

    ExactReturnAnnotation: Explain the returned value and its meaning.

If the return value is unannotated, provide only its description and do not invent a type. Omit
`Returns:` when the function has no value-returning path; a bare `return` does not require this
section.

Base the description on the executable body, including conditional return paths, rather than on
the function name alone.

## List only explicitly raised exceptions

Include `Raises:` only when the function itself contains an explicit `raise` statement naming an
exception type. Document every such exception type and the condition that reaches that statement:

    ExceptionType: Explain the exact condition that causes the exception.

Do not list exceptions merely because they:

- Appear in an `except` clause.
- May be raised by a called helper.
- Could result from an operation.
- Are raised only inside a different function or method.

Do not omit an exception type that is explicitly raised by the named function.

## Add a real doctest to every function

Every named function must have its own `Examples:` section with at least one runnable `>>>` prompt.
A prose example is insufficient.

Each doctest must:

- Directly call the function whose docstring contains it.
- Run in the original module's namespace without omitted setup.
- Use valid concrete arguments.
- Be deterministic.
- Show the exact Python representation of every displayed result.
- Include no pseudocode, placeholders, guessed output, or ellipses standing for unknown output.

Prefer the simplest call whose result can be verified from the body. If the concrete result can
vary, assert or display a deterministic property instead. If a call produces no displayed result,
do not invent an output line.

Do not satisfy multiple functions with one shared example. Check every function separately for its
own `Examples:` section and `>>>` prompt.

## Perform the final checks

Before responding, verify all of the following:

- Every requested function appears exactly once and in the requested order.
- Every returned definition includes its entire original body.
- No source text changed except for the inserted docstrings.
- Every eligible parameter appears exactly once in `Args:` and in signature order.
- Every documented annotation exactly matches the corresponding signature annotation.
- `Returns:` covers all value-returning paths and is absent when inapplicable.
- `Raises:` exactly covers exception types explicitly raised by the function itself.
- Every function has an `Examples:` section containing a direct, runnable `>>>` doctest.
- Every expected doctest output is exact.
- The completed definitions parse successfully.
- The response contains only the completed function definitions, with no fence or commentary.