---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to named public functions in an already-correct Python module. Use when signatures, executable bodies, source formatting, and requested function order must remain unchanged and the response must contain only those complete function definitions.
---

# Document named public Python functions

The source module is already correct. Add one docstring to each named public function and make no other change.

Return exactly one complete definition for every named function, in the requested order. Include every decorator, signature, statement, nested definition, comment, and blank line belonging to each function. Copy the existing source verbatim except for inserting the docstring as the function body’s first statement.

Do not:

- Return a named function more than once.
- Include imports, unrelated definitions, module-level text, commentary, or a code fence.
- Change formatting, decorators, signatures, annotations, defaults, comments, or executable statements.
- Add, remove, reorder, or rewrite existing executable code.
- Replace any part of a function body with `...`, `pass`, or another placeholder.
- Put a doctest outside the function it documents.

## Trace the implementation

Before drafting each docstring, inspect the function’s actual operations, branches, default path, validation, explicit `raise` statements, and return paths. Base every claim and doctest expectation on the implementation rather than the function’s name, annotation, or likely intent.

In particular:

- Follow the branch selected by each declared default. Do not describe a nondefault behavior as the default.
- Describe Boolean switches and other branch controls using the behavior their values actually select.
- Keep input units distinct from output length, encoding, or representation.
- Calculate size changes introduced by loops, encodings, hexadecimal conversion, or other transformations.
- Describe string checks literally when the implementation performs prefix, regular-expression, or substring checks. Do not claim semantic validation or standards compliance that the code does not establish.
- Treat rejected input that returns `False`, `None`, or another value as a return case, not as an exception.
- Describe every branch-dependent return representation and sentinel value.

## Use this docstring structure

Use an indented multiline triple-double-quoted docstring. If its text contains a backslash, use raw triple-double quotes.

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

Adapt every name, annotation, description, input, and result to the function being documented. Do not copy sample names or values unless they genuinely apply.

## Document every parameter

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every such parameter exactly once and in signature order. Copy each parameter name and annotation character-for-character from the signature:

    Args:
        name (annotation): Description of the value.

If a parameter has no annotation, omit the parentheses and type:

    Args:
        name: Description of the value.

Do not simplify, normalize, quote, or reformat annotations. Do not invent parameters or types.

Describe what the implementation uses each parameter to control. State established constraints, units, accepted values, and default behavior accurately. Verify default behavior by tracing the branch selected by the declared default.

## Document every returned value

Include `Returns:` whenever the function has a value-returning path. Copy the return annotation character-for-character from the signature:

    Returns:
        annotation: Description of the returned value.

Describe every behavior-dependent alternative, including differences in type, representation, format, length, shape, or sentinel value. State input-to-output size relationships only after calculating them from the operations that produce the result.

A return annotation does not replace `Returns:`. Omit the section only when the function has no value-returning path.

## Document only explicit raises

Include `Raises:` only for exceptions produced by explicit `raise` statements in the named function’s implementation. An explicit raise inside a nested helper counts when the named function invokes that helper as part of its behavior.

Document each applicable exception type exactly once:

    Raises:
        ExceptionType: The exact condition that reaches the explicit raise.

Do not document:

- An exception merely because it appears in an `except` clause.
- Invalid input handled by returning a value.
- Possible exceptions from separate called functions, operators, imports, parsing, conversions, or other indirect behavior.
- Exceptions inferred from annotations, names, comments, or conventions.

Do not write `Raises: None`. If there is no applicable explicit `raise`, omit the entire section.

## Add an exact, runnable doctest

Every named function’s own docstring must contain an `Examples:` section with at least one `>>>` doctest. A doctest in another function, a nested function, or module-level text does not count.

The doctest must run in the module’s normal doctest environment without adding imports or referring to undefined names. Every displayed output line must exactly equal Python’s representation of the evaluated result.

For deterministic functions, choose an input with a small, exact, stable result.

For nondeterministic functions—including functions that produce random identifiers, random text, secrets, timestamps, or unordered output—never display or guess the generated value. Call the function once and check an invariant guaranteed by the implementation, for example:

    Examples:
        >>> result = function_name(valid_input)
        >>> deterministic_check(result)
        True

Replace `deterministic_check` with an expression that uses only names available in the module’s normal doctest environment. Suitable invariants include:

- The result’s type.
- Its exact calculated length or shape.
- A required prefix, suffix, or structural property.
- Whether all characters belong to the implementation’s permitted character set.
- Another stable relationship established by the implementation.

Calculate the expected invariant from the code. Account for transformations that change size, such as encodings or hexadecimal conversion. Count literal expected output carefully and ensure it agrees with the supplied input.

Do not:

- Show a plausible generated string as expected output.
- Use output with an unverified length, format, or character set.
- Compare separate nondeterministic calls as though they should match.
- Display a generator or iterator object representation; consume enough of it to obtain stable output.
- Use illustrative output that would fail when executed.
- Use ellipsis output unless the doctest explicitly enables the required option.

Keep every prompt, continuation line, and expected-output line inside the docstring and indented beneath `Examples:`.

## Verify before returning

Compare the final response with the source and confirm:

- Every requested function appears exactly once and in the requested order.
- No unrequested definition or surrounding text appears.
- Every definition includes its entire body, including nested definitions.
- Every decorator, signature, annotation, default, comment, blank line, and executable statement is unchanged.
- Each docstring is the function’s first statement.
- Every parameter except `self` and `cls` is documented exactly once, in order, with its exact annotation.
- Every value-returning function has `Returns:` with its exact return annotation and all return alternatives described.
- `Raises:` contains all and only applicable explicit raises.
- Caught exceptions and value-returning rejection paths are not documented as raises.
- Every function has its own runnable `>>>` doctest.
- Every expected doctest result is exact and deterministic.
- No nondeterministic result has been fabricated.
- The returned Python parses successfully.
- The response contains only the complete requested function definitions, without a code fence or explanation.