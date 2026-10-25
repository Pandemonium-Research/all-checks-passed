---
name: docstring-api
description: Use when asked to add complete Google-style docstrings and runnable doctests to specified public Python functions while returning only those complete definitions and preserving their source code and behavior.
---

# Add docstrings to named public functions

Treat the supplied module as correct. The only permitted edit is inserting one docstring as the first statement of each named public function.

Return only the complete definitions of the named functions, in the requested order. Do not return imports, unrelated definitions, commentary, or Markdown code fences.

## Preserve each definition

Process every named function independently:

1. Copy its complete definition exactly once, including any decorators.
2. Preserve its signature verbatim.
3. Insert the docstring immediately before its first original statement.
4. Preserve every original executable statement verbatim and in its original order.
5. Keep the full body; never replace any code with `...`, `pass`, or another placeholder.

Removing the added docstring must reproduce the supplied definition. Never repeat a function to add examples or correct an earlier docstring.

## Format the docstring

Use a multiline triple-double-quoted docstring. Put the one-line summary on the same line as the opening quotes. Put the closing quotes on its own line immediately after the final documentation line and immediately before the first original statement.

All section labels, entries, `>>>` prompts, and expected outputs must be inside the opening and closing quotes. Documentation placed after a `return`, after the closing quotes, or between function definitions is invalid.

Use exactly one blank line between the summary and the first section and between consecutive sections. Do not put a blank line immediately before the closing quotes or between the closing quotes and the first original statement. Use `r"""..."""` when the docstring contains backslashes that Python would otherwise interpret.

## Write the summary

Start with a one-line imperative summary that:

- begins with a capital letter;
- ends with `.`, `!`, or `?`;
- describes the function without repeating its signature; and
- begins with one of these recognized words:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, `Validate`.

## Add Google-style sections

Use applicable sections in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

`Examples:` is required for every named function. Include the other sections only when applicable. Indent each entry four spaces beyond its section label.

### Args

Document every signature parameter except `self` and `cls`. List parameters exactly once, in signature order, using their exact names.

For an annotated parameter, reproduce its annotation text exactly:

    parameter_name (ExactAnnotation): Explain what the parameter represents or controls.

For an unannotated parameter, omit the type:

    parameter_name: Explain what the parameter represents or controls.

Do not omit optional parameters, invent parameters, rename parameters, or copy parameters from another function. Describe the effect of defaults, flags, modes, and restricted values when the implementation supports them.

### Returns

Include `Returns:` when the function returns a value. Reproduce the return annotation exactly when one is present:

    ExactReturnAnnotation: Explain every possible returned result.

Inspect every return path. For a Boolean result, state both the condition that produces `True` and the condition that produces `False`. Omit `Returns:` only when the function has no value return.

### Raises

Inspect the original body for explicit `raise` statements. Document every explicitly raised exception type and its exact trigger:

    ExceptionType: Explain the condition that explicitly raises the exception.

Do not list exceptions that might arise only from an operation or called function. Omit `Raises:` when the function contains no explicit raise.

### Examples

Give each function its own `Examples:` section with at least one runnable `>>>` doctest that calls that same function.

Before including an example:

1. Confirm that the called name is the function currently being documented.
2. Compare every positional and keyword argument with that function's exact signature.
3. Trace the supplied values through its actual body, including defaults, early returns, conversions, exception handling, flags, and regular expressions.
4. Determine the exact Python representation of the result.
5. Run the doctest in the supplied module's context.

Do not infer behavior from the function name, annotation, or a similar function. Do not reuse another function's parameters or examples. Prefer the smallest deterministic example; add further examples only when their calls and outputs have also been verified. If a concrete result varies, demonstrate a deterministic property instead.

Keep every prompt and expected output before the docstring's closing quotes. Do not append examples after the executable body and do not create a second copy of the function to hold them.

## Verify the response

Check each named function separately:

- It appears exactly once and in the requested order.
- Its signature, decorators, and complete executable body are unchanged.
- Its single docstring is the first statement.
- Every parameter is documented once, in signature order.
- Every return outcome and explicitly raised exception is documented.
- Its `Examples:` section is inside its docstring.
- Every doctest calls that function using only accepted arguments.
- Every expected output matches the preserved implementation exactly.

Finally, confirm that the response contains only the requested complete definitions, parses as Python, and has passing doctests.