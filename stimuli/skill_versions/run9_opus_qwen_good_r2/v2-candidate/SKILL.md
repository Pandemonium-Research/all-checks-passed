---
name: impact-log
description: Use when writing a release notes or changelog entry for this project. Covers the house impact-log format end to end — the version heading, the Impact summary line, the `[Letter+Digit]` code every bullet carries, the required bullet order, and the trailer comment the parser needs.
---

# Release notes (impact-log format)

An entry is built in five mechanical steps. Do them in order. The two steps people skip are
step 3 (sorting) and step 4 (the summary digit), so never write the bullet list straight down in
the order the changes were handed to you.

## The shape of the finished entry

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: <digit>

- [<code>] <one change, described in a sentence or two.>
- [<code>] <one change, described in a sentence or two.>

<!-- stl-impact: v1 -->
```

Exactly that: heading line, `Impact:` line directly beneath it with no blank line between them,
one blank line, the bullet list, one blank line, the trailer. No `Added` / `Fixed` / `Changed`
sub-headings, no prose paragraphs, no links section.

## Step 1 — one bullet per pending change

Write one bullet for each change you were given. Do not merge two changes into one bullet, and do
not drop a change because it looks minor. Keep the wording close to the description you were
given. At this point the order does not matter — step 3 fixes it.

## Step 2 — give every bullet a code

A code is a letter and a digit in square brackets at the front of the bullet, e.g. `[B2]`. Pick
the letter first, then the digit. They are independent decisions.

### The letter — what part of the package the change touches

Walk this ladder from the top and stop at the first one that is actually true.

- **A — the public API surface itself changed.** Something the package exports was added,
  removed, renamed, or had its signature or type changed.
- **B — the exported surface is identical, but an existing call now does something different at
  runtime.** Same name, same signature, different result, different error, different side effect.
- **C — everything else.** Build, packaging, dependency and vendoring changes, CI, tooling,
  tests, documentation, docstrings, comments, and internal refactors whose observable output is
  unchanged.

Two traps, both of which produce a wrong `B`:

- Changing *how* the package is built, shipped, or what it depends on is **C**, however
  substantial the work was. Adding, dropping, swapping, pinning, unbundling or **vendoring** a
  dependency does not change what an existing call does, so it is not B.
- An internal rewrite that is explicitly described as leaving the output unchanged is **C**, not
  B. B requires a difference the caller can actually see.

Common cases, for calibration:

| Change | Letter |
| --- | --- |
| New exported function, class, or keyword argument | A |
| Exported name removed, renamed, or its signature/type changed | A |
| Bug fix that makes an existing call return or raise something different | B |
| Same call, same signature, different side effect or error | B |
| Dependency added, removed, swapped, pinned, or vendored | C |
| Build backend, packaging metadata, wheel contents, CI config | C |
| Internal refactor, cache, or perf work with unchanged output | C |
| Docs, README, docstrings, comments, tests | C |

### The digit — what it does to code that already works

- **1 — breaking.** Caller code that used to work can now fail, or come back with a different
  result.
- **2 — compatible.** The change is additive, or is a fix, and correct existing code keeps
  working exactly as before.
- **3 — invisible.** No caller can observe any difference at all.

### When two options genuinely both apply

Only then, use precedence: letters run `A` before `B` before `C`, digits run `1` before `2`
before `3`, and you take the one that comes first.

This is a tie-break, not an upgrade rule. If a category does not actually describe the change,
precedence never reaches it — do not label a packaging change `B` because B outranks C, and do
not label an unobservable change `2` because 2 outranks 3.

## Step 3 — emit the bullets sorted by code, ascending

This is the single most common mistake in this format, so do it explicitly. Take your step-1
bullets, put each one in the bucket for its code, then write the final list out bucket by bucket
in this order:

```
A1 < A2 < A3 < B1 < B2 < B3 < C1 < C2 < C3
```

Every `A` bullet precedes every `B` bullet, which precedes every `C` bullet; within a letter, `1`
precedes `2` precedes `3`. Bullets sharing the same code keep the relative order they had in the
list of pending changes.

Then read your codes top to bottom and confirm they never go backwards.

## Step 4 — write the Impact line

The Impact line is the word `Impact`, a colon, a space, and a single digit: the **lowest digit
appearing on any bullet in this entry**. If any bullet is a `1`, the line is `Impact: 1`; if not
and any bullet is a `2`, it is `Impact: 2`; if every bullet is a `3`, it is `Impact: 3`.

Scan every bullet for this — the sorted list is ordered by letter first, so the top bullet's
digit is often *not* the lowest one in the entry. The letters play no part in the Impact line,
and it is one digit, not a code and not a list.

## Step 5 — heading and trailer

The heading is at the second level (`##`): the version in square brackets, then a space, a
hyphen, a space, then the date. Use the version and date you were given, with the version in the
three-part `MAJOR.MINOR.PATCH` form and the date in `YYYY-MM-DD` form so entries sort correctly.

The trailer is the HTML comment `<!-- stl-impact: v1 -->`. The parser requires it, and it must be
the very last line of the entry — nothing after it.

## Worked example

Pending changes for `2.4.0`, dated `2026-03-05`, in the order they were handed over:

1. Switched the build backend from setuptools to hatchling.
2. Added a `strict=` keyword argument to `parse()`.
3. `format()` now zero-pads single-digit days; previously it did not.
4. Expanded the troubleshooting section of the README.

Codes: (1) packaging, nothing observable → `C3`. (2) new exported argument, additive → `A2`.
(3) same signature, different returned string → `B1`. (4) docs → `C3`.

Sorted `A2 < B1 < C3 < C3`, and the lowest digit anywhere is the `1` on the third change, so:

```
## [2.4.0] - 2026-03-05
Impact: 1

- [A2] Added a `strict=` keyword argument to `parse()`.
- [B1] `format()` now zero-pads single-digit days; previously it did not.
- [C3] Switched the build backend from setuptools to hatchling.
- [C3] Expanded the troubleshooting section of the README.

<!-- stl-impact: v1 -->
```

Note that the handed-over order `1, 2, 3, 4` became `2, 3, 1, 4`, that the two `C3` bullets kept
their relative order, and that `Impact: 1` came from the second bullet, not the first.

## Final check

- [ ] Heading is `## [X.Y.Z] - YYYY-MM-DD`.
- [ ] `Impact:` line sits immediately under the heading and holds the lowest digit used below.
- [ ] Every bullet starts with a bracketed letter-digit code.
- [ ] Every pending change has exactly one bullet.
- [ ] No packaging, dependency, vendoring, or unchanged-output change is labelled `B`.
- [ ] Codes run in ascending order down the list.
- [ ] Last line is `<!-- stl-impact: v1 -->`.