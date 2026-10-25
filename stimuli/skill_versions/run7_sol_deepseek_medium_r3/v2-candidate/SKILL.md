---
name: impact-log
description: Create a parser-compatible release-notes entry from a supplied version, date, and list of pending project changes. Use when writing release notes, changelog entries, or version history in the project's impact-log format.
---

# Release notes

Create exactly one release entry:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Description of change.

<!-- stl-impact: v1 -->

Use the supplied three-part version and date exactly. Write one bullet for every pending change. Do not add other headings, prose, or comments. The trailer comment must be the entry’s final line.

## Classify each change

Each code contains a letter and a digit. Choose them independently: the letter identifies what changed, while the digit identifies its compatibility impact.

### Choose the letter

Use the first applicable letter:

- `A` — The public API surface changes: an exported name is added, removed, or renamed; a public signature changes; accepted argument types broaden or narrow; or a documented return type changes.
- `B` — An existing public call retains the same API surface, but its runtime semantics change, including returned values, exceptions, side effects, normalization, or formatting.
- `C` — No supported public API or runtime semantics change. Use this for internal implementation, performance, build, packaging, tooling, test, and documentation changes.

A changed value from an existing call is `B`, not `A`, unless the public signature or documented type also changes. If a change fits multiple categories, precedence is `A`, then `B`, then `C`.

### Choose the digit

Apply these tests in order:

1. Use `1` if any previously supported, successful use can now fail, require caller changes, return a different value or type, or produce different side effects. This applies even when the change is described as a fix.
2. Otherwise, use `2` if capability is added or repaired without changing previously successful supported uses. New APIs, broader accepted inputs, and support for inputs that previously failed or were unsupported are `2`.
3. Otherwise, use `3` when there is no functional difference for supported callers.

Determine the digit from the before-and-after effect, not from words such as “added” or “fixed.” In particular:

- Adding a public API is `A2`, not `A1`.
- Removing a public API or changing its return type incompatibly is `A1`.
- Broadening accepted argument types is `A2`.
- Changing the result for an input that already completed successfully is `B1`.
- Making a previously failing or unsupported input succeed is `B2`.
- A maintenance-only change with unchanged functional behavior is normally `C3`.

For compatibility changes outside the exported API, such as removing a supported runtime or installation environment, keep the appropriate non-API letter and use digit `1`.

Base classifications only on stated effects. Do not invent hypothetical incompatibilities.

## Compute the entry impact

Set `Impact` to the lowest digit used by any bullet. For example, digits `2`, `2`, and `3` produce `Impact: 2`.

## Order and write the bullets

Sort bullets by complete code in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied relative order of changes that receive the same code.

Write each description as a concise sentence stating what changed and, when relevant, its effect on callers. End every bullet with a period.