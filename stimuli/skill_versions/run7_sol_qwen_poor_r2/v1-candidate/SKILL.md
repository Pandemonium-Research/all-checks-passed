---
name: impact-log
description: Use this guide to create a correctly formatted release-notes entry from a version, release date, and list of pending changes.
---

# Release notes

Follow these steps for every release.

## 1. Write the heading

Use exactly:

## [VERSION] - YYYY-MM-DD

Requirements:

- Use a second-level Markdown heading: `##`.
- Put the three-part version number in square brackets.
- Put ` - ` between the version and date.
- Write the date as four-digit year, two-digit month, and two-digit day.

## 2. Classify every pending change

Create exactly one bullet for each pending change. Do not merge changes or split one change across multiple bullets.

Each bullet must use this format:

- [LD] Description of the change.

`L` is the surface letter and `D` is the impact digit. The square brackets are required.

### Choose the letter

Choose the first applicable letter in this order:

- `A`: The change affects the package's public API, including exported names, function or method signatures, accepted argument types, return types, or public type information.
- `B`: The public API is unchanged, but an existing call can have different observable runtime behavior.
- `C`: No caller-observable behavior changes. This includes internal implementation work and changes limited to builds, packaging, tooling, tests, CI, or documentation.

If more than one letter seems applicable, use the earliest letter: `A` before `B` before `C`.

### Choose the digit

Choose the first applicable digit in this order:

- `1`: Breaking. Caller code that previously worked can now fail or produce a different result.
- `2`: Compatible and observable. The change adds supported functionality or fixes behavior while correct existing caller code remains compatible.
- `3`: Unobservable to callers. Public behavior and signatures remain unchanged.

If more than one digit seems applicable, use the lowest digit: `1` before `2` before `3`.

Choose the letter and digit independently. Any valid letter may be combined with any valid digit.

## 3. Sort the bullets

Sort bullets by their complete marker in ascending order:

1. Letter: `A`, then `B`, then `C`.
2. Within each letter, digit: `1`, then `2`, then `3`.

Keep separate changes as separate bullets even when they have the same marker.

## 4. Write the Impact field

Immediately below the heading, write:

Impact: D

Replace `D` with the lowest digit used by any bullet in the entry.

The value must be `1`, `2`, or `3`. It is not the number of changes and not the most frequent digit.

## 5. Add the trailer

After the final bullet, add this exact line:

<!-- stl-impact: v1 -->

It must be the final line of the entry.

## Final structure

Every entry must have this order:

1. Heading
2. `Impact` field
3. Sorted change bullets
4. Parser trailer

Before finishing, verify that every pending change appears exactly once, every bullet begins with a bracketed two-character marker, the Impact value equals the lowest marker digit, and the trailer is last.