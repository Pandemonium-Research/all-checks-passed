---
name: impact-log
description: Use this skill when given a project version, release date, and pending changes to write one correctly classified, sorted, and machine-parseable impact-log release-notes entry.
---

# Release notes

Create exactly one entry containing every pending change exactly once. Use the supplied version and date exactly. Do not invent facts, combine changes, or copy formatting from older entries; some older entries use obsolete syntax.

Use this exact structure:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace the placeholders as follows:

- `VERSION` is the supplied version number.
- `YYYY-MM-DD` is the supplied ISO-format date.
- Each pending change becomes one bullet.
- `CODE` is one letter followed by one digit, selected using the rules below.
- `DIGIT` is the lowest digit appearing in any bullet code.
- The trailer is exactly `<!-- stl-impact: v1 -->`. It immediately follows the final bullet and is the final line.

## Classify each pending change

Classify the stated effect of the change, not merely the subsystem or implementation technique mentioned. Choose the letter and digit independently.

### Choose the letter

Use the first applicable letter:

1. `A` — The declared public API contract changes.
2. `B` — An existing public operation has an observable runtime change without a public API-contract change.
3. `C` — Neither the public API contract nor observable public runtime behavior changes.

#### Use `A` for public API-contract changes

Use `A` for changes to:

- Exported public names.
- Public function, method, or constructor signatures.
- Public parameters.
- Accepted argument types.
- Declared return types.
- Type annotations on public functions, methods, attributes, or other public objects.
- Other declared public types.

Both compatible additions and breaking removals use `A`.

Adding or changing annotations across public functions is an `A` change even when runtime behavior is unchanged. A marker or integration file that only makes existing annotations discoverable to type checkers is `C`.

#### Use `B` for observable runtime changes

Use `B` when an existing public operation keeps the same API contract but changes:

- Results or returned values.
- Raised exceptions.
- Side effects.
- Correctness.
- Import time, execution time, latency, or other explicitly stated performance.
- Memory or other resource usage, including fixing a resource leak.

Classify the stated runtime effect as `B` even when it was achieved through an internal refactor, cache change, deferred import, or similar implementation technique.

A statement that output is unchanged rules out a result change only. It does not cancel a separately stated timing, memory, exception, side-effect, or resource change.

#### Use `C` for non-runtime or unobservable changes

Use `C` for changes limited to:

- Build or release configuration.
- Packaging or dependency management.
- CI and developer tooling.
- Tests.
- Documentation or examples.
- Type-checker discovery or integration that does not alter declared public types.
- Internal implementation details with no stated observable runtime effect.

An internal refactor or cache replacement is `C` when the input states no change to public behavior, performance, or resource usage. Do not infer a performance or memory improvement merely from implementation terms such as “deferred,” “cached,” or “bounded”; classify only effects the pending change states.

If multiple letters apply, use the earliest: `A` before `B` before `C`.

### Choose the digit

Choose the digit separately from the letter:

1. `1` — Breaking.
2. `2` — Externally visible and backward-compatible.
3. `3` — Strictly internal and externally unobservable.

#### Use `1` for breaking changes

Use `1` when supported caller code or a supported external workflow:

- Must be changed.
- Can now fail.
- Can no longer use a previously supported API or input.
- No longer receives behavior promised by the public contract.

A bug fix is not breaking merely because the corrected result differs from the old incorrect result. Use `1` only when supported or documented behavior is broken.

#### Use `2` for compatible visible changes

Use `2` for backward-compatible changes visible to users, downstream tools, or supported workflows, including:

- Public API additions.
- Compatible public signature or declared-type changes.
- Compatible behavior changes and bug fixes.
- Explicitly stated performance or resource improvements.
- Documentation changes.
- Type-checker integration.
- Compatible build, packaging, dependency, CI, or tooling changes.

Packaging, dependency, documentation, and tooling changes are normally digit `2`, even when runtime behavior is unchanged.

#### Use `3` only for wholly unobservable changes

Use `3` only when all of the following remain unchanged:

- Public API and declared public types.
- Runtime results and exceptions.
- Side effects.
- Stated performance and resource behavior.
- Supported external workflows.
- Shipped artifacts and dependency behavior.
- Documentation and type-checker behavior.

Do not use `3` for a bug fix, leak fix, stated performance improvement, documentation update, packaging change, dependency change, or tooling change.

If two digits remain applicable, choose the lower, more disruptive digit.

## Write and order the bullets

Write one bullet for each pending change:

```text
- [LETTERDIGIT] Concise description of the change.
```

Preserve the supplied facts. Do not add claims about compatibility, performance, motivation, resource usage, or unchanged behavior unless the pending change supports them.

Sort bullets in this exact code order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

For bullets with the same code, preserve their order from the pending-changes list.

## Calculate Impact

Set `Impact` to the lowest numeric digit appearing in any bullet code, regardless of letter.

For example, digits `2`, `2`, and `3` produce:

```text
Impact: 2
```

Place `Impact` immediately below the release heading.

## Final check

Before returning the entry, verify that:

- The heading contains the exact supplied version and date.
- Every pending change appears exactly once.
- Every declared public signature or type-annotation change uses `A`.
- Every stated runtime, import-time, performance, memory, or leak change uses `B`.
- No observable or externally visible change uses digit `3`.
- Bullets follow the required code order.
- `Impact` is the lowest digit used by any bullet.
- The exact trailer immediately follows the final bullet and is the final line.