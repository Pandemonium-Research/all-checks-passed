---
name: docstring-api
description: How to add complete Google-style docstrings to the public functions named in a task — which sections are mandatory, how to copy types out of the signature, which exceptions to list, how to write doctests that actually pass, and how to return each function otherwise unchanged.
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
4. **`Raises:`** — whenever the body contains an explicit `raise`.
5. **`Examples:`** — **always, for every named function, with no exceptions.**

The single most common failure is writing a summary line plus a sentence or two of description and
stopping there. That is an incomplete docstring and it is wrong. Extra prose is optional and never
substitutes for a section: a sentence describing the arguments is not `Args:`, a sentence describing
the result is not `Returns:`, and a sentence describing the behavior is not `Examples:`. If a
function takes a parameter, it gets an `Args:` block listing it. If it returns a value, it gets a
`Returns:` block. If it can be called, it gets an `Examples:` block containing at least one `>>>`
line. Skip a section only when its trigger above is genuinely absent — for example, a
zero-parameter function has no `Args:`, and a function whose body never raises has no `Raises:`.

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

- List exactly the exceptions raised by an explicit `raise` statement in the function body —
  including `raise` statements inside helper functions defined within that body, since calling the
  function triggers them.
- Format: `ExceptionType: condition that triggers it.` Use the exception class name, not a phrase
  like "error" or "failure."
- Do not list exceptions that merely propagate from called code, and do not invent plausible ones
  (`TypeError`, `KeyError`) that the body never raises itself.

## `Examples:`

- Every named function needs at least one runnable `>>>` doctest inside **its own** docstring. An
  example in another function's docstring or elsewhere in the module does not count.
- Doctests must execute successfully, and expected output must match the interpreter's output
  exactly — including quotes on strings, `True`/`False` capitalization, and list/dict reprs.
- A statement that prints nothing gets no expected-output line.
- Names imported at module level are available inside the doctest; if you need anything else, import
  it on a `>>>` line first.
- **Deterministic results:** show the call and its literal output.
- **Nondeterministic results** (randomness, UUIDs, `os.urandom`, time, environment, hashing of random
  input): never print the value. Assert a stable property instead — its length, its type, its
  membership in an allowed set:

  ```
  >>> value = make_token(8)
  >>> len(value)
  8
  >>> isinstance(value, str)
  True
  ```

- **Generators:** materialize them, e.g. `>>> list(walk(3))` with the resulting list as output.
- **Raised exceptions** may be demonstrated, but only if you reproduce the message exactly:

  ```
  >>> clip_to_range(5, 9, 2)
  Traceback (most recent call last):
      ...
  ValueError: lowest must not exceed highest
  ```

  When in doubt, prefer a plain successful call over a traceback.

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

Read each returned function and confirm: summary line present and correctly worded; every parameter
listed with the exact annotation from the signature; `Returns:` present and matching the return
annotation if a value is returned; `Raises:` matching the explicit raises exactly; `Examples:`
present with at least one doctest whose output you have verified is stable and exact; body byte-for
byte unchanged.