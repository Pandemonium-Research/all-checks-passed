---
name: impact-log
description: Use this guide when converting a supplied release version, date, and list of pending changes into a classified, sorted, parser-compatible release notes entry.
---

# Release notes

Follow these steps for every release.

## 1. Write the heading

Use the supplied version and date in exactly this format:

`## [VERSION] - YYYY-MM-DD`

The version must have three numeric parts, such as `1.4.0`. Write the date in year-month-day order.

## 2. Write one bullet per change

Include every pending change exactly once. Do not combine separate changes or divide one change into multiple bullets.

Use this format:

`- [LD] Description of the change.`

`L` is the impact letter and `D` is the impact digit. Classify each change independently before sorting the bullets.

## 3. Choose the impact letter

Choose the first applicable letter:

- `A` — Public API or typing surface. Use for added, removed, or modified exported names, public signatures, parameters, return types, public annotations, or shipped typing information. Making existing annotations discoverable to type checkers is `A`.
- `B` — Runtime behavior of an existing public operation. Use when results, errors, side effects, or caller-observable performance change without changing the public API or typing surface.
- `C` — Supporting material or implementation details. Use for builds, distribution artifacts, supported-platform packaging, dependencies, tooling, tests, documentation, refactoring, reorganization, or internal implementations that do not qualify for `A` or `B`.

If multiple letters apply, use this precedence:

`A` before `B` before `C`

Classify the affected surface, not the kind of engineering work. For example, a typing change is `A` even if implemented through packaging, while support for a new installation target is `C` because it does not change the package API.

## 4. Choose the impact digit

Choose the first applicable digit:

- `1` — Breaking. Correct, previously supported caller code may now fail, become invalid, or produce a different result.
- `2` — Compatible and caller-observable. Use for additive public APIs or typing support, fixes limited to previously incorrect behavior, observable performance improvements, and newly supported platforms or installation targets.
- `3` — No caller-observable effect. Use when supported usage and public behavior remain unchanged.

If multiple digits apply, use this precedence:

`1` before `2` before `3`

Apply these rules exactly:

- A bug fix is `2`, not `1`, when it changes only previously incorrect behavior and leaves correct existing usage valid.
- An additive exported API is `A2`.
- Adding shipped typing information or making shipped annotations available to type checkers is `A2`.
- A caller-observable performance improvement in an existing public operation is `B2`.
- A newly supported platform, runtime, wheel, or installation target is `C2`.
- Documentation changes, including examples, are `C3`.
- Test additions, moves, and reorganizations are `C3`.
- Internal cache, dependency, build, packaging, or implementation changes are `C3` when supported usage and public behavior remain unchanged.

Choose the letter and digit separately. Do not infer one from the other.

## 5. Sort the bullets

Sort bullets by their complete marker in exactly this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes have the same marker, preserve their supplied order.

## 6. Write the Impact summary

Immediately below the heading, write:

`Impact: D`

Replace `D` with the lowest digit used in any bullet marker. Ignore the letters.

`Impact` is not the number of changes, the most common digit, or the digit of the first sorted bullet.

## 7. Add the parser trailer

After the final bullet, add this exact line:

`<!-- stl-impact: v1 -->`

The spaces after `<!--` and before `-->` are required.

The completed entry must have this structure:

`## [VERSION] - YYYY-MM-DD`  
`Impact: D`  
`- [LD] First pending change.`  
`- [LD] Second pending change.`  
`<!-- stl-impact: v1 -->`

Before submitting, verify that:

- The supplied version and date use the exact heading format.
- Every pending change appears exactly once.
- Every bullet starts with one valid two-character marker.
- Each letter and digit was classified independently.
- Bullets follow the required marker order.
- Changes with the same marker remain in supplied order.
- `Impact` is the lowest digit present.
- The trailer matches `<!-- stl-impact: v1 -->` exactly.