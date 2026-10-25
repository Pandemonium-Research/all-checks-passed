---
name: impact-log
description: Use this skill when given a version, ISO date, and pending changes to classify their compatibility impact and produce one parser-compatible release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every pending change exactly once.

The entry must have this exact shape, with no blank lines:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace `VERSION`, `YYYY-MM-DD`, `DIGIT`, and each bullet with the supplied information. The HTML comment must be exactly `<!-- stl-impact: v1 -->` and must be the final line.

## Classify each change

Each bullet code contains one letter and one digit. Determine them independently.

### Choose the letter

Test the categories in this order and use the first match:

1. `A` — A public interface changes. This includes exported names, signatures, parameters, accepted input types, return types, public annotations, exception types exposed as API, and shipped typing metadata.
2. `B` — An existing public operation keeps the same interface but changes its runtime behavior. This includes returned values, exceptions, side effects, command-line behavior, execution speed, startup time, and import time.
3. `C` — The change concerns documentation, internals, builds, packaging, dependencies, tooling, or tests and does not qualify as `A` or `B`.

Important distinctions:

- Adding, removing, or renaming an exported name is `A`.
- Adding an optional parameter is `A`.
- Adding shipped type-checker metadata is `A`, even when it is delivered as a packaging file.
- Changing the result of an existing call without changing its interface is `B`.
- Improving runtime, startup, or import performance is `B`, even when achieved through an internal optimization.
- Replacing an internal implementation while preserving both behavior and consumer-visible performance is `C`.
- Documentation and docstring changes are `C`.
- Dependency and installation changes are `C` unless they also alter a public API or runtime behavior.

### Choose the digit

Use the first applicable digit:

1. `1` — Breaking. A previously supported or successfully working consumer use can now fail, return a semantically different result, expose a different type or exception, or require a consumer change.
2. `2` — Compatible but consumer-observable. The change adds capability, fixes a previously failing use without breaking working uses, improves performance, adds consumer-facing documentation, or compatibly changes installation behavior.
3. `3` — Consumer-unobservable. Public interfaces, semantic runtime behavior, consumer-visible performance, documentation, and installation behavior all remain unchanged.

Apply these rules to the actual effect, regardless of whether the change is described as a feature, fix, refactor, optimization, or migration.

Common classifications:

- New exported API: `A2`.
- Removed or renamed public API: `A1`.
- New optional parameter whose default preserves existing behavior: `A2`.
- Broadened accepted input type: `A2`.
- Narrowed accepted input type: `A1`.
- Changed return type, return shape, or value for a previously successful call: `A1` or `B1`, depending on whether the public interface also changed.
- Shipped typing metadata that enables type checkers to recognize existing annotations: `A2`.
- Compatible runtime performance, startup-time, or import-time improvement: `B2`. A timing improvement is not breaking merely because the measured duration changes.
- Corrected behavior that changes the result or exception of a previously successful invocation: `B1`.
- Fix for a case that previously failed, with existing successful cases preserved: `B2`.
- User-visible documentation or docstring addition: `C2`.
- Compatible addition, removal, or vendoring of a runtime dependency that changes installed artifacts or dependency resolution: `C2`.
- Dependency or packaging change that breaks installation or requires consumer action: `C1`.
- Development-only dependency, test, or tooling change with no consumer effect: `C3`.
- Internal implementation replacement with unchanged consumer behavior: `C3`.

When a change has several effects, use the highest-priority letter (`A` before `B` before `C`) and the lowest applicable digit (`1` before `2` before `3`).

## Write and order the bullets

Write one concise bullet for each pending change. State what changed and include compatibility details needed to understand its impact.

Sort bullets in this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes with the same code.

Set `Impact` to the smallest digit appearing in any bullet. For example, bullets containing digits `1`, `2`, and `3` require `Impact: 1`.

Before returning the entry, verify all of the following:

- The heading is exactly `## [VERSION] - YYYY-MM-DD` with the supplied values.
- There are no blank lines in the entry.
- Every pending change appears once and only once.
- Every bullet begins with one valid code matching `[A-C][1-3]`.
- Letters reflect the public API, runtime behavior, and non-runtime distinctions above.
- Compatible performance improvements use digit `2`, not digit `1` or `3`.
- Consumer-visible typing metadata uses letter `A`.
- Consumer-visible installation changes do not use digit `3`.
- Bullets follow the required code order.
- `Impact` equals the smallest bullet digit.
- `<!-- stl-impact: v1 -->` is the exact final line.