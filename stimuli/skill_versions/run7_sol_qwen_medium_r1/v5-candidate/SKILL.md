---
name: impact-log
description: Use this skill when given a release version, ISO date, and pending changes to classify each change by consumer impact and produce one parser-compatible release-notes entry.
---

# Release notes

Produce exactly one entry containing every pending change exactly once:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace every placeholder with the supplied values. Do not output headings, explanations, or blank lines before, within, or after the entry. The HTML comment must be the exact final line.

## Classify each change

A code combines one letter with one digit. Determine the letter and digit independently from the change's actual effect, not from labels such as feature, fix, optimization, refactor, or migration.

If one change has several effects, use the highest-priority applicable letter (`A` before `B` before `C`) and the lowest applicable digit (`1` before `2` before `3`).

### Choose the letter

1. `A` — A public or static interface changes: exported names, public modules, signatures, parameters, accepted input types, return types or shapes, public annotations, exported exception types, or shipped typing metadata.
2. `B` — An existing public operation keeps the same interface but changes observably at runtime: values, exceptions, side effects, CLI output or exit status, execution speed, startup time, or import time.
3. `C` — Only documentation, internals, builds, packaging, dependencies, tooling, or tests change.

Apply these rules:

- New, removed, or renamed public APIs are `A`.
- A new optional parameter is `A`, even if its default preserves existing behavior.
- Broadening or narrowing accepted input types is `A`.
- Changing a public return type or shape is `A`; changing only the value returned through the same interface is `B`.
- Adding public exception classes is `A`; changing the exception raised by an existing operation is `B`.
- A shipped `py.typed` marker or equivalent typing metadata is `A`, not `C`.
- Runtime, startup, and import-time improvements are `B`, even when implemented by an internal optimization.
- An internal replacement is `C` only when behavior and consumer-visible performance are unchanged.
- Documentation and docstring changes are `C`.
- Packaging and dependency changes are `C` unless they also alter a public interface or runtime behavior.

### Choose the digit

1. `1` — Breaking: a previously supported or successful use can now fail, return a semantically different result, expose a different public type or exception, or require consumer changes.
2. `2` — Compatible and consumer-observable: the change adds capability, supports a new use, repairs a previously failing use while preserving successful uses, improves performance, adds consumer-facing documentation, exposes typing information, or compatibly changes installation behavior.
3. `3` — Consumer-unobservable: public interfaces, semantic runtime behavior, consumer-visible performance, documentation, and installation behavior are all unchanged.

Use these classifications:

| Change | Code |
|---|---|
| New public API | `A2` |
| Removed or renamed public API | `A1` |
| New optional parameter with a behavior-preserving default | `A2` |
| Broadened accepted input type | `A2` |
| Narrowed accepted input type | `A1` |
| Changed public return type or shape for an existing successful use | `A1` |
| Shipped typing metadata recognized by type checkers | `A2` |
| Different value or exception for a previously successful invocation, with no API change | `B1` |
| Fix for a case that previously failed, while preserving successful cases | `B2` |
| Faster execution, startup, or import with unchanged semantic results | `B2` |
| Consumer-facing documentation or docstring addition | `C2` |
| Compatible runtime dependency addition, removal, or vendoring that changes installed artifacts or dependency resolution | `C2` |
| Packaging or dependency change that breaks installation or requires consumer action | `C1` |
| Development-only dependency, test, or tooling change with no consumer effect | `C3` |
| Internal implementation change with unchanged behavior and consumer-visible performance | `C3` |

Do not classify an improvement as breaking merely because performance or a bug-related result changed. Performance improvements with unchanged semantic results are always digit `2`. A result or exit-status change for an invocation that previously completed successfully is digit `1`, even when described as a bug fix.

## Write and order the bullets

Write one concise bullet for each supplied change. State only supplied facts, retaining compatibility details needed to support the code. Do not combine changes, omit changes, duplicate changes, or invent effects.

Sort bullets in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes with the same code.

Set `Impact` to the smallest digit appearing in any bullet, regardless of letter.

Before returning the entry, verify:

- The heading exactly matches `## [VERSION] - YYYY-MM-DD` using the supplied version and date.
- There are no blank lines.
- Every pending change appears exactly once.
- Every bullet begins with one valid `[A-C][1-3]` code.
- Typing metadata uses `A`.
- Performance, startup-time, and import-time changes use `B`.
- Compatible performance improvements use digit `2`.
- Consumer-facing documentation and compatible runtime dependency changes use digit `2`, not `3`.
- Bullets follow the required code order.
- `Impact` is the smallest bullet digit.
- `<!-- stl-impact: v1 -->` is the exact final line.