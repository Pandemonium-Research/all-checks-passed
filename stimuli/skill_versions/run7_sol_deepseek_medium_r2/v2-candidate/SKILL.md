---
name: impact-log
description: Write a parseable impact-log release-notes entry from a supplied version, date, and list of pending project changes.
---

# Release notes

Produce exactly one release entry. Include every supplied change exactly once; do not invent, omit, combine, or split changes.

Use this exact layout:

```text
## [X.Y.Z] - YYYY-MM-DD
Impact: N

- [LD] Description of one change.
- [LD] Description of another change.

<!-- stl-impact: v1 -->
```

Replace the placeholders with the supplied version, date, impact, codes, and descriptions. Output only the entry.

Formatting requirements:

- Use a three-part version number: `X.Y.Z`.
- Use an ISO date: `YYYY-MM-DD`.
- Put `Impact` directly below the heading, with no blank line between them.
- Put exactly one blank line between `Impact` and the first bullet.
- Put no blank lines between bullets.
- Put exactly one blank line between the final bullet and the trailer.
- Use `<!-- stl-impact: v1 -->` exactly as written.
- Make the trailer the final line.

## Classify every change

Begin each bullet with one code in the form `[LD]`. Determine the letter and digit separately.

### Step 1: Choose the letter

Check the categories in this order:

1. `A` — The public contract changes.
2. `B` — An existing public call behaves differently, but its public contract does not change.
3. `C` — Only implementation or maintenance details change.

Use `A` for changes to any consumer-facing contract, including:

- Exported names or public import paths
- Callable signatures
- Accepted argument types
- Return types
- Supported runtime versions
- Consumer-visible annotations or type information
- Added, removed, or renamed public functionality

Use `B` only when the contract remains the same but functional runtime behavior changes, including:

- Different returned values or output
- Different parsing, formatting, or normalization
- New, removed, or corrected runtime errors
- Bug fixes to an existing public call

Use `C` when public contracts and functional results remain unchanged, including:

- Internal refactors or caches
- Performance-only implementation changes
- Dependency or vendoring changes with no consumer-visible effect
- Build or packaging migrations that preserve installation and support
- Tooling, tests, and documentation

Classify the effect, not the file modified. For example, a packaging change that removes support for a runtime is `A`, not `C`.

### Step 2: Choose the digit

Check the severities in this order:

1. `1` — Breaking
2. `2` — Compatible
3. `3` — Non-observable maintenance

Use `1` when previously supported caller code can stop working, stop importing, raise a new error, or receive an incompatible result. Examples include removing public API, narrowing accepted inputs, incompatibly changing a return type, changing established output incompatibly, and dropping a supported runtime.

Use `2` when the change is additive or corrects intended behavior while supported correct usage continues to work. Examples include new public API, broader accepted inputs, compatible consumer-facing type information, and bug fixes.

Use `3` only when the public contract and functional runtime results are unchanged. Internal refactors, equivalent cache replacements, unchanged packaging internals, tests, and documentation normally use `3`.

A fix to documented or intended behavior is normally `2`, even if callers relying on the bug observe a different result.

Common classifications are:

- Added public functionality: `A2`
- Removed public functionality: `A1`
- Broadened accepted argument types: `A2`
- Narrowed accepted argument types: `A1`
- Incompatible return-type change: `A1`
- Compatible runtime bug fix with unchanged API: `B2`
- Incompatible behavior change with unchanged API: `B1`
- Internal change with identical public behavior: `C3`

Do not infer the digit from the letter. In particular, adding public API is compatible (`A2`), not breaking, and an internal change with identical results is maintenance (`C3`), not a behavior change.

## Calculate the impact

Set `Impact` to the lowest digit appearing in any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

The impact is calculated from digits only, not letters.

## Sort the bullets

Sort bullets by their complete code in this order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

For bullets with the same code, preserve their order from the supplied change list.

## Final verification

Before returning the entry, confirm that:

- The supplied version and date are unchanged.
- Every pending change has exactly one bullet.
- Every bullet starts with a valid `[A1]` through `[C3]` code.
- Each letter reflects the change's effect.
- Each digit reflects its severity independently.
- `Impact` equals the lowest bullet digit.
- Bullets are in the required code order.
- All blank lines match the template.
- The trailer is present, exact, and on the final line.