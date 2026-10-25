---
name: impact-log
description: Use this guide when converting a release version, date, and pending changes into a correctly formatted release-notes entry with impact markers, summary, ordering, and parser trailer.
---

# Release notes

Create one release entry using the exact structure and classification rules below.

## Required structure

Write the entry in this order:

1. A second-level heading: `## [VERSION] - YYYY-MM-DD`
2. A blank line.
3. The summary: `Impact: DIGIT`
4. A blank line.
5. One list item per pending change: `- [LETTERDIGIT] Description`
6. A blank line.
7. The trailer: `<!-- stl-impact: v1 -->`

Use the supplied three-part version and ISO date exactly. Do not add introductory or closing text. Do not put a colon after an impact marker.

## Classify each change

Each marker contains one letter and one digit, such as `[B2]`. Choose the letter and digit independently.

### Choose the letter

Use the first applicable category:

- `A` — The public interface or supported compatibility surface changes. This includes exported names, parameters, signatures, accepted or returned types, and supported runtime versions.
- `B` — The public interface is unchanged, but callers can observe different functional behavior, results, or errors.
- `C` — Neither the public interface nor functional behavior changes. This includes internal implementation, performance-only work, tests, documentation, tooling, and packaging changes that preserve installation behavior.

If multiple letters apply, use the earliest letter: `A` before `B` before `C`.

A compatible addition to the public interface is `A`, not `B`. A bug fix that changes runtime results without changing the interface is `B`, not `A`. An internal optimization with unchanged results and interface is `C`, not `B`.

### Choose the digit

- `1` — Breaking: supported caller code may fail, produce incompatible results, or require modification after upgrading.
- `2` — Compatible and caller-visible: functionality is added, accepted inputs are broadened, or a defect is fixed without breaking correct existing code.
- `3` — Caller-invisible: there is no change to the public contract or functional results.

If multiple digits apply, use the lowest digit: `1` before `2` before `3`.

A defect fix may change the result that exposed the defect and still be digit `2`; reserve digit `1` for a backward-incompatible change to supported behavior.

## Write and order the list

Represent every pending change exactly once. Do not combine separate changes or split one change into multiple items.

Begin every item with a square-bracketed marker in the exact form `[A1]` through `[C3]`, followed by one space and a concise description.

Sort items by letter first and digit second:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Keep the supplied order for items with the same marker.

## Calculate the summary

Set `Impact` to the lowest digit used in the list-item markers.

Consider only marker digits. Ignore every other numeral, including numerals in the version, date, descriptions, and `stl-impact: v1` trailer.

For example, if the markers contain digits `2`, `3`, and `1`, write `Impact: 1`.

## Final check

Before finishing, verify that:

- The heading has the supplied version and date in the required format.
- Every pending change appears once.
- Every list item starts with a valid square-bracketed marker.
- The items are sorted by marker.
- `Impact` is the lowest marker digit.
- The trailer is the final line.