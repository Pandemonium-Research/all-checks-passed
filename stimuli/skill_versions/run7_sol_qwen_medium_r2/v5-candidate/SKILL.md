---
name: impact-log
description: Use this document to classify a supplied list of pending project changes and turn it into one sorted, machine-parseable release-notes entry for the supplied version and date.
---

# Release notes

Given a version, date, and list of pending changes, return exactly one release entry. Include every pending change exactly once.

Use this structure:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace every placeholder. Do not return the code fence, an explanation, or any other text.

## 1. Classify every change

Each code contains one letter followed by one digit:

- The letter identifies the affected area.
- The digit identifies compatibility or visibility.

Choose the letter and digit independently. Classify every change before sorting the bullets.

### Choose the letter

Test the categories in this order and use the first match: **A, then B, then C**.

#### A — Public interface or typing contract

Use `A` when the change:

- Adds, removes, or renames an exported name.
- Changes a public signature, parameter, return contract, accepted input type, exception contract, or annotation.
- Expands the supported inputs of a public operation.
- Adds or changes shipped typing information.
- Marks the distributed package as typed.

A newly exported operation is `A`, even though it also adds runtime behavior. An accepted-input expansion is `A`, even when the written signature does not change.

#### B — Package runtime behavior or implementation

Use `B` when the change is not `A` and it:

- Fixes a runtime bug.
- Changes the result or behavior of an existing operation.
- Changes performance, memory use, caching, cache eviction, import timing, or another runtime characteristic.
- Refactors code that runs as part of the package.

Runtime fixes, optimizations, cache changes, and internal runtime refactors are `B`, not `C`.

#### C — Work outside the package runtime

Use `C` only when the change is neither `A` nor `B` and it affects:

- Builds or packaging.
- Dependencies or installation metadata.
- Development or test tooling.
- Tests.
- Documentation.

A build or packaging migration is `C` when it does not change the public contract or package runtime behavior.

### Choose the digit

Test the levels in this order and use the first match: **1, then 2, then 3**.

#### 1 — Breaking

Use `1` when previously supported callers must change, can now fail, receive different supported results, or lose a public guarantee.

This includes:

- Removing or incompatibly changing a public name, parameter, accepted input, return guarantee, exception guarantee, or documented behavior.
- Removing a deprecated public interface. Deprecation does not make its removal compatible.
- Changing result semantics for inputs that were already supported.

A result change for previously supported input is `1` unless the pending change explicitly identifies the old result as a bug and the new result as a compatible correction. Do not infer that a behavior change is a bug fix merely because the new behavior seems preferable.

#### 2 — Compatible and observable

Use `2` when supported existing callers remain compatible and the change has any observable effect.

This includes:

- Adding public functionality or supported input.
- Fixing an explicitly identified bug without violating a supported guarantee.
- Making a compatible result or behavior change.
- Changing speed, memory use, caching, cache eviction, import timing, or resource use.
- Changing installation, dependencies, tooling, tests, or documentation in a way users or contributors can observe.

Unchanged output does not imply digit `3`. A runtime optimization or cache-policy change is `B2` when it changes performance, memory use, eviction behavior, timing, or another runtime characteristic.

#### 3 — Unobservable

Use `3` only when every externally observable property remains unchanged, including:

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
- Changed semantics for previously supported input, unless explicitly identified as a compatible bug fix: `B1`
- Compatible runtime bug fix: `B2`
- Runtime performance, memory, cache, or import-timing change: `B2`
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

After classifying all changes, sort the bullets in this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

All `A` bullets must precede all `B` bullets, and all `B` bullets must precede all `C` bullets. For changes with the same code, preserve their order from the supplied pending-change list.

## 4. Validate the finished entry

Before returning it, verify that:

- The heading is exactly `## [VERSION] - YYYY-MM-DD`, using the supplied values.
- `Impact: DIGIT` appears immediately below the heading.
- Every pending change appears exactly once.
- Every bullet starts with `- [CODE]`.
- Every code contains one valid letter and one valid digit.
- Public API removal, including deprecated API removal, is `A1`.
- A result change for previously supported input is digit `1` unless explicitly described as a compatible bug fix.
- Performance, memory, cache, and import-timing changes are digit `2`, even when output is unchanged.
- Bullets follow the exact required code order.
- Changes sharing a code retain their supplied order.
- The impact digit is the lowest digit among all bullets.
- The final line is exactly `<!-- stl-impact: v1 -->`.
- Nothing appears after the trailer.