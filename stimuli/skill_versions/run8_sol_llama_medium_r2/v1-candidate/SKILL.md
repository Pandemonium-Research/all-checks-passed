---
name: docstring-api
description: Use this skill to add complete Google-style docstrings and runnable doctests to specified public Python functions while preserving their signatures, executable bodies, and output order exactly.
---

# Document named public Python functions

The source module is already correct. Add docstrings only to the named public functions.

Return exactly one complete definition for each named function, in the order requested. Include each function’s decorators, signature, and entire body. Copy all existing source text verbatim except for inserting the docstring as the first statement in the function body. Do not duplicate a definition, include an unrelated definition, change executable code, replace a body with `...` or `pass`, add imports, or include commentary or a code fence.

## Write the docstring

Use an indented, multiline, triple-double-quoted Google-style docstring. If the docstring contains backslashes, use raw triple double quotes.

Place the summary immediately after the opening quotes. The summary must:

- Be one imperative sentence on one line.
- Start with a capitalized word from this list: `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`, `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`, `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, or `Validate`.
- End with `.`, `!`, or `?`.
- Describe the function’s behavior without repeating its signature.

After the summary, include only the applicable sections in this order:

1. `Args:`
2. `Returns:`
3. `Raises:`
4. `Examples:`

Put exactly one blank line before every section. Do not put a blank line between a section label and its entries, between consecutive entries, immediately before the closing quotes, or immediately after the docstring. Put the closing triple quotes on their own line.

## Document arguments exactly

Include `Args:` when the signature has parameters other than `self` or `cls`.

Document every such parameter exactly once, in signature order. Use the parameter’s exact name and exact annotation:

```text
Args:
    name (annotation): Description of the value.
```

For an unannotated parameter, omit the parenthesized type:

```text
Args:
    name: Description of the value.
```

Do not invent, simplify, or reformat annotations. Describe the parameter’s meaning, relevant accepted values, and default behavior when useful; do not merely restate its name.

## Document return values exactly

Include `Returns:` if the body returns a value. Document every possible returned value and use the exact return annotation:

```text
Returns:
    annotation: Description of the returned value and any behavior-dependent alternatives.
```

Do not treat a signature annotation as a substitute for this section. Omit `Returns:` only when the function has no value return.

## Document explicit exceptions exactly

Include `Raises:` only for exceptions explicitly raised by a `raise` statement in that function’s body. Document every explicitly raised exception exactly once:

```text
Raises:
    ExceptionType: The precise condition that causes the exception.
```

Do not add `Raises: None`, document speculative exceptions from called functions, or omit an explicit `raise`.

## Add a runnable doctest to every function

Every named function’s own docstring must contain an `Examples:` section with at least one `>>>` doctest. A doctest in another function or at module level does not count.

Each example must be valid in the module’s normal doctest environment and must have exact expected output. Do not add imports or depend on undefined names.

For deterministic behavior, call the function with input whose result can be stated exactly. For nondeterministic behavior—such as random identifiers, random text, timestamps, or unordered results—do not guess or show one possible concrete result. Instead, test a deterministic property of the result, such as its type, length, format, membership, or a stable relationship, and show the exact result of that property check.

Keep all doctest lines inside the docstring, indented beneath `Examples:`:

```text
Examples:
    >>> deterministic_expression
    exact_output
```

## Verify the final output

Before returning the definitions, check all of the following:

- There is exactly one definition for every requested function and no other definition.
- The definitions appear in the requested order.
- Every signature, decorator, and executable statement is unchanged.
- Every full body is present.
- Every parameter and value return is documented with its exact annotation.
- `Raises:` lists all and only exceptions explicitly raised by that function.
- Every function has its own `Examples:` section and runnable doctest.
- Nondeterministic calls are checked through deterministic properties rather than fabricated output.
- The returned Python parses, and every doctest’s expected output matches its actual output.
- The response contains only the complete function definitions, with no code fence or surrounding explanation.