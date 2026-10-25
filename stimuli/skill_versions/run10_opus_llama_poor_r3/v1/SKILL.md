---
name: docstring-api
description: How to add Google-style docstrings to named public Python functions — summary line, Args/Returns/Raises/Examples sections, doctests that actually run, and the rules for returning the functions unchanged apart from the docstring.
---

# Adding Google-style docstrings

## What you are producing

You are given a working Python module and a list of public function names. For each named
function, insert one Google-style docstring. Then return those functions — and nothing else.

Hard constraints on the output:

- Return **only** the named public functions, in the exact order they were listed.
- Each function is **verbatim** except for the inserted docstring: same decorators, same
  `def` line, same annotations, same defaults, same body statements, same nested helpers.
- Include the **full body**. Never substitute `...`, `pass`, or a comment for real code.
- Do not document, include, or modify any other function in the module.
- Do not rename, reorder, refactor, or "improve" anything.
- No code fence, no preamble, no trailing explanation.

Everything you write must be derived from the function's actual signature and body. Do not
guess behavior, and do not reuse wording from these instructions in a docstring.

## The shape of a docstring

```python
def normalize_slug(text: str, separator: str = "-") -> str:
    """Normalize text into a URL-safe slug.

    Args:
        text (str): The text to convert.
        separator (str): Character used to join words. Defaults to "-".

    Returns:
        str: The slug, lowercased and joined by the separator.

    Raises:
        ValueError: If text is empty or only whitespace.

    Examples:
        >>> normalize_slug("Hello World")
        'hello-world'
        >>> normalize_slug("Hello World", separator="_")
        'hello_world'
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("text must not be empty")
    return separator.join(cleaned.lower().split())
```

Formatting rules, all visible in that example:

- Triple **double** quotes. The summary starts on the same line as the opening `"""` — no
  newline or space after the quotes.
- The closing `"""` sits on its own line, indented like the body.
- No blank line before the docstring, and no blank line between the closing `"""` and the
  first statement of the body.
- The docstring is indented to the function body's level; section contents are indented one
  further level (4 more spaces).
- Exactly one blank line separates the summary from the first section, and one blank line
  separates each section from the next.
- If the docstring text contains a backslash, prefix it: `r"""..."""`.

## Write exactly one docstring per function

This is the most common way people fail. A function gets **one** docstring block: one opening
`"""`, one closing `"""`, and every section lives between them.

- Do not write a short docstring, close it, and then start a second `Args:` / `Returns:` /
  `Examples:` block. Text after the closing quotes is code, and stray section labels there are
  a syntax error.
- Do not repeat a section. There is at most one `Args:`, one `Returns:`, one `Raises:`, one
  `Examples:` per function.
- Do not document two functions inside one docstring.

If you find yourself about to write a second `Args:` for the same function, merge it into the
first one instead.

## The summary line

One line, imperative mood, describing what the function does.

- Starts with a capital letter; ends with `.`, `!`, or `?`.
- The first word must be one of:
  `Add`, `Build`, `Check`, `Clip`, `Compress`, `Convert`, `Count`, `Create`, `Decode`,
  `Detect`, `Encode`, `Format`, `Generate`, `Identify`, `Interpret`, `Iterate`, `Join`,
  `Normalize`, `Parse`, `Remove`, `Return`, `Reverse`, `Test`, `Transform`, `Validate`.
- Do not restate the signature, and do not copy a line of source code.
- The summary is the only prose that is required. If you add an extended description, put it
  in its own paragraph after one blank line, and make sure it says something true about *this*
  function's body. Never pad with a second sentence that just rewords the summary.

## Args

Include `Args:` whenever the function takes at least one parameter (other than `self`/`cls`).

- List **every** parameter, in signature order. Omit `self` and `cls`.
- Use the parameter names exactly as written in the signature. Invent no extra names.
- Annotated parameter: `name (annotation): description`, where `annotation` is copied
  character-for-character from the signature (`Any`, `bool`, `int`, `Optional[str]`, …).
- Unannotated parameter: `name: description`. Do not invent a type for it.
- For a parameter with a default, mention the default in the description.
- Keep the type in the docstring even though the signature already carries it.

Omit the whole `Args:` section only when there are no parameters to document.

## Returns

- Include `Returns:` only if the body actually returns a value (a `return <expr>`, or a
  generator/`yield`-backed value the function hands back).
- Format: `annotation: description`, with the annotation copied exactly from the `->` in the
  signature.
- Omit `Returns:` entirely for a function that returns nothing (`-> None`, or bare `return` /
  fall-through only).

## Raises

`Raises:` is an exact reflection of the body — no more, no less.

- Include an entry for every exception the body raises with an explicit `raise` statement,
  including `raise` statements inside nested helper functions defined within this function.
- Format: `ExceptionType: the condition that triggers it.`
- Exclude anything the body does not explicitly raise. In particular, exceptions **caught** in
  a `try`/`except` clause are not raised by this function — a body that does
  `except (TypeError, ValueError): pass` gets no `Raises:` entry from that.
- Exclude exceptions the function might merely propagate from a call it makes.
- If the body contains no `raise` statement, omit the `Raises:` section completely.

## Examples

Every named function gets an `Examples:` section with at least one `>>>` doctest **in its own
docstring**. A doctest elsewhere in the module does not count.

- The doctest must run successfully, and the expected output line must match the interpreter's
  output character-for-character — including quotes on strings (`'hello-world'`, not
  `hello-world`), `True`/`False`, and `None` producing no output line at all.
- Call the function by its real name with real arguments.
- Prefer a deterministic call whose output you can state with certainty.
- When the result depends on randomness, time, the environment, or object identity, assert a
  **stable property** instead of the raw value. Bind the result and check something invariant:

  ```
  >>> value = make_token(12)
  >>> len(value)
  12
  >>> isinstance(value, str)
  True
  ```

- For a generator, materialize it before showing output, e.g. `>>> list(walk(3))`.
- Prefer several short deterministic lines over one clever line you are unsure about.

## Section order

When more than one applies, they always appear in this order, each separated by one blank line:

`Args:` → `Returns:` → `Raises:` → `Examples:`

Skip any section that does not apply. Never invent content to fill a section.

## Final check before returning

For each named function, in listed order, confirm:

1. Exactly one docstring, opened and closed once, with nothing left dangling after it.
2. Summary on the opening-quote line, approved starting verb, terminal punctuation.
3. Every signature parameter present in `Args:`, in order, names and annotations exact.
4. `Returns:` present iff a value is returned, and its type matches the annotation.
5. `Raises:` lists exactly the explicitly raised exceptions — none from `except` clauses.
6. At least one `>>>` doctest that would really pass, with exact expected output.
7. Blank-line spacing and indentation as shown in the example.
8. The signature and every executable statement are unchanged, and the body is complete.

Then output the functions alone — no fence, no commentary.