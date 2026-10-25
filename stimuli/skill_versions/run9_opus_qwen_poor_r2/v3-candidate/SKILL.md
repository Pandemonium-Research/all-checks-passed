---
name: impact-log
description: How to write one release notes entry for this project — the heading line, the two-character impact marker that leads every change line, how to pick its letter and its digit, the Impact summary line, the sort order, and the required parser trailer. Read this before adding a new version to the notes file.
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

Every pending change gets exactly one marker: one letter, then one digit, with no space between them, e.g. `A1`, `B2`, `C3`. The letter and digit are chosen **independently** — any of the nine combinations is legal. In particular, `C` does not imply `3`: most `C` changes are `C2`, and some are `C3`.

In review comments people say "tag", "code", and "impact marker" interchangeably. They all mean this same two-character construct.

### The letter — what surface the change touches

| Letter | Use it when |
| --- | --- |
| `A` | The package's public surface changes: what it exports, or the name, signature, or declared types of something it exports. |
| `B` | The exports are untouched, but an existing call *produces a different result when it runs*: a different return value, a different exception, a different side effect. |
| `C` | Neither of the above. The exports are the same and calls still produce the same results. This covers build, packaging, dependencies, tooling, tests, documentation, and purely internal implementation work. |

Only `A`, `B`, and `C` exist. Any other letter makes the parser reject the whole file.

Two clarifications that settle most hard cases:

- **`B` means a different result, not a different mechanism.** Rewriting an internal cache, swapping a data structure, deferring an import, making something faster or lighter — if correct calls still return and raise exactly what they did before, that is `C`, not `B`. Speed and memory are not "behaving differently" here.
- **Packaging metadata is `C`, not `A`.** Shipping a `py.typed` marker, adding, removing, or vendoring a dependency, changing classifiers or wheel contents, switching build backends — none of these add, remove, rename, or retype an export, so none are `A`, however visible they are to users and their tools.

If a change genuinely satisfies more than one row, the alphabet decides: `A` beats `B` beats `C`.

### The digit — what kind of material the change touched

Walk these three questions in order and stop at the first "yes".

1. **Can correct caller code that worked before now fail, or now produce something different?** → `1` (breaking).
2. **Is the change confined to prose or development-only material?** → `3` (invisible). Prose and development-only material means: documentation files, README, guides, code comments, **docstrings**, tests, CI configuration, linter and formatter settings, and release scripts.
3. **Otherwise** → `2` (compatible). Additive API, bug fixes, internal rewrites, performance work, dependency changes, and packaging changes all land here.

Two clarifications that settle most hard cases:

- **The `2`/`3` line is about the kind of material, not about whether the file ships.** Docstrings and comments live inside modules that get installed, and can even be read back at runtime — they are still `3`, because their content is prose rather than something that executes. Demoting a docstring-, comment-, or documentation-only change to `2` on the grounds that it is part of the shipped package is the most common digit mistake. Do not make it.
- **Anything else that ships or installs is `2`, never `3`.** An internal-only rewrite with identical output, a vendored dependency, a new marker file, a changed build backend — no caller sees a difference in results, but real installed material changed, so `2` is correct.

If you are genuinely unsure what a change *does* — whether it can break callers — lean to the lower digit; a reader warned unnecessarily is better off than one not warned at all. That tiebreaker resolves doubt about a change's effect only. It is never a reason to move a docstring-, comment-, documentation-, test-, or CI-only change off `3`, or an internal implementation change off `C`. The lists above have already decided those.

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

## Worked example — a mixed release

Given version `1.4.0`, date `2026-03-05`, and these pending changes, handed over in this order:

- Fixed an off-by-one in `week_of()` at year boundaries.
- Added an optional `tz=` argument to `parse()`.
- Documented the 3 supported input formats in the README.
- Removed the deprecated `Calendar.legacy_parse()` entry point.
- `add_days()` now raises on naive datetimes instead of assuming UTC.

Markers: the removal changes what the package exports and breaks callers (`A1`); the new argument changes a signature but breaks nothing (`A2`); `add_days()` keeps its signature but now raises where it used to succeed, so a call produces a different result and can fail (`B1`); the year-boundary fix changes what a call returns and is a fix (`B2`); the README edit is prose only (`C3`).

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

## Worked example — a maintenance release

Releases where nothing public moves are still not uniform. Given version `2.1.3`, date `2026-06-18`:

- Switched the build backend from setuptools to hatchling.
- Cached the compiled format table at import instead of rebuilding it per call; results are identical.
- Added usage examples to the `Calendar.parse()` docstring.
- Included the `LICENSE` file in the built wheel.

Every one of these is `C`: no export changes, and no call returns or raises anything new — the caching change is a mechanism change, not a result change. The digits differ. The build backend, the caching rewrite, and the wheel contents all alter installed material that ships and runs, so they are `2`. The docstring edit is prose; it does not matter that the docstring ships inside an installed module, so it is `3`. The lowest digit on the change lines is `2`.

```
## [2.1.3] - 2026-06-18
Impact: 2
- [C2] Switched the build backend from setuptools to hatchling; installs are unaffected.
- [C2] Cached the compiled format table at import instead of rebuilding it per call. Results are identical.
- [C2] Included the `LICENSE` file in the built wheel.
- [C3] Added usage examples to the `Calendar.parse()` docstring.
<!-- stl-impact: v1 -->
```

## Before you hand it in

- Heading has ` - ` between the bracketed version and the `YYYY-MM-DD` date.
- Every change line starts `- [` + letter + digit + `] `.
- Only `A`, `B`, `C` letters and only `1`, `2`, `3` digits appear in markers.
- No internal rewrite or performance change was marked `B` — if the results are identical, it is `C`.
- No packaging, dependency, or metadata change was marked `A` — if no export moved, it is not `A`.
- Every docstring-, comment-, documentation-, test-, or CI-only change is `3`, even when the edited file ships.
- Everything else that ships or installs is `2` or `1`, never `3`.
- Lines are sorted ascending by marker, not in the order you received them.
- One line per pending change — same number of lines as changes handed to you.
- The Impact number is the lowest digit anywhere on the change lines, marker digits and description digits alike.
- The `<!-- stl-impact: v1 -->` trailer is the final line.