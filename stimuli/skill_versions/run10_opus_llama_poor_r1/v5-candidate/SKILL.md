---
name: docstring-api
description: How to add Google-style docstrings to named public Python functions in this project — which sections are required, summary-line wording, exact formatting, doctests whose calls and expected output are traced from the real code, and exactly which lines of the file you may emit. Reach for it whenever you are asked to document, "add docstrings to," or write API help for a list of public functions in an existing module.
---

# Docstrings for named public functions

## What you are producing

You are given a working module and a list of public function names. For each named function you add
one Google-style docstring and change nothing else. You then return those functions' complete
definitions, in the order the names were listed.

Do not document functions that were not named. Do not refactor, reformat, rename, reorder, or
"improve" any code. Signatures and every executable statement — including nested helpers, comments,
and decorators — come through byte-for-byte identical. Never abbreviate a body with `...` or
`# unchanged`.

## The five defects that sink most entries

Check these before anything else; almost every rejected entry has at least one.

1. **Extra lines in the output.** Imports, `__all__`, module constants, or an unnamed helper got
   copied along with the functions. See *Emit the functions, not the module*.
2. **A missing `Examples:` block.** Every named function needs its own. See *`Examples:`*.
3. **An invented `Raises:` section.** A function with no `raise` in its body does not raise
   anything. See *`Raises:`*.
4. **A doctest that cannot pass** — a made-up UUID, a hand-typed hex blob, a placeholder like
   `'xxxx…'`, a random string printed as if it were fixed, or an expected line guessed from what the
   function's name implies. See *`Examples:`* and *Values you must not print*.
5. **An example that passes an argument the signature does not define.** A keyword you invented to
   show off a behavior raises `TypeError` and the doctest fails. See *Call only what the signature
   allows*.

## Emit the functions, not the module (a common failure)

Your output is a sequence of `def` blocks and nothing else. Starting from the top of the file and
copying downward is wrong.

**Never include**, even though they are in the source file and even though the functions depend on
them:

- `import` / `from … import` lines
- `__all__`, module-level constants, compiled regexes, configuration
- the module docstring, module-level comments, `if __name__ == '__main__':`
- any function that was not named, including private helpers the named functions call

The named functions will reference imports, constants, and helpers that you are not emitting. That
is expected and correct. Your snippet is not meant to run standalone, so do not add imports to make
it so, and do not paste in a dependency's definition.

Separate consecutive functions with two blank lines. The first character of your output is the `d`
of the first named function's `def` (or its decorator, if it has one). Output no code fence and no
commentary.

## The four required parts

For **every single named function**, the docstring must contain all of the following that apply, and
`Examples:` always applies:

| Section | Include it when | Skip it when |
| --- | --- | --- |
| summary line | always | never |
| `Args:` | the signature has at least one parameter (excluding `self`/`cls`) | the signature takes no parameters |
| `Returns:` | the body has a `return <value>` or a `yield` | the function only returns `None` implicitly |
| `Raises:` | the body contains an explicit `raise` statement | the body has no explicit `raise` |
| `Examples:` | **always — every named function needs one** | never |

A docstring that is only a summary plus a sentence or two of prose is wrong, no matter how well
written the prose is. A docstring with `Args:` and `Returns:` but no `Examples:` is wrong. Before you
finish, count the `Examples:` headers and the named functions; the two numbers must be equal.

Sections appear in exactly this order: `Args:` → `Returns:` → `Raises:` → `Examples:`. These four are
the only headers this project uses. Do not introduce `Yields:`, `Note:`, `Warning:`, `See Also:`,
`Attributes:`, or `Parameters:`.

## Exact layout

Follow this skeleton literally. The summary text starts on the same line as the opening `"""` — never
on the line below it.

```python
def example_name(first: str, second: int = 0) -> bool:
    """Validate one short imperative sentence here.

    Args:
        first (str): What this parameter is.
        second (int): What this parameter is.

    Returns:
        bool: What the result means.

    Raises:
        ValueError: When the condition that triggers it holds.

    Examples:
        >>> example_name('abc', 1)
        True
    """
    ...
```

