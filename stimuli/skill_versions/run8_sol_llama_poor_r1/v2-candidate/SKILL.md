---
name: docstring-api
description: Use when adding complete Google-style docstrings to specified public Python functions without changing their signatures, executable bodies, behavior, or requested order.
---

# Add docstrings to named public functions

## Output contract

Return only the complete definitions of the named public functions, in the order listed in the request.

For each requested function:

- Include its decorators, signature, and full body.
- Preserve the signature exactly.
- Preserve every existing source line exactly, including indentation, comments, nested functions, literals, executable statements, and blank lines.
- Add only the docstring. Do not move, reformat, correct, or refactor existing code.
- Never replace any part of the body with `...`, `pass`, a comment, or another placeholder.

Do not return imports, unrelated functions, external helper definitions, Markdown fences, or explanatory text.

## Insert the docstring

Make the docstring the first statement inside the function. Insert it before the original first body statement; never place documentation after executable code.

Use an indented multiline triple-double-quoted docstring:

- Put the opening and closing `"""` on their own lines.
- Put the summary immediately after the opening quotes.
- Put no blank line between the closing quotes and the original first body line.
- Use `r"""` when the docstring source contains a backslash.

Everything being documented—including the summary, sections, entries, and doctests—must remain inside the triple quotes.

## Write the summary

Begin with exactly one one-line imperative summary.

The first word must be one of:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

The summary must:

- Describe the function's actual behavior.
- End with `.`, `!`, or `?`.
- Not repeat the signature.
- Not contain instructions, allowed-word lists, or other commentary about writing docstrings.

## Add Google-style sections

After the summary, add each applicable section in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line after the summary and between consecutive sections. Do not put a blank line between a section label and its first entry. Indent every entry four spaces beyond its section label.

### Args

Add `Args:` when the signature has parameters other than `self` or `cls`.

Document every applicable parameter exactly once and in signature order. Use the exact parameter name from the signature. Do not add, omit, rename, or reorder parameters.

For an annotated parameter, use:

`name (annotation): Description.`

Copy the annotation text exactly as written in the signature. Do not simplify, expand, qualify, or infer a different type.

For an unannotated parameter, use:

`name: Description.`

Describe the parameter's purpose and any accepted values, units, constraints, or default-dependent behavior established by the signature or body.

### Returns

Add `Returns:` when the function returns a value, generator, or iterator. Omit it for a function that only returns `None`, whether implicitly or through a bare return.

For an annotated return value, use:

`annotation: Description.`

Copy the return annotation exactly from the signature. Do not substitute the runtime type or a more specific inferred type.

If there is no return annotation, provide only a description without inventing a type.

Describe every possible result or result form, including differences selected by parameters or separate return paths. For a generator or iterator, use `Returns:` with the exact return annotation and describe the values it produces; do not replace this section with `Yields:`.

### Raises

Add `Raises:` only for exceptions raised by explicit `raise` statements within the requested function's definition and capable of escaping it.

This includes explicit raises inside a nested local function when that local function is used by the requested function. Do not list exceptions merely because a separate called function, method, operator, or library routine could raise them. Do not treat annotations, assertions, or assumed validation failures as explicit raises.

Use:

`ExceptionType: Condition that triggers it.`

Document every explicitly raised exception type and every triggering condition. If the same exception type is raised under multiple conditions, make its description cover all of them.

### Examples

Every requested function must contain its own `Examples:` section with at least one runnable doctest prompt beginning with `>>>`.

Each doctest must:

- Call or otherwise exercise that specific function.
- Be valid in the module's normal namespace.
- Complete successfully.
- Show the exact expected output for every expression that produces output.
- Avoid fabricated results, placeholders, and ellipsis-based output matching.

Use deterministic inputs and outputs whenever possible. For random, time-dependent, environment-dependent, unordered, or address-bearing results, check a stable property such as the type, length, membership, normalized value, or a Boolean invariant. Never present a changing result as fixed output.

## Verify before returning

Check every requested function independently:

- The complete definition is present and appears in the requested order.
- The docstring is the first statement.
- All documentation is inside the triple quotes.
- The summary starts with an allowed word and ends with permitted punctuation.
- Every applicable parameter appears once, in order, with its exact annotation.
- Every returned result is documented with the exact return annotation.
- Every applicable explicit raise is documented, and no inferred exception is added.
- The function has a runnable, deterministic `>>>` doctest.
- Sections are applicable, correctly ordered, and separated by exactly one blank line.
- No original source text outside the inserted docstring has changed.
- The response contains no surrounding prose or code fence.