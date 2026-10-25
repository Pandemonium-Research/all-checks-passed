---
name: impact-log
description: Use this document to turn a supplied release version, release date, and pending-change list into one classified, sorted, parser-compatible release notes entry.
---

# Release notes

Produce exactly one entry with this structure:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT

- [LETTERDIGIT] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders with the supplied release information. Include every pending change exactly once.

## Procedure

1. Write the supplied version and date exactly as:

   `## [VERSION] - YYYY-MM-DD`

   Keep the version inside square brackets. Do not add other text to the heading.

2. Classify each pending change independently:

   - Choose the letter from the affected surface.
   - Choose the digit from the compatibility effect.

   Classify the change’s complete effect, regardless of whether its implementation is described as internal.

3. Write exactly one bullet per pending change:

   `- [LETTERDIGIT] Change description.`

   Do not combine changes, split a change into multiple bullets, omit the marker’s square brackets, or add a colon after the marker.

4. Sort the bullets in this exact marker order:

   `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

   Preserve the supplied order among bullets with the same marker.

5. Set `Impact` to the numerically smallest digit used by any bullet. Ignore the marker letters and the number of bullets.

6. Leave one blank line after the final bullet, then add this exact trailer as the entry’s final line:

   `<!-- stl-impact: v1 -->`

## Choose the letter

Choose the earliest applicable letter: `A` before `B` before `C`.

### A — Public interface or compatibility contract

Use `A` when the change affects what callers are allowed to import, call, pass, receive by type or shape, type-check, or run in a supported environment.

Use `A` for:

- Adding, removing, renaming, moving, or newly exporting a public name.
- Changing a public function or method signature.
- Broadening or narrowing documented accepted argument types.
- Changing a public return type or return shape.
- Adding or correcting shipped annotations, typing metadata, or typing behavior, including adding `py.typed`.
- Adding or dropping support for a documented Python version or other runtime.

A changed result is not automatically an `A` change. If the signature, accepted inputs, return type, and return shape remain unchanged, classify a result, exception, side-effect, performance, or resource change as `B`.

### B — Observable runtime behavior with an unchanged public interface

Use `B` when callers use the same public interface but can observe a runtime difference.

Use `B` for:

- Correcting an erroneous result or exception.
- Changing output without changing its public type or shape.
- Changing which exception occurs.
- Changing side effects or other runtime behavior.
- Intentionally changing established output or behavior.
- Improving or degrading execution time, import time, memory use, caching, or resource consumption.

A performance or resource change is `B` even when signatures and results are unchanged and the work is described as an internal rewrite. For example, optimizing a loop, deferring an import, or adding, removing, bounding, or replacing a cache is `B` when the change claims a speed, memory, or resource effect.

### C — No caller-visible package effect

Use `C` only when callers cannot observe any difference in the public interface, runtime results, exceptions, side effects, performance, resource use, installation, or supported environments.

Use `C` for:

- Behavior-preserving internal refactors with no claimed performance or resource effect.
- Tests, comments, examples, docstrings, and documentation.
- Tooling and build-system changes.
- Packaging migrations, vendoring, or dependency-layout changes when installation, runtime behavior, and supported environments remain unchanged.
- Distribution metadata or artifacts that do not alter the public compatibility contract.

Do not choose `C` merely because the changed code is internal. If the pending-change description claims faster execution, reduced import time, bounded memory, or another observable effect, choose `B`.

## Choose the digit

Choose the digit independently of the letter. If multiple rules apply, choose the smallest digit: `1` before `2` before `3`.

### 1 — Breaking

Use `1` when previously supported caller code can become invalid, fail, or receive an intentionally incompatible result.

Use `1` for:

- Removing or renaming a public API, even if it was deprecated.
- Narrowing accepted inputs.
- Making a formerly optional argument required.
- Changing a public return type or return shape.
- Dropping a supported runtime.
- Intentionally replacing established behavior or output that callers may rely on.

Do not use `1` for an ordinary bug fix merely because the corrected result differs from the buggy result. A correction that restores the intended contract uses `2`.

### 2 — Compatible and caller-visible

Use `2` when callers can observe or use the change while correct existing caller code remains supported.

Use `2` for:

- Adding a public API or export.
- Broadening accepted inputs.
- Adding or correcting shipped typing information.
- Correcting an erroneous result or exception to match the intended contract.
- Improving observable performance or resource use without changing supported behavior.

### 3 — Unobservable to callers

Use `3` when callers cannot observe a difference in the public interface, runtime behavior, compatibility, performance, resource use, installation, or supported environments.

Documentation, tests, unchanged packaging machinery, and behavior-preserving internal work normally use `3`.

## Classification reference

Use these classifications for common changes:

- New public function or export: `A2`.
- Removed or renamed public function or export: `A1`.
- Broadened accepted argument type: `A2`.
- Narrowed accepted argument type: `A1`.
- Changed public return type or return shape: `A1`.
- Added or corrected shipped typing metadata: `A2`.
- Dropped a supported runtime: `A1`.
- Compatible bug fix with the same interface and return shape: `B2`.
- Intentional incompatible output change with the same interface and return shape: `B1`.
- Observable execution-time, import-time, memory, caching, or resource improvement: `B2`.
- Internal refactor with unchanged behavior and no observable performance effect: `C3`.
- Documentation, examples, or docstring-only change: `C3`.
- Packaging, vendoring, or dependency migration with unchanged installation, behavior, and support: `C3`.

Most changes should produce one of these five markers:

- `A1`: breaking public-interface or compatibility-contract change.
- `A2`: compatible public-interface or compatibility-contract change.
- `B1`: intentionally incompatible runtime behavior change with an unchanged interface.
- `B2`: compatible observable runtime, performance, or resource change.
- `C3`: no caller-visible effect.

Reclassify any proposed `A3`, `B3`, `C1`, or `C2`. An `A` or `B` effect is caller-visible, so it cannot use `3`; a genuine `C` effect is unobservable, so it must use `3`.

## Final check

Before submitting, verify that:

- The heading is exactly `## [VERSION] - YYYY-MM-DD` using the supplied values.
- `Impact` is the smallest digit appearing in any bullet marker.
- Every pending change appears exactly once.
- Every bullet starts with `- [LETTERDIGIT] `.
- No marker is followed by a colon.
- Public interface and compatibility-contract changes use `A`.
- Runtime result, exception, side-effect, performance, and resource changes use `B`.
- Only changes with no caller-visible effect use `C`.
- Breaking changes use `1`, compatible caller-visible changes use `2`, and unobservable changes use `3`.
- Bullets follow the required marker order.
- The trailer appears exactly once and is the final line.