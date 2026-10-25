---
name: docstring-api
description: Notes for supplying the project's expected help text around selected Python callables, including types, outcomes, failures, examples, and source-preservation constraints.
---

# Notes about function help

## Background

The accumulated habit is the Google docstring convention. The habit applies to the named public
functions only, even though people sometimes call these targets selected callables, exported
routines, or simply the requested functions. Do not document unrelated functions. The module is
working input rather than an invitation to refactor. Within the returned definitions: Do not
modify executable code or signatures.

There is a presentation sentence at the beginning of each help block. It is a one-line imperative
summary. Start it with a capital letter, end it with punctuation, specifically `.`, `!`, or `?`,
and do not repeat the function signature there. Capitalize one locally recognized first word from
this pipe-delimited set:
`add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.
The opening is a summary, not a declaration copied out of the source. Put the summary immediately
after the opening triple quotes, with no surrounding whitespace.

The longer record has a few labeled neighborhoods. `Args:` is where the
inputs are recorded, `Returns:` is about the result, `Raises:` covers failures, and `Examples:`
holds executable samples. Put a blank line between the summary and each section, using exactly one
blank line at each break. When several are applicable their conventional arrangement is `Args:` →
`Returns:` → `Raises:` → `Examples:`. Use spaces and the standard indented Google layout:
indent the docstring to match the function body and indent section entries one additional level.
Use triple double quotes, putting the closing triple quotes on their own line for a multiline
docstring. There is no blank line immediately before or after the docstring. Use a raw
triple-quoted docstring when it contains backslashes.

## Inputs, outputs, and errors

The input catalog must document every parameter. In `Args:`, follow signature order but leave out
`self` and `cls`; use exactly the signature's parameter names and no extra names. The typed shape
for an annotated input is `name (annotation): description`, and its type must match the signature
annotation exactly. An input with no annotation uses `name: description` rather than inventing a
type. Parameter and return types belong in the docstrings even though the signatures
already carry annotations.

The outcome paragraph is not unconditional. When the body returns a value, document every return
value in `Returns:` as `type: description`, and match the return annotation exactly. Do not add
`Returns:` for a function without a value return. The failure list is an exact body-derived set:
in `Raises:`, document every exception raised explicitly in the function body as
`ExceptionType: condition`, and no exception that the body does not explicitly raise. In this
context an error, failure, thrown condition, and exception may all be mentioned in discussion, but
the actual entry uses the exception class name and explains the condition that triggers it.

## Samples and checking

The examples neighborhood is not decorative. Add `Examples:` with at least one runnable `>>>`
doctest per named public function. Every doctest must execute successfully and its expected output
must match exactly. A demonstration elsewhere in the file does not cover the requested routine;
the sample sits in that routine's own docstring. Prefer a deterministic call. Where a function
varies by time, randomness, or environment, test a deterministic property so that the expected
line is stable.

People use "doc block," "API note," "function help," and "docstring" for the same artifact in
casual review. Whatever it is called, infer its contents from the exact signature and function
body, not from assumptions. If two instructions seem awkward together, resolve ambiguities by
precedence and omit an inapplicable section rather than inventing material. The work may be done
in whatever sequence seems natural, but inspect names, annotations, returned values, explicit
raises, formatting, and runnable examples before considering the returned definitions finished.

Return only the complete definitions of the named public functions, in the order listed, with the
requested docstrings inserted. Keep their full executable bodies; do not replace them with `...`.
Include no code fence or surrounding explanation.
