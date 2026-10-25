---
name: impact-log
description: Use this document when given a release version, date, and pending-change list to write one classified, sorted, parser-compatible release-notes entry.
---

# Release notes

## Required output structure

Write exactly one entry in this order:

    ## [{version}] - {YYYY-MM-DD}
    Impact: {lowest marker digit}

    - [{marker}] {pending change}
    - [{marker}] {pending change}

    <!-- stl-impact: v1 -->

Follow these formatting rules exactly:

- Use the supplied version and date without changing them.
- Start the heading with exactly `##`.
- Put the version in square brackets.
- Write the date as `YYYY-MM-DD`.
- Write `Impact:` with a capital `I`.
- Leave one blank line after the `Impact` line.
- Start every change with `- ` followed immediately by its square-bracketed marker.
- Preserve each pending change's wording and punctuation.
- Leave one blank line between the last bullet and the trailer.
- End with `<!-- stl-impact: v1 -->` exactly as shown.
- Do not add an introduction, summary, extra heading, or footer.

## Process

For each pending change:

1. Create exactly one bullet. Do not combine or split changes.
2. Choose its letter using the letter rules.
3. Choose its digit independently using the digit rules.
4. Combine them into a marker such as `[B2]`.
5. Sort all bullets by marker, preserving the supplied order among bullets with the same marker.
6. Set `Impact` to the smallest marker digit.

## Select the letter

Choose the first applicable letter in this order: `A`, then `B`, then `C`.

### A — public API surface or type contract

Use `A` when the exposed interface or public type contract changes, including:

- Adding or removing a public name.
- Changing a public function or class signature.
- Changing accepted argument types.
- Changing a public return type.
- Adding or changing publicly shipped typing information.

A change to the value or content returned by existing functionality is not `A` when its public name, signature, and return type remain unchanged. Use `B` for that change.

### B — caller-visible runtime behavior

Use `B` when the public API and type contract remain unchanged, but existing functionality can produce a different:

- Return value or rendered output.
- Side effect.
- Exception or error-handling result.
- Other caller-visible runtime behavior.

Runtime bug fixes normally use `B`.

### C — non-API work

Use `C` when neither `A` nor `B` applies, including:

- Internal refactoring or optimization with unchanged results.
- Build, packaging, installation, artifact, metadata, or dependency changes.
- Supported-language, platform, or environment changes.
- Tooling, tests, or documentation changes.

Dropping or adding support for a language version, platform, or environment uses `C`.

## Select the digit

Choose the lowest applicable digit.

### 1 — breaking

Use `1` when previously supported, correct usage can stop working or its documented result can change. This includes:

- Removing public functionality.
- Making an incompatible signature or type-contract change.
- Intentionally changing documented behavior for supported inputs.
- Dropping a supported language version, platform, or environment.

Do not use `1` merely because a bug fix changes an incorrect result. If the old behavior was outside the supported contract and correct existing usage remains valid, use `2`.

### 2 — compatible and observable

Use `2` when correct existing usage remains valid but a supported consumer can observe the change. Supported consumers include callers, type checkers, installers, packagers, and integrators.

Examples include:

- New public functionality.
- Compatible additions or changes to shipped typing information.
- Compatible runtime bug fixes.
- Corrections to behavior outside the supported contract.
- Added environment support.
- Changes to installed files, distributed artifacts, package metadata, or external dependencies.

Adding, removing, replacing, externalizing, or vendoring a dependency is observable and normally uses `C2`, even when application output is unchanged.

### 3 — unobservable to supported consumers

Use `3` only when supported consumers cannot observe any API, typing, runtime, environment, installation, dependency, metadata, or artifact difference.

Examples include:

- Internal refactoring with unchanged results.
- Optimizations with unchanged results.
- Tests and internal tooling.
- Documentation-only changes.
- Operational migrations that preserve supported behavior and distributed metadata.

Unchanged runtime output alone does not justify `3`. Use `2` if installers, packagers, or integrators can observe the change.

## Calculate `Impact`

Set `Impact` to the smallest digit appearing in the bullet markers:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Consider only marker digits. Ignore digits in the version, date, change descriptions, and trailer.

## Sort the bullets

Sort markers in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

When multiple changes have the same marker, keep them in their original supplied order.

## Final check

Before submitting, verify that:

- The heading uses the supplied values and matches `## [{version}] - {YYYY-MM-DD}`.
- Every pending change appears exactly once with its original wording.
- Every bullet begins with a marker from `[A1]` through `[C3]`.
- Same-type value or output changes use `B`, not `A`.
- Supported-environment changes use `C`.
- Bug fixes are not marked breaking solely because their results changed.
- Observable installation, artifact, metadata, or dependency changes use `2`, not `3`.
- `Impact` equals the smallest marker digit.
- Bullets follow the required marker order.
- Changes sharing a marker retain their supplied order.
- The final line is exactly `<!-- stl-impact: v1 -->`.