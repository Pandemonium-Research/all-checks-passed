---
name: impact-log
description: Use this document when converting a release version, date, and list of pending changes into a correctly classified, globally sorted, parser-compatible release notes entry.
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
- [A2] Change description.
- [B2] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders with release-specific values. Do not copy classifications from another release.

## Classify each change

Every pending change must have exactly one two-character impact marker in square brackets:

- The first character is `A`, `B`, or `C`.
- The second character is `1`, `2`, or `3`.
- Write the marker immediately after the bullet prefix: `- [A1] Description.`
- Do not add a colon after the marker.

Choose the letter and digit independently. An `A` change is not automatically breaking.

### Choose the letter

Use the first applicable category:

- `A` — Public API surface or caller-visible contract: exported names, functions, methods, signatures, accepted argument types, return types, or documented output behavior.
- `B` — Runtime implementation or behavior when no public API or caller-visible contract changes. This includes runtime fixes, algorithm changes, performance work, and internal caching, even when results remain unchanged.
- `C` — Non-runtime project work, such as supported-environment policy, build configuration, packaging infrastructure, development tooling, tests, or documentation.

For a change spanning multiple categories, use the alphabetically earliest applicable letter: `A` before `B` before `C`.

Do not invent other letters.

### Choose the digit

Use the first applicable category:

- `1` — Breaking: previously working caller code can now fail, become invalid, or produce a different caller-visible result.
- `2` — Compatible: the change adds a capability or fixes incorrect behavior while correct existing use remains unaffected.
- `3` — Unobservable to callers: no caller can observe a functional difference.

Apply these rules explicitly:

- Adding a new public function, method, export, parameter, or accepted input type is additive and therefore `A2`, not `A1`, unless it invalidates previously working use.
- Removing or incompatibly changing a public API is `A1`.
- Changing a return type or documented result is `A1` when previously working callers can be affected.
- A bug fix is `2` when it restores intended behavior without disrupting correct existing use, even if the buggy case now returns a different result.
- Internal runtime work with unchanged results and public interface is `B3`.
- Non-runtime work can be breaking; for example, ending support for a previously supported environment is `C1`.

If more than one digit applies, use the lowest digit: `1` before `2` before `3`.

## Write the entry

Use a second-level Markdown heading in exactly this form:

`## [VERSION] - YYYY-MM-DD`

Use the supplied three-part version number and ISO-formatted date.

Leave one blank line after the heading, then write:

`Impact: N`

Classify every pending change before calculating `N`. Set `N` to the lowest digit used in any bullet marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Inspect only marker digits. Ignore digits in the version, date, descriptions, and parser trailer.

Leave one blank line after the impact field. Create exactly one bullet for each pending change:

- Do not omit a pending change.
- Do not merge pending changes.
- Do not split one pending change into multiple bullets.
- Describe the release-specific change after its marker.

After every change has been classified, sort the entire bullet list by complete marker in this exact order:

1. `A1`
2. `A2`
3. `A3`
4. `B1`
5. `B2`
6. `B3`
7. `C1`
8. `C2`
9. `C3`

All bullets with the same marker must be contiguous. Preserve the original relative order only among bullets that share the same marker. Never leave an `A1` bullet after an `A2` or `A3` bullet.

Leave one blank line after the final bullet and end with this exact HTML comment:

`<!-- stl-impact: v1 -->`

Before returning the entry, verify that:

- Every pending change appears exactly once.
- Every additive public API change is marked `A2`, unless it breaks existing use.
- Bullets are globally sorted by the required marker order.
- The `Impact` value is the lowest digit present in the bullet markers.