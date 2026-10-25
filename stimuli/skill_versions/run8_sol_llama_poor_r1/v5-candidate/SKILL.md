---
name: docstring-api
description: Add complete Google-style docstrings to named public Python functions while preserving their exact signatures and bodies. Use when returning only selected function definitions with documented parameters, results, explicit exceptions, and runnable doctests.
---

# Add docstrings to named public functions

## Output requirements

Return every named public function, in the order requested. Do not omit or truncate any requested function.

For each function:

- Include its decorators, exact signature, and complete body.
- Insert only the new docstring.
- Preserve all original source text outside the docstring character-for-character, including indentation, line wrapping, comments, literals, nested definitions, executable statements, and blank lines.
- Do not reformat, refactor, correct, move, add, or delete executable code.
- Do not replace code with `...`, `pass`, comments, or any other placeholder.

Return only the requested function definitions. Do not include imports, unrelated definitions, external helpers, Markdown code fences, or explanatory text.

## Insert each docstring

Place the docstring as the function's first statement, immediately before its original first body statement. All documentation must remain inside the docstring; never place an `Args:`, `Returns:`, `Raises:`, or `Examples:` section after executable code.

Use an indented multiline triple-double-quoted docstring:

- Put the opening and closing `"""` on separate lines.
- Put the summary on the line immediately after the opening quotes.
- Put no blank line before the opening quotes.
- Put no blank line immediately before the closing quotes.
- Put no blank line between the closing quotes and the original first body line.
- Use `r"""` when the docstring source contains backslashes.

## Write the summary

Begin each docstring with exactly one one-line imperative summary that accurately describes the function's behavior.

Its first word must be exactly one of these capitalized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

Do not repeat the function signature, add a second summary sentence, or include these instructions or the allowed-word list in the docstring.

## Add Google-style sections

After the summary, include every applicable section in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between consecutive sections. Put no blank line between a section label and its first entry. Indent entries four spaces beyond the section label, and indent continuation lines to align with the entry description.

### Args

Include `Args:` when the signature contains parameters other than `self` or `cls`.

Document every applicable parameter exactly once and in signature order. Use each parameter's exact name. Do not add, omit, rename, or reorder parameters, and do not treat `/` or a standalone `*` as a parameter. Preserve leading stars in variadic names such as `*args` and `**kwargs`.

For an annotated parameter, use:

`name (annotation): Description.`

Copy the annotation text exactly as written in the signature. Do not simplify, expand, qualify, or replace it with an inferred runtime type.

For an unannotated parameter, use:

`name: Description.`

Describe the parameter's purpose and all accepted values, constraints, units, and default-dependent behavior established by the signature and body. Distinguish input units from output length or size when they differ.

### Returns

Include `Returns:` when the function returns a value, generator, or iterator. Omit it only when the function has no value return and produces only `None`.

For an annotated return value, use:

`annotation: Description.`

Copy the return annotation exactly as written in the signature. If there is no return annotation, describe the result without inventing a type.

Describe every possible result form, including differences caused by parameters or separate return paths. Describe the result of the requested outer function rather than unrelated values returned by nested helpers.

For a returned generator or iterator, retain the exact return annotation and describe the values obtained by iterating it. Use `Returns:`, not `Yields:`.

### Raises

Include `Raises:` only for caller-visible exceptions produced by explicit `raise` statements inside the requested function's complete definition.

Include an explicit raise inside a nested local function when that local function is executed by the requested function or while consuming a result returned by it. Omit an exception that is caught before it can escape.

Do not document exceptions merely because a separately defined function, method, operator, or library routine might raise them. Do not infer exceptions from annotations, assertions, validation assumptions, or other possible runtime failures.

Use one entry per distinct exception type:

`ExceptionType: Condition that triggers it.`

Document every triggering condition. If one exception type is explicitly raised under multiple conditions, combine all those conditions in its description.

### Examples

Every requested function must have its own `Examples:` section containing at least one runnable doctest prompt beginning with `>>>`.

Each doctest must:

- Call or otherwise exercise that specific function.
- Run in the module's normal namespace without depending on another function's docstring example.
- Complete successfully.
- Show the exact expected output for every expression that produces output.
- Use valid inputs and real expectations, never placeholders or fabricated results.
- Avoid output wildcards and unenabled doctest directives.

Prefer deterministic calls and outputs. For random, time-dependent, environment-dependent, unordered, or address-bearing results, assign the result once and test stable properties such as its type, length, format, membership, sorted form, or a Boolean invariant. Never show a changing result as fixed expected output.

## Verify before returning

Check every requested function independently:

- Its complete definition appears in the requested order.
- Its signature and all original body text remain verbatim.
- Its docstring is the first statement.
- All docstring content is inside the triple quotes.
- Its summary has one line, begins with an allowed word, and ends with permitted punctuation.
- Every applicable parameter is documented exactly once, in order, with its exact annotation.
- Every returned result is documented with the exact return annotation.
- Every applicable explicit raise is documented, and no inferred exception is added.
- It has its own runnable, deterministic `>>>` doctest.
- Its sections are applicable, correctly ordered, and separated by exactly one blank line.

Finally, verify that the response contains only the complete requested function definitions and no code fence or surrounding explanation.