---
name: impact-log
description: Use this skill when given a release version, release date, and pending project changes that must be converted into one complete, correctly classified, stably sorted, parser-compatible impact-log entry.
---

# Release notes

Produce exactly one release entry containing every supplied pending change exactly once.

Do not merge changes, split a change across bullets, omit changes, duplicate changes, or invent facts. Return only the completed entry.

## Procedure

Follow these steps in order:

1. Record each pending change and its original position.
2. Assign each change one letter using the letter rules.
3. Independently assign each change one digit using the digit rules.
4. Combine the letter and digit into a code.
5. Stably sort the changes by the required code order.
6. Set `Impact` to the lowest digit assigned to any change.
7. Render and verify the entry.

Do not arrange bullets until every change has been classified.

## Required output

Use this exact structure, repeating the bullet line for every pending change:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Description.
<!-- stl-impact: v1 -->

There must be no blank lines anywhere inside the entry.

Substitute:

- `VERSION` with the supplied version exactly as given.
- `YYYY-MM-DD` with the supplied release date exactly as given.
- `DIGIT` with the lowest digit appearing in any bullet code.
- `CODE` with one classification letter immediately followed by one digit.

The heading must contain exactly one literal pair of square brackets around the version: `## [VERSION] - YYYY-MM-DD`.

The final line must be exactly `<!-- stl-impact: v1 -->`.

## Assign the letter

Choose the first applicable letter. Letter priority is `A`, then `B`, then `C`.

### `A` — Public API contract

Use `A` when the declared public API contract changes, including:

- Adding, removing, renaming, or relocating exported functionality.
- Adding, removing, or changing public parameters.
- Changing public signatures, accepted types, or return types.
- Adding or changing public type annotations.

Public type-annotation changes are `A` even when runtime behavior is unchanged.

### `B` — Public behavior

Use `B` when an existing public call has different observable behavior but its declared API contract does not change.

Observable behavior includes different results, errors, or state changes.

### `C` — Neither public API nor public behavior

Use `C` when neither the declared public API contract nor the semantic behavior of a public call changes.

This includes:

- Internals and refactoring.
- Performance and resource use.
- Runtime or platform support.
- Dependencies and packaging.
- Builds, tooling, tests, and documentation.
- Packaging markers that expose annotations already present in the package.

A memory- or resource-leak fix is `C` when it does not change the public API or public-call semantics. Its digit must still be selected independently.

## Assign the digit

Choose the first applicable digit. Digit priority is `1`, then `2`, then `3`.

### `1` — Breaking or incompatible

Use `1` when supported callers, installations, or deployments may require changes, including:

- Removing public functionality or parameters.
- Making an incompatible public contract change.
- Dropping a supported runtime or platform.
- Intentionally changing previously documented public behavior.

When an existing public call changes behavior, use `1` unless the supplied change explicitly calls the change a bug fix, correction, or restoration of intended behavior. Do not assume that preferable behavior is corrective.

### `2` — Compatible addition or explicit correction

Use `2` for:

- Compatible public API additions.
- New optional public capabilities.
- Newly accepted inputs.
- Changes explicitly described as fixes, corrections, or restorations of intended behavior.

An explicit bug fix remains digit `2` even if it concerns memory, resource use, or other non-semantic internals. For example, a leak described as fixed is `C2`, not `C3`, when the public API and public-call semantics remain unchanged.

A corrective public-behavior change is `B2`, even though affected inputs now produce different results.

### `3` — No compatibility or semantic change

Use `3` for changes that are neither incompatible, observably additive, nor explicitly corrective, including:

- Public type-annotation-only changes.
- Packaging markers for already-shipped annotations.
- Refactoring and internal cache changes.
- Performance or resource-use improvements not described as bug fixes.
- Tests, documentation, and tooling.
- Compatible dependency, packaging, or configuration migrations.

Do not use `3` for a change explicitly described as a fix merely because it also improves performance or resource use.

## Common code combinations

Use these combinations as classification checks:

- Incompatible public API change: `A1`
- Compatible public API addition: `A2`
- Public type-annotation-only change: `A3`
- Intentional public behavior change not identified as corrective: `B1`
- Explicit public behavior bug fix: `B2`
- Dropped supported environment with no public API or semantic change: `C1`
- Explicit internal, memory, or resource bug fix: `C2`
- Internal optimization, tooling, documentation, compatible dependency migration, or existing-annotation packaging marker: `C3`

The letter and digit are independent. A change can therefore be `A3`, `B2`, `C1`, or `C2`.

## Write the bullets

Use exactly this syntax:

- [A1] Description.

For every description:

- State only the supplied change.
- Include a supplied compatibility effect when relevant.
- Do not infer or add a compatibility claim.
- Put functions, classes, modules, arguments, files, and similar identifiers in backticks.
- End with a period, without adding a second period when one is already present.

## Sort the bullets

Sort the complete bullet list by this exact code order:

1. `A1`
2. `A2`
3. `A3`
4. `B1`
5. `B2`
6. `B3`
7. `C1`
8. `C2`
9. `C3`

This is a stable sort:

- Every bullet with an earlier code must precede every bullet with a later code.
- Changes with the same code must remain in their original supplied order.
- Never alphabetize, prioritize, or otherwise rearrange changes within the same code.
- If every change has the same code, preserve the entire supplied order.

## Set the impact summary

Set `Impact` from the bullet digits only:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

## Final verification

Before returning the entry, verify all of the following:

- The heading is exactly `## [VERSION] - YYYY-MM-DD` after substitution.
- The version and date exactly match the supplied values.
- Every supplied change appears once, and only once.
- The number of bullets equals the number of supplied changes.
- Every bullet contains exactly one valid code.
- Every letter and digit was selected independently.
- Public type-annotation-only changes use `A3`.
- Packaging markers for existing annotations use `C3`.
- Intentional public behavior changes not identified as fixes use digit `1`.
- Explicit bug fixes use digit `2`, including internal leak fixes.
- Dropped supported environments use `C1`.
- Bullets follow the exact code order.
- Changes sharing a code retain their original supplied order.
- `Impact` is the lowest digit used by any bullet.
- No blank lines occur inside the entry.
- The exact HTML trailer is the final line.