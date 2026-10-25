---
name: docstring-api
description: Use this skill when adding Google-style docstrings to the named public functions of an already-correct Python module, so the returned definitions carry a complete Args/Returns/Raises/Examples contract, with doctests that actually pass and with no change to the code itself.
---

# API documentation notes

## 1. What you return

Return only the complete definitions of the **named** public functions, in the order they were
listed. Nothing else.

- Do not document, include, or even echo any function that was not named — not helper functions,
  not private functions, not other public functions in the same module, not classes. The module is
  already correct and complete; your job is narrow. Expanding the scope to be helpful is the most
  common way this task is failed.
- Each returned definition is verbatim except for the inserted docstring. Preserve the `def` line,
  every annotation, every default, and every executable statement exactly as written.
- Include each full function body. Never abbreviate a body to `...`, `pass`, or a comment.
- Output raw Python only: no ``` code fences, no `python` language tag, no headings, no preamble,
  no closing explanation. If you were about to open a fence before the first `def`, or close one
  after the last line of the last body, delete it.

## 2. The shape of every docstring

Every named function gets one docstring, inserted as the first statement of its body, indented to
match the body. Use triple double quotes. Use a raw docstring (`r"""`) if the text contains a
backslash.

```python
def function_name(first: str, second: int = 0) -> bool:
    """Validate the incoming record.

    Args:
        first (str): What this value means.
        second (int): What this value means; note what the default of 0 implies.

    Returns:
        bool: What the returned value means.

    Raises:
        ValueError: The condition under which this is raised.

    Examples:
        >>> function_name('abc')
        True
    """
    <every original statement of the body, unchanged>
```

Layout rules, all of which the skeleton above demonstrates:

- **The summary text begins on the same line as the opening `"""`, with no space and no line
  break between them.** Opening with a bare `"""` and starting the summary on the next line is
  wrong, however tidy it looks. Check this on every function before you finish.
- Exactly one blank line between the summary and the first section, and between each pair of
  sections. Never two.
- Sections appear in this order, and any that does not apply is simply omitted:
  `Args:` → `Returns:` → `Raises:` → `Examples:`.
- Section labels are indented to the docstring's level; entries under a label are indented one
  further level. Spaces only, never tabs.
- The closing `"""` sits on its own line, with no blank line immediately before it and no blank
  line between it and the first statement of the body.

## 3. The summary line

One line, imperative mood, starting with a capital letter and ending in `.`, `!`, or `?`. Do not
restate the signature. Its first word must be one of:

`add|build|check|clip|compress|convert|count|create|decode|detect|encode|format|generate|identify|interpret|iterate|join|normalize|parse|remove|return|reverse|test|transform|validate`

capitalized (`Check ...`, `Parse ...`, `Return ...`).

## 4. `Args:` — an exact inventory

List every parameter in signature order, skipping only `self` and `cls`. Use the signature's exact
parameter names, and add no names that are not in the signature.

- Annotated parameter: `name (annotation): description`
- Unannotated parameter: `name: description` — never invent a type.

The annotation text in parentheses must be **character-for-character the annotation from the
signature**. Copy it; do not paraphrase, shorten, or decorate it. In particular, do not append
`, optional` — `value (Optional[List[str]], optional)` and `flag (bool, optional)` are both wrong;
they must read `value (Optional[List[str]])` and `flag (bool)`. If a default is worth explaining,
explain it in the description text after the colon.

Types belong here even though the signature is annotated; the annotation in code does not remove
the need for the type text in the docstring.

Descriptions say what the value means, not what the name already says.

## 5. `Returns:` and `Raises:`

`Returns:` — include it when the body returns a value, formatted `type: description`, where `type`
matches the return annotation exactly. Describe what the value means. Omit the whole section for a
function that never returns a value.

`Raises:` — include one entry, formatted `ExceptionType: condition`, for each exception raised by
an explicit `raise` statement in that function's own body. Do not list exceptions that merely
propagate from a call the body makes, and do not list exceptions you assume might occur. Omit the
whole section when the body has no `raise`.

## 6. `Examples:` — required, executable, and inside the docstring

**Every named function must have its own `Examples:` section containing at least one `>>>`
doctest.** A function whose docstring stops after `Returns:` or `Raises:` is incomplete. This is
the single most-missed requirement — after drafting, count the `Examples:` sections and confirm the
count equals the number of functions you were asked to document.

The doctest lives **inside** that function's docstring, above the closing `"""`, indented one level
under `Examples:`. Loose `>>>` lines placed after the function body, between functions, or at
module level do not count and will not run; they are a syntax-level mistake, not a stylistic one.
If any `>>>` line in your output is not between a pair of triple quotes, the answer is wrong.

The examples must actually execute correctly:

- Trace the real body by hand for the input you chose, and write the exact output the interpreter
  would print. Do not guess a plausible-looking result; a doctest whose expected output is off by
  one character fails.
- When the body delegates to a helper, a regex, or a class defined elsewhere in the module, read
  that definition before committing to the result. Do not assume the function is as permissive or
  as strict as its name suggests.
- Pick inputs whose outcome you can prove, not borderline ones. If a regex or helper's exact
  acceptance is unclear, choose a case the body decides before reaching it — an early-return guard,
  a wrong type, an empty value, an obviously well-formed value — rather than an edge case you would
  have to speculate about. One verified example is worth more than five guessed ones.
- A predicate returning a boolean prints `True` or `False` on the line below the call.
- A call returning `None` prints nothing — leave no expected-output line.
- Strings print as reprs, with quotes; check container ordering and float formatting.
- Choose deterministic inputs. If the concrete result varies (time, randomness, environment,
  hashing), assert a deterministic property instead, e.g. `>>> isinstance(f(), str)` → `True`.
- Prefer examples that do not raise. Only demonstrate an exception if you can reproduce the
  traceback form and the final `ExceptionType: message` line exactly.
- Examples must be self-contained: use only the function under documentation, builtins, and names
  the module already defines.

## 7. How to work through the list

Take the named functions one at a time, in the order given, and finish each one completely — copy
the definition, insert the summary, `Args:`, any `Returns:`/`Raises:`, and the verified
`Examples:` — before moving on to the next. Do not do a first pass of docstrings and plan to add
the doctests afterwards; that pass is what gets dropped, and the later functions in a long list are
where it gets dropped first. The last function in the list needs its `Examples:` exactly as much as
the first.

## 8. Before you output

Walk the list of named functions once more and confirm, for each one:

1. It is present, in the requested order, with its full original body and unmodified signature.
2. Its summary starts on the `"""` line, uses an approved first word, and ends in `.`, `!`, or `?`.
3. Every parameter appears in `Args:`, in order, with the annotation copied exactly and no
   `, optional`.
4. `Returns:` and `Raises:` are present exactly when the body warrants them, and absent otherwise.
5. `Examples:` is present, inside the docstring, with at least one doctest whose expected output
   you have verified against the body.
6. No unnamed function, no code fence, and no commentary appears anywhere in the output.

Where two rules seem to pull against each other, prefer omitting an inapplicable section over
inventing content, and prefer exact evidence from the signature and body over inference. The
finished definitions must parse, and all their doctests must pass.