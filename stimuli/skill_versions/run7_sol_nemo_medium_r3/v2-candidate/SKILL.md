---
name: impact-log
description: Use this skill when given a release version, release date, and pending project changes that must be formatted as one parser-compatible impact-log release notes entry.
---

# Release notes

Produce exactly one release entry. Include every supplied pending change exactly once. Do not combine changes, omit them, split one change into multiple bullets, or add information that was not supplied.

## Output structure

Return only the entry, using this exact layout with no blank lines:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Description.
<!-- stl-impact: v1 -->

Replace:

- `VERSION` with the supplied three-part version number.
- `YYYY-MM-DD` with the supplied release date.
- `DIGIT` with the lowest digit assigned to any bullet.
- `CODE` with one classification letter followed immediately by one digit, inside one pair of brackets.

The final line must be exactly `<!-- stl-impact: v1 -->`.

## Classify every change

Assign the letter and digit separately. Do not infer the letter from the digit or the digit from the letter.

### Step 1: Assign the letter

Use the first applicable category:

1. `A` — The declared public API contract changes.
   This includes adding, removing, renaming, or relocating exported functionality; changing public signatures, parameters, accepted types, return types, or public type annotations.
2. `B` — The observable semantic behavior of an existing public call changes without changing its declared public API contract.
   This includes changed results, error behavior, state changes, or other caller-visible semantics.
3. `C` — Neither the declared public API nor the semantic behavior of a public call changes.
   This includes internals, performance or resource-use work, supported runtimes or platforms, dependencies, build and packaging configuration, tooling, tests, and documentation.

Apply these rules carefully:

- Adding or changing public type annotations is `A`, even when runtime execution is unchanged.
- Adding an optional public parameter or exported function is `A`.
- Dropping a supported runtime or platform is `C`, because it changes the supported environment rather than the project API.
- A performance optimization or memory-leak fix is `C` when public call semantics remain unchanged.
- If multiple letters apply, choose the earliest: `A` before `B` before `C`.

### Step 2: Assign the digit

Use the first applicable category:

1. `1` — Breaking or incompatible.
   Supported callers, installations, or deployments may need changes. Use `1` for removals, incompatible contract changes, dropped supported environments, and intentional changes to previously documented behavior.
2. `2` — Compatible but observably additive or corrective.
   Use `2` for additive public APIs, new optional capabilities, newly accepted inputs, and bug fixes that restore intended behavior.
3. `3` — No public API or semantic behavior change.
   Use `3` for refactoring, performance or resource-use improvements, internal caching, tests, documentation, tooling, and configuration migrations that preserve supported behavior.

For an existing public call whose output or behavior changes:

- Use digit `2` only when the pending change explicitly identifies the change as a bug fix or restoration of intended behavior.
- Otherwise, treat the behavior change as intentional and use digit `1`.
- Do not assign digit `2` merely because the new behavior seems preferable.
- A bug fix remains digit `2` even though affected inputs now produce different results.

If multiple digits apply, choose the lowest: `1` before `2` before `3`.

## Write the bullets

Use this exact syntax:

- `[A1] Description.`

For every description:

- State what changed.
- State the compatibility effect when it is relevant.
- Put identifiers such as functions, classes, modules, arguments, and files in backticks.
- End with a period.
- Use only information present in the supplied pending change.

## Sort the bullets

Sort by code in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes assigned the same code.

## Set the impact summary

Set `Impact` to the lowest digit appearing in any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

## Final verification

Before returning the entry, confirm that:

- The version and date match the supplied values.
- Every pending change appears exactly once.
- Every bullet has one valid `[CODE]`.
- Letters and digits were decided independently.
- Intentional public behavior changes use digit `1`.
- Explicit corrective bug fixes use digit `2`.
- Dropped supported environments use letter `C` and digit `1`.
- Public type-annotation changes use letter `A`.
- Bullets are in the required order.
- `Impact` equals the lowest bullet digit.
- There are no blank lines inside the entry.
- The HTML trailer is exact and is the final line.