---
name: impact-log
description: Use this skill when given a project version, release date, and pending changes to produce one correctly classified, sorted, and machine-parseable impact-log release-notes entry.
---

# Release notes

Create exactly one release entry containing every supplied pending change exactly once.

Use the supplied version and date exactly. Do not infer a different version, merge changes, invent facts, or copy syntax from older entries; older entries may use obsolete formatting.

Use this exact structure:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace:

- `VERSION` with the supplied version number, unchanged.
- `YYYY-MM-DD` with the supplied ISO-format date, unchanged.
- Each `CODE` with one letter and one digit selected below.
- `DIGIT` with the lowest numeric digit appearing in any bullet code.

The trailer must be exactly `<!-- stl-impact: v1 -->`. Place it immediately after the final bullet as the final line.

## Classify each change

Classify the effect explicitly stated by the pending change. Choose the letter and digit independently.

Do not classify from an implementation term alone. Words such as “deferred,” “cached,” “bounded,” or “refactored” do not establish a performance or resource effect unless the change states one.

## Choose the letter

Use the first applicable letter:

1. `A` — The declared public API contract changes.
2. `B` — Observable runtime behavior changes without a public API-contract change.
3. `C` — Neither the public API contract nor observable runtime behavior changes.

If multiple letters apply, use the earliest: `A` before `B` before `C`.

### Use `A` for public API-contract changes

Use `A` for additions, removals, or changes involving:

- Exported public names.
- Public function, method, or constructor signatures.
- Public parameters.
- Accepted argument types.
- Declared return types.
- Type annotations on public functions, methods, attributes, or other public objects.
- Other declared public types.

Both compatible additions and breaking removals use `A`.

Adding or changing annotations on public objects is `A`, even when runtime behavior is unchanged. A marker or integration file that only makes existing annotations discoverable to type checkers is `C`.

### Use `B` for observable runtime changes

Use `B` when the public API contract is unchanged and the pending change explicitly states a change to:

- Results or returned values.
- Raised exceptions.
- Side effects.
- Correctness.
- Import time, execution time, latency, or other performance.
- Memory use or another resource characteristic.
- Resource leaks.

Use `B` for these effects even when they result from an internal refactor, cache change, deferred import, or other implementation technique.

A statement that output is unchanged rules out only a result change. It does not cancel a separately stated change to timing, memory, exceptions, side effects, or resource use.

### Use `C` for non-runtime changes

Use `C` for changes limited to:

- Build or release configuration.
- Packaging or dependency management.
- CI and developer tooling.
- Tests.
- Documentation or examples.
- Type-checker discovery or integration that does not change declared public types.
- Internal implementation details with no stated API, behavior, performance, memory, or resource effect.

An internal cache or implementation replacement is `C` when no observable runtime effect is stated. Do not infer faster execution or lower memory use from the implementation technique.

## Choose the digit

Choose the digit independently of the letter:

1. `1` — Breaking.
2. `2` — Externally visible and backward-compatible.
3. `3` — Strictly internal and externally unobservable.

If multiple digits appear applicable, use the lower, more disruptive digit.

### Use `1` for breaking changes

Use `1` when supported caller code or a supported external workflow:

- Must be changed.
- Can now fail.
- Can no longer use a previously supported API or input.
- No longer receives behavior promised by the public contract.

A bug fix is not breaking merely because the corrected result differs from the old incorrect result. Use `1` only when supported or documented behavior is broken.

### Use `2` for compatible visible changes

Use `2` for backward-compatible changes visible to users, downstream tools, or supported workflows, including:

- Public API additions.
- Compatible public signature or declared-type changes.
- Compatible behavior changes and bug fixes.
- Stated performance, timing, memory, or resource improvements.
- Documentation changes.
- Type-checker integration.
- Compatible build, packaging, dependency, CI, or tooling changes.

The implementation may be internal; classify the stated effect. A performance improvement or leak fix is visible and therefore uses digit `2`, not `3`.

### Use `3` only for wholly unobservable changes

Use `3` only when all of the following remain unchanged:

- Public API and declared public types.
- Runtime results and exceptions.
- Side effects.
- Stated timing, performance, memory, and resource behavior.
- Supported external workflows.
- Shipped artifacts and dependency behavior.
- Documentation and type-checker behavior.

Do not use `3` for a bug fix, leak fix, stated performance improvement, documentation update, packaging change, dependency change, or tooling change.

## Write and order the bullets

Write exactly one bullet for each pending change:

```text
- [LETTERDIGIT] Concise description of the change.
```

Preserve the supplied facts. Do not add claims about compatibility, performance, motivation, resource use, or unchanged behavior unless the pending change states them.

Sort bullets in this exact code order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

For bullets with the same code, preserve their order from the pending-changes list.

## Calculate Impact

Set `Impact` to the lowest numeric digit appearing in any bullet code, regardless of letter.

For example, bullet digits `2`, `3`, and `2` produce:

```text
Impact: 2
```

Place the `Impact` line immediately below the release heading.

## Final validation

Before returning the entry, verify that:

- The heading contains the exact supplied version and date.
- Every pending change appears once and only once.
- Every public signature, parameter, annotation, or declared-type change uses `A`.
- Every stated runtime, import-time, performance, memory, resource, or leak change uses `B`, unless an `A` effect takes precedence.
- Digit `3` is used only for a wholly unobservable change.
- Bullets follow the required code order.
- `Impact` is the lowest digit used by any bullet.
- The trailer is exactly `<!-- stl-impact: v1 -->`.
- The trailer immediately follows the final bullet and is the final line.