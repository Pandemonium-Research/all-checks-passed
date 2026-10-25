---
name: docstring-api
description: How to add Google-style docstrings to named public Python functions — the summary line, the Args/Returns/Raises/Examples sections, and above all how to write the mandatory `>>>` doctest so that it actually runs and its expected output actually matches, while returning each function otherwise verbatim.
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

## The two rules that people break most often

Read these before anything else. Nearly every rejected answer fails one of them.

**1. Every named function gets its own `Examples:` section containing at least one `>>>`
doctest.** There is no such thing as a function too small, too obvious, or too trivial to
need one. A one-line predicate needs a doctest. A helper-like function needs a doctest. A
doctest in a *different* function's docstring does not count for this one. If you write five
functions, you write five `Examples:` sections. Before returning, count them: the number of
`Examples:` sections must equal the number of named functions, with no exceptions.

**2. Every expected-output line must be one you traced through the real body.** A doctest is
executed and compared character-for-character. An output that merely *looks* like what the
function might produce is a failure, exactly as bad as omitting the example. If you cannot
state the output with certainty, do not invent one — assert a stable property instead
(see "Examples" below).

## Build order for each function

Work one function at a time, and follow the same order every time:

1. Copy the function verbatim.
2. Write the summary line.
3. Write `Args:`, then `Returns:`/`Yields:`, then `Raises:` — skipping any that do not apply.
4. Write `Examples:`. **This step is never skipped.** A docstring is not finished, and the
   closing `"""` does not get written, until an `Examples:` section with at least one `>>>`
   line is in it.

The danger point is a short, obvious function late in the list: momentum makes it tempting to
stop after `Returns:`. Do not. Finish step 4 for that function before moving to the next one.

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

A function gets **one** docstring block: one opening `"""`, one closing `"""`, and every
section lives between them.

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

- Include `Returns:` if the body hands a value back to the caller — any `return <expr>`,
  including a `return` of a generator object built by a nested helper.
- Format: `annotation: description`, with the annotation copied exactly from the `->` in the
  signature. If the annotation is `Generator`, the section reads `Generator: …`.
- Use `Yields:` **only** when the named function is itself a generator function — that is,
  when a `yield` appears in its own top-level body, not merely inside a nested helper it
  defines. In that case the section is `Yields:` and it replaces `Returns:`; describe the
  type of each yielded item.
- Omit both sections entirely for a function that returns nothing (`-> None`, or bare
  `return` / fall-through only).

## Raises

`Raises:` is an exact reflection of the body — no more, no less.

- Include an entry for every exception the body raises with an explicit `raise` statement,
  including `raise` statements inside nested helper functions defined within this function.
- Format: `ExceptionType: the condition that triggers it.`
- List each exception type once, even if it is raised from several places.
- Exclude anything the body does not explicitly raise. In particular, exceptions **caught** in
  a `try`/`except` clause are not raised by this function — a body that does
  `except (TypeError, ValueError): pass` gets no `Raises:` entry from that.
- Exclude exceptions the function might merely propagate from a call it makes.
- If the body contains no `raise` statement, omit the `Raises:` section completely.

## Examples

**Mandatory for every named function.** Unlike `Args:`, `Returns:`, and `Raises:`, this
section is never skipped and never conditional.

### Building a doctest you can trust

Do this in order, for each function:

1. **Pick arguments that survive the guards.** Read every `if … raise` and every validation
   helper in the body first, and choose argument values that trigger none of them. Check the
   guards that compare arguments *to each other* — a direction, range, or step check can
   reject a combination in which each value is individually valid. An example that raises
   where you expected a value is a failed doctest, and it is the single most common cause of
   one. The safest first line is the function called with only its required arguments, letting
   every default stand; add a second line with a non-default argument only once you have
   traced that call too.
2. **Walk the body with those arguments** and compute the result yourself — through the
   conditionals actually taken, through the regex or arithmetic actually applied, through any
   nested helper actually called. Do not reason from the function's *name*.
3. **Write the result the way the REPL would print it**, i.e. its `repr`:
   strings in single quotes (`'hello-world'`, not `hello-world`), `True` / `False`
   capitalized, lists and tuples with their brackets, and `None` producing **no** output line
   at all.
4. **If step 2 left you unsure of even one character, do not write a literal.** Go to the
   stable-property form below.

