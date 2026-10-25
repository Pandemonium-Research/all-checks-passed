---
name: impact-log
description: Use when given a release version, date, and pending changes to produce one correctly classified, sorted, parser-compatible release notes entry.
---

# Release notes

Use this procedure for every release:

1. Classify each pending change independently.
2. Assign each change its own complete marker.
3. Sort the marked bullets.
4. Calculate the release-level `Impact` from the finished markers.

Do not choose `Impact` first or copy its digit into every bullet marker.

## Required output format

Produce one entry in this exact structure:

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
- Write exactly one bullet for each pending change. Do not merge changes or split one change into multiple bullets.
- Preserve each change’s meaning without inventing effects.
- Start every bullet with `- ` followed immediately by its bracketed marker.
- Put `<!-- stl-impact: v1 -->` on the final line.

## Classify each pending change independently

Each marker contains one uppercase letter and one digit, such as `[B2]`.

Determine both characters from that pending change alone. Different changes in the same release may require different digits even though the entry has only one release-level `Impact`.

## Assign the marker letter

Choose the letter by asking these questions in order. Stop at the first “yes.”

1. Does the change alter the public API or public type contract? Use `A`.
2. Otherwise, can an existing call return a different value, raise differently, or produce another caller-visible runtime effect? Use `B`.
3. Otherwise, use `C`.

### `A`: Public API or type contract

Use `A` for changes to:

- Exported public names
- Function or method signatures
- Required or optional parameters
- Accepted input types, even if the written signature is unchanged
- Return types
- Public annotations or their availability to type checkers

Important distinctions:

- Adding or removing a public name is `A`.
- Broadening or narrowing the accepted input types is `A`, not `B`.
- Changing a return type is `A`, not `B`, even though callers also observe different runtime values.
- Making shipped public annotations discoverable to type checkers is `A`, even when runtime behavior is unchanged.

### `B`: Caller-visible runtime behavior

Use `B` only when the public API and type contract remain unchanged but an existing call can behave differently.

This includes changes to:

- Returned values without a return-type change
- Formatting, normalization, or output content
- Raised exceptions
- Other externally visible runtime effects
- Incorrect edge-case behavior

A defect fix that changes an erroneous result or exception is `B`, not `C`.

Do not use `B` merely because internal code runs differently or faster.

### `C`: Runtime support, packaging, documentation, or internals

Use `C` for changes confined to:

- Supported language runtimes or installation environments
- Build and packaging configuration
- Installation artifacts or dependency handling
- Documentation
- Tests, tooling, or CI
- Internal implementation details that preserve the public contract and runtime results
- Performance work with unchanged results and effects

Important distinctions:

- Dropping support for a language runtime or installation environment is `C`, not `A`.
- Documentation examples are `C`.
- Refactoring, import deferral, cache changes, and optimizations are `C` when signatures, results, exceptions, and other visible effects remain unchanged.
- A build-system migration is `C` when it does not alter the public API or runtime behavior.

If one pending change affects multiple surfaces, use the earliest applicable letter:

```text
A, B, C
```

## Assign the marker digit

Choose the digit separately for each pending change:

| Digit | Use when |
| --- | --- |
| `1` | A previously supported API, call, runtime, or installation environment becomes incompatible or intentionally behaves differently |
| `2` | Users gain a compatible capability, a supported defect is fixed, or installation artifacts or dependency handling change compatibly |
| `3` | The public contract, runtime results, and supported installation behavior remain unchanged |

### Use `1` for breaking changes

Examples include:

- Removing a public API
- Narrowing accepted input types
- Adding a required parameter
- Incompatibly changing a return type
- Intentionally changing results for previously supported calls
- Dropping a supported runtime or installation environment

### Use `2` for compatible additions and fixes

Examples include:

- Adding a public API
- Broadening accepted input types
- Adding compatible public typing support
- Correcting an erroneous result or exception
- Compatibly changing an installation artifact or dependency arrangement

### Use `3` for externally unchanged maintenance

Examples include:

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

This is letter-first order: every `A` bullet precedes every `B` bullet, and every `B` bullet precedes every `C` bullet, regardless of digit.

When two bullets have the same marker, preserve their original pending-change order.

Do not place markers at the end of bullets or write unbracketed markers.

## Calculate the Impact field

Calculate `Impact` only after all bullet markers are final.

Set `Impact` to the lowest digit appearing in any bullet marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Inspect only the digits in bullet markers. Ignore digits in the version, date, descriptions, and trailer.

Do not change individual bullet markers to match the calculated `Impact`.

## Final verification

Before submitting, verify that:

- The heading is exactly `## [X.Y.Z] - YYYY-MM-DD`.
- `Impact: N` is directly below the heading.
- Every pending change appears exactly once.
- Every bullet begins with one bracketed letter-and-digit marker.
- Each change was classified independently.
- Public names, signatures, parameters, accepted types, return types, and public typing information use `A`.
- Runtime-only result, exception, and visible-effect changes use `B`.
- Runtime support, packaging, documentation, tooling, and behavior-preserving internal changes use `C`.
- Breaking changes use `1`.
- Compatible additions and defect fixes use `2`.
- Externally unchanged maintenance uses `3`.
- Bullets follow the complete-marker sort order.
- Equal-marker bullets preserve their input order.
- `Impact` is the lowest bullet-marker digit.
- The final line is exactly `<!-- stl-impact: v1 -->`.