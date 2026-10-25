---
name: impact-log
description: Use this skill when given a project version, release date, and pending changes to produce one correctly classified, ordered, and machine-parseable release-notes entry.
---

# Release notes

Create exactly one release entry. Include every supplied pending change exactly once. Do not invent facts or copy syntax from older release entries.

The final entry must have this exact structure:

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
- `CODE` with the classification for that individual change.
- `DIGIT` with the lowest digit used by any bullet.

The trailer must be exactly `<!-- stl-impact: v1 -->`, immediately follow the final bullet, and be the final line.

## Classify each change

Classify the effect described by the pending change, not merely the subsystem or implementation mechanism it mentions. Determine the letter first and the digit separately.

### Choose the letter

Use the first applicable letter in this order:

1. `A` — The public API contract changes.
2. `B` — An existing public operation has an observable runtime change, but its public API contract does not change.
3. `C` — Neither the public API contract nor the observable runtime behavior of a public operation changes.

#### Use `A` for public contract changes

Public API contract changes include:

- Adding or removing an exported name.
- Adding, removing, or renaming a public parameter.
- Changing a public function, method, or constructor signature.
- Changing accepted argument types or declared return types.
- Adding or changing type annotations that declare the types of public parameters, returns, attributes, or other public objects.
- Adding, removing, or changing another public type.

Both compatible additions and breaking removals belong to `A`. Runtime behavior being unchanged does not make a public signature or declared-type change `C`.

A marker or integration file that only helps type checkers discover already-declared types is `C`; it does not by itself change the public type contract.

#### Use `B` for observable runtime changes

Use `B` when an existing public call keeps the same API contract but changes any of the following:

- Returned values or other results.
- Raised exceptions.
- Side effects.
- Resource usage that callers can observe, including fixing a memory or resource leak.
- User-facing or explicitly claimed performance, including import time, execution time, latency, or memory consumption.

Bug fixes to public runtime behavior are normally `B`, even if the fixed behavior was unintended.

Classify an explicitly stated performance or resource improvement as `B` even when it was achieved through an internal refactor, cache change, deferred import, or similar implementation technique. A statement that output is unchanged excludes only a result change; it does not erase a separately stated timing, memory, exception, or side-effect change.

#### Use `C` for non-runtime and unobservable changes

Use `C` for changes limited to:

- Build or release configuration.
- Packaging or dependency management.
- CI and developer tooling.
- Tests.
- Documentation and examples.
- Type-checker discovery or integration that does not change declared public types.
- Internal implementation details with no stated observable runtime effect.

An internal implementation change is `C` only when the pending change does not also describe a public behavioral, performance, resource-usage, or contract change.

If multiple letters apply, select the earliest: `A` before `B` before `C`.

### Choose the digit

Choose the digit independently of the letter:

1. `1` — Breaking.
2. `2` — Externally visible and backward-compatible.
3. `3` — Strictly internal and externally unobservable.

#### Use digit `1` for breaking changes

Use `1` when supported caller code or a supported external workflow:

- Must be changed.
- Can now fail.
- Can no longer use a previously supported API or input.
- No longer receives behavior promised by the public contract.

A bug fix is not breaking merely because it changes an incorrect old result. Use `1` only if the old behavior was supported or documented and the change breaks reliance on it.

#### Use digit `2` for compatible visible changes

Use `2` for backward-compatible changes that users, downstream tools, or supported workflows can observe, including:

- Public API additions.
- Compatible public type or signature changes.
- Compatible behavior and bug fixes.
- Documented or explicitly claimed performance and resource improvements.
- Documentation changes.
- Type-checker integration.
- Compatible build, packaging, dependency, CI, or tooling changes.

Packaging, dependency, documentation, and tooling changes are normally `2`, because they alter shipped artifacts, project information, installation behavior, or supported workflows.

#### Use digit `3` only for wholly unobservable changes

Use `3` only when all of the following remain unchanged:

- Public API and declared public types.
- Runtime results and exceptions.
- Side effects and resource behavior.
- User-facing performance claims.
- Supported external workflows.
- Shipped artifacts and dependency behavior.
- Documentation and type-checker behavior.

Do not use `3` for a bug fix, leak fix, stated performance improvement, documentation update, packaging change, dependency change, or tooling change merely because its implementation is internal.

If two digits still appear applicable, choose the lower, more disruptive digit.

## Write the bullets

Write one bullet per pending change:

```text
- [LETTERDIGIT] Concise description of the change.
```

Preserve the supplied facts. Do not add compatibility, performance, or unchanged-behavior claims unless the pending change supports them.

Sort all bullets by code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

When multiple bullets have the same code, retain their order from the pending-changes list.

## Calculate Impact

Set `Impact` to the lowest digit appearing in any bullet, regardless of letter.

For example, bullets with digits `2`, `3`, and `2` produce:

```text
Impact: 2
```

Place the `Impact` line immediately below the release heading. Place the exact HTML trailer immediately after the final bullet, with no blank line or other content after it.