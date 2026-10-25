---
name: impact-log
description: Use this skill when given a version, release date, and pending changes to produce one complete, classified, sorted release-notes entry in the project's machine-parseable impact-log format.
---

# Release notes

Produce exactly one entry in this form:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Use the supplied version and date exactly. Never infer, increment, normalize, or correct the version. Include every pending change exactly once and do not add unrelated changes.

## Classify each change

Choose the code's letter and digit independently.

### Letter: what changed

- `A` — Public API or public type information. This includes exported names, signatures, parameters, return types, declared public types, and metadata that makes shipped annotations discoverable by type checkers.
- `B` — Runtime implementation or behavior without a public API change. This includes bug fixes, performance work, caching, deferred runtime work, and internal runtime refactors, even when functional output is unchanged.
- `C` — Non-runtime project material. This includes builds, distribution packaging, dependency packaging or vendoring, tooling, tests, and documentation.

Apply these distinctions:

- A marker that exposes shipped annotations to type checkers is `A`.
- A runtime performance improvement is `B`.
- An output-preserving runtime refactor is `B`.
- Dependency packaging or vendoring is `C` unless the change explicitly alters runtime behavior.
- Wheels and other distribution support are `C`.
- Documentation-only changes, including docstring examples, are `C`.
- Test-only changes are `C`.

If more than one letter applies, choose the earliest: `A`, then `B`, then `C`.

### Digit: effect on consumers

Consumers include callers, installers, type checkers, and users of supported distributions.

- `1` — Breaking. Previously valid, supported usage can now fail, become invalid, or produce an incompatible result.
- `2` — Compatible and observable. A capability, corrected behavior, performance characteristic, type-checking result, installation or dependency result, or distribution availability changes without breaking supported usage.
- `3` — Unobservable maintenance. No consumer-visible capability, behavior, compatibility, performance, installation result, type-checking result, or distribution availability changes.

Apply these distinctions:

- Additive public APIs are `2`.
- Bug fixes that restore intended behavior are normally `2`, even when they change formerly incorrect output. Do not assign `1` merely because a bug fix changes output.
- Performance improvements are `2`, even when functional output is unchanged.
- Newly discoverable shipped annotations are `2`.
- Dependency or vendoring changes that affect installation are `2`.
- Newly available wheels or other distributions are `2`.
- Output-preserving internal refactors with no observable performance effect are `3`.
- Documentation-only and test-only changes are `3`.

If more than one digit applies, choose the lowest: `1`, then `2`, then `3`.

## Assemble the entry

1. Write the heading as `## [VERSION] - YYYY-MM-DD`, substituting the supplied version and date unchanged.
2. Prefix every change with its code in the form `- [CODE]`.
3. Set `Impact` to the lowest digit assigned to any bullet.
4. Sort bullets in this exact order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
5. Preserve the supplied order among changes with the same code.
6. End with exactly `<!-- stl-impact: v1 -->`. It must be the final line.
7. Do not add introductory text, explanations, blank sections, or text after the trailer.