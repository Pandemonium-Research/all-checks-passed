---
name: impact-log
description: Use when given a release version, release date, and pending-change list to produce a classified, correctly ordered, parser-compatible impact-log release-notes entry.
---

# Release notes

Produce one release entry. Create exactly one bullet for each pending change: do not omit, duplicate, combine, or invent changes.

## Required format

Use exactly this structure:

```text
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: N
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Formatting requirements:

- Use a level-two Markdown heading beginning with `##`.
- Write the supplied version as three numeric components inside square brackets.
- Write the supplied date as `YYYY-MM-DD`.
- Put `Impact: N` immediately below the heading.
- Begin every change bullet with `- [CODE]`.
- End with the exact comment `<!-- stl-impact: v1 -->`.
- Make that comment the final line. Do not add text, bullets, or headings after it.

## Classify each change

A code contains one letter and one digit. Determine them independently:

1. Choose the letter from the surface affected by the change.
2. Choose the digit from its compatibility and observability.
3. If several letters or digits apply, use the higher-impact choice according to the priority rules below.

Classify the actual effect, not words such as “internal,” “refactor,” “fix,” or “cleanup” in the pending-change description.

### Choose the letter

Use the earliest applicable letter:

1. `A` — Public API contract
2. `B` — Observable runtime behavior
3. `C` — Packaging, environments, tooling, documentation, tests, or truly unobservable implementation details

#### `A`: public API contract

Use `A` when the change affects:

- Exported modules, classes, functions, methods, constants, or other public names
- Function or method signatures
- Accepted argument types or returned types
- Public type definitions

Adding or removing an exported name is `A`. A return-type change is also `A`, even if runtime results change too.

#### `B`: observable runtime behavior

Use `B` when the public API contract is unchanged but execution can differ, including:

- Returned values
- Raised exceptions
- Side effects
- Runtime or import performance
- Timing
- CPU or memory use
- Other resource use

A different result from an existing call is `B`. Performance or resource-use changes are also `B`, even when functional output is identical and the implementation is described as internal.

#### `C`: non-runtime surfaces or unobservable work

Use `C` for:

- Supported language, interpreter, operating-system, or platform versions
- Dependencies and dependency vendoring
- Packaging and distribution metadata
- Builds and release tooling
- Consumer-facing type-checker configuration or package typing metadata
- Development tooling
- Tests
- Documentation
- Editorial changes
- Internal implementation changes with no API, runtime, environment, packaging, or tooling effect

Dropping support for a language or platform version is `C`, not `A`.

### Choose the digit

Use the lowest applicable digit:

1. `1` — Breaking or incompatible
2. `2` — Compatible but externally observable
3. `3` — Completely unobservable to users and consumers

#### `1`: breaking or incompatible

Use `1` when something that previously worked on the affected surface can now:

- Fail or raise a different exception
- Become unavailable or unsupported
- Be rejected
- Produce a different semantic result
- Require consumers to change their code, environment, installation, or tooling

A change to the result or exception of an existing valid call is `1`, even when described as a bug fix or improvement. Choose the digit from the before-and-after behavior, not from whether the change is beneficial.

Typical combinations include:

- `A1` for removing or incompatibly changing public API
- `B1` for changing the result or exception of an existing call
- `C1` for dropping supported environments or making incompatible packaging or tooling changes

#### `2`: compatible but observable

Use `2` when consumers can observe or use the change without previously working behavior becoming incompatible. This includes:

- Compatible public API additions
- Performance or resource-use improvements that preserve semantic results
- Compatible dependency, packaging, build, or tooling changes
- Changes that affect installation or dependency resolution
- Changes that affect type-checker behavior

Typical combinations include `A2`, `B2`, and `C2`.

Do not assign `2` to a changed result or exception merely because the new behavior fixes a defect; such a runtime change is `B1`.

#### `3`: completely unobservable

Use `3` only when the change has no effect on:

- Public API
- Runtime results, exceptions, side effects, timing, performance, or resources
- Supported environments
- Installation, dependencies, or package metadata
- Consumer-facing typing or tooling behavior

Purely editorial documentation work and behavior-preserving internal cleanup are normally `C3`.

Do not use `3` merely because functional output is unchanged. Performance, memory use, dependency handling, installation behavior, package metadata, and type-checker behavior are observable and therefore require `2` unless incompatible, in which case use `1`.

## Set the impact summary

After assigning all bullet codes, set `Impact: N` to the lowest digit appearing in any code:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

The letter does not affect the summary.

## Sort the bullets

Sort bullets by this exact code order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

When multiple bullets have the same code, preserve their relative order from the supplied pending-changes list.