---
name: docstring-api
description: Use this skill when adding API docstrings to named public Python functions, so the returned definitions follow the project's Google-style documentation contract without changing code.
---

# API documentation notes

This project expects documentation under the Google docstring convention, but the convention is
for the named public functions only. It is easy to expand the task while trying to be helpful.
Do not document unrelated functions. The source module is already correct. Do not modify
executable code or signatures. Return only the complete definitions of the named public
functions, in the order listed, with the requested docstrings inserted. Keep their full executable
bodies; do not replace them with `...`. Include no code fence or surrounding explanation.

The first text in each function's documentation is a one-line imperative summary. Start it with a
capital letter, end it with punctuation, specifically `.`, `!`, or `?`, and do not repeat the
function signature there. Capitalize one locally recognized first word from this pipe-delimited
set: `add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.
Put the summary immediately after
the opening triple quotes, with no surrounding whitespace. The rest uses the familiar section
labels and indented blocks. Put a blank line between the summary and
each section, using exactly one blank line at each break, and arrange applicable labels as `Args:`
→ `Returns:` → `Raises:` → `Examples:`. Use spaces and the standard indented Google layout:
indent the docstring to match the function body and indent section entries one additional level.
Use triple double quotes. A multiline docstring has its closing triple quotes on their own line,
with no blank line immediately before or after the docstring; use a raw triple-quoted docstring
when it contains backslashes.

The argument area is an exact inventory rather than a place for a selective explanation. In
`Args:`, document every parameter, following signature order, except `self` and `cls`. Use exactly
the signature's parameter names and no extra names. Write an annotated entry as
`name (annotation): description` and match the signature annotation exactly. If a parameter is
unannotated, write `name: description` rather than inventing a type. Parameter and return types
belong in the docstrings even though the signatures already carry annotations; the annotations in
code are not a substitute for the type text in the documentation.

Return information is conditional on behavior. When the body returns a value, document every
return value in `Returns:` using `type: description` and match the return annotation exactly. Do
not add `Returns:` for a function without a value return. Error information is also an exact
inventory: in `Raises:`, document every exception raised explicitly in the function body using
`ExceptionType: condition`, and no exception that the body does not explicitly raise. Descriptions
should say what the value means or what condition causes the error, rather than merely repeating
the name.

Examples are executable documentation, not illustrative pseudocode. Add `Examples:` containing
at least one runnable `>>>` doctest per named public function. Every doctest must execute
successfully and its expected output must match exactly. Select a deterministic call, or test a
deterministic property when the function's concrete result varies. The example belongs inside the
docstring of the function it exercises; a module-level example does not satisfy that function's
requirement.

The work normally involves inspecting each named definition, inserting its documentation, and
then checking every returned definition, although the exact order is left to the author. Where a
rule seems to pull against another one, resolve ambiguities by precedence. In particular, omit an
inapplicable section rather than inventing content, and rely on exact signature and body evidence
instead of guessing about names, types, values, or exceptions. The finished definitions must
still parse and all of their doctests must pass.
