---
name: impact-log
description: Use this skill when given a release version, release date, and pending project changes to produce one classified, sorted, and parser-compatible release notes entry.
---

# Release notes

Create one entry containing every pending change exactly once.

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace `VERSION` with the supplied three-part version number and use the supplied date in `YYYY-MM-DD` format.

Do not insert blank lines between the heading, impact line, bullets, or trailer. The trailer must immediately follow the final bullet and must be the exact final line:

```text
<!-- stl-impact: v1 -->
```

Nothing may follow the trailer.

## Classify each change

Each bullet starts with one impact code consisting of a surface letter and an impact digit. Choose the letter and digit independently.

### Choose the surface letter

- `A` — The public API or accepted public contract changes. This includes adding, removing, or changing exported names, accepted argument types or values, parameters, signatures, declared return types, or exported type definitions.
- `B` — The runtime behavior of existing functionality changes without changing its public API or accepted contract. This includes results, exceptions, side effects, performance, timing, caching, memory use, and other resource use.
- `C` — The change is limited to packaging, supported environments, dependencies, builds, tooling, tests, documentation, or a purely internal implementation with no API or runtime effect.

Use these distinctions:

- Adding an exported API or compatibly expanding the inputs accepted by a public API is `A`.
- Do not choose `A` merely because a change fixes or mentions a public function. If an existing call returns a corrected result or raises a corrected exception while its public contract remains unchanged, choose `B`.
- Adding, removing, bounding, or replacing a cache is a runtime resource or performance change and therefore `B`, even when results and signatures are unchanged.
- Choose `C` for an internal refactor only when it preserves results, exceptions, side effects, performance, timing, caching, memory use, and other resource use.

### Choose the impact digit

- `1` — Breaking. Previously working caller code, installations, or supported environments can fail, stop working, or become incompatibly different.
- `2` — Compatible but observable. The change adds capability, fixes a defect, changes runtime behavior or resource use, or changes packaging or tooling without breaking correct existing use.
- `3` — Unobservable to callers. Use this only for documentation, tests, or a purely internal refactor with no API, runtime, packaging, tooling, performance, timing, caching, memory, or resource-use effect.

Apply these code rules:

- Removing or incompatibly changing a public API is `A1`.
- Adding a public API or compatibly expanding its accepted input contract is `A2`.
- Changing only the result or exception produced by an existing call is `B1` when incompatible and `B2` when it is a compatible fix.
- A compatible performance, timing, caching, memory, or resource-use change is `B2`, even when output is unchanged.
- Dropping support for a runtime, platform, or environment is `C1`.
- A compatible packaging, dependency, metadata, or type-checking integration change is `C2`.
- Documentation-only and test-only changes are `C3`.
- An internal refactor is `C3` only when it has no API, behavior, performance, timing, caching, memory, resource, packaging, or tooling effect.

If more than one letter applies, use the earliest applicable letter in `A`, `B`, `C`. If more than one digit applies, use the lowest applicable digit in `1`, `2`, `3`. Any breaking aspect requires digit `1`.

## Order and summarize

Sort bullets by their complete codes in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep the supplied order among changes assigned the same code.

Set `Impact` to the lowest digit used by any bullet, regardless of its letter. For example, if the bullets use digits `2` and `3`, write `Impact: 2`.

Before finishing, verify that:

- The version and date exactly match the supplied values.
- Every pending change appears exactly once.
- Every bullet has exactly one code.
- Fixes to existing results or exceptions are under `B`, not `A`, unless the public contract also changes.
- Cache, performance, timing, memory, and resource-use changes are under `B`, not `C3`.
- Bullets follow the required complete-code order.
- Changes with the same code retain their supplied order.
- `Impact` is the lowest digit present.
- There are no blank lines anywhere inside the entry.
- The exact HTML trailer immediately follows the final bullet and is the final line.