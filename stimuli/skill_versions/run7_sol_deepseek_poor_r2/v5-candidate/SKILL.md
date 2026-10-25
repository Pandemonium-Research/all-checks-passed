---
name: impact-log
description: Use this document to turn a release version, date, and pending-change list into a classified, globally sorted, parser-compatible release notes entry.
---

# Release notes

Produce one release entry in this exact order:

1. Release heading
2. Impact field
3. One bullet for every pending change
4. Parser trailer

The completed entry must have this structure:

## [VERSION] - YYYY-MM-DD

Impact: LOWEST_MARKER_DIGIT

- [A1] Change description.
- [A2] Change description.
- [B2] Change description.

<!-- stl-impact: v1 -->

Replace all placeholders with information for the current release.

## Classify every change

Assign each pending change exactly one marker. A marker contains one letter and one digit, such as `[B2]`.

Choose the letter and digit independently. Write the marker immediately after the bullet prefix:

`- [B2] Description.`

Do not put a colon after the marker.

### Choose the letter

Use the first applicable category:

- `A` — The public API surface changes. This includes exported names, functions, methods, signatures, accepted argument types, and return types.
- `B` — Runtime behavior or implementation changes while the public API surface remains unchanged. This includes changed output values, bug fixes, algorithms, performance work, and internal caching.
- `C` — Non-runtime project work. This includes supported-environment policy, build configuration, packaging infrastructure, development tooling, tests, and documentation.

Important distinctions:

- Adding, removing, or changing a public export or signature is `A`.
- Changing runtime results without changing the public API surface is `B`, even when callers can observe the result change.
- Dropping a previously supported runtime or platform is `C`.
- If one change spans categories, choose `A` before `B` before `C`.

Do not use any other letter.

### Choose the digit

Use the first applicable category:

- `1` — Breaking: previously working use can fail, become invalid, or produce a different correct, documented result.
- `2` — Compatible: the change adds a capability or fixes incorrect behavior without disrupting correct existing use.
- `3` — Unobservable: callers cannot observe a functional difference.

Apply these rules:

- A new public function, method, export, parameter, or accepted input type is additive and therefore `A2`, unless it invalidates previously working use.
- Removing or incompatibly changing public API is `A1`.
- Changing a return type in a way that can affect existing callers is `A1`.
- A runtime behavior change that disrupts previously correct use is `B1` when the public API surface is unchanged.
- A bug fix is `2` when it restores intended behavior without disrupting correct existing use, even if the buggy case now returns a different result.
- Internal runtime work with unchanged results and public API is `B3`.
- Non-runtime work can be breaking; ending support for a previously supported environment is `C1`.

If multiple digits apply, choose the lowest digit: `1` before `2` before `3`.

## Write the entry

Write the heading exactly as:

`## [VERSION] - YYYY-MM-DD`

Use the supplied three-part version number and ISO-formatted date.

Leave one blank line after the heading. Then write:

`Impact: N`

Classify every pending change before calculating `N`. Set `N` to the lowest digit present in any bullet marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only marker digits for this calculation. Ignore numbers in the version, date, descriptions, and parser trailer.

Leave one blank line after the impact field. Write exactly one bullet for each pending change:

- Include every pending change exactly once.
- Do not combine separate pending changes.
- Do not split one pending change into multiple bullets.
- Describe only the release-specific change after its marker.

After classifying all changes, globally sort the entire bullet list in this exact order:

1. `A1`
2. `A2`
3. `A3`
4. `B1`
5. `B2`
6. `B3`
7. `C1`
8. `C2`
9. `C3`

Do not preserve input order when it conflicts with this marker order. Preserve the original relative order only between bullets with the same marker. For example, every `A1` bullet must appear before every `A2` bullet, regardless of their original positions.

Leave one blank line after the final bullet. End with this exact trailer:

`<!-- stl-impact: v1 -->`

Before returning the entry, verify that:

- Every pending change appears exactly once.
- Every additive public API change is `A2` unless it breaks existing use.
- Runtime result changes with an unchanged API surface use `B`.
- The entire bullet list follows the required marker order.
- `Impact` equals the lowest digit in the bullet markers.