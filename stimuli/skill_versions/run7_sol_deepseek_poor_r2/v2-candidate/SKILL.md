---
name: impact-log
description: Use this document to turn a release version, release date, and list of pending project changes into a classified, sorted, parser-compatible release notes entry.
---

# Release notes

For every release, classify each pending change, sort the resulting bullets, and then calculate the release impact.

The finished entry must contain, in order:

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

Replace all placeholders with values for the current release. Never reuse classifications merely because an older release contained a similar-looking change.

## Classify every pending change

Assign exactly one marker to each pending change. A marker consists of one letter and one digit in square brackets, such as `[A2]`.

Write each bullet as:

`- [A2] Description.`

The letter and digit answer separate questions:

- The letter identifies what part of the project changed.
- The digit identifies how disruptive or observable the change is.

Choose the letter first, then choose the digit. Do not infer the digit from the letter.

### Choose the letter

Use the alphabetically earliest category that applies:

- `A` — Public API surface or caller-visible contract. This includes exported names, functions, methods, signatures, accepted argument types, return types, and documented caller-facing behavior.
- `B` — Runtime implementation or behavior without a public API or caller-visible contract change. This includes runtime bug fixes, algorithm changes, performance work, and caching.
- `C` — Non-runtime project work. This includes build configuration, packaging infrastructure, supported-environment policy, development tooling, tests, and documentation.

For a change spanning categories, choose `A` over `B` over `C`.

Examples of how to choose the letter:

- Adding an exported function is `A` because it expands the public API.
- Changing a function's accepted argument types or return type is `A`.
- Changing documented output behavior is `A`.
- Fixing runtime behavior while preserving the public contract is `B`.
- Refactoring or caching runtime code with identical results is `B`.
- Changing packaging files without changing the installed user experience is `C`.
- Dropping support for a Python version or other supported environment is `C`.

Do not use any other letter.

### Choose the digit

Use the lowest-numbered category that applies:

- `1` — Breaking. Previously valid or working use can fail, become invalid, or produce a different caller-visible result.
- `2` — Compatible. The change is additive, or it corrects faulty behavior without disrupting correct existing use.
- `3` — Unobservable to callers. No caller can observe a functional difference.

Important distinctions:

- Adding a public API is additive, so it is `A2`, not `A1`.
- Removing a public API is breaking, so it is `A1`.
- Changing an accepted argument type or return type is `A1` if previously working calls can break.
- A bug fix can be `2` even when the buggy case now produces a different result, provided the new result restores intended behavior and correct existing use remains unaffected.
- An internal runtime optimization with unchanged interface and results is `B3`.
- Non-runtime work can still be breaking, such as dropping a supported environment; use `C1`.

When multiple digits apply, choose `1` over `2` over `3`.

## Build the entry

Write the release heading exactly as:

`## [VERSION] - YYYY-MM-DD`

Use the supplied three-part version number and ISO-formatted date.

Leave one blank line after the heading, then write:

`Impact: N`

Determine `N` only after every pending change has been classified. Set it to the lowest digit present in any bullet marker:

- Any marker ending in `1` makes the impact `1`.
- Otherwise, any marker ending in `2` makes the impact `2`.
- Otherwise, the impact is `3`.

Ignore numbers in the version, date, descriptions, and parser trailer.

Leave one blank line after the impact field. Create exactly one bullet for each pending change:

- Do not omit a pending change.
- Do not combine pending changes.
- Do not split one pending change into multiple bullets.
- Put the marker immediately after `- `.
- Do not place a colon after the marker.
- Describe the release-specific change after the marker.

After classifying all changes, sort the bullets by their complete markers in this exact order:

1. `A1`
2. `A2`
3. `A3`
4. `B1`
5. `B2`
6. `B3`
7. `C1`
8. `C2`
9. `C3`

Do not preserve the input order when it conflicts with this marker order. Keep changes sharing the same marker in their original relative order.

Leave one blank line after the final bullet and end with this exact trailer:

`<!-- stl-impact: v1 -->`

Before returning the entry, verify that every pending change appears exactly once, all bullets are sorted, and the `Impact` value equals the lowest bullet-marker digit.