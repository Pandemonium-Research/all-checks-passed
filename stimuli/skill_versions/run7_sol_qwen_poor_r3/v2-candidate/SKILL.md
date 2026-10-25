---
name: impact-log
description: Use when converting a release version, release date, and pending changes into a classified, sorted, parser-compatible release notes entry.
---

# Release notes

Follow this procedure for every release.

## Required output

Produce exactly one entry:

```text
## [<X.Y.Z>] - <YYYY-MM-DD>
Impact: <digit>
- [<marker>] <change description>
- [<marker>] <change description>
<!-- stl-impact: v1 -->
```

Apply these rules:

- Write the version as three numeric parts inside square brackets. Do not add `v`.
- Write the date in `YYYY-MM-DD` format.
- Separate the version and date with exactly ` - `.
- Put `Impact: N` immediately below the heading.
- Write exactly one bullet for each pending change. Do not merge changes or split one change across multiple bullets.
- Begin every bullet with `- ` and its bracketed marker, such as `[A2]`.
- Preserve the meaning of each pending change when writing its description.
- Put `<!-- stl-impact: v1 -->` on the final line.

## Classify each change

Each marker contains one uppercase letter and one digit. Determine the letter and digit separately.

### Step 1: Choose the letter

Ask the following questions in order. Stop at the first “yes.”

1. Does the change affect the public API contract? Use `A`.
2. Otherwise, does it change runtime behavior visible to an existing caller? Use `B`.
3. Otherwise, use `C`.

#### `A`: Public API contract

Use `A` when a change affects any of the following:

- Exported modules, classes, functions, methods, constants, or other public names
- Function or method signatures
- Parameters, including whether they are required or optional
- Accepted input types, even if the written signature is unchanged
- Return types
- Public typing information or whether type checkers can discover that information

Examples of `A` changes include:

- Adding or removing a public name
- Adding, removing, or changing a parameter
- Broadening or narrowing the types accepted by an argument
- Changing a return value from one type to another
- Adding distributable metadata that makes shipped public annotations available to type checkers

A return-type change is `A`, not `B`, even though callers also observe different runtime behavior.

#### `B`: Caller-visible runtime behavior

Use `B` when the public API contract remains unchanged, but an existing call can return a different value, raise a different exception, or produce a different externally visible effect.

Examples include:

- Correcting an erroneous result
- Changing output formatting or normalization
- Changing when an existing call raises
- Fixing an edge case without changing accepted types or the signature

#### `C`: Packaging, documentation, tooling, or internals

Use `C` for changes confined to:

- Supported runtimes or installation environments
- Build and packaging configuration
- Installed artifacts or dependency handling
- Tooling, tests, documentation, or CI
- Internal implementation details that preserve the public API and caller-visible results

Dropping support for a language-runtime version is `C`, not `A`, unless the same pending change also alters the public API.

Behavior-preserving optimizations, caching changes, import deferral, and refactors are `C`. Do not classify them as `B` merely because they execute inside public code.

If one pending change has multiple applicable surfaces, use the earliest letter in this order:

```text
A, B, C
```

### Step 2: Choose the digit

Choose the digit based on compatibility and observability:

| Digit | Use when |
| --- | --- |
| `1` | Previously supported use can become invalid, fail, or produce an intentionally different result |
| `2` | Users gain a compatible capability, or a defect in supported behavior is fixed |
| `3` | The change is externally unchanged: no public-contract change, caller-visible result change, or supported installation change |

Use `1` for changes such as:

- Removing a public API
- Narrowing accepted inputs
- Adding a required argument
- Changing the type or meaning of a returned result
- Intentionally changing behavior for previously supported calls
- Dropping a supported runtime or installation environment

Use `2` for changes such as:

- Adding a public API
- Broadening accepted inputs
- Adding compatible public typing support
- Fixing incorrect runtime behavior
- Compatibly adding or changing an installation artifact or dependency arrangement

Use `3` for changes such as:

- Documentation-only additions or corrections
- Test, CI, or tooling maintenance
- Internal refactors or cache changes with unchanged results and signatures
- Performance work with unchanged public behavior
- Build-system or packaging migrations that leave supported installation behavior unchanged

Classify the effect, not the action word. A change does not become `2` merely because its description says “added,” “fixed,” “improved,” or “replaced.”

If a single pending change contains effects with different digits, use the lowest digit:

```text
1 before 2 before 3
```

Combine the selected letter and digit inside brackets, for example `[B2]`.

## Sort the bullets

Sort bullets by their complete markers in exactly this order:

```text
[A1], [A2], [A3], [B1], [B2], [B3], [C1], [C2], [C3]
```

This is letter-first order, not digit-first or severity order. For example, every `B` marker precedes every `C` marker, including `C1`.

When multiple bullets have the same marker, keep their original pending-change order.

## Calculate `Impact`

Set `Impact` to the lowest digit appearing in any bullet marker:

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only the digits in bullet markers. Ignore digits in the version, date, descriptions, and trailer.

## Final verification

Before submitting, confirm all of the following:

- The heading is exactly `## [X.Y.Z] - YYYY-MM-DD`.
- `Impact: N` is directly below the heading.
- Every pending change appears exactly once.
- Every bullet begins with a bracketed marker.
- Public names, signatures, accepted types, return types, and public typing information use `A`.
- Runtime-only result, exception, and effect changes use `B`.
- Runtime support, packaging, documentation, tooling, and behavior-preserving internal work use `C`.
- Breaking changes use `1`, compatible additions and fixes use `2`, and externally unchanged work uses `3`.
- Bullets follow the complete-marker sort order.
- Equal-marker bullets preserve their input order.
- `Impact` is the lowest bullet-marker digit.
- The final line is exactly `<!-- stl-impact: v1 -->`.