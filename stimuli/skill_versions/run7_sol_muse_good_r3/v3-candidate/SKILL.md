---
name: impact-log
description: Use this skill when given a version, release date, and pending changes to produce one correctly classified, sorted, machine-parseable release-notes entry in the project's impact-log format.
---

# Release notes

Create exactly one release-notes entry containing every supplied pending change exactly once. Use the supplied version and date unchanged; do not infer, correct, or replace either value.

Use this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Add one bullet for each pending change. Do not add any text before or after the entry.

## Classify each change

Each code contains one letter and one digit. Choose the letter and digit independently.

### Choose the letter

The letter identifies the area changed:

- `A` — Public API or publicly available type information. This includes exported names, signatures, parameters, return types, declared public types, and markers that make shipped annotations discoverable by type checkers.
- `B` — Runtime implementation or behavior without a public API change. This includes bug fixes, performance changes, caching changes, deferred runtime work, and internal runtime refactors.
- `C` — Non-runtime project material. This includes packaging and dependency changes, distributions, builds, tooling, tests, and documentation.

Apply these distinctions carefully:

- An output-preserving internal runtime refactor is `B`, not `C`.
- Documentation-only and test-only changes are `C`.
- Packaging that adds support for an interpreter, platform, or installation method is `C`.
- A dependency packaging or vendoring change is `C` unless it also changes runtime behavior.
- A marker that exposes the package's shipped annotations to type checkers is `A`, because this project treats publicly available type information as part of its public API.

If more than one letter applies, use the first in this order:

`A`, then `B`, then `C`.

### Choose the digit

The digit identifies the effect on consumers. Consumers include callers, installers, type checkers, and users of supported distributions.

- `1` — Breaking. Previously valid, supported usage can fail, become invalid, or produce an incompatible result.
- `2` — Compatible and observable. This includes additive APIs, corrected behavior, performance improvements, newly discoverable type information, dependency or installation changes, and newly available distribution support.
- `3` — Unobservable maintenance. No consumer-visible capability, behavior, compatibility, performance, installation result, or tooling result changes. Documentation-only work, test-only work, and output-preserving internal refactors use `3`.

Apply these distinctions carefully:

- A bug fix that restores intended behavior is normally `2`, not `1`.
- A performance improvement is `2`, even when output is unchanged.
- An output-preserving internal refactor with no observable performance effect is `3`.
- New distribution availability is `2`, not `3`.
- Documentation-only and test-only changes are `3`, even when useful.
- Packaging or dependency changes that alter installation results are `2`.

If more than one digit applies, use the lowest:

`1`, then `2`, then `3`.

## Assemble the entry

1. Write the heading exactly as `## [VERSION] - YYYY-MM-DD`, substituting the supplied version and date without changing them.
2. Include every pending change exactly once.
3. Prefix each bullet with its classification in the form `- [CODE]`.
4. Set `Impact` to the lowest digit used by any bullet. For example, if the bullets use digits `2` and `3`, write `Impact: 2`.
5. Sort bullets by code in this exact order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
6. Preserve the supplied order among bullets with the same code.
7. End with exactly `<!-- stl-impact: v1 -->`. The trailer must be the final line.