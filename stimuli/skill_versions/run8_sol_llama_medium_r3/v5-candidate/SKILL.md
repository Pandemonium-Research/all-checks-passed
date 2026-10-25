---
name: docstring-api
description: Use when adding complete Google-style docstrings and runnable doctests to named public Python functions while preserving their signatures, executable bodies, order, and behavior.
---

# Add docstrings to named public functions

The supplied module is already correct. For each named public function, insert one complete Google-style docstring as its first statement. Make no other change.

Return only the complete definitions of the named functions, in the requested order. Do not include imports, unrelated definitions, Markdown fences, or explanatory text.

## Preserve the source

For each named function:

1. Copy the complete definition exactly once.
2. Preserve the signature verbatim.
3. Insert the docstring immediately before the first original executable statement.
4. Preserve every original executable statement verbatim and in its original order.
5. Include the full body; never replace code with `...`, `pass`, or another placeholder.

Deleting the added docstring from the response must reproduce the supplied function definition. Never repeat a function to add or correct documentation.

## Format the docstring

Use a multiline triple-double-quoted docstring. Put the one-line summary on the same line as the opening quotes. Put the closing quotes on their own line immediately before the first original executable statement.

All sections, `>>>` prompts, and expected outputs must appear before the closing quotes. Never place documentation after the docstring, after a `return`, between definitions, or in a second copy of the function.

Use exactly one blank line between the summary and the first section and between sections. Do not put a blank line immediately before the closing quotes or between the closing quotes and the first original statement. Use `r"""..."""` when the docstring contains backslashes that Python would otherwise interpret.

## Write the summary

Begin with a one-line imperative summary that:

- starts with a capital letter;
- ends with `.`, `!`, or `?`;
- describes the function without repeating its signature; and
- begins with one of these recognized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, `Validate`.

## Add sections

Use applicable sections in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is mandatory for every named function. Include the other sections when applicable. Indent each entry four spaces beyond its section label.

### Args

Document every signature parameter except `self` and `cls`. List parameters exactly once, in signature order, using their exact names.

For an annotated parameter, copy the annotation text from the signature exactly:

    parameter_name (ExactAnnotation): Explain what the parameter represents or controls.

For an unannotated parameter, do not invent a type:

    parameter_name: Explain what the parameter represents or controls.

Do not omit optional parameters, add nonexistent parameters, rename parameters, or reuse parameters from another function. Describe meaningful accepted values and the effects of flags or modes supported by the implementation.

### Returns

Include `Returns:` whenever the function returns a value. For an annotated return value, copy the return annotation exactly:

    ExactReturnAnnotation: Explain what the returned value means.

Inspect every return path. For a Boolean result, state both when the function returns `True` and when it returns `False`. Omit `Returns:` only when the function has no value return.

### Raises

Inspect the original function body for explicit `raise` statements. Document every explicitly raised exception type and the exact condition that triggers it:

    ExceptionType: Explain the condition that causes the exception.

Do not list exceptions that could arise only incidentally from an operation or called function. Omit `Raises:` when the body contains no explicit `raise`.

### Examples

Give every named function its own `Examples:` section containing at least one runnable `>>>` doctest that calls that function.

Validate each doctest against that function alone:

1. Confirm that the called name is the function being documented.
2. Compare the call with its preserved signature.
3. Use only positional and keyword arguments accepted by that signature.
4. Trace the supplied values through the actual body, including defaults, early returns, conversions, flags, and regular expressions.
5. Show the exact Python representation of the result.

Do not infer output from the function name, annotation, or a similar function. Use deterministic inputs. If a concrete result can vary, test a deterministic property instead. Verify every included doctest, not only the first one.

## Final verification

Before responding, check each named function independently:

- It appears exactly once and in the requested order.
- Its signature and complete original executable body are unchanged.
- Its docstring is the first statement.
- Its summary follows the required form.
- Every parameter is documented once, in signature order.
- Every return value and explicitly raised exception is documented.
- Its own `Examples:` section is inside its docstring.
- Every doctest uses a valid call and exact expected output.

Finally, confirm that the response contains only the requested complete function definitions, parses as Python, and has passing doctests.