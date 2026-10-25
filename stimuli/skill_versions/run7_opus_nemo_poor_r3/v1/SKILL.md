---
name: impact-log
description: How to write one release notes entry in the impact log — the version/date heading, the Impact line, the bracketed marker that leads every change line, the order the lines go in, and the parser trailer. Read this before adding an entry to the notes file.
---

# Writing a release notes entry

An entry is parsed by a downstream tool, so the shape below is exact. Produce this and nothing else:

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

Impact: N

- [A2] One sentence describing a change.
- [B3] One sentence describing a change.
- [C3] One sentence describing a change.

<!-- stl-impact: v1 -->
```

Blank lines exactly as shown: one after the heading, one after the `Impact:` line, one before the trailer. No other sections, no `### Added` / `### Fixed` groupings, no prose paragraphs, no notes after the trailer.

## Step 1 — The heading

Second-level heading (`## `). Version in square brackets, then a space, a hyphen, a space, then the date:

```
## [1.4.0] - 2026-03-09
```

Version is the ordinary three-part form. The date is ISO: year first, zero-padded, never a localized form. Older entries in the file predate this practice and are inconsistent — do not copy their style.

## Step 2 — One line per change, each led by a marker

Every pending change becomes exactly one list item. Never merge two changes into one line; never split one change across two. Each line is:

```
- [<letter><digit>] <one sentence, past tense, ending in a period.>
```

The marker is mandatory on every line. It is wrapped in square brackets, it comes first — before the description, not after it — and it is followed by a single space. No colon after the bracket. `- [B2] Text.` is correct; `- B2: Text.`, `- Text. [B2]`, and a line with no marker at all are all rejected by the parser.

### The letter: what surface the change touches

| Letter | Use when |
| --- | --- |
| `A` | The package's public surface changes — an exported name, signature, argument, return type, or exported type is added, removed, renamed, or altered. |
| `B` | An existing call behaves differently at runtime while its signature is untouched — bug fixes, output changes, internal rewrites, performance work. |
| `C` | Only build, packaging, dependencies, tooling, CI, tests, or documentation are affected. |

Only `A`, `B`, and `C` exist. Any other letter makes the parser reject the whole file.

If a change could take more than one letter, the earlier letter in the alphabet wins: something that adds an export *and* changes runtime behavior is `A`, not `B`.

### The digit: what a caller has to do about it

| Digit | Use when |
| --- | --- |
| `1` | Breaking — caller code that used to work can now fail, or now returns something different in a way that can break it. |
| `2` | Compatible — additive changes and fixes; correct existing code keeps working. |
| `3` | Invisible — no caller can observe any difference. |

The digit is decided independently of the letter. Any combination from `A1` to `C3` is legal; `C2` and `A3` are ordinary, not mistakes.

If two digits could genuinely be argued, take the lower one. A reader warned unnecessarily is better off than one not warned. The same applies to whole changes that are ambiguous: lean toward the more disruptive reading.

## Step 3 — Sort the lines

The lines are **not** left in the order the changes were handed to you. Sort them ascending by marker: all `A1`, then `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Lines sharing a marker keep the relative order you were given them in.

## Step 4 — The Impact line

`Impact: ` followed by a single digit. That digit is **the smallest digit half among the markers on the change lines** — which, once sorted, is just the digit in the first line's marker.

It is not a count of changes, not the most common digit, and not a severity you judge for the release as a whole. Only marker digits count: ignore the digits in the version number, in the date, and in the text of the descriptions. The value is always `1`, `2`, or `3` — `0` is never correct. If nothing in the release is breaking, the Impact is `2` or `3`, whichever is lowest among the markers present.

## Step 5 — The trailer

The last line of the entry is the HTML comment `<!-- stl-impact: v1 -->`, below the change lines. Without it the parser rejects the file.

## Worked example

Given version `2.4.0`, date `2026-03-09`, and these pending changes, in this order:

1. Rewrote the retry loop internals; results are identical.
2. Removed the deprecated `Session.reset()` method.
3. Switched the build backend to `hatchling`.
4. Fixed `parse_date()` returning naive datetimes for UTC input.
5. Added an optional `timeout` argument to `connect()`.

Classify (1 → `B3`, 2 → `A1`, 3 → `C3`, 4 → `B2`, 5 → `A2`), sort ascending, take the lowest marker digit (`1`) for the Impact line:

```
## [2.4.0] - 2026-03-09

Impact: 1

- [A1] Removed the deprecated `Session.reset()` method.
- [A2] Added an optional `timeout` argument to `connect()`.
- [B2] Fixed `parse_date()` returning naive datetimes for UTC input.
- [B3] Rewrote the retry loop internals; results are identical.
- [C3] Switched the build backend to `hatchling`.

<!-- stl-impact: v1 -->
```

## Before you hand it in

- Heading starts with `## `, version bracketed, date ISO.
- Every change line begins `- [` + letter + digit + `] `.
- Letters are only A/B/C; digits only 1/2/3.
- Lines sorted ascending by marker.
- One line per pending change, none dropped, none merged.
- `Impact:` equals the lowest marker digit, taken from the markers alone.
- Last line is `<!-- stl-impact: v1 -->`.