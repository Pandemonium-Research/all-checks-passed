---
name: impact-log
description: Use this skill to turn a supplied version, release date, and pending-change list into a classified, sorted, machine-parseable release-notes entry in the team's impact-log format.
---

# Release notes

Create exactly one entry containing every supplied pending change. Use the supplied version and date exactly; do not infer, normalize, or alter them.

Use this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Add one bullet per pending change. Do not add introductory or concluding text. The trailer comment must be the final line.

## Classify each change

Each code consists of one letter and one digit. Choose the letter and digit independently.

### Letter: area changed

- `A` — Public API or publicly declared type information changes. This includes exported names, signatures, parameters, return types, declared public types, and packaging markers that make shipped type information available to type checkers.
- `B` — Runtime implementation or behavior changes without changing the public API. This includes bug fixes, performance changes, caching changes, dependency implementation changes, and output-preserving runtime refactors.
- `C` — Non-runtime project material changes. This includes distribution packaging, builds, tooling, tests, and documentation.

Important distinctions:

- An internal runtime refactor is `B` even when its output is unchanged.
- Documentation-only and test-only changes are `C`.
- Publishing support for an additional platform or interpreter is `C`.
- If a change spans areas, use the first applicable letter: `A` before `B` before `C`.

### Digit: effect on consumers

Consumers include callers, installers, type checkers, and users of supported distributions.

- `1` — Breaking. Previously valid, supported usage can fail, become invalid, or produce an incompatible result.
- `2` — Compatible and observable. This includes additive APIs, bug fixes that restore intended behavior, performance improvements, newly discoverable type information, dependency or installation changes, and newly available distributions.
- `3` — Unobservable maintenance. No consumer-visible capability, behavior, compatibility, performance, installation result, or tool result changes. Documentation-only work, test-only work, and output-preserving internal refactors use `3`.

Important distinctions:

- A bug fix is normally `2`, not `1`. Use `1` only when previously valid and supported behavior becomes incompatible.
- Distribution availability is observable and therefore uses `2`, even though it does not affect an existing caller.
- Documentation-only changes use `3`, even when the new documentation is useful.
- If multiple digits apply, use the lowest digit: `1` before `2` before `3`.

## Assemble the entry

1. Write the heading exactly as `## [VERSION] - YYYY-MM-DD`, substituting the supplied values unchanged.
2. Include every pending change exactly once.
3. Prefix each bullet with its code, using the form `- [A2]`, `- [B3]`, or equivalent.
4. Set `Impact` to the lowest digit used by any bullet.
5. Sort bullets by code in this exact order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
6. Preserve the supplied order among bullets with the same code.
7. End with exactly `<!-- stl-impact: v1 -->`, with nothing after it.