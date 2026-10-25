---
name: impact-log
description: Use this document to classify pending changes and write a parseable impact-log release-notes entry for any project version and release date.
---

# Release notes

Write each release entry in this exact structure:

## [`VERSION`] - `YYYY-MM-DD`
Impact: `DIGIT`
- [`CODE`] Change description.
<!-- stl-impact: v1 -->

Replace every placeholder. Use the supplied three-part version number, date, and pending changes. Include one bullet for every pending change.

## Classify each change

Each code contains a letter and a digit, such as `[A2]`. Choose the letter and digit independently.

### Choose the letter

Use the first matching category:

1. **A — Public API or public typing contract**
   - Exported names are added, removed, or renamed.
   - Parameters, return values, accepted input types, exceptions, or annotations change.
   - A previously rejected kind of input becomes supported.
   - Shipped typing information becomes available or changes.

2. **B — Runtime behavior or implementation**
   - An existing operation changes behavior without changing its public API contract.
   - A bug is fixed.
   - Performance, caching, import timing, or another runtime characteristic changes.
   - An internal runtime implementation changes, even when callers cannot observe the result.

3. **C — Non-runtime project work**
   - Build, packaging, dependencies, tooling, tests, or documentation change.
   - No package runtime behavior or public API contract changes.

When multiple letters apply, use the earliest letter: **A before B before C**. For example, an implementation change that also alters the public contract is A, not B.

### Choose the digit

Use the first matching category:

1. **1 — Breaking**
   - Previously supported caller code must change, can now fail, or no longer receives a result guaranteed by the public contract.
   - Public names, parameters, accepted inputs, or documented behavior are removed or incompatibly changed.

2. **2 — Compatible but observable**
   - Functionality or supported input is added without breaking existing callers.
   - A bug is fixed while correct existing caller code remains compatible.
   - Users can observe a compatible change in behavior, performance, packaging, dependencies, documentation, or tooling.

3. **3 — Unobservable**
   - The change is internal and produces no externally observable difference.
   - Results, supported inputs, public signatures, installation behavior, and documented behavior remain unchanged.

Do not mark a compatible addition as 1. Do not mark a bug fix as 1 merely because the corrected result differs from the buggy result. Use 1 only when the supported contract becomes incompatible.

If one change has several effects, use the lowest applicable digit: **1 before 2 before 3**.

## Calculate the impact summary

Set `Impact:` to the lowest digit used by any bullet in the entry.

For example, if the entry contains digits 2 and 3, write `Impact: 2`. Never calculate the summary from the letters.

## Order the bullets

Sort bullets by code in ascending order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among bullets with the same code.

## Formatting requirements

- Use a level-two heading: `## [VERSION] - YYYY-MM-DD`.
- Put `Impact: DIGIT` immediately below the heading.
- Begin every change with `- [CODE]`.
- End with the literal HTML comment `<!-- stl-impact: v1 -->`.
- Make that comment the final line of the entry, with nothing after it.