Rules embodied above:

- `"""Summary…` — no newline and no space between the quotes and the first word.
- Exactly one blank line between the summary and the first section, and between each pair of
  sections. No blank line before the closing `"""`.
- Closing `"""` on its own line, indented to the function body's level.
- Section headers (`Args:`, `Returns:`, `Raises:`, `Examples:`) sit at the docstring's indent level;
  their entries are indented one further level. Spaces only, never tabs.
- No blank line between `def` and the docstring, or between the docstring and the first statement.
- If the docstring text contains a backslash, make it a raw string: `r"""…"""`.

## The summary line

One line, imperative mood, describing what the function does — not a restatement of the signature and
not a line copied out of the body.

- Capitalize the first word and end with `.`, `!`, or `?`.
- The first word must be one of:
  `add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`.
  Pick the one that genuinely fits the function's behavior; capitalize it (`Check…`, `Generate…`).
- Do not repeat the function name or parameter list in it.

## `Args:`

- List every parameter in signature order. Omit `self` and `cls`. Add no name that is not in the
  signature, and drop none that is.
- Annotated parameter: `name (annotation): description`. The text inside the parentheses is the
  annotation copied **exactly** from the signature and nothing else — `bool`, `Any`, `Generator`,
  `Optional[List[str]]`. A parameter with a default is written with its bare annotation: `count: int = 1`
  becomes `count (int): …`.
- Do **not** append `, optional` or `optional` inside the parentheses, do not write the default value
  there, and do not translate a type into words.
- Unannotated parameter: `name: description`. Do not invent a type for it.
- Mention a default's effect at the end of the description if it matters (`Defaults to None.`); the
  parenthesized field stays the annotation alone.

## `Returns:`

- Format: `annotation: description`, with the annotation copied exactly from the signature's return
  annotation.
- For a generator function, or a function annotated `-> Generator` that returns one, still use
  `Returns:` with the declared annotation and describe what gets yielded. Never use a `Yields:`
  header.
- Omit the whole section for a function that returns nothing.

## `Raises:`

Search the body for the literal token `raise`. That search — not the parameter names, not what a
careful implementation "should" validate — decides this section.

- One entry per exception class reached by an explicit `raise` statement in the body, including
  `raise`s inside nested helper functions and inside `except` blocks.
- Format: `ExceptionType: condition that triggers it.` Use the class name exactly as written in the
  code (project-specific error classes included). Never name an error class you did not read in a
  `raise` line of this body — a plausible-sounding project error is still an invented one.
- **If the body contains no `raise` statement, omit the entire `Raises:` section.** This is the
  single most common invented section. In particular, none of the following is a raise:
  - a validity check that ends in `return False` — a predicate that rejects bad input *returns*, it
    does not raise;
  - a `try:` / `except SomeError:` block that catches, retries, or swallows an error;
  - a guard that delegates to a helper such as a "has text" or "is valid" check.

  A `bool` flag, a string handed to a regex, or a value passed straight to a constructor is not
  validated unless you can point at the `raise` line.
- Do not list exceptions that merely propagate from a call.

## `Examples:`

At least one `>>>` line per named function, inside that function's own docstring. An example that
lives in another function's docstring or elsewhere in the module does not count.

The doctest must actually run and its expected output must match character-for-character. **One
example you have traced beats three plausible ones** — each extra example is another chance to write
a line that fails.

### Call only what the signature allows

Re-read the `def` line before writing the call. Every argument you pass must be a parameter that
appears there, spelled exactly, in a valid positional/keyword order. Never invent a keyword to
illustrate a behavior you assume exists; a keyword the signature does not define raises `TypeError`
and the doctest fails. If the signature offers no way to show the variation you had in mind, do not
show it.

### Trace the expected output; never infer it from the name

Derive every expected line by executing the body on paper with the exact arguments you wrote:

1. Pick arguments and walk the body statement by statement, into every nested helper, until you reach
   the `return` or final `yield`.
2. Write the `repr` of that value as the expected line.

Where guesses go wrong most often:

