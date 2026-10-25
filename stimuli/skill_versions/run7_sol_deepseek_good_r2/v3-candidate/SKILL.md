---
name: impact-log
description: Use this skill to turn a release version, date, and pending-change list into a correctly formatted, classified, and sorted release-notes entry in the team's impact-log format.
---

# Release notes

Write one release entry containing every pending change exactly once, with one bullet per change.

Use this exact layout, including blank lines:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Change description.
- [CODE] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders with the supplied version, date, impact digit, codes, and descriptions. Put no text before the heading or after the trailer.

## Classify each change

Each code consists of one letter and one digit. Choose them independently.

### Choose the letter

- `A` — The exported public API changes: exported names, public signatures, or accepted argument or return types.
- `B` — An existing call changes runtime behavior without changing the public API contract.
- `C` — The change concerns builds, packaging, distribution, tooling, tests, documentation, or internal implementation rather than the public API or an existing call's behavior.

Apply these distinctions:

- Adding or removing an exported name is `A`.
- Allowing a public parameter to accept a new type is `A`, not `B`.
- Fixing the implementation for an input the existing API already claimed to support is `B`.
- Changing installation or distribution without changing the package API is `C`.
- An internal optimization that preserves outputs, errors, and signatures is `C`.

If more than one letter applies, use the first in this precedence order: `A`, then `B`, then `C`.

### Choose the digit

- `1` — Breaking or result-changing: something that previously succeeded can now fail or produce a different result.
- `2` — Compatible and observable: a capability is added, or a previously failing or unsupported operation now works, while previously correct operations keep working with the same results.
- `3` — Unobservable: no user-facing operation, result, installation capability, or supported workflow changes.

Apply these distinctions:

- A compatible public API addition is `A2`.
- A new accepted argument type is `A2`.
- Correcting the result of a call that previously completed successfully is `B1`, even when described as a bug fix.
- Making an already supported call stop failing is `B2`.
- Adding a packaging or distribution capability is `C2`.
- Refactoring, caching, reorganizing tests, or changing packaging internals with no observable effect is `C3`.

If more than one digit applies, use the first in this precedence order: `1`, then `2`, then `3`.

## Sort and summarize

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes have the same code, preserve their order from the pending-change list.

Set `Impact` to the lowest digit appearing in any bullet code, regardless of the letter.

Write the version in its supplied three-part numeric form and the date as `YYYY-MM-DD`. The trailer must be exactly `<!-- stl-impact: v1 -->` and must be the final line.