---
name: impact-log
description: Use this guide when converting a supplied release version, date, and pending-change list into a classified, sorted release-notes entry with an Impact value and parser trailer.
---

# Release notes

Follow this procedure for every release. Output only the completed entry.

## 1. Write the heading

Use this exact pattern:

`## [VERSION] - YYYY-MM-DD`

Copy the supplied three-part version and date exactly. Use a second-level heading, square brackets around the version, and ` - ` between the version and date.

## 2. Create one bullet per pending change

Include every pending change exactly once. Do not merge separate changes or split one change into multiple bullets.

Use this exact format:

`- [LD] Description of the change.`

`L` is the surface letter and `D` is the impact digit. Choose them independently.

### Choose the letter

Apply these rules in order and stop at the first match:

1. Use `A` if the public API or public type contract changes.
2. Otherwise, use `B` if the observable runtime behavior of an existing public operation changes.
3. Otherwise, use `C`.

#### `A`: Public API or type contract

Use `A` for:

- Adding, removing, or renaming an exported name.
- Changing a public function or method signature.
- Widening or narrowing accepted argument types.
- Changing a public return type.
- Adding or changing information consumed by type checkers.

A compatible API addition uses `A`. A newly accepted input type also uses `A`, even though it affects runtime behavior.

#### `B`: Existing public runtime behavior

Use `B` when the public interface is unchanged but an existing public operation has a different observable result, error, side effect, or performance characteristic.

This includes compatible runtime bug fixes and explicitly stated user-visible performance improvements, such as reduced execution, import, or startup time.

An implementation technique such as caching or lazy loading does not by itself require `B`. Use `C` if the pending change states that public behavior is unchanged and does not claim an observable performance improvement.

#### `C`: Internal, project, or distribution surface

Use `C` for changes outside the public API and existing-operation runtime behavior, including:

- Internal refactoring or caching with unchanged public behavior.
- Replacing, removing, or vendoring an internal dependency without changing supported behavior.
- Tests, documentation, CI, and tooling.
- Packaging and build-system migrations.
- Runtime, platform, artifact, wheel, and installation-support changes.

Distribution and installation-support changes use `C`, even when they add or remove a supported capability.

### Choose the digit

Judge compatibility against documented, supported, and intended behavior. Accidental or faulty behavior is not a compatibility promise.

Apply these rules in order and stop at the first match:

1. Use `1` if supported behavior is removed or incompatibly changed so users must change code, configuration, or a supported workflow.
2. Otherwise, use `2` if the change adds a supported capability or provides an observable improvement.
3. Otherwise, use `3`.

#### `1`: Breaking

Use `1` for:

- Removing or renaming public API.
- Narrowing supported inputs.
- Incompatibly changing the intended result or meaning of a supported operation.
- Removing support for a runtime, platform, artifact, or installation method.

Do not use `1` merely because a result changes. If the old result was faulty and the change restores intended behavior while valid existing usage remains supported, use `2`.

#### `2`: Compatible and meaningful

Use `2` for:

- Adding public API.
- Widening accepted inputs.
- Adding public type information.
- Correcting faulty runtime behavior.
- Improving observable runtime performance.
- Adding support for a runtime, platform, artifact, or installation method.

#### `3`: No supported or observable effect

Use `3` for:

- Internal implementation work with unchanged public results and signatures.
- Internal caching without a stated observable performance improvement.
- Internal dependency substitutions that preserve supported behavior.
- Test reorganization.
- Documentation updates.
- Packaging or build migrations that preserve installation support.

Implementation effort alone does not justify digit `2`.

### Marker reference

| Marker | Use it for |
|---|---|
| `A1` | Breaking public API or type-contract change |
| `A2` | Compatible public API or type-contract addition |
| `B1` | Incompatible intended runtime-behavior change with no API change |
| `B2` | Compatible runtime fix or observable performance improvement |
| `C1` | Removal of supported runtime, platform, artifact, or installation support |
| `C2` | Addition of supported runtime, platform, artifact, or installation support |
| `C3` | Internal, dependency, documentation, test, tooling, packaging, or build work with no supported or observable effect |

In particular:

- A new exported operation is `A2`.
- A newly accepted argument type is `A2`.
- A compatible bug fix is `B2`.
- Internal caching with otherwise unchanged behavior is `C3`.
- An internal dependency substitution with unchanged behavior is `C3`.
- Added runtime, platform, wheel, artifact, or installation support is `C2`.
- A packaging migration with unchanged installation support is `C3`.

## 3. Sort the bullets

Sort by the complete marker:

1. Letter: `A`, then `B`, then `C`.
2. Within each letter: `1`, then `2`, then `3`.

For bullets with identical markers, preserve their order from the pending-change list.

## 4. Write the Impact field

After classifying all bullets, find the numerically lowest digit present. Immediately below the heading, write:

`Impact: D`

For example, an entry containing digits `2` and `3` has `Impact: 2`.

Impact is not the number of changes, the most frequent digit, or necessarily the digit on the first bullet.

## 5. Add the trailer

After the final bullet, add this exact line:

`<!-- stl-impact: v1 -->`

The trailer must be the final line of the entry.

## Required layout

Use exactly this order, with blank lines between the sections:

1. Heading
2. `Impact` field
3. Sorted change bullets
4. Parser trailer

Before finishing, verify:

- The version and date match the supplied release.
- Every pending change appears exactly once.
- Every bullet begins with a bracketed two-character marker.
- The letter and digit were chosen independently.
- Compatible public API additions and widened inputs use `A2`.
- Compatible runtime fixes use `B2`.
- Internal changes with unchanged behavior use `C3`.
- Added distribution or platform support uses `C2`.
- Bullets are sorted by letter and then digit.
- Impact equals the numerically lowest digit present.
- The parser trailer is the final line.