---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to named public Python functions when their signatures, executable code, full bodies, and requested order must remain unchanged.
---

# Add docstrings to named public functions

## Output contract

Return only the complete definitions of the named public functions, in the order listed in the request.

For each named function:

- Copy its decorators, signature, annotations, and full body verbatim.
- Insert exactly one docstring as the first statement in its body.
- Preserve every executable statement, including nested definitions, in its original order and form.
- Do not add docstrings to nested functions unless they are separately named in the request.
- Never replace body content with `...`, `pass`, comments, or another placeholder.

Do not output imports, unrelated definitions, Markdown code fences, headings, notes, or commentary. Removing the inserted docstrings from the response must leave the original requested definitions unchanged.

## Docstring format

Use an indented, multiline, triple-double-quoted Google-style docstring with these parts in order:

1. One-line summary
2. `Args:` when applicable
3. `Returns:` when applicable
4. `Raises:` when applicable
5. `Examples:`

Separate the summary and every included section with exactly one blank line. Put the closing triple quotes on their own line, immediately before the function's original first statement.

Use ordinary `"""` delimiters. Use `r"""` only when the docstring contains backslashes that Python would otherwise interpret as escape sequences.

## Summary

Write one imperative sentence describing the behavior implemented by the function.

Begin with the capitalized form of exactly one approved verb:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

Describe the complete observed behavior without narrowing or exaggerating it. For example, if non-string input produces `False`, describe checking a value rather than claiming that the function accepts only strings or raises for non-strings.

Do not repeat the signature, mention these documentation instructions, expose implementation details unnecessarily, or claim behavior unsupported by the body.

## Args section

Include `Args:` when the signature contains parameters other than `self` or `cls`.

Document every eligible parameter exactly once and in signature order. Use its exact identifier and do not invent parameters.

For an annotated parameter, use:

    name (annotation): Description.

Copy the annotation text exactly from the signature. Do not simplify, expand, qualify, or infer a different type.

For an unannotated parameter, use:

    name: Description.

Describe the parameter's actual role, supported values, relevant constraints, and any default that changes behavior. Derive these facts from the signature and body. Distinguish between invalid input that causes a normal result such as `False` or `None` and invalid input that reaches an explicit `raise`.

## Returns section

Include `Returns:` when the function explicitly returns a value, yields values, or returns a generator or iterator object.

For an annotated return, use:

    annotation: Description.

Copy the return annotation exactly from the signature. Describe every meaningful result represented by the implementation, including parameter-controlled variants and sentinel results such as `False` or `None`.

For generators and iterators, describe the values produced and any relevant ordering or endpoint behavior. Do not describe an explicitly raised exception as a return value.

Omit `Returns:` only when the function has no value-returning or yielding behavior.

## Raises section

Document all and only exceptions produced by explicit `raise` statements within the complete named function definition.

Inspect nested helpers defined inside the named function. Include an exception explicitly raised by a nested helper when the named function invokes that helper as part of its behavior.

For each applicable exception type, use:

    ExceptionType: Exact condition that triggers the explicit raise.

Document each exception type once. Combine all triggering conditions when several explicit branches raise the same type.

Do not infer a `Raises:` entry from:

- A parameter annotation, function name, or validation-like purpose.
- A call to another separately defined function.
- An operator, conversion, parser, regular expression, or library operation.
- An exception type that appears only in an `except` clause.
- Invalid input that is handled by returning a value.
- The possibility that Python could raise an incidental runtime exception.

Omit `Raises:` when there is no applicable explicit `raise`. Never write an entry such as “Not applicable.”

## Examples section

Every named function must have its own `Examples:` section containing at least one runnable `>>>` doctest that directly calls that function.

Before writing an example, verify the function's exact name, parameters, defaults, and behavior from its definition. Each doctest must:

- Call the function whose docstring contains it.
- Pass only arguments accepted by that function's signature.
- Use inputs supported by the implementation.
- Run in the module's normal doctest namespace without imports, files, network access, user interaction, or unstated setup.
- Match Python's displayed output exactly, including type, capitalization, quoting, collection syntax, and ordering.
- Avoid duplicate calls unless they demonstrate different documented behavior.

Use literal expected output only when the implementation guarantees that exact result.

For random, UUID-generating, time-dependent, environment-dependent, or otherwise variable results, call the function once, assign the result, and test properties guaranteed by the implementation. Suitable properties include type, length, format, range, or membership constraints. Never invent a particular variable result.

For a finite generator or iterator, consume it with a deterministic operation such as `list(...)` only when the chosen inputs guarantee the exact resulting sequence.

An example that intentionally raises must match doctest traceback formatting exactly. Prefer a successful deterministic example when exception output is unnecessary.

## Final verification

Check every named function independently:

- The complete original definition is present in the requested position.
- Its decorators, signature, annotations, nested definitions, and executable statements are unchanged.
- Its docstring is the first body statement and the only inserted content.
- Its summary starts with an approved capitalized verb and ends with valid punctuation.
- Every eligible parameter appears once, in signature order, with its annotation copied exactly.
- `Returns:` covers the function's actual value-returning or yielding behavior.
- `Raises:` includes every applicable explicit raise and no inferred exceptions.
- `Examples:` directly calls the correct function using its real signature.
- Every doctest is runnable and every expected result is guaranteed by the implementation.
- No variable output has been fabricated.
- The response contains no imports, unrelated definitions, placeholders, code fences, or commentary.