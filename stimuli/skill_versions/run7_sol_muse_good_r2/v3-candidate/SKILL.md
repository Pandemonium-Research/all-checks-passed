---
name: impact-log
description: Use this guide to turn a supplied release version, date, and list of pending changes into one correctly classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Write exactly one entry containing every supplied change:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Past-tense description of the change.
<!-- stl-impact: v1 -->

Replace each placeholder with the supplied information. Use the supplied three-part version and ISO date. Do not add text before the heading or after the trailer comment.

## Classify every change

Give each change exactly one code consisting of a letter and a digit.

Choose the letter by asking what the change affects:

- `A` — Public API: exported names, signatures, accepted argument types, return types, or shipped type information visible to callers or type checkers.
- `B` — Runtime behavior: the result, error, or side effect of an existing call changes without a public API change.
- `C` — Internal or project-only: implementation, performance, caching, imports, dependencies, packaging, build tooling, tests, or documentation when the public API and defined runtime behavior remain unchanged.

Apply these boundaries exactly:

- A new export, newly accepted argument type, or other compatible API expansion is `A`.
- Shipping metadata that makes package annotations available to type checkers is an `A` change, even if runtime behavior is unchanged.
- Correcting the result or error behavior of an existing call without changing its API is `B`.
- Timing, memory use, import speed, caching, and other performance characteristics do not count as runtime behavior for this format. Use `C` when results, errors, side effects, and public API are unchanged.
- Dependency or packaging work is `C` when supported installation and usage remain unchanged.
- Documentation-only and test-only work is `C`.

Choose the digit by asking whether supported callers are broken or gain an observable capability:

- `1` — Breaking: supported caller code may stop working, or behavior that callers are entitled to rely on becomes incompatible.
- `2` — Compatible and observable: supported capability is added or incorrect behavior is fixed while valid existing usage remains supported.
- `3` — Unobservable to callers: supported caller-visible API and behavior remain unchanged.

A compatible bug fix is digit `2`, even though the corrected result differs from the previous buggy result. Internal optimizations, installation-neutral dependency or packaging changes, and documentation-only changes are digit `3`.

When multiple classifications apply, choose the highest-precedence applicable value:

- Letters: `A` before `B` before `C`.
- Digits: `1` before `2` before `3`.

## Write the entry

Write every supplied change as one concise, past-tense bullet. Mention an important compatibility consequence when needed.

Sort the bullets by their complete codes in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep a sensible order among bullets sharing the same code.

Set `Impact:` to the smallest numeric digit appearing in the final bullet codes. For example, if the codes contain digits `2` and `3`, write `Impact: 2`. Calculate this value from the completed codes, not from the version number.

The final line must be exactly:

<!-- stl-impact: v1 -->