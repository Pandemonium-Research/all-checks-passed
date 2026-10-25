---
name: docstring-api
description: Add complete Google-style docstrings to specified public Python functions while preserving their signatures, bodies, behavior, and requested order. Use when returning selected function definitions with documented parameters, results, explicit exceptions, and runnable doctests.
---

# Add docstrings to named public functions

## Output contract

Return only the complete definitions of every named public function, in the order requested.

For each function:

- Include its decorators, exact signature, and full body.
- Preserve every original source line exactly, including indentation, comments, literals, nested functions, executable statements, and internal blank lines.
- Add only the docstring. Do not reformat, refactor, correct, move, or delete existing code.
- Never replace code with `...`, `pass`, comments, or other placeholders.
- Do not stop before all requested functions are complete.

Do not include imports, unrelated definitions, external helpers, Markdown code fences, or explanatory text.

## Insert the docstring

Insert the docstring as the first statement inside the function, before the original first body statement. Never put documentation after executable code.

Use an indented multiline triple-double-quoted docstring:

- Put the opening and closing `"""` on separate lines.
- Put the summary immediately after the opening quotes.
- Put no blank line before the opening quotes or between the closing quotes and the original first body line.
- Use `r"""` when the docstring contains a backslash.
- Keep the summary, sections, entries, and doctests inside the quotes.

## Write the summary

Start every docstring with exactly one one-line imperative summary.

Its first word must be exactly one of:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

The summary must:

- Describe the function's actual behavior.
- End with `.`, `!`, or `?`.
- Not repeat the signature.
- Not contain instructions, the allowed-word list, or commentary about writing docstrings.

## Add Google-style sections

After the summary, include every applicable section in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line after the summary and between sections. Do not put a blank line between a section label and its first entry. Indent each entry four spaces beyond its section label.

### Args

Include `Args:` when the signature contains parameters other than `self` or `cls`.

Document every applicable parameter exactly once and in signature order. Use its exact name from the signature; never add, omit, rename, or reorder parameters.

For an annotated parameter, use:

`name (annotation): Description.`

Copy the annotation text exactly as written in the signature. Do not simplify, expand, qualify, or infer a replacement type.

For an unannotated parameter, use:

`name: Description.`

Describe the parameter's purpose and any accepted values, constraints, units, or default-dependent behavior established by the signature and body.

### Returns

Include `Returns:` when the function returns a value, generator, or iterator. Omit it only when the function has no value return.

For an annotated return value, use:

`annotation: Description.`

Copy the return annotation exactly from the signature. Do not replace it with an inferred runtime type. If there is no return annotation, provide a description without inventing a type.

Describe every possible result or result form, including differences selected by parameters or separate return paths. For a returned generator or iterator, retain the exact return annotation and describe the values it produces; do not substitute a `Yields:` section.

### Raises

Include `Raises:` only for exceptions produced by explicit `raise` statements within the requested function's definition and capable of escaping it.

This includes an explicit raise inside a nested local function when the requested function executes that local function or exposes its execution through the returned result. It does not include exceptions that might arise from separate called functions, methods, operators, or library routines.

Use:

`ExceptionType: Condition that triggers it.`

Document every explicitly raised exception type and all conditions that trigger it. If one type is raised for multiple conditions, make its description cover every condition. Do not infer exceptions from annotations, assertions, validation assumptions, or possible library failures.

### Examples

Every requested function must have its own `Examples:` section containing at least one runnable doctest prompt beginning with `>>>`.

Each doctest must:

- Call or otherwise exercise that specific function.
- Be valid in the module's normal namespace.
- Complete successfully.
- Show the exact expected output for every expression that produces output.
- Use real inputs and expectations, not placeholders or fabricated results.
- Avoid output wildcards and unenabled doctest directives.

Prefer deterministic inputs and outputs. For random, time-dependent, environment-dependent, unordered, or address-bearing results, assign the result if necessary and test a stable property such as its type, length, membership, normalized value, or a Boolean invariant. Never present a changing result as fixed output.

## Verify the response

Before returning the definitions, check every requested function independently:

- The complete definition is present and in the requested order.
- The docstring is the first statement.
- All documentation remains inside the triple quotes.
- The summary starts with an allowed word and ends with permitted punctuation.
- Every applicable parameter appears once, in order, with its exact annotation.
- Every returned result is documented with the exact return annotation.
- Every applicable explicit raise is documented, with no inferred exception added.
- The function has its own runnable, deterministic `>>>` doctest.
- Sections are applicable, correctly ordered, and separated by exactly one blank line.
- No original source text outside the inserted docstring has changed.
- The response contains no surrounding prose or code fence.