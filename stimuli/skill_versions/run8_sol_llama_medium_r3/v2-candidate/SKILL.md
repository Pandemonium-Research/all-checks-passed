---
name: docstring-api
description: Use this skill when adding complete Google-style docstrings and runnable doctests to specified public Python functions while preserving their definitions and behavior exactly.
---

# Add docstrings to named public functions

The source module is already correct. Add only docstrings to the named public functions.

Return only the complete definitions of those functions, in the requested order. Do not include imports, unrelated functions, Markdown code fences, or explanatory text.

## Preserve each definition

For every named function:

1. Include it exactly once.
2. Preserve its signature verbatim.
3. Preserve every existing executable statement verbatim and in its original order.
4. Preserve the complete body; never replace code with `...`, `pass`, or another placeholder.
5. Insert the docstring as the first statement in the function body.
6. Do not place examples or any other text after the function body.

Do not duplicate a function to add or revise its documentation.

## Format the docstring

Use a multiline triple-double-quoted docstring. The summary begins on the same line as the opening quotes:

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

All sections and doctests must be inside the triple quotes. The closing triple quotes must appear after the final doctest and immediately before the first original statement. A doctest placed after the closing quotes, after a `return`, or between function definitions is invalid.

Use exactly one blank line:

- between the summary and the first section; and
- between consecutive sections.

Do not put a blank line immediately after the opening quotes, immediately before the closing quotes, or between the closing quotes and the first original statement.

Use a raw triple-double-quoted docstring, `r"""..."""`, when the docstring contains backslashes that Python would otherwise interpret.

## Write the summary

Start with a one-line imperative summary. It must:

- start with a capital letter;
- end with `.`, `!`, or `?`;
- describe the function rather than repeat its signature; and
- begin with one of these recognized verbs:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, `Validate`.

## Add sections in order

Include the applicable sections in this exact order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Indent each entry four spaces beyond its section label.

### Args

Document every signature parameter except `self` and `cls`. List parameters once each and in signature order.

For an annotated parameter, copy the annotation text exactly:

    parameter_name (ExactAnnotation): Explain what the argument controls or represents.

For an unannotated parameter, omit the type:

    parameter_name: Explain what the argument controls or represents.

Do not rename parameters, add nonexistent parameters, omit optional parameters, or infer a different type. Explain meaningful accepted values and the effects of flags or modes when the implementation supports them.

### Returns

Include `Returns:` whenever the function returns a value. Copy the return annotation exactly:

    ExactReturnAnnotation: Explain every possible result and what each outcome means.

Inspect all return paths. For a Boolean result, explain both the `True` and `False` conditions. Do not add `Returns:` when the function has no value return.

### Raises

Inspect the function body for explicit `raise` statements. Document every exception type explicitly raised by that function:

    ExceptionType: State the exact condition that triggers the exception.

Do not document exceptions that might arise incidentally from operations or called functions. Omit `Raises:` when the function contains no explicit raise.

### Examples

Every named function must have its own `Examples:` section containing at least one runnable `>>>` doctest that calls that same function.

Before writing the expected output, trace the preserved implementation from the supplied arguments through the relevant branches. Check defaults, accepted options, validation rules, conversions, regular expressions, and early returns. Do not infer output from the function name or from a similar function.

Each doctest must:

- call only parameters present in that function's signature;
- use arguments valid for the preserved implementation;
- execute in the module's normal environment;
- produce exactly the displayed Python representation;
- be deterministic; and
- remain inside that function's docstring.

When a concrete result can vary, demonstrate a deterministic property instead. Additional doctests may cover important flags or edge cases, but each must be independently correct. Never copy an example from another function or call a different function in place of the documented one.

## Final verification

Before returning the result, verify that:

- every requested function appears exactly once and in the requested order;
- no unrequested definition or surrounding prose appears;
- every signature and original executable statement is unchanged;
- every complete function body is present;
- each docstring is the first statement in its function;
- every parameter is documented once, in signature order, with its exact annotation;
- every returned outcome is documented with the exact return annotation;
- every explicitly raised exception, and no inferred exception, is documented;
- each function has an `Examples:` section inside its docstring;
- every doctest calls the correct function with a valid signature and exact expected output;
- the resulting Python parses; and
- the doctests pass.