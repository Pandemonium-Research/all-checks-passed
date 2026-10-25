---
name: impact-log
description: Instructions for converting a release version, date, and pending changes into a correctly classified, sorted, parser-compatible release notes entry.
---

# Release notes

Use the following procedure for every release.

## Required output format

Produce one entry in this exact structure:

```text
## [<X.Y.Z>] - <YYYY-MM-DD>
Impact: <digit>
- [<marker>] <change description>
- [<marker>] <change description>
<!-- stl-impact: v1 -->
```

The requirements are:

- Write the version as three numeric parts inside square brackets. Do not add `v`.
- Put a space, hyphen, and space between the version and date.
- Write the date in `YYYY-MM-DD` format.
- Put `Impact: N` immediately below the heading.
- Write exactly one bullet for each pending change. Do not merge changes or split one change into multiple bullets.
- Start every bullet with `- ` followed immediately by its bracketed impact marker, such as `[A2]`.
- Put the trailer `<!-- stl-impact: v1 -->` after the final bullet.

## Assign the marker letter

Each marker contains one letter followed by one digit.

Choose the letter according to the surface affected:

| Letter | Use when the change affects |
| --- | --- |
| `A` | The public API contract: exported names, function or method signatures, parameters, accepted input types, return types, or public type information |
| `B` | Runtime behavior visible to an existing caller, while the public API contract remains unchanged |
| `C` | Build, packaging, installation artifacts, tooling, tests, documentation, CI, or an internal implementation detail with no public API or runtime-behavior change |

Common `A` changes include adding or removing an exported name, adding or removing a parameter, changing whether a parameter is required, or broadening or narrowing the documented types accepted by an argument.

Use `B` for an implementation change that alters what an existing call returns, raises, or otherwise does without changing its public signature or type contract.

Use `C` for changes confined to project infrastructure or internals. A behavior-preserving refactor or cache belongs to `C`, even when it is inside a public function.

If more than one letter seems applicable, choose the earliest letter in this order:

```text
A, B, C
```

## Assign the marker digit

Choose the digit independently of the letter:

| Digit | Meaning |
| --- | --- |
| `1` | Breaking: previously supported caller code can now fail, become invalid, or produce a different result |
| `2` | Compatible: the change is additive or fixes a defect while correct, supported existing code remains valid |
| `3` | Unobservable to callers: there is no change to the public contract or caller-visible results |

Use `1` for incompatible removals, restrictions, required new arguments, or intentional behavior changes that affect previously supported calls.

Use `2` for additions, backward-compatible extensions, and defect fixes. A fix remains `2` when it changes only erroneous or unsupported behavior and does not break correct, supported usage.

Use `3` for changes such as internal refactoring, test reorganization, CI maintenance, or documentation-only work when callers cannot observe a difference.

If one pending change contains effects with different digits, use the lowest digit:

```text
1 before 2 before 3
```

Combine the selected letter and digit inside square brackets. The marker must contain exactly one uppercase letter and one digit, for example `[B2]`.

## Sort the bullets

Sort all bullets by their complete markers in this order:

```text
[A1], [A2], [A3], [B1], [B2], [B3], [C1], [C2], [C3]
```

Keep the original pending-change order when two bullets have the same marker.

Do not place markers at the end of bullets and do not write unbracketed markers.

## Calculate the Impact field

Set `Impact` to the lowest digit used by any bullet marker in the entry.

For example:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Only inspect digits in the bullet markers. Ignore digits in the version, date, change descriptions, and parser trailer.

## Final verification

Before submitting the entry, verify that:

- The heading is exactly `## [X.Y.Z] - YYYY-MM-DD`.
- Every pending change appears once.
- Every bullet begins with a bracketed marker.
- Public API contract changes use `A`.
- Runtime-only behavior changes use `B`.
- Infrastructure-only or unobservable internal changes use `C`.
- Breaking changes use `1`, compatible additions and fixes use `2`, and caller-unobservable changes use `3`.
- Bullets are sorted by marker.
- `Impact` is the lowest bullet-marker digit.
- The final line is exactly `<!-- stl-impact: v1 -->`.