- **Predicates returning `bool`.** The function's name tells you its intent, not its answer. Choose a
  canonical, unambiguous input — one the function is plainly meant to accept, and one it is plainly
  meant to reject — and make sure the answer you write is the one the code produces for it. Steer
  away from borderline inputs (embedded spaces, punctuation, mixed separators, unusual casing) whose
  verdict is decided entirely by a regex or constant you cannot fully evaluate.
- **A second call that overrides a default.** Re-trace it from the top. A different flag, separator,
  or bound usually selects a different branch, so the first example's answer does not carry over. In
  particular, an input built for one separator or mode is normally rejected under the default one.
- **Loops and generators.** Confirm the loop terminates for your arguments before writing the
  expected list — a `while current != stop` loop whose step steps *past* `stop` never exits, and a
  hanging doctest is a failure. Re-check the guard clauses above the loop too: arguments you thought
  were ordinary may trip a `raise` and yield a traceback instead of a value.
- **Any call where you would have to say "probably."** Replace the arguments with ones you can
  resolve exactly, or use the bound-and-assert form below.

### Formatting the expected line

- Show the true `repr`. A string result prints as `'abc'` with quotes; use `print(...)` if you want
  bare text.
- A call that returns `None` produces **no** expected-output line at all.
- Consume a generator so the output is concrete, e.g. `>>> list(gen(...))` or `>>> next(gen(...))`.
- Multi-line setup is allowed with `...` continuation lines.
- Avoid floats with long representations, unordered `set`/`dict` output, and objects whose repr
  contains a memory address.
- Never write a placeholder or an illustrative stand-in as expected output. Strings like
  `'xxxxxxxx-xxxx-xxxx'`, `'abc1234567890'`, or a hand-typed hex blob are wrong answers, not
  approximations: a doctest that cannot pass is worse than a modest one.

### Values you must not print

If the result depends on randomness, a UUID, the clock, `os.urandom`, a hash, the environment, or
anything else that differs between runs, the value can never be matched — not even by copying a real
one you saw once. Bind it to a name and assert a stable property instead, so every expected line is
fixed:

```
>>> value = nondeterministic_call(8)
>>> isinstance(value, str)
True
>>> len(value)
8
```

Compute the property from the code, not from the argument. If a function hex-encodes *n* random
bytes, its length is `2 * n`, so `len(...)` for `n = 8` is `16` — check the transformation before you
write the number. When even the length is not obvious, fall back to something you are certain of,
such as `isinstance(value, str)` → `True` or `value.count('-')` for a canonical UUID.

When a flag changes the shape of a nondeterministic result, show both calls in this bound-and-assert
form rather than printing either value.

### Showing an error path

Either call the function inside `try`/`except` and print something fixed, or use the traceback form,
whose final line must match the real message exactly:

```
>>> failing_call(-1)
Traceback (most recent call last):
    ...
ValueError: exact message text from the code
```

If you are not certain of the message text, use a passing call instead — a broken doctest is worse
than a modest one.

## Before you hand it back

Walk each named function once more and confirm:

1. Summary begins on the `"""` line, uses an approved capitalized first word, ends in `.`/`!`/`?`.
2. Every signature parameter appears in `Args:` in order, with the bare annotation in parentheses and
   no `, optional`.
3. `Returns:` present iff the function returns or yields a value, annotation copied exactly; no
   `Yields:` header anywhere.
4. `Raises:` lists exactly the classes named by a literal `raise` in this body — no more, no fewer —
   and is absent entirely when there is no `raise`. A `return False` on bad input is not a raise.
5. `Examples:` present with at least one `>>>`. Every call uses only parameters that appear in the
   signature, and every expected line is one you traced through the body — not one the function's
   name implied. No nondeterministic value is printed, and no example hangs or unexpectedly raises.
6. Blank-line and indentation rules hold; body and signature are untouched.
7. The output contains only the named functions' `def` blocks — no imports, no `__all__`, no module
   constants, no unnamed functions — in the order the names were listed.

Terms like "doc block," "API note," "function help," and "docstring" all mean this artifact. Derive
its contents from the actual signature and body, never from what the name suggests.