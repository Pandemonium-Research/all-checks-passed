---
name: docstring-api
description: Use when adding complete Google-style API docstrings and runnable doctests to named public Python functions without changing their signatures, executable code, order, or behavior.
---

# Add docstrings to named public functions

The supplied module is already correct. Add one docstring to each named public function and make no other changes.

Return only the complete definitions of the named functions, in the requested order. Do not include imports, unrelated definitions, Markdown code fences, or explanatory text.

## Preserve the source

For each named function:

1. Include the function exactly once.
2. Preserve its signature verbatim.
3. Preserve every original executable statement verbatim and in its original order.
4. Include the complete body; never replace code with `...`, `pass`, or another placeholder.
5. Insert the docstring as the first statement, immediately before the first original statement.

After removing the added docstring, the definition must match the supplied definition exactly. Never duplicate a function to add examples or revise its documentation.

## Keep all documentation inside the docstring

Use a multiline triple-double-quoted docstring. Begin the summary on the same line as the opening quotes. Place the closing quotes after the final doctest output and immediately before the first original statement.

Every section, `>>>` prompt, and expected output must be between the opening and closing quotes. Never place documentation after a `return`, after the closing quotes, or between function definitions.

Use exactly one blank line between the summary and the first section and between consecutive sections. Do not place a blank line immediately before the closing quotes. Use a raw triple-double-quoted docstring, `r"""..."""`, if its contents include backslashes that Python would otherwise interpret.

## Write the summary

Start with a one-line imperative summary that:

- begins with a capital letter;
- ends with `.`, `!`, or `?`;
- describes the function without repeating its signature; and
- begins with one of these recognized verbs:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, `Validate`.

## Add Google-style sections

Use applicable sections in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is required for every named function. Include the other sections only when applicable. Indent every entry four spaces beyond its section label.

### Args

Document every parameter except `self` and `cls. List parameters exactly once, in signature order, using their exact names.

For an annotated parameter, copy the annotation text exactly:

    parameter_name (ExactAnnotation): Explain what the parameter represents or controls.

For an unannotated parameter, omit the type:

    parameter_name: Explain what the parameter represents or controls.

Do not omit optional parameters, invent parameters, rename parameters, or copy parameters from another function. Describe meaningful accepted values and the effects of flags or modes when the implementation supports them.

### Returns

Include `Returns:` when the function returns a value. Copy the return annotation exactly:

    ExactReturnAnnotation: Explain every possible result and what each result means.

Inspect every return path. For a Boolean result, describe both when the function returns `True` and when it returns `False`. Do not add `Returns:` to a function that has no value return.

### Raises

Document every exception type raised by an explicit `raise` statement in that function:

    ExceptionType: Explain the exact condition that triggers the exception.

Do not document exceptions that might arise only from operations or called functions. Omit `Raises:` when the function contains no explicit raise.

### Examples

Give each named function its own `Examples:` section with at least one runnable `>>>` doctest that calls that same function.

For every doctest:

1. Check the documented function’s signature.
2. Use only positional and keyword arguments accepted by that signature.
3. Trace the actual preserved implementation, including defaults, early returns, validation, conversions, flags, and regular expressions.
4. Show the exact Python representation of the result.
5. Keep the prompt and output inside the docstring.

Do not infer results from the function name, annotation, or behavior of a similar function. Use deterministic inputs. If the concrete result can vary, demonstrate a deterministic property instead. Verify every example independently, including additional examples for flags or edge cases.

## Verify the response

Before returning it, confirm that:

- every requested function appears exactly once and in the requested order;
- no unrequested definition or surrounding text appears;
- every signature and original executable statement is unchanged;
- every complete body is present;
- every docstring is the first statement in its function;
- every parameter is documented once, in signature order, with its exact annotation;
- every return outcome and explicitly raised exception is documented;
- every function has an `Examples:` section inside its docstring;
- every doctest calls the correct function with a valid signature and exact expected output;
- the response parses as Python; and
- all doctests pass.