---
name: impact-log
description: Use this guide when converting a release version, date, and list of pending changes into a classified, sorted release-notes entry with an Impact value and parser trailer.
---

# Release notes

Follow these steps for every release.

## 1. Write the heading

Use this exact pattern:

`## [VERSION] - YYYY-MM-DD`

Requirements:

- Use a second-level Markdown heading: `##`.
- Put the three-part version number in square brackets.
- Put ` - ` between the version and date.
- Format the date as a four-digit year, two-digit month, and two-digit day.

## 2. Create one bullet per pending change

Every pending change must appear exactly once. Do not merge separate changes or split one change into multiple bullets.

Use this format:

`- [LD] Description of the change.`

`L` is the surface letter and `D` is the impact digit. Include the square brackets.

Classify the letter and digit separately. The letter identifies what surface changed; the digit identifies the change's compatibility or observable impact.

### Choose the letter

Ask these questions in order and stop at the first match:

1. Does the change affect the public API or public type contract? Use `A`.
2. Otherwise, does it change the observable runtime behavior of an existing public operation? Use `B`.
3. Otherwise, use `C`.

Use `A` for any public-interface change, including:

- Adding, removing, or renaming an exported name.
- Changing a function or method signature.
- Widening or narrowing the accepted argument types.
- Changing a public return type.
- Adding or changing information consumed by type checkers.

An additive or backward-compatible API change is still `A`. For example, a new exported function or a newly accepted argument type is `A`, not `B`.

Use `B` only when the public interface remains the same but existing calls have a different observable runtime result, error, side effect, or performance characteristic. Runtime bug fixes normally use `B`.

Use `C` when neither the public API nor caller-visible runtime behavior changes. This includes internal refactoring, tests, documentation, CI, tooling, and packaging or build work. Packaging and build changes remain `C` even when they add or remove installation support.

### Choose the digit

Judge compatibility against the project's supported and intended behavior, not against accidental buggy behavior.

Ask these questions in order:

1. Must users change code, configuration, or a supported workflow because previously supported behavior was removed or made incompatible? Use `1`.
2. Otherwise, does the change add a supported capability or produce an observable improvement? Use `2`.
3. Otherwise, use `3`.

Use `1` for breaking changes such as:

- Removing or renaming a public API.
- Narrowing supported inputs.
- Changing the intended meaning or result of an existing supported call incompatibly.
- Removing a supported runtime, platform, artifact, or installation method.

Do not use `1` merely because output changes when a bug is fixed. If the new output restores intended behavior and correct existing caller code remains compatible, use `2`.

Use `2` for compatible, meaningful changes such as:

- Adding a public API.
- Widening accepted argument types.
- Fixing incorrect runtime behavior.
- Improving observable performance.
- Adding support for a runtime, platform, artifact, or installation method.
- Adding public type information.

Use `3` when the change has no public or caller-observable effect, such as an internal refactor with unchanged results and signatures, a test reorganization, or a documentation-only update.

The letter and digit describe different axes. For example:

- A compatible public API addition is `A2`.
- A compatible runtime bug fix with no API change is `B2`.
- New build or installation support is `C2`.
- An internal implementation change with unchanged public behavior is `C3`.

Do not assign `2` solely because implementation work occurred. There must be a new supported capability or an observable improvement; otherwise use `3`.

## 3. Sort the bullets

Sort bullets by their complete marker in ascending order:

1. Letter: `A`, then `B`, then `C`.
2. Within each letter: `1`, then `2`, then `3`.

Keep separate changes as separate bullets when they have the same marker.

## 4. Write the Impact field

Immediately below the heading, write:

`Impact: D`

Replace `D` with the lowest digit used by any bullet.

The value must be `1`, `2`, or `3`. It is not the number of changes, the most frequent digit, or the digit from the first bullet.

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

Before finishing, verify all of the following:

- The version and date match the supplied release.
- Every pending change appears exactly once.
- Every bullet begins with a bracketed two-character marker.
- Public API additions and widened accepted types use letter `A`.
- Compatible additions and bug fixes use digit `2`, not `1`.
- Unobservable internal changes use digit `3`, not `2`.
- Bullets are sorted by letter and then digit.
- The Impact value equals the lowest bullet digit.
- The parser trailer is the final line.