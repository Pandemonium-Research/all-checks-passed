---
name: impact-log
description: Use this document to turn a release version, date, and list of pending changes into one correctly classified, ordered, parser-compatible release-notes entry.
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
- Put the three-part version in square brackets.
- Write the date as `YYYY-MM-DD`.
- Write `Impact:` with a capital `I`.
- Start every change with `- ` followed immediately by a square-bracketed marker such as `[A2]`.
- Put the trailer `<!-- stl-impact: v1 -->` at the bottom exactly as shown, including its spaces.
- Do not add another heading, introduction, summary, or footer.

## Process

For each pending change:

1. Write one bullet. Do not combine changes or split one change into multiple bullets.
2. Select its letter using the letter rules below.
3. Select its digit independently using the digit rules below.
4. Join them inside square brackets, such as `[B2]`.
5. After all bullets are marked, sort them by marker.
6. Set `Impact` to the lowest digit used in the markers.

## Select the letter

Choose the first applicable letter in this order: `A`, then `B`, then `C`.

### A — public API surface

Use `A` when the change affects something the package publicly exposes, including:

- Adding or removing a public name.
- Changing a public function or class signature.
- Changing accepted argument types or public return types.
- Adding or changing publicly shipped typing information.

### B — runtime behavior

Use `B` when the public API surface is unchanged, but calling existing functionality can produce different runtime behavior, output, or errors.

Bug fixes to runtime behavior normally use `B`.

### C — non-API work

Use `C` when neither `A` nor `B` applies, including:

- Internal refactoring or optimization with unchanged results.
- Build or packaging changes.
- Supported-environment changes.
- Tooling, tests, or documentation changes.

The letter and digit are independent. For example, a packaging change may be breaking, compatible, or unobservable.

## Select the digit

Choose the lowest applicable digit.

### 1 — breaking

Use `1` when previously supported, correct usage can stop working or its documented result can change. This includes removals, incompatible contract changes, and dropping a supported environment.

Do not mark a bug fix as `1` merely because correcting the bug changes its output. Use `1` only when the change breaks behavior that was part of the supported contract.

### 2 — compatible and observable

Use `2` for an additive change or compatible fix that users, callers, or type-checking tools can observe while correct existing usage remains valid.

This includes new public functionality and corrections of behavior that was outside the supported contract.

### 3 — unobservable to callers

Use `3` when callers cannot observe a functional or API difference. This includes internal refactoring, unchanged-result optimizations, tests, documentation, and operational migrations that preserve supported behavior.

## Calculate `Impact`

Set `Impact` to the smallest digit appearing in the bullet markers:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Consider only marker digits. Ignore digits in the version, date, change descriptions, and trailer.

## Sort the bullets

Sort markers in this exact ascending order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Keep the supplied order for changes that receive the same marker.

## Final check

Before submitting, verify that:

- The heading matches `## [{version}] - {YYYY-MM-DD}`.
- Every pending change appears exactly once.
- Every bullet begins with a marker in the form `[A1]` through `[C3]`.
- The letter and digit were chosen independently.
- Bug fixes are not automatically classified as breaking.
- `Impact` equals the lowest marker digit.
- Bullets follow the required marker order.
- The final line is exactly `<!-- stl-impact: v1 -->`.