---
name: impact-log
description: Use this guide to turn a supplied release version, release date, and list of pending changes into one parser-ready release-notes entry with classified impact markers, sorted items, an aggregate impact summary, and the required trailer.
---

# Release notes

Create exactly one release entry from the supplied version, date, and pending changes. Return only the entry.

## Required output

Write these elements in this exact order:

1. `## [VERSION] - YYYY-MM-DD`
2. One blank line.
3. `Impact: DIGIT`
4. One blank line.
5. One list item for each pending change: `- [LETTERDIGIT] Description`
6. One blank line.
7. `<!-- stl-impact: v1 -->`

Copy the supplied version and date exactly. Do not add an introduction, conclusion, subsection, or colon after a marker.

## Classify each pending change

Choose the letter and digit independently from the change’s actual effect. Do not classify from labels such as “fix,” “improve,” “optimize,” or “refactor” alone.

If one pending change has several effects, use the earliest applicable letter and the lowest applicable digit.

### Choose the letter

Use the first applicable category:

- `A` — The public interface or supported compatibility surface changes. This includes exported names, public classes or functions, parameters, signatures, accepted or returned types, public type annotations, and supported runtime or platform versions.
- `B` — The public interface is unchanged, but callers can observe different functional behavior, output, state, or errors.
- `C` — Neither the public interface nor functional results change. This includes internal implementation, performance or resource-use changes, tests, documentation, CI, tooling, and packaging maintenance that preserves installation behavior.

Use `A` before `B` before `C`.

Apply these rules:

- Adding an optional public capability is `A`, even when existing calls behave identically.
- Removing or narrowing a public capability is `A`.
- Changing a public return type is `A`, not `B`.
- Adding or changing public type annotations is `A`, even without a runtime effect.
- Dropping a supported runtime or platform version is `A`.
- Changing results or errors while retaining the same public interface is `B`.
- Improving speed, memory use, or other resource use while preserving the interface and functional results is `C`.
- A packaging change that alters installation compatibility or supported environments is `A`; packaging maintenance that preserves them is `C`.

### Choose the digit

Apply these tests in order:

1. If any supported existing use can become incompatible, choose `1`.
2. Otherwise, if the change adds a capability, broadens supported use, corrects behavior outside the supported contract, or improves performance or resource use, choose `2`.
3. Otherwise, choose `3`.

The digits mean:

- `1` — Breaking. A supported existing use may fail, receive an incompatible value or type, produce different supported results, encounter a new error, or require code or expectation changes.
- `2` — Compatible but meaningful. Correct existing uses remain compatible, while the change adds functionality, broadens accepted use, corrects behavior outside the supported contract, removes an erroneous failure, or improves performance or resource use.
- `3` — Caller-invisible. The supported runtime contract, functional results, performance characteristics, and resource behavior remain unchanged.

Use the lowest applicable digit: `1` before `2` before `3`.

#### Use digit `1` for incompatible changes

This includes:

- Removing, renaming, or narrowing a supported public interface.
- Dropping a supported runtime or platform version.
- Changing a public return type.
- Changing output for ordinary supported inputs when callers could rely on the previous output.
- Introducing an error for a previously supported use.
- Any change that requires supported callers to update code or expectations.

A change remains digit `1` when described as a fix or improvement if it invalidates supported existing behavior.

When a description says that output now differs for a class of ordinary inputs, choose `1` unless it explicitly establishes that the old output was outside the supported contract.

#### Use digit `2` for compatible meaningful changes

This includes:

- Adding an optional public capability while preserving existing behavior.
- Broadening accepted inputs.
- Correcting behavior that was outside the documented or supported contract.
- Eliminating an erroneous failure while preserving correct existing uses.
- Improving speed, memory consumption, or other resource behavior without changing the interface or functional results.

A bug fix is not automatically digit `2`. Choose `2` only when the old behavior was outside the supported contract and correct existing callers remain compatible.

An optimization explicitly described as faster, more memory-efficient, or less resource-intensive is digit `2`, even when its interface and output are unchanged.

#### Use digit `3` for caller-invisible changes

This includes:

- Public metadata changes, such as annotations, with no runtime effect.
- Internal rewrites with no stated interface, result, performance, or resource change.
- Tests, documentation, CI, or tooling changes with no caller-facing effect.
- Maintenance-only packaging changes that preserve installation behavior.

Do not use digit `3` when the change explicitly improves speed, memory use, or another runtime property; use digit `2`.

### Common marker combinations

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
- Every incompatible public-interface, supported-version, return-type, output, or error change uses digit `1`.
- Every compatible addition, contract-preserving correction, or stated performance or resource improvement uses digit `2`.
- Public metadata-only changes and maintenance-only changes use digit `3`.
- Items follow the required marker order, with supplied ordering preserved for ties.
- `Impact` is the lowest list-marker digit.
- The trailer is the final line.