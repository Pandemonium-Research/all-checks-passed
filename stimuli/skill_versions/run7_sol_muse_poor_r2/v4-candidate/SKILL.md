---
name: impact-log
description: Use this guide to turn a supplied version, date, and list of pending changes into a classified, sorted, parser-compatible release notes entry.
---

# Release notes

Follow these steps for every release.

## 1. Write the heading

Use the supplied version and date in exactly this format:

`## [VERSION] - YYYY-MM-DD`

The version must contain three numeric parts, such as `1.4.0`. Write the date in year-month-day order.

## 2. Create the bullets

Include every pending change exactly once. Do not merge separate changes or split one change into multiple bullets.

Each bullet must have this format:

`- [LD] Description of the change.`

The two-character marker consists of:

- `L`: the impact letter, describing the affected surface.
- `D`: the impact digit, describing the severity.

Choose the letter and digit independently for each change. Any valid letter may be paired with any valid digit.

## 3. Choose the impact letter

Choose the first applicable letter:

- `A` — Public API or typing surface. Use when the change adds, removes, or modifies exported names, public signatures, parameters, return types, public annotations, or the availability of shipped type information to type checkers.
- `B` — Observable runtime behavior of an existing public operation. Use when results, errors, side effects, or caller-observable performance change without changing the public API or typing surface.
- `C` — Supporting material or implementation details. Use for builds, distribution artifacts, packaging machinery, dependencies, tooling, tests, documentation, refactoring, reorganization, or internal implementation changes that do not qualify for `A` or `B`.

If multiple letters apply, choose the earliest:

`A` before `B` before `C`

Classify the affected surface, not merely the kind of engineering work performed. In particular:

- An additive exported API is `A`.
- Making shipped annotations discoverable to type checkers is `A`.
- An observable speed improvement in an existing public operation is `B`.
- A runtime bug fix that does not change the public API is `B`.
- A distribution or supported-platform change remains `C`; its external usefulness affects the digit, not the letter.
- An internal replacement with unchanged public behavior is `C`.

## 4. Choose the impact digit

Choose the first applicable digit:

- `1` — Breaking. Correct, previously supported caller code may now fail, become invalid, or produce a different result.
- `2` — Compatible and externally useful. Use for additive public APIs or typing support, newly supported platforms or installation targets, caller-observable performance improvements, and fixes limited to previously incorrect behavior.
- `3` — No caller-observable effect. Use when supported usage and public behavior remain unchanged, including documentation, tests, refactoring, reorganization, and internal implementation, dependency, build, or packaging maintenance.

If multiple digits apply, choose the lowest:

`1` before `2` before `3`

Apply these distinctions exactly:

- A bug fix is normally `2`, not `1`, when only previously incorrect behavior changes and correct existing usage remains valid.
- A newly supported installation or runtime target is `2`, even though its letter is `C`.
- Packaging maintenance that does not change supported installation or usage is `3`.
- Documentation changes, including examples, are `3`.
- Moving or reorganizing tests is `3`.
- Replacing an internal cache, dependency, or implementation while preserving public behavior is `3`.
- Adding public typing information or making shipped annotations available to type checkers is `2`, paired with letter `A`.

Do not infer the digit from the letter.

## 5. Sort the bullets

Sort bullets by their complete marker in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes with the same marker.

## 6. Write the Impact summary

Immediately below the heading, write:

`Impact: D`

Replace `D` with the lowest digit used by any bullet. Ignore the letters.

For example, if an entry contains digits `2`, `3`, and `3`, write `Impact: 2`.

The Impact value is not:

- The number of changes.
- The most common digit.
- The digit on the first bullet after sorting.

## 7. Add the parser trailer

After the final bullet, add this exact line:

`<!-- stl-impact: v1 -->`

The spaces after `<!--` and before `-->` are required. Do not omit or move them.

The completed entry must have exactly this structure:

`## [VERSION] - YYYY-MM-DD`  
`Impact: D`  
`- [LD] First pending change.`  
`- [LD] Second pending change.`  
`<!-- stl-impact: v1 -->`

Before submitting, verify that:

- The supplied version and date appear in the exact heading format.
- Every pending change appears exactly once.
- Every bullet begins with one valid two-character marker.
- Each letter and digit was classified independently.
- Typing-surface changes use letter `A`.
- Supported installation or platform additions use digit `2`.
- Documentation, test reorganization, and behavior-preserving internal changes use digit `3`.
- Bug fixes limited to previously incorrect behavior use digit `2`.
- Bullets follow the required marker order.
- `Impact` is the lowest digit present.
- The trailer matches `<!-- stl-impact: v1 -->` exactly.