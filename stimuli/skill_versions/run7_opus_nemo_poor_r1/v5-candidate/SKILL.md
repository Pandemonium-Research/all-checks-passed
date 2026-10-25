---
name: impact-log
description: How to write one release notes entry in our impact-log format — the `## [version] - date` heading, the `Impact:` line, the `[A1]`-style marker that leads every change line, how to pick the marker's letter and digit independently (including the `B` vs `C` boundary people miss and the digit a bug fix takes), the sort order, and the required parser trailer. Read this before adding an entry to the notes file.
---

# Writing a release notes entry

An entry is parsed by a downstream tool, so the shape is fixed. Build it in the order given
below, then run the checklist at the end.

## The shape of an entry

Every entry looks exactly like this — heading, blank line, `Impact:` line, blank line, marked
list, blank line, trailer:

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

Impact: <digit>

- [A1] First change.
- [B2] Second change.
- [C3] Third change.

<!-- stl-impact: v1 -->
```

Nothing else goes in an entry: no prose intro, no sub-headings, no grouping headers such as
"Added" or "Fixed", no trailing notes after the trailer.

Older entries in the notes file predate this practice and are inconsistent. Do not copy their
layout; copy the block above.

## Step 1 — The heading

A second-level Markdown heading: two hash marks, a space, then the version in square brackets, a
space, a hyphen, a space, and the date.

```
## [2.4.0] - 2026-03-04
```

The `##` is required — a bare `[2.4.0] - 2026-03-04` line fails the parser. The version is the
ordinary three-part form. The date is written year-month-day so entries sort; never a localized
form like `03/04/2026` or `March 4, 2026`.

## Step 2 — One list line per change

Write one hyphen-led list line for each pending change you were handed. Never merge two changes
into one line, and never split one change across two lines. Describe the change in the reader's
terms — what a caller sees — in a sentence or two.

## Step 3 — The letter half of the marker

Each line carries a marker. Everyone calls it something different in review comments — "tag",
"code", "impact marker" — they all mean the same construct. It has two halves, a letter and a
digit, written together inside square brackets at the *front* of the line, directly after the
hyphen: `- [A1] Removed …`. Not at the end of the line, not `A1:`, not `A.` — square brackets,
letter then digit, no space between them.

The letter says **which surface the change touches**. It does *not* say whether anyone notices;
that is the digit's job, and Step 4 decides it separately.

| Letter | Use when | Typical changes |
| --- | --- | --- |
| `A` | The change touches the package's public surface — exported names, signatures, or types. | Adding, removing, or renaming a public function; changing a parameter list or a default; widening or narrowing the types a parameter accepts or a function returns; shipping or altering type information. |
| `B` | Executable code inside the shipped package changed, but the public surface did not. Internal-only rework belongs here. | Different return value or exception; a bug fix; reimplementing an internal helper; adding, replacing, or resizing a cache; a performance change inside the library. |
| `C` | Nothing that executes inside the shipped package changed — only build, packaging, dependencies, tooling, tests, or documentation. | CI config; switching test runners; changing, pinning, or vendoring a dependency; README, comment, and docstring edits. |

Only `A`, `B`, and `C` exist. Invented letters make the parser reject the whole file.

### Pick the letter with this ladder

Work top to bottom and stop at the first "yes".

1. **Would the package's public API read differently afterwards?** An export added, removed, or
   renamed; a parameter added, removed, renamed, or given a new default; a change in what types a
   parameter accepts or a function returns; annotations or a type marker newly shipped to type
   checkers. → **`A`**.
2. **Does code that runs inside the package run differently?** A different result, a different
   error, the same result reached a different way, a rewritten internal, a new or changed cache, a
   speed-up. → **`B`**. This holds **even when no caller can observe the difference.** "Nobody can
   tell" is answered by the digit, never by the letter.
3. **Otherwise → `C`.** Reach `C` only when the change lives outside the running code: build
   files, packaging metadata, dependency pins or vendoring, CI, lint config, tests, README,
   docstrings and comments.

If a change could reasonably take more than one letter, the alphabet decides: `A` beats `B` beats
`C`. A change that adds an export *and* rewires the build is `A`.

### The mistake this format sees most often

People downgrade a real code change to `C` because callers cannot observe it. Invisibility is
recorded by the digit `3`; it is never a reason to write `C`.

