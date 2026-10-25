---
name: impact-log
description: Use this skill to turn a release version, release date, and list of pending project changes into a complete, parser-compatible release notes entry in the team's impact-log format.
---

# Release notes

Create exactly one entry containing every pending change. Do not omit, merge, or invent changes.

## Required structure

Use this exact layout, with no blank lines inside the entry:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Description of change.
<!-- stl-impact: v1 -->

Replace the placeholders as follows:

- `VERSION`: the supplied three-part version number.
- `YYYY-MM-DD`: the supplied date in year-month-day format.
- `DIGIT`: the lowest digit used by any bullet.
- `CODE`: one letter immediately followed by one digit inside a single pair of brackets, such as `[A2]`.

The trailer must be exactly `<!-- stl-impact: v1 -->` and must be the entry's final line. Do not write it as plain text.

## Classify each change

Assign each pending change one letter and one digit. Decide the letter and digit independently.

### Choose the letter

Use the first matching category:

1. `A` — The public API contract changes. This includes exported names, function or method signatures, accepted argument types, return types, and additions, removals, or relocations of exported functionality.
2. `B` — The runtime behavior of an existing public call changes, but its public API contract does not.
3. `C` — The change is limited to internals, performance, supported environments, dependencies, build or packaging configuration, tooling, tests, or documentation.

If more than one letter applies, use the earliest letter: `A` before `B` before `C`. For example, a change that alters both an exported return type and runtime behavior is `A`, because the public API contract changed.

### Choose the digit

Use the first matching category:

1. `1` — Breaking or incompatible. Supported caller code, installation, or deployment may need to change. This includes removals, incompatible contract changes, deliberately changed documented behavior, and dropping a supported runtime or platform.
2. `2` — Compatible but observable. This includes additive public APIs, newly accepted inputs, new compatible behavior, and bug fixes that restore intended behavior. A bug fix remains `2` merely because inputs affected by the bug now produce the corrected result.
3. `3` — No public API or semantic runtime behavior changes. Use this for refactoring, internal caching, performance-only work, tests, documentation, tooling, or packaging migrations whose externally supported behavior remains unchanged.

If several digits could apply, use the lowest digit: `1` before `2` before `3`.

## Write and order the bullets

Write one bullet for each pending change in this form:

- `[A1] Description.`
- `[A2] Description.`
- `[B2] Description.`
- `[C3] Description.`

The examples above demonstrate syntax only. Use descriptions derived from the supplied pending changes.

Each description must state what changed and, when relevant, its compatibility effect. Put identifiers such as functions, modules, arguments, and files in backticks. End each description with a period.

Sort bullets by code in ascending letter-then-digit order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep the supplied order for bullets with the same code.

## Set the impact summary

Inspect the digits assigned to all bullets. Set `Impact` to the lowest digit present:

- Any digit `1` means `Impact: 1`.
- Otherwise, any digit `2` means `Impact: 2`.
- Otherwise, use `Impact: 3`.

Before returning the entry, verify that the heading is exact, every pending change appears once, every tag has the form `[A1]`, the bullets are sorted, the impact equals the lowest bullet digit, and the HTML trailer is the final line.