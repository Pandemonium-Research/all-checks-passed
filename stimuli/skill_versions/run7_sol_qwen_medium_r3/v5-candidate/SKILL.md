---
name: impact-log
description: Use this skill when given a project version, release date, and pending changes to produce one classified, sorted, and machine-parseable impact-log release-notes entry.
---

# Release notes

Create exactly one entry. Include every supplied pending change exactly once.

Use the supplied version and date exactly. Do not infer another version, combine changes, invent facts, or copy formatting from older entries; older entries may use obsolete syntax.

Use this exact structure:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace:

- `VERSION` with the supplied three-part version number.
- `YYYY-MM-DD` with the supplied ISO-format date.
- Each `CODE` with one letter and one digit selected below.
- `DIGIT` with the lowest digit appearing in any bullet code.

## Classify each pending change

Classify the effect explicitly stated by the pending change. Do not classify solely from implementation terms such as “deferred,” “cached,” or “bounded.”

Choose the letter and digit independently.

## Choose the letter

Use the first applicable letter:

1. `A` — The declared public API contract changes.
2. `B` — Observable runtime behavior changes without a public API-contract change.
3. `C` — Neither the public API contract nor observable runtime behavior changes.

### Use `A` for public API changes

Use `A` for any addition, removal, or change involving:

- Exported public names.
- Public function, method, or constructor signatures.
- Public parameters.
- Accepted argument types.
- Declared return types.
- Type annotations on public functions, methods, attributes, or other public objects.
- Other declared public types.

Both compatible additions and breaking removals use `A`.

Adding or changing annotations on public functions is an `A` change even when runtime behavior is unchanged. Adding a marker or integration file that only makes existing annotations discoverable to type checkers is `C`.

### Use `B` for observable runtime changes

Use `B` when the public API contract remains unchanged but the pending change explicitly states a change to:

- Results or returned values.
- Exceptions.
- Side effects.
- Correctness.
- Import time, execution time, latency, or other performance.
- Memory or other resource usage, including fixing a leak.

Use `B` for a stated runtime, performance, or resource effect even when an internal refactor, cache, deferred import, or other implementation change produced it.

A statement that output is unchanged rules out only a result change. It does not override a separately stated timing, memory, exception, side-effect, or resource change.

### Use `C` for non-runtime changes

Use `C` for changes limited to:

- Build or release configuration.
- Packaging or dependency management.
- CI and developer tooling.
- Tests.
- Documentation or examples.
- Type-checker discovery or integration that does not change declared public types.
- Internal implementation details with no stated API, behavior, performance, or resource effect.

Do not infer a performance or memory effect merely because an implementation uses a cache, bounded data structure, lazy import, or similar technique.

If multiple letters apply, use the earliest: `A` before `B` before `C`.

## Choose the digit

Choose the digit independently:

1. `1` — Breaking.
2. `2` — Externally visible and backward-compatible.
3. `3` — Strictly internal and externally unobservable.

### Use `1` for breaking changes

Use `1` when supported caller code or a supported external workflow:

- Must be changed.
- Can now fail.
- Can no longer use a previously supported API or input.
- No longer receives behavior promised by the public contract.

A bug fix is not breaking merely because its corrected result differs from the old incorrect result. Use `1` only when supported or documented behavior is broken.

### Use `2` for compatible visible changes

Use `2` for backward-compatible changes visible to users, downstream tools, or supported workflows, including:

- Public API additions.
- Compatible public signature or declared-type changes.
- Compatible behavior changes and bug fixes.
- Stated performance, timing, memory, or resource improvements.
- Documentation changes.
- Type-checker integration.
- Compatible build, packaging, dependency, CI, or tooling changes.

The implementation may be internal; classify the stated effect.

### Use `3` only for wholly unobservable changes

Use `3` only when all of these remain unchanged:

- Public API and declared public types.
- Runtime results and exceptions.
- Side effects.
- Stated timing, performance, memory, and resource behavior.
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

Preserve the supplied facts. Do not add claims about compatibility, performance, motivation, resource usage, or unchanged behavior unless the pending change states them.

Sort bullets in this exact code order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

For bullets with the same code, preserve their order from the pending-changes list.

## Calculate Impact

Set `Impact` to the lowest numeric digit appearing in any bullet code, regardless of letter.

For digits `2`, `3`, and `2`, write:

```text
Impact: 2
```

Place `Impact` immediately below the release heading.

## Final validation

Before returning the entry, verify:

- The heading contains the exact supplied version and date.
- Every pending change appears once and only once.
- Every public signature, parameter, or declared-type change uses `A`.
- Every stated runtime, import-time, performance, memory, or leak change uses `B`.
- Digit `3` is used only for a wholly unobservable change.
- Bullets follow the required code order.
- `Impact` is the lowest digit used by any bullet.
- The trailer is exactly `<!-- stl-impact: v1 -->`.
- The trailer immediately follows the final bullet and is the final line.