---
name: docstring-api
description: Use when adding complete Google-style docstrings to named public functions while preserving their signatures, source bodies, output order, and executable behavior.
---

# Add docstrings to named public functions

## Required output

Return only the complete definitions of the named public functions, in the order requested.

For every returned function:

- Preserve its signature exactly.
- Preserve every existing line of its definition exactly, including decorators, comments, nested functions, executable statements, indentation, literals, and blank lines.
- Make no refactors, corrections, formatting changes, or other edits.
- Add only the new docstring.
- Include the full body. Never replace code with `...`, `pass`, or another placeholder.

Do not return imports, unrelated functions, helper definitions outside the requested functions, code fences, or explanatory text.

## Place the docstring correctly

Insert the docstring as the first statement inside the function, before every executable statement. All summaries, sections, entries, and doctests must remain inside its triple quotes. Never place documentation after a `return`, `raise`, or other body statement.

Use an indented multiline triple-double-quoted docstring:

- Put the opening and closing `"""` on their own lines.
- Put the summary on the line immediately after the opening quotes.
- Put no blank line between the closing quotes and the original first body line.
- Use `r"""` instead of `"""` if the docstring source contains a backslash.

## Write the summary

Begin each docstring with exactly one one-line imperative summary.

The summary must:

- Start with one of these capitalized words: `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.
- Describe the function's actual behavior.
- End with `.`, `!`, or `?`.
- Not repeat the signature.
- Not contain instructions about writing the docstring.

A second prose sentence does not replace any required section.

## Add the Google-style sections

After the summary, add every applicable section in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between consecutive sections. Indent each section entry four spaces beyond its section label.

### Args

Add `Args:` when the signature has parameters other than `self` or `cls`.

Document every applicable parameter exactly once and in signature order. Use its exact signature name; do not add, omit, rename, or reorder parameters.

For an annotated parameter, use:

`name (annotation): Description.`

Copy the annotation text exactly from the signature. Do not simplify, expand, or substitute it. For an unannotated parameter, use:

`name: Description.`

Describe the parameter's meaning, units, accepted values, and default behavior when those details affect the function. Derive those details from the signature and body.

### Returns

Add `Returns:` when the function returns a value. Omit it only when the function has no value return.

Use:

`annotation: Description.`

Copy the return annotation exactly from the signature. Describe all possible returned values or forms, including behavior selected by parameters or different return paths. For a returned generator or iterator, describe what it produces while retaining the exact return annotation as the entry type.

### Raises

Add `Raises:` only when the function definition contains an explicit `raise` whose exception can escape the named function.

Use:

`ExceptionType: Condition that triggers it.`

Document every explicitly raised exception type and every triggering condition. This includes explicit raises in a local function that the named function invokes. If one exception type is raised under several conditions, its description must cover all of them.

Do not list exceptions merely because a called function, method, operator, or library routine might raise them. Do not infer undocumented failures from annotations or validation assumptions.

### Examples

Every named function must have its own `Examples:` section containing at least one runnable doctest prompt beginning with `>>>`.

The doctest must:

- Call or otherwise exercise that function.
- Be valid in the module's normal namespace.
- Complete successfully.
- Show the exact expected output for every expression that produces output.
- Avoid placeholders, invented output, and unenabled doctest directives.

Use a deterministic call whenever possible. For random, time-dependent, environment-dependent, unordered, or address-bearing results, test a stable property such as a type, length, membership condition, normalized value, or Boolean invariant. Do not write a changing value as fixed expected output.

## Final verification

Before returning the definitions, verify each function independently:

- Its docstring is the first statement and contains all documentation.
- Its summary begins with an allowed word and ends with permitted punctuation.
- Every parameter appears once with its exact name and annotation.
- Every returned value is documented with the exact return annotation.
- Every applicable explicit raise is documented, with no inferred exceptions added.
- Its `Examples:` section contains a runnable, deterministic `>>>` doctest.
- The required sections are ordered and separated correctly.
- The signature and all original source text remain unchanged outside the inserted docstring.
- The requested functions are complete, in the requested order, with no surrounding material.