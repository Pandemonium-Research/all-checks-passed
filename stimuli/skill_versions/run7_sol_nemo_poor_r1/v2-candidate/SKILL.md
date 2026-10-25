---
name: impact-log
description: Use this document when given a release version, date, and pending-change list to produce one classified, correctly ordered, parser-compatible release-notes entry.
---

# Release notes

## Required output

Produce exactly one entry:

    ## [{version}] - {YYYY-MM-DD}
    Impact: {lowest marker digit}

    - [{marker}] {pending change}
    - [{marker}] {pending change}

    <!-- stl-impact: v1 -->

Replace only the placeholders. Preserve each pending change’s wording and punctuation.

Formatting requirements:

- Begin the heading with exactly `##`.
- Put the three-part version in square brackets.
- Format the date as `YYYY-MM-DD`.
- Write `Impact:` with a capital `I`.
- Begin every change with `- ` followed immediately by a marker from `[A1]` through `[C3]`.
- Leave one blank line after `Impact:` and one before the trailer.
- End with exactly `<!-- stl-impact: v1 -->`.
- Do not add any other heading, introduction, summary, or footer.

## Classification process

For every pending change:

1. Create exactly one bullet. Never combine changes or split a change.
2. Choose the letter using the letter decision below.
3. Choose the digit separately using the digit decision below.
4. Combine them into one marker, such as `[B2]`.
5. Sort all bullets by marker, preserving supplied order among bullets with the same marker.
6. Set `Impact` to the smallest digit used by any marker.

The letter identifies what kind of thing changed. The digit identifies compatibility. Do not infer one from the other.

## Choose the letter

Apply this decision in order:

1. Did the public API surface or public type contract change? Use `A`.
2. Otherwise, can a call to existing functionality return a different value, produce different output or side effects, or raise a different error? Use `B`.
3. Otherwise, use `C`.

### A — public API or type contract

Use `A` for changes to the exposed interface itself, including:

- Adding or removing a public name.
- Changing a public function, method, or class signature.
- Changing accepted argument types.
- Changing a public return type.
- Adding or changing publicly shipped typing information.

A change in a returned value is not automatically an `A` change. If the public name, signature, and type contract stay the same but runtime results change, use `B`.

### B — runtime behavior

Use `B` when the public API surface and type contract are unchanged, but existing functionality can produce different:

- Return values or rendered output.
- Side effects.
- Exceptions or error handling.
- Other caller-visible runtime behavior.

Runtime bug fixes normally use `B`, not `A`.

### C — non-API and non-runtime work

Use `C` when neither `A` nor `B` applies, including:

- Internal refactoring.
- Performance work whose supported results remain identical.
- Build, packaging, installation, or dependency changes.
- Supported-language, platform, or environment changes.
- Tooling, tests, or documentation changes.

Dropping a supported environment is `C1`, not `A1`: it is breaking, but it does not change the package’s public API surface.

## Choose the digit

Apply this decision independently of the letter:

1. Can previously supported, correct usage stop working or have its documented result changed? Use `1`.
2. Otherwise, is the change observable to users, callers, type checkers, installers, packagers, or other supported consumers? Use `2`.
3. Otherwise, use `3`.

### 1 — breaking

Use `1` for an incompatible change to supported behavior or environments, including:

- Removing public functionality.
- Making an incompatible signature or type-contract change.
- Changing behavior that was part of the documented contract.
- Dropping a supported language version, platform, or environment.

Do not use `1` merely because a bug fix changes what buggy code previously did. If the old behavior was outside the supported contract and correct existing usage remains valid, use `2`.

### 2 — compatible and observable

Use `2` when correct existing usage remains valid but the change is observable. This includes:

- New public functionality.
- New or changed shipped typing information that remains compatible.
- Compatible runtime fixes.
- Corrections to behavior that was outside the supported contract.
- Added environment support.
- Packaging, installation, dependency, or artifact changes visible to installers or integrators, such as changing whether another package is an external dependency.

A non-runtime change can therefore be `C2`.

### 3 — unobservable to supported consumers

Use `3` only when supported consumers cannot observe a functional, API, typing, environment, installation, dependency, or artifact difference. This includes:

- Internal refactoring with unchanged results.
- Unchanged-result optimizations.
- Tests and internal tooling.
- Documentation-only changes.
- Operational or packaging migrations that preserve all supported externally visible behavior and metadata.

Do not classify a change as `3` merely because application runtime output is unchanged. Installation and dependency changes may still be observable and therefore use `2`.

## Calculate `Impact`

Use only the digits in the bullet markers:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore all digits in the version, date, descriptions, and trailer.

## Sort the bullets

Sort by this exact marker order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

For multiple changes with the same marker, retain their order from the supplied pending-change list.

## Final verification

Before submitting, confirm all of the following:

- The heading is exactly `## [{version}] - {YYYY-MM-DD}` with the supplied values.
- Every pending change appears exactly once with its original wording.
- Every bullet begins with a valid marker.
- Value or output changes with an unchanged API/type contract use `B`, not `A`.
- Supported-environment changes use `C`.
- Compatible bug fixes are not marked breaking solely because behavior changed.
- Observable installation, dependency, or artifact changes are not marked `3`.
- `Impact` is the smallest marker digit.
- Bullets follow the required marker order.
- Equal-marker bullets retain their supplied order.
- The final line is exactly `<!-- stl-impact: v1 -->`.