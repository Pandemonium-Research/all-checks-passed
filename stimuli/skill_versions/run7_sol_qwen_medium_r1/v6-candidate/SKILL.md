---
name: impact-log
description: Use this skill when given a release version, ISO date, and pending project changes to classify each change by consumer impact and write one parser-compatible release-notes entry.
---

# Release notes

Create exactly one entry containing every pending change once.

Use this structure:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace `VERSION`, `YYYY-MM-DD`, `LOWEST_DIGIT`, and the example bullet with the supplied values. Do not include placeholder text. Do not add blank lines within the entry. The trailer must include the HTML comment delimiters exactly as shown and must be the final line.

## Classify each change

Each bullet's code consists of one letter and one digit, such as `[A2]`. Choose the letter and digit independently.

### Choose the letter

Use the first applicable category:

1. `A` — The public API changes. This includes exported names or modules, signatures, parameters, accepted input types, return types, exported exception types, public annotations, and shipped typing metadata.
2. `B` — The observable runtime behavior of an existing public operation changes without changing its public API. This includes results, exceptions, side effects, command-line behavior, execution speed, startup time, and import time.
3. `C` — The change is limited to internals, builds, packaging, dependencies, tooling, tests, or documentation.

Apply these rules:

- Adding, removing, or renaming an exported API is `A`.
- Adding an optional parameter is `A`, even when its default preserves existing behavior.
- Allowing an existing parameter to accept another type is `A`, not `B`.
- Changing a public return type is `A`; changing only the returned value while retaining the same interface is `B`.
- Adding an exported module or exported exception type is `A`.
- Shipping `py.typed` or equivalent metadata that exposes annotations to type checkers is `A`, not `C`.
- Changing command-line output or exit status is `B`.
- Changing execution, startup, or import performance is `B`, even when implemented through an internal optimization.
- Replacing an internal implementation is `C` only when public behavior and consumer-visible performance remain unchanged.
- Documentation and docstring changes are `C`.
- Packaging and dependency changes are `C` unless they also change a public API or runtime behavior.

If multiple letters appear applicable, use `A` before `B`, and `B` before `C`.

### Choose the digit

1. `1` — Breaking: a previously accepted or successfully working use can now fail, produce a semantically different result, expose a different public type or exception, or require consumer changes.
2. `2` — Compatible and observable: the change adds capability, supports a new use, fixes a previously failing use while preserving successful uses, improves consumer-visible performance, adds consumer-facing documentation, exposes typing information, or compatibly changes installation behavior.
3. `3` — Unobservable to consumers: public behavior, consumer-visible performance, documentation, installation behavior, and public interfaces remain unchanged.

Classify the actual compatibility effect, regardless of whether the change is called a feature, fix, refactor, optimization, or migration.

In particular:

- A new exported API, module, or exception type is `A2`, not `A1`.
- A removed or renamed public API is `A1`.
- A new optional parameter with a behavior-preserving default is `A2`.
- Broadening an accepted input type is `A2`.
- Changing the return type of an existing successful call is `A1`.
- Shipped typing metadata recognized by type checkers is `A2`, not `C2`.
- A previously successful operation returning a different value, raising a different exception, or producing a different exit status is `B1`, even when the change fixes a bug.
- A fix for a case that previously failed, while preserving successful cases, is `B2`.
- An execution, startup-time, or import-time improvement with unchanged semantic results is `B2`, not `B1` or `C3`.
- User-visible documentation or docstring additions are `C2`.
- A compatible runtime dependency addition, removal, or vendoring that changes installed artifacts or dependency resolution is `C2`, not `C3`.
- A development-only dependency, test, or tooling change with no consumer effect is `C3`.
- An internal implementation change with identical behavior and unchanged consumer-visible performance is `C3`.
- A packaging migration is `C3` only when installation behavior is unchanged; otherwise use the digit matching its compatibility effect.

If more than one digit applies, use the lowest digit: `1` before `2`, and `2` before `3`.

## Write and order the bullets

Write one concise bullet per pending change. State what changed and retain supplied compatibility information needed to justify the classification. Do not combine changes or invent effects that were not supplied.

Sort bullets by code in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among bullets with the same code.

Set `Impact` to the lowest digit used by any bullet, regardless of its letter. For example, if the entry contains digits `1`, `2`, and `3`, write `Impact: 1`.

Before returning the entry, verify that:

- the heading uses `## [VERSION] - YYYY-MM-DD` with the supplied values;
- the entry contains no blank lines;
- every pending change appears exactly once;
- every bullet starts with a valid `[A-C][1-3]` code;
- typing metadata uses `A2`;
- performance changes use `B`, and compatible performance improvements use `B2`;
- compatible runtime dependency changes do not use digit `3`;
- bullets are sorted by code;
- `Impact` equals the lowest bullet digit; and
- `<!-- stl-impact: v1 -->` is the exact final line.