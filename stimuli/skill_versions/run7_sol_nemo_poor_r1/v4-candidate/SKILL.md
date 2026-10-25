---
name: impact-log
description: Use this document when given a release version, date, and pending-change list to produce one classified, sorted, parser-compatible release-notes entry.
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

- Start the heading with exactly `##`.
- Put the supplied version in square brackets.
- Write the date as `YYYY-MM-DD`.
- Write `Impact:` with a capital `I`.
- Leave one blank line after `Impact:`.
- Start every change with `- ` followed immediately by a square-bracketed marker such as `[A2]`.
- Leave one blank line between the last bullet and the trailer.
- Put `<!-- stl-impact: v1 -->` at the bottom exactly as shown.
- Do not add another heading, introduction, summary, or footer.

## Process

For each pending change:

1. Write exactly one bullet. Do not combine changes or split one change into multiple bullets.
2. Select its letter using the letter rules below.
3. Select its digit independently using the digit rules below.
4. Join them inside square brackets, such as `[B2]`.
5. After all bullets are marked, sort them by marker.
6. Set `Impact` to the lowest digit used in the markers.

## Select the letter

Choose the first applicable letter in this order: `A`, then `B`, then `C`.

### A — public API or type surface

Use `A` when the exposed interface or public type contract changes, including:

- Adding or removing a public name.
- Changing a public function or class signature.
- Changing accepted argument types.
- Changing a public return type.
- Adding or changing publicly shipped typing information.

Use `A` only for interface or type-contract changes. A change to the value or content returned by a public function is not `A` when its public name, signature, and return type remain unchanged; use `B`.

### B — runtime behavior

Use `B` when the public API and type contract are unchanged, but existing functionality can produce a different:

- Return value or rendered output.
- Side effect.
- Exception or error-handling result.
- Other caller-visible runtime behavior.

Bug fixes to runtime behavior normally use `B`.

### C — non-API and non-runtime work

Use `C` when neither `A` nor `B` applies, including:

- Internal refactoring or optimization with unchanged results.
- Build, packaging, installation, artifact, or dependency changes.
- Supported-language, platform, or environment changes.
- Tooling, tests, or documentation changes.

Dropping a supported language, platform, or environment uses `C`, not `A`.

The letter and digit are independent. A `C` change may be breaking, compatible and observable, or unobservable.

## Select the digit

Choose the lowest applicable digit.

### 1 — breaking

Use `1` when previously supported, correct usage can stop working or its documented result can change. This includes:

- Removing public functionality.
- Making an incompatible signature or type-contract change.
- Intentionally changing documented behavior for supported inputs.
- Dropping a supported language version, platform, or environment.

Do not mark a bug fix as `1` merely because correcting the bug changes its output. If the old behavior was outside the supported contract and correct existing usage remains valid, use `2`.

### 2 — compatible and observable

Use `2` when correct existing usage remains valid but the change is observable to a supported consumer, including a caller, type checker, installer, packager, or integrator.

This includes:

- New public functionality.
- Compatible additions or changes to shipped typing information.
- Compatible runtime bug fixes.
- Corrections to behavior outside the supported contract.
- Added environment support.
- Changes to installed files, distributed artifacts, package metadata, or external dependencies.

A packaging or dependency change can therefore be `C2` even when application runtime output is unchanged.

### 3 — unobservable to supported consumers

Use `3` only when supported consumers cannot observe an API, typing, runtime, environment, installation, dependency, metadata, or artifact difference. This includes:

- Internal refactoring with unchanged results.
- Optimizations with unchanged results.
- Tests and internal tooling.
- Documentation-only changes.
- Operational migrations that preserve all supported external behavior and distributed metadata.

Do not choose `3` merely because runtime output is unchanged. If installers, packagers, or integrators can observe the change, use `2`.

## Calculate `Impact`

Set `Impact` to the smallest digit appearing in the bullet markers:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Consider only marker digits. Ignore digits in the version, date, change descriptions, and trailer.

## Sort the bullets

Sort markers in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Keep the supplied order for changes that receive the same marker.

## Final check

Before submitting, verify that:

- The heading matches `## [{version}] - {YYYY-MM-DD}` using the supplied values.
- Every pending change appears exactly once.
- Every bullet begins with a marker in the form `[A1]` through `[C3]`.
- Same-type value or output changes use `B`, not `A`.
- Supported-environment changes use `C`.
- Compatible bug fixes are not marked breaking solely because behavior changed.
- Observable installation, artifact, or dependency changes use `2`, not `3`.
- `Impact` equals the lowest marker digit.
- Bullets follow the required marker order.
- Changes with the same marker retain their supplied order.
- The final line is exactly `<!-- stl-impact: v1 -->`.