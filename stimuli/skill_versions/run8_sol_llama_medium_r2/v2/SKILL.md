---
name: docstring-api
description: Use this skill to add complete Google-style docstrings and runnable doctests to specified public Python functions while preserving their signatures, executable bodies, and requested order exactly.
---

# Document named public Python functions

The source module is already correct. Add a docstring to each named public function and make no other change.

Return exactly one complete definition for every named function, in the order requested. Include its decorators, signature, and entire body. Copy all existing source text verbatim except for inserting the docstring as the function body’s first statement.

Do not:

- Return a named function more than once.
- Include unrelated functions, imports, or module-level text.
- Change, remove, reorder, or add executable statements.
- Change decorators, signatures, annotations, defaults, or formatting.
- Replace any part of a body with `...`, `pass`, or another placeholder.
- Put doctests outside the function they document.
- Add commentary or wrap the result in a code fence.

## Use this docstring structure

Use an indented multiline triple-double-quoted docstring. If its text contains a backslash, use raw triple double quotes.

Place the summary immediately after the opening quotes. Write one imperative sentence on one line that describes the function’s behavior without repeating its signature. Begin with one of these capitalized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.

End the summary with `.`, `!`, or `?`.

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

Adapt the content to the actual function. Do not copy the sample names or values unless they genuinely apply.

## Document every parameter

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every such parameter exactly once and in signature order. Copy each parameter name and annotation exactly as written in the signature:

    Args:
        name (annotation): Description of the value.

If a parameter has no annotation, omit the parentheses and type:

    Args:
        name: Description of the value.

Do not simplify, normalize, quote, or otherwise reformat an annotation. Do not invent parameters or types. Describe what each value controls, including accepted values, constraints, and default behavior when the function provides that information.

## Document every returned value

Include `Returns:` whenever the function body returns a value. Copy the return annotation exactly as written in the signature:

    Returns:
        annotation: Description of the returned value.

Describe all behavior-dependent return alternatives. A return annotation in the signature does not replace this section. Omit `Returns:` only when the body has no value-returning path.

## Document only explicitly raised exceptions

Include `Raises:` only when the function’s own body contains an explicit `raise` statement. Document every explicitly raised exception exactly once:

    Raises:
        ExceptionType: The exact condition that triggers the raise.

Do not write `Raises: None`. Do not document possible exceptions from function calls, operators, imports, parsing, type conversion, or other indirect behavior unless the named function explicitly raises them. Do not omit an exception that appears in an explicit `raise`.

## Add a runnable doctest to every function

Every named function’s own docstring must contain an `Examples:` section with at least one `>>>` doctest. A doctest in another function or at module level does not count.

Each doctest must run in the module’s normal doctest environment without adding imports or relying on undefined names. Its displayed output must exactly match the evaluated expression’s representation.

For deterministic functions, choose inputs with an exact, stable result. For nondeterministic results such as random identifiers, random strings, timestamps, or unordered collections, never display an invented example result. Instead, test a deterministic property, such as:

- The result’s type.
- Its length or shape.
- Its required format.
- Membership in a permitted character set.
- A stable relationship between the input and output.

Prefer a single expression whose result is predictably `True`, an exact integer, or another stable value. Ensure the example satisfies the function’s actual validation rules and does not accidentally raise an exception.

Keep every prompt, continuation line, and expected-output line inside the docstring and indented beneath `Examples:`.

## Verify before returning

Check the final response against the source:

- Every requested function appears exactly once.
- No unrequested definition or other surrounding text appears.
- Definitions are in the requested order.
- Every decorator, signature, annotation, default, and executable statement is unchanged.
- Every function body is complete.
- Each docstring is the first statement of its function.
- Every parameter except `self` and `cls` is documented exactly once with its exact annotation.
- Every value-returning function has `Returns:` with its exact return annotation.
- `Raises:` contains all and only exceptions explicitly raised in that function’s body.
- Every function has its own runnable `>>>` doctest.
- Every expected doctest result is exact and deterministic.
- The returned Python parses successfully.
- The response contains only the complete function definitions, without a code fence or explanation.