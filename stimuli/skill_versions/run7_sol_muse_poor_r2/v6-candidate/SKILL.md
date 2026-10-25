---
name: impact-log
description: Use this guide to convert a supplied version, date, and list of pending changes into a correctly classified, sorted, parser-compatible release notes entry.
---

# Release notes

Apply the following procedure to every release.

## 1. Write the heading

Use the supplied version and date in exactly this format:

`## [VERSION] - YYYY-MM-DD`

The version must contain three numeric parts, such as `1.4.0`. The date must use year-month-day order.

## 2. Create one bullet per change

Include every pending change exactly once. Do not combine changes or split one change across multiple bullets.

Each bullet must use this format:

`- [LD] Description of the change.`

Classify every change before sorting it:

- `L` is its impact letter.
- `D` is its impact digit.

Choose the letter and digit independently. A letter does not imply a particular digit.

## 3. Choose the impact letter

Test the affected surface in this order and use the first match:

1. `A` — Public API or public typing surface.
2. `B` — Observable runtime behavior of an existing public operation.
3. `C` — Supporting material or internal implementation.

Use `A` for changes to:

- Exported names.
- Public functions, methods, parameters, or signatures.
- Public return types or annotations.
- Shipped typing information.
- Whether type checkers can discover shipped annotations.

Use `B` when an existing public operation changes its:

- Results or errors.
- Side effects.
- Runtime behavior.
- Caller-observable performance.

Use `C` for changes limited to:

- Builds or distribution artifacts.
- Supported-platform packaging.
- Dependencies.
- Tooling.
- Tests.
- Documentation.
- Refactoring or file reorganization.
- Internal implementations whose public behavior is unchanged.

If more than one letter appears applicable, use this precedence:

`A` before `B` before `C`

Classify the affected surface, not the engineering mechanism. For example, making annotations discoverable through packaging is still `A`, while publishing an artifact for a newly supported platform is `C`.

## 4. Choose the impact digit

Test the effect in this order and use the first match:

1. `1` — Breaking.
2. `2` — Compatible and externally useful or observable.
3. `3` — No caller-observable effect.

Use `1` only when correct, previously supported caller code can now fail, become invalid, or produce a different result.

Use `2` for compatible changes such as:

- Adding a public API.
- Adding public typing support or making shipped annotations discoverable.
- Fixing previously incorrect behavior while preserving correct existing usage.
- Improving caller-observable performance.
- Adding support for a platform, runtime, wheel, or installation target.

Use `3` when supported usage and public behavior remain unchanged, including:

- Documentation and examples.
- Test additions, moves, or reorganizations.
- Refactoring.
- Internal cache or implementation replacements.
- Dependency vendoring or replacement with unchanged behavior.
- Build or packaging maintenance that does not add or remove a supported target.

If more than one digit appears applicable, use this precedence:

`1` before `2` before `3`

Apply these common classifications exactly:

- An additive exported API is `A2`.
- Newly available public typing information is `A2`.
- A compatible runtime bug fix is `B2`, even if previously incorrect output changes.
- An observable performance improvement in an existing public operation is `B2`.
- A newly supported platform, runtime, wheel, or installation target is `C2`.
- Documentation and test-only changes are `C3`.
- Behavior-preserving internal, dependency, build, and packaging changes are `C3`.

Do not classify a bug fix as breaking merely because its output changes. It is `1` only if correct, previously supported usage is broken.

## 5. Sort the bullets

Sort bullets by their complete marker in exactly this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order of changes that have the same marker.

## 6. Write the Impact summary

Immediately below the heading, write:

`Impact: D`

Replace `D` with the lowest digit used by any bullet. Ignore the letters.

For example, an entry containing digits `2`, `3`, and `3` has:

`Impact: 2`

The Impact value is not:

- The number of changes.
- The most common digit.
- The digit on the first bullet after sorting.

## 7. Add the parser trailer

After the final bullet, add this exact line:

`<!-- stl-impact: v1 -->`

The spaces after `<!--` and before `-->` are required. Do not change, omit, or move the trailer.

## Required entry structure

The completed entry must contain only this structure:

`## [VERSION] - YYYY-MM-DD`  
`Impact: D`  
`- [LD] First pending change.`  
`- [LD] Next pending change.`  
`<!-- stl-impact: v1 -->`

Before submitting, verify that:

- The supplied version and date appear in the exact heading format.
- Every pending change appears exactly once.
- Every bullet begins with one valid two-character marker.
- Each letter and digit was chosen independently.
- Public API and typing-surface changes use `A`.
- Compatible runtime fixes and performance improvements use `B2`.
- Newly supported installation or platform targets use `C2`.
- Documentation, tests, and behavior-preserving internal changes use `C3`.
- Bullets follow the required marker order.
- Changes sharing a marker remain in supplied order.
- `Impact` is the lowest digit present.
- The trailer is exactly `<!-- stl-impact: v1 -->`.