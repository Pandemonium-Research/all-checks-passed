---
name: impact-log
description: Use these instructions when converting a release version, release date, and pending-change list into one classified, sorted, parser-compatible release notes entry.
---

# Release notes

Produce exactly one entry with this structure:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT

- [LETTERDIGIT] Change description.

<!-- stl-impact: v1 -->

Replace every placeholder with the supplied release information. Include every pending change exactly once.

## Procedure

1. Write the supplied version and date exactly as:

   `## [VERSION] - YYYY-MM-DD`

   Keep the version inside square brackets. Do not add other text to the heading.

2. Classify each pending change independently:

   - Choose its letter from the affected-surface rules.
   - Choose its digit from the compatibility rules.

3. Write one bullet per pending change:

   `- [LETTERDIGIT] Change description.`

   Do not combine changes, split a change into multiple bullets, omit the marker’s brackets, or add a colon after the marker.

4. Sort the bullets in this exact marker order:

   `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

   When multiple bullets have the same marker, preserve their order from the pending-change list.

5. Set `Impact` to the numerically smallest digit used by any bullet. Ignore the marker letters and the number of bullets.

6. Leave one blank line after the final bullet. Then add this exact trailer as the entry’s final line:

   `<!-- stl-impact: v1 -->`

## Choose the letter: what surface changed?

Choose the earliest applicable letter: `A` before `B` before `C`.

### A — Public interface or compatibility contract

Use `A` when the change affects what callers can import, call, pass, receive by type or shape, type-check, or run in a supported environment.

Use `A` for:

- Adding, removing, renaming, or relocating a public export.
- Changing a public function or method signature.
- Broadening or narrowing documented accepted argument types.
- Changing a public return type or return shape.
- Adding or correcting shipped annotations, typing metadata, or typing behavior, including adding `py.typed`.
- Adding or dropping support for a documented Python version or other runtime.

Do not use `A` merely because users can observe the change. If callers use the same public interface and only the result, exception, side effect, or performance changes, use `B`.

### B — Observable runtime behavior with an unchanged public interface

Use `B` when the public interface remains unchanged but callers can observe a runtime difference.

Use `B` for:

- Correcting an erroneous result.
- Changing a returned value without changing its public type or shape.
- Fixing or changing an exception.
- Changing side effects or other runtime behavior.
- Intentionally changing established output or behavior.
- Improving or degrading import time, execution time, memory use, or caching performance.

A stated performance improvement is `B` even when signatures and results are unchanged. A caching change that claims a speed, memory, or resource benefit is therefore `B`; a purely internal cache refactor with no claimed observable effect is `C`.

### C — No caller-visible package effect

Use `C` when neither the public interface nor caller-observable runtime behavior changes.

Use `C` for:

- Behavior-preserving internal refactors with no observable performance effect.
- Internal implementation changes that do not affect results, exceptions, side effects, or resource use.
- Tests, comments, examples, docstrings, and documentation.
- Tooling and build-system changes.
- Packaging migrations or dependency-layout changes when installation, supported environments, and runtime behavior remain unchanged.
- Distribution metadata or artifacts that do not alter the public compatibility contract.

## Choose the digit: how compatible is the change?

Choose the digit independently of the letter. If multiple rules apply, choose the smallest digit: `1` before `2` before `3`.

### 1 — Breaking

Use `1` when a supported caller can become invalid, fail, or receive an intentionally incompatible result.

Use `1` for:

- Removing or renaming a public API.
- Narrowing accepted inputs.
- Making a formerly optional argument required.
- Changing a public return type or return shape.
- Dropping a supported runtime.
- Intentionally replacing established behavior or output that callers may rely on.

Removing an already deprecated API is still breaking.

Do not classify an ordinary bug fix as `1` merely because the corrected result differs from the buggy result. Use `2` when the change restores the intended contract.

### 2 — Compatible and caller-visible

Use `2` when callers can observe or use the change while correct existing caller code remains supported.

Use `2` for:

- Adding a public API.
- Broadening accepted inputs.
- Adding or correcting shipped typing information.
- Fixing an incorrect result or exception to match the intended contract.
- Improving observable performance without changing supported behavior.

### 3 — Unobservable to callers

Use `3` when callers cannot observe a difference in the public interface, runtime behavior, compatibility, performance, installation, or supported environments.

Documentation, tests, unchanged packaging machinery, and behavior-preserving internal work normally use `3`.

## Classification reference

- New public function: `A2`.
- Removed or renamed public function: `A1`.
- Broadened accepted argument type: `A2`.
- Narrowed accepted argument type: `A1`.
- Changed public return type or shape: `A1`.
- Added or corrected shipped typing metadata: `A2`.
- Dropped a supported runtime: `A1`.
- Compatible bug fix with the same interface: `B2`.
- Intentional incompatible output change with the same interface: `B1`.
- Observable speed, import-time, memory, or caching improvement: `B2`.
- Internal refactor with unchanged behavior and no observable performance effect: `C3`.
- Documentation, examples, or docstring-only change: `C3`.
- Packaging or dependency migration with unchanged installation and support: `C3`.

## Final check

Before submitting, verify that:

- The heading is exactly `## [VERSION] - YYYY-MM-DD` using the supplied values.
- `Impact` is the smallest digit appearing in any bullet marker.
- Every pending change appears exactly once.
- Every bullet starts with `- [LETTERDIGIT] `.
- No marker is followed by a colon.
- Public interface and compatibility-contract changes use `A`.
- Runtime behavior and observable performance changes use `B`.
- Changes with no caller-visible effect use `C`.
- Breaking changes use digit `1`, compatible caller-visible changes use `2`, and unobservable changes use `3`.
- Bullets follow the required marker order.
- The trailer appears exactly once and is the final line.