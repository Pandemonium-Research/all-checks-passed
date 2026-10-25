---
name: impact-log
description: Use this procedure to turn a release version, release date, and list of pending changes into one classified, sorted, parser-compatible release notes entry.
---

# Release notes

Classify each pending change separately, sort the resulting bullets, and then calculate the release-level `Impact`.

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
- Write the date in `YYYY-MM-DD` format.
- Separate the version and date with exactly ` - `.
- Put `Impact: N` immediately below the heading.
- Write exactly one bullet for each pending change. Do not merge or split changes.
- Preserve each change’s meaning without inventing effects.
- Begin every bullet with `- ` followed immediately by its bracketed marker.
- Put `<!-- stl-impact: v1 -->` on the final line.

## Classify each pending change independently

A marker contains one uppercase letter followed by one digit, such as `[B2]`.

Determine the letter and digit from that pending change alone. Do not copy the release-level `Impact` digit into every marker.

## Choose the letter

Ask these questions in order and stop at the first “yes”:

1. Does the change affect the public API or public type contract? Use `A`.
2. Otherwise, can an existing call return a different value, raise differently, or produce a different visible runtime effect? Use `B`.
3. Otherwise, use `C`.

### `A`: Public API or type contract

Use `A` for changes to:

- Exported public names
- Function or method signatures
- Required or optional parameters
- Accepted input types, even if the written signature is unchanged
- Return types
- Public annotations or their availability to type checkers

Therefore:

- Adding a public API is `A2`.
- Removing a public API is `A1`.
- Broadening accepted input types is `A2`.
- Narrowing accepted input types is `A1`.
- Changing the return type is `A`, not `B`; choose `1` if previously supported callers become incompatible.
- Making shipped public annotations discoverable to type checkers is `A2`, even when runtime behavior is unchanged.

### `B`: Caller-visible runtime behavior

Use `B` when the public API and type contract remain unchanged, but an existing call can behave differently.

This includes changes to:

- Returned values without a return-type change
- Formatting, normalization, or output content
- Raised exceptions
- Other externally visible runtime effects

An intentional behavior change affecting supported calls is `B1`. A defect fix that corrects an erroneous result or exception is `B2`.

Do not use `B` merely because internal code executes differently or faster.

### `C`: Runtime support, packaging, documentation, or internals

Use `C` for changes confined to:

- Supported language runtimes or installation environments
- Build and packaging configuration
- Installation artifacts or dependency handling
- Documentation
- Tests, tooling, or CI
- Internal implementation details that preserve the public contract and runtime results
- Performance improvements with unchanged results and effects

Examples:

- Dropping a supported runtime or installation environment is `C1`, not `A1`.
- A compatible change to installed artifacts or dependency handling is `C2`.
- Documentation-only work is `C3`.
- Import deferral, caching, refactoring, or optimization with unchanged behavior is `C3`.
- A build-system migration that preserves supported installation behavior is `C3`.

If one pending change affects multiple surfaces, use the earliest applicable letter:

```text
A, B, C
```

## Choose the digit

Choose the digit independently for every pending change:

| Digit | Use when |
| --- | --- |
| `1` | A previously supported API, call, runtime, or installation environment becomes incompatible or intentionally behaves differently |
| `2` | Users gain a compatible capability, a supported defect is fixed, or installation behavior changes compatibly |
| `3` | Public contracts, runtime results, and supported installation behavior remain unchanged |

Classify the effect, not the action word. Words such as “added,” “fixed,” “improved,” “replaced,” or “migrated” do not determine the digit.

If one pending change contains effects with different digits, choose the lowest digit:

```text
1 before 2 before 3
```

## Sort the bullets

After assigning all markers, sort the bullets in exactly this order:

```text
[A1], [A2], [A3], [B1], [B2], [B3], [C1], [C2], [C3]
```

This is letter-first order: every `A` bullet precedes every `B` bullet, and every `B` bullet precedes every `C` bullet.

When multiple bullets have the same marker, preserve their original pending-change order.

## Calculate `Impact`

Calculate `Impact` only after every bullet has its own marker.

Set `Impact` to the lowest digit appearing in any bullet marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only marker digits. Ignore digits in the version, date, descriptions, and trailer. Do not alter individual markers to match `Impact`.

## Final verification

Before submitting, confirm that:

- The heading is exactly `## [X.Y.Z] - YYYY-MM-DD`.
- `Impact: N` is directly below the heading.
- Every pending change appears exactly once.
- Every bullet begins with one bracketed letter-and-digit marker.
- Each change was classified independently.
- Public names, signatures, accepted types, return types, and public typing information use `A`.
- Runtime-only result, exception, and effect changes use `B`.
- Runtime support, packaging, documentation, tooling, and behavior-preserving internal work use `C`.
- Breaking changes use `1`, compatible additions and fixes use `2`, and externally unchanged maintenance uses `3`.
- Bullets follow the complete-marker order.
- Equal-marker bullets preserve their input order.
- `Impact` is the lowest bullet-marker digit.
- The final line is exactly `<!-- stl-impact: v1 -->`.