---
name: impact-log
description: Format and classify a release-nototes entry from a supplied version, date, and list of pending changes; use this whenever adding a release to the notes file.
---

# Release notes

Create exactly one release entry with this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [MARKER] Change description.
<!--stl-impact: v1-->

Replace the placeholders with the supplied version, date, changes, markers, and impact digit. Use the supplied three-part numeric version and the supplied date in `YYYY-MM-DD` form.

## Write one bullet per change

For every pending change:

1. Write exactly one bullet.
2. Do not combine separate changes or split one change into multiple bullets.
3. Start the bullet with `- [LETTERDIGIT] `.
4. Describe the change after the marker.

Choose the marker's letter and digit independently.

## Choose the letter

Classify the surface affected:

- `A`: The public interface changes. This includes adding or removing exported names, changing signatures or return types, or changing accepted argument types.
- `B`: An existing public operation's runtime behavior or result changes while its public interface remains unchanged.
- `C`: Only internals, performance implementation, builds, packaging, tooling, tests, or documentation change. Public interfaces and runtime results remain unchanged.

When more than one letter applies, choose the earliest letter: `A` before `B` before `C`.

## Choose the digit

Classify compatibility:

- `1`: Breaking. The change makes previously correct, documented, or otherwise supported usage incompatible or requires callers to change.
- `2`: Compatible but caller-visible. This includes new features, newly accepted inputs, and fixes that correct unintended behavior without breaking supported usage.
- `3`: Not caller-visible. Public interfaces and runtime results remain unchanged.

Do not classify a defect correction as breaking merely because its corrected result differs from the buggy result. A bug fix is `2` unless the change explicitly removes or changes behavior that was previously supported. Use `1` only when supported usage becomes incompatible; do not infer that impact solely from any change in output.

When multiple digits apply, choose the lowest digit.

## Sort the bullets

Sort all bullets by their complete markers in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Preserve the supplied order among changes with the same marker.

## Set Impact

Set `Impact` to the lowest digit appearing in the bullet markers.

Consider only the digit in each marker. Ignore all other numbers, including those in the version, date, descriptions, and trailer.

For example, markers with digits `2`, `2`, and `3` produce:

Impact: 2

## Add the trailer

Place this exact trailer immediately after the final bullet:

<!--stl-impact: v1-->

Do not add spaces inside the comment. Do not put any release-entry text after it.