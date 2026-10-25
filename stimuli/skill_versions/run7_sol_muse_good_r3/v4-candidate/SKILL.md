---
name: impact-log
description: Use this skill when given a version, release date, and pending changes to produce one complete, classified, sorted release-notes entry in the project's machine-parseable impact-log format.
---

# Release notes

Produce exactly one entry using the supplied version, date, and pending changes.

Use this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Use the supplied version and date exactly. Do not correct, normalize, infer, or increment the version. Include every pending change exactly once, without adding unrelated changes.

## Classify each change

Each code consists of one letter and one digit. Determine them independently.

### Letter: area changed

- `A` — Public API or public type information. Use this for exported names, signatures, parameters, return types, declared public types, and packaging markers that make shipped annotations available to type checkers.
- `B` — Runtime implementation or behavior without a public API change. Use this for bug fixes, performance changes, caching changes, deferred runtime work, and internal runtime refactors, including output-preserving refactors.
- `C` — Non-runtime project material. Use this for builds, distribution packaging, dependency packaging or vendoring, tooling, tests, and documentation.

Apply these rules:

- A runtime implementation change remains `B` when its output is unchanged.
- A documentation-only or test-only change is `C`.
- Adding distribution support for an interpreter or platform is `C`.
- A dependency packaging or vendoring change is `C` unless it also changes runtime behavior.
- A marker that exposes shipped annotations to type checkers is `A`.
- If multiple letters apply, choose the first in this order: `A`, `B`, `C`.

### Digit: effect on consumers

Consumers include callers, installers, type checkers, and users of supported distributions.

- `1` — Breaking. Previously valid, supported usage can now fail, become invalid, or produce an incompatible result.
- `2` — Compatible and observable. Use this for additive APIs, bug fixes that restore intended behavior, performance improvements, newly discoverable type information, installation or dependency changes, and newly available distributions.
- `3` — Unobservable maintenance. Use this when there is no consumer-visible change to capability, behavior, compatibility, performance, installation, distribution availability, or tool results.

Apply these rules:

- A bug fix is normally `2`, even if correcting the bug changes output. Use `1` only when previously supported behavior becomes incompatible.
- A performance improvement is `2`, even when functional output is unchanged.
- An output-preserving internal refactor with no observable performance effect is `3`.
- New distribution availability is `2`.
- Documentation-only and test-only changes are `3`, even when useful.
- If multiple digits apply, choose the lowest: `1`, then `2`, then `3`.

## Assemble the entry

1. Write the heading as `## [VERSION] - YYYY-MM-DD`, substituting the supplied version and date unchanged.
2. Write `Impact: DIGIT`, using the lowest digit assigned to any bullet.
3. Prefix each pending change with its code in the form `- [A2]`, `- [B3]`, or equivalent.
4. Sort bullets in this exact code order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
5. Preserve the supplied order among changes with the same code.
6. End with exactly `<!-- stl-impact: v1 -->`. It must be the final line.
7. Do not add introductory text, explanations, blank sections, or text after the trailer.