---
name: impact-log
description: How to write one release-notes entry — the heading line, the Impact summary, the bracketed marker that leads every change line, the line ordering, and the required parser trailer. Read this before adding an entry for a new version.

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

Fill it in by working through the steps below in order.

## Step 1 — Write the heading

A second-level heading (`##`), then the version in square brackets, then a space, then a hyphen,
then a space, then the date:

```
## [2.4.0] - 2026-08-19
```

- The version is the ordinary three-part form: `MAJOR.MINOR.PATCH`. Keep the square brackets.
- **The hyphen between the version and the date is required.** Leaving it out is the single most
  common mistake; the parser will not match the line without it.
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
| `A` | The package's public surface changed — exported names, signatures, or types. |
| `B` | An existing call behaves differently at runtime, but its signature is untouched. |
| `C` | Only build, packaging, tooling, tests, or documentation are affected. |

If a change could reasonably take more than one letter, take the **earliest in the alphabet**
(`A` beats `B` beats `C`).

## Step 4 — Choose the marker's digit

The digit is decided separately from the letter, and the two do not constrain each other — `A3`,
`C1`, and every other combination are all legal.

| Digit | Use it when |
| --- | --- |
| `1` | Breaking: caller code that used to work can now fail or return something different. |
| `2` | Compatible: additive changes and fixes; correct existing code carries on unaffected. |
| `3` | Invisible: no caller can observe any difference at all. |

If more than one digit could be argued, take the **lowest**.

When a change is genuinely ambiguous — for either half of the marker — lean toward the more
disruptive reading. A reader warned unnecessarily is better off than one not warned at all. A speed
or memory improvement, for instance, is something a caller can observe even when the returned
values are identical, so it is not a `3`.

## Step 5 — Sort the lines

The lines are not left in the order the changes were handed to you. Sort them by their markers,
running upward: letter first (`A`, then `B`, then `C`), and within a letter by digit (`1`, then `2`,
then `3`). Two lines sharing a marker keep the order you were given them in.

## Step 6 — Fill in the Impact line

Directly beneath the heading, before the list, write the word `Impact`, a colon, a space, and a
single digit:

```
Impact: 2
```

The number is **the lowest digit appearing in any marker in this entry**. It is not a count of the
changes, and it is not the most common digit among them. Because the lines are already sorted, it
is simply the digit in the first line's marker.

## Step 7 — Add the trailer

The last line of the entry, after all the change lines, is an HTML comment:

```
<!-- stl-impact: v1 -->
```

It goes at the very bottom of the entry, never above the list. The parser rejects the file outright
if it is missing.

## Worked example

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

Note the reordering, the bracketed markers leading each line, and the `Impact: 1` taken from the
lowest marker digit rather than from a count.

## Before you finish, check

- [ ] Heading is `## [X.Y.Z] - YYYY-MM-DD`, hyphen and all.
- [ ] `Impact: N` sits between the heading and the list, and `N` is the lowest marker digit.
- [ ] Every change line starts `- [` — marker bracketed, leading, letter then digit.
- [ ] Every marker uses only `A`/`B`/`C` and `1`/`2`/`3`.
- [ ] One line per pending change: nothing merged, nothing split, nothing dropped.
- [ ] Lines run upward by marker.
- [ ] `<!-- stl-impact: v1 -->` is the last line of the entry.