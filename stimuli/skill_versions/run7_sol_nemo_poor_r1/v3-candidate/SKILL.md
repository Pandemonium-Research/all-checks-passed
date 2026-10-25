---
name: impact-log
description: Use this document when given a release version, release date, and pending-change list to write one classified, sorted, parser-compatible release-notes entry.
---

# Release notes

## Required output structure

Write exactly one entry:

    ## [{version}] - {YYYY-MM-DD}
    Impact: {smallest marker digit}

    - [{marker}] {pending change}
    - [{marker}] {pending change}

    <!-- stl-impact: v1 -->

Replace the placeholders with the supplied values and classified changes.

Formatting requirements:

- Start the heading with exactly `##`.
- Put the version in square brackets.
- Format the date as `YYYY-MM-DD`.
- Write `Impact:` with a capital `I`.
- Leave one blank line after `Impact:`.
- Start every change with `- ` followed immediately by its marker.
- Leave one blank line between the last bullet and the trailer.
- End with exactly `<!-- stl-impact: v1 -->`.
- Do not add an introduction, summary, additional heading, or footer.

## Classification procedure

Process every pending change as follows:

1. Create exactly one bullet for the change. Do not combine changes or split a change into multiple bullets.
2. Select the marker letter using the letter decision below.
3. Select the marker digit separately using the digit decision below.
4. Combine the letter and digit inside square brackets, such as `[B2]`.
5. Sort all bullets using the required marker order.
6. Set `Impact` to the smallest digit used in any marker.

The letter describes what changed. The digit describes compatibility. Choose them independently.

## Select the letter

Apply these questions in order:

1. Did the public API surface or public type contract change? Use `A`.
2. Otherwise, can existing functionality produce a different runtime result, output, side effect, or error? Use `B`.
3. Otherwise, use `C`.

### A — public API or type contract

Use `A` when the exposed interface itself changes, including:

- Adding or removing a public name.
- Changing a public function, method, or class signature.
- Changing accepted argument types.
- Changing a public return type.
- Adding or changing publicly shipped typing information.

Distinguish a return-type change from a value change:

- If the declared or actual kind of value returned changes, use `A`.
- If the function still returns the same type but the value or content can differ, use `B`.

### B — runtime behavior

Use `B` when the public API and type contract remain unchanged, but calling existing functionality can produce different:

- Return values or rendered output.
- Side effects.
- Exceptions or error handling.
- Other caller-visible runtime behavior.

Runtime bug fixes normally use `B`, not `A`. A changed result does not make a change `A` unless the public interface or type contract also changed.

### C — non-API and non-runtime work

Use `C` when neither `A` nor `B` applies, including:

- Internal refactoring.
- Performance work with identical supported results.
- Build, packaging, installation, artifact, or dependency changes.
- Supported-language, platform, or environment changes.
- Tooling, tests, or documentation changes.

Dropping a supported language, platform, or environment uses `C1`. It is breaking, but it does not change the package’s public API.

## Select the digit

Apply these questions independently of the letter:

1. Can previously supported, correct usage stop working or have a documented result changed? Use `1`.
2. Otherwise, is the change observable to a supported consumer? Use `2`.
3. Otherwise, use `3`.

Supported consumers include callers, type checkers, installers, packagers, and integrators.

### 1 — breaking

Use `1` when previously supported, correct usage can become incompatible, including:

- Removing public functionality.
- Making an incompatible signature or type-contract change.
- Changing behavior that was part of the documented contract.
- Dropping a supported language version, platform, or environment.

A behavior change may therefore be `B1`.

Do not use `1` solely because a bug fix changes previous buggy behavior. If the old behavior was outside the supported contract and correct existing usage remains valid, use `2`.

### 2 — compatible and observable

Use `2` when correct existing usage remains valid but a supported consumer can observe the change, including:

- New public functionality.
- Compatible additions or changes to shipped typing information.
- Compatible runtime fixes.
- Corrections to behavior outside the supported contract.
- Added environment support.
- Changes to installed files, package metadata, artifacts, or external dependencies.
- Other packaging or installation changes visible to installers or integrators.

Observable does not mean only runtime-observable. A dependency that becomes bundled, external, added, removed, or replaced is normally `C2`, even when application output is unchanged.

### 3 — unobservable to supported consumers

Use `3` only when supported consumers cannot observe an API, typing, runtime, environment, installation, dependency, metadata, or artifact difference, including:

- Internal refactoring with unchanged results.
- Optimizations with unchanged results.
- Tests and internal tooling.
- Documentation-only changes.
- Operational migrations that preserve all supported external behavior and distributed metadata.

Do not choose `3` merely because runtime output is unchanged.

## Calculate `Impact`

Use only the digits in the bullet markers:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore digits in the version, date, change descriptions, and trailer.

## Sort the bullets

Use this exact marker order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

When multiple changes have the same marker, retain their order from the supplied pending-change list.

## Final check

Before submitting, verify all of the following:

- The heading contains the supplied version and date in the required format.
- Every pending change appears exactly once.
- Every bullet begins with a marker from `[A1]` through `[C3]`.
- Public return-type changes use `A`; same-type value or output changes use `B`.
- Supported-environment changes use `C`.
- Compatible bug fixes are not marked breaking solely because behavior changed.
- Observable dependency, installation, metadata, or artifact changes use `2`, not `3`.
- `Impact` is the smallest digit in the markers.
- Bullets follow the exact marker order.
- Equal-marker bullets retain their supplied order.
- The final line is exactly `<!-- stl-impact: v1 -->`.