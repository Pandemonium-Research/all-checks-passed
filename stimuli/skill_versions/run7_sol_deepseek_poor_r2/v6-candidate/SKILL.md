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

- `A` — The public API surface changes. This includes adding, removing, or changing exported names, function or method signatures, accepted argument types, or return types.
- `B` — Runtime implementation or behavior changes while the public API surface remains unchanged. This includes changed results, runtime fixes, algorithm changes, performance work, and internal caching.
- `C` — Non-runtime project work, such as supported-environment policy, build configuration, packaging infrastructure, development tooling, tests, or documentation.

Apply these distinctions:

- Adding, removing, or changing a public export or signature is `A`.
- A changed runtime result is `B` when exported names, signatures, accepted argument types, and return types are unchanged. The fact that callers can observe the result does not make the change `A`.
- Dropping support for a previously supported runtime, platform, or environment is `C`.
- If one pending change genuinely spans categories, use `A` before `B` before `C`.

Do not invent other letters.

### Choose the digit

Use the first applicable category:

- `1` — Breaking: previously working caller code can now fail, become invalid, or produce a different result.
- `2` — Compatible: the change adds a capability or fixes incorrect behavior while correct existing code remains unaffected.
- `3` — Unobservable to callers: no caller can observe a functional difference.

Apply these rules:

- Adding a public function, method, export, parameter, or accepted argument type is additive. Use `A2` unless the addition itself breaks previously working code.
- Removing or incompatibly changing public API is `A1`.
- A runtime result change that disrupts previously working use is `B1` when the public API surface is unchanged.
- A bug fix may change the result for the buggy case and still use digit `2` when it restores intended behavior without breaking correct existing use.
- Internal runtime work whose results and public API are unchanged is `B3`.
- Non-runtime work can be breaking; dropping a previously supported environment is `C1`.

If more than one digit applies to the same change, choose the lowest digit: `1` before `2` before `3`. Do not classify an additive public API change as breaking merely because `1` is more disruptive than `2`.

## Write the entry

Use a second-level Markdown heading in exactly this form:

`## [VERSION] - YYYY-MM-DD`

Use the supplied three-part version number and ISO date. Leave one blank line after the heading.

Write the impact field as:

`Impact: N`

Classify all pending changes before calculating `N`. Set `N` to the lowest digit used in any bullet marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Inspect only the marker digits. Ignore all digits in the version, date, descriptions, and parser trailer.

Leave one blank line after the impact field. Create exactly one bullet for each pending change:

- Include every pending change exactly once.
- Do not merge multiple pending changes into one bullet.
- Do not split one pending change across multiple bullets.
- Describe the release-specific change after its marker.

Sort the entire bullet list by complete marker in this exact order:

1. `A1`
2. `A2`
3. `A3`
4. `B1`
5. `B2`
6. `B3`
7. `C1`
8. `C2`
9. `C3`

Preserve the original relative order only among bullets with the same marker.

Leave one blank line after the final bullet. End the entry with this exact HTML comment:

`<!-- stl-impact: v1 -->`

Before returning the entry, verify that every pending change appears exactly once, additive public API changes use `A2` unless they are breaking, runtime result changes with an unchanged API surface use `B`, the bullets follow the required marker order, and `Impact` equals the lowest bullet-marker digit.