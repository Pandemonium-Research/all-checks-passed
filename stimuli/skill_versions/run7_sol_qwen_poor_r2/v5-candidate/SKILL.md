---
name: impact-log
description: Use this guide when converting a release version, release date, and list of pending project changes into a classified, sorted release-notes entry with an Impact value and parser trailer.
---

# Release notes

Follow this procedure for every release.

## 1. Write the heading

Use this exact pattern:

`## [VERSION] - YYYY-MM-DD`

Requirements:

- Use a second-level Markdown heading.
- Put the supplied version in square brackets.
- Separate the version and date with ` - `.
- Preserve the supplied version and date exactly.

## 2. Create one bullet per pending change

Include every pending change exactly once. Do not combine separate changes or split one change into multiple bullets.

Use this exact format:

`- [LD] Description of the change.`

`L` is the surface letter. `D` is the impact digit. Choose them independently using the rules below.

### Choose the letter

Apply these rules in order and stop at the first match:

1. Use `A` if the public API or public type contract changes.
2. Otherwise, use `B` if an existing public operation has different observable runtime behavior.
3. Otherwise, use `C`.

#### `A`: Public interface or type contract

Use `A` for changes such as:

- Adding, removing, or renaming an exported name.
- Changing a public function or method signature.
- Widening or narrowing accepted argument types.
- Changing a public return type.
- Adding or changing information consumed by type checkers.

A compatible API addition uses `A`. A newly accepted input type also uses `A`, even though accepting it affects runtime behavior.

#### `B`: Existing runtime behavior

Use `B` only when the public interface is unchanged but an existing public operation changes its observable result, error, side effect, or performance.

Compatible runtime bug fixes and observable performance improvements normally use `B`.

#### `C`: Internal, project, or distribution surface

Use `C` for changes outside the public API and existing-operation runtime behavior, including:

- Internal refactoring or caching with unchanged results and signatures.
- Replacing, removing, or vendoring an internal dependency without changing supported behavior.
- Tests, documentation, CI, and tooling.
- Packaging, build-system, artifact, platform, runtime-support, and installation-support changes.

Distribution and installation changes always use letter `C`, even when they add or remove supported installation capabilities.

### Choose the digit

Evaluate compatibility against documented, supported, and intended behavior—not accidental or faulty behavior.

Apply these rules in order and stop at the first match:

1. Use `1` if the change removes or incompatibly alters supported behavior and requires users to change code, configuration, or a supported workflow.
2. Otherwise, use `2` if the change adds a supported capability or provides an observable improvement.
3. Otherwise, use `3`.

#### `1`: Breaking

Use `1` for changes such as:

- Removing or renaming public API.
- Narrowing supported inputs.
- Incompatibly changing the intended behavior of a supported operation.
- Removing support for a runtime, platform, artifact, or installation method.

Do not use `1` merely because an output changes. Correcting faulty behavior is compatible when valid existing usage remains supported; such a fix uses `2`.

#### `2`: Compatible and meaningful

Use `2` for changes such as:

- Adding public API.
- Widening accepted inputs.
- Adding public type information.
- Correcting faulty runtime behavior.
- Improving observable runtime performance.
- Adding support for a runtime, platform, artifact, or installation method.

#### `3`: No supported or observable effect

Use `3` for changes such as:

- Internal implementation work with unchanged public results and signatures.
- Internal caching with unchanged behavior.
- Replacing or vendoring an internal dependency without changing supported behavior.
- Reorganizing tests.
- Updating documentation.
- Migrating packaging or build configuration without changing installation support.

Implementation effort alone does not justify digit `2`.

### Marker reference

| Marker | Use it for |
|---|---|
| `A1` | Breaking public API or public type-contract change |
| `A2` | Compatible public API or type-contract addition |
| `B1` | Incompatible change to intended runtime behavior with no API change |
| `B2` | Compatible runtime fix or observable performance improvement |
| `C1` | Removal of supported runtime, platform, artifact, or installation support |
| `C2` | Addition of supported runtime, platform, artifact, or installation support |
| `C3` | Internal, dependency, documentation, test, tooling, or packaging work with no supported or observable effect |

In particular:

- A new exported operation is `A2`, not `A1`.
- A newly accepted argument type is `A2`, not `B2`.
- A compatible bug fix is `B2`, not `B1`.
- Internal caching with unchanged behavior is `C3`, not `C2`.
- An internal dependency substitution is `C3`, not `C2`.
- Added distribution or platform support is `C2`.
- A packaging migration with unchanged installation support is `C3`.

## 3. Sort the bullets

Sort by the complete marker:

1. Letter: `A`, then `B`, then `C`.
2. Within each letter: `1`, then `2`, then `3`.

Keep separate changes as separate bullets when they have the same marker.

## 4. Write the Impact field

After classifying all bullets, find the numerically lowest digit present and write this immediately below the heading:

`Impact: D`

For example, digits `2` and `3` produce `Impact: 2`.

Impact is not:

- The number of changes.
- The most frequent digit.
- Necessarily the digit on the first bullet.

## 5. Add the trailer

After the final bullet, add this exact line:

`<!-- stl-impact: v1 -->`

The trailer must be the final line of the entry.

## Required structure

Use this order:

1. Heading
2. `Impact` field
3. Sorted change bullets
4. Parser trailer

Before finishing, verify:

- The version and date match the supplied release.
- Every pending change appears exactly once.
- Every bullet starts with a bracketed two-character marker.
- Each letter was chosen before and independently from its digit.
- Public API additions and widened inputs use `A2`.
- Compatible runtime fixes use `B2`.
- Unchanged internal, dependency, and packaging work uses `C3`.
- Added installation, artifact, platform, or runtime support uses `C2`.
- Bullets are sorted by letter and then digit.
- Impact equals the numerically lowest digit present.
- The parser trailer is the final line.