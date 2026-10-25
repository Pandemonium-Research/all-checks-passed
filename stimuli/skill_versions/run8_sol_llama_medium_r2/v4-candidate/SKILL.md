---
name: docstring-api
description: Use when adding complete Google-style docstrings and runnable doctests to named public functions in an already-correct Python module without changing existing code, signatures, formatting, or requested function order.
---

# Document named public Python functions

Add one docstring to each named public function. The source module is already correct; do not fix, simplify, or otherwise edit it.

Return only the complete definitions of the named functions, exactly once each and in the requested order. Include every decorator, signature, executable statement, nested definition, comment, and blank line from each definition. The only permitted change is inserting the function’s docstring as its first statement.

Do not:

- Include imports, unrelated definitions, module-level text, commentary, or a code fence.
- Change formatting, decorators, signatures, annotations, defaults, comments, or executable statements.
- Add, remove, reorder, or rewrite existing statements.
- Replace any part of a function body with `...`, `pass`, or another placeholder.
- Place a function’s doctest outside that function’s own docstring.

## Inspect the implementation first

Before writing each docstring, trace the implementation’s default path, branches, validation, explicit `raise` statements, and value-returning paths.

Base every claim on the code, not on names, annotations, conventions, or likely intent. In particular:

- Determine which branch each declared default selects.
- For Boolean switches, distinguish the default behavior from the behavior enabled by the nondefault value.
- Distinguish an input quantity from the returned value’s length, units, encoding, or representation.
- Calculate relationships introduced by transformations such as encoding or hexadecimal conversion.
- Describe branch-dependent return formats and sentinel values.
- Do not claim standards compliance, validation semantics, accepted formats, or exceptions unless the implementation establishes them.
- Treat rejected input that returns `False`, `None`, or another value as a return case, not as a raised exception.

## Use the required docstring format

Use an indented multiline triple-double-quoted docstring. If the docstring contains a backslash, use raw triple-double quotes.

Place a one-line summary immediately after the opening quotes. Write one imperative sentence describing the function’s actual behavior without repeating its signature. Begin with one of these capitalized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

After the summary, include only the applicable sections in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line before each included section. Do not place blank lines between a section heading and its entries, between consecutive entries, immediately before the closing quotes, or between the docstring and the following statement. Put the closing triple quotes on their own line.

Use this layout:

    """Check whether the value satisfies the required condition.

    Args:
        value (Any): The value to examine.

    Returns:
        bool: Whether the value satisfies the condition.

    Examples:
        >>> function_name(valid_input)
        True
    """

Adapt every name, type, description, input, and result to the function being documented.

## Document every parameter

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every such parameter exactly once and in signature order. Copy its name and annotation character-for-character from the signature:

    Args:
        name (annotation): Description of the value.

For an unannotated parameter, omit the parentheses and type:

    Args:
        name: Description of the value.

Do not simplify, normalize, quote, or reformat annotations. Do not invent parameters or types.

Describe what the implementation uses each parameter to control. State established constraints, units, accepted values, and default behavior. Verify default behavior from the branch selected by the declared default; never describe a nondefault branch as the default. Do not describe an input count as the output length unless the implementation makes them equal.

## Document every returned value

Include `Returns:` whenever the function has a value-returning path. Copy the return annotation character-for-character from the signature:

    Returns:
        annotation: Description of the returned value.

Describe every behavior-dependent alternative, including differences in type, representation, format, length, shape, or sentinel value. State any input-to-output size relationship accurately.

A return annotation does not replace `Returns:`. Omit the section only when the function has no value-returning path.

## Document only explicit raises

Include `Raises:` only for exceptions produced by explicit `raise` statements in the named function’s implementation. An explicit raise inside a nested helper counts when the named function invokes that helper as part of its behavior.

Document each applicable exception type exactly once:

    Raises:
        ExceptionType: The exact condition that reaches the explicit raise.

Do not document:

- An exception merely because it appears in an `except` clause.
- Invalid input handled by returning a value.
- Possible exceptions from separate called functions, operators, parsing, conversion, imports, or other indirect behavior.
- Exceptions inferred from annotations, names, comments, or conventional expectations.

Do not write `Raises: None`. If there is no applicable explicit `raise`, omit the entire section.

## Add an exact, runnable doctest

Every named function’s own docstring must contain an `Examples:` section with at least one `>>>` doctest. A doctest in another function, a nested function, or module-level text does not count.

The doctest must run in the module’s normal doctest environment without adding imports or referring to undefined names. Every displayed output line must exactly equal Python’s representation of the evaluated result.

For deterministic functions, use an input with a small, exact, stable result.

For nondeterministic functions, including functions that produce random identifiers, random text, secrets, timestamps, or unordered output, do not display a plausible generated value. Instead, evaluate a deterministic property of one generated result, such as:

- Its type.
- Its exact length or shape.
- A required prefix, suffix, or structural property.
- Whether every character belongs to the implementation’s permitted character set.
- Another invariant guaranteed by the implementation.

Call the nondeterministic function only once within the property being checked. Calculate the expected property from the actual operations in the implementation, including transformations that change the input-to-output length. Use valid input and show the exact resulting Boolean, integer, or other stable value.

Do not:

- Invent or guess generated output.
- Show output with an unverified length, format, or character set.
- Compare separate nondeterministic calls as if they should match.
- Use illustrative output that would fail when executed.
- Use ellipsis output unless the doctest explicitly enables the required option.

Keep every prompt, continuation line, and expected-output line inside the docstring and indented beneath `Examples:`.

## Verify the response

Before returning, compare the response with the source and confirm:

- Every requested function appears exactly once and in the requested order.
- No unrequested definition or surrounding text appears.
- Every definition includes its complete body, including nested definitions.
- Every decorator, signature, annotation, default, comment, blank line, and executable statement is unchanged.
- Each docstring is the function’s first statement.
- Every parameter except `self` and `cls` is documented exactly once, in order, with its exact annotation.
- Every value-returning function has `Returns:` with its exact return annotation and all return alternatives described.
- `Raises:` includes all and only applicable explicit raises.
- Caught exceptions and value-returning rejection paths are not documented as raises.
- Every function has its own runnable `>>>` doctest.
- Every expected doctest result is exact and deterministic.
- No nondeterministic result has been fabricated.
- The returned Python parses successfully.
- The response contains only the complete requested function definitions, without a code fence or explanation.