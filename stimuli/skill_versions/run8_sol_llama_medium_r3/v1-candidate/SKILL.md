---
name: docstring-api
description: Use this skill to add contract-compliant Google-style docstrings and runnable doctests to specified public Python functions while preserving their signatures, bodies, order, and behavior exactly.
---

# Add docstrings to named public functions

Return only the complete definitions of the named public functions. Follow these requirements exactly.

## Preserve the source

For each named function:

1. Return the function exactly once.
2. Keep the functions in the order listed by the task.
3. Preserve the signature verbatim.
4. Preserve every executable statement verbatim and in its original order.
5. Insert only the function's docstring.
6. Include the complete body; never replace code with `...`, `pass`, or another placeholder.

Do not return imports, unrelated functions, duplicate definitions, code fences, or explanatory text.

## Place the docstring correctly

Insert the docstring as the first statement inside the function. Everything described below, including all doctests, must appear between its opening and closing triple quotes.

Use this structure:

    def function_name(...):
        """Summary.

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

The closing triple quotes must come after the final doctest output and before the first original executable statement. Never place a doctest after the closing triple quotes or after a `return` statement.

Use triple double quotes. If the docstring contains a backslash, use raw triple double quotes: `r"""..."""`.

Do not put a blank line immediately after the opening triple quotes, before the closing triple quotes, or between the closing triple quotes and the first executable statement.

## Write the summary

The first docstring line must be a one-line imperative summary that:

- starts with a capital letter;
- ends with `.`, `!`, or `?`;
- does not repeat the function signature; and
- begins with one locally recognized verb from this set:

`Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, `Validate`.

## Add the sections

Include only applicable sections, in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Use exactly one blank line between the summary and the first section and between consecutive sections. Indent section entries four spaces beyond their labels.

### Args

Document every signature parameter in signature order, except `self` and `cls`. Do not omit parameters, add parameters, rename them, or describe arguments that the function does not accept.

For an annotated parameter, copy its annotation text exactly:

    parameter_name (ExactAnnotation): Meaning of the parameter.

For an unannotated parameter, do not invent a type:

    parameter_name: Meaning of the parameter.

Describe the parameter's meaning, including the effect of important flags, modes, or accepted values. Do not merely restate its name.

### Returns

Include `Returns:` when the function returns a value. Document every possible returned value or outcome.

Copy the return annotation exactly:

    ExactReturnAnnotation: Meaning of the returned value and its possible outcomes.

Do not add `Returns:` when the function has no value return.

### Raises

Inspect the function body for explicit `raise` statements. Document every exception type raised explicitly by that function and no others:

    ExceptionType: Exact condition that causes the exception.

Do not infer exceptions that could arise incidentally from called operations.

### Examples

Every named function must have its own `Examples:` section with at least one runnable doctest:

    Examples:
        >>> function_name(valid_arguments)
        expected_output

A doctest must:

- call the function whose docstring contains it;
- use only parameters accepted by that function's preserved signature;
- execute successfully in the module's normal environment;
- produce exactly the shown output;
- agree with the preserved implementation, including flags and edge cases; and
- be deterministic.

Do not copy an example from another function. Do not guess an expected result from the function's name alone; trace the implementation to verify it. If a concrete result can vary, demonstrate a deterministic property instead.

## Validate the final response

Before returning the definitions, check every named function:

- It appears exactly once and in the requested order.
- Its signature is unchanged.
- Its complete executable body is unchanged.
- Its docstring is the first statement.
- Every parameter is documented once, in signature order, with the exact annotation.
- Its return behavior is documented with the exact return annotation when applicable.
- Every explicitly raised exception is documented, with no invented exceptions.
- `Examples:` is inside the docstring.
- At least one doctest calls that function with a valid signature and has correct output.
- The resulting Python parses.
- The doctests pass.
- Nothing outside the requested function definitions is present.