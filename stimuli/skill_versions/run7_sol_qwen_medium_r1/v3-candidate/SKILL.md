---
name: impact-log
description: Use this skill when given a release version, ISO date, and pending project changes to classify each change by compatibility impact and produce one parser-compatible release-notes entry.
---

# Release notes

Create exactly one entry. Include every pending change exactly once.

Use this structure:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace all placeholders with supplied values. Do not add blank lines within the entry. The HTML comment must appear exactly as shown and be the final line.

## Classify each change

Classify the change's consumer-visible effect, not the implementation used to produce it. Determine the letter and digit independently.

When one pending change has multiple effects, use the highest-priority applicable letter and the lowest applicable digit.

### Choose the letter

Check these categories in order and stop at the first match:

1. `A` — The public API or static interface changes. This includes exported names, public modules, signatures, parameters, accepted input types, return types or shapes, public annotations, exported exception types, and shipped typing metadata.
2. `B` — An existing public operation keeps the same API but changes at runtime. This includes returned values, raised exceptions, side effects, CLI results or exit status, execution speed, startup time, and import time.
3. `C` — The change affects documentation, internals, builds, packaging, dependencies, tooling, or tests without qualifying as `A` or `B`.

Apply these distinctions:

- Adding, removing, or renaming a public name is `A`.
- Adding an optional parameter is `A`, even when its default preserves existing behavior.
- Changing a public return type or shape is `A`; changing only the value produced by the same interface is `B`.
- Adding exported exception classes is `A`; changing which exception an existing call raises is `B`.
- Shipping metadata that exposes annotations to type checkers is `A`, even though the metadata is packaged as a file.
- A runtime, startup, or import-time improvement is `B`, even when implemented entirely through an internal optimization.
- An internal replacement is `C` only if public behavior and consumer-visible performance remain unchanged.
- Documentation and docstring changes are `C`.
- Packaging and dependency changes are `C` unless they also change the public API or runtime behavior.

### Choose the digit

Check these digits in order and stop at the first match:

1. `1` — Breaking. A previously supported or successful consumer use can now fail, return a semantically different result, expose a different public type or exception, or require a consumer change.
2. `2` — Compatible but consumer-observable. The change adds capability, supports a new use, fixes a previously failing use while preserving successful uses, improves performance, adds consumer-facing documentation, exposes typing information, or compatibly changes installation behavior.
3. `3` — Consumer-unobservable. Public interfaces, semantic runtime behavior, consumer-visible performance, documentation, and installation behavior are all unchanged.

The change's label—feature, fix, refactor, optimization, or migration—does not determine its digit.

Use these required classifications:

- New public API: `A2`.
- Removed or renamed public API: `A1`.
- New optional parameter with a behavior-preserving default: `A2`.
- Broadened accepted input type: `A2`.
- Narrowed accepted input type: `A1`.
- Changed public return type or shape for an existing successful use: `A1`.
- Changed result or exception for an existing successful invocation without an API change: `B1`, even when correcting a bug.
- Fix for a case that previously failed, with existing successful cases preserved: `B2`.
- Performance, startup-time, or import-time improvement with unchanged semantic results: `B2`. Improved timing is compatible, not breaking or unobservable.
- Shipped typing metadata recognized by consumers' type checkers: `A2`.
- Consumer-facing documentation or docstring addition: `C2`.
- Compatible runtime dependency addition, removal, or vendoring that changes installed artifacts or dependency resolution: `C2`.
- Packaging or dependency change that breaks installation or requires consumer action: `C1`.
- Development-only dependency, test, or tooling change with no consumer effect: `C3`.
- Internal implementation change with unchanged behavior and consumer-visible performance: `C3`.

## Write and order the bullets

Write one concise bullet for each supplied pending change. State what changed and retain any compatibility detail needed to justify its classification. Do not invent effects that were not supplied.

Sort bullets in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes with the same code.

Set `Impact` to the smallest digit used by any bullet, regardless of its letter.

Before returning the entry, verify all of the following:

- The heading is exactly `## [VERSION] - YYYY-MM-DD` with the supplied version and date.
- The entry contains no blank lines.
- Every pending change appears once and only once.
- Every bullet starts with one valid `[A-C][1-3]` code.
- Public API and typing changes use `A`.
- Runtime and performance changes use `B` when no `A` effect applies.
- Compatible performance improvements use digit `2`.
- Consumer-visible documentation and installation changes do not use digit `3`.
- Bullets follow the required code order.
- `Impact` is the smallest bullet digit.
- `<!-- stl-impact: v1 -->` is the exact final line.