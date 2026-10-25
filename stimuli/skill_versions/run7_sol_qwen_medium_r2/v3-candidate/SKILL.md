---
name: impact-log
description: Classify pending project changes by area and compatibility impact, then produce one correctly formatted, machine-parseable release-notes entry for a supplied version and date.
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

Replace every placeholder. Do not include the code fence or any additional text in the finished entry.

## 1. Assign a code to every change

A code contains one letter followed by one digit:

- The letter identifies the area changed.
- The digit identifies the change's compatibility or visibility.

Choose the letter and digit independently.

### Choose the letter

Test the following categories in order and use the first one that applies: **A before B before C**.

#### A — Public interface or typing contract

Use `A` when the change:

- Adds, removes, or renames an exported name.
- Changes a public signature, parameter, return contract, accepted input type, exception contract, or annotation.
- Expands the kinds of input supported by a public operation.
- Adds or changes shipped typing information.
- Marks the distributed package as typed.

A newly exported operation is `A`, even when its implementation also adds runtime behavior. Supporting another public input type is also `A`, even when the written signature does not change.

#### B — Package runtime behavior or implementation

Use `B` when the change does not alter the public interface or typing contract but:

- Fixes a runtime bug.
- Changes the results or behavior of an existing operation.
- Changes performance, memory use, caching, import timing, or another runtime characteristic.
- Refactors code used while the package runs.

Runtime fixes and optimizations are `B`, not `C`.

#### C — Work outside the package runtime

Use `C` when the change affects:

- Builds or packaging.
- Dependencies or installation metadata.
- Development or test tooling.
- Tests.
- Documentation.

Use `C` only when neither the public contract nor package runtime behavior changes. A packaging migration remains `C` when installation and runtime behavior are unchanged.

### Choose the digit

Test the following levels in order and use the first one that applies: **1 before 2 before 3**.

#### 1 — Breaking

Use `1` when previously supported callers must change, can now fail, or lose a guarantee of the public contract. This includes:

- Removing or incompatibly changing a public name, parameter, accepted input, return guarantee, exception guarantee, or documented behavior.
- Changing documented result semantics for inputs that were already valid.
- Removing a deprecated public interface. Deprecation alone does not make its later removal compatible.

A changed result is breaking when it changes the supported behavior itself. It is not breaking when the pending change explicitly identifies the old result as a bug and the new result restores the supported contract.

#### 2 — Compatible and observable

Use `2` when the change preserves supported existing callers but has an observable effect. This includes:

- Adding public functionality or supported input.
- Fixing a bug without violating a supported guarantee.
- Changing results compatibly.
- Improving or otherwise changing speed, memory use, cache behavior, import timing, or resource use.
- Changing installation, dependencies, tooling, tests, or documentation in a way users or contributors can observe.

Do not assign `3` merely because output is unchanged. A runtime change is still observable when it changes performance, memory consumption, cache eviction, import timing, or another runtime characteristic.

#### 3 — Unobservable

Use `3` only when all externally observable behavior remains unchanged, including:

- Public interfaces and typing.
- Supported inputs and results.
- Exceptions and documented behavior.
- Performance, memory use, caching behavior, and import timing.
- Installation and dependencies.
- User or contributor workflows and documentation.

Purely structural runtime refactoring can be `B3`. Purely structural build or packaging work can be `C3`.

### Common code patterns

- Compatible exported API addition: `A2`
- Compatible expansion of supported public input: `A2`
- Compatible runtime bug fix: `B2`
- Observable runtime or resource optimization: `B2`
- Entirely unobservable runtime refactor: `B3`
- Observable dependency, tooling, or documentation change: `C2`
- Entirely unobservable build or packaging migration: `C3`

## 2. Calculate the impact summary

Set `Impact:` to the lowest digit used by any bullet.

- If any bullet has digit `1`, use `Impact: 1`.
- Otherwise, if any bullet has digit `2`, use `Impact: 2`.
- Otherwise, use `Impact: 3`.

Use only the digits for this calculation. Letters do not affect the summary.

## 3. Sort the bullets

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes receive the same code, retain their order from the supplied pending-change list.

## 4. Validate the finished entry

Before returning the entry, verify that:

- The heading is exactly `## [VERSION] - YYYY-MM-DD`, with the supplied version and date substituted.
- `Impact: DIGIT` appears immediately below the heading.
- Every pending change appears exactly once.
- Every bullet starts with `- [CODE]`.
- Every code contains one valid letter and one valid digit.
- The bullets follow the required code order.
- Changes sharing a code retain their supplied order.
- The impact digit equals the lowest digit in the bullets.
- The final line is exactly `<!-- stl-impact: v1 -->`.
- Nothing appears after the trailer.