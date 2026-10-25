---
name: impact-log
description: Use when writing a release notes or changelog entry for this project. Covers the house impact-log format end to end — the version heading, the Impact summary line, the `[Letter+Digit]` code that every bullet carries, the order the bullets must be in, and the trailer comment the parser requires.
---

# Release notes (impact-log format)

A release entry is built in five mechanical steps. Do them in order. Step 3 (sorting) and step 4
(the summary number) are the two people most often skip — do not write the bullets down in the
order the changes were handed to you.

## The shape of the finished entry

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: <digit>

- [<code>] <one change, described in a sentence or two.>
- [<code>] <one change, described in a sentence or two.>

<!-- stl-impact: v1 -->
```

Exactly that: heading line, Impact line directly beneath it with no blank line between them, one
blank line, the bullet list, one blank line, the trailer. No `Added` / `Fixed` / `Changed`
sub-headings, no prose paragraphs, no links section.

## Step 1 — write one bullet per change

One bullet per pending change, in the order you were given them for now (step 3 reorders them).
Do not merge two changes into one bullet and do not drop a change because it looks minor.
Keep the wording close to the change description you were given.

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

Two traps worth naming:

- Changing *how* the package is built, shipped, or what it depends on is **C**, even when the
  work was substantial. Swapping, vendoring, dropping, or pinning a dependency does not change
  what an existing call does, so it is not B.
- An internal rewrite that is explicitly described as producing the same output is **C**, not B.
  B requires an observable difference for the caller.

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

## Step 3 — sort the bullets by code, ascending

Reorder the whole bullet list by its codes. This is required, and it is the single most common
mistake in this format. Sort on the letter first, then on the digit:

```
A1 < A2 < A3 < B1 < B2 < B3 < C1 < C2 < C3
```

So every `A` bullet precedes every `B` bullet, which precedes every `C` bullet; within a letter,
`1` precedes `2` precedes `3`. Bullets that share the same code keep the relative order they had
in the list of pending changes.

Before moving on, read your codes top to bottom and confirm they never go backwards.

## Step 4 — write the Impact line

The Impact line is the word `Impact`, a colon, a space, and a single digit: the **lowest digit
appearing on any bullet in this entry**. If any bullet is a `1`, the line is `Impact: 1`; if not
and any bullet is a `2`, it is `Impact: 2`; if every bullet is a `3`, it is `Impact: 3`.

It is derived only from the digits — the letters play no part in it — and it is one number, not
a code and not a list.

## Step 5 — heading and trailer

The heading is at the second level (`##`): the version in square brackets, then a space, a
hyphen, a space, then the date. Use the version and date you were given, with the version in the
three-part `MAJOR.MINOR.PATCH` form and the date in `YYYY-MM-DD` form so entries sort correctly.

The trailer is the HTML comment `<!-- stl-impact: v1 -->`. The parser requires it, and it must be
the very last line of the entry — nothing after it.

## Final check

- [ ] Heading is `## [X.Y.Z] - YYYY-MM-DD`.
- [ ] `Impact:` line sits immediately under the heading and holds the lowest digit used below.
- [ ] Every bullet starts with a bracketed letter-digit code.
- [ ] Every pending change has exactly one bullet.
- [ ] Codes run in ascending order down the list.
- [ ] Last line is `<!-- stl-impact: v1 -->`.