---
name: impact-log
description: Use when converting a supplied release version, date, and list of pending changes into the project's classified, sorted, parser-compatible release notes entry.
---

# Release notes

Produce exactly one release entry containing every pending change exactly once.

## Required output

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT

- [CODE] Change description.
- [CODE] Change description.

<!-- stl-impact: v1 -->
```

Follow these requirements exactly:

- Use the supplied three-part version and date.
- Put `Impact:` immediately below the heading, with no intervening blank line.
- Write one bullet for each pending change. Do not combine, split, duplicate, or omit changes.
- Start every bullet with an unformatted code such as `[A2]`. Do not bold the code.
- Leave one blank line before the trailer.
- End with the exact trailer `<!-- stl-impact: v1 -->`.
- Make the trailer the final line; add nothing after it.
- Do not include a title, explanation, or code fence around the entry.
- Do not copy conflicting formatting or classifications from existing release entries.

## Classify each change

Each code consists of one letter and one digit. Choose the letter and digit independently.

### Choose the letter

Test the letters in this order and use the first applicable category: A, then B, then C.

- **A — Public API or typing contract:** The change adds, removes, renames, or modifies an exported name, module, type, signature, parameter, default, accepted type, return type, public annotation, or other public typing contract.
- **B — Observable runtime behavior:** The public API and typing contract are unchanged, but callers can observe a difference in results, exceptions, normalization, performance, import time, memory use, or other runtime behavior or resource use.
- **C — Project or environment:** The change affects only documentation, tests, CI, build or release tooling, packaging, dependencies, behavior-preserving internals, or supported runtime, operating-system, or platform versions.

Apply the precedence strictly:

- A public API or typing change is A even if it also changes runtime behavior.
- Adding public annotations or making shipped annotations visible to type checkers is A, not C.
- A performance, import-time, memory-use, or other resource-use change is B even when functional results are identical.
- An internal refactor is C only if callers cannot observe any difference in API, typing, behavior, performance, or resource use.
- A packaging or dependency change is C only if it does not alter the public API, typing contract, or observable runtime behavior.
- Adding or dropping support for a language, runtime, operating-system, or platform version is C.

### Choose the digit

Test the digits in this order and use the first applicable category: 1, then 2, then 3.

- **1 — Breaking:** Previously supported code can now fail, stop installing or running, fail type checking, or receive a different result.
- **2 — Compatible and observable:** The change adds capability, makes a previously failing case work, provides compatible typing information, adds environment support, or changes performance or resource use without changing the results of previously successful code.
- **3 — Unobservable:** Supported callers and their tools cannot observe any difference in API, typing, results, errors, compatibility, performance, or resource use.

Use these rules for common cases:

- Removing or renaming an exported API: `A1`
- Removing a parameter or adding a required parameter: `A1`
- Changing an existing return type or default in a way that affects callers: `A1`
- Narrowing public types so previously valid code is rejected: `A1`
- Adding an exported API or optional parameter: `A2`
- Adding compatible public annotations or exposing them to type checkers: `A2`
- Changing the result of a previously successful call without changing its public signature or types: `B1`
- Making a formerly failing input succeed while preserving previously successful results: `B2`
- Improving speed, import time, or memory use while preserving results: `B2`
- Dropping a supported runtime or platform version: `C1`
- Adding support for a runtime or platform version: `C2`
- Changing only documentation, tests, or CI: `C3`
- Making an internal, packaging, or dependency change with no caller-visible effect: `C3`

A bug fix is not automatically digit 2. If a previously successful input now produces a different result, use digit 1. Use digit 2 only when the change is compatible with all previously successful uses, such as making a formerly failing case succeed or improving resource use without changing results.

## Sort the bullets

Sort bullets by complete code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the original pending-change order among bullets with the same code.

## Calculate the impact

Set `Impact:` to the lowest digit used by any bullet, regardless of its letter:

- If any bullet has digit 1, use `Impact: 1`.
- Otherwise, if any bullet has digit 2, use `Impact: 2`.
- Otherwise, use `Impact: 3`.

If a classification remains genuinely ambiguous after applying all rules, choose the earliest applicable letter and the lowest applicable digit.