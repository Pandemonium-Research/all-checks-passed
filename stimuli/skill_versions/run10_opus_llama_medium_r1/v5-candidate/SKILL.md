---
name: docstring-api
description: Use this skill when adding Google-style docstrings to named public Python functions, so the returned definitions carry a complete Args/Returns/Raises/Examples contract — including a passing doctest inside every docstring — with no change to the existing code.
---

# API documentation notes

## What you return

The source module is already correct. Your only edit is inserting one docstring into each named
public function.

- Return the complete definitions of the **named** public functions, in the order listed.
- Every line other than the inserted docstring is verbatim from the source: same signature, same
  decorators, same executable statements, same order.
- Keep each full executable body. Never substitute `...`, `pass`, or an abbreviating comment.
- Document only the named public functions. Do not document, include, or touch anything else, even
  when a helper looks like it would benefit. Expanding the task is the most common way to fail it.
- Output the definitions and nothing else: no Markdown fences, no `python` language tags, no
  headings, no prose before or after. If you drafted your answer inside a fence, strip it.

## Work one function at a time

Handle the named functions as a sequence of independent, finished units. Take the first name,
build its complete definition — summary, `Args:`, `Returns:` if applicable, `Raises:` if
applicable, `Examples:`, then the original body — and only then move to the next name. Do not
sweep the list once for docstrings and plan a second pass for examples; a second pass is easy to
forget, and every failure of this task looks the same from the outside: docstrings that read well
but contain no `>>>` line.

## Where the docstring goes

The docstring is the first statement inside the function, on the line after the `def` line, and it
ends before the first executable statement. Nothing from the docstring may appear anywhere else.

Everything you write for a function — summary, `Args:`, `Returns:`, `Raises:`, and especially the
`>>>` examples — lives **between the opening and closing triple quotes**. Text placed after the
body's `return` is not a docstring; it is a syntax error or dead code, and it fails the task. After
the closing triple quotes, the very next line is the function's original first statement.

Build each definition in this order, so nothing lands outside the quotes: write the `def` line,
open the triple quotes, write the summary and every section including `Examples:`, close the triple
quotes, then paste the original body unchanged beneath them.

Use triple double quotes. Indent the docstring to match the function body, and indent section
entries one further level. A multiline docstring puts its closing triple quotes on their own line,
with no blank line immediately before them and none between them and the body. Use a raw
triple-quoted docstring (`r"""`) if the text contains backslashes.

## Summary line

The first text begins immediately after the opening triple quotes, with no leading space or
newline. Write one line, imperative mood, starting with a capital letter and ending in `.`, `!`,
or `?`. Do not restate the signature.

Capitalize one first word from this locally recognized set:
`add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.

Then one blank line before each following section. Exactly one blank line at each break. Applicable
sections appear in this order: `Args:` → `Returns:` → `Raises:` → `Examples:`.

## Args — an exact inventory

List every parameter in signature order, excluding `self` and `cls`. Use the signature's exact
parameter names, and no name that is not in the signature.

- Annotated parameter: `name (annotation): description`, with the annotation copied exactly from
  the signature, including `Optional[...]`, `List[...]`, unions, and defaults phrasing.
- Unannotated parameter: `name: description`. Do not invent a type.

The annotations in code do not excuse omitting the type text here; both carry it.

## Returns — conditional on behavior

If the body returns a value, write `Returns:` with `type: description`, the type matching the
return annotation exactly. If the function returns no value, omit the section entirely.

## Raises — an exact inventory

Document every exception raised by an explicit `raise` in that function's own body, as
`ExceptionType: condition`. Do not list an exception that only propagates from a call the function
makes, and do not list one the body never raises. If the body has no `raise`, omit `Raises:`.

Descriptions state what a value means or what condition triggers an error, rather than restating
the name.

## Examples — required for every named function, inside its own docstring

`Examples:` is not optional and not conditional. Each named public function gets its own
`Examples:` section containing at least one runnable `>>>` doctest, positioned as the last section
of that function's docstring, above the closing triple quotes.

Draft the doctest first. Before you type the summary for a function, read its body, pick a call,
work out the exact result, and write those `>>>` lines down. Then write the summary, `Args:`,
`Returns:`, and `Raises:` above them. The section you write first is the section you cannot
forget.

- One function's example never counts for another. A module-level example counts for none of them.
- A long list of functions does not relax the requirement, and neither does a body so small the
  behavior looks self-evident. The fifteenth function gets the same `Examples:` section as the
  first; short predicates, one-line wrappers, and thin delegations to a helper included.
- Every doctest must actually execute and its expected output must match character for character,
  including quotes on strings and `True`/`False` capitalization. Mentally run each line against the
  real body before writing the expected output.
- Choose a deterministic call that needs nothing outside the module — no files, network, clock, or
  randomness. When the concrete result varies, assert a deterministic property instead (for
  example, call the function and compare a length or a type).
- If a function raises, a second `>>>` line can show the error, written as a `Traceback (most
  recent call last):` block ending in the exception line — but only if you can reproduce that
  output exactly. Otherwise stay with the plain successful call.
- Continuation lines use `...`; blank output lines use `<BLANKLINE>`.

If you are about to write a closing triple-quote and the docstring has no `>>>` in it, stop and add
the `Examples:` section first.

## Shape to match

Shown indented four spaces for display only — do not copy that extra indent, and do not wrap your
answer in fences.

    def clip_text(text: str, limit: int = 8) -> str:
        """Clip a string to a maximum number of characters.

        Args:
            text (str): The string to shorten.
            limit (int): Maximum number of characters to keep.

        Returns:
            str: The leading characters of ``text``, at most ``limit`` of them.

        Raises:
            ValueError: If ``limit`` is negative.

        Examples:
            >>> clip_text('documentation', 4)
            'docu'
            >>> clip_text('short')
            'short'
        """
        if limit < 0:
            raise ValueError(limit)
        return text[:limit]

Note where each piece sits: the examples are inside the quotes, and `if limit < 0:` is the first
line after them.

## Resolving conflicts

Rely on exact signature and body evidence rather than guessing at names, types, values, or
exceptions. Where two rules seem to pull against each other, omit an inapplicable section rather
than inventing content — except that `Examples:` is never inapplicable.

## Before you answer, verify each returned definition

1. It is one of the named functions, and they appear in the order listed.
2. Signature, decorators, and every executable statement are unchanged, and the body is complete.
3. The docstring is the first statement, and nothing after the closing quotes belongs to it.
4. The summary is one line, starts with an approved capitalized verb, ends in `.`, `!`, or `?`.
5. `Args:` names match the signature exactly — none missing, none added.
6. `Returns:` present if and only if a value is returned; `Raises:` matches the explicit `raise`
   statements exactly.
7. `Examples:` is present with at least one `>>>` line, inside this function's docstring, and each
   expected output is what the code really produces.
8. The whole answer parses as Python, and contains no Markdown fences or explanatory text.

Then check the answer as a whole: count the docstrings that contain a `>>>` line. That count must
equal the number of named functions you were asked to document. If it is lower, go back to the
functions that are missing one and add their `Examples:` sections before answering. A near-miss —
every function documented but two of them without a doctest — is a failed answer, not a partial
one, so spend the extra pass rather than shipping it.