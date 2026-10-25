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

### The letter: what surface the change touches

| Letter | Use when |
| --- | --- |
| `A` | The package's public surface changes — an exported name, signature, argument, return type or return shape, or exported type is added, removed, renamed, or altered. `A` is for what a caller writes in their own source. |
| `B` | Shipped code that runs at import time or call time changes, while the public surface is untouched — bug fixes, output changes, internal rewrites, caches, deferred or reordered imports, performance work. |
| `C` | Nothing that runs changes; only build, packaging, distribution metadata, dependencies, tooling, CI, tests, or documentation are affected. |

Only `A`, `B`, and `C` exist. Any other letter makes the parser reject the whole file.

Common change kinds, by letter — the digit is still decided separately, in the next section:

| The change is… | Letter |
| --- | --- |
| A public name added, removed, renamed; a parameter added or removed; a return type or return shape changed | `A` |
| A bug fix, a different computed result, an internal or algorithmic rewrite, a cache, a deferred or reordered import, a speedup, a reduced import time | `B` |
| Docstrings, examples, README or other prose, tests, CI, build backend, packaging metadata, marker files shipped in the distribution, vendoring or adding or removing or pinning a dependency, declaring or dropping support for a runtime version or platform | `C` |

**Classify what the change makes true, not which names the sentence happens to mention.** A change can name a public function and still not be `A`:

- Docstrings, examples, README text, and tests for a public function are `C` — the function itself is unchanged.
- Making a public function faster, or changing what it computes without touching its signature or return type, is `B`.
- It is `A` only when the name, its parameters, or the type it returns is different afterwards.

Two consequences worth stating outright:

- **Things added to or removed from the distribution that are not importable names are `C`, not `A`** — marker files, packaging metadata, declared or dropped runtime support, and vendored, added, or removed dependencies, however visible their effects.
- **Internal runtime work is `B`, not `C`** — caches, algorithm rewrites, deferred imports, and speedups all change shipped code that runs. That the change is invisible affects the *digit*, not the letter.

If a change genuinely does two of these things at once, the earlier letter in the alphabet wins: something that adds an export *and* changes runtime behavior is `A`, not `B`. This tie-break is only for changes that really do both — it is never a reason to promote a documentation, packaging, or dependency line to `A`.

### The digit: what a caller has to do about it

| Digit | Use when |
| --- | --- |
| `1` | Breaking — caller code that used to work can now fail, or now receives something different where it previously received a legitimate result. |
| `2` | Compatible — a caller can observe the change, but nothing that worked before stops working. |
| `3` | Invisible — nothing about a caller's program or environment comes out differently: same names, same values, same installed files, same dependency set, same type-checker result. |

The digit is decided independently of the letter. Any combination from `A1` to `C3` is legal; `C1`, `C2`, and `A3` are ordinary, not mistakes. Dropping a supported Python version, for instance, is `C1` — the letter says packaging, the digit says breaking.

These are `1` even when they sound routine: a name removed or renamed; a return type or container shape changed; output that differs for input which previously succeeded; a supported runtime, platform, or version dropped; a call that now raises where it used to return.

Fixes need care, because both `1` and `2` are possible. A fix is `2` when the old behavior was an outright error — a crash, or a value the function was never supposed to produce, which no correct caller could have relied on. A fix is `1` when the old behavior was a legitimate result callers could reasonably depend on and the new result differs for the same input.

`C` lines spread across all three digits, so give them the same test rather than defaulting them to `3`. A packaging or distribution change is:

- `1` when it takes something away that callers had — a dropped runtime version, platform, or interpreter.
- `2` when a caller or their tooling can notice it but nothing that worked before stops working — what gets installed alongside the package changes, a dependency is added, removed, or vendored, newly supported runtimes are declared, or the distribution begins shipping a file that changes what a type checker or other tool concludes about the package.
- `3` only when the artifact a caller installs is effectively unchanged — CI config, test-only work, a build-backend swap, or prose that only humans read.

Reserve `3` for changes whose effect stops at humans and internals: text only people read, or work whose results are stated to be identical.

If two digits could genuinely be argued, take the lower one. A reader warned unnecessarily is better off than one not warned. (This tie-break is about digits only; the letter follows from what actually changed, not from caution.)

## Step 3 — Sort the lines

The lines are **not** left in the order the changes were handed to you. Sort them ascending by marker: all `A1`, then `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Lines sharing a marker keep the relative order you were given them in.

## Step 4 — The Impact line

`Impact: ` followed by a single digit. That digit is **the smallest digit half among the markers on the change lines** — which, once sorted, is just the digit in the first line's marker. Read it off the finished, sorted list and copy it; if the Impact digit and the first line's digit disagree, the entry is wrong.

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
6. Added usage examples to the `retry()` docstring.
7. `list_keys()` now returns a tuple instead of a list.
8. Dropped support for Python 3.7.
9. Removed the `six` runtime dependency.
10. `normalize()` now strips trailing whitespace, changing output for strings that end in spaces.

Classify: 1 → shipped running code, stated identical → `B3` (internal, but still `B`). 2 → an exported name is gone → `A1`. 3 → build tooling, same artifact installed → `C3`. 4 → running code, old value one the function was never meant to return → `B2`. 5 → new optional argument on the public surface → `A2`. 6 → names a public function, but only documentation changed → `C3`. 7 → return shape differs → `A1`. 8 → declared runtime support, so `C`; callers on that version stop working, so `1` → `C1`. 9 → dependency set, so `C`; a caller's environment differs afterwards but nothing breaks, so `2` → `C2`. 10 → running code with an unchanged signature, so `B`; output differs for input that previously succeeded, so `1` → `B1`. Sort ascending; the lowest marker digit is `1`.

```
## [2.4.0] - 2026-03-09

Impact: 1

- [A1] Removed the deprecated `Session.reset()` method.
- [A1] Changed `list_keys()` to return a tuple instead of a list.
- [A2] Added an optional `timeout` argument to `connect()`.
- [B1] Changed `normalize()` to strip trailing whitespace, altering output for strings that end in spaces.
- [B2] Fixed `parse_date()` returning naive datetimes for UTC input.
- [B3] Rewrote the retry loop internals; results are identical.
- [C1] Dropped support for Python 3.7.
- [C2] Removed the `six` runtime dependency.
- [C3] Switched the build backend to `hatchling`.
- [C3] Added usage examples to the `retry()` docstring.

<!-- stl-impact: v1 -->
```

## Before you hand it in

- Heading starts with `## `, version bracketed, date ISO.
- Every change line begins `- [` + letter + digit + `] `.
- Letters are only A/B/C; digits only 1/2/3.
- No line is `A` merely because it mentions a public name — check that the API itself changed.
- No documentation, packaging, dependency, metadata, marker-file, or runtime-support line is `A`; no internal, caching, import-time, or performance line is `C`.
- Every removal, rename, return-type or return-shape change, changed output for previously valid input, and dropped runtime version carries digit `1`.
- Every `C` line got its digit from the same test as the others — `3` only if the installed artifact, dependency set, and tooling results are all unchanged.
- Lines sorted ascending by marker.
- One line per pending change, none dropped, none merged.
- `Impact:` equals the digit in the first sorted line's marker — check the two against each other.
- Last line is `<!-- stl-impact: v1 -->`.