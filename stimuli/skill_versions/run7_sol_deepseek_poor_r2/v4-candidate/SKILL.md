---
name: impact-log
description: Use this document to convert a release version, date, and list of pending project changes into a classified, sorted, parser-compatible release notes entry.
---

# Release notes

Produce one entry containing, in this order:

1. The release heading.
2. The `Impact` field.
3. Exactly one bullet for each pending change.
4. The parser trailer.

Use this structure:

## [VERSION] - YYYY-MM-DD

Impact: LOWEST_MARKER_DIGIT

- [A1] Change description.
- [B2] Change description.
- [C3] Change description.

<!-- stl-impact: v1 -->

Replace every placeholder with information for the current release. Do not reuse classifications from another release.

## Classify each change

Assign every pending change exactly one marker. Write the marker immediately after `- `:

`- [A1] Description.`

Do not put a colon after the marker.

Choose the letter and digit independently. The letter identifies the kind of change; it does not determine whether the change is breaking.

### Choose the letter

Use the first applicable category:

- `A` — Public API surface: exported names, functions, methods, signatures, accepted argument types, return types, or other caller-visible interfaces.
- `B` — Runtime implementation or behavior when the public API surface is unchanged. This includes runtime bug fixes, output-behavior changes, algorithm changes, performance work, and internal caching.
- `C` — Non-runtime project work, such as supported-environment policy, build configuration, packaging infrastructure, development tooling, tests, or documentation.

For a change spanning multiple categories, use `A` before `B` before `C`.

Important distinctions:

- Adding, removing, or changing an exported API is `A`.
- Changing runtime output while leaving the public API surface unchanged is `B`, even when callers can observe the new output.
- Runtime work with unchanged output and public API is `B`.
- Dropping support for a previously supported environment is `C`.

Do not use any other letter.

### Choose the digit

Use the first applicable category:

- `1` — Breaking: previously working use can fail, become invalid, or produce a different result.
- `2` — Compatible: the change adds a capability or fixes incorrect behavior while correct existing use remains unaffected.
- `3` — Unobservable to callers: callers cannot observe a functional difference.

Apply these rules:

- Adding a public function, method, export, parameter, or accepted input type is additive. Use `A2`, not `A1`, unless the addition itself breaks previously working use.
- Removing or incompatibly changing public API is `A1`.
- A runtime output change that disrupts previously working use is `B1` when the public API surface is unchanged.
- A bug fix is `2` when it restores intended behavior without disrupting correct existing use, even if the buggy case now returns a different result.
- Internal runtime work with unchanged results and public API is `B3`.
- Non-runtime work may be breaking; dropping a supported environment is `C1`.

If multiple digits apply, use the lowest digit: `1` before `2` before `3`.

## Write the entry

Write the heading exactly as:

`## [VERSION] - YYYY-MM-DD`

Use the supplied three-part version number and ISO-formatted date.

Leave one blank line after the heading, then write:

`Impact: N`

Classify all pending changes before calculating `N`. Set `N` to the lowest digit found in any bullet marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only marker digits when calculating impact. Ignore numbers in the version, date, descriptions, and parser trailer.

Leave one blank line after the impact field. Create exactly one bullet for each pending change:

- Do not omit a change.
- Do not combine changes.
- Do not split one change into multiple bullets.
- Describe the release-specific change after its marker.

After classifying every change, sort the entire bullet list by complete marker in this exact order:

1. `A1`
2. `A2`
3. `A3`
4. `B1`
5. `B2`
6. `B3`
7. `C1`
8. `C2`
9. `C3`

Do not preserve input order when it conflicts with this marker order. Preserve the original relative order only among bullets with the same marker.

Leave one blank line after the final bullet and end with this exact trailer:

`<!-- stl-impact: v1 -->`

Before returning the entry, verify that every pending change appears exactly once, the bullets are globally sorted, every additive public API change is classified as `A2` unless it is breaking, and `Impact` equals the lowest bullet-marker digit.