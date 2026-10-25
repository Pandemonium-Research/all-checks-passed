---
name: impact-log
description: Use this guide to convert a supplied release version, date, and list of pending changes into one correctly formatted release-notes entry with classified impact markers, sorted items, an aggregate impact, and the required parser trailer.
---

# Release notes

Create exactly one release entry using the structure and classification rules below. Return only the entry.

## Required structure

Write these elements in order:

1. `## [VERSION] - YYYY-MM-DD`
2. One blank line.
3. `Impact: DIGIT`
4. One blank line.
5. One list item for each pending change: `- [LETTERDIGIT] Description`
6. One blank line.
7. `<!-- stl-impact: v1 -->`

Copy the supplied version and date exactly. Do not add introductory text, closing text, subsections, or a colon after an impact marker.

## Classify each change

Each marker contains a letter and a digit, such as `[B2]`. Choose the letter and digit independently from the change’s effect.

If one change has multiple effects, use the earliest applicable letter and the lowest applicable digit.

### Choose the letter

Use the first applicable category:

- `A` — The public interface or supported compatibility surface changes. This includes exported names, public functions or classes, parameters, signatures, accepted or returned types, public type annotations, and supported runtime or platform versions.
- `B` — The public interface is unchanged, but callers can observe different functional behavior, results, state, or errors.
- `C` — Neither the public interface nor functional results change. This includes internal implementation, performance or resource-use work, tests, documentation, CI, tooling, and packaging maintenance that preserves installation behavior.

Use `A` before `B` before `C`.

In particular:

- Adding, removing, or changing an exported feature, parameter, signature, accepted type, or returned type is `A`.
- Adding or changing public type annotations is `A`, even when runtime behavior is unchanged.
- Dropping support for a runtime or platform version is `A`.
- Changing output or errors without changing the public interface is `B`.
- Improving speed, memory use, or resource use while preserving the interface and functional results is `C`.
- Internal or project-maintenance work with no caller-facing effect is `C`.

### Choose the digit

Use the first applicable rule:

1. `1` — Breaking: a supported existing use can fail, receive an incompatible type or value, produce different supported results, encounter a new error, or require changed code or expectations.
2. `2` — Compatible and meaningful: existing supported uses remain compatible, while functionality is added, accepted use is broadened, an erroneous failure is removed, behavior outside the supported contract is corrected, or performance or resource use improves.
3. `3` — Caller-invisible: the supported runtime behavior, functional results, performance, and resource use remain unchanged.

Use `1` before `2` before `3`.

Apply these specific rules:

- Removing or narrowing a supported interface is digit `1`.
- Dropping a supported runtime or platform version is digit `1`.
- Changing a public return type is digit `1`, not digit `2`.
- Changing output for ordinary supported inputs is digit `1` unless the pending change explicitly establishes that the old behavior was erroneous or outside the supported contract.
- Introducing an error for a previously supported use is digit `1`.
- Adding an optional public capability while preserving existing behavior is digit `2`.
- Eliminating an erroneous failure while preserving correct existing uses is digit `2`.
- A defect fix is digit `2` only when correct supported callers remain compatible. Calling a change a “fix” does not by itself make it digit `2`.
- An explicit speed, memory, or resource-use improvement is digit `2`, even when interface and functional results are unchanged.
- Public annotations or other public metadata with no runtime effect are digit `3`.
- Internal rewrites, tests, documentation, CI, tooling, and maintenance-only packaging changes are digit `3` when they do not change behavior, performance, or resource use.

### Common marker combinations

- `A1` — Breaking public-interface or compatibility change, including a changed return type.
- `A2` — Compatible public-interface addition or broadening.
- `A3` — Public-interface metadata change with no runtime effect.
- `B1` — Breaking behavior or output change with an unchanged interface.
- `B2` — Contract-preserving behavioral correction or enhancement.
- `C2` — Performance or resource improvement with unchanged interface and results.
- `C3` — Caller-invisible internal or project-maintenance change.

## Write and order the list

Represent every pending change exactly once. Do not combine separate changes or split one change into multiple items.

Write each item in this exact form:

`- [LETTERDIGIT] Concise description`

Use exactly one space after the closing bracket. Preserve the facts needed to understand the change and its compatibility effect. Do not invent details.

Sort items in this exact marker order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

For items with the same marker, retain their supplied order.

## Calculate the summary

Set `Impact` to the lowest digit appearing in any list-item marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Consider only digits inside list-item markers. Ignore all other numerals, including those in the version, date, descriptions, and trailer.

## Final check

Before returning the entry, verify that:

- The heading contains the supplied version and date exactly.
- Every pending change appears exactly once.
- Every list item has a valid marker and one space before its description.
- Changed return types and dropped supported versions use `A1`.
- Compatible public additions use `A2`.
- Runtime-inert public annotations use `A3`.
- Incompatible output changes with unchanged interfaces use `B1`.
- Contract-preserving corrections use `B2`.
- Explicit performance or resource improvements use `C2`.
- Caller-invisible maintenance uses `C3`.
- Items follow the required marker order, preserving supplied order for ties.
- `Impact` is the lowest list-marker digit.
- The trailer is the final line.