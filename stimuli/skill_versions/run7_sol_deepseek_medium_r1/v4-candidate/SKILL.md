---
name: impact-log
description: Use when converting a release version, date, and list of pending changes into a classified, sorted, parser-compatible release-nototes entry.
---

# Release notes

Create exactly one release entry. Include every pending change once, classify each independently, sort the bullets by code, and calculate the entry’s overall impact.

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT

- [CODE] Change description.
- [CODE] Change description.

<!-- stl-impact: v1 -->
```

Follow the format exactly:

- Use the supplied three-part version and date.
- Put `Impact:` directly below the heading, with no blank line between them.
- Write exactly one bullet for each pending change. Do not combine, split, duplicate, or omit changes.
- Begin every bullet with an unformatted code such as `[A2]`. Do not bold the code.
- Leave one blank line before the trailer.
- End with the exact trailer `<!-- stl-impact: v1 -->`.
- Make the trailer the final line.
- Do not copy inconsistent formatting or classifications from older entries.

## Classify each change

A code contains a letter and a digit. Choose them independently.

### Choose the letter

Test the letters in this order and use the first one that applies: A, then B, then C.

- **A — Public API or typing contract:** The change adds, removes, renames, or modifies an exported name, module, type, signature, parameter, default, accepted type, return type, public annotation, or other public typing contract.
- **B — Observable runtime behavior:** The public API and typing contract are unchanged, but callers can observe different results, exceptions, normalization, performance, import time, memory use, or other resource use.
- **C — Project or environment:** The change affects only documentation, tests, CI, build or release tooling, packaging, dependencies, behavior-preserving internals, or supported runtime, operating-system, or platform versions.

Apply the precedence strictly:

- A public API or typing change is A even when it also changes runtime behavior.
- Adding public annotations or making shipped annotations visible to type checkers is A.
- A performance, import-time, or memory-use change is B even when results are identical.
- An internal refactor is C only when callers cannot observe any API, typing, behavior, performance, or resource-use difference.
- A dependency or packaging change is C unless it changes the public API, typing contract, or observable runtime behavior.
- Adding or dropping support for a runtime, language, operating system, or platform version is C.

### Choose the digit

Test the digits in this order and use the first one that applies: 1, then 2, then 3.

- **1 — Breaking:** Previously supported code can now fail, stop installing or running, fail type checking, or receive a different result.
- **2 — Compatible and observable:** The change adds capability, makes a previously failing case work, adds compatible typing information or environment support, or improves performance or resource use without changing previously working results.
- **3 — Unobservable:** Supported callers and their tools cannot observe any change in API, typing, results, errors, compatibility, performance, or resource use.

Do not classify every bug fix as digit 2:

- If a previously successful input now produces a different result, use digit 1.
- If a previously failing input now succeeds while previously successful inputs remain unchanged, use digit 2.
- If speed, import time, or memory use changes while results remain identical, use digit 2.
- Use digit 3 only when the change is entirely unobservable to supported callers and their tools.

### Common classifications

- Remove or rename an exported API: `A1`
- Remove a parameter or change an existing return type: `A1`
- Narrow public annotations so previously valid code is rejected: `A1`
- Add an exported API or optional parameter: `A2`
- Add compatible public annotations or expose them to type checkers: `A2`
- Change an existing call’s result without changing its public signature or types: `B1`
- Make a formerly failing input succeed without changing successful inputs: `B2`
- Improve speed, import time, or memory use while preserving results: `B2`
- Drop a supported runtime or platform version: `C1`
- Change only documentation, tests, or CI: `C3`
- Make an internal, packaging, or dependency change with no caller-visible effect: `C3`

## Sort and summarize

Sort bullets by their complete code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the pending-change order among bullets that have the same code.

Set `Impact:` to the lowest digit used by any bullet, regardless of its letter. If any bullet has digit 1, the impact is 1; otherwise, if any bullet has digit 2, the impact is 2; otherwise, the impact is 3.

When a change remains genuinely ambiguous after applying these rules, choose the earliest applicable letter and the lowest applicable digit.