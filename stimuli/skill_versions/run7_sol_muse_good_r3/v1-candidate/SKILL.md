---
name: impact-log
description: Use this skill to turn a supplied version, release date, and list of pending project changes into a correctly classified, sorted, machine-parseable release-notes entry in the team's impact-log format.
---

# Release notes

Create one release-notes entry containing every supplied pending change. Use the supplied version and date exactly; do not infer or alter either value.

Use this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace the placeholders and add one bullet for each pending change. The trailer comment must be the final line.

## Classify each change

Each code consists of one letter and one digit. Choose the letter and digit independently.

### Letter: area changed

- `A` — The public API itself changes. This includes exported names, signatures, parameters, return types, and declared public types.
- `B` — Runtime implementation or behavior changes without changing the public API. This includes bug fixes, performance changes, caching changes, and internal runtime refactors.
- `C` — Non-runtime project material changes. This includes packaging and dependency metadata, distributions, builds, tooling, tests, and documentation.

Use `C`, not `A`, for packaging metadata that helps external tools discover existing type information; the public names, signatures, and declared types themselves have not changed.

Do not choose `C` merely because a runtime implementation change is invisible to callers. An internal runtime refactor is `B`; its digit may be `3`.

If a change spans multiple areas, use the first applicable letter in this precedence order:

`A` before `B` before `C`.

### Digit: effect on consumers

Treat consumers broadly: callers, installers, type-checking tools, and users of supported distributions can all observe a change.

- `1` — Breaking. Previously valid, supported usage can fail, become invalid, or produce an incompatible result.
- `2` — Compatible and observable. This includes additive APIs, behavior fixes that restore intended behavior, performance improvements, newly available distribution support, and observable packaging or dependency changes.
- `3` — Unobservable maintenance. No consumer-visible capability, behavior, compatibility, performance, installation result, or tool result changes. Documentation-only work, test-only work, and output-preserving internal refactors normally use `3`.

A corrected result from a bug fix is `2`, not automatically `1`. Use `1` only when previously valid and supported behavior becomes incompatible.

If more than one digit applies, use the lowest digit:

`1` before `2` before `3`.

## Assemble the entry

1. Write the heading exactly as `## [VERSION] - YYYY-MM-DD`.
2. Classify every pending change and prefix its bullet with the resulting code, such as `- [B2]`.
3. Set `Impact` to the lowest digit used by any bullet. For example, an entry containing digits `2` and `3` has `Impact: 2`.
4. Sort bullets by code in ascending letter-then-digit order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Preserve the supplied order when multiple bullets have the same code.
5. End with exactly `<!-- stl-impact: v1 -->`. Do not place any text after it.