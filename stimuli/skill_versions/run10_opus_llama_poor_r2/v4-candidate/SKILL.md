---
name: docstring-api
description: How to add complete Google-style docstrings to the public functions named in a task — which sections are mandatory, how to copy types out of the signature, which exceptions may be listed, how to write doctests whose expected output is actually correct, and how to return each function otherwise unchanged.
---

# Google-style docstrings for named public functions

## The job

You are given a working module and a list of public function names. For each named function, insert
one Google-style docstring as the first statement of its body. Change nothing else. Then return the
complete definitions of those functions.

The task may call these targets "selected callables," "exported routines," or "the requested
functions"; the artifact may be called a "doc block," "API note," "function help," or "docstring."
They all mean the same thing. Only the named functions get a docstring. Do not document, modify,
refactor, or return any other function in the module.

## Mandatory sections — check this first

Every docstring you write contains these parts, in this exact order:

1. **Summary line** — always.
2. **`Args:`** — whenever the signature has at least one parameter (other than `self`/`cls`).
3. **`Returns:`** — whenever the body returns a value.
4. **`Raises:`** — **only** when the body contains an explicit `raise`. Otherwise the section must
   not appear at all.
5. **`Examples:`** — **always, for every named function, with no exceptions.**

Extra prose is optional and never substitutes for a section: a sentence describing the arguments is
not `Args:`, a sentence describing the result is not `Returns:`, and a sentence describing the
behavior is not `Examples:`. If a function takes a parameter, it gets an `Args:` block listing it.
If it returns a value, it gets a `Returns:` block. If it can be called, it gets an `Examples:` block
containing at least one `>>>` line. Skip a section only when its trigger above is genuinely absent —
a zero-parameter function has no `Args:`, and a function whose body never raises has no `Raises:`.

Before you consider any function done, count its sections against this list.

## Summary line

- Put it immediately after the opening `"""`, on the same line, with no leading space and no blank
  line before it.
- One line, one sentence, imperative mood, ending in `.`, `!`, or `?`.
- Its first word must be one of these, capitalized:
  `Add|Build|Check|Clip|Compress|Convert|Count|Create|Decode|Detect|Encode|Format|Generate|Identify|Interpret|Iterate|Join|Normalize|Parse|Remove|Return|Reverse|Test|Transform|Validate`.
- Summarize what the function does; do not restate or paraphrase the signature.

## `Args:`

