---
name: docstring-api
description: Add complete Google-style docstrings to an ordered set of public Python functions without changing their signatures or executable bodies. Use when given a correct module and asked to return only selected function definitions with documented parameters, results, explicit exceptions, and runnable doctests.
---

# Add docstrings to public functions

## Return only the requested definitions

Return every named public function, once, in the order requested. Continue through the final requested function.

For each requested function:

- Include its attached decorators, signature, and complete body.
- Add only a docstring as its first statement.
- Preserve the signature and all original source within the definition character-for-character, including indentation, line wrapping, comments, literals, nested definitions, blank lines, and executable statements.
- Do not move, reformat, refactor, correct, add, or delete executable code.
- Do not replace any part of the body with `...`, `pass`, a comment, or another placeholder.

Omit imports, unrelated definitions, external helpers, Markdown fences, and explanatory text.

## Inspect each function before writing

Read the complete signature and body of each requested function. Record:

1. Every parameter except `self` and `cls`, in signature order.
2. The exact source text of each parameter annotation.
3. Every possible returned result and the exact return annotation, if present.
4. Every caller-visible exception produced by an explicit `raise` within the requested definition.
5. Stable behavior that can be demonstrated by a successful doctest.

Derive documentation only from the supplied source. Do not infer behavior, accepted inputs, exceptions, or guarantees that the code does not establish.

## Insert the docstring

Insert an indented multiline triple-double-quoted docstring immediately before the original first body statement:

- Put the opening `"""` and closing `"""` on separate lines.
- Put the summary immediately after the opening quotes.
- Keep the summary and every section inside the quotes.
- Leave no blank line immediately before the closing quotes.
- Leave no blank line between the closing quotes and the original first body statement.
- Use `r"""` instead of `"""` when the docstring source contains backslashes.

Never put documentation after an executable statement.

## Write one imperative summary

Start each docstring with exactly one one-line summary of the function’s actual behavior.

The summary must begin with exactly one of these capitalized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

Do not add another summary sentence, repeat the signature, or copy these instructions or the allowed-word list into the docstring.

## Add Google-style sections

After the summary, include every applicable section in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between consecutive sections. Put no blank line between a section label and its first entry.

Align section labels with the summary. Indent entries four additional spaces. Align wrapped continuation lines with the entry’s description.

### Document arguments

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every applicable parameter exactly once and in signature order. Do not treat `/` or a standalone `*` as parameters. Preserve leading stars in variadic names such as `*args` and `**kwargs`.

For an annotated parameter, use:

`name (annotation): Description.`

Copy the annotation exactly from the signature. Do not simplify, expand, qualify, or replace it with an inferred runtime type.

For an unannotated parameter, use:

`name: Description.`

Describe the parameter’s role and every accepted value, constraint, unit, or default-dependent behavior established by the signature or body. Distinguish input units from output length or size when they differ. Do not invent constraints or guarantees.

### Document returned results

Include `Returns:` when the function returns a value, generator, or iterator. Omit it only when every path produces only `None` through a bare return or fall-through.

For an annotated return value, use:

`annotation: Description.`

Copy the return annotation exactly from the signature. When no return annotation exists, provide only the result description; do not invent a type.

Describe every possible result form and every parameter-dependent or branch-dependent difference. For a generator or iterator, describe the values obtained by consuming it while retaining the exact return annotation. Use `Returns:`, not `Yields:`.

Document the result of the requested outer function, not values returned only by its nested helpers.

### Document explicitly raised exceptions

Include `Raises:` only when an explicit `raise` in the requested function’s complete definition can produce a caller-visible exception.

Include an explicit raise inside a nested local function only when that local function is called by the requested function or can execute while consuming the requested function’s returned result. Omit exceptions caught before they escape.

Do not list exceptions merely because a separately defined function, method, operator, or library call could raise them. Do not infer exceptions from annotations, assertions, validation assumptions, or possible runtime failures.

Use one entry for each distinct exception type:

`ExceptionType: Condition that triggers it.`

State every triggering condition established by the code. Combine multiple conditions for the same exception type into one entry.

### Add a runnable doctest

Every requested function must have its own `Examples:` section containing at least one prompt beginning with `>>>`.

Each doctest must:

- Exercise that specific function with valid input.
- Run in the module’s normal namespace without imports or setup supplied by another function’s docstring.
- Complete successfully.
- Show the exact output of every expression that produces output.
- Use real values and expectations, never fabricated output or placeholders.
- Avoid output wildcards and doctest directives that are not enabled.

Prefer deterministic calls. For random, time-dependent, environment-dependent, unordered, or address-bearing results, assign the result once and test stable properties such as its type, length, format, membership, sorted contents, or a Boolean invariant. Never present a changing value as fixed expected output.

When the function returns a generator or iterator, assign or consume it and check deterministic yielded values instead of displaying its unstable object representation.

## Verify the response

Check every requested function independently:

- The complete definition is present in the requested position.
- Its decorators, signature, and original body remain verbatim.
- Removing the inserted docstring would restore the original definition exactly.
- The docstring is the first statement, and all documentation is inside it.
- The summary is one line, begins with an allowed capitalized word, and ends with permitted punctuation.
- Every applicable parameter appears once, in order, with its exact annotation.
- Every returned result is covered using the exact return annotation.
- Every applicable explicit raise is documented, and no inferred exception is listed.
- The sections are applicable, correctly ordered, and separated by exactly one blank line.
- The function has its own runnable, deterministic `>>>` doctest.

Finally, verify that the response contains only the requested complete function definitions, with no code fence or surrounding explanation.