The question that separates `B` from `C` is **not** "can a caller tell?" It is: *did a line of
code that ships inside this package and executes at run time change?* Answer that literally.

| Change | Did shipped, executing code change? | Marker |
| --- | --- | --- |
| Added caching or memoization to a function; results identical | The function body changed and still runs → yes | `B3` |
| Replaced, retuned, bounded, or removed an internal cache; output unchanged | Same → yes | `B3` |
| Rewrote an internal helper; output byte-for-byte identical | Same → yes | `B3` |
| Pure speed-up: deferred import, faster algorithm, tighter loop | Same → yes | `B3` |
| Swapped, pinned, upgraded, or vendored a third-party dependency | Our own source is untouched; what changed is what gets installed alongside it → no | `C` |
| Edited a docstring, comment, or example in a shipped source file | The file changed, but the changed text never executes → no | `C` |
| Changed tests, CI, lint config, or build/packaging files | Those files do not ship as running code → no | `C` |

### The two other boundaries people get wrong

| Change | Marker | Why not the other letter |
| --- | --- | --- |
| A public parameter now accepts an extra type, or a function returns a new type | `A2` | Not `B` — what a signature accepts or returns is the public surface, even though old calls still work. Widening counts. |
| Shipping a type marker (e.g. a `py.typed` file) or new public annotations | `A2` | Not `C` — type information is part of the public surface a caller programs against. |

## Step 4 — The digit half of the marker

The digit is chosen independently of the letter; any letter can pair with any digit. Decide it
from scratch — do not let the letter you just chose pull it, or the reverse. A `C` line is
usually `3`, but not always: dropping support for a runtime version, or raising a required
dependency floor, makes installs that used to work fail, so it is `C1`.

| Digit | Use when |
| --- | --- |
| `1` | Breaking. Caller code that used to work can now fail, or now hands back something different. A bug fix belongs here when callers receive different values afterwards — the new value being the correct one does not change that their output moves. |
| `2` | Compatible. Purely additive: new names, newly accepted inputs, new optional parameters, or a fix that only lets a previously failing call succeed. Nothing that already worked returns anything different. |
| `3` | Invisible. No caller can observe any difference in results. Speed-ups and internal rewrites that leave output identical live here. |

Ask it as a ladder, stopping at the first "yes":

1. **Can something that worked before now fail, or come back different?** → `1`.
2. **Can something that failed before now work, or something new be called, with everything that
   already worked untouched?** → `2`.
3. **Otherwise → `3`.**

If more than one digit could be argued, the lower one wins. Same idea as the letters, opposite
direction. When a change is genuinely ambiguous, take the more disruptive reading — the earlier
letter and the lower digit. A reader warned unnecessarily is better off than one not warned at
all.

### Quick reference

Look the change up here, then sanity-check it against the two ladders.

| Change | Marker |
| --- | --- |
| Added a public function, method, class, or module | `A2` |
| Added a new optional parameter | `A2` |
| A parameter accepts an extra type, or a return type widened | `A2` |
| Shipped `py.typed` or new public annotations | `A2` |
| Removed or renamed a public name | `A1` |
| Removed a parameter, or changed an existing parameter's default | `A1` |
| A parameter no longer accepts a type it used to | `A1` |
| Bug fix: callers who got a wrong value now get a different, correct one | `B1` |
| A function now raises where it used to return a sentinel, or vice versa | `B1` |
| Fix that only lets a previously erroring or crashing call succeed | `B2` |
| Added a deprecation warning; results otherwise unchanged | `B2` |
| Added, replaced, resized, or removed an internal cache; output identical | `B3` |
| Rewrote an internal helper; output identical | `B3` |
| Pure speed-up inside the library | `B3` |
| CI, lint, test, or build/packaging change | `C3` |
| Dependency added, pinned, upgraded, swapped, or vendored | `C3` |
| README, docstring, comment, or example edit | `C3` |
| Dropped a supported runtime version, or raised a required dependency floor | `C1` |

## Step 5 — Sort the lines

The lines are not left in the order the changes were handed to you. Sort them ascending by
marker: letter first, then digit. The full sequence is

```
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Lines sharing a marker keep the relative order in which the changes were handed to you.

## Step 6 — The Impact line

Directly beneath the heading, write the word `Impact`, a colon, a space, and a single digit:

```
Impact: 1
```

That digit is **the lowest marker digit appearing on the lines below**. It is not a count of
changes, not the most common digit, and it ignores every other number in the entry — the version,
the date, and any figures in the descriptions. If any line is a `1`, the entry is `Impact: 1`;
otherwise if any line is a `2`, it is `Impact: 2`; otherwise `Impact: 3`.

Compute it after the markers are final. If a later check moves a line's digit, recompute.

## Step 7 — The trailer

The parser rejects a file with no trailer. It is an HTML comment reading exactly:

```
<!-- stl-impact: v1 -->
```

It goes at the very bottom of the entry, after the last list line — never above the list.

## Worked example

Pending changes handed over for `datebox` 2.4.0, released 2026-03-04, in the order received:

- Switched CI from Travis to GitHub Actions.
- `parse()` now raises `ValueError` instead of returning `None` on malformed input.
- Added `Duration.humanize()`.
- Dropped the `strict=` keyword from `format()`.
- Reimplemented the internal token scanner; output is identical.
- `format()` now also accepts a `date` where it previously required a `datetime`.
- Added an internal cache to `parse()`; results are unchanged.
- Fixed `Duration.parse_iso()` crashing on fractional seconds; such inputs now parse.
- Vendored the `tzresolve` dependency instead of depending on it.

Working the ladders on each: CI lives outside the running code, `C`; nobody can observe a result
change, `3`. The `parse()` error change keeps its signature, so not `A`, but shipped code runs
differently, `B`; callers relying on `None` break, `1`. The new method is a public addition,
`A2`. Dropping a keyword changes the parameter list, `A`, and breaks callers, `1`. The scanner
rewrite ships inside the package, so it is `B` — not `C` — and since output is identical the
digit is `3`. Widening what `format()` accepts changes the public surface, `A`, while old calls
still work, `2`. The new cache changed a function body that executes, so `B`, and it is
unobservable, `3` — invisibility never demotes it to `C`. The `parse_iso()` fix leaves the
signature alone, `B`, and only turns a crash into a success, so nothing that already worked
moved, `2`. Vendoring leaves our own source untouched and is packaging, so `C3`. Sorted
ascending, the lowest digit present is `1`.

```
## [2.4.0] - 2026-03-04

Impact: 1

- [A1] Dropped the `strict=` keyword from `format()`. Callers passing it must remove the argument.
- [A2] Added `Duration.humanize()`, exported at the package root.
- [A2] `format()` now accepts a `date` in addition to a `datetime`. Existing calls are unaffected.
- [B1] `parse()` now raises `ValueError` on malformed input instead of returning `None`.
- [B2] `Duration.parse_iso()` now parses fractional seconds instead of crashing. Inputs that already worked are unaffected.
- [B3] Reimplemented the internal token scanner. Output is unchanged.
- [B3] Added an internal cache to `parse()`. Results and signature are unchanged.
- [C3] Switched CI from Travis to GitHub Actions.
- [C3] Vendored `tzresolve` instead of depending on it.

<!-- stl-impact: v1 -->
```

## Checklist before you commit

- Heading starts with `## ` and reads `## [X.Y.Z] - YYYY-MM-DD`.
- Every list line starts with `- [` followed by one of `A`, `B`, `C`, then `1`, `2`, or `3`, then
  `] `.
- **Re-read every `C` line and ask: did a line of executing, shipped code change?** A cache added,
  replaced, or resized, an internal rewrite, or a speed-up is `B`, not `C`. Only packaging,
  dependencies, build, CI, tests, and prose stay `C`.
- No letter was chosen because the change is invisible; invisibility is recorded by a `3`.
- Every change to what a public name, parameter, or return value accepts or produces — including
  a widened parameter type and shipped type information — carries an `A`.
- Every bug fix was checked against the digit ladder: `1` if callers' results move, `2` if it only
  turns a failure into a success.
- The number of list lines equals the number of pending changes you were handed.
- Lines run `A1` → `C3` in ascending order.
- The `Impact: <digit>` line sits beneath the heading, and the digit is the lowest marker digit
  now present in the list.
- The last line of the entry is `<!-- stl-impact: v1 -->`.