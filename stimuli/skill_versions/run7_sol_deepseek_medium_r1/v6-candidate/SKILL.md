---
name: impact-log
description: Create one classified, sorted, parser-compatible release-notes entry from a supplied version, date, and list of pending project changes. Use when preparing this project's release notes, changelog, or version history.
---

# Release notes

Create exactly one release entry. Include every pending change once, classify each change independently, sort the bullets by code, and calculate the overall impact.

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
- Put `Impact:` directly below the heading, with no blank line between them.
- Write exactly one bullet for each pending change. Do not combine, split, duplicate, or omit changes.
- Preserve each change’s factual meaning. Do not invent compatibility guarantees or effects that were not supplied.
- Begin every bullet with an unformatted code such as `[A2]`. Do not bold the code.
- Leave one blank line before the trailer.
- End with the exact trailer `<!-- stl-impact: v1 -->`.
- Make the trailer the final line. Add no title, explanation, or code fence around the completed entry.
- Do not copy conflicting formatting or classifications from older release entries.

## Classify each change

A code contains one letter and one digit. Choose the letter and digit independently.

Classify the effect of the change, not merely the implementation area named in its description. For example, an internal optimization with measurable performance or memory effects is observable runtime behavior, while a packaging change that exposes public typing information is a typing-contract change.

### Choose the letter

Test the letters in this order and use the first one that applies: A, then B, then C.

- **A — Public API or typing contract:** An exported name, module, type, signature, parameter, default, accepted type, return type, public annotation, or other public contract is added, removed, renamed, or modified.
- **B — Observable runtime behavior:** The public API and typing contract are unchanged, but callers can observe different results, exceptions, normalization, performance, import time, memory use, or other runtime or resource behavior.
- **C — Project or environment:** The change affects only documentation, tests, CI, build or release tooling, packaging, dependencies, behavior-preserving internals, or supported language, runtime, operating-system, or platform versions.

Apply the precedence strictly:

- Use A whenever the public API or typing contract changes, even if runtime behavior also changes.
- Adding public annotations or making shipped annotations visible to type checkers is A, not C.
- Changing the runtime value returned within an unchanged public signature and type contract is B.
- A performance, import-time, memory-use, or other resource-use change is B even when functional results are identical.
- An internal refactor is C only when callers cannot observe any API, typing, behavior, performance, or resource-use difference.
- A packaging or dependency change is C only when it does not alter the public API, typing contract, or observable runtime behavior.
- Adding or dropping support for a language, runtime, operating-system, or platform version is C.

### Choose the digit

Test the digits in this order and use the first one that applies: 1, then 2, then 3.

- **1 — Breaking:** A previously supported use can now fail, stop installing or running, fail type checking, or produce a different result.
- **2 — Compatible and observable:** The change adds capability, makes a previously failing case work, adds compatible typing or environment support, or improves performance or resource use without changing previously successful results.
- **3 — Unobservable:** Supported callers and their type-checking or runtime tools cannot observe any difference in API, typing, results, errors, compatibility, performance, or resource use.

Apply these rules even when a change is described as a fix:

- If a previously successful input now produces a different result, use digit 1.
- If a previously failing input now succeeds while previously successful inputs remain unchanged, use digit 2.
- If speed, import time, or memory use changes while functional results remain identical, use digit 2.
- Use digit 3 only when the change is entirely unobservable within the public API, supported environments, type checking, and runtime behavior. Documentation, tests, and CI-only changes qualify as unobservable for this classification.

### Common classifications

- Remove or rename an exported API: `A1`
- Remove a parameter or add a required parameter: `A1`
- Change a public return type or narrow public annotations: `A1`
- Add an exported API or optional parameter: `A2`
- Add compatible public annotations or expose them to type checkers: `A2`
- Change a previously successful call’s result without changing its public signature or types: `B1`
- Make a formerly failing input succeed without changing successful inputs: `B2`
- Improve speed, import time, or memory use while preserving results: `B2`
- Drop a supported runtime or platform version: `C1`
- Add support for a runtime or platform version: `C2`
- Change only documentation, tests, or CI: `C3`
- Make a behavior-preserving internal, packaging, or dependency change with no caller-visible effect: `C3`

## Sort the bullets

Sort bullets by complete code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the original pending-change order among bullets that have the same code.

## Calculate the impact

Set `Impact:` to the lowest digit used by any bullet, regardless of its letter:

- If any bullet has digit 1, use `Impact: 1`.
- Otherwise, if any bullet has digit 2, use `Impact: 2`.
- Otherwise, use `Impact: 3`.

If a classification remains genuinely ambiguous after applying all rules, choose the earliest applicable letter and the lowest applicable digit.