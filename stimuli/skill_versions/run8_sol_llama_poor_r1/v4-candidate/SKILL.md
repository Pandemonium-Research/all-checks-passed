---
name: docstring-api
description: Add complete Google-style docstrings to named public Python functions while preserving their exact signatures and executable bodies. Use when returning only selected function definitions with documented parameters, results, explicit exceptions, and runnable doctests.
---

# Add docstrings to named public functions

## Preserve and return the requested code

Return every named public function, in the requested order. Do not stop before the final requested function.

For each function:

- Include its decorators, signature, and complete body.
- Insert only its docstring.
- Preserve every original character outside the inserted docstring, including indentation, line wrapping, comments, literals, nested definitions, blank lines, and executable statements.
- Do not move, reformat, refactor, correct, add, or delete executable code.
- Do not replace any code with `...`, `pass`, comments, or other placeholders.

Return no imports, unrelated definitions, external helpers, Markdown fences, or explanatory text.

## Insert the docstring correctly

Insert the docstring as the function's first statement, immediately before its original first body statement. Never place documentation after executable code.

Use an indented multiline triple-double-quoted docstring:

- Put the opening and closing `"""` on separate lines.
- Put the summary on the line immediately after the opening quotes.
- Keep the summary, sections, entries, and doctests inside the quotes.
- Leave no blank line immediately before the closing quotes.
- Leave no blank line between the closing quotes and the original first body line.
- Use `r"""` when the docstring source contains backslashes.

## Write one summary

Begin each docstring with exactly one one-line imperative summary describing the function's actual behavior.

Start the summary with exactly one of these capitalized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

Do not repeat the signature, add a second summary sentence, or copy these writing instructions or the allowed-word list into the docstring.

## Add Google-style sections

After the summary, include every applicable section in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between consecutive sections. Put no blank line between a section label and its first entry. Indent section entries four spaces beyond the label, and indent wrapped continuation lines to align with their descriptions.

### Args

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every applicable parameter exactly once and in signature order. Do not treat `/` or a standalone `*` as parameters. Preserve leading stars on variadic names such as `*args` and `**kwargs`.

For an annotated parameter, use:

`name (annotation): Description.`

Copy the annotation text exactly from the signature. Do not simplify, expand, qualify, or replace it with an inferred runtime type.

For an unannotated parameter, use:

`name: Description.`

Describe the parameter's role and all accepted values, units, constraints, and default-dependent behavior established by the signature or body. Distinguish input units from output size when they differ.

### Returns

Include `Returns:` if the requested function returns a value, generator, or iterator. Omit it only when the function has no value return and produces only `None`.

For an annotated return value, use:

`annotation: Description.`

Copy the return annotation exactly from the signature. If no return annotation exists, provide the description without inventing a type.

Describe every possible result form and every parameter-dependent or branch-dependent difference. Describe the result of the requested outer function, not unrelated values returned by its nested helpers.

For a returned generator or iterator, retain the exact return annotation and describe the values obtained by iterating it. Use `Returns:`, not `Yields:`.

### Raises

Include `Raises:` only for caller-visible exceptions produced by explicit `raise` statements inside the requested function's complete definition.

Include an explicit raise inside a nested local function when that local function is executed by the requested function or while consuming a result returned by it. Omit raises that are caught before they escape.

Do not document exceptions merely because a separately defined function, method, operator, or library routine could raise them. Do not infer exceptions from annotations, assertions, validation assumptions, or possible runtime failures.

Use one entry per distinct exception type:

`ExceptionType: Condition that triggers it.`

Document every triggering condition. If one exception type is explicitly raised under multiple conditions, combine all of those conditions in its description.

### Examples

Every requested function must have its own `Examples:` section containing at least one runnable doctest prompt beginning with `>>>`.

Each doctest must:

- Exercise that specific function.
- Run in the module's normal namespace without relying on another function's docstring example.
- Complete successfully.
- Show the exact expected output for every expression that produces output.
- Use valid values and real expectations rather than fabricated results or placeholders.
- Avoid doctest output wildcards and unenabled doctest directives.

Prefer deterministic calls. For random, time-dependent, environment-dependent, unordered, or address-bearing results, assign the result once and test stable properties such as its type, length, format, membership, sorted form, or a Boolean invariant. Never show a changing value as fixed expected output.

## Final verification

Before returning the response, check each requested function independently:

- Its complete definition is present in the requested position.
- Its signature and all original body text remain verbatim.
- Its docstring is the first statement and all documentation is inside the quotes.
- Its summary uses an allowed first word and permitted ending punctuation.
- Every applicable parameter is documented once, in order, with its exact annotation.
- Every returned result is documented with the exact return annotation.
- Every applicable explicit raise is documented, and no inferred exception is listed.
- It contains a runnable, deterministic `>>>` doctest.
- Its sections are applicable, correctly ordered, and separated by exactly one blank line.

Finally, verify that the response contains only the requested complete function definitions and no code fence or surrounding explanation.