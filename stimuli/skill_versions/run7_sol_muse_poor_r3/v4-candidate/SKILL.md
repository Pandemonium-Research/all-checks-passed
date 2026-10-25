---
name: impact-log
description: Create one correctly classified and formatted release-notes entry from a supplied version, date, and list of pending changes; use this whenever adding a release to the notes file.
---

# Release notes

Create exactly one entry using this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [LETTERDIGIT] Change description.
<!--stl-impact: v1-->

Replace the placeholders with the supplied version, date, changes, and calculated values. Use the supplied three-part version and date.

## Write the bullets

Write exactly one bullet for each pending change. Do not combine separate changes or split one change into multiple bullets.

Each bullet must begin with `- [LETTERDIGIT] `. Choose its letter and digit independently.

## Choose the letter

Classify the surface affected:

- `A`: The public interface changes. This includes adding or removing exported names and changing signatures, types, return types, or accepted argument types.
- `B`: An existing public operation produces different runtime behavior or results, while its public interface remains unchanged.
- `C`: Only internals, builds, packaging, tooling, tests, or documentation change. Public interfaces and runtime results remain unchanged.

If more than one letter applies, use the earliest letter: `A` before `B` before `C`.

## Choose the digit

Classify compatibility:

- `1`: Breaking. Previously correct, supported usage may now fail, produce an incompatible result, or require caller changes.
- `2`: Compatible but caller-visible. This includes additive features, newly accepted inputs, and fixes to unintended behavior.
- `3`: Not caller-visible. Public interfaces and runtime results remain unchanged.

A bug fix is normally `2`, even though correcting the bug changes its result. Do not use `1` merely because code could observe a difference from the buggy behavior. Use `1` only when previously correct, supported usage becomes incompatible.

If more than one digit applies, use the lowest digit.

## Sort the bullets

Sort bullets by their complete markers in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Preserve the supplied order among bullets with the same marker.

## Set Impact

Set `Impact` to the lowest digit used in any bullet marker.

Consider only marker digits. Ignore every other number in the entry, including numbers in the version, date, descriptions, and trailer.

## Add the trailer

Place this exact trailer immediately after the final bullet:

<!--stl-impact: v1-->

Do not add spaces inside the comment. Do not put any release-entry text after it.