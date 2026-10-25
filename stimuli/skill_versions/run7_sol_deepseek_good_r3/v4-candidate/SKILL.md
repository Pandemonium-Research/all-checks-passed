---
name: impact-log
description: Use this skill when given a version number, release date, and pending project changes to produce one complete, correctly classified, parseable release-notes entry in the team's house impact-log format.
---

# Release notes

Produce exactly one entry containing every pending change, using this layout:

## [version] - YYYY-MM-DD

Impact: N

- [code] Change description.
- [code] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders with the supplied version, date, impact digit, codes, and descriptions. Preserve every blank line shown. Add no introductory text, closing text, extra headings, or content after the trailer.

## Classify each change

Assign each change a two-character code: one letter followed by one digit. Determine the letter and digit independently.

### 1. Choose the letter

Choose the first applicable category:

- **A — Public API:** An exported name, public signature, parameter, return type, accepted input type, or other public type is added, removed, renamed, or modified.
- **B — Runtime behavior:** The public API is unchanged, but an existing call can produce different behavior or results.
- **C — Non-API work:** The change concerns internals, performance, builds, packaging, distribution, supported installation environments, tooling, tests, or documentation without changing the public API or an existing call's behavior.

When categories overlap, use the precedence **A before B before C**. For example, a change that modifies both a public parameter and runtime behavior is A.

Apply these rules:

- Add an exported function, class, method, constant, or other public name: **A**.
- Add an optional public parameter: **A**.
- Remove or rename public API: **A**.
- Broaden or narrow the inputs accepted by public API: **A**, even if the written signature is unchanged.
- Change only the result or behavior of an existing call: **B**.
- Refactor, cache, or optimize internals without changing public results: **C**.
- Change packaging, distribution, supported installation environments, tests, tooling, or documentation: **C**.

### 2. Choose the digit

Choose the first applicable category:

- **1 — Breaking:** Previously valid, correct, supported usage can now fail, become invalid, lose support, or intentionally produce an incompatible result.
- **2 — Compatible and observable:** The change adds a capability, expands support or compatibility, or corrects faulty behavior while previously correct and supported usage continues to work.
- **3 — Unobservable:** Users gain no capability or compatibility and observe no changed public behavior or results.

When categories overlap, use the precedence **1 before 2 before 3**.

Apply these classifications directly:

- Add compatible public API or an optional parameter: **A2**.
- Broaden the accepted inputs of public API: **A2**.
- Remove, rename, or incompatibly modify public API: **A1**.
- Add a required parameter or narrow accepted inputs: **A1**.
- Fix incorrect runtime behavior without changing public API: **B2**.
- Add compatible behavior to an existing call without changing public API: **B2**.
- Intentionally change previously correct runtime behavior incompatibly: **B1**.
- Drop an existing supported installation target or otherwise break a supported packaging or distribution workflow: **C1**.
- Add a usable installation target, platform, interpreter version, or distribution artifact: **C2**.
- Migrate packaging while preserving installation compatibility: **C3**.
- Optimize, cache, or refactor internals without changing results or signatures: **C3**.
- Reorganize tests or tooling without a user-visible effect: **C3**.
- Make documentation-only changes: **C3**.

A new feature is not breaking merely because it is new. A bug fix is not breaking merely because its output differs from the buggy output. Both use digit **2** when previously correct usage remains compatible.

## Assemble the entry

1. Copy the supplied version and date exactly into the heading.
2. Write one concise bullet for every pending change.
3. Do not omit a change, combine unrelated changes, or invent details.
4. Begin every bullet with its code in square brackets.
5. Sort bullets in this exact order: **A1, A2, A3, B1, B2, B3, C1, C2, C3**.
6. Preserve the supplied order among changes assigned the same code.
7. Set `Impact` to the lowest digit used by any bullet, regardless of letter.
8. End with exactly `<!-- stl-impact: v1 -->` as the final line.