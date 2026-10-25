---
name: impact-log
description: Use this skill to classify pending project changes and write a parseable release-notes entry for a specified version and date in the team's impact-log format.
---

# Release notes

Create one entry containing every pending change exactly once.

## Required layout

Use this exact structure, including blank lines:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Change description.
- [CODE] Change description.

<!-- stl-impact: v1 -->

Requirements:

- Write the version as three numeric parts, such as `1.4.0`.
- Write the date as `YYYY-MM-DD`.
- Put the trailer `<!-- stl-impact: v1 -->` on the final line.
- Do not add text before the heading or after the trailer.

## Classify each change

Each bullet starts with one impact code: a letter followed by a digit.

Choose the letter first:

- `A` — The public API changes. This includes adding or removing exported names, changing signatures, or changing accepted argument or return types.
- `B` — The public API is unchanged, but an existing call's observable runtime behavior changes.
- `C` — Callers cannot observe the change. This includes internal-only work and changes limited to builds, packaging, tooling, tests, or documentation.

Use `A` for an additive public API change as well as for a breaking one. For example, a newly exported function or a newly accepted argument type is an `A` change.

Choose the digit independently:

- `1` — Previously working caller code can now fail or return a different result. A bug fix is still `1` when it changes the result of an input that previously completed successfully.
- `2` — The change is caller-visible but compatible. It only adds a capability or makes a previously failing or unsupported case work; all previously working calls keep the same results.
- `3` — No caller can observe any difference.

Do not classify every bug fix as `2`. Determine whether a previously successful call changes result:

- If yes, use `1`.
- If the affected case previously failed or was unsupported, use `2`.
- If nothing caller-visible changes, use `3`.

If a change matches multiple categories, use the highest-precedence letter and digit:

- Letter precedence: `A`, then `B`, then `C`.
- Digit precedence: `1`, then `2`, then `3`.

For example, a compatible public API addition is `A2`, an output change with no signature change is `B1`, and an unobservable internal optimization is `C3`.

## Order and summary

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep the original pending-change order when two bullets have the same code.

Set `Impact` to the lowest digit used by any bullet, regardless of its letter. For example, if the entry contains digits `2`, `1`, and `3`, write `Impact: 1`.