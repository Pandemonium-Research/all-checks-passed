---
name: impact-log
description: Instructions for converting a release version, date, and pending changes into a correctly classified, sorted, parser-compatible release notes entry.
---

# Release notes

Use this procedure for every release.

## Required output format

Produce exactly one entry:

```text
## [<X.Y.Z>] - <YYYY-MM-DD>
Impact: <digit>
- [<marker>] <change description>
- [<marker>] <change description>
<!-- stl-impact: v1 -->
```

Requirements:

- Write the version as three numeric parts inside square brackets. Do not add `v`.
- Separate the version and date with exactly ` - `.
- Write the date in `YYYY-MM-DD` format.
- Put `Impact: N` immediately below the heading.
- Write exactly one bullet for each pending change. Do not merge or split changes.
- Begin every bullet with `- ` followed immediately by its bracketed marker.
- Preserve the meaning of each pending change without inventing additional effects.
- Put `<!-- stl-impact: v1 -->` on the final line.

## Classify every change independently

Determine each bullet’s letter and digit from that pending change alone.

Do not give all bullets the release’s `Impact` digit. Calculate `Impact` only after every bullet has its own marker.

## Assign the marker letter

Ask these questions in order and stop at the first “yes”:

1. Does the change affect the public API contract? Use `A`.
2. Otherwise, can an existing call return a different value, raise differently, or produce a different visible effect? Use `B`.
3. Otherwise, use `C`.

### `A`: Public API contract

Use `A` for changes to:

- Exported public names
- Function or method signatures
- Required or optional parameters
- Accepted input types, even when the written signature is unchanged
- Return types
- Public typing information or its availability to type checkers

Typical `A` changes include adding or removing a public API, broadening or narrowing accepted argument types, changing a return type, and making shipped public annotations discoverable.

A return-type change is `A`, not `B`. An accepted-input-type change is also `A`, even if it is backward compatible.

### `B`: Caller-visible runtime behavior

Use `B` when the public API contract is unchanged but an existing call can behave differently.

This includes changes to:

- Returned values without a return-type change
- Output formatting or normalization
- Raised exceptions
- Other externally visible runtime effects
- Incorrect edge-case behavior

A defect fix that changes an erroneous result is `B`, not `C`.

### `C`: Packaging, documentation, tooling, or internals

Use `C` for changes confined to:

- Supported language runtimes or installation environments
- Build and packaging configuration
- Installation artifacts and dependency handling
- Documentation
- Tests, tooling, or CI
- Internal implementation details that preserve the public contract and runtime results

Behavior-preserving performance work, import deferral, caching changes, and refactoring are `C`. Documentation examples are also `C`.

Dropping support for a runtime version is `C`, not `A`, unless the same pending change separately alters the public API.

If one pending change affects multiple surfaces, use the earliest applicable letter:

```text
A, B, C
```

## Assign the marker digit

Choose the digit independently for each pending change:

| Digit | Use when |
| --- | --- |
| `1` | A previously supported use, API, runtime, or installation environment becomes incompatible |
| `2` | Users gain a compatible capability, a supported defect is fixed, or an externally relevant compatible packaging change occurs |
| `3` | The change is maintenance-only and preserves the public contract, runtime results, and supported installation behavior |

### Use `1` for breaking changes

Examples include:

- Removing a public API
- Narrowing accepted input types
- Adding a required parameter
- Changing a return type incompatibly
- Intentionally changing results for previously supported calls
- Dropping a supported runtime or installation environment

### Use `2` for compatible additions and fixes

Examples include:

- Adding a public API
- Broadening accepted input types
- Adding compatible public typing support
- Correcting erroneous runtime behavior
- Compatibly changing an installation artifact or dependency arrangement

### Use `3` for externally unchanged maintenance

Examples include:

- Documentation-only work
- Test, tooling, or CI maintenance
- Internal refactoring or cache replacement with identical results and signatures
- Performance improvements with unchanged behavior
- Build-system migrations that preserve supported installation behavior

Classify the effect, not the action word. Words such as “added,” “improved,” “fixed,” “replaced,” or “migrated” do not automatically imply `2`.

If a single pending change has effects with different digits, use the lowest digit:

```text
1 before 2 before 3
```

Combine the selected letter and digit inside square brackets, such as `[B2]`.

## Sort the bullets

After assigning all markers, sort the bullets in exactly this order:

```text
[A1], [A2], [A3], [B1], [B2], [B3], [C1], [C2], [C3]
```

This is letter-first order. Every `A` bullet precedes every `B` bullet, and every `B` bullet precedes every `C` bullet, regardless of digit.

When multiple bullets have the same marker, preserve their original pending-change order.

## Calculate the Impact field

After classifying the bullets, set `Impact` to the lowest digit appearing in any bullet marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only bullet-marker digits. Ignore digits in the version, date, descriptions, and trailer.

Do not change bullet markers to match the calculated `Impact`.

## Final verification

Before submitting, confirm that:

- The heading is exactly `## [X.Y.Z] - YYYY-MM-DD`.
- `Impact: N` is directly below the heading.
- Every pending change appears exactly once.
- Every bullet begins with one bracketed letter-and-digit marker.
- Public names, signatures, accepted types, return types, and public typing information use `A`.
- Runtime-only result, exception, and effect changes use `B`.
- Runtime support, packaging, documentation, tooling, and behavior-preserving internal work use `C`.
- Breaking changes use `1`.
- Compatible additions and fixes use `2`.
- Externally unchanged maintenance uses `3`.
- Each bullet was classified independently of the release-level `Impact`.
- Bullets follow the complete-marker sort order.
- Equal-marker bullets preserve their input order.
- `Impact` is the lowest bullet-marker digit.
- The final line is exactly `<!-- stl-impact: v1 -->`.