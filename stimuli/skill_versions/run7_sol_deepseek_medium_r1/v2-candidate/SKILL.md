---
name: impact-log
description: Use when converting a release version, date, and list of pending changes into a classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Write exactly one bullet for every pending change. Classify each change independently, sort the bullets by code, and calculate the overall impact.

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
- Use an `##` heading with the version in square brackets.
- Put `Impact:` immediately below the heading, with no blank line between them.
- Begin every bullet with an unformatted code such as `[A2]`. Do not bold the code.
- Include exactly one bullet per pending change.
- End with the exact trailer `<!-- stl-impact: v1 -->`.
- Make the trailer the final line.
- Do not copy conflicting formatting or classifications from older entries.

## Choose the letter

Choose the first applicable category in this precedence order: A, then B, then C.

- **A — Public API or typing contract:** The change adds, removes, renames, or modifies an exported name, signature, parameter, default, return type, accepted type, public type, annotation, or other public typing contract.
- **B — Observable runtime behavior:** The public API surface is unchanged, but callers can observe a change in results, exceptions, normalization, speed, memory use, or other runtime behavior.
- **C — Project infrastructure:** The change affects only documentation, tests, CI, build or release tooling, packaging, dependencies, internal implementation, or the supported environment matrix.

Apply the precedence strictly:

- A signature or public typing change is A even if runtime behavior also changes.
- An optimization or memory-use change is B even when output is identical.
- An internal refactor is C only when callers cannot observe any difference.
- Adding public annotations or making shipped annotations discoverable is A.
- Dropping support for a language, runtime, operating system, or platform version is C.

## Choose the digit

Choose the first applicable digit in this precedence order: 1, then 2, then 3. Choose it independently of the letter.

- **1 — Breaking:** Previously supported caller code can now fail, stop installing or running, or receive a different result.
- **2 — Compatible and observable:** The change adds capability, makes a previously failing case work, or improves observable performance or resource use while preserving the behavior of previously working callers.
- **3 — Unobservable:** Supported callers cannot observe any change in API, typing, results, errors, compatibility, performance, or resource use.

Important distinctions:

- A bug fix is not automatically digit 2. If an input that previously returned a result now returns a different result, use 1.
- If an input previously failed and now succeeds, while previously working inputs are unchanged, use 2.
- Identical output does not imply digit 3 when speed or memory use changes.
- Documentation, tests, and CI-only changes normally use 3.
- A behavior-preserving internal refactor normally uses 3.

Common classifications:

- Remove or rename an exported API: `A1`
- Remove a parameter or change an existing return type: `A1`
- Add an exported function, type, or optional parameter: `A2`
- Add or expose non-narrowing public annotations: `A2`
- Change output without changing the public signature: `B1`
- Fix a formerly failing input without changing successful inputs: `B2`
- Improve runtime speed or memory use with identical results: `B2`
- Change only documentation, tests, or CI: `C3`
- Change only an internal implementation with no observable effect: `C3`
- Change only dependency or packaging internals with no caller-visible effect: `C3`
- Drop a supported runtime or platform version: `C1`

## Sort and summarize

Sort bullets by complete code in this order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the input order of changes that have the same code.

Set `Impact:` to the lowest digit used by any bullet. For example, if the entry contains digits 1, 2, and 3, write `Impact: 1`.