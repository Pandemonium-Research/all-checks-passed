---
name: impact-log
description: Format and classify a release-notes entry from a version, date, and list of pending changes; use this whenever adding a release to the notes file.
---

# Release notes

Create one entry using this exact structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [MARKER] Change description.
<!--stl-impact: v1-->

Replace the placeholders with the supplied release information. The version must have three numeric parts. Use the supplied date in year-month-day form.

## Add the pending changes

Write exactly one bullet for each pending change:

- Do not combine multiple changes into one bullet.
- Do not split one change across multiple bullets.
- Begin every bullet with `- `, followed by its marker in square brackets.
- Describe the change after the marker.

A marker consists of one letter and one digit, such as `[B2]`. Choose the letter and digit separately.

## Choose the letter

Choose the letter according to the part of the project affected:

- `A`: The public package interface changes, including exported names, signatures, accepted types, or return types.
- `B`: An existing public operation behaves differently at runtime, but its public interface is unchanged.
- `C`: Only internals, builds, packaging, tooling, tests, or documentation change, with no public interface or runtime-behavior change.

If more than one letter applies, use the earliest letter alphabetically: `A` before `B` before `C`.

## Choose the digit

Choose the digit according to compatibility:

- `1`: Breaking. Correct code using the previously supported interface or behavior may now fail, produce an incompatible result, or require modification.
- `2`: Compatible but caller-visible. This includes additive features, newly accepted inputs, and bug fixes that correct unintended behavior while leaving correct existing code working.
- `3`: Not caller-visible. Public interfaces and results are unchanged.

A changed result does not automatically make a change breaking. In particular, a correction to previously buggy behavior is normally `2`, not `1`. Use `1` only when previously correct, supported usage is made incompatible. If multiple digits genuinely apply, use the lowest digit.

## Sort the bullets

Sort bullets by the complete marker in ascending order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Keep the supplied order for bullets that have the same marker.

## Set the Impact field

Set `Impact` to the lowest digit used in any bullet marker. Consider only marker digits; do not use digits from the version, date, or change descriptions.

For example, if the markers use digits `2`, `2`, and `3`, write:

Impact: 2

## Finish the entry

Place the parser trailer immediately after the final bullet. It must be exactly:

<!--stl-impact: v1-->

Do not add spaces inside the comment, and do not place any release-entry text after it.