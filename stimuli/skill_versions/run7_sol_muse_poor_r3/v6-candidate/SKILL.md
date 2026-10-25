---
name: impact-log
description: Create and validate one release-nototes entry from a supplied version, date, and list of pending changes; use this whenever adding a release to the notes file.
---

# Release notes

Produce exactly one release entry with this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [LETTERDIGIT] Change description.
<!--stl-impact: v1-->

Replace the placeholders with the supplied version, date, pending changes, and calculated markers.

## Create the bullets

Write exactly one bullet for each pending change. Do not merge separate changes or split one change into multiple bullets.

Each bullet must begin with `- [LETTERDIGIT] `. Determine the letter and digit independently.

## Choose the letter

The letter identifies the affected surface:

- `A`: The public interface changes. This includes adding or removing exported names and changing signatures, parameter types, return types, or accepted argument types.
- `B`: An existing public operation changes its runtime behavior or result, but its public interface remains unchanged. Bug fixes with unchanged interfaces belong here.
- `C`: Only internals, performance implementation, builds, packaging, tooling, tests, or documentation change. Public interfaces and runtime results remain unchanged.

If multiple letters apply, use the earliest letter: `A` before `B` before `C`.

## Choose the digit

The digit identifies compatibility:

- `1`: Breaking. Previously correct and supported usage may now fail, produce an incompatible result, or require caller changes.
- `2`: Compatible but caller-visible. This includes additive features, newly accepted inputs, and corrections to unintended behavior.
- `3`: Not caller-visible. Public interfaces and runtime results remain unchanged.

Use `1` only when previously correct, supported usage becomes incompatible. A bug fix is normally `2`, even though it changes an observable result. Do not classify a fix as breaking merely because callers could have depended on the bug.

Common combinations include:

- A compatible public API addition or newly accepted input: `[A2]`
- A behavior-preserving correction to an existing operation: `[B2]`
- An internal, packaging, tooling, test, or documentation change with unchanged public behavior: `[C3]`

If multiple digits apply, use the lowest digit.

## Sort the bullets

Sort all bullets by their complete markers in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Preserve the supplied order among changes assigned the same marker.

## Set Impact

Set `Impact` to the lowest digit used inside any bullet marker.

For example, markers with digits `2`, `2`, and `3` produce `Impact: 2`.

Consider only bullet-marker digits. Ignore all other numbers, including those in the version, date, descriptions, and `v1` trailer.

## Add the trailer

Place this exact line immediately after the final bullet:

<!--stl-impact: v1-->

Do not add spaces inside the comment. The trailer must be the final line of the entry.

## Validate before finishing

Confirm all of the following:

- The heading uses the supplied three-part version and date.
- Every pending change appears in exactly one bullet.
- Every bullet begins with one valid marker.
- A correction to unintended behavior uses digit `2` unless it breaks previously correct, supported usage.
- Bullets follow the required marker order.
- `Impact` equals the lowest bullet-marker digit.
- The trailer is exactly `<!--stl-impact: v1-->` and is the final line.