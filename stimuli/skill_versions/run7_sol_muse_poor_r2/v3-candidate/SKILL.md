---
name: impact-log
description: Use this guide to convert a supplied release version, date, and list of pending changes into a correctly classified, sorted, parser-compatible release notes entry.
---

# Release notes

Follow every step for each release.

## 1. Write the heading

Use this exact format:

`## [VERSION] - YYYY-MM-DD`

Use the supplied version and date. The version must have three numeric parts, such as `1.4.0`. Write the date in year-month-day order.

## 2. Create one bullet per pending change

Include every pending change exactly once. Do not merge separate changes or split one change into multiple bullets.

Use this format:

`- [LD] Description of the change.`

`L` is the impact letter and `D` is the impact digit. Classify each change independently.

## 3. Choose the impact letter

Choose the first applicable letter:

- `A` — Public API or typing surface. Use when a change adds, removes, or modifies exported names, public signatures, parameters, return types, public annotations, or the availability of shipped type information to type checkers. Making existing annotations discoverable is an `A` change.
- `B` — Runtime behavior through an existing public operation. Use when results, errors, side effects, or caller-observable performance change without changing the public API or typing surface.
- `C` — Supporting material or implementation details only. Use for builds, distribution artifacts, packaging machinery, dependencies, tooling, tests, documentation, refactoring, reorganization, or internal implementation changes that do not qualify for `A` or `B`.

If several letters apply, use the earliest:

`A` before `B` before `C`

Classify the affected surface, not merely the kind of engineering work performed.

## 4. Choose the impact digit

Choose the first applicable digit:

- `1` — Breaking. Correct, previously supported caller code may now fail, become invalid, or produce a different result.
- `2` — Compatible and caller-observable. Use for additive public APIs or typing support, newly supported platforms or installation targets, observable performance improvements, and fixes limited to previously incorrect behavior.
- `3` — No caller-observable effect. Use for documentation, tests, refactoring, reorganization, or internal cache, dependency, build, and packaging changes when supported usage and public behavior remain unchanged.

If several digits apply, use the lowest:

`1` before `2` before `3`

Apply these rules carefully:

- A bug fix is `2`, not `1`, when it changes only previously incorrect behavior and correct existing usage remains valid.
- A packaging change is `2` when it adds or changes a supported installation or runtime target. Packaging maintenance that does not change supported usage is `3`.
- Documentation changes, including added examples, are `3`.
- Replacing an internal implementation while preserving public behavior is `3`.
- Adding public typing information or making shipped annotations available to type checkers is `2`, paired with letter `A`.

Choose the letter and digit separately. Any letter may be paired with any digit.

## 5. Sort the bullets

Sort bullets by their complete marker in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes with the same marker.

## 6. Write the Impact summary

Immediately below the heading, write:

`Impact: D`

Replace `D` with the lowest digit used in any bullet marker. Ignore the letters.

The Impact value is not the number of changes, the most frequent digit, or the digit on the first bullet.

## 7. Add the parser trailer

After the final bullet, add this exact line:

`<!-- stl-impact: v1 -->`

The spaces after `<!--` and before `-->` are required.

Use this complete structure:

`## [VERSION] - YYYY-MM-DD`  
`Impact: D`  
`- [LD] First pending change.`  
`- [LD] Second pending change.`  
`<!-- stl-impact: v1 -->`

Before submitting, verify that:

- The supplied version and date use the exact heading format.
- Every pending change appears exactly once.
- Every bullet begins with a valid two-character marker.
- Each letter and digit was classified independently.
- The bullets follow the required marker order.
- `Impact` is the lowest digit present.
- The trailer matches `<!-- stl-impact: v1 -->` exactly.