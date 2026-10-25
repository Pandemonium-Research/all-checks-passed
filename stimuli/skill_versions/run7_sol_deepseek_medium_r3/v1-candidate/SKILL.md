---
name: impact-log
description: Use this skill to turn a release version, date, and list of pending changes into a correctly classified, sorted, and parser-compatible release-notes entry in the project's impact-log format.
---

# Release notes

Create one release entry using this exact structure:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Description of change.
- [CODE] Description of change.

<!-- stl-impact: v1 -->

Replace `VERSION` and `YYYY-MM-DD` with the supplied version and date. Use the supplied three-part version number exactly. The trailer comment must be the final line of the entry.

Write one bullet for each pending change. Start every bullet with an impact code consisting of one letter and one digit, such as `[A2]`. Classify the letter and digit independently using the rules below.

## Choose the letter

Use the first matching category:

1. Use `A` when the public API surface changes. This includes:

   - Adding, removing, or renaming an exported name.
   - Changing a public function or method signature.
   - Broadening or narrowing accepted public argument types.
   - Changing a documented return type.

2. Use `B` when an existing public call keeps the same API surface but its runtime behavior changes. This includes changes to returned values, exceptions, side effects, normalization, formatting, or other semantics.

3. Use `C` when no supported public API or runtime behavior changes. This includes internal refactoring or optimization with unchanged results, plus build, packaging, tooling, test, and documentation changes.

Classify environment and installation-support changes, such as changing the supported Python versions, as `C` because they concern packaging or project support rather than exported names or signatures.

Do not classify a value-only behavior change as `A` merely because it occurs in a public function. Use `A` for changes to the public surface or types and `B` for changed behavior behind an unchanged surface.

## Choose the digit

Use the first matching category:

1. Use `1` if a previously supported, successful use can now fail, require caller changes, return a different value or type, or produce different side effects. Removals, incompatible signature changes, narrowed input support, and changed results for previously working inputs are `1`.

2. Use `2` if the change is compatible and adds or repairs capability without altering previously successful supported uses. New APIs, broadened accepted inputs, and fixes for inputs that previously failed or were unsupported are `2`.

3. Use `3` if supported callers cannot observe a functional difference. Internal rewrites, tests, documentation, and maintenance-only changes are normally `3`.

Do not assign `1` merely because the letter is `A`. For example, adding a public API is additive and therefore uses digit `2`. Likewise, do not assign `2` merely because a change is described as a fix: if it changes the result for an input that previously completed successfully, use digit `1`.

Base the classification on the stated effects of the change. Do not invent hypothetical incompatibilities that are not present in the pending-change description.

## Compute and order the entry

Set the `Impact` value to the lowest digit used by any bullet in the entry. For example, if the bullets use digits `2`, `2`, and `3`, write `Impact: 2`.

Sort bullets by their complete codes in ascending order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple bullets have the same code, retain their original relative order.

Write each description as a concise sentence explaining what changed and, when relevant, how callers are affected. End each bullet with a period. Do not add prose, headings, or comments outside the required entry structure.