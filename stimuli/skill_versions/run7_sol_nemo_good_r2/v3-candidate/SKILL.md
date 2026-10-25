---
name: impact-log
description: Use this skill when given a release version, release date, and pending project changes to write one correctly classified, sorted, and parser-compatible release notes entry.
---

# Release notes

Create one entry containing every pending change exactly once. Do not insert blank lines between the heading, impact line, bullets, or trailer.

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace `VERSION` with the supplied three-part version number. Use the supplied date in `YYYY-MM-DD` format.

The trailer must immediately follow the last bullet and must be the exact final line:

```text
<!-- stl-impact: v1 -->
```

Include both `<!--` and `-->`. Do not place a blank line before the trailer or any content after it.

## Classify each change

Each bullet begins with one impact code consisting of a surface letter and an impact digit. Choose the letter and digit independently.

### Choose the surface letter

- `A` — The public API or accepted public contract changes. This includes adding, removing, or changing exported names, accepted argument types or values, parameters, signatures, declared return types, or exported type definitions.
- `B` — Existing functionality changes at runtime without changing its public API or accepted contract. This includes results, exceptions, side effects, performance, timing, caching, memory use, and other resource use.
- `C` — The change is limited to packaging, supported environments, dependencies, builds, tooling, tests, documentation, or an internal implementation with no API, runtime behavior, performance, timing, caching, memory, or resource-use effect.

Use these distinctions:

- Classify a change as `A` only when the public API or accepted contract itself changes.
- Adding an exported API is `A`. Expanding the documented inputs accepted by an existing API is also `A`.
- Do not choose `A` merely because a change mentions a public function. If an existing call produces a corrected result or exception while its interface and accepted inputs remain the same, choose `B`.
- A cache change is a runtime resource or performance change. Adding, removing, bounding, or replacing a cache is `B`, even when results and signatures are unchanged.
- Use `C` for an internal refactor only when it preserves API, results, exceptions, side effects, performance, timing, caching, memory use, and other resource use.

### Choose the impact digit

- `1` — Breaking. Previously working caller code, installations, or supported environments can fail, stop working, or become incompatibly different.
- `2` — Compatible but observable. The change adds capability, fixes a defect, changes runtime performance or resource use, or changes packaging or tooling without breaking correct existing use.
- `3` — Unobservable to callers. Use this only for documentation, tests, or a purely internal refactor with no API, runtime, packaging, tooling, performance, timing, caching, memory, or resource-use effect.

Apply these code rules:

- Removing or incompatibly changing a public API is `A1`.
- Adding a public API or compatibly expanding its accepted input contract is `A2`.
- Changing only the result or exception produced by an existing call is `B1` when incompatible and `B2` when it is a compatible fix.
- A performance, timing, caching, memory, or resource-use change is `B2` when compatible, even if output is unchanged.
- Dropping support for a runtime, platform, or environment is `C1`.
- A compatible packaging, dependency, metadata, or type-checking integration change is `C2`.
- Documentation-only and test-only changes are `C3`.
- A behavior- and resource-preserving internal refactor is `C3`.

If more than one letter applies, use the earliest applicable letter in `A`, `B`, `C`. If more than one digit applies, use the lowest applicable digit in `1`, `2`, `3`. For example, any breaking aspect requires digit `1`, even if other aspects are compatible.

## Order and summarize

Sort bullets by their complete codes in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep the supplied order among changes assigned the same code.

Set `Impact` to the lowest digit used by any bullet, regardless of its letter. If the bullets use digits `2` and `3`, for example, write `Impact: 2`.

Before finishing, verify that:

- The heading begins with `##`.
- The version and date exactly match the supplied values.
- Every pending change appears exactly once.
- Every bullet has exactly one code.
- Result or exception fixes with unchanged APIs are classified under `B`, not `A`.
- Cache, performance, timing, memory, and resource-use changes are classified under `B`, not `C3`.
- Bullets follow the required complete-code order.
- Changes with the same code retain their supplied order.
- `Impact` is the lowest digit present.
- There are no blank lines inside the entry.
- The exact HTML trailer immediately follows the last bullet and is the final line.