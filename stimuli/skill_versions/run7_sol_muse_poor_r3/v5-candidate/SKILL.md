---
name: impact-log
description: Create and validate one release-notes entry from a supplied version, date, and list of pending changes; use this when adding any release to the notes file.
---

# Release notes

Create exactly one release entry in this form:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [LETTERDIGIT] Change description.
<!--stl-impact: v1-->

Use the supplied three-part version and date exactly. Write the date in `YYYY-MM-DD` format.

## Write one bullet per change

For every pending change:

1. Write exactly one bullet. Do not merge changes or split one change across bullets.
2. Begin the bullet with `- [LETTERDIGIT] `.
3. Describe the change after the marker.
4. Choose the marker’s letter and digit independently using the rules below.

## Choose the letter

The letter identifies the affected surface:

- `A`: The public interface changes. Use this for added or removed exported names, changed signatures or return types, and changes to accepted argument types.
- `B`: An existing public operation’s runtime behavior or result changes, but its public interface does not.
- `C`: Only internals, performance implementation, builds, packaging, tooling, tests, or documentation change. Public interfaces and runtime results remain unchanged.

If more than one letter applies, choose the earliest: `A` before `B` before `C`.

## Choose the digit

The digit identifies compatibility:

- `1`: Breaking. Previously correct, documented, or otherwise supported usage becomes incompatible or requires caller changes.
- `2`: Compatible but caller-visible. Use this for additive features, newly accepted inputs, and corrections to unintended behavior.
- `3`: Not caller-visible. Public interfaces and runtime results remain unchanged.

A defect correction is normally `2`, even when callers can observe that the incorrect result has changed. Do not mark a fix as `1` merely because code could have depended on the bug. Use `1` only when the change breaks behavior that was previously correct and supported.

If more than one digit applies, choose the lowest digit.

## Sort the bullets

Sort all bullets by their complete markers in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Preserve the supplied order among changes that receive the same marker.

## Set Impact

Set `Impact` to the lowest digit appearing in a bullet marker.

Use only the digits inside bullet markers. Ignore every other number, including numbers in the version, date, descriptions, and trailer.

## Add the trailer

Place this exact trailer immediately after the final bullet:

<!--stl-impact: v1-->

Do not add spaces inside the comment. Do not place any release-entry text after it.

## Validate the entry

Before finishing, confirm that:

- The heading contains the supplied version and date.
- Every pending change appears in exactly one bullet.
- Every bullet has one valid marker.
- Bug fixes are `2` unless they break previously supported behavior.
- Bullets follow the required marker order.
- `Impact` is the lowest bullet-marker digit.
- The trailer matches exactly and is the final line.