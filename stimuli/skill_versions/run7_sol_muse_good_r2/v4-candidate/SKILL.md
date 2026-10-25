---
name: impact-log
description: Use this guide to convert a supplied version, date, and list of pending changes into one classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Write exactly one entry containing every supplied change:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Past-tense description of the change.
<!-- stl-impact: v1 -->

Replace the placeholders with the supplied version, date, impact digit, code, and change description. Do not add text before the heading or after the trailer comment.

## Classify each change

Assign every change exactly one code: one letter followed by one digit.

### Choose the letter

Use the first applicable category:

1. `A` — Public API. Use this for changes to exported names, signatures, accepted argument types, return types, or shipped typing information visible to callers or type checkers.
2. `B` — Runtime behavior. Use this when an existing call produces a different result, error, or side effect without a public API change.
3. `C` — Project or implementation details. Use this for internal implementation, performance, caching, imports, dependencies, packaging, build tooling, tests, or documentation when the public API and defined runtime behavior remain unchanged.

Apply these boundaries:

- Adding an export or accepting a new argument type is `A`.
- Shipping metadata that exposes package annotations to type checkers is `A`, even when runtime behavior is unchanged.
- Correcting the result, error, or side effect of an existing call without changing its API is `B`.
- Faster execution, reduced memory use, deferred imports, and internal caching are `C` when results, errors, side effects, and public API remain unchanged.
- Dependency or packaging changes are `C` when supported installation and use remain unchanged.
- Documentation-only and test-only changes are `C`.

If multiple letters apply, use the earliest one: `A` before `B` before `C`.

### Choose the digit

Use the first applicable level:

1. `1` — Breaking. Supported caller code may stop working, or supported behavior becomes incompatible.
2. `2` — Compatible and observable. A supported capability is added or incorrect behavior is fixed without breaking valid existing usage.
3. `3` — Unobservable to callers. Supported caller-visible API and behavior remain unchanged.

A bug fix is `2` when it corrects previously incorrect behavior while preserving valid usage; do not mark it `1` merely because the corrected result differs from the buggy result. Internal optimizations and documentation-only changes are `3`. Installation-neutral dependency and packaging changes are also `3`.

If multiple digits apply, use the lowest one: `1` before `2` before `3`.

## Write and order the bullets

Write one concise, past-tense bullet for every supplied change. Include any important compatibility consequence.

Sort bullets by their complete codes in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep a sensible order among bullets with the same code.

Set `Impact:` to the lowest digit used by any bullet. For example, an entry containing digits `2` and `3` has `Impact: 2`. Derive this value from the completed codes, not from the version number.

The final line must be exactly:

<!-- stl-impact: v1 -->