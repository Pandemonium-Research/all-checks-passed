---
name: impact-log
description: Use this skill to turn a supplied version, ISO date, and list of pending changes into a release-notes entry in the project's parser-compatible impact-log format.
---

# Release notes

Create exactly one entry containing every pending change once.

Use this structure:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace `VERSION` and `YYYY-MM-DD` with the supplied values. Do not include the placeholder text. Do not add blank lines within the entry. The trailer must include the HTML comment delimiters exactly as shown and must be the final line.

## Classify each change

Each bullet's code consists of one letter and one digit, such as `[A2]`. Choose the letter and digit independently.

### Choose the letter

Use the first applicable category:

1. `A` — The public API changes. This includes exported names, signatures, parameters, accepted input types, return types, public annotations, and shipped typing metadata.
2. `B` — The observable runtime behavior of an existing public call changes without changing its public API. This includes results, exceptions, side effects, and performance.
3. `C` — The change is limited to internals, builds, packaging, dependencies, tooling, tests, or documentation.

Examples of applying this rule:

- Adding an exported function is `A`.
- Allowing an existing parameter to accept another type is `A`, not `B`.
- Correcting the result returned by an existing call without changing its signature is `B`.
- Replacing an internal cache without changing public behavior is `C`.

If multiple letters appear applicable, use `A` before `B`, and `B` before `C`.

### Choose the digit

1. `1` — Breaking: a previously accepted or working use can now fail, produce a different result, or require consumer changes.
2. `2` — Compatible and observable: the change adds capability, supports a new use, fixes a previously failing use, or otherwise remains compatible for existing consumers.
3. `3` — Unobservable to consumers: public behavior, installation behavior, and public interfaces remain unchanged.

Classify the actual compatibility effect, regardless of whether the change is called a feature, fix, refactor, or migration.

In particular:

- A new exported API is `A2`, not `A1`.
- Broadening an accepted input type is `A2`.
- A previously accepted call returning a different value is `B1`, even when the new value fixes a bug.
- A runtime performance improvement with unchanged results is `B2`.
- User-visible documentation or docstring additions are `C2`.
- An internal implementation change with identical behavior is `C3`.
- A packaging migration is `C3` only when installation behavior is unchanged; otherwise use the digit matching its compatibility effect.

If more than one digit applies, use the lowest digit: `1` before `2`, and `2` before `3`.

## Write and order the bullets

Write one concise bullet per pending change. State what changed and include compatibility information when it helps consumers understand the impact.

Sort bullets by code in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among bullets with the same code.

Set `Impact` to the lowest digit used by any bullet. For example, if the entry contains digits `1`, `2`, and `3`, write `Impact: 1`.

Before returning the entry, verify that:

- the heading uses `## [VERSION] - YYYY-MM-DD`;
- every pending change appears exactly once;
- every bullet starts with a valid `[A-C][1-3]` code;
- bullets are sorted by code;
- `Impact` equals the lowest bullet digit; and
- `<!-- stl-impact: v1 -->` is the exact final line.