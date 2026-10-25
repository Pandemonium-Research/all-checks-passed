---
name: impact-log
description: Use this guide to convert a supplied release version, date, and list of pending project changes into one parser-ready release-nototes entry with correctly classified markers, stable ordering, aggregate impact, and the required trailer.
---

# Release notes

Create exactly one release entry. Return only the entry.

## Required output

Write these elements in this exact order:

1. `## [VERSION] - YYYY-MM-DD`
2. One blank line.
3. `Impact: DIGIT`
4. One blank line.
5. One list item for every supplied pending change: `- [LETTERDIGIT] Description`
6. One blank line.
7. `<!-- stl-impact: v1 -->`

Copy the supplied version and date exactly. Do not add an introduction, conclusion, subsection, or colon after a marker.

## Classify every pending change

Choose the marker letter and digit independently according to the change’s actual effect. Do not rely only on labels such as “fix,” “improvement,” “refactor,” or “internal.”

If a change has several effects, use the earliest applicable letter and the lowest applicable digit.

### Choose the letter

Determine which surface changes:

- `A` — The public interface or supported compatibility surface changes. This includes exported names, public functions or classes, parameters, signatures, accepted or returned types, public annotations, and supported runtime or platform versions.
- `B` — The public interface remains the same, but callers can observe different functional behavior, output, state, or errors.
- `C` — Neither the public interface nor functional results change. This includes implementation work, performance or resource-use changes, tests, documentation, CI, tooling, and packaging maintenance that preserves installation and compatibility.

Use the first applicable letter: `A` before `B` before `C`.

Apply these rules:

- Adding an optional public parameter or exported feature is `A`.
- Removing or narrowing a public capability is `A`.
- Changing a public return type is `A`, even if the signature otherwise looks unchanged.
- Adding or changing public type annotations is `A`, even if runtime behavior is unchanged.
- Dropping a supported runtime or platform version is `A`.
- Changing results or errors without changing the public interface is `B`.
- Improving speed, memory use, or resource use while preserving interface and results is `C`.
- A packaging change that alters installation or supported compatibility is `A`; maintenance that preserves them is `C`.

### Choose the digit

Determine the effect on supported existing callers:

- `1` — Breaking. A supported existing use may fail, receive a different or incompatible type or value, produce incompatible results, encounter a new error, or require modification.
- `2` — Compatible but meaningful. The change adds usable functionality, broadens accepted use, corrects behavior outside the supported contract, or improves performance or resource use without invalidating correct existing use.
- `3` — Caller-invisible. The supported runtime contract, functional results, performance characteristics, and resource behavior remain unchanged.

Apply these tests in order:

1. If any supported existing use can become incompatible, choose `1`.
2. Otherwise, if the change adds a capability, fixes behavior outside the supported contract, or improves a runtime property such as speed or memory use, choose `2`.
3. Otherwise, choose `3`.

Use the lowest applicable digit: `1` before `2` before `3`.

#### Breaking changes: digit `1`

Use `1` for:

- Removing, renaming, or narrowing a supported interface.
- Dropping a supported runtime or platform version.
- Changing a public return type.
- Changing output for ordinary supported inputs when callers could validly rely on the previous output.
- Introducing an error for a previously supported use.
- Any change that requires supported callers to update their code or expectations.

A change is still breaking when described as a fix or improvement if it invalidates supported existing behavior.

#### Compatible changes: digit `2`

Use `2` for:

- Adding an optional public capability while preserving existing behavior.
- Broadening accepted inputs.
- Correcting behavior that was outside the documented or supported contract.
- Eliminating an erroneous failure while preserving correct existing uses.
- Improving speed, memory consumption, or other resource behavior without changing interface or functional results.

Do not assign `2` merely because a change is called a bug fix. If the old result was supported and callers could rely on it, an incompatible new result is `1`.

When a description states only that output now differs for a class of ordinary inputs, treat that as `1` unless it also establishes that the old behavior violated the supported contract.

#### Caller-invisible changes: digit `3`

Use `3` for:

- Public metadata changes, such as annotations, with no runtime effect.
- Internal rewrites with no stated interface, result, performance, or resource change.
- Tests, documentation, CI, or tooling changes with no caller-facing effect.
- Maintenance-only packaging changes that preserve installation behavior.

If an internal rewrite explicitly improves speed or resource use, use `2`, not `3`.

### Common marker combinations

- `A1` — Breaking public-interface or compatibility change.
- `A2` — Compatible public-interface addition or broadening.
- `A3` — Public-interface metadata change without runtime effect.
- `B1` — Breaking functional-behavior change with an unchanged interface.
- `B2` — Contract-preserving behavioral correction or enhancement.
- `C2` — Performance or resource improvement with unchanged interface and results.
- `C3` — Caller-invisible internal or project-maintenance change.

## Write and sort the items

Represent every supplied pending change exactly once. Do not merge separate changes or divide one change into multiple items.

Write each item as:

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

Consider only digits inside list-item markers. Ignore numerals in the version, date, descriptions, and trailer.

## Final verification

Before returning the entry, confirm that:

- The heading contains the supplied version and date exactly.
- Every pending change appears exactly once.
- Each letter reflects the changed surface.
- Each digit reflects compatibility with supported existing uses.
- Every incompatible return-type, supported-version, output, or error change uses digit `1`.
- Every compatible addition, contract-preserving correction, or performance or resource improvement uses digit `2`.
- Metadata-only and maintenance-only changes use digit `3`.
- Items follow the required marker order, with supplied ordering preserved for ties.
- `Impact` is the lowest list-marker digit.
- The trailer is the final line.