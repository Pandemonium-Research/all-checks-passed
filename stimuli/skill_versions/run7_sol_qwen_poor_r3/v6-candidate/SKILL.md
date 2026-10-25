---
name: impact-log
description: Use when given a release version, date, and pending changes to write one classified, sorted, parser-compatible release notes entry.
---

# Release notes

Use this procedure for every release:

1. Assign each pending change its own marker.
2. Sort the marked bullets.
3. Calculate `Impact` from the completed markers.

Classify every change independently. Do not choose `Impact` first or copy the release-level digit into each marker.

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
- Put exactly ` - ` between the version and date.
- Write the date in `YYYY-MM-DD` format.
- Put `Impact: N` immediately below the heading.
- Write exactly one bullet for each pending change. Do not merge changes or split one change into multiple bullets.
- Preserve the meaning of each pending change without inventing effects.
- Start every bullet with `- ` followed immediately by its bracketed marker, such as `[A2]`.
- Put `<!-- stl-impact: v1 -->` on the final line.

## Assign each marker independently

A marker contains exactly one uppercase letter followed by one digit.

Determine both characters from the pending change being classified. Changes in the same release may have different digits.

## Assign the marker letter

Ask these questions in order and stop at the first “yes”:

1. Does the change affect the public API or public type contract? Use `A`.
2. Otherwise, can an existing call return a different value, raise differently, or have another caller-visible runtime effect? Use `B`.
3. Otherwise, use `C`.

### `A`: Public API or type contract

Use `A` for changes to:

- Exported public names
- Function or method signatures
- Required or optional parameters
- Accepted input types, even if the written signature is unchanged
- Return types
- Public annotations or whether type checkers can discover them

Important classifications:

- Adding or removing an exported public name is `A`.
- Broadening or narrowing the accepted input types is `A`, not `B`.
- Changing from one return type to another is `A`, not `B`.
- Making shipped public annotations available to type checkers is `A`, even when runtime behavior is unchanged.

### `B`: Caller-visible runtime behavior

Use `B` when the public API and type contract remain unchanged, but an existing call can behave differently.

This includes changes to:

- Returned values without a return-type change
- Formatting, normalization, or output content
- Raised exceptions
- Other externally visible runtime effects

A defect fix that corrects an erroneous result or exception is `B`. An intentional result change for previously supported input is also `B`.

Do not use `B` merely because internal code runs differently or faster.

### `C`: Runtime support, packaging, documentation, or internals

Use `C` for changes confined to:

- Supported language runtimes or installation environments
- Build and packaging configuration
- Installation artifacts or dependency handling
- Documentation
- Tests, tooling, or CI
- Internal implementation details that preserve public contracts and runtime results
- Performance improvements with unchanged results and effects

Important classifications:

- Dropping support for a language runtime or installation environment is `C`, not `A`.
- Documentation examples are `C`.
- Import deferral, caching, refactoring, and optimization are `C` when public contracts, results, exceptions, and visible effects remain unchanged.
- Packaging and dependency changes are `C` unless they also change the public API or runtime behavior.

If a pending change affects more than one surface, use the earliest applicable letter:

```text
A, B, C
```

## Assign the marker digit

Choose the digit separately for each pending change:

| Digit | Meaning |
| --- | --- |
| `1` | Breaking: a previously supported API, call, runtime, or installation environment becomes incompatible or intentionally behaves differently |
| `2` | Compatible: users gain a capability, a supported defect is fixed, or installation artifacts or dependency handling change compatibly |
| `3` | Externally unchanged: public contracts, runtime results, and supported installation behavior remain unchanged |

Use `1` for changes such as:

- Removing a public API
- Narrowing accepted input types
- Adding a required parameter
- Incompatibly changing a return type
- Intentionally changing results for previously supported calls
- Dropping a supported runtime or installation environment

Use `2` for changes such as:

- Adding a public API
- Broadening accepted input types
- Making compatible public typing information available
- Correcting an erroneous result or exception
- Compatibly changing an installation artifact or dependency arrangement

Use `3` for changes such as:

- Documentation-only work
- Test, tooling, or CI maintenance
- Internal refactoring or cache replacement with identical behavior
- Performance improvements with unchanged behavior
- Build or packaging migrations that preserve supported installation behavior

Classify the effect, not the action word. Words such as “added,” “fixed,” “improved,” “replaced,” or “migrated” do not determine the digit.

If one pending change contains effects with different digits, use the lowest digit:

```text
1 before 2 before 3
```

Combine the selected letter and digit inside square brackets.

## Sort the bullets

After every pending change has its own marker, sort all bullets in this exact order:

```text
[A1], [A2], [A3], [B1], [B2], [B3], [C1], [C2], [C3]
```

This is letter-first order: all `A` bullets precede all `B` bullets, and all `B` bullets precede all `C` bullets.

When multiple bullets have the same marker, preserve their original pending-change order.

Do not place markers at the end of bullets or write unbracketed markers.

## Calculate the Impact field

Calculate `Impact` only after all bullet markers are final.

Set `Impact` to the lowest digit appearing in any bullet marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Inspect only the digits in bullet markers. Ignore digits in the version, date, descriptions, and trailer.

Do not change individual bullet markers to match `Impact`.

## Final verification

Before submitting the entry, verify that:

- The heading is exactly `## [X.Y.Z] - YYYY-MM-DD`.
- `Impact: N` is directly below the heading.
- Every pending change appears exactly once.
- Every bullet begins with one bracketed letter-and-digit marker.
- Each pending change was classified independently.
- Public names, signatures, parameters, accepted types, return types, and public typing information use `A`.
- Runtime-only result, exception, and visible-effect changes use `B`.
- Runtime support, packaging, documentation, tooling, and behavior-preserving internal changes use `C`.
- Breaking changes use `1`, compatible additions and fixes use `2`, and externally unchanged maintenance uses `3`.
- Bullets follow the complete-marker sort order.
- Equal-marker bullets preserve their input order.
- `Impact` is the lowest bullet-marker digit.
- The final line is exactly `<!-- stl-impact: v1 -->`.