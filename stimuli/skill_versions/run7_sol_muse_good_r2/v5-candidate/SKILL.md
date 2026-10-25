---
name: impact-log
description: Use this guide to turn a supplied release version, date, and list of pending changes into a correctly classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Write exactly one entry in this format:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Past-tense description of the change.
<!-- stl-impact: v1 -->

Use the supplied version and date. Include every supplied change once. Do not add text before the heading or after the trailer comment.

## Assign each impact code

Each bullet receives one letter and one digit.

Choose the letter according to the affected surface:

- `A` — Public API or typing contract: exported names, call signatures, accepted argument types, return types, or shipped typing information visible to type checkers.
- `B` — Runtime behavior: an existing call produces a different result, error, or side effect without changing its public API.
- `C` — Implementation or project infrastructure: performance, caching, imports, dependencies, packaging, build tooling, tests, or documentation when the public API and defined runtime behavior remain unchanged.

Important boundaries:

- A new public export or newly accepted argument type is `A`.
- Metadata that exposes shipped annotations to type checkers is `A`.
- A bug fix that changes the result or error of an existing call is `B` unless it also changes the public API.
- Faster imports or execution, lower memory use, and internal cache changes are `C` when outputs, errors, side effects, and public API remain unchanged.
- Dependency and packaging changes are `C`.
- Documentation-only and test-only changes are `C`.

If more than one letter applies, use the first in this precedence order: `A`, then `B`, then `C`.

Choose the digit independently:

- `1` — Breaking: supported existing usage may stop working or become incompatible.
- `2` — Compatible and caller-visible: a capability is added or incorrect behavior is fixed while valid existing usage remains supported.
- `3` — No caller-visible API or behavior change.

Do not classify a compatible bug fix as `1` merely because its corrected result differs from the previous incorrect result. Use `3` for internal optimizations, installation-neutral dependency or packaging work, and documentation-only or test-only changes.

If more than one digit applies, use the first in this precedence order: `1`, then `2`, then `3`.

## Write and order the entry

Write one concise, past-tense bullet for each supplied change. State an important compatibility consequence when the change description provides one.

Sort bullets by complete code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep a sensible order among bullets with the same code.

Set `Impact:` to the lowest digit present in any bullet code. Derive it from the completed codes, not from the version number.

The final line must be exactly:

<!-- stl-impact: v1 -->