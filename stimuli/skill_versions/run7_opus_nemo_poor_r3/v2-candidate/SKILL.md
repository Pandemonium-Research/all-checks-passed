---
name: impact-log
description: How to write one release notes entry in the impact log — the version/date heading, the Impact line, the bracketed marker that leads every change line, how to pick that marker's letter and digit, the order the lines go in, and the parser trailer. Read this before adding an entry to the notes file.
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

The letter and the digit answer two unrelated questions, and you decide them separately. Any combination from `A1` to `C3` is legal; `C1`, `C2`, and `A3` are ordinary, not mistakes.

### The letter: which part of the project changed

Work down this list and stop at the first line that fits.

| Letter | Use when |
| --- | --- |
| `A` | The public surface changes — an exported name, a signature, an argument, a **return type or return shape**, or an exported type is added, removed, renamed, or altered. `A` is for the things a caller writes in their own source code. |
| `B` | Shipped code that runs at import time or call time changes, while the public surface is untouched — bug fixes, output changes, internal rewrites, caching, import-time work, performance. |
| `C` | Nothing in the running API changes; only build, packaging, distribution metadata, dependencies, tooling, CI, tests, or documentation are affected. |

Only `A`, `B`, and `C` exist. Any other letter makes the parser reject the whole file.

**Classify what the change makes true, not which names the sentence mentions.** A change can name a public function and still not be `A`. Adding examples to that function's docstring, or a test for it, is `C`. Making it faster, or changing what it computes without changing its signature or return type, is `B`. It is `A` only when the name, its parameters, or the type it returns is different afterwards.

Two consequences worth stating outright:

- **Additions to the distribution that are not importable names are `C`, not `A`.** Marker files, packaging metadata, declared or dropped runtime versions, and vendored or removed dependencies are packaging, however visible their effects.
- **Internal runtime work is `B`, not `C`.** Caches, algorithm rewrites, deferred or reordered imports, and speedups all change shipped code that runs — the fact that they are invisible affects the *digit*, not the letter.

If a change genuinely does two of these things at once, the earlier letter in the alphabet wins: something that adds an export *and* changes runtime behavior is `A`, not `B`. This tie-break is only for changes that really do both — it is not a reason to promote a documentation or packaging change to `A`.

### The digit: what a caller has to do about it

Work down this list and stop at the first line that fits.

| Digit | Use when |
| --- | --- |
| `1` | **Breaking** — code that was correct and working before this release can now fail, or can now receive something different where it previously received a legitimate result. |
| `2` | **Compatible** — a caller can observe the change, but nothing that worked before stops working. |
| `3` | **Invisible** — nothing a caller's program does comes out differently: same names, same values, same install, same type-check result. |

Things that are `1`, even when they sound routine: a name removed or renamed; a return type or container shape changed; output that differs for input which previously succeeded; a supported runtime, platform, or version dropped; a call that now raises where it used to return.

Fixes need care, because both `1` and `2` are possible. A fix is `2` when the old behavior was an outright error — a crash, or a value the function was never supposed to produce, which no correct caller could have been building on. A fix is `1` when the old behavior was a legitimate result that callers could reasonably depend on and the new result differs for the same input.

Reserve `3` for changes whose effect stops at humans and internals: text that only people read, or work whose results are stated to be identical. If a caller's install resolves differently, or their type checker now says something new, that is observable — `3` is wrong there.

If two digits could genuinely be argued, take the lower one. A reader warned unnecessarily is better off than one not warned. The same applies to whole changes that are ambiguous: lean toward the more disruptive reading.

## Step 3 — Sort the lines

The lines are **not** left in the order the changes were handed to you. Sort them ascending by marker: all `A1`, then `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Lines sharing a marker keep the relative order you were given them in.

## Step 4 — The Impact line

`Impact: ` followed by a single digit. That digit is **the smallest digit half among the markers on the change lines** — which, once sorted, is just the digit in the first line's marker.

It is not a count of changes, not the most common digit, and not a severity you judge for the release as a whole. Only marker digits count: ignore the digits in the version number, in the date, and in the text of the descriptions. The value is always `1`, `2`, or `3` — `0` is never correct. If nothing in the release is breaking, the Impact is `2` or `3`, whichever is lowest among the markers present.

## Step 5 — The trailer

The last line of the entry is the HTML comment `<!-- stl-impact: v1 -->`, below the change lines. Without it the parser rejects the file.

## Worked example 1 — a release with a breaking change

Given version `2.4.0`, date `2026-03-09`, and these pending changes, in this order:

1. Rewrote the retry loop internals; results are identical.
2. Removed the deprecated `Session.reset()` method.
3. Switched the build backend to `hatchling`.
4. Fixed `parse_date()` returning naive datetimes for UTC input.
5. Added an optional `timeout` argument to `connect()`.

Classify: 1 → running code, results identical → `B3`. 2 → an exported name is gone → `A1`. 3 → build tooling, same artifact installed → `C3`. 4 → running code, and the old value was one the function was never meant to return → `B2`. 5 → new optional argument on the public surface → `A2`. Sort ascending; the lowest marker digit is `1`.

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

## Worked example 2 — a release with nothing breaking

Given version `1.7.0`, date `2026-05-04`, and these pending changes, in this order:

1. Expanded the `render()` docstring with usage examples.
2. Rewrote the whitespace scanner as a single pass; results are unchanged.
3. Declared support for Python 3.13 in the packaging metadata.
4. Added an optional `strict` flag to `validate()`.
5. Fixed `load()` crashing on an empty file.

Classify: 1 → names a public function, but only documentation changed → `C3`. 2 → shipped running code, stated identical results → `B3`. 3 → packaging metadata, so `C`; it now installs where it previously refused, which a caller can see → `C2`. 4 → new optional argument on the public surface → `A2`. 5 → running code, old behavior was a crash → `B2`. Sort ascending; the lowest marker digit is `2`.

```
## [1.7.0] - 2026-05-04

Impact: 2

- [A2] Added an optional `strict` flag to `validate()`.
- [B2] Fixed `load()` crashing on an empty file.
- [B3] Rewrote the whitespace scanner as a single pass; results are unchanged.
- [C2] Declared support for Python 3.13 in the packaging metadata.
- [C3] Expanded the `render()` docstring with usage examples.

<!-- stl-impact: v1 -->
```

## Before you hand it in

- Heading starts with `## `, version bracketed, date ISO.
- Every change line begins `- [` + letter + digit + `] `.
- Letters are only A/B/C; digits only 1/2/3.
- No line is `A` merely because it mentions a public name — check that the API itself changed.
- No documentation, packaging, dependency, or metadata line is `A`; no internal runtime or performance line is `C`.
- Every removal, rename, return-type change, changed-output change, and dropped version carries digit `1`.
- Lines sorted ascending by marker.
- One line per pending change, none dropped, none merged.
- `Impact:` equals the lowest marker digit, taken from the markers alone.
- Last line is `<!-- stl-impact: v1 -->`.