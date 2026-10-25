---
name: impact-log
description: Use when given a version, date, and pending changes to write release notes, a changelog entry, or version history in the project's parser-compatible impact-log format.
---

# Release notes

Produce exactly one release entry. Include every pending change once, classify each change independently, sort the bullets by code, and calculate the overall impact.

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT

- [CODE] Change description.
- [CODE] Change description.

<!-- stl-impact: v1 -->
```

Follow this format exactly:

- Use the supplied three-part version and date.
- Put `Impact:` immediately below the heading, without a blank line.
- Write exactly one bullet for each pending change. Do not combine, split, or omit changes.
- Begin each bullet with an unformatted code such as `[A2]`. Never bold the code.
- Leave one blank line before the trailer.
- End with the exact trailer `<!-- stl-impact: v1 -->`.
- Make the trailer the entry's final line. Add nothing after it.
- Do not copy conflicting formatting or classifications from older entries.

## Choose the letter

Test the categories in this order and use the first one that applies: A, then B, then C.

- **A — Public API or typing:** The change adds, removes, renames, or modifies an exported name, module, type, signature, parameter, default, accepted type, return type, public annotation, or other public typing contract.
- **B — Observable runtime behavior:** The public API and typing contract are unchanged, but callers can observe different results, exceptions, normalization, speed, import time, memory use, or other runtime behavior.
- **C — Project or environment:** The change affects only documentation, tests, CI, build or release tooling, packaging, dependencies, behavior-preserving internals, or the supported runtime, operating-system, or platform matrix.

Apply these distinctions strictly:

- A public API or typing change remains A even when it also changes runtime behavior.
- Adding public annotations or making shipped annotations visible to type checkers is A, not C.
- A speed, import-time, memory-use, or other resource-use change is B even when results are identical.
- An internal refactor is C only when callers cannot observe any API, typing, behavior, performance, or resource-use difference.
- A packaging or dependency change is C unless it changes the public typing contract, which takes precedence as A.
- Adding or dropping support for a runtime, language, operating system, or platform version is C.

## Choose the digit

Choose the digit independently of the letter. Test the digits in this order and use the first one that applies: 1, then 2, then 3.

- **1 — Breaking:** Previously supported code can now fail, stop installing or running, fail type checking, or receive a different result. Removing support for a previously supported environment is also breaking.
- **2 — Compatible and observable:** The change adds capability, makes a previously failing case work, exposes compatible typing information, adds environment support, or changes performance or resource use without changing the results of previously working code.
- **3 — Unobservable:** Supported callers and their tools cannot observe any change in API, typing, results, errors, compatibility, performance, or resource use.

Common classifications:

- Remove or rename an exported API: `A1`
- Remove a parameter or change an existing return type: `A1`
- Narrow a public typing contract so previously valid code is rejected: `A1`
- Add an exported API or optional parameter: `A2`
- Add non-narrowing public annotations or expose them to type checkers: `A2`
- Change an existing call's result without changing its signature: `B1`
- Make a formerly failing input succeed without changing successful inputs: `B2`
- Improve speed, import time, or memory use while preserving results: `B2`
- Drop a supported runtime or platform version: `C1`
- Change only documentation, tests, or CI: `C3`
- Make a behavior-preserving internal, packaging, or dependency change with no observable effect: `C3`

A bug fix is not automatically digit 2. If an input previously produced a result and now produces a different result, use digit 1. If it previously failed and now succeeds while working inputs remain unchanged, use digit 2.

## Sort and summarize

Sort bullets by their complete code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the pending-change order among bullets with the same code.

Set `Impact:` to the lowest digit used by any bullet, regardless of its letter. For example, if any bullet has digit 1, write `Impact: 1`.

If a classification remains genuinely ambiguous after applying these rules, choose the earliest applicable letter and the lowest applicable digit.