---
name: impact-log
description: Classify and format one release-notes entry from a supplied version, date, and list of pending changes; use this whenever adding a release to the notes file.
---

# Release notes

Create exactly one entry in this form:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [MARKER] Change description.
<!--stl-impact: v1-->

Replace the placeholders with the supplied information. Use the supplied three-part numeric version and date.

## Write the bullets

Write exactly one bullet for each pending change:

- Do not merge separate changes.
- Do not split one change into multiple bullets.
- Start each bullet with `- [LETTERDIGIT] `.
- Describe the change after the marker.

Choose the marker’s letter and digit independently.

## Choose the letter

Choose the surface affected:

- `A`: The public interface changes. This includes adding or removing exported names, changing signatures or return types, and accepting new argument types.
- `B`: An existing public operation produces different runtime behavior, but its public interface is unchanged.
- `C`: Only internals, builds, packaging, tooling, tests, or documentation change; public interfaces and runtime behavior remain unchanged.

If multiple letters apply to one change, choose the earliest alphabetically: `A` before `B` before `C`.

## Choose the digit

Choose the compatibility impact:

- `1`: Breaking. Previously correct, supported usage may now fail, produce an incompatible result, or require caller changes.
- `2`: Compatible but caller-visible. This includes additive features, newly accepted inputs, and corrections to unintended behavior.
- `3`: Not caller-visible. Public interfaces and results are unchanged.

A bug fix is normally `2`, even when it changes the result. Do not mark a bug fix as `1` merely because code relying on the buggy result could observe a difference. Use `1` only when previously correct, supported usage becomes incompatible.

If multiple digits apply to one change, choose the lowest digit.

## Sort the bullets

Sort bullets by their complete markers in this order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Preserve the supplied order among bullets with the same marker.

## Set Impact

Set `Impact` to the lowest digit used in any bullet marker.

Consider only marker digits. Ignore every other number in the entry, including numbers in the version, date, and descriptions.

For marker digits `2`, `2`, and `3`, write:

Impact: 2

## Add the trailer

Place this exact trailer immediately after the final bullet:

<!--stl-impact: v1-->

Do not add spaces inside the comment. Do not place any release-entry text after it.