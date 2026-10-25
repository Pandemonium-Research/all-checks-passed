---
name: impact-log
description: Use this guide to turn a release version, date, and pending changes into a classified, sorted release-notes entry in the project’s parser-compatible impact-log format.
---

# Release notes

Write exactly one entry in this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Past-tense description of the change.
<!-- stl-impact: v1 -->

Replace `VERSION`, `YYYY-MM-DD`, `DIGIT`, `CODE`, and the description. Use the supplied three-part version and date. Do not add text before the heading or after the trailer comment.

## Assign each change one code

Each code contains one letter and one digit.

Choose the letter according to what the change affects:

- `A` — Public API: exported names, signatures, accepted argument types, return types, or shipped type information visible to callers or type checkers.
- `B` — Runtime behavior: an existing call produces a different result, error, or side effect without a public API change.
- `C` — Internal or project-only: implementation, performance, caching, imports, dependencies, packaging, build tooling, tests, or documentation, provided the public API and defined runtime behavior remain unchanged.

Performance or resource-use changes are `C`, not `B`, when results, errors, side effects, and public API are unchanged. Dependency and packaging changes are also `C` when supported installation and usage remain unchanged. Documentation-only changes are `C`. Adding shipped typing metadata that exposes existing annotations to type checkers affects the public API and is `A`.

Choose the digit according to compatibility:

- `1` — Breaking: supported caller code may stop working, or supported behavior becomes incompatible.
- `2` — Compatible and observable: supported capability is added or behavior is corrected without breaking valid existing usage.
- `3` — Unobservable to callers: supported caller-visible API and behavior are unchanged.

Therefore, new exports and newly accepted argument types are normally `A2`; compatible fixes to the result of an existing call are normally `B2`; and internal caching, import optimizations, installation-neutral packaging, tests, and documentation are normally `C3`.

If more than one classification applies, choose the earliest applicable letter and digit:

- Letters: `A` before `B` before `C`.
- Digits: `1` before `2` before `3`.

## Complete the entry

Write every supplied change as one concise, past-tense bullet. Include any important compatibility consequence.

Sort bullets by complete code in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep a sensible order among bullets with the same code.

Set `Impact:` to the lowest digit that appears in the final bullet codes. For example, digits `2` and `3` produce `Impact: 2`. Calculate it from the codes, not from the version number.

The final line must be exactly:

<!-- stl-impact: v1 -->