- List every parameter in the signature, in signature order. Omit `self` and `cls`.
- Use the parameter names exactly as written in the signature. Never add a name that is not a
  parameter (a nested helper's arguments are not parameters of the outer function), and never omit
  one because it "looks obvious."
- **Annotated parameter:** `name (annotation): description` — the text in parentheses must be the
  annotation copied character-for-character from the signature (`int`, `bool`, `str`, `Any`,
  `Generator`, `list[str]`, `str | None`). This holds even for broad annotations like `Any`.
  Do not translate the annotation into prose, do not add words such as "optional" inside the
  parentheses, and do not put the default value there — mention a default in the description
  instead ("Defaults to 1.").
- **Unannotated parameter:** `name: description`. Do not invent a type for it.
- Document `*args` and `**kwargs` under those names if they appear.
- Yes, the types are repeated even though the signature already carries annotations. That is
  intended.

## `Returns:`

- Include it when the body returns a value; omit it when the body has no value-returning `return`.
- Format: `annotation: description`, where `annotation` matches the signature's return annotation
  exactly (`str:`, `bool:`, `Generator:`).
- If the function returns a generator or iterator, keep the annotation as written and describe what
  it produces in the description.

## `Raises:`

This section is the second most common source of wrong docstrings. Follow it literally.

1. Scan the function body — including any helper functions defined inside it — for the literal
   keyword `raise`.
2. **If there are none, there is no `Raises:` section.** A function that only calls other functions,
   only evaluates a regex, only guards with `if ...: return False`, or only returns an expression
   raises nothing of its own, no matter how plausible a `ValueError` or a project-specific error
   class would look. A validation-flavored name, an `Any`-typed parameter, or a length/format check
   is not evidence of a raise. Do not add a section "for completeness."
3. `except SomeError:` is the opposite of a raise. A class that appears only in an `except` clause,
   a `try` block, or a comment must never be listed. Only the token following the keyword `raise`
   counts.
4. If there are some, list exactly those exception classes, spelled exactly as they appear after
   `raise`. Never name a class you did not read in the body.
5. Do not list exceptions that merely propagate from called code.

Format: `ExceptionType: condition that triggers it.` Describe the *actual* guard condition taken
from the code — the range, the type check, the comparison that fails — not a placeholder phrase.
"If an invalid value is passed for `n`." says nothing; "If `n` is not an integer between 1 and 100."
is a description. Use the exception class name, never a word like "error" or "failure."

## `Examples:`

**This is where most incorrect docstrings go wrong.** A doctest whose expected output does not match
what the interpreter would really print makes the whole entry wrong, even if every other section is
perfect. Work through the following steps for each example, in order.

### Step 1 — Decide whether the value can be shown at all

If the result depends on anything the interpreter does not fix in advance, **no literal result value
may appear in the expected output — not even a plausible, "representative," or "illustrative" one.**
Triggers include: `random`, `secrets`, `uuid`/`uuid4`, `os.urandom`, `token_hex`,
`choice`/`shuffle`/`sample`, the clock or dates, the environment or filesystem, object identity
(`id`, default `repr` with an address), and anything derived from those — hex encodings, digests,
base64, joins, slices, concatenations.

One nondeterministic ingredient contaminates the whole result. A UUID with its dashes stripped is
still a UUID; a random string cut to five characters is still random.

```
# WRONG — invented value; the real call prints something else every time
>>> make_token(8)
'f47ac10b'

# RIGHT — assign, then assert stable properties: type, length, character set, membership
>>> value = make_token(8)
>>> isinstance(value, str)
True
>>> len(value)
8
```

Assert a length only when you can derive it exactly from the code. If the function transforms the
input before returning — hex-encoding, for instance, produces two characters per byte, so the
returned length is not the number the caller passed — either do the arithmetic and use the true
result, or fall back to `isinstance(...)` → `True`, which is always safe.

Never write a literal UUID, token, random string, hex digest, timestamp, or memory address as
expected output.

### Step 2 — Hand-execute the call you are about to write

For deterministic values, do not write the output you expect the function to have; write the output
you have traced. Walk the body with the exact arguments in your example:

- **Use only this function's own signature.** Every positional argument must line up with a
  parameter of *this* function, and every keyword you type must be a name that appears in *this*
  signature. Never copy an argument list from a neighboring function because the two look similar —
  a keyword the function does not accept raises `TypeError`, and the entry is wrong.
- **Substitute the defaults.** If you pass fewer arguments than there are parameters, every omitted
  parameter takes its default. Evaluate the branch that those defaults select, not the one you were
  thinking about. A predicate with a `joiner='_'` default is being asked about underscores, whatever
  the string you passed looks like.
- **Run the validation guards first, in source order, with your literal numbers.** Evaluate each
  guard's boolean expression rather than judging it by feel. Guards that compare direction or sign
  are the usual trap: a negative step normally requires a start above the stop, and a positive step
  a start below it, so an example that reverses them raises instead of returning. Choose arguments
  that pass every guard, or document the raise deliberately (Step 4).
- **Check that loops terminate.** A loop that advances by a step and exits on `!=` or `==` only ends
  when it lands on the boundary exactly. Confirm your arguments reach the exit condition; if they
  step past it, the example hangs and is wrong.
- **Follow the real predicate.** For regex or comparison logic, decide the result by reading the
  pattern, not by intuition about the input. If you cannot determine the answer with certainty, pick
  a different, unambiguous input.
- Prefer plain, obvious calls over clever argument combinations. Two simple verified examples beat
  one elaborate unverified one, and one traced example beats a second one you guessed at.

### Step 3 — Write the output in interpreter form

Expected output must match what the REPL prints, character for character: quotes around strings,
capitalized `True`/`False`, full list/tuple/dict reprs. A statement that prints nothing gets no
expected-output line. Materialize generators and iterators, e.g. `>>> list(walk(3))` followed by the
resulting list.

### Step 4 — Optional: demonstrating an exception

You may show a raise, but only by reproducing the message exactly as the code formats it:

```
>>> clip_to_range(5, 9, 2)
Traceback (most recent call last):
    ...
ValueError: lowest must not exceed highest
```

When in doubt, prefer a plain successful call over a traceback.

### Scope

Every named function needs at least one runnable `>>>` doctest inside **its own** docstring, calling
**that** function. An example in another function's docstring or elsewhere in the module does not
count. Names imported at module level are available inside the doctest; if you need anything else,
import it on a `>>>` line first.

## Layout

- Indent the docstring to the function-body level; indent entries inside a section one further
  level.
- Exactly one blank line between the summary line and the first section, and exactly one blank line
  between consecutive sections.
- Use triple double quotes. For a multiline docstring, the closing `"""` sits on its own line at the
  docstring's indentation.
- No blank line immediately before or immediately after the docstring inside the body.
- Use a raw docstring (`r"""`) if the text contains a backslash.

## Shape to follow

```python
def clip_to_range(value: int, lowest: int = 0, highest: int = 10) -> int:
    """Clip a number into an inclusive range.

    Args:
        value (int): The number to clip.
        lowest (int): Lower bound of the range. Defaults to 0.
        highest (int): Upper bound of the range. Defaults to 10.

    Returns:
        int: The value moved inside the range, unchanged if already within it.

    Raises:
        ValueError: If lowest is greater than highest.

    Examples:
        >>> clip_to_range(15)
        10
        >>> clip_to_range(-4, lowest=-2)
        -2
    """
    if lowest > highest:
        raise ValueError('lowest must not exceed highest')
    return max(lowest, min(value, highest))
```

## What you return

- Only the complete definitions of the named public functions, in the order the task lists them.
- Each function verbatim apart from the inserted docstring: identical decorators, identical
  signature line, identical statements in identical order, including nested helper functions and
  their bodies. Do not add docstrings to nested helpers — that would alter the body.
- Full bodies. Never replace a body or any part of it with `...`, `pass`, or a comment.
- No imports, no other module code, no code fence, no explanation before or after.

## Final pass

Read each returned function and confirm, one line at a time:

- Summary line present, one sentence, opening verb from the approved list.
- Every parameter listed, in order, with the annotation copied exactly from the signature.
- `Returns:` present and matching the return annotation whenever a value is returned.
- `Raises:` lists exactly the classes that appear after a literal `raise` in the body — and is
  absent entirely if there are none. No class taken from an `except` clause.
- `Examples:` present, and for every `>>>` line: the call uses only parameter names from this
  function's own signature; the arguments pass every guard in the body; and the expected output is
  either one you traced through the code with the real defaults, or a property assertion because the
  value is nondeterministic. No literal UUID, token, random string, hex digest, or timestamp
  anywhere in the block.
- Body byte-for-byte unchanged.