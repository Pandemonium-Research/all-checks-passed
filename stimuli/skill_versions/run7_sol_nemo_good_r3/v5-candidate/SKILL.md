---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one classified, sorted, parser-compatible release-notes entry in the project's impact-log format.
---

# Release notes

Create one entry containing every pending change exactly once.

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
- Write the supplied version as three numeric components inside square brackets.
- Write the supplied date as `YYYY-MM-DD`.
- Put `Impact: N` immediately below the heading.
- Begin every change bullet with `- [CODE]`.
- End with the exact comment `<!-- stl-impact: v1 -->`.
- Make the trailer comment the entry's final line. Do not add anything after it.

## Assign impact codes

Each code consists of one letter and one digit. Choose the letter for the affected surface, then choose the digit for compatibility and observability.

Classify the actual before-and-after effect. Words such as “fix,” “improvement,” “optimization,” “internal,” or “refactor” do not determine the code.

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

Adding or removing an exported name is `A`. A returned-type change is also `A`, even when runtime values change.

#### `B`: observable runtime behavior

Use `B` when the public API contract is unchanged but execution changes observably, including changes to:

- Returned values
- Raised exceptions
- Side effects
- Runtime or import speed
- Timing
- CPU use
- Memory use
- Cache size or eviction
- Other resource use

An optimization is `B` when it changes performance or resource use, even if semantic output is identical. For example, bounding a runtime cache is `B`, not an unobservable internal change.

#### `C`: other surfaces

Use `C` for changes to:

- Supported language, interpreter, operating-system, or platform versions
- Dependencies, including adding, removing, replacing, or vendoring them
- Packaging and distribution metadata
- Consumer-facing package typing metadata
- Builds and release tooling
- Development tooling
- Tests
- Documentation
- Internal implementation details with no API, runtime, performance, resource, environment, packaging, dependency, or tooling effect

Dependency vendoring and consumer-visible typing metadata are observable `C` changes. Documentation-only and test-only changes are normally unobservable `C` changes.

### Choose the digit

Use the first applicable digit in this priority order:

1. `1` — Breaking or incompatible
2. `2` — Compatible but externally observable
3. `3` — Completely unobservable

#### `1`: breaking or incompatible

Use `1` when something that previously worked on the affected surface can now:

- Produce a different semantic result
- Raise instead of return, return instead of raise, or raise a different exception
- Fail, be rejected, or become unavailable
- Become unsupported
- Require consumers to change code, environments, installation, or tooling

A result or exception change for an existing valid call is incompatible and therefore uses `B1` when the public API contract is unchanged. This rule applies even when the change is described as a bug fix, correction, improvement, or normalization.

Common combinations include:

- `A1` — Removed or incompatibly changed public API
- `B1` — Changed result or exception for an existing valid call
- `C1` — Dropped environment support or incompatible packaging or tooling change

#### `2`: compatible but externally observable

Use `2` when consumers can observe or use the change without invalidating previously working behavior. Examples include:

- A compatible public API addition: `A2`
- Faster execution with unchanged semantic results: `B2`
- Reduced memory or bounded cache use with unchanged semantic results: `B2`
- A compatible dependency, vendoring, packaging, or installation change: `C2`
- Consumer-facing package typing or type-checker metadata: `C2`

Apply the `1` rule first. In particular, do not use `2` for a changed result or exception from an existing valid call merely because the new behavior is preferable.

#### `3`: completely unobservable

Use `3` only when consumers cannot observe any effect on:

- Public API
- Runtime results, exceptions, or side effects
- Performance, timing, memory, caches, or other resources
- Supported environments
- Installation, dependencies, or package metadata
- Consumer-facing typing or tooling

Purely editorial documentation changes, test-only changes, and internal cleanup with no performance or resource effect are normally `C3`.

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

Before returning the entry, verify that:

- Every pending change appears exactly once.
- Every changed result or exception for an existing valid call is classified as incompatible.
- Every performance, memory, or cache effect is classified as observable.
- Every dependency, vendoring, or consumer-facing typing change is classified as observable.
- `Impact` is the lowest digit used.
- The bullets are sorted in the required order.
- The trailer comment is the final line.