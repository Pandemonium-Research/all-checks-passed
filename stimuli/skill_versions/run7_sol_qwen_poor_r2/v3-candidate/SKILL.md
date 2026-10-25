---
name: impact-log
description: Use this guide to turn a release version, date, and list of pending changes into a classified, sorted release-notes entry with an Impact value and parser trailer.
---

# Release notes

Follow these steps for every release.

## 1. Write the heading

Use this exact pattern:

`## [VERSION] - YYYY-MM-DD`

Requirements:

- Use a second-level Markdown heading: `##`.
- Put the three-part version number in square brackets.
- Separate the version and date with ` - `.
- Write the date with a four-digit year, two-digit month, and two-digit day.

## 2. Create one bullet per pending change

Include every pending change exactly once. Do not merge separate changes or split one change into multiple bullets.

Use this exact format:

`- [LD] Description of the change.`

`L` is the surface letter. `D` is the impact digit. Classify them independently.

### Choose the letter

Ask these questions in order. Stop at the first match.

1. Does the change affect the public API or public type contract? Use `A`.
2. Otherwise, does it change the observable runtime behavior of an existing public operation? Use `B`.
3. Otherwise, use `C`.

Use `A` for any public-interface change, including:

- Adding, removing, or renaming an exported name.
- Changing a public function or method signature.
- Widening or narrowing accepted argument types.
- Changing a public return type.
- Adding or changing information consumed by type checkers.

A compatible public API addition is still `A`. A newly accepted argument type is also `A`, even though it affects runtime behavior.

Use `B` only when the public interface is unchanged but an existing public operation has a different observable result, error, side effect, or performance characteristic. Runtime bug fixes normally use `B`.

Use `C` when neither the public API nor the behavior of existing public operations changes. This includes:

- Internal refactoring or caching with unchanged public results and signatures.
- Dependency or implementation substitutions that do not alter supported installation or runtime behavior.
- Tests, documentation, CI, and tooling changes.
- Packaging or build-system changes.

Packaging and build changes use `C` even when they add or remove support for an installation method, artifact, platform, or runtime.

### Choose the digit

Judge compatibility against documented, supported, and intended behavior. Do not treat accidental buggy behavior as a compatibility promise.

Ask these questions in order. Stop at the first match.

1. Does the change remove or incompatibly alter supported behavior, requiring users to change code, configuration, or a supported workflow? Use `1`.
2. Otherwise, does it add a supported capability or provide an observable improvement? Use `2`.
3. Otherwise, use `3`.

Use `1` for breaking changes, including:

- Removing or renaming a public API.
- Narrowing supported inputs.
- Incompatibly changing the intended meaning or result of a supported operation.
- Removing a supported runtime, platform, artifact, or installation method.

A different result is not automatically breaking. If a change corrects unintended behavior and valid existing usage remains supported, it is a compatible fix and uses `2`.

Use `2` for compatible, meaningful changes, including:

- Adding a public API.
- Widening accepted inputs.
- Adding public type information.
- Correcting faulty runtime behavior.
- Improving observable runtime performance.
- Adding support for a runtime, platform, artifact, or installation method.

Use `3` when there is no new supported capability and no public or caller-observable improvement, including:

- An internal implementation change with unchanged results and signatures.
- Replacing or vendoring an internal dependency without changing supported behavior.
- Reorganizing tests.
- Updating documentation.
- Migrating build or packaging configuration without changing installation support.

Implementation effort alone does not justify `2`.

Common combinations include:

- `A1`: breaking public API change.
- `A2`: compatible public API or type-contract addition.
- `B1`: incompatible change to intended runtime behavior with no API change.
- `B2`: compatible runtime fix or observable performance improvement.
- `C1`: removal of supported build, platform, artifact, or installation support.
- `C2`: addition of supported build, platform, artifact, or installation support.
- `C3`: internal, documentation, test, tooling, or packaging work with no supported or observable effect.

## 3. Sort the bullets

Sort bullets by their complete marker:

1. Letter: `A`, then `B`, then `C`.
2. Within each letter: `1`, then `2`, then `3`.

Keep separate changes as separate bullets when they share a marker.

## 4. Write the Impact field

Immediately below the heading, write:

`Impact: D`

Replace `D` with the lowest digit used by any bullet.

For example, if the entry contains digits `2` and `3`, its Impact is `2`.

Impact is not:

- The number of changes.
- The most frequent digit.
- Necessarily the digit on the first bullet.

## 5. Add the trailer

After the final bullet, add this exact line:

`<!-- stl-impact: v1 -->`

The trailer must be the final line of the entry.

## Final structure

Use this order:

1. Heading
2. `Impact` field
3. Sorted change bullets
4. Parser trailer

Before finishing, verify:

- The version and date match the supplied release.
- Every pending change appears exactly once.
- Every bullet starts with a bracketed two-character marker.
- Public API additions and widened inputs use `A2`, not `A1` or `B2`.
- Compatible bug fixes normally use `B2`, not `B1`.
- Internal changes with unchanged behavior use digit `3`.
- Added installation or platform support uses `C2`; an internal packaging migration uses `C3`.
- Bullets are sorted by letter and then digit.
- Impact equals the lowest digit present.
- The parser trailer is the final line.