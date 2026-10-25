---
name: impact-log
description: Use this document when converting a supplied version, date, and pending-change list into one classified, sorted, machine-parseable release-notes entry.
---

# Release notes

Given a version, date, and list of pending changes, return exactly one release entry. Include every pending change exactly once.

The finished entry must have this form:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace every placeholder. Return no code fence, explanation, or other text.

## 1. Classify every change

Each bullet code contains one letter followed by one digit:

- The letter identifies the affected area.
- The digit identifies compatibility or visibility.

Choose the letter and digit independently.

### Choose the letter

Test the categories in this order and use the first match: **A, then B, then C**.

#### A — Public interface or typing contract

Use `A` if the change:

- Adds, removes, or renames an exported name.
- Changes a public signature, parameter, return contract, accepted input type, exception contract, or annotation.
- Adds a supported input type or otherwise expands a public operation's accepted inputs.
- Adds or changes shipped typing information.
- Marks the distributed package as typed.

A newly exported operation is `A`, even though it also introduces runtime behavior. An accepted-input expansion is `A`, even when the written signature is unchanged.

#### B — Package runtime behavior or implementation

Use `B` if the change is not `A` and it:

- Fixes a runtime bug.
- Changes the result or behavior of an existing operation.
- Changes performance, memory use, caching, cache eviction, import timing, or resource use.
- Refactors code that runs as part of the package.

Runtime fixes, optimizations, cache changes, and internal runtime refactors are `B`, not `C`.

#### C — Work outside the package runtime

Use `C` only if the change is neither `A` nor `B` and it affects:

- Builds or packaging.
- Dependencies or installation metadata.
- Development or test tooling.
- Tests.
- Documentation.

A build or packaging migration is `C` when it does not change the public contract or package runtime behavior.

### Choose the digit

Test the levels in this order and use the first match: **1, then 2, then 3**.

#### 1 — Breaking

Use `1` if previously supported callers must change, can now fail, receive different documented results, or lose a public guarantee.

This includes:

- Removing or incompatibly changing a public name, parameter, accepted input, return guarantee, exception guarantee, or documented behavior.
- Removing a deprecated public interface.
- Changing result semantics for inputs that were already valid.

Treat a result change for previously valid input as breaking unless the pending change explicitly says that the old result was a bug and the new result restores the supported contract. Do not assume that a behavior change is a bug fix merely because the new behavior seems preferable.

#### 2 — Compatible and observable

Use `2` if supported existing callers remain compatible and the change has any observable effect.

This includes:

- Adding public functionality or supported input.
- Fixing an explicitly identified bug without violating a supported guarantee.
- Making a compatible result or behavior change.
- Changing performance, memory use, caching, cache eviction, import timing, or resource use.
- Changing installation, dependencies, tooling, tests, or documentation in a user- or contributor-visible way.

Output does not need to change for digit `2` to apply. Performance and cache behavior are observable. For example, replacing an unbounded cache with a bounded one is `B2` even if returned values are unchanged.

#### 3 — Unobservable

Use `3` only if every externally observable property remains unchanged, including:

- Public interfaces and typing.
- Supported inputs, results, exceptions, and documented behavior.
- Performance, memory use, caching, cache eviction, import timing, and resource use.
- Installation and dependencies.
- User and contributor workflows.
- Documentation.

Use `B3` only for a purely structural runtime refactor with no observable runtime effect. Use `C3` only for purely structural external work with no observable installation, workflow, or documentation effect.

### Classification reference

- Compatible exported API addition: `A2`
- Compatible expansion of supported public input: `A2`
- Removal of a public API, including a deprecated one: `A1`
- Changed semantics for previously valid input, unless explicitly identified as a contract-restoring bug fix: `B1`
- Compatible runtime bug fix: `B2`
- Runtime performance, memory, import-timing, or cache change: `B2`
- Purely structural runtime refactor: `B3`
- Observable dependency, tooling, test, or documentation change: `C2`
- Purely structural build or packaging change: `C3`

## 2. Calculate the impact summary

Set `Impact:` to the lowest digit used by any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only the digits. Letters do not affect the summary.

## 3. Sort the bullets

Sort bullets in this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For changes with the same code, preserve their order from the supplied pending-change list.

## 4. Validate the finished entry

Before returning it, verify that:

- The heading is exactly `## [VERSION] - YYYY-MM-DD`, using the supplied values.
- `Impact: DIGIT` is immediately below the heading.
- Every pending change appears exactly once.
- Every bullet starts with `- [CODE]`.
- Every code contains one valid letter and one valid digit.
- Result changes for previously valid inputs are digit `1` unless explicitly described as contract-restoring bug fixes.
- Performance, memory, cache, and import-timing changes are digit `2`, even when output is unchanged.
- Bullets follow the required code order.
- Changes sharing a code retain their supplied order.
- The impact digit is the lowest digit among all bullets.
- The final line is exactly `<!-- stl-impact: v1 -->`.
- Nothing appears after the trailer.