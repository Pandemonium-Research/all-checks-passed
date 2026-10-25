---
name: impact-log
description: Use this skill to convert a supplied release version, release date, and list of pending project changes into one classified, sorted, parser-compatible impact-log release notes entry.
---

# Release notes

Produce exactly one release entry. Include every supplied pending change exactly once. Do not combine changes, omit them, split one change into multiple bullets, or add information that was not supplied.

## Required output

Return only the entry. Use this exact structure with no blank lines:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Description.
<!-- stl-impact: v1 -->

Replace:

- `VERSION` with the supplied version exactly as given.
- `YYYY-MM-DD` with the supplied release date exactly as given.
- `DIGIT` with the lowest digit used by any bullet.
- `CODE` with one classification letter followed immediately by one digit.

The heading must contain exactly one pair of literal square brackets around the version. Write `## [VERSION]`, never `## VERSION`.

The final line must be exactly `<!-- stl-impact: v1 -->`.

## Classify every change

Assign the letter and digit independently. The letter identifies what changed; the digit identifies its compatibility impact.

### Assign the letter

Use the first applicable category:

1. `A` — The declared public API contract changes.
   This includes adding, removing, renaming, or relocating exported functionality and changing public signatures, parameters, accepted types, return types, or type annotations.
2. `B` — The observable semantic behavior of an existing public call changes without changing its declared public API contract.
   This includes changed results, errors, state changes, or other caller-visible semantics.
3. `C` — Neither the declared public API nor the semantic behavior of a public call changes.
   This includes internals, performance, resource use, supported runtimes or platforms, dependencies, packaging, builds, tooling, tests, and documentation.

Apply these rules:

- Adding or changing type annotations on public functions, classes, parameters, or return values is `A`, even when runtime execution is unchanged.
- Adding a packaging marker that lets type checkers discover already-shipped annotations is `C`; it does not itself add or change those annotations.
- Adding an optional public parameter or a new exported function is `A`.
- Dropping a supported runtime or platform is `C`.
- A performance improvement or memory-leak fix is `C` when public-call semantics remain unchanged.
- If multiple letters apply, choose the earliest: `A` before `B` before `C`.

### Assign the digit

Use the first applicable category:

1. `1` — Breaking or incompatible.
   Use `1` when supported callers, installations, or deployments may need changes. This includes removals, incompatible contract changes, dropped supported environments, and intentional changes to previously documented behavior.
2. `2` — Compatible and observably additive or corrective.
   Use `2` for compatible public API additions, new optional capabilities, newly accepted inputs, and explicit bug fixes that restore intended behavior.
3. `3` — No public API or semantic behavior change.
   Use `3` for type-annotation-only changes, packaging markers for already-shipped annotations, refactoring, performance or resource-use improvements, internal caching, tests, documentation, tooling, and compatible configuration or dependency migrations.

For changed behavior in an existing public call:

- Use `2` only when the supplied change explicitly identifies it as a bug fix or restoration of intended behavior.
- Otherwise, use `1`.
- Do not use `2` merely because the new behavior seems preferable.
- A bug fix remains `2` even when affected inputs now produce different results.

If multiple digits apply, choose the lowest: `1` before `2` before `3`.

## Write the bullets

Use this exact syntax:

- `[A1] Description.`

For each description:

- State what changed.
- State the compatibility effect when relevant and supplied.
- Put identifiers such as functions, classes, modules, arguments, and files in backticks.
- End with a period.
- Use only information from the supplied pending change.

## Sort the bullets

Classify all changes before arranging any bullets. Then sort the complete bullet list by this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

No bullet with an earlier code may appear after a bullet with a later code. Preserve the supplied order only among changes that have the same code.

## Set the impact summary

Set `Impact` to the lowest digit appearing in any bullet:

- If any bullet uses `1`, write `Impact: 1`.
- Otherwise, if any bullet uses `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

## Final verification

Before returning the entry, confirm that:

- The version and date exactly match the supplied values.
- The heading is exactly `## [VERSION] - YYYY-MM-DD` after substitution.
- The version has square brackets.
- Every pending change appears exactly once.
- Every bullet contains exactly one valid `[CODE]`.
- The letter and digit for each change were chosen independently.
- Packaging markers for existing shipped annotations use `C3`.
- Intentional public behavior changes use digit `1`.
- Explicit corrective bug fixes use digit `2`.
- Dropped supported environments use `C1`.
- Bullets follow the required code order.
- Changes sharing a code retain their supplied order.
- `Impact` equals the lowest bullet digit.
- There are no blank lines inside the entry.
- The exact HTML trailer is the final line.