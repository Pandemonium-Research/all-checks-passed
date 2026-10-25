---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to named public functions in an already-correct Python module. Use when the output must preserve all existing code and contain only the complete requested function definitions in their specified order.
---

# Document named public Python functions

Add one docstring to each named public function. Do not correct, simplify, or otherwise alter the source module.

Return each named function exactly once, in the requested order. Include every decorator, signature, nested definition, and executable statement. The only permitted change is inserting the docstring as the function body’s first statement.

Do not:

- Include imports, unrelated definitions, module-level text, commentary, or a code fence.
- Change existing formatting, decorators, signatures, annotations, defaults, or statements.
- Add, remove, reorder, or rewrite executable code.
- Replace any part of a function body with `...`, `pass`, or another placeholder.
- Place a function’s doctest outside its own docstring.

## Trace the implementation first

Before writing a docstring, follow every relevant branch in the function and record:

- What each parameter actually controls.
- Which behavior each declared default selects.
- Every value-returning path and how its result is represented.
- Every explicit `raise` statement and the exact condition that reaches it.
- Whether any returned value is nondeterministic.

Base documentation only on the implementation. Do not infer behavior from names, annotations, conventions, or likely intent.

In particular:

- Do not describe a nondefault branch as the default.
- Do not confuse an input quantity with the output’s length, units, or representation.
- Calculate any size change performed by encoding, hexadecimal conversion, or another transformation.
- Describe rejected input that returns `False`, `None`, or another value as a return case, not an exception.
- Do not claim standards compliance or validation rules that the code does not establish.

## Use this docstring structure

Use an indented multiline triple-double-quoted docstring. If its text contains a backslash, use raw triple double quotes.

Place the summary immediately after the opening quotes. Write one imperative sentence on one line that describes the function’s actual behavior without repeating its signature. Begin with one of these capitalized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`. Do not add a second introductory paragraph.

After the summary, include only the applicable sections in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line before each included section. Do not place blank lines between a section heading and its entries, between consecutive entries, immediately before the closing quotes, or between the docstring and the next statement. Put the closing triple quotes on their own line.

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

Adapt every name, annotation, description, input, and result to the function being documented.

## Document every parameter

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every such parameter exactly once and in signature order. Copy each parameter name and annotation character-for-character from the signature:

    Args:
        name (annotation): Description of the value.

For an unannotated parameter, omit the parentheses and type:

    Args:
        name: Description of the value.

Do not simplify, normalize, quote, or reformat annotations. Do not invent parameters or types.

Describe how the implementation uses each value. Include constraints, units, accepted values, and default behavior only when established by the code. Determine default behavior by tracing the branch selected by the declared default.

## Document every returned value

Include `Returns:` whenever the function has a value-returning path. Copy the return annotation character-for-character from the signature:

    Returns:
        annotation: Description of the returned value.

Describe every branch-dependent alternative, including differences in representation, format, length, shape, or sentinel value. State input-to-output size relationships accurately after tracing the operations that produce the result.

A return annotation does not replace `Returns:`. Omit the section only when the function has no value-returning path.

## Document only explicit raises

Include `Raises:` only for exceptions produced by an explicit `raise` statement in the named function. An explicit raise inside a nested helper counts when the named function invokes that helper.

Document each applicable exception type exactly once:

    Raises:
        ExceptionType: The exact condition that reaches the explicit raise.

An `except ExceptionType` clause is not an explicit raise. Do not document:

- Exceptions that are merely caught.
- Invalid input handled by returning a value.
- Possible exceptions from called functions, operators, imports, parsing, or conversions.
- Exceptions inferred from comments, names, annotations, or expected conventions.

Do not write `Raises: None`. Omit the section when there is no applicable explicit raise.

## Add an exact, runnable doctest

Every named function’s own docstring must contain an `Examples:` section with at least one `>>>` doctest.

The doctest must run in the module’s normal doctest environment without adding imports or using undefined names. Every displayed output must exactly equal Python’s representation of the evaluated result.

For a deterministic function, use an input with a small, stable result.

For a nondeterministic function, never display a generated value. Bind exactly one result and test a deterministic property guaranteed by the implementation:

    Examples:
        >>> result = function_name(valid_input)
        >>> isinstance(result, str)
        True

Adapt this pattern to the actual function. Verify the property from the code; suitable properties include the exact type, calculated length, structural format, or permitted character set. If the function returns an iterator or generator, consume enough of it to produce stable output instead of displaying its object representation.

Do not:

- Invent or guess random output.
- Use a plausible-looking value as expected output.
- Show output with an unverified length, format, or character set.
- call a nondeterministic function more than once to test one result.
- Use illustrative output that would fail if executed.
- Use ellipsis output unless the doctest explicitly enables the required option.

Keep every prompt, continuation line, and expected-output line inside the docstring and indented beneath `Examples:`.

## Verify before returning

Compare the final response with the source and confirm:

- Every requested function appears exactly once and in the requested order.
- No unrequested definition or surrounding text appears.
- Every definition contains its complete body, including nested definitions.
- Every decorator, signature, annotation, default, and executable statement is unchanged.
- Each docstring is the first statement of its function.
- Every parameter except `self` and `cls` is documented exactly once, in order, with its exact annotation.
- Every value-returning function has `Returns:` with its exact return annotation and all return alternatives described.
- `Raises:` contains all and only applicable explicit raises.
- Caught exceptions and value-returning rejection paths are not documented as raises.
- Every function has its own runnable `>>>` doctest.
- Every expected doctest result is exact and deterministic.
- No nondeterministic output has been fabricated.
- The returned Python parses successfully.
- The response contains only the complete requested function definitions, without a code fence or explanation.