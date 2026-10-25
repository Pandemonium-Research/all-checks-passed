---
name: docstring-api
description: Use this skill when adding Google-style API docstrings to named public Python functions in this project — it defines the required docstring shape (summary line, Args/Returns/Raises/Examples), the mandatory runnable doctest, and the exact form of the returned output, without changing any code.
---

# API docstring notes

## What you return

Return only the complete definitions of the named public functions, in the order they were named.
Each definition is reproduced verbatim except that a docstring has been inserted as the first
thing inside the function.

- The source module is already correct. Do not modify executable code or signatures.
- Do not document unrelated functions, helper functions, private functions, or classes, even
  when they look like they need it. It is easy to expand the task while trying to be helpful.
- Keep each full executable body. Never replace a body with `...`, `pass`, or a comment.
- Every named function ends up with an `Examples:` block containing a runnable doctest, inside
  its docstring. There are no exceptions to this, however long the list of functions is.
- Emit raw Python only. No Markdown code fences (` ``` `), no headings, no prose before, between,
  or after the definitions. The whole answer is one continuous block of Python: definitions
  follow one another directly, separated only by a blank line.

## The four ways this task is usually failed

Read these before you start; the rest of this document is mostly about avoiding them.

1. The summary line is pushed onto the line below the opening `"""` instead of starting on the
   same line. See *Summary line*.
2. A function has no `Examples:` block at all — usually functions late in a long list, or short
   predicates and one-line delegators that felt too obvious to demonstrate. See *Examples*.
3. The `>>>` lines are written *below* the function body instead of inside the docstring, which
   turns them into stray statements that do not parse. See *Examples*.
4. A `raise` in the body has no matching `Raises:` entry, or code fences leak into the output.
   See *Raises* and *What you return*.

## The shape of one docstring

Every named function gets a docstring built on this shape. The illustration below shows placement
and spacing only; write real content drawn from the actual signature and body.

```
def convert_ratio(numerator: int, denominator: int) -> float:
    """Convert two integers into their quotient as a float.

    Args:
        numerator (int): Value divided into parts.
        denominator (int): Number of parts; must not be zero.

    Returns:
        float: The quotient of the two arguments.

    Raises:
        ZeroDivisionError: If ``denominator`` is zero.

    Examples:
        >>> convert_ratio(3, 4)
        0.75
    """
    if denominator == 0:
        raise ZeroDivisionError("denominator must be non-zero")
    return numerator / denominator
```

(The fences above delimit the illustration for you. Your own output contains no fences.)

Mechanics that this shape encodes:

- Triple double quotes. The docstring is the first statement in the function, before any
  executable line.
- Indent the docstring to match the function body; indent section entries one further level.
- The closing `"""` sits on its own line. No blank line immediately before it, and no blank line
  between it and the first executable statement.
- Exactly one blank line between the summary and the first section, and between each pair of
  sections. Never two.
- Applicable sections appear in this order and no other: `Args:` → `Returns:` → `Raises:` →
  `Examples:`. Omit an inapplicable section rather than inventing content for it.
- If the docstring contains a backslash, make it a raw docstring (`r"""`).

## Summary line

The summary text starts on the same line as the opening `"""`, with no space and no newline
between them.

- Wrong: `"""` followed by a newline, then `    Check whether the value is a string.`
- Right: `"""Check whether the value is a string.`

The habit of opening the quotes and dropping to the next line is the single most frequent defect
here, and it repeats across every function once it starts. Type the first word of the summary
immediately after the third quote character, every time.

The summary is one imperative line. Start it with a capital letter and end it with `.`, `!`, or
`?`. Do not restate the signature. Its first word must be a capitalized form of one word from
this set:

`add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`

## Args

`Args:` is an exact inventory, not a selective explanation.

- List every parameter in signature order, excluding `self` and `cls`.
- Use exactly the signature's parameter names. Add no names that are not in the signature, and
  omit none that are.
- Annotated parameter: `name (annotation): description`, with the annotation text copied exactly
  from the signature, including `Optional[...]`, `List[...]`, and so on.
- Unannotated parameter: `name: description`. Do not invent a type.
- The code annotations are not a substitute for the type text here; write the types out even
  though the signature already carries them.
- Describe what the value means, rather than restating its name.

## Returns

- If the body returns a value, write `Returns:` with `type: description`, where `type` matches
  the return annotation exactly.
- If the function returns no value, omit the section entirely.

## Raises

`Raises:` is also an exact inventory, and it is easy to skip by accident. Scan the whole body for
`raise` statements before you decide.

- One entry per exception raised explicitly in that function's body, as
  `ExceptionType: condition`.
- Include exceptions raised from inside `if`, `try`, `except`, or nested blocks — anywhere a
  literal `raise` appears in the body. A one-line guard clause near the top of an otherwise short
  body is still a `raise` and still needs an entry.
- Do not list exceptions the body does not explicitly raise, including ones that a function it
  calls might raise.
- Say what condition triggers the error, rather than restating the exception name.
- If the body contains no `raise` statement, omit the section.

## Examples

Every named public function needs its own `Examples:` section with at least one runnable `>>>`
doctest. A function with no doctest is a failed entry, and so is a doctest written in the wrong
place.

The `Examples:` block lives **inside** the docstring, after `Raises:` and above the closing `"""`.

- Wrong: the docstring closes, the body follows, and then `>>>` lines appear underneath the body
  or after the definition. Those lines are not documentation; they are stray statements that
  break the file.
- Right: the `>>>` lines sit above the closing `"""`, indented one level under `Examples:`, and
  the body begins only after the docstring has closed.
- No `>>>` line may appear anywhere outside a docstring, at module level, or between definitions.

Content rules:

- Doctests are executable, not illustrative. Each must run successfully, and the expected output
  written under it must match the real output character for character — including quotes on
  strings, `True`/`False` capitalization, and float formatting.
- A doctest runs in the module's own namespace. Call the function directly and use only builtins
  and names the module already defines or imports. Do not invent fixtures, objects, or imports
  that the module does not provide.
- A call that evaluates to `None` prints nothing, so write no expected-output line beneath it.
- Choose a deterministic call. When the concrete result varies or is unwieldy, assert a
  deterministic property of it instead (for example, its type, its length, or a comparison that
  prints `True`).
- Prefer a call that returns normally. If you do demonstrate an exception, the expected output
  must be a real doctest traceback block (`Traceback (most recent call last):`, an ellipsis line,
  then the exception line); when in doubt, doctest the non-raising path instead.
- Every named function needs one, including short one-line functions, predicates, and functions
  that mostly delegate to a helper. "Obvious" is not an exemption: a two-line predicate and a
  one-line wrapper around a private class each get their own example. Near-identical sibling
  functions each need their own example exercising that specific function by name.

## Working through the list

Handle the named functions one at a time, and finish each one completely before moving to the
next. Write each `Examples:` block as you write that docstring rather than planning to add them
at the end. A long list of functions is still a list of individually complete definitions;
quality does not taper off toward the end.

For each named function, in the order given:

1. Copy the `def` line and the entire body exactly as they appear in the source.
2. Read the body once, noting what it returns and every `raise` it contains.
3. Open `"""` and write the summary on that same line, then `Args:`, `Returns:`, and `Raises:`
   as applicable.
4. Write the `Examples:` block, then close the docstring with `"""` on its own line.
5. Confirm the body now starts immediately below that closing `"""`, unchanged and unabridged.

Step 5 is what keeps doctests from drifting past the end of the function. If you find yourself
writing a `>>>` line and the docstring is already closed, the docstring closed too early — move
the closing quotes down instead of leaving the example outside.

## Before you finish

Reread each definition you are about to return and confirm:

1. Every named function is present, in the order listed, and nothing extra is.
2. Each signature and each executable statement is unchanged; no body was shortened.
3. Each docstring's summary begins immediately after `"""` on the same line — check this one
   function at a time, not by spot check — starts with an approved capitalized verb, and ends
   with `.`, `!`, or `?`.
4. `Args:` names match the signature exactly; annotations are copied exactly.
5. `Returns:` is present exactly when a value is returned; `Raises:` matches the body's `raise`
   statements exactly, including guard clauses.
6. Count the functions, then count the `Examples:` blocks. The two numbers are equal, every
   `>>>` line sits above a closing `"""`, and every doctest would pass.
7. Section order and single-blank-line spacing hold throughout.
8. The output is bare Python that parses — no fences, no commentary, nothing between definitions
   but a blank line.

Where one rule appears to pull against another, prefer the exact evidence in the signature and
body over any guess about names, types, values, or exceptions, and prefer omitting a section over
inventing its contents.