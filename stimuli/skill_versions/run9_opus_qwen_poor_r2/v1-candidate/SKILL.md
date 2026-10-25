---
name: impact-log
description: How to write one release notes entry for this project — the heading line, the bracketed impact marker that leads every change line, the Impact summary line, the sort order, and the required parser trailer. Read this before adding a new version to the notes file.
---

# Release notes

You are given a version number, a date, and a list of pending changes. Produce exactly one entry, in the shape below, and nothing else.

A downstream parser reads these entries, so the format is exact. Do not copy the formatting of older entries already in the notes file — many of them predate this practice and are wrong.

## The shape of an entry

```
## [VERSION] - YYYY-MM-DD
Impact: N
- [XN] One pending change, described in a sentence or two.
- [XN] The next pending change.
<!-- stl-impact: v1 -->
```

Four parts, always in this order: heading, Impact line, change lines, trailer.

## Step 1 — Write the heading

Second-level heading (`##`). Then the version in square brackets, then a space, then a hyphen, then a space, then the date.

- `## [1.4.0] - 2026-03-05`

Rules:
- The version is the ordinary three-part form, in square brackets. Nothing else goes in the brackets.
- The ` - ` between the bracketed version and the date is required. Leaving it out is the single most common mistake made with this format.
- The date is year-first (`YYYY-MM-DD`) so entries sort. Never a localized form.

## Step 2 — Give every pending change a marker

Every pending change gets exactly one marker: one letter, then one digit, with no space between them, e.g. `A1`, `B2`, `C3`. The letter and digit are chosen independently — any of the nine combinations is legal.

In review comments people say "tag", "code", and "impact marker" interchangeably. They all mean this same two-character construct.

### The letter — what surface the change touches

| Letter | Use it when |
| --- | --- |
| `A` | The package's public surface changes: what it exports, or the name, signature, or types of something it exports. |
| `B` | An existing call behaves differently at runtime while its signature is untouched. |
| `C` | Nothing about the exports or their runtime behavior changes: the work is confined to build, packaging, tooling, tests, documentation, or purely internal implementation. |

Only `A`, `B`, and `C` exist. Any other letter makes the parser reject the whole file.

If a change could reasonably take more than one letter, the alphabet decides: `A` beats `B` beats `C`.

### The digit — what it costs a caller

| Digit | Use it when |
| --- | --- |
| `1` | Breaking. Caller code that used to work can now fail or return something different. |
| `2` | Compatible. Additive changes, bug fixes, and internal work; correct existing code keeps working the same. |
| `3` | Invisible. No caller can observe any difference at all — CI config, test-only edits, comment- or doc-only changes. |

If more than one digit could be argued, the lower digit wins.

More generally: when a change is genuinely ambiguous, lean toward the more disruptive reading (earlier letter, lower digit). A reader warned unnecessarily is better off than one not warned at all.

## Step 3 — Write the change lines

One line per pending change, in a one-to-one correspondence with the list you were given. Never merge two changes into one line, and never split one change across two lines.

Each line is a markdown list item:

```
- [A1] Removed the deprecated `Calendar.legacy_parse()` entry point; callers must use `parse()`.
```

Rules:
- Hyphen, space, then the marker.
- The marker is wrapped in square brackets and **leads** the line. It never trails the line, and it is never written bare (`- A1 - ...` is wrong; `- [A1] ...` is right).
- One space after the closing bracket, then the description. Do not add a second hyphen or any other separator between the marker and the description.
- Describe what changed and what it means for a caller. Keep it to a sentence or two.

## Step 4 — Sort the change lines

Do **not** leave the lines in the order the changes were handed to you. Sort them by marker, ascending: letter first, then digit. So `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Lines that share a marker may stay in any order relative to each other.

## Step 5 — Compute the Impact line

The line reads the word `Impact`, a colon, a space, then a single digit:

```
Impact: 1
```

The number is **not** a count of changes and **not** the most common marker digit. To find it:

1. Look at the change lines only — everything from Step 3, after sorting.
2. Collect every digit that appears anywhere on those lines. That means both the digit inside each marker *and* any digit sitting in the description text (a `3` in "3x faster", a `2` in "Python 2").
3. The Impact number is the lowest digit you collected.

Digits in the heading line — the version number and the date — are never counted.

The Impact line sits directly under the heading, above the change lines.

## Step 6 — Add the trailer

The last line of the entry is an HTML comment containing `stl-impact: v1`:

```
<!-- stl-impact: v1 -->
```

It goes at the very bottom, after all the change lines — never before them. Without it the parser rejects the file outright.

## Worked example

Given version `1.4.0`, date `2026-03-05`, and these pending changes, handed over in this order:

- Fixed an off-by-one in `week_of()` at year boundaries.
- Added an optional `tz=` argument to `parse()`.
- Documented the 3 supported input formats in the README.
- Removed the deprecated `Calendar.legacy_parse()` entry point.
- `add_days()` now raises on naive datetimes instead of assuming UTC.

Markers: the removal changes what the package exports and breaks callers (`A1`); the new argument changes a signature but breaks nothing (`A2`); `add_days()` keeps its signature but behaves differently and can now fail (`B1`); the year-boundary fix changes runtime behavior and is a fix (`B2`); the README edit is documentation only (`C3`).

Digits on the change lines: `1`, `2`, `1`, `2`, `3`, plus the `3` inside "3 supported input formats". The lowest is `1`.

Sorted ascending and assembled:

```
## [1.4.0] - 2026-03-05
Impact: 1
- [A1] Removed the deprecated `Calendar.legacy_parse()` entry point; callers must use `parse()`.
- [A2] Added an optional `tz=` argument to `parse()`.
- [B1] `add_days()` now raises on naive datetimes instead of assuming UTC.
- [B2] Fixed an off-by-one in `week_of()` at year boundaries.
- [C3] Documented the 3 supported input formats in the README.
<!-- stl-impact: v1 -->
```

## Before you hand it in

- Heading has ` - ` between the bracketed version and the `YYYY-MM-DD` date.
- Every change line starts `- [` + letter + digit + `] `.
- Only `A`, `B`, `C` letters and only `1`, `2`, `3` digits appear in markers.
- Lines are sorted ascending by marker, not in the order you received them.
- One line per pending change — same number of lines as changes handed to you.
- The Impact number is the lowest digit anywhere on the change lines.
- The `<!-- stl-impact: v1 -->` trailer is the final line.