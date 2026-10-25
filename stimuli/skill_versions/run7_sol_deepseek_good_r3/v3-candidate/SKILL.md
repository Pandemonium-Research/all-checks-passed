---
name: impact-log
description: Use this skill when given a version number, release date, and pending project changes to produce a correctly classified, parseable release-notes entry in the team's house impact-log format.
---

# Release notes

Create exactly one entry containing every pending change. Use this exact layout:

## [version] - YYYY-MM-DD

Impact: N

- [code] Change description.
- [code] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders with the supplied values. Preserve the blank lines shown. Do not add introductory or closing text. The trailer must be the final line, with nothing after it.

## Classify every change

Give each change one two-character code: one letter followed by one digit. Determine the letter and digit independently.

### Choose the letter

- **A — Public API:** An exported name, signature, parameter, return type, accepted input type, or other public type is added, removed, renamed, or modified.
- **B — Runtime behavior:** The public API is unchanged, but an existing call can produce different behavior or results.
- **C — Non-API work:** The change affects implementation internals, performance, builds, packaging, distribution, tooling, tests, or documentation without changing the public API or an existing call's behavior.

Use these rules:

- A new exported function, class, method, or constant is **A**.
- Broadening or narrowing the inputs accepted by public API is **A**, even when its written signature is unchanged.
- Correcting an existing function's result without changing its API is **B**.
- Internal caching, optimization, or refactoring with unchanged public results is **C**.
- Packaging and distribution changes are **C**.
- Test, tooling, and documentation changes are **C**.

If multiple letters apply to one change, use the earliest letter: **A before B before C**.

### Choose the digit

- **1 — Breaking:** Previously valid, correct usage can now fail, become invalid, or intentionally produce an incompatible result.
- **2 — Compatible and observable:** The change adds a usable capability, expands compatibility, or fixes incorrect behavior while correct existing usage continues to work.
- **3 — Unobservable:** Callers receive no new capability and observe no change in behavior or compatibility.

Apply these classifications directly:

- Add public API: **A2**.
- Broaden inputs accepted by public API: **A2**.
- Remove, rename, or incompatibly change public API: **A1**.
- Narrow inputs accepted by public API: **A1**.
- Fix incorrect runtime behavior without changing the API: **B2**.
- Intentionally change previously correct runtime behavior incompatibly: **B1**.
- Optimize, cache, or refactor internals without changing results or signatures: **C3**.
- Add a usable packaging or distribution capability, such as support for another installation target: **C2**.
- Migrate packaging while preserving installation compatibility: **C3**.
- Reorganize tests or tooling without a user-visible effect: **C3**.

Do not assign digit **1** merely because a feature is new or a buggy result changed. New compatible capabilities and bug fixes use digit **2**.

If multiple digits apply to one change, use the lowest digit: **1 before 2 before 3**.

## Write the entry

1. Copy the supplied three-part version number and date exactly into the heading.
2. Write one concise bullet for every pending change. Do not omit changes or merge unrelated changes.
3. Start every bullet with its code in square brackets.
4. Sort bullets by code in this order: **A1, A2, A3, B1, B2, B3, C1, C2, C3**.
5. Preserve the supplied order among changes with the same code.
6. Set `Impact` to the lowest digit appearing in any bullet, regardless of its letter.
7. End with exactly `<!-- stl-impact: v1 -->`.