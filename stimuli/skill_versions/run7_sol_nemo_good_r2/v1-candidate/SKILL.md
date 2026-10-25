---
name: impact-log
description: Use this skill to turn a version number, release date, and list of pending project changes into a correctly classified, sorted, and parser-compatible release notes entry.
---

# Release notes

Create one entry containing every pending change exactly once. Use this structure, with no blank lines inside the entry:

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace `VERSION` with the supplied three-part version number and use the supplied date in `YYYY-MM-DD` format.

The final line must be exactly `<!-- stl-impact: v1 -->`. It is an HTML comment, including the opening `<!--` and closing `-->`, and nothing may follow it.

## Classify each change

Each bullet starts with one impact code. The code consists of a surface letter and an impact digit.

Choose the letter first:

- `A` — The public API changes. This includes exported names, parameters, signatures, return types, and exported type definitions.
- `B` — The runtime behavior of existing functionality changes without changing its public API. This includes results, exceptions, side effects, performance, timing, and resource use.
- `C` — The change is limited to packaging, supported environments, dependencies, builds, tooling, tests, documentation, or an internal implementation with no stated runtime effect.

Choose the digit independently:

- `1` — Breaking. Previously working caller code, installations, or supported environments can fail, stop working, or produce a different result.
- `2` — Compatible but observable. The change adds capability, fixes a defect, improves runtime behavior, or changes packaging or tooling without breaking correct existing use.
- `3` — Unobservable to callers. Use this only for documentation, tests, or a purely internal refactor whose API, runtime behavior, packaging, and tooling effects are all unchanged.

Apply these rules consistently:

- Removing or incompatibly changing a public API is `A1`.
- Adding a public API without breaking existing use is `A2`.
- Changing the result or exception behavior of an existing call is `B1` when breaking and `B2` when it is a compatible fix.
- A stated performance, timing, memory, or resource improvement is observable runtime behavior and therefore `B2`, not `C3`.
- Dropping support for a runtime, platform, or environment is `C1`.
- A compatible packaging, dependency, metadata, or type-checking integration change is `C2`.
- Documentation-only, test-only, and behavior-preserving internal refactors are `C3`.

If more than one letter applies, use the earliest letter in `A`, `B`, `C`. If more than one digit applies, use the lowest digit in `1`, `2`, `3`. For example, a public return-type change also changes runtime behavior, but precedence makes it `A`, and any breaking aspect makes its digit `1`.

## Order and summarize

Sort bullets by their complete codes in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep the original order among bullets that have the same code.

Set the `Impact` value to the lowest digit used by any bullet, regardless of its letter. For example, if the entry contains codes ending in `2` and `3`, write `Impact: 2`.

Before finishing, verify that:

- The heading begins with `##`.
- Every pending change appears once.
- Every bullet has exactly one code.
- Bullets are sorted by code.
- `Impact` is the lowest digit present.
- The HTML trailer is the exact final line.