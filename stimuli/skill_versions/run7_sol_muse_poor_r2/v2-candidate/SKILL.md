---
name: impact-log
description: Use this guide when converting a release version, date, and list of pending changes into a classified, sorted, parser-compatible release notes entry.
---

# Release notes

Follow these steps for every release.

## 1. Write the heading

Use exactly:

`## [VERSION] - YYYY-MM-DD`

Use the supplied version and date. The version must have three numeric parts, such as `1.4.0`, and the date must be in year-month-day order.

## 2. Create one bullet per pending change

Include every pending change exactly once. Do not merge separate changes or split one change into multiple bullets.

Use this format:

`- [LD] Description of the change.`

`L` is the impact letter and `D` is the impact digit. Determine them independently for each change.

## 3. Choose the impact letter

Choose the first applicable letter:

- `A` — Public API or typing surface. Use for changes to exported names, public call signatures, parameters, return types, public annotations, or whether shipped type information is available to type checkers. Adding `py.typed` is an `A` change.
- `B` — Runtime behavior visible through an existing public operation, with no public API or typing-surface change. Use for changed results, bug fixes, errors, side effects, or caller-observable performance.
- `C` — Everything limited to supporting material or implementation details. Use for builds, distribution artifacts, packaging machinery, dependencies, tooling, tests, documentation, refactoring, or internal implementation changes that do not qualify for `A` or `B`.

When more than one letter applies, use the earliest one:

`A` before `B` before `C`

Classify the affected surface, not the type of work. For example, an internal cache replacement with unchanged behavior is `C`, while an observable performance improvement through the public API is `B`.

## 4. Choose the impact digit

Choose the first applicable digit:

- `1` — Breaking. Correct, previously supported caller code may now fail, become invalid, or produce a different result.
- `2` — Compatible and externally useful. Use for additive public APIs or typing support, newly supported platforms or installation targets, caller-observable performance improvements, and fixes limited to previously incorrect behavior.
- `3` — No caller-observable effect. Use for documentation, tests, refactoring, reorganization, or internal cache and dependency changes when public behavior and supported usage remain unchanged.

When more than one digit applies, use the lowest one:

`1` before `2` before `3`

Apply these distinctions carefully:

- A bug fix is normally `2`, not `1`, when only previously erroneous behavior changes and correct existing usage remains valid.
- A packaging-related change is `2` when it adds or changes a supported installation or runtime target, such as publishing wheels for a newly supported Python version. Packaging maintenance that does not change supported usage is `3`.
- Documentation examples are `3`; clearer documentation alone is not an externally useful software behavior change.
- An implementation replacement with unchanged output is `3`.
- Adding public typing information or making shipped annotations discoverable is `2`, paired with letter `A`.

Any letter may be paired with any digit. Do not infer the digit from the letter.

## 5. Sort the bullets

Sort bullets by the complete marker in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes that have the same marker.

## 6. Write the Impact summary

Immediately below the heading, write:

`Impact: D`

Replace `D` with the lowest digit used by any bullet. Ignore the letters.

The Impact value is not the number of changes, the most common digit, or the digit on the first bullet.

## 7. Add the parser trailer

After the final bullet, add this exact line:

`<!-- stl-impact: v1 -->`

The spaces after `<!--` and before `-->` are required. Do not use `<!--stl-impact: v1-->`.

The completed entry must have this structure:

## [VERSION] - YYYY-MM-DD
Impact: D
- [LD] First pending change.
- [LD] Second pending change.
<!-- stl-impact: v1 -->

Before submitting, verify:

- The supplied version and date appear in the exact heading format.
- Every pending change appears exactly once.
- Every bullet begins with a valid two-character marker.
- Each letter and digit was classified independently.
- The bullets follow the required marker order.
- `Impact` is the lowest digit present.
- The trailer matches `<!-- stl-impact: v1 -->` exactly.