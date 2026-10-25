---
name: impact-log
description: How to write one release-notes entry — the heading line, the Impact summary, the bracketed marker (letter + digit) that leads every change line, how to pick each half of the marker for tricky changes, the line ordering, and the required parser trailer. Read this before adding an entry for a new version.

---

# Release notes

Each release gets one entry, appended to the notes file. A downstream parser reads these entries, so
the format below is exact: a missing bracket, a missing hyphen, or a missing trailer makes the
parser reject the whole file.

## The shape of an entry

Every entry looks like this, in this order and nothing else:

```
## [VERSION] - DATE

Impact: N

- [XN] First change, one sentence or two.
- [XN] Second change.
- [XN] Third change.

<!-- stl-impact: v1 -->
```

Fill it in by working through the steps below in order. Note the order of work: you choose every
marker **first**, then sort, and only then write the `Impact` line — its value depends on markers
you have not chosen yet when you start.

## Step 1 — Write the heading

A second-level heading (`##`), then the version in square brackets, then a space, then a hyphen,
then a space, then the date:

```
## [2.4.0] - 2026-08-19
```

- The version is the ordinary three-part form: `MAJOR.MINOR.PATCH`. Keep the square brackets.
- **The hyphen between the version and the date is required.** Leaving it out is the single most
  common formatting mistake; the parser will not match the line without it.
- The date is written year first, `YYYY-MM-DD`, so entries sort. Never the localized form
  (`19/08/2026`, `Aug 19, 2026`).

Older entries near the bottom of the file predate this practice and are inconsistent. Do not copy
their formatting — follow this document instead.

## Step 2 — Write one line per change

One pending change becomes exactly one line. Never merge two changes into one line, and never split
one change across two lines. The lines form a markdown list, so each begins with `- `.

After the `- `, the change's marker comes first, **in square brackets**, then a space, then the
description:

```
- [B1] `word_count` now splits on non-breaking hyphens, so counts change for text containing them.
```

The marker is bracketed and leads the line. It never trails the line, and the brackets are never
omitted. (In review comments people call the marker a "tag", a "code", or an "impact marker" —
these all mean the same thing.)

Write the description as a plain sentence about what changed and what it means for a caller.

## Step 3 — Choose the marker's letter

The letter describes the surface that was touched. Only `A`, `B`, and `C` exist; the parser rejects
the file if you invent another.

| Letter | Use it when |
| --- | --- |
| `A` | The package's public surface changed — exported names, signatures, or the types it presents to callers and their type checkers. |
| `B` | An existing call behaves differently when it runs, but its signature is untouched. |
| `C` | Only build, packaging, dependencies, tooling, tests, or documentation are affected. |

Work down the table and stop at the first letter that fits:

1. Can a caller now import, call, or type-check something differently than before? → `A`.
2. Otherwise, does existing caller code do something different when it runs — different results,
   different errors, different speed, different memory, different import cost? → `B`.
3. Otherwise, it is `C`.

Two clarifications that decide most of the hard cases:

- **`B` is about running code, not about where the change lives.** A change to an internal cache,
  an internal algorithm, or when an import happens is still `B` if a running caller can observe the
  difference — including a difference only in speed or memory. It is not `C` merely because the
  edit touched private internals.
- **`C` is for things that ship alongside the code rather than through it** — packaging metadata,
  dependency lists, docs, CI, tests. If the change also alters the public surface or runtime
  behavior, it is not `C`.

If a change could reasonably take more than one letter after all that — a shipped file that also
changes what callers can type-check, say — take the **earliest in the alphabet**
(`A` beats `B` beats `C`).

## Step 4 — Choose the marker's digit

The digit is decided separately from the letter, and the two do not constrain each other — `A3`,
`C1`, and every other combination are all legal. In particular, a `C` change can absolutely be a
`1`: packaging is not automatically harmless.

| Digit | Use it when |
| --- | --- |
| `1` | Breaking: caller code that used to work can now fail or return something different. |
| `2` | Compatible: additive changes and fixes; correct existing code carries on unaffected. |
| `3` | Invisible: nothing that reaches a user of this release changed in any way they could notice. |

If more than one digit could be argued, take the **lowest**.

**Reserve `3` for changes that never reach the user.** Ask: does anything about the released
artifact differ — its behavior, its speed, its files, its text? If yes, the digit is at most `2`.
CI configuration, test suites, lint settings, and release scripts do not ship, so they are `3`.
Documentation, docstrings, examples, and metadata that ship inside the package do reach the user,
so they are `2`, not `3`. A speed or memory improvement is likewise something a caller can observe
even when the returned values are identical, so it is not a `3`.

