---
name: docstring-api
description: Use this skill when adding complete Google-style docstrings and runnable doctests to specified public Python functions without changing their signatures, executable bodies, formatting, or requested order.
---

# Document named public Python functions

The source module is already correct. Add one docstring to each named public function and make no other change.

Return exactly one complete definition for each named function, in the requested order. Include every decorator, the signature, and the entire body, including nested definitions. Copy all existing source text verbatim except for inserting the docstring as the function body’s first statement.

Do not:

- Return a named function more than once.
- Include unrelated definitions, imports, module-level text, commentary, or a code fence.
- Change formatting, decorators, signatures, annotations, defaults, or executable statements.
- Add, remove, reorder, or rewrite executable statements.
- Replace any part of a body with `...`, `pass`, or another placeholder.
- Put a function’s doctest anywhere except its own docstring.

## Derive documentation from the implementation

Trace the function before writing its docstring. Account for its default argument paths, conditional branches, validation checks, explicit raises, and returned values.

Do not infer behavior solely from a parameter name or annotation. In particular:

- Verify which branch each default value selects.
- Distinguish an input quantity from the size or format of the returned value.
- Describe every return alternative selected by the function’s branches.
- Do not claim that a function raises an exception merely because it rejects input by returning a false value.
- Do not invent validation rules, standards compliance, output values, or exceptions that the implementation does not establish.

## Use this docstring structure

Use an indented multiline triple-double-quoted docstring. If the docstring text contains a backslash, use raw triple-double quotes.

Place the summary immediately after the opening quotes. Write one imperative sentence on one line that describes the function’s actual behavior without repeating its signature. Begin with one of these capitalized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`. Do not add another introductory paragraph.

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

Adapt all content to the function being documented. Do not reuse the sample names or values unless they genuinely apply.

## Document every parameter

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every such parameter exactly once and in signature order. Copy each parameter name and annotation character-for-character from the signature:

    Args:
        name (annotation): Description of the value.

If a parameter has no annotation, omit the parentheses and type:

    Args:
        name: Description of the value.

Do not simplify, normalize, quote, or reformat an annotation. Do not invent parameters or types.

Describe what each parameter controls based on the implementation. Include accepted values, constraints, units, and default behavior when the code establishes them. Confirm default behavior by tracing the branch taken by the signature’s default value; do not describe a nondefault branch as the default.

## Document every returned value

Include `Returns:` whenever the named function has a value-returning path. Copy the return annotation character-for-character from the signature:

    Returns:
        annotation: Description of the returned value.

Describe every behavior-dependent return alternative, including differences in representation, length, shape, or sentinel values. If an argument is measured in one unit and the result in another, state that relationship accurately.

A return annotation does not replace `Returns:`. Omit `Returns:` only when the function has no value-returning path.

## Document only explicitly raised exceptions

Include `Raises:` only for exceptions produced by explicit `raise` statements in the named function’s implementation. This includes explicit raises in a nested helper when the named function calls that helper as part of its execution.

Document each explicitly raised exception type exactly once:

    Raises:
        ExceptionType: The exact condition that reaches the explicit raise.

Do not document:

- Exceptions merely caught by an `except` clause.
- Invalid inputs that cause the function to return a value instead of raising.
- Possible exceptions from called functions, operators, parsing, conversions, imports, or other indirect behavior.
- Exceptions mentioned only in comments, names, or type annotations.

Do not write `Raises: None`. If the implementation has no applicable explicit `raise`, omit the entire section.

## Add a runnable doctest to every function

Every named function’s own docstring must contain an `Examples:` section with at least one `>>>` doctest. A doctest in another function, a nested function, or module-level text does not count.

Each doctest must run in the module’s normal doctest environment without adding imports or referring to undefined names. Its displayed output must exactly equal Python’s representation of the evaluated result.

For deterministic functions, use input with an exact, stable result.

For nondeterministic results—such as random identifiers, random text, timestamps, secrets, or unordered collections—never display a sample generated value. Test one deterministic property of a single generated result instead, such as:

- Its type.
- Its exact length or shape.
- A required prefix, suffix, or format.
- Whether all characters belong to a permitted set.
- Another stable invariant established by the implementation.

Prefer an expression whose output is predictably `True`, an exact integer, or another small stable value. Calculate expected lengths and formats from the implementation, including encodings that expand the output relative to the input. Ensure the chosen input passes all validation and cannot accidentally raise.

Do not:

- Guess what a random call will return.
- Use an output with a different length or character set from the implementation.
- Compare two separate nondeterministic calls as though they return the same value.
- Use ellipsis output unless the doctest explicitly enables a compatible option.
- Show output that is illustrative rather than exactly executable.

Keep every prompt, continuation line, and expected-output line inside the docstring and indented beneath `Examples:`.

## Verify before returning

Compare the final response against the source and confirm all of the following:

- Every requested function appears exactly once and in the requested order.
- No unrequested definition or surrounding text appears.
- Every decorator, signature, annotation, default, formatting choice, and executable statement is unchanged.
- Every function body is complete, including nested definitions.
- Each docstring is the first statement of its function.
- Every parameter except `self` and `cls` is documented exactly once, in order, with its exact annotation.
- Every value-returning function has `Returns:` with its exact return annotation and all return alternatives described.
- `Raises:` contains all and only exceptions from applicable explicit `raise` statements.
- A caught exception is not incorrectly documented as an explicitly raised exception.
- Every function has its own runnable `>>>` doctest.
- Every expected doctest result is exact and deterministic.
- No nondeterministic result has been fabricated.
- The returned Python parses successfully.
- The response contains only the complete function definitions, without a code fence or explanation.