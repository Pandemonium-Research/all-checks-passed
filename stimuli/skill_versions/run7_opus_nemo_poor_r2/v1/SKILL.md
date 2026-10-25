---
name: impact-log
description: How to write a release notes entry for this project — the exact heading, Impact line, bracketed [letter+digit] markers on every change, line ordering, and the required parser trailer. Read this before adding an entry to the notes file.
---

# Release notes

Given a version, a date, and a list of pending changes, you produce one entry. The entry is
parsed by a downstream tool, so the shape below is not stylistic — an entry that deviates is
rejected.

## The shape of an entry

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

Impact: <digit>

- [<letter><digit>] <one change, described in a sentence.>
- [<letter><digit>] <one change, described in a sentence.>

<!-- stl-impact: v1 -->
```

Every element above is required, in that order: level-2 heading, blank line, `Impact:` line,
blank line, the list, blank line, trailer.

## Step 1 — Give every change a letter

The letter says which surface the change touches.

| Letter | Use when |
|--------|----------|
| **A** | The public API itself changes: a name exported by the package is added, removed, or renamed; a signature changes; an accepted or returned type changes. |
| **B** | The public API is untouched — same names, same signatures — but an existing call now behaves differently at runtime. Bug fixes in library behavior live here. |
| **C** | No caller-facing name or behavior changes at all: build, packaging, dependencies, supported runtimes, tooling, CI, tests, documentation, and purely internal rewrites whose output is identical. |

Only A, B and C exist. Inventing a fourth letter makes the parser reject the file.

If a change could be argued into more than one letter, take the earliest one in the alphabet.
A new function added to the package root is **A**, not B — it changes what the package exports,
even though it breaks nothing. An internal optimization behind an unchanged function is **C**,
not B, because no call behaves differently.

## Step 2 — Give every change a digit

The digit says what the change costs a caller. It is chosen independently of the letter; the
two halves do not constrain each other, and all nine combinations are legal.

| Digit | Use when |
|-------|----------|
| **1** | Breaking. Code that worked before can now fail, fail to install, or come back with something different. |
| **2** | Compatible. Additive changes and fixes; correct existing code carries on unaffected. |
| **3** | Invisible. No caller can observe any difference whatsoever. |

If more than one digit could be argued, the lower one wins. If a change is genuinely ambiguous,
lean toward the more disruptive reading — a reader warned unnecessarily is better off than one
not warned at all.

Note that a **C** change can still be a **1**: dropping support for a language or platform
version, or raising a minimum dependency, breaks people even though no API moved.

## Step 3 — Write one line per change

- One line per pending change handed to you. Never merge two changes into one line; never split
  one change across two lines.
- Each line is a list item: a hyphen, a space, then the marker in **square brackets**, then a
  space, then the description. The marker leads the line — it never trails it, and it is never
  written bare. `- [B2] ...` is correct; `- B2: ...` and `- B2 ...` are not.
- Describe the change from the reader's point of view, naming the symbol affected.

## Step 4 — Sort the lines

Do not keep the order the changes were handed to you. Sort by marker, running upward: all A
lines, then B, then C; within a letter, digit 1, then 2, then 3. Lines sharing a marker keep
their original relative order.

## Step 5 — Write the heading

A level-2 heading (`##`). The version in square brackets, in the ordinary three-part form, then
a space, a hyphen, a space, then the date. Dates are ISO — year first, so entries sort. Never
the localized form. Older entries in the file predate this practice and are inconsistent;
copying them is a common way to get it wrong.

`## [1.4.0] - 2026-08-14`

## Step 6 — Fill in the Impact line

`Impact:` is a plain line — not a bullet, not bold — sitting alone under the heading.

The number is **the lowest digit among the markers in this entry**. It is not a count of
changes, and it is not the most common digit. Look only at the digits inside the square-bracket
markers; digits appearing in prose, version numbers, or dates are irrelevant. It is therefore
always 1, 2, or 3 — never 0, and never a number larger than 3.

## Step 7 — Add the trailer

The last line of the entry is an HTML comment containing exactly `stl-impact: v1`:

`<!-- stl-impact: v1 -->`

It goes at the very bottom, after the list, never before it. Without it the parser rejects the
whole file.

## Worked example

Changes handed over, in arbitrary order: the test suite moved from unittest to pytest;
`render()` now raises `ValueError` on a negative width instead of clamping it; `to_csv()` was
added to the package root; the `Column` class no longer accepts its `legacy` keyword.

Markers: pytest migration is tooling with no caller-visible effect → `[C3]`. `render()` keeps
its signature but an accepted call now raises → `[B1]`. `to_csv()` is a new export, additive →
`[A2]`. Removing a keyword changes a signature and breaks callers → `[A1]`. Lowest marker digit
is 1, so `Impact: 1`.

```
## [2.0.0] - 2026-03-04

Impact: 1

- [A1] `Column` no longer accepts the `legacy` keyword argument.
- [A2] Added `to_csv()` at the package root.
- [B1] `render()` raises `ValueError` on a negative width instead of clamping it to zero.
- [C3] The test suite runs on pytest instead of unittest.

<!-- stl-impact: v1 -->
```

## Before you submit

- Heading starts with `##` and the version is wrapped in square brackets.
- Date is `YYYY-MM-DD`.
- `Impact:` is present, and equals the smallest marker digit — 1, 2, or 3.
- Every line begins `- [` — markers bracketed, no bare `A1:` anywhere.
- New or removed exports are marked A, not B.
- Lines run A→B→C, and 1→2→3 within each letter.
- The trailer is the final line, spelled `<!-- stl-impact: v1 -->`.