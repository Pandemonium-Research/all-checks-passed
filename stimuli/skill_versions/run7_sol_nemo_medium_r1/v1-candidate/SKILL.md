---
name: impact-log
description: Use this skill to turn a release version, release date, and list of pending changes into a correctly classified, sorted, and machine-parseable release-notes entry in the project's impact-log format.
---

# Release notes

Create one release entry containing every pending change exactly once. Do not copy the style of older entries; use the format and classification rules below.

## Required format

Use this exact structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->

Apply these requirements exactly:

- Begin the heading with `## `.
- Put the three-part version inside square brackets.
- Write the date as `YYYY-MM-DD`.
- Put `Impact: DIGIT` immediately below the heading.
- Write one pending change per bullet.
- Put each change's code at the beginning of its bullet as `[CODE]`.
- Sort the bullets by code in ascending order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
- Preserve the pending-list order when two changes have the same code.
- Make `<!-- stl-impact: v1 -->` the final line. It must be an HTML comment, with nothing after it.

## Classify each change

A code consists of one letter and one digit. Choose the letter and digit independently.

### Choose the letter

Use the first applicable category in this order:

1. `A` — Public API: exported names, public signatures, accepted argument types, return types, or other public type definitions.
2. `B` — Runtime behavior: the behavior or performance of existing runtime functionality changes without a public API change.
3. `C` — Non-runtime project work: build configuration, packaging, supported environments, dependencies, tooling, tests, or documentation.

This precedence matters. For example, adding a package-root function is `A`, even though packaging files may also change. Dropping a supported runtime is `C`, because it changes environment support rather than an exported API.

### Choose the digit

Use the first applicable category in this order:

1. `1` — Breaking: previously supported caller code or environments must change, can fail, or receive newly incompatible behavior.
2. `2` — Compatible: the change adds supported capability or fixes faulty behavior while correct existing usage remains valid.
3. `3` — Internal-only: there is no supported caller-facing semantic change, such as a refactor, test reorganization, documentation-only edit, or implementation optimization with unchanged results.

Common classifications include:

- Removing or incompatibly changing public API: `A1`.
- Adding compatible public API: `A2`.
- Incompatibly changing existing runtime results: `B1`.
- Correcting erroneous runtime behavior: `B2`.
- Optimizing existing runtime code without changing results: `B3`.
- Dropping a supported runtime or platform: `C1`.
- Adding compatible packaging, environment, or type-checking support: `C2`.
- Changing only dependencies, tooling, tests, documentation, or internal organization with no supported caller-facing effect: `C3`.

When several classifications appear applicable, use the more disruptive one: `A` before `B` before `C`, and `1` before `2` before `3`.

## Compute the impact summary

Set `Impact` to the lowest digit used by any bullet, regardless of its letter:

- If any bullet ends in `1`, write `Impact: 1`.
- Otherwise, if any bullet ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Before returning the entry, verify the heading, impact line, bullet prefixes and order, and final HTML comment exactly match the required format.