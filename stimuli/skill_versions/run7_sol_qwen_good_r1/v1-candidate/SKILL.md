---
name: impact-log
description: Use this skill to turn a release version, release date, and list of pending project changes into a correctly classified, ordered, and machine-parseable release-notes entry.
---

# Release notes

Produce exactly one release entry in the house impact-log format.

## Required structure

Use this structure:

## `[VERSION] - YYYY-MM-DD`
Impact: `DIGIT`

- `[CODE]` Change description.
- `[CODE]` Change description.

`<!-- stl-impact: v1 -->`

Apply these formatting rules:

- Use the supplied version in three-part form inside square brackets.
- Use the supplied date in `YYYY-MM-DD` form.
- Put `Impact: DIGIT` immediately below the heading.
- Start every bullet with its impact code in square brackets. Do not put the code at the end.
- Leave one blank line before the bullets and one blank line before the trailer.
- Make `<!-- stl-impact: v1 -->` the final line, with nothing after it.

## Classify every change

Each impact code consists of one letter and one digit.

Choose the letter by what the change affects:

- `A` — Public API surface: exported names, signatures, parameters, return types, or other public types.
- `B` — Runtime behavior of an existing call changes without a public API-surface change.
- `C` — Internals, build, packaging, dependencies, tooling, tests, or documentation only.

Choose the digit by compatibility:

- `1` — Breaking: previously working caller code can fail or produce a different result.
- `2` — Compatible: additive change or fix; correct existing caller code continues to work.
- `3` — Unobservable: callers cannot observe the change.

Combine the selected letter and digit, such as `[A2]` or `[C3]`.

If more than one classification applies, use the highest-precedence value:

- Letter precedence: `A` before `B` before `C`.
- Digit precedence: `1` before `2` before `3`.

Assess each change independently. Do not assign every bullet the release-level impact digit.

## Order the bullets

Sort bullets by their complete codes in ascending letter-first order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep bullets with the same code in a clear, stable order.

## Calculate the impact summary

Set the `Impact` value to the lowest digit used by any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

The letter does not affect the summary value.