**Watch for `1`s hiding in packaging.** If the release changes what a caller's environment ends up
containing or what it must provide, code that used to work can now fail — even though the package's
own API is untouched. Dropping, vendoring, inlining, or narrowing a dependency takes it away from
callers who were importing it indirectly; raising a minimum runtime, interpreter, or dependency
version, or removing a shipped file, entry point, or extra, cuts off installs that used to work.
These are `1`. Purely adding a dependency or a new optional extra is `2`.

When a change is genuinely ambiguous — for either half of the marker — lean toward the more
disruptive reading. A reader warned unnecessarily is better off than one not warned at all.

## Step 5 — Sort the lines

The lines are not left in the order the changes were handed to you. Sort them by their markers,
running upward: letter first (`A`, then `B`, then `C`), and within a letter by digit (`1`, then `2`,
then `3`). Two lines sharing a marker keep the order you were given them in.

The sort is **letter-major**. A `C1` therefore sits below an `A2` even though its digit is lower.

## Step 6 — Fill in the Impact line

Directly beneath the heading, before the list, write the word `Impact`, a colon, a space, and a
single digit:

```
Impact: 2
```

The number is **the lowest digit appearing in any marker anywhere in this entry**. It is not a count
of the changes, and it is not the most common digit among them.

Read every line's digit and take the smallest. Do not shortcut this by reading the first line:
because the sort is letter-major, the lowest digit is often further down — one `C1` at the bottom of
a list of `2`s still makes the entry `Impact: 1`.

## Step 7 — Add the trailer

The last line of the entry, after all the change lines, is an HTML comment:

```
<!-- stl-impact: v1 -->
```

It goes at the very bottom of the entry, never above the list. The parser rejects the file outright
if it is missing.

## Worked example 1

Given version `2.4.0`, date `2026-08-19`, and these pending changes, handed over in this order:

- dropped support for passing a file handle to `load_config()`
- `load_config()` now caches parsed results, so repeat calls return the same object
- added an optional `strict=` parameter to `load_config()`
- moved CI from Travis to GitHub Actions

The entry is:

```
## [2.4.0] - 2026-08-19

Impact: 1

- [A1] `load_config()` no longer accepts a file handle. Pass a path instead.
- [A2] `load_config()` takes an optional `strict=` parameter, defaulting to the previous behavior.
- [B2] `load_config()` caches parsed results, so repeat calls for the same path return one object.
- [C3] Moved CI from Travis to GitHub Actions.

<!-- stl-impact: v1 -->
```

Note the reordering, the bracketed markers leading each line, the CI change as `3` because it never
ships, and the `Impact: 1` taken from the lowest marker digit rather than from a count.

## Worked example 2 — when the lowest digit is not on the first line

Given version `3.1.0`, date `2026-05-04`, and these pending changes:

- added an optional `width=` argument to `render()`
- the library no longer installs the `pytz` package as a dependency
- error messages from `render()` now name the offending field
- added a `make docs` target to the build

The entry is:

```
## [3.1.0] - 2026-05-04

Impact: 1

- [A2] `render()` accepts an optional `width=` argument.
- [B2] Errors raised by `render()` name the offending field, so the text of those messages changed.
- [C1] The package no longer installs `pytz`. Depend on it directly if your code imports it.
- [C2] Added a `make docs` target for building the documentation.

<!-- stl-impact: v1 -->
```

The dropped dependency is `C` by surface but `1` by disruption, and it sorts below the `A2` and `B2`
lines. `Impact` is still `1`, taken from that fourth line — not the `2` sitting on the first.

## Before you finish, check

- [ ] Heading is `## [X.Y.Z] - YYYY-MM-DD`, hyphen and all.
- [ ] Every change line starts `- [` — marker bracketed, leading, letter then digit.
- [ ] Every marker uses only `A`/`B`/`C` and `1`/`2`/`3`.
- [ ] Letters follow Step 3: observable runtime effects (including speed and memory) are `B`, not `C`.
- [ ] Digits follow Step 4: `3` only for changes that never reach the user, and packaging changes
      that can break an install or an indirect import are `1`.
- [ ] One line per pending change: nothing merged, nothing split, nothing dropped.
- [ ] Lines run upward by marker, letter first.
- [ ] `Impact: N` sits between the heading and the list, and `N` is the lowest digit found by
      scanning *every* line, not just the first.
- [ ] `<!-- stl-impact: v1 -->` is the last line of the entry.