---
name: impact-log
description: Use this skill when given a project version, release date, and pending changes to produce one correctly classified, ordered, and machine-parseable impact-log release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every supplied pending change exactly once.

Copy the supplied version and date exactly. Do not infer a different version, reuse values from another release, invent facts, combine pending changes, or copy obsolete formatting from existing release notes.

The completed entry must have this exact structure:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace:

- `VERSION` with the supplied version number.
- `YYYY-MM-DD` with the supplied ISO-format date.
- `CODE` with the classification of that bullet.
- `DIGIT` with the lowest digit appearing in any bullet code.

## Classify each pending change

Classify the effect stated by the pending change, not the implementation technique used to achieve it.

Choose the letter and digit independently. For example, an internal implementation can still produce a `B2` change when the pending change states that it improves timing or resource usage.

### Choose the letter

Use the first applicable letter in this order:

1. `A` — The public API contract changes.
2. `B` — An existing public operation has an observable runtime change, without an API-contract change.
3. `C` — Neither the public API contract nor observable public runtime behavior changes.

#### `A`: public API contract changes

Use `A` for any change to the declared public interface, including:

- Adding, removing, or renaming an exported public name.
- Adding, removing, or renaming a public parameter.
- Changing a public function, method, or constructor signature.
- Changing the accepted argument types or declared return types.
- Adding or changing type annotations on public functions, methods, attributes, or other public objects.
- Adding, removing, or changing another declared public type.

Compatible additions and breaking removals both use `A`.

Adding annotations to public functions is an API-contract change even when runtime behavior is unchanged. In contrast, adding a marker or integration file that merely helps type checkers discover existing annotations uses `C`.

#### `B`: observable runtime changes

Use `B` when an existing public operation keeps the same API contract but changes any observable runtime property, including:

- Results or returned values.
- Raised exceptions.
- Side effects.
- Correctness of existing behavior.
- Timing, latency, execution speed, or import time.
- Memory or other resource usage, including fixing a leak.

Use `B` whenever the pending change explicitly states a runtime, performance, or resource effect. This remains true when the implementation is an internal refactor, cache change, deferred import, or similar internal mechanism.

A statement that output is unchanged rules out a result change only. It does not override a separately stated improvement to timing, memory, exceptions, side effects, or another observable property.

#### `C`: non-runtime or unobservable changes

Use `C` for changes limited to:

- Build or release configuration.
- Packaging or dependency management.
- CI and developer tooling.
- Tests.
- Documentation or examples.
- Type-checker discovery or integration that does not alter declared public types.
- Internal implementation details with no stated observable effect.

Use `C` for an internal refactor only if the pending change states no public contract, behavior, performance, or resource effect.

If multiple letters apply, use the earliest: `A` before `B` before `C`.

### Choose the digit

Choose the digit separately from the letter:

1. `1` — Breaking.
2. `2` — Externally visible and backward-compatible.
3. `3` — Strictly internal and externally unobservable.

#### `1`: breaking

Use `1` when supported caller code or a supported external workflow:

- Must be changed.
- Can now fail.
- Can no longer use a previously supported API or input.
- No longer receives behavior promised by the public contract.

Do not label a bug fix as breaking solely because the corrected result differs from the old buggy result. Use `1` only when supported or documented behavior is broken.

#### `2`: compatible and externally visible

Use `2` for backward-compatible changes visible to users, downstream tools, or supported workflows, including:

- Public API additions.
- Compatible public signature or type changes.
- Compatible behavior changes and bug fixes.
- Stated timing, performance, memory, or resource improvements.
- Documentation changes.
- Type-checker integration.
- Compatible packaging, dependency, build, CI, or tooling changes.

A change can use digit `2` even if its implementation is internal. Judge the stated effect.

#### `3`: wholly unobservable

Use `3` only when all of these remain unchanged:

- Public API and declared public types.
- Runtime results and exceptions.
- Side effects.
- Timing and other stated performance.
- Memory and other resource behavior.
- Supported external workflows.
- Shipped artifacts and dependency behavior.
- Documentation and type-checker behavior.

Do not use `3` for a leak fix, performance improvement, bug fix, documentation update, packaging change, dependency change, or tooling change.

If two digits still appear applicable, choose the lower, more disruptive digit.

## Write and sort the bullets

Write one bullet for each pending change:

```text
- [LETTERDIGIT] Concise description of the change.
```

Preserve the supplied facts. Do not add claims about compatibility, performance, motivation, or unchanged behavior unless the pending change supports them.

Sort all bullets using this exact code order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

When multiple bullets have the same code, preserve their order from the pending-changes list.

## Calculate Impact

Set `Impact` to the lowest numeric digit appearing in any bullet code, regardless of letter.

For digits `2`, `3`, and `2`, write:

```text
Impact: 2
```

## Final validation

Before returning the entry, verify all of the following:

- The heading contains the exact supplied version and date.
- Every pending change appears once and only once.
- Every public signature or declared-type change uses `A`.
- Every stated runtime, timing, import-time, memory, or leak change uses `B`.
- Digit `3` is used only for a wholly unobservable change.
- Bullets follow the required code order.
- `Impact` is the lowest bullet digit.
- `Impact` appears immediately below the heading.
- The trailer is exactly `<!-- stl-impact: v1 -->`.
- The trailer immediately follows the final bullet and is the final line.