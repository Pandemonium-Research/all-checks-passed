---
name: docstring-api
description: Use this skill when adding Google-style API docstrings to named public Python functions, so the returned definitions document every parameter, return, and raised exception and carry doctests that actually run, without changing any code.
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
   parameter, use `name: description` rather than inventing a type. Never annotate an entry from a
   guess about what callers "should" pass.
3. When the body returns a value, document every return value in `Returns:` as
   `type: description`; match the return annotation exactly. If the function has no return
   annotation, write the entry as `description` alone rather than inferring a type. Do not add
   `Returns:` for a function without a value return.
4. In `Raises:`, document every exception raised explicitly in the function body as
   `ExceptionType: condition`, and no exception that the body does not explicitly raise.
5. Add `Examples:` with at least one runnable `>>>` doctest per named public function. Every
   doctest must execute successfully and its expected output must match exactly.

## Raises: only what the body raises

Scan the function body for literal `raise` statements. Each one, and only each one, becomes a
`Raises:` entry, using the exception class name exactly as written — including project-defined
classes such as a module's own error type.

Do not add an entry for:

- an exception the interpreter might produce on its own (`TypeError` from a bad argument type,
  `ZeroDivisionError`, `AttributeError`, `KeyError`) when no `raise` statement produces it;
- an exception a called helper might raise;
- a condition you described in `Args:` (writing "must be a boolean" does not mean the body raises
  `TypeError`);
- an exception raised in a different function.

A body whose only guard is `if not isinstance(x, int) or x < 1: raise ValueError(...)` documents
exactly one entry: `ValueError`. A body with no `raise` statement gets no `Raises:` section.

## Writing doctests that actually pass

Doctests are the most common source of failure. Do not predict output from the function's name or
from what the docstring says it does. Derive it from the code.

For each doctest, in order:

1. Pick a small, concrete input.
2. Walk the body statement by statement with that input, including every guard clause and early
   return. If an input trips a guard such as `if not <predicate>(value): return value`, the result
   is the unchanged input, not the transformed one — either accept that result or choose an input
   that reaches the branch you meant to show.
3. Write down the value the final `return` actually produces, character for character. Apply the
   real semantics of every call in the path: `''.join(parts)` inserts no separator, `str.title()`
   capitalizes each alphabetic run, slicing with `[::-1]` reverses, and so on.
4. Write the expected line as Python's `repr` of that value: strings appear in quotes (`'olleh'`),
   `True`/`False` capitalized, floats in full repr. An expression evaluating to `None` prints
   nothing, so leave no expected-output line under it.
5. Keep the example internally consistent with the arguments used — an input of `10` items must not
   produce a result of a different size.

Use `...` to continue a multi-line statement. Put no blank line inside `Examples:`; a blank line
ends the expected output block.

## Nondeterministic results must be stabilized

If the value depends on randomness, cryptographic entropy, the clock, process state, hashing of
random data, iteration order of a set, object identity, or a temporary path, its literal output can
never be matched. Sources include `random`, `secrets`, `os.urandom`, `uuid`, `time`,
`datetime.now`, `id()`, and `tempfile`.

Never paste a sample value such as a specific UUID or a specific random string as expected output.
Instead, bind the result to a name and assert a deterministic property of it:

```
Examples:
    >>> value = generate_thing(8)
    >>> len(value)
    8
    >>> isinstance(value, str)
    True
    >>> value.startswith('prefix-')
    True
    >>> set(value) <= set('0123456789abcdef')
    True
```

Choose properties the code guarantees for every run. If the size of the output is a transformation
of the argument — for example a byte count rendered as hexadecimal characters — check the
transformed size, not the argument.

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

## Worked example: nondeterministic function with unannotated parameters

Before:

```python
def build_session_id(prefix):
    return prefix + "-" + str(uuid4())
```

After:

```python
def build_session_id(prefix):
    """Build a session identifier from a prefix.

    Args:
        prefix: Text placed in front of the generated identifier.

    Returns:
        The prefix joined to a freshly generated identifier.

    Examples:
        >>> session = build_session_id('web')
        >>> session.startswith('web-')
        True
        >>> len(session) - len('web-')
        36
    """
    return prefix + "-" + str(uuid4())
```

Note what this example does not do: it invents no type for the unannotated parameter or return, it
adds no `Raises:` section because the body raises nothing, and it prints no sample identifier.

## Final check before returning

- Every parameter in the signature appears in `Args:`, with no extras and no invented types.
- Every `Raises:` entry corresponds to a literal `raise` in that function's body, and every such
  `raise` has an entry.
- Every expected doctest output was traced through the body, not guessed from the summary.
- No doctest expects a value that varies between runs.
- Sections appear in the required order, with the required blank lines.

## Output schema

Return only the complete definitions of the named public functions, in the order listed, with the
requested docstrings inserted. Keep their full executable bodies; do not replace them with `...`.
Include no code fence or surrounding explanation.