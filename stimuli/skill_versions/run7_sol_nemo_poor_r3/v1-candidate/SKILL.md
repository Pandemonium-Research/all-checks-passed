---
name: impact-log
description: Use this document to turn a release version, date, and list of pending changes into a correctly formatted, classified, and sorted release-notes entry.
---

# Release notes

Create exactly one release entry using the format and rules below.

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT

- [LETTERDIGIT] Description of one pending change.
- [LETTERDIGIT] Description of another pending change.

<!-- stl-impact: v1 -->
```

Replace the placeholders as follows:

- `VERSION`: the supplied three-part version, such as `1.4.0`. Do not add a `v`.
- `YYYY-MM-DD`: the supplied date in year-month-day format.
- `LOWEST_DIGIT`: the lowest digit used in any change marker.
- `LETTERDIGIT`: the change's letter followed immediately by its digit.

The release heading must begin with exactly two `#` characters. Write the summary exactly as `Impact: N`.

## Write one bullet per change

Represent every pending change with exactly one bullet. Do not combine changes or split one change across multiple bullets.

Every bullet must begin with a hyphen, a space, and a square-bracketed marker:

```text
- [A2] Description.
```

Do not omit the brackets, put the marker after the description, or write the marker with a colon.

## Choose the marker letter

Choose the letter according to the surface affected:

- `A` — Public API surface: exported names, import paths, signatures, parameters, return types, public annotations, or shipped typing information.
- `B` — Runtime behavior of calls without a public API-surface change.
- `C` — Build, packaging, dependencies, tooling, tests, documentation, performance-only work, or internal implementation details.

If more than one letter applies, use the earliest letter: `A` before `B` before `C`.

## Choose the marker digit

Choose the digit independently of the letter:

- `1` — Breaking: supported caller code can fail, become invalid, or produce a different result.
- `2` — Compatible: the change is additive or fixes behavior while supported existing code remains valid.
- `3` — Unobservable to callers: public behavior and public API are unchanged.

A genuine bug correction may use `2` when it restores intended behavior without breaking supported usage. Use `1` when supported callers can observe an incompatible result, even if the change is described as a fix.

If more than one digit could apply, use the lowest digit: `1` before `2` before `3`. When uncertain, choose the more disruptive classification.

## Calculate Impact

Set `Impact` to the lowest digit among the change markers, not the number of changes and not the most common digit.

Only marker digits count. Ignore numbers appearing in the version, date, or change descriptions.

For example, markers `A2`, `B1`, and `C3` produce `Impact: 1`.

## Sort the bullets

Sort bullets by their complete markers in this order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Keep supplied order between changes with the same marker.

## Add the trailer

After the final bullet, add this exact HTML comment as the final line:

```text
<!-- stl-impact: v1 -->
```

Do not add any content after the trailer.

## Final check

Before submitting, verify that:

- The heading is exactly `## [VERSION] - YYYY-MM-DD`.
- The summary is exactly `Impact: N`.
- Every pending change appears once.
- Every bullet begins with a bracketed marker such as `[B2]`.
- The bullets are sorted by marker.
- `Impact` is the lowest marker digit.
- The trailer is present and is the final line.