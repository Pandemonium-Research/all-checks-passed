---
name: impact-log
description: Use this document to turn a release version, release date, and pending-change list into one classified, sorted, parser-compatible release notes entry.
---

# Release notes

Produce exactly one entry in this form:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT

- [LETTERDIGIT] Change description.

<!-- stl-impact: v1 -->

Replace all placeholders with the supplied release information. Include one bullet for every pending change.

## Procedure

1. Write the supplied version and date exactly as:

   `## [VERSION] - YYYY-MM-DD`

   Keep the version inside square brackets. Do not add text to the heading.

2. Classify each pending change independently:

   - Choose its letter from the affected-surface rules below.
   - Choose its digit from the compatibility rules below.

3. Write exactly one bullet per pending change:

   `- [LETTERDIGIT] Change description.`

   Do not combine changes, split a change into multiple bullets, add a colon after the marker, or omit the marker’s square brackets.

4. Sort all bullets by marker in this order:

   `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

   For bullets with the same marker, preserve their order from the supplied pending-change list.

5. Set `Impact` to the smallest digit used by any bullet. Ignore the letters and the number of bullets.

6. Leave one blank line after the final bullet, then add this exact trailer as the entry’s final line:

   `<!-- stl-impact: v1 -->`

## Choose the letter: what surface changed?

Choose the earliest applicable letter: `A` before `B` before `C`.

### A — Public interface or compatibility contract

Use `A` when the change affects what callers can import, call, pass, receive by type, or run in a supported environment. This includes:

- Adding, removing, renaming, or relocating a public export.
- Changing a public function or method signature.
- Changing documented accepted argument types.
- Changing a public return type or return shape.
- Changing shipped annotations, typing metadata, or typing behavior.
- Adding or removing support for a Python version or other documented runtime.

A change is not `A` merely because users can notice it. If the public interface stays the same but a call produces different results, exceptions, side effects, or performance, use `B`.

### B — Observable runtime behavior with an unchanged public interface

Use `B` when callers use the same public interface but can observe a runtime difference. This includes:

- Changing a returned value without changing its public type or shape.
- Fixing an incorrect result or exception.
- Changing which exception occurs.
- Changing side effects or other documented behavior.
- Improving or degrading import time, execution time, memory use, or caching performance.

Use `B` for observable performance changes even when results and signatures are identical.

### C — No caller-visible package effect

Use `C` when neither the public interface nor caller-observable runtime behavior changes. This includes:

- Behavior-preserving internal refactors.
- Internal implementation changes with no observable performance effect.
- Tests, comments, examples, docstrings, and documentation.
- Tooling and build-system changes.
- Packaging or dependency-layout changes when installation and supported environments remain unchanged for users.
- Distribution metadata or artifacts that do not change the public compatibility contract.

## Choose the digit: how compatible is the change?

Choose the digit independently of the letter. If multiple rules apply, choose the lowest digit: `1` before `2` before `3`.

### 1 — Breaking

Use `1` when previously supported caller code can become invalid, fail, or intentionally produce incompatible results. This includes:

- Removing or renaming a public API.
- Narrowing accepted inputs.
- Making a formerly optional argument required.
- Changing a public return type or return shape.
- Dropping a supported runtime.
- Intentionally changing established behavior in a way callers may rely on.

A deprecation does not prevent removal from being breaking.

### 2 — Compatible and caller-visible

Use `2` when callers can observe or use the change, but correct existing caller code remains supported. This includes:

- Adding a public API.
- Broadening accepted inputs.
- Adding or correcting shipped typing information.
- Fixing a bug so the implementation follows its intended contract.
- Fixing an erroneous exception or result.
- Improving observable performance without changing supported behavior.

A bug fix normally uses `2`, even though affected calls may now return a corrected result. Use `1` instead only when the change intentionally replaces previously supported or established behavior.

### 3 — Unobservable to callers

Use `3` when callers cannot observe a public-interface, runtime-behavior, compatibility, or performance difference. Documentation, tests, unchanged installation machinery, and behavior-preserving internal work normally use `3`.

## Common classifications

- New public function: `A2`.
- Removed public function: `A1`.
- Broadened accepted argument type: `A2`.
- Changed return type or shape: `A1`.
- Added or corrected shipped typing metadata: `A2`.
- Dropped supported Python version: `A1`.
- Compatible bug fix with the same interface: `B2`.
- Intentional incompatible output change with the same interface: `B1`.
- Observable speed, import-time, memory, or caching improvement: `B2`.
- Internal refactor with unchanged behavior and no observable performance change: `C3`.
- Documentation or docstring-only change: `C3`.
- Packaging migration with unchanged installation and support: `C3`.

## Final check

Before submitting, verify that:

- The heading is exactly `## [VERSION] - YYYY-MM-DD` with supplied values.
- `Impact` is the smallest digit appearing in any marker.
- Every pending change appears exactly once.
- Every bullet starts with `- [LETTERDIGIT] `.
- No marker is followed by a colon.
- Interface changes are `A`, observable behavior or performance changes are `B`, and unobservable changes are `C`.
- Breaking changes are digit `1`, compatible caller-visible changes are digit `2`, and unobservable changes are digit `3`.
- Bullets follow the required marker order.
- The trailer is present exactly once and is the final line.