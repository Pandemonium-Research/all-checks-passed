---
name: impact-log
description: Use this document to turn a release version, date, and pending-change list into a correctly classified, ordered, parser-compatible release notes entry.
---

# Release notes

Create exactly one entry in this structure, replacing each uppercase placeholder:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Concise change summary.
- [CODE] Concise change summary.

<!-- stl-impact: v1 -->

Formatting requirements:

- Write `VERSION` as three numeric parts, such as `1.4.0`, without backticks.
- Write the zero-padded date in `YYYY-MM-DD` form.
- Preserve the blank lines shown above.
- Include every pending change exactly once.
- End with exactly `<!-- stl-impact: v1 -->`. Nothing may follow it.

## Assign each code

Classify every change independently. A code contains a letter describing the affected area and a digit describing its impact. Determine the letter and digit separately.

### Letter

Use the first applicable letter:

1. `A` — The public API surface changes. This includes:
   - adding, removing, or renaming an exported name;
   - changing a public signature;
   - changing accepted argument types or return types;
   - allowing an additional type in an existing public API.

2. `B` — The public API surface stays the same, but an existing public call produces observably different runtime behavior. Compatible bug fixes normally use `B`.

3. `C` — Neither the public API surface nor an existing call's runtime behavior changes. This includes internal implementation work, build and packaging changes, distribution artifacts, tooling, tests, and documentation.

If several letters appear applicable, use the precedence `A`, then `B`, then `C`.

### Digit

Use the first applicable digit:

1. `1` — Breaking: previously valid caller code can fail or encounter an incompatible result. Do not use `1` merely because a compatible bug fix changes an incorrect result.

2. `2` — Compatible and externally observable. This includes:
   - adding a public API;
   - widening the types accepted by a public API;
   - correcting behavior without breaking valid callers;
   - adding a supported installation target or distributable artifact.

3. `3` — Not observable by callers. This includes unchanged-result optimizations, internal refactoring, test or documentation changes, and packaging migrations that leave installation behavior unchanged.

If several digits appear applicable, use the precedence `1`, then `2`, then `3`.

The letter does not determine the digit. Common combinations include:

- Additive or widened public API: `A2`
- Compatible runtime bug fix with an unchanged API: `B2`
- New distribution artifact: `C2`
- Internal optimization with unchanged results: `C3`

## Order and summarize

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes have the same code, preserve their order from the pending-change list.

Describe only the supplied change. Keep the summary concise, format identifiers with backticks where appropriate, and do not invent compatibility claims.

Set `Impact` to the lowest digit present among all bullet codes, regardless of their letters.

Before finishing, verify that every pending change appears once, every code follows the rules above, the bullets are sorted, the `Impact` digit is correct, the blank lines are present, and the trailer is the final line.