---
name: impact-log
description: Use this guide to convert a supplied release version, release date, and list of pending project changes into one parser-ready release-notes entry with classified impact markers, sorted items, an aggregate impact summary, and the required trailer.
---

# Release notes

Create exactly one release entry from the supplied version, date, and pending changes.

## Required output

Write only the following, in this exact order:

1. `## [VERSION] - YYYY-MM-DD`
2. One blank line.
3. `Impact: DIGIT`
4. One blank line.
5. One list item for each pending change: `- [LETTERDIGIT] Description`
6. One blank line.
7. `<!-- stl-impact: v1 -->`

Copy the supplied version and date exactly. Do not add an introduction, conclusion, subsection, or colon after a marker.

## Classify each pending change

Choose the marker letter and digit independently from the change’s actual effect. Do not classify from words such as “fix,” “improve,” or “refactor” alone.

If one pending change has several effects, use the earliest applicable letter and the lowest applicable digit.

### Choose the letter

Ask what surface the change alters:

- `A` — The public interface or supported compatibility surface changes. This includes exported names, public classes or functions, parameters, signatures, accepted or returned types, public type annotations, and supported runtime or platform versions.
- `B` — The public interface is unchanged, but callers can observe different functional behavior, output, state, or errors.
- `C` — Neither the public interface nor functional results change. This includes internal implementation, speed or memory changes, tests, documentation, CI, tooling, and packaging work that preserves installation behavior.

Use the first applicable letter: `A` before `B` before `C`.

Important distinctions:

- Adding an optional public capability is `A`, even when existing calls behave identically.
- Changing a public return type is `A`, not merely `B`.
- Adding or changing public annotations is `A`, even without a runtime effect.
- Changing results or errors while retaining the same public interface is `B`.
- Improving performance or resource use while preserving interface and results is `C`.
- A packaging change that alters supported installation or runtime compatibility is `A`; packaging maintenance that preserves it is `C`.

### Choose the digit

Ask what happens to supported existing callers:

- `1` — Breaking. A supported existing use may fail, receive an incompatible value or type, produce incompatible results, encounter a new error, or require code changes.
- `2` — Compatible but meaningful. The change adds usable functionality, broadens what is accepted, corrects behavior outside the supported contract, or improves performance or resource use without invalidating correct existing use.
- `3` — Caller-invisible. The supported runtime contract, functional results, performance characteristics, and resource behavior remain unchanged.

Use the lowest applicable digit: `1` before `2` before `3`.

Apply these tests in order:

1. If any supported existing use can become incompatible, choose `1`.
2. Otherwise, if the change adds a capability, corrects a defect, or improves a non-functional runtime property, choose `2`.
3. Otherwise, choose `3`.

Specific rules:

- Removing, renaming, or narrowing a supported public interface is `1`.
- Dropping a supported runtime or platform version is `1`.
- Changing a public return type is `1`, even if the new type seems preferable.
- Changing output or error behavior for ordinary supported inputs is `1` when callers could validly rely on the old behavior.
- A change described as a bug fix is not automatically `2`. Use `2` only when the old result was outside the supported contract and correct existing code remains compatible.
- Adding an optional public parameter or exported capability without changing existing behavior is `2`.
- A public metadata-only change with no runtime effect is `3`.
- A speed, memory-use, or resource-use improvement with unchanged interface and functional results is `2`.
- A pure refactor or a tests, documentation, CI, or tooling change is normally `3`.

Typical combinations are:

- `A1` — Breaking public-interface or compatibility change.
- `A2` — Compatible public-interface addition or broadening.
- `A3` — Public-interface metadata change without runtime effect.
- `B1` — Breaking functional-behavior change with an unchanged interface.
- `B2` — Contract-preserving behavioral correction or enhancement.
- `C2` — Performance or resource improvement with unchanged interface and results.
- `C3` — Caller-invisible internal or project-maintenance change.

## Write and sort the items

Represent every supplied pending change exactly once. Do not merge separate pending changes or divide one pending change into multiple items.

Write each item as:

`- [LETTERDIGIT] Concise description`

Use exactly one space after the closing bracket. Preserve the facts needed to understand the change and its compatibility effect; do not invent details.

Sort items in this exact marker order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

For items with the same marker, retain their supplied order.

## Calculate the summary

Set `Impact` to the lowest digit appearing in any list-item marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Consider only digits inside list-item markers. Ignore numerals in the version, date, descriptions, and trailer.

## Final verification

Before returning the entry, confirm that:

- The heading contains the supplied version and date exactly.
- Every pending change appears exactly once.
- The letter reflects the changed surface: public interface, functional behavior, or non-functional/internal work.
- Every incompatible return-type, supported-version, output, or error change uses digit `1`.
- Every compatible addition, contract-preserving correction, or performance/resource improvement uses digit `2`.
- Metadata-only and maintenance-only changes use digit `3`.
- Items follow the required marker order, with stable ordering for ties.
- `Impact` is the lowest list-marker digit.
- The trailer is the final line.