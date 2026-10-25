---
name: docstring-api
description: Use this skill when adding Google-style docstrings to named public Python functions — it defines the required sections, how to derive `Raises:` and doctest output from the actual body, and how to write examples for functions whose results vary between runs, all without editing any code.
---

# API docstrings

Add documentation under the Google docstring convention to the named public functions only.
Do not document unrelated functions. Do not modify executable code or signatures. Parameter and
return types belong in the docstrings even though the signatures already carry annotations.

## Required content

For every named public function:

1. Write a one-line imperative summary. Start it with a capital letter, end it with punctuation,
   specifically `.`, `!`, or `?`, and do not repeat the function signature there. Capitalize one
   locally recognized first word from this pipe-delimited set:
   `add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.
2. In `Args:`, document every parameter, in signature order, except `self` and `cls`. Use exactly
   the signature's parameter names and no extra names. An annotated entry is
   `name (annotation): description`; match the signature annotation exactly. For an unannotated
   parameter, use `name: description` rather than inventing a type.
3. When the body returns a value, document every return value in `Returns:` as
   `type: description`; match the return annotation exactly. Do not add `Returns:` for a function
   without a value return.
4. In `Raises:`, document every exception raised explicitly in the function body as
   `ExceptionType: condition`, and no exception that the body does not explicitly raise.
5. Add `Examples:` with at least one runnable `>>>` doctest per named public function. Every
   doctest must execute successfully and its expected output must match exactly.

## Raises: one entry per literal `raise`

Scan the body for `raise` statements. Each one, and only each one, becomes an entry, using the
exception class name exactly as written — including a project's own error classes. Do not add an
entry for:

- an exception the interpreter might produce on its own (`TypeError` for a wrong argument type,
  `ValueError`, `KeyError`, `AttributeError`, `ZeroDivisionError`) when no `raise` in this body
  produces it;
- an exception that some helper called by the body might raise;
- a rule you stated in `Args:` — describing a parameter as a boolean is not evidence that the body
  raises `TypeError` when it is not one;
- an exception raised in a neighbouring function.

A guard such as `if not isinstance(x, int) or x < 1: raise ValueError(...)` yields exactly one
entry: `ValueError`. A body containing no `raise` gets no `Raises:` section at all.

## Doctest output is traced from the body, never guessed

Do not predict output from the function's name, its summary, or what the code appears to intend.
For each example, in order:

1. Choose a small, concrete input.
2. Walk the body statement by statement with that input, including every guard clause and early
   return. If your input trips a guard such as `if not <predicate>(value): return value`, the
   result is the unchanged input — either show that, or pick an input that reaches the branch you
   meant to demonstrate.
3. Apply the real semantics of every call on the path: `''.join(parts)` inserts no separator,
   `str.title()` capitalizes each alphabetic run, `[::-1]` reverses, a hex encoding of *n* bytes is
   *2n* characters.
4. Write the expected line as Python's `repr` of the resulting value: strings quoted (`'olleh'`),
   `True`/`False` capitalized, floats in full repr. An expression evaluating to `None` prints
   nothing, so leave no expected-output line under it.
5. Keep the example self-consistent: a length argument of `10` must not produce a result of a
   different length.

Use `...` to continue a multi-line statement. Put no blank line inside `Examples:`; a blank line
ends the expected output block.

## Varying results must be asserted, not printed

If the value depends on randomness, cryptographic entropy, the clock, process state, iteration
order, object identity, or a temporary path — `random`, `secrets`, `os.urandom`, `uuid`, `time`,
`datetime.now`, `id()`, `tempfile` — its literal output can never match on a later run.

Never paste a sample value such as a specific UUID or a specific random string as expected output,
however plausible it looks. Instead, bind the result to a name and assert properties that the code
guarantees on every run:

```
Examples:
    >>> value = generate_token(8)
    >>> isinstance(value, str)
    True
    >>> len(value)
    8
    >>> set(value) <= set('0123456789abcdef')
    True
```

When the size of the output is a transformation of the argument, assert the transformed size, not
the argument. A function whose result varies only in part — a fixed prefix plus a random tail —
may assert the fixed part with `.startswith(...)` and the tail by length.

## Layout and order

Use triple double quotes, and use a raw triple-quoted docstring when it contains backslashes. Put
the summary immediately after the opening triple quotes, with no surrounding whitespace. For a
multiline docstring, put the closing triple quotes on their own line. Leave no blank line
immediately before or after the docstring. Use spaces and the standard indented Google layout:
indent the docstring to match the function body and indent section entries one additional level.
Put a blank line between the summary and each section, using exactly one blank line at each break.
Order applicable sections as
`Args:` → `Returns:` → `Raises:` → `Examples:`.

Resolve overlaps in this precedence: preserve source, limit scope to named functions, then trust
exact signature/body evidence over guesses. Omit inapplicable sections.

## Worked example: deterministic function

Before:

```python
def root(value: float) -> float:
    if value < 0:
        raise ValueError("value")
    return value ** 0.5
```

After:

```python
def root(value: float) -> float:
    """Return the square root of a value.

    Args:
        value (float): Number to process.

    Returns:
        float: The square root.

    Raises:
        ValueError: If value is negative.

    Examples:
        >>> root(9.0)
        3.0
    """
    if value < 0:
        raise ValueError("value")
    return value ** 0.5
```

## Worked example: function whose result varies

Before:

```python
def build_tag(size: int = 4) -> str:
    return "tag-" + os.urandom(size).hex()
```

After:

```python
def build_tag(size: int = 4) -> str:
    """Build a tag with a random suffix.

    Args:
        size (int): Number of random bytes in the suffix. Defaults to 4.

    Returns:
        str: The tag, with the suffix rendered as hexadecimal characters.

    Examples:
        >>> tag = build_tag(4)
        >>> tag.startswith('tag-')
        True
        >>> len(tag) - len('tag-')
        8
    """
    return "tag-" + os.urandom(size).hex()
```

Note what this example does not do: it prints no sample tag, and it adds no `Raises:` section,
because the body raises nothing.

## Final check before returning

- Every signature parameter appears in `Args:`, with no extras and no invented types.
- Every `Raises:` entry matches a literal `raise` in that function's own body, and every such
  `raise` has an entry.
- Every expected output was traced through the body — guards and early returns included — rather
  than inferred from the summary.
- No doctest expects a value that could differ on the next run.
- Sections appear in the required order, with the required blank lines.

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with the
requested docstrings inserted. Keep their full executable bodies; do not replace them with `...`.
Include no code fence or surrounding explanation.