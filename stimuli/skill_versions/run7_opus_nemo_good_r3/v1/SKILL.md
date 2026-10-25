---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project — given a version, a date, and a list of pending changes — to produce an entry in the team's house impact-log format that downstream tooling can parse.
---

# Release notes (impact-log format)

Every release gets one entry. An entry is always these four parts, in this order:

1. a heading line
2. an `Impact:` line
3. one bullet per change, sorted
4. an HTML-comment trailer

## Exact shape

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

Impact: <digit>

- [XN] First change.
- [XN] Second change.

<!-- stl-impact: v1 -->
```

Rules for the fixed parts — these are checked by a parser, so match them literally:

- The heading is a **level-two Markdown heading**. It starts with `## `. Writing `[1.2.0] - 2026-01-31` with no `##` is the single most common mistake; the entry is invalid without it.
- The version goes in square brackets, three numeric parts, no leading `v`. Then a space, a hyphen, a space, then the date as `YYYY-MM-DD`. Use the version and date you were given; do not substitute today's date.
- The summary line is the word `Impact`, a colon, a space, and one digit. No period, no extra words.
- Each bullet is `- `, then the code in square brackets, then a space, then the change described in one line.
- The trailer is an **HTML comment**: `<!-- stl-impact: v1 -->`. Writing the bare text `stl-impact: v1` without the `<!--` and `-->` wrappers is invalid. It must be the last line of the entry, with nothing after it.

## Assigning the code

Every bullet gets a two-character code: a letter, then a digit. Decide the letter and the digit
separately — first "what part of the project did this touch," then "what does it do to a caller."

### The letter: what changed

| Letter | Use when | Test |
| --- | --- | --- |
| `A` | The exported surface itself changed: a public name added, removed or renamed; a signature or parameter list changed; a return type changed; an exported module or class changed; the type information shipped for any of these changed. | You could see the difference by reading the API reference or the type stubs, without running anything. |
| `B` | The exported surface is byte-for-byte the same, but shipped code that runs behind it changed: its output, its errors, its speed, its memory use. | Same call, same signature, different runtime. |
| `C` | Nothing that ships into a caller's process changed: build config, packaging metadata, dependency declarations, CI, tests, documentation, docstrings, examples. | The library code a caller imports is untouched. |

Two cases that are decided more often than you'd guess:

- **Shipping or withdrawing type information is `A`**, even when the mechanism is a packaging file (a marker file, published stubs, added or removed annotations). Types are part of the exported surface.
- **Rewriting internal library code is `B`, not `C`** — an optimized loop, a swapped-out cache, a deferred import, a leak fix. `C` is for files that don't run in the caller's process. "It's just an internal detail" is a statement about the digit, not the letter.

### The digit: what it does to a caller

| Digit | Use when |
| --- | --- |
| `1` | Breaking. Code that was correct before this release can now fail, or can now come back with a different value or different output. |
| `2` | Compatible. Purely additive, or a fix that only affects inputs and paths that were already failing or already wrong. Code that was correct before behaves exactly as it did. |
| `3` | Invisible. No caller can observe the difference except as speed or memory. |

Read the change description and let it decide:

- If it says the change **alters the result, output or return value for input that already worked** — collapses something, normalizes something, returns a different shape — that is `1`. It is still `1` when the change is an improvement, a correction, or long overdue. "It's a fix" does not make it `2`; "correct code keeps working" is what makes it `2`.
- Removing or renaming an export, tightening a signature, dropping a supported runtime or platform, raising a dependency floor: `1`.
- Adding something optional, or fixing a call that used to raise or crash so that it now succeeds: `2`. Nothing that used to work changed.
- If the description says the output, results or behavior are **unchanged / identical / equivalent**, or the only effect is that something is faster or uses less memory: `3`, never `2`. `2` means a caller can see something new; `3` means they cannot see anything.

### When two codes both genuinely fit

Only if a change truly satisfies two definitions at once, take the one that comes first: `A` before
`B` before `C`, and `1` before `2` before `3`. This tiebreak is for real overlap. If the change fits
exactly one definition on an axis, apply that definition — do not fall back to precedence to avoid
choosing.

## The `Impact:` line

It is the **lowest digit that appears on any bullet in the entry** — `1` if any bullet is breaking,
otherwise `2` if any bullet is compatible, otherwise `3`. Compute it after you have finalized every
code, and recompute it if you revise one.

## Bullet order

Sort bullets by their code, ascending — all `A` before all `B` before all `C`, and within a letter
`1` before `2` before `3`. So: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Bullets sharing
a code keep the relative order they were given in. Never emit them in the order the changes happened
to arrive.

## Worked example

For version `2.3.0` released on `2025-11-04`:

```
## [2.3.0] - 2025-11-04

Impact: 1

- [A1] `open_store()` no longer accepts the `retries` argument.
- [A2] `Store` gained an optional `timeout` parameter; omitting it keeps the previous behavior.
- [B1] `resolve()` now returns absolute paths, changing the result for relative inputs.
- [B2] Fixed `count()` raising instead of returning `0` for an empty store.
- [B3] Replaced the internal index with a hash map. Results are unchanged.
- [C3] Moved the test suite to a new runner.

<!-- stl-impact: v1 -->
```

Note the pairs that are easy to confuse: `A1` changes a signature, `B1` changes a result behind an
unchanged signature; `B2` repairs a path that was already broken, `B3` leaves every result identical;
`B3` is internal library code, `C3` is code that never ships to a caller.

## Before you submit

- [ ] Heading starts with `## `, version in brackets, ` - `, date as `YYYY-MM-DD`.
- [ ] Every bullet has a letter-and-digit code in square brackets.
- [ ] Every bullet describing a changed result for previously-working input is a `1`.
- [ ] Every bullet saying output is unchanged, or that only cites speed or memory, is a `3`.
- [ ] Internal library rewrites are `B`, not `C`.
- [ ] `Impact:` equals the lowest digit present.
- [ ] Bullets sorted ascending by code.
- [ ] Last line is exactly `<!-- stl-impact: v1 -->`, comment markers included, nothing after it.