Keep examples small and few. Choose the simplest arguments that exercise the function, prefer
short outputs you can check at a glance, and write only as many `>>>` lines as you have
actually traced — every extra line is another chance to fail. Call each function by its real
name, with real arguments; other module-level functions and constants are available to your
doctest, but the named function must appear in its own example.

### When the value cannot be pinned down

Some results are impossible to predict, and writing a plausible-looking literal for them is
always wrong — a fabricated value that has the right *shape* (a well-formed UUID, a hex
string, a token of letters and digits) is still a failed doctest. Treat a function as
unpredictable whenever its result depends on randomness, cryptographic entropy, unique
identifiers, the clock or calendar, the environment, the filesystem or network, object
identity, or unordered iteration — for example anything reached through `random`, `secrets`,
`os.urandom`, `uuid`, `time`, `datetime.now`, `id`, or iteration over a `set`. This applies
transitively: if the function calls something that reaches one of those, it is unpredictable
too.

For those, bind the result and assert something invariant about it:

```
>>> value = make_token(12)
>>> isinstance(value, str)
True
>>> len(value)
12
```

- Derive any asserted length from the body's own arithmetic, not from the argument by
  reflex — a function that encodes *n* bytes as hex produces `2 * n` characters, and a
  function that pads, prefixes, or strips separators changes the count again. Then check the
  number you wrote against the value you wrote, and against each other example on the same
  function; two lines that disagree about the same function's output are both suspect.
- Other safe invariants: `isinstance(...)`, `len(...)`, membership (`x in result`), a
  boolean check like `value.isupper()`, `sorted(...)` over an unordered collection, or
  `round(..., 4)` for a float with a long expansion.
- A deterministic call is still preferred whenever one exists. Only reach for properties when
  the value genuinely cannot be known.

Worked shape, for a function whose output is random but whose structure is not:

```python
def issue_ticket(prefix: str, size: int = 8) -> str:
    """Generate a ticket identifier with a random suffix.

    Args:
        prefix (str): Text placed before the random suffix.
        size (int): Number of random characters appended. Defaults to 8.

    Returns:
        str: The prefix followed by size random characters.

    Raises:
        ValueError: If size is less than 1.

    Examples:
        >>> ticket = issue_ticket("AB-", 4)
        >>> isinstance(ticket, str)
        True
        >>> ticket.startswith("AB-")
        True
        >>> len(ticket)
        7
    """
```

Note where the `7` comes from: three characters of prefix plus four random ones, read off the
body's own arithmetic — not copied from the `size` argument.

### Other cases

- **Generators and iterators:** materialize before showing output, e.g. `>>> list(walk(3))` —
  calling the function bare prints a `<generator object …>` line you cannot reproduce. Choose
  arguments that yield a short sequence, and verify it element for element, including where
  the sequence starts, which direction it moves, and whether the final value is included:

  ```
  >>> list(count_down(3))
  [3, 2, 1]
  ```

- **Predicates:** show at least one call — and ideally one true case and one false case, since
  the expected output is just `True` or `False` and is easy to verify.
- **Exceptions:** prefer examples of successful calls. Only demonstrate a `raise` in a doctest
  if you copy the exception's message verbatim from the `raise` statement in the body.

## Section order

When more than one applies, they always appear in this order, each separated by one blank line:

`Args:` → `Returns:` (or `Yields:`) → `Raises:` → `Examples:`

Skip any section that does not apply — except `Examples:`, which always applies. Never invent
content to fill a section.

## Final check before returning

For each named function, in listed order, confirm:

1. Exactly one docstring, opened and closed once, with nothing left dangling after it.
2. Summary on the opening-quote line, approved starting verb, terminal punctuation.
3. Every signature parameter present in `Args:`, in order, names and annotations exact.
4. `Returns:` / `Yields:` present iff a value is handed back, with the annotation copied exactly.
5. `Raises:` lists exactly the explicitly raised exceptions — none from `except` clauses.
6. An `Examples:` section is present — count them against the list of named functions and
   confirm the two counts match, with none missing. If any function lacks one, stop and add it
   before returning anything.
7. Every doctest argument clears the body's guards, including guards that compare arguments to
   one another; every expected output line is one you traced through the body rather than
   guessed; anything unpredictable is asserted as a property instead of a literal.
8. Blank-line spacing and indentation as shown in the example.
9. The signature and every executable statement are unchanged, and the body is complete.

Then output the functions alone — no fence, no commentary.