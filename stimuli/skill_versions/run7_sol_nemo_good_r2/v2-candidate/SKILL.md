---
name: impact-log
description: Use this skill when given a release version, date, and pending project changes to produce one correctly classified, sorted, and parser-compatible release notes entry.
---

# Release notes

Create one entry containing every pending change exactly once. Do not add blank lines anywhere inside the entry.

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace `VERSION` with the supplied three-part version number and use the supplied date in `YYYY-MM-DD` format.

The final line must be exactly `<!-- stl-impact: v1 -->`, including the opening `<!--` and closing `-->`. Nothing may follow it.

## Classify each change

Each bullet starts with one impact code. The code consists of a surface letter and an impact digit.

### Choose the surface letter

- `A` — The public interface or contract changes. This includes adding, removing, or changing exported names, accepted arguments, parameters, signatures, declared return types, or exported type definitions.
- `B` — The runtime behavior of existing functionality changes without changing its public interface. This includes returned values, exceptions, side effects, performance, timing, caching, memory use, and other resource use.
- `C` — The change is limited to packaging, supported environments, dependencies, builds, tooling, tests, documentation, or an internal implementation that preserves API, runtime behavior, performance, timing, memory use, and other resource use.

Do not choose `A` merely because a change mentions or fixes a public function. Choose `A` only when the function's public interface or accepted contract changes. A fix that changes the result of an existing call while preserving its interface is `B`.

An internal implementation change is not automatically `C3`. If it adds, removes, bounds, or replaces a cache, or otherwise affects performance, timing, memory, or resource use, classify it as `B`.

### Choose the impact digit independently

- `1` — Breaking. Previously working caller code, installations, or supported environments can fail, stop working, or produce a different result incompatibly.
- `2` — Compatible but observable. The change adds capability, fixes a defect, improves or otherwise observably changes runtime behavior, or changes packaging or tooling without breaking correct existing use.
- `3` — Unobservable to callers. Use this only for documentation, tests, or a purely internal refactor whose API, runtime behavior, packaging, tooling, performance, timing, memory use, and resource use are all unchanged.

Apply these rules consistently:

- Removing or incompatibly changing a public API is `A1`.
- Adding a public API or expanding the accepted public input contract without breaking existing use is `A2`.
- Changing only the value or exception produced by an existing call is `B1` when breaking and `B2` when it is a compatible fix.
- A stated or inherent performance, timing, caching, memory, or resource-use change is observable runtime behavior and therefore `B2`, even when results and signatures are unchanged.
- Dropping support for a runtime, platform, or environment is `C1`.
- A compatible packaging, dependency, metadata, or type-checking integration change is `C2`.
- Documentation-only and test-only changes are `C3`.
- An internal refactor is `C3` only when no API, behavior, performance, timing, caching, memory, resource, packaging, or tooling effect is stated or implied.

If more than one letter applies, use the earliest letter in `A`, `B`, `C`. If more than one digit applies, use the lowest digit in `1`, `2`, `3`. For example, a public return-type contract change also affects runtime behavior, but precedence makes it `A`; any breaking aspect makes its digit `1`.

## Order and summarize

Sort bullets by their complete codes in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep the original order among bullets that have the same code.

Set `Impact` to the lowest digit used by any bullet, regardless of its letter. For example, if the entry contains codes ending in `2` and `3`, write `Impact: 2`.

Before finishing, verify that:

- The heading begins with `##`.
- The version and date exactly match the supplied values.
- Every pending change appears exactly once.
- Every bullet has exactly one code.
- Bullets are sorted by complete code.
- Changes with the same code retain their original order.
- `Impact` is the lowest digit present.
- There are no blank lines inside the entry.
- The HTML trailer is the exact final line.