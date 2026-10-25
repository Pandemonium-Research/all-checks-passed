---
name: impact-log
description: Use this skill to turn a supplied release version, release date, and list of pending project changes into one parser-compatible impact-log release notes entry.
---

# Release notes

Produce exactly one release entry. Include every supplied pending change exactly once. Do not combine changes, omit changes, split one change into multiple bullets, or add facts that were not supplied.

## Output structure

Return only the entry. Use this exact layout and do not insert blank lines:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Description.
<!-- stl-impact: v1 -->

Replace:

- `VERSION` with the supplied three-part version number. Keep the version inside one pair of square brackets.
- `YYYY-MM-DD` with the supplied release date.
- `DIGIT` with the lowest digit used by any bullet.
- `CODE` with one classification letter followed immediately by one digit, inside one pair of square brackets.

The final line must be exactly `<!-- stl-impact: v1 -->`.

## Classify each change

Determine the letter first and the digit second. They measure different things:

- The letter identifies what area changed.
- The digit identifies compatibility impact.

Do not derive either one from the other.

### Step 1: Assign the letter

Use the first applicable category:

1. `A` — The declared public API contract changes.
   This includes adding, removing, renaming, or relocating exported functionality; changing public signatures, parameters, accepted types, return types, or public type information.
2. `B` — The observable behavior of an existing public call changes without changing its declared public API contract.
   This includes changed results, errors, state changes, or other caller-visible semantics.
3. `C` — Neither the declared public API contract nor the behavior of a public call changes.
   This includes internals, performance, resource use, supported runtimes or platforms, dependencies, packaging, builds, tooling, tests, and documentation.

Apply these rules:

- Adding or changing public type annotations is `A`, even if runtime execution is unchanged.
- Making shipped annotations newly discoverable to type checkers, such as by adding a typing-package marker, is also `A`.
- Adding an optional public parameter or a new exported function is `A`.
- Dropping a supported runtime or platform is `C`, because the supported environment changes rather than the project API.
- A performance improvement or memory-leak fix is `C` when public-call semantics remain unchanged.
- If more than one letter appears applicable, choose the earliest: `A` before `B` before `C`.

### Step 2: Assign the digit

Use the first applicable category:

1. `1` — Breaking or incompatible.
   Use `1` when supported callers, installations, or deployments may need changes. This includes removals, incompatible contract changes, dropped supported environments, and intentional changes to previously documented behavior.
2. `2` — Compatible and observably additive or corrective.
   Use `2` for compatible public API additions, new optional capabilities, newly accepted inputs, newly published public typing information, and explicit bug fixes that restore intended behavior.
3. `3` — No public API, public typing, or semantic behavior change.
   Use `3` for refactoring, performance or resource-use improvements, internal caching, tests, documentation, tooling, and configuration or dependency migrations that preserve supported behavior.

Important consequences:

- A compatible addition to the public API is digit `2`, not digit `3`.
- Adding compatible public type annotations is `A2`, even when runtime behavior is unchanged.
- Making existing shipped annotations newly visible to type checkers is `A2`, unless the supplied change says the typing contract is incompatible.
- Digit `3` is not appropriate merely because runtime behavior is unchanged; a public API or public typing contract change is still observable.
- Removing or incompatibly changing public API or public typing information is digit `1`.
- For an existing public call whose output or behavior changes, use digit `2` only when the pending change explicitly calls it a bug fix or a restoration of intended behavior.
- Otherwise, treat a public behavior change as intentional and use digit `1`.
- Do not use digit `2` merely because the new behavior seems preferable.
- A bug fix remains digit `2` even when affected inputs now produce different results.
- If more than one digit appears applicable, choose the lowest: `1` before `2` before `3`.

## Write the bullets

Use this exact syntax:

- `[A1] Description.`

For every description:

- State what changed.
- State the compatibility effect when it is relevant and was supplied.
- Put identifiers such as functions, classes, modules, arguments, and files in backticks.
- End with a period.
- Use only information present in the supplied pending change.

## Sort the bullets

Sort bullets by code in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes assigned the same code.

## Set the impact summary

Set `Impact` to the lowest digit appearing in any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

## Final verification

Before returning the entry, confirm that:

- The version and date exactly match the supplied values.
- The version is enclosed in square brackets in the heading.
- Every pending change appears exactly once.
- Every bullet has exactly one valid `[CODE]`.
- Letters and digits were decided independently.
- Compatible public API and public typing additions use digit `2`.
- Intentional public behavior changes use digit `1`.
- Explicit corrective bug fixes use digit `2`.
- Dropped supported environments use letter `C` and digit `1`.
- Public type changes, including newly discoverable shipped annotations, use letter `A`.
- Bullets follow the required code order.
- Changes with the same code retain their supplied order.
- `Impact` equals the lowest bullet digit.
- There are no blank lines inside the entry.
- The HTML trailer is exact and is the final line.