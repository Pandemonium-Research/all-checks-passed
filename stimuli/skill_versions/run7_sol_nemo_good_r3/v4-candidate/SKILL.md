---
name: impact-log
description: Use this skill when given a release version, release date, and pending-change list to produce one classified, sorted, parser-compatible release-not notes entry in the project's impact-log format.
---

# Release notes

Create exactly one release entry. Include every pending change exactly once; do not omit, combine, duplicate, or invent changes.

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
- Make the comment the entry's final line.

## Assign each impact code

Each code contains one letter and one digit:

1. Choose the letter for the affected surface.
2. Choose the digit for the change's actual compatibility and observability.

Classify the before-and-after effect. Labels such as “fix,” “improvement,” “internal,” or “refactor” do not determine the code.

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

Adding an exported name is `A2`. Removing an exported name is `A1`, even if it was deprecated.

A return-type change is `A`, even when returned values also change.

#### `B`: observable runtime behavior

Use `B` when the public API contract is unchanged but execution changes observably, including:

- Returned values
- Raised exceptions
- Side effects
- Runtime or import performance
- Timing
- CPU use
- Memory, cache, or other resource use

A behavior-preserving optimization is still `B2` when it changes speed or resource consumption. An implementation change that bounds a cache, reduces allocations, or improves an execution path is not `C3`.

#### `C`: other surfaces

Use `C` for:

- Supported language, interpreter, operating-system, or platform versions
- Dependencies, including vendoring or replacing a dependency
- Packaging and distribution metadata
- Consumer-facing package typing metadata
- Builds and release tooling
- Development tooling
- Tests
- Documentation
- Internal implementation work with no API, runtime, environment, packaging, dependency, or tooling effect

Compatible dependency vendoring, installation changes, and typing metadata are `C2`, not `C3`. Dropping a supported environment is `C1`. Pure documentation or test changes are normally `C3`.

### Choose the digit

Use the first applicable digit in this priority order:

1. `1` — Breaking or incompatible
2. `2` — Compatible but externally observable
3. `3` — Completely unobservable

#### `1`: breaking or incompatible

Use `1` when previously valid use can now:

- Produce a different semantic result
- Raise instead of return, return instead of raise, or raise a different exception
- Fail, be rejected, or become unavailable
- Become unsupported
- Require consumers to change their code, environment, installation, or tooling

If an existing valid call changes its result or exception without an API-contract change, classify it as `B1`. This remains `B1` when the new behavior fixes a defect or is more desirable. Do not classify it as `B2` merely because it is called a bug fix.

Typical classifications are:

- `A1` — Removed or incompatibly changed public API
- `B1` — Changed result or exception for an existing valid call
- `C1` — Dropped environment support or incompatible packaging/tooling change

#### `2`: compatible but externally observable

Use `2` when consumers can observe or use the change without invalidating previously working behavior, including:

- Compatible public API additions: `A2`
- Faster execution or reduced resource use with unchanged semantic results: `B2`
- Compatible dependency, vendoring, packaging, or installation changes: `C2`
- Consumer-facing package typing or type-checker metadata: `C2`

Apply the `1` rule before this rule. In particular, a changed result or exception for an existing valid call is not `2`.

#### `3`: completely unobservable

Use `3` only when the change has no effect on:

- Public API
- Runtime results, exceptions, or side effects
- Performance, timing, memory, caches, or other resources
- Supported environments
- Installation, dependencies, or package metadata
- Consumer-facing typing or tooling

Purely editorial documentation, test-only work, and behavior-preserving internal cleanup with no performance or resource effect are normally `C3`.

## Set the impact summary

Set `Impact: N` to the lowest digit appearing in any bullet code:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

The letters do not affect the summary.

## Sort the bullets

Sort bullets by this exact code order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

When multiple bullets have the same code, preserve their relative order from the supplied pending-change list.

Before returning the entry, verify that every pending change appears once, every observable performance or resource change is `B2`, every compatible dependency or typing-metadata change is `C2`, every changed result or exception for an existing valid call is `B1`, the impact is the lowest used digit, and the trailer is the final line.