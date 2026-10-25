---
name: impact-log
description: Use this skill when given a version, release date, and pending changes to write a classified, sorted release-nototes entry in the project's machine-parseable impact-log format.
---

# Release notes

Produce exactly one entry in this form:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Use the supplied version and date unchanged. Include every pending change exactly once. Do not add introductory text, section headings, explanations, or text after the trailer.

## Classify each change

Each code has one letter and one digit. Choose them independently.

### Choose the letter

Classify what was changed:

- `A` — Public API or public type information: exported names, signatures, parameters, return types, declared public types, or metadata that makes shipped annotations discoverable by type checkers.
- `B` — Runtime implementation or behavior without a public API change: bug fixes, performance work, caching, deferred runtime work, and internal runtime refactors.
- `C` — Non-runtime project material: builds, distributions, dependency packaging or vendoring, tooling, tests, and documentation.

Important distinctions:

- A marker that exposes shipped annotations to type checkers is `A`.
- An internal runtime change is `B` even when output is unchanged.
- Dependency vendoring or packaging is `C` unless it also changes runtime behavior.
- Wheels or other distribution support are `C`.
- Documentation-only changes, including docstring examples, are `C`.
- Test-only changes are `C`.

If multiple letters apply, choose the earliest: `A`, then `B`, then `C`.

### Choose the digit

Classify the effect on consumers. Consumers include callers, installers, type checkers, and users of distributed packages.

- `1` — Breaking: previously valid, supported usage can fail, become invalid, or produce an incompatible result.
- `2` — Compatible and observable: a capability, corrected behavior, performance, type-checking result, dependency or installation result, or distribution availability changes.
- `3` — Unobservable maintenance: no consumer-visible capability, behavior, compatibility, performance, installation result, type-checking result, or distribution availability changes.

Important distinctions:

- Additive public APIs are `2`.
- Bug fixes that restore intended behavior are normally `2`, not `1`.
- Performance improvements are `2`, even when functional output is unchanged.
- Newly discoverable shipped annotations are `2`.
- Dependency or vendoring changes that affect installation are `2`.
- Newly available wheels or other distributions are `2`.
- Output-preserving internal refactors with no observable performance effect are `3`.
- Documentation-only and test-only changes are `3`.

If multiple digits apply, choose the lowest: `1`, then `2`, then `3`.

## Assemble the entry

1. Write the heading as `## [VERSION] - YYYY-MM-DD`, substituting the supplied version and date unchanged.
2. Prefix every change with its code in the form `- [CODE]`.
3. Set `Impact` to the lowest digit assigned to any bullet.
4. Sort bullets in this exact order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
5. Preserve the supplied order among changes with the same code.
6. End with exactly `<!-- stl-impact: v1 -->`. It must be the final line.