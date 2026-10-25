---
name: impact-log
description: Use when given a release version, release date, and pending changes to produce one classified, sorted, parser-compatible release-notes entry in the project's impact-log format.
---

# Release notes

Create one release entry containing every pending change exactly once. Do not omit, combine, duplicate, or invent changes.

## Required format

Use this structure:

```text
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Follow these requirements exactly:

- Use a level-two Markdown heading beginning with `##`.
- Copy the supplied version as three numeric components inside square brackets.
- Copy the supplied date in `YYYY-MM-DD` format.
- Put `Impact: N` immediately below the heading.
- Begin every change bullet with `- [CODE]`.
- End with the exact comment `<!-- stl-impact: v1 -->`.
- Make the comment the final line. Do not add text, bullets, or headings after it.

## Assign each impact code

Each code has one letter and one digit. Determine them independently:

1. Choose the letter for the highest-priority affected surface.
2. Choose the digit from the change's actual before-and-after effect.

Classify effects, not labels such as “fix,” “improvement,” “internal,” or “refactor.”

### Choose the letter

Use the first applicable letter in this priority order:

1. `A` — Public API contract
2. `B` — Observable runtime behavior
3. `C` — Packaging, environments, tooling, documentation, tests, or unobservable implementation work

#### `A`: public API contract

Use `A` when the change adds, removes, or modifies:

- An exported module, class, function, method, constant, or other public name
- A public function or method signature
- Accepted argument types
- Returned types
- Public type definitions

Adding a public API is `A`, not `B`. Changing a return type is `A`, even if returned values also change.

#### `B`: observable runtime behavior

Use `B` when the public API contract is unchanged but execution differs in any observable way, including:

- Returned values
- Raised exceptions
- Side effects
- Runtime or import speed
- Timing
- CPU use
- Memory or cache use
- Other resource use

Behavior-preserving optimization is still `B` when it changes performance or resource use. For example, bounding a runtime cache affects memory use and therefore is not an unobservable `C3` change.

#### `C`: other consumer-facing or unobservable surfaces

Use `C` for:

- Supported language, interpreter, operating-system, or platform versions
- Dependencies, including adding, removing, replacing, or vendoring them
- Packaging and distribution metadata
- Consumer-facing package typing metadata
- Builds and release tooling
- Development tooling
- Tests
- Documentation
- Internal implementation work with no API, runtime, environment, packaging, dependency, or tooling effect

Dependency vendoring is observable packaging work and normally uses `C2`, not `C3`. Dropping support for an environment is `C1`, not `A1`.

### Choose the digit

Use the first applicable digit in this priority order:

1. `1` — Breaking or incompatible
2. `2` — Compatible but externally observable
3. `3` — Completely unobservable

#### `1`: breaking or incompatible

Use `1` when previously valid use on the affected surface can now:

- Produce a different semantic result
- Raise instead of return, return instead of raise, or raise a different exception
- Fail, be rejected, or become unavailable
- Become unsupported
- Require consumers to change code, environments, installation, or tooling

A changed result or exception from an existing valid call is always `B1` when the public API contract is unchanged. This remains true when the new behavior is described as a bug fix, correction, improvement, or normalization. Do not use `B2` merely because the new result is preferable.

Typical classifications include:

- `A1` — Public API removal or incompatible contract change
- `B1` — Changed result or exception for an existing call
- `C1` — Dropped environment support or incompatible packaging/tooling change

#### `2`: compatible but externally observable

Use `2` when consumers can observe or use the change without invalidating previously working behavior. Examples include:

- A compatible public API addition: `A2`
- Faster execution or lower resource use with unchanged semantic results: `B2`
- A compatible dependency, vendoring, packaging, or installation change: `C2`
- Consumer-facing type-checker or package-typing metadata: `C2`

Do not classify a changed result or exception as `2`; apply the `1` rule first.

#### `3`: completely unobservable

Use `3` only when no user or consumer can observe any effect on:

- Public API
- Runtime results, exceptions, or side effects
- Performance, timing, memory, caches, or other resources
- Supported environments
- Installation, dependencies, or package metadata
- Consumer-facing typing or tooling

Purely editorial documentation changes, test-only changes, and behavior-preserving internal cleanup with no performance or resource effect are normally `C3`.

## Set the impact summary

Set `Impact: N` to the lowest digit appearing in any bullet code:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Letters do not affect the summary.

## Sort the bullets

Sort bullets by this exact code order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

When multiple bullets have the same code, preserve their relative order from the supplied pending-changes list.