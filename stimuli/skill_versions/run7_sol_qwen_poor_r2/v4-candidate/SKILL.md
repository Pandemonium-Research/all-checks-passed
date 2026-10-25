---
name: impact-log
description: Use this guide to convert a release version, date, and list of pending changes into a classified, sorted release-notes entry with an Impact value and parser trailer.
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

Include every pending change exactly once. Do not combine separate changes or split one change into multiple bullets.

Use this exact format:

`- [LD] Description of the change.`

`L` is the surface letter and `D` is the impact digit. Choose them independently.

### Choose the letter

Apply these rules in order and stop at the first match:

1. If the public API or public type contract changes, use `A`.
2. Otherwise, if the observable runtime behavior of an existing public operation changes, use `B`.
3. Otherwise, use `C`.

#### Use `A` for public-interface changes

This includes:

- Adding, removing, or renaming an exported name.
- Changing a public function or method signature.
- Widening or narrowing accepted argument types.
- Changing a public return type.
- Adding or changing information consumed by type checkers.

A compatible API addition still uses `A`. A newly accepted argument type also uses `A`, even though it affects runtime behavior.

#### Use `B` for runtime-behavior changes

Use `B` only when the public interface is unchanged but an existing public operation has a different observable result, error, side effect, or performance characteristic.

Runtime bug fixes and observable runtime performance improvements normally use `B`.

#### Use `C` for all other changes

Use `C` when neither the public API nor the behavior of an existing public operation changes. This includes:

- Internal refactoring or caching with unchanged public results and signatures.
- Replacing, removing, or vendoring an internal dependency without changing supported behavior.
- Tests, documentation, CI, and tooling changes.
- Packaging, build-system, distribution, platform-support, and installation-support changes.

Packaging and build changes always use letter `C`, including changes that add or remove a supported runtime, platform, artifact, or installation method.

### Choose the digit

Judge compatibility against documented, supported, and intended behavior. Accidental buggy behavior is not a compatibility promise.

Apply these rules in order and stop at the first match:

1. If supported behavior is removed or incompatibly changed so users must change code, configuration, or a supported workflow, use `1`.
2. Otherwise, if the change adds a supported capability or provides an observable improvement, use `2`.
3. Otherwise, use `3`.

#### Use `1` for breaking changes

This includes:

- Removing or renaming a public API.
- Narrowing supported inputs.
- Incompatibly changing the intended meaning or result of a supported operation.
- Removing a supported runtime, platform, artifact, or installation method.

Do not use `1` merely because a result changes. If the old result was faulty and the new result restores intended behavior while valid existing usage remains supported, use `2`.

#### Use `2` for compatible, meaningful changes

This includes:

- Adding a public API.
- Widening accepted inputs.
- Adding public type information.
- Correcting faulty runtime behavior.
- Improving observable runtime performance.
- Adding support for a runtime, platform, artifact, or installation method.

#### Use `3` for changes without supported or observable effect

This includes:

- Internal implementation work with unchanged public results and signatures.
- Replacing or vendoring an internal dependency without changing supported behavior.
- Reorganizing tests.
- Updating documentation.
- Migrating packaging or build configuration without changing installation support.

Implementation effort alone does not justify digit `2`.

### Common marker combinations

- `A1`: Breaking public API or type-contract change.
- `A2`: Compatible public API or type-contract addition.
- `B1`: Incompatible change to intended runtime behavior with no API change.
- `B2`: Compatible runtime fix or observable performance improvement.
- `C1`: Removal of supported runtime, platform, artifact, or installation support.
- `C2`: Addition of supported runtime, platform, artifact, or installation support.
- `C3`: Internal, dependency, documentation, test, tooling, or packaging work with no supported or observable effect.

## 3. Sort the bullets

Sort bullets by their complete marker:

1. Letter: `A`, then `B`, then `C`.
2. Within each letter: `1`, then `2`, then `3`.

Keep separate changes as separate bullets when they have the same marker.

## 4. Write the Impact field

Immediately below the heading, write:

`Impact: D`

Replace `D` with the lowest digit used by any bullet.

For example, an entry containing digits `2` and `3` has `Impact: 2`.

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
- Added installation or platform support uses `C2`.
- Internal dependency or packaging changes use `C3` when supported behavior is unchanged.
- Bullets are sorted by letter and then digit.
- Impact equals the lowest digit present.
- The parser trailer is the final line.