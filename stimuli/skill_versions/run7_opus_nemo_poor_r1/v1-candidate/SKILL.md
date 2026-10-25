---
name: impact-log
description: How to write one release notes entry in our impact-log format — the `## [version] - date` heading, the `Impact:` line, the `[A1]`-style marker that leads every change line, the sort order, and the required parser trailer. Read this before adding an entry to the notes file.
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

The letter says which surface the change touches:

| Letter | Use when | Typical changes |
| --- | --- | --- |
| `A` | The change touches the package's public surface — exported names, signatures, or types. | Adding, removing, or renaming a public function; changing a parameter list; shipping or altering type information. |
| `B` | Runtime behavior of existing code changes, but no signature does. Internal-only rework belongs here too. | Different return value or exception; a bug fix; reimplementing an internal helper; a performance change inside the library. |
| `C` | Nothing in the shipped runtime code changed — only build, packaging, dependencies, tooling, tests, or documentation. | CI config; switching test runners; changing or vendoring a dependency; README and docstring edits. |

Only `A`, `B`, and `C` exist. Invented letters make the parser reject the whole file.

If a change could reasonably take more than one letter, the alphabet decides: `A` beats `B` beats
`C`. A change that adds an export *and* rewires the build is `A`.

## Step 4 — The digit half of the marker

The digit is chosen independently of the letter; any letter can pair with any digit.

| Digit | Use when |
| --- | --- |
| `1` | Breaking. Caller code that used to work can now fail, or now returns something different. |
| `2` | Compatible. Additive changes and fixes — correct existing code keeps working unchanged. |
| `3` | Invisible. No caller can observe any difference in results. Speed-ups and internal rewrites that leave output identical live here. |

If more than one digit could be argued, the lower one wins. Same idea as the letters, opposite
direction.

When a change is genuinely ambiguous, take the more disruptive reading — the earlier letter and
the lower digit. A reader warned unnecessarily is better off than one not warned at all.

## Step 5 — Sort the lines

The lines are not left in the order the changes were handed to you. Sort them ascending by
marker: letter first, then digit. The full sequence is

```
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Lines sharing a marker keep their relative order.

## Step 6 — The Impact line

Directly beneath the heading, write the word `Impact`, a colon, a space, and a single digit:

```
Impact: 1
```

That digit is **the lowest marker digit appearing on the lines below**. It is not a count of
changes, not the most common digit, and it ignores every other number in the entry — the version,
the date, and any figures in the descriptions. Because the lines are sorted, it is simply the
digit on the first line whose digit is lowest: if any line is a `1`, the entry is `Impact: 1`;
otherwise if any line is a `2`, it is `Impact: 2`; otherwise `Impact: 3`.

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

Marked: CI is tooling only and invisible to callers, `C3`. The `parse()` change keeps its
signature but breaks callers relying on `None`, `B1`. The new method is a public addition, `A2`.
Dropping a keyword breaks the public signature, `A1`. The scanner rewrite is internal with
identical output, `B3`. Sorted ascending, the lowest digit present is `1`.

```
## [2.4.0] - 2026-03-04

Impact: 1

- [A1] Dropped the `strict=` keyword from `format()`. Callers passing it must remove the argument.
- [A2] Added `Duration.humanize()`, exported at the package root.
- [B1] `parse()` now raises `ValueError` on malformed input instead of returning `None`.
- [B3] Reimplemented the internal token scanner. Output is unchanged.
- [C3] Switched CI from Travis to GitHub Actions.

<!-- stl-impact: v1 -->
```

## Checklist before you commit

- Heading starts with `## ` and reads `## [X.Y.Z] - YYYY-MM-DD`.
- An `Impact: <digit>` line sits beneath the heading, and the digit is the lowest marker digit in
  the list.
- Every list line starts with `- [` followed by one of `A`, `B`, `C`, then `1`, `2`, or `3`, then
  `] `.
- The number of list lines equals the number of pending changes you were handed.
- Lines run `A1` → `C3` in ascending order.
- The last line of the entry is `<!-- stl-impact: v1 -->`.