---
name: docstring-api
description: Add complete Google-style docstrings and runnable doctests to specified public Python functions while preserving every signature, executable statement, function order, and behavior.
---

# Add docstrings to named public functions

The supplied module is already correct. Add only a docstring to each named public function.

Return only the complete definitions of the named functions, in the requested order. Do not include imports, unrelated definitions, Markdown code fences, or explanatory text.

## Preserve the source exactly

For each named function:

1. Copy its complete definition exactly once.
2. Preserve its signature verbatim.
3. Preserve every original executable statement verbatim and in its original order.
4. Insert one docstring as the first statement in the function body.
5. Include the full body; never replace it with `...`, `pass`, or another placeholder.

After removing the newly added docstring, the returned definition must match the original definition exactly. Do not duplicate a function to add examples or revise its documentation.

## Put all documentation inside the docstring

Use a multiline triple-double-quoted docstring whose summary starts on the opening line:

    def function_name(...):
        """Check whether the value meets the required condition.

        Args:
            ...

        Returns:
            ...

        Raises:
            ...

        Examples:
            >>> function_name(...)
            ...
        """
        first_original_statement

The closing triple quotes must appear after the final doctest output and before the first original executable statement. Never place an example:

- after the closing triple quotes;
- after a `return` or other executable statement;
- between two function definitions; or
- in a second copy of the function.

Use a raw triple-double-quoted docstring, `r"""..."""`, when its text contains backslashes.

Do not put a blank line immediately after the opening quotes, immediately before the closing quotes, or between the closing quotes and the first original statement.

## Write the summary

Begin with a one-line imperative summary that:

- starts with a capital letter;
- ends with `.`, `!`, or `?`;
- describes the function without repeating its signature; and
- starts with one of these recognized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, `Validate`.

## Add sections in order

Use the applicable sections in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is mandatory for every named function. The other sections are included when applicable.

Use exactly one blank line between the summary and the first section and between consecutive sections. Indent each section entry four spaces beyond its label.

### Args

Document every signature parameter except `self` and `cls`. List each parameter exactly once, in signature order.

For an annotated parameter, copy the annotation text from the signature exactly:

    parameter_name (ExactAnnotation): Explain what the parameter represents or controls.

For an unannotated parameter, do not invent a type:

    parameter_name: Explain what the parameter represents or controls.

Do not rename parameters, omit optional parameters, add nonexistent parameters, or copy a parameter from another function. Describe important accepted values and the effects of flags or modes when the implementation supports them.

### Returns

Include `Returns:` whenever the function returns a value. Copy the return annotation exactly:

    ExactReturnAnnotation: Explain every possible result and what each outcome means.

Inspect every return path. For a Boolean return, describe both the `True` and `False` conditions. Omit `Returns:` only when the function has no value return.

### Raises

Inspect the preserved body for explicit `raise` statements. Document every explicitly raised exception type and the exact condition that triggers it:

    ExceptionType: Explain the condition that causes the exception.

Do not document exceptions that could arise only incidentally from operations or called functions. Omit `Raises:` when the function contains no explicit `raise`.

### Examples

Give every named function its own `Examples:` section with at least one runnable `>>>` doctest that calls that same function.

Before including an example:

1. Compare the call with the preserved signature.
2. Confirm that every keyword argument exists in that signature.
3. Trace the supplied arguments through the actual implementation, including early returns, defaults, flags, conversions, and regular expressions.
4. Verify that the displayed output is the exact Python representation produced by the call.

Do not infer a result from the function's name, annotation, or a similar function. Use a deterministic call; when the concrete result can vary, test a deterministic property instead. Every additional doctest must also be valid and verified.

## Check the response

Before returning the definitions, verify each named function independently:

- The function appears exactly once and in the requested order.
- Its signature is unchanged.
- Its complete original executable body is unchanged.
- Its docstring is the first statement.
- The summary follows the required form.
- Every parameter is documented once, in signature order, with its exact annotation.
- Every return outcome is documented with the exact return annotation.
- Every explicitly raised exception, and no inferred exception, is documented.
- `Examples:` is inside the docstring.
- At least one doctest calls that function with only accepted arguments and exact output.

Finally, confirm that the complete response contains only the requested function definitions, parses as Python, and has passing doctests.