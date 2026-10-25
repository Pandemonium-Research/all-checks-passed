---
name: impact-log
description: Use these instructions to turn a supplied release version, release date, and pending-change list into one classified, sorted, parser-compatible release notes entry.
---

# Release notes

Produce exactly one entry in this form:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT

- [LETTERDIGIT] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders with the supplied values. Include every pending change exactly once.

## Procedure

1. Write the heading exactly as:

   `## [VERSION] - YYYY-MM-DD`

   Use the supplied version inside square brackets and the supplied date. Add no other heading text.

2. Classify each pending change independently:

   - Choose the letter from the surface affected.
   - Choose the digit from the compatibility effect.

   Classify the complete effect described, not whether the implementation is called internal.

3. Write exactly one bullet per pending change:

   `- [LETTERDIGIT] Change description.`

   Do not combine changes, split a change into multiple bullets, omit the marker’s brackets, or put a colon after the marker.

4. Sort bullets in this exact order:

   `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

   Preserve the pending-list order among bullets with the same marker.

5. Set `Impact` to the numerically smallest digit used in any bullet marker. Ignore the letters and the number of changes.

6. Leave one blank line after the final bullet. Add this exact trailer as the final line:

   `<!-- stl-impact: v1 -->`

## Choose the letter

If more than one letter applies, choose the earliest: `A` before `B` before `C`.

### A — Public interface or compatibility contract

Use `A` when the change affects what callers can import, call, pass, receive by type or shape, type-check, or run in a supported environment.

This includes:

- Adding, removing, renaming, moving, or newly exporting a public name.
- Changing a public function or method signature.
- Broadening or narrowing documented accepted argument types.
- Changing a public return type or return shape.
- Adding or correcting shipped annotations, typing metadata, or typing behavior, including `py.typed`.
- Adding or dropping support for a documented Python version or other runtime.

A changed return value is not automatically `A`. If the signature, accepted inputs, return type, and return shape remain unchanged, classify a result, exception, side-effect, or performance change as `B`.

### B — Observable runtime effect with an unchanged public interface

Use `B` when callers use the same public interface but can observe a runtime difference.

This includes:

- Correcting an erroneous result or exception.
- Changing output without changing its public type or shape.
- Changing which exception occurs.
- Changing side effects or other runtime behavior.
- Intentionally changing established output or behavior.
- Improving or degrading execution time, import time, memory use, caching, or resource consumption.

Performance and resource effects are `B` even when results and signatures are unchanged or the implementation is described as internal. For example, an optimized loop, deferred import, bounded cache, or new cache is `B` when it changes speed or resource use.

### C — No caller-visible package effect

Use `C` only when callers cannot observe a difference in the public interface, runtime behavior, performance, resource use, installation, or supported environments.

This includes:

- Behavior-preserving internal refactors with no stated performance or resource effect.
- Tests, comments, examples, docstrings, and documentation.
- Tooling and build-system changes.
- Packaging migrations, vendoring, or dependency-layout changes with no stated effect on installation, runtime behavior, or supported environments.
- Distribution metadata or artifacts that do not change the compatibility contract.

Do not choose `C` merely because code is internal. If the description states or clearly entails faster execution, reduced import time, bounded memory, or another observable effect, choose `B`.

## Choose the digit

Choose the digit independently of the letter. If more than one digit applies, choose the smallest: `1` before `2` before `3`.

### 1 — Breaking

Use `1` when previously supported caller code can become invalid, fail, or receive an intentionally incompatible result.

This includes:

- Removing or renaming a public API, even if it was deprecated.
- Narrowing accepted inputs.
- Making a formerly optional argument required.
- Changing a public return type or return shape.
- Dropping a supported runtime.
- Intentionally replacing established behavior or output that callers may rely on.

Do not use `1` for an ordinary bug fix merely because the corrected result differs from the buggy result. A correction that restores the intended contract uses `2`.

### 2 — Compatible and caller-visible

Use `2` when callers can observe or use the change while supported correct caller code remains valid.

This includes:

- Adding a public API or export.
- Broadening accepted inputs.
- Adding or correcting shipped typing information.
- Correcting an erroneous result or exception to match the intended contract.
- Improving observable performance or resource use without changing supported behavior.

### 3 — Unobservable to callers

Use `3` when callers cannot observe any difference in interface, behavior, compatibility, performance, resource use, installation, or supported environments.

Documentation, tests, unchanged packaging machinery, dependency-layout work, and behavior-preserving internal changes normally use `3`.

## Classification reference

- New public API or export: `A2`.
- Removed or renamed public API: `A1`.
- Broadened accepted argument type: `A2`.
- Narrowed accepted argument type: `A1`.
- Changed public return type or shape: `A1`.
- Added or corrected shipped typing metadata: `A2`.
- Dropped a supported runtime: `A1`.
- Compatible bug fix with the same interface and return shape: `B2`.
- Intentional incompatible output change with the same interface and return shape: `B1`.
- Observable speed, import-time, memory, caching, or resource improvement: `B2`.
- Internal refactor with unchanged behavior and no observable performance effect: `C3`.
- Documentation, examples, or docstring-only change: `C3`.
- Packaging, vendoring, or dependency migration with unchanged installation, behavior, and support: `C3`.

Most entries use `A1`, `A2`, `B1`, `B2`, and `C3`. Recheck any `A3`, `B3`, `C1`, or `C2`: an `A` or `B` effect is caller-visible, while a genuine `C` effect is unobservable.

## Final check

Before submitting, verify that:

- The heading exactly matches `## [VERSION] - YYYY-MM-DD` with the supplied values.
- `Impact` is the smallest digit appearing in any bullet marker.
- Every pending change appears exactly once.
- Every bullet starts with `- [LETTERDIGIT] `.
- No marker is followed by a colon.
- Public interface and compatibility-contract changes use `A`.
- Runtime results, exceptions, side effects, performance, and resource changes use `B`.
- Only changes with no caller-visible effect use `C`.
- Breaking changes use `1`, compatible caller-visible changes use `2`, and unobservable changes use `3`.
- Bullets follow the required marker order.
- The trailer appears exactly once and is the final line.