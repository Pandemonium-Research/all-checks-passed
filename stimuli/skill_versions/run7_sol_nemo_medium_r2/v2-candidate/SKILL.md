---
name: impact-log
description: Use this guide when converting a supplied release version, date, and pending-change list into one classified, ordered, parser-compatible release-notes entry.
---

# Release notes

Produce exactly one entry. Include every pending change once and only once.

The entry must have this exact layout, with no blank lines:

## [VERSION] - YYYY-MM-DD
Impact: N
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace each placeholder with the supplied information. Every change-description sentence must end with a period.

## 1. Write the heading

Use exactly:

`## [VERSION] - YYYY-MM-DD`

- Keep the literal `##`.
- Put the supplied three-part version in square brackets.
- Copy the supplied date in `YYYY-MM-DD` format.
- Put `Impact: N` immediately on the next line.

## 2. Classify every change

Assign each change one letter and one digit. Classify the effect of the change, not the implementation technique used to make it.

### Choose the letter

Use the first applicable letter:

1. `A` — The published public API shape changes.

   This includes exported names, public availability, function or method signatures, accepted parameter types, return types, and other published types.

   Examples include adding or removing an exported helper, adding a parameter, or widening the documented inputs a parameter accepts.

2. `B` — An existing runtime operation changes, but its public API shape does not.

   This includes changed results, errors, parsing rules, performance, import time, memory use, and caching behavior.

   A bug fix that changes an existing call's result is `B`, not `A`. A cache or import change with an observable performance or memory effect is also `B`, even when results and signatures stay unchanged.

3. `C` — The change concerns packaging or project support work rather than an existing runtime operation.

   This includes installation, dependencies, distribution artifacts, typing metadata, build configuration, development tooling, tests, and documentation.

If several letters apply, choose the earliest: `A` before `B` before `C`.

### Choose the digit independently

Use the first applicable digit:

1. `1` — Breaking or behavior-changing for existing supported use.

   Use `1` when previously supported caller code can fail, require modification, raise a different error, or receive a different result. This includes bug fixes that intentionally change the result of an existing call.

2. `2` — Compatible and externally observable.

   Use `2` for new compatible capability, broader accepted inputs, installation or packaging fixes, new shipped artifacts or metadata, dependency-distribution changes, or observable performance or memory improvements that preserve existing results.

3. `3` — Not observable to package callers.

   Use `3` for documentation, tests, development tooling, refactoring, or build/configuration migration that does not alter installation, shipped artifacts, public behavior, performance, or memory use.

Do not assign `3` merely because a change is described as “internal.” If callers can observe its effect, use `1` or `2`.

If several digits apply, choose the lowest: `1` before `2` before `3`. When genuinely uncertain, choose the lower digit.

## 3. Write the bullets

Use exactly this syntax for every change:

`- [CODE] Description.`

Requirements:

- Begin with a hyphen followed by one space.
- Put the two-character code inside square brackets.
- Put one space after the closing bracket.
- End the description with a period.
- Do not use `A1 Description`, `A1: Description`, or `- A1 Description`.
- Do not omit, combine, or duplicate pending changes.

## 4. Sort the bullets

Sort by this fixed code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes have the same code, keep their original order from the pending-change list.

## 5. Calculate the impact summary

Set `N` to the lowest digit appearing in any bullet code.

- Any digit `1` means `Impact: 1`.
- Otherwise, any digit `2` means `Impact: 2`.
- Otherwise, use `Impact: 3`.

Ignore the letters when calculating the summary. Never place an impact number in the summary that does not appear in at least one bullet code.

## 6. Add the trailer

Put this exact line immediately after the final bullet:

`<!-- stl-impact: v1 -->`

The trailer must be the final line. Do not insert a blank line before it, and do not put any text or blank line after it.

Before submitting, verify:

- There is exactly one release heading.
- `Impact: N` is directly below the heading.
- Every pending change appears in exactly one bullet.
- Every bullet uses `- [CODE] Description.`
- The codes follow the required sort order.
- `N` equals the lowest bullet-code digit.
- There are no blank lines in the entry.
- The trailer is the final line.