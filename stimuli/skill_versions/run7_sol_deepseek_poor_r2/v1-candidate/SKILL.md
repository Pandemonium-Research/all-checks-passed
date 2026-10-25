---
name: impact-log
description: Use this document when converting a release version, date, and list of pending changes into a correctly classified, ordered, parser-compatible release notes entry.
---

# Release notes

Write each release entry in this exact order:

1. Release heading
2. Impact field
3. One bullet for each pending change
4. Parser trailer

Use this structure:

## [VERSION] - YYYY-MM-DD

Impact: LOWEST_MARKER_DIGIT

- [A1] Change description.
- [B2] Change description.
- [C3] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders with release-specific values. Do not copy classifications from another release.

## Classify each change

Every pending change must have exactly one two-character impact marker in square brackets:

- The first character is `A`, `B`, or `C`.
- The second character is `1`, `2`, or `3`.
- Write the marker immediately after the bullet prefix, followed by the change description: `- [A1] Description.`
- Do not add a colon after the marker.

Choose the letter and digit independently.

### Choose the letter

Use the first applicable category:

- `A` — Public API surface: exported names, function or method signatures, accepted argument types, return types, or other caller-visible interfaces.
- `B` — Runtime implementation or behavior when the public API surface is unchanged. This includes runtime fixes, algorithm changes, performance work, and internal caching, even when the change does not alter results.
- `C` — Non-runtime project work only, such as build configuration, packaging infrastructure, development tooling, tests, or documentation.

For a change spanning multiple categories, use the alphabetically earliest applicable letter: `A` before `B` before `C`.

Do not invent other letters.

### Choose the digit

Use the first applicable category:

- `1` — Breaking: previously working caller code can now fail, become invalid, or produce a different result.
- `2` — Compatible: the change is additive or fixes incorrect behavior while correct existing code remains unaffected.
- `3` — Unobservable to callers: no caller can observe a functional difference.

A bug fix may change the result for the buggy case and still be `2` when it restores the intended behavior without breaking correct existing use. Internal runtime work whose results and public interface are unchanged is `3`.

If more than one digit seems plausible, choose the lowest number. The lower number represents the more disruptive classification.

## Write the entry

Use a second-level Markdown heading in exactly this form:

`## [VERSION] - YYYY-MM-DD`

Use a three-part version number and an ISO date. Do not copy formatting from older, inconsistent entries.

On the next field line, write:

`Impact: N`

Set `N` to the lowest digit used in the bullet markers. Inspect only the marker digits. Ignore all digits in the version, date, descriptions, and parser trailer. For example, markers `[A2]`, `[B1]`, and `[C3]` produce `Impact: 1`.

Create exactly one bullet for each pending change:

- Do not merge multiple pending changes into one bullet.
- Do not split one pending change across multiple bullets.
- Describe the release-specific change after its marker.
- Sort bullets by the complete marker in this order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.

End the entry with this exact HTML comment after all bullets:

`<!-- stl-impact: v1 -->`

If a classification remains ambiguous, choose the more disruptive option: the alphabetically earlier letter and the lower digit.