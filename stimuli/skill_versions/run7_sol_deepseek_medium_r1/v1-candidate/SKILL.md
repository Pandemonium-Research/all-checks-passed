---
name: impact-log
description: Use when converting a release version, date, and pending changes into a correctly classified, ordered, parser-compatible release-notes entry for this project.
---

# Release notes

Create exactly one bullet for every pending change. Classify each bullet independently, sort the bullets, calculate the release impact, and then apply the exact format shown below.

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT

- [CODE] Change description.
- [CODE] Change description.

<!-- stl-impact: v1 -->
```

Follow these formatting rules exactly:

- Use the supplied three-part version and date.
- Put `Impact:` on the line immediately after the heading, with no blank line between them.
- Start every bullet with an unformatted code such as `[A2]`. Do not make the code bold.
- End the entry with `<!-- stl-impact: v1 -->`.
- The trailer must be the entry's final line. Do not put anything after it.
- Do not copy older entries when they conflict with these rules.

## Choose the letter

Choose the earliest applicable letter: A takes precedence over B, and B takes precedence over C.

- **A — Public API:** The change adds, removes, renames, or modifies an exported name, signature, parameter, default, return type, accepted type, public type, or public typing contract.
- **B — Runtime behavior:** The public API surface is unchanged, but using it can produce different results, exceptions, normalization, performance, memory use, or other runtime behavior.
- **C — Project infrastructure:** The change affects only documentation, tests, CI, build tooling, packaging, dependencies, release infrastructure, or the supported environment matrix.

Examples of applying precedence:

- A signature change that also changes runtime behavior uses A.
- A runtime optimization with unchanged output uses B because performance is observable.
- A purely internal refactor with no observable runtime effect uses C.
- Dropping support for a language or platform version uses C because it changes the supported environment rather than an exported API.

## Choose the digit

Choose the lowest applicable digit: 1 takes precedence over 2, and 2 takes precedence over 3. Decide the digit independently of the letter.

- **1 — Breaking:** Any previously supported caller code can now fail, stop installing or running, or receive a different result. Use 1 even when the change is an intentional correction.
- **2 — Compatible:** The change is additive or fixes a case that previously failed, while previously correct caller code continues to work with the same result. Observable performance or resource-use improvements also use 2.
- **3 — Unobservable to callers:** No supported caller can observe a change in API, results, errors, compatibility, performance, or resource use. Documentation, tests, CI changes, and behavior-preserving internal refactors normally use 3.

Common classifications include:

- Removing an exported API or parameter: A1.
- Changing an existing function's return type: A1.
- Adding an exported function or optional parameter: A2.
- Adding public annotations without narrowing the existing contract: A2.
- Changing output without changing the signature: B1.
- Fixing a formerly failing input without affecting working inputs: B2.
- Improving runtime performance with identical output: B2.
- Changing only documentation or CI: C3.
- Dropping a supported runtime or platform: C1.

## Sort and summarize

Sort bullets by their complete code in ascending order, using the letter first and the digit second:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Keep the input order for bullets with the same code.

Set `Impact:` to the lowest digit used by any bullet. For example, an entry containing digits 1, 2, and 3 has `Impact: 1`.