---
name: impact-log
description: Use this skill when given a version number, release date, and pending project changes to produce one complete, correctly classified, parser-compatible release-nototes entry in the team's house impact-log format.
---

# Release notes

Produce exactly one entry containing every pending change. Use this exact structure, including the blank lines:

## [version] - YYYY-MM-DD

Impact: N

- [code] Change description.
- [code] Change description.

<!-- stl-impact: v1 -->

Replace only the placeholders. Add no introduction, conclusion, extra heading, or content after the trailer.

## Classify every change

Assign each change one code consisting of a letter and a digit. Determine the letter and digit separately.

### Choose the letter

Use the first applicable category:

- **A — Public API:** The change adds, removes, renames, or modifies an exported name, public signature, parameter, return type, accepted input type, or other public type.
- **B — Runtime behavior:** The public API remains unchanged, but an existing call can produce different behavior or results.
- **C — Non-API work:** The change affects implementation internals, performance, builds, packaging, distribution, supported installation environments, tooling, tests, or documentation without changing the public API or an existing call's behavior.

Apply these rules:

- A new exported function, class, method, constant, or other public name is **A**.
- Adding an optional public parameter is **A**.
- Broadening or narrowing accepted inputs is **A**, even if the written signature does not change.
- Changing only the result or behavior of an existing call is **B**.
- Fixing an existing function's incorrect result without changing its API is **B**.
- Caching, optimization, and refactoring with unchanged public results are **C**.
- Packaging, distribution, installation-target, test, tooling, and documentation changes are **C**.

If categories overlap, use the precedence **A before B before C**.

### Choose the digit

Use the first applicable category:

- **1 — Breaking:** Previously valid, correct, supported usage can now fail, become invalid, lose support, or intentionally produce an incompatible result.
- **2 — Compatible and observable:** The change adds a usable capability, expands support or compatibility, or corrects faulty behavior while previously correct and supported usage continues to work.
- **3 — Unobservable:** Users gain no capability or compatibility and observe no change in public behavior or results.

Apply these classifications directly:

| Change | Code |
|---|---|
| Add compatible public API | **A2** |
| Add an optional public parameter | **A2** |
| Broaden inputs accepted by public API | **A2** |
| Remove or rename public API | **A1** |
| Add a required public parameter | **A1** |
| Narrow accepted inputs or incompatibly modify public API | **A1** |
| Fix incorrect runtime behavior without changing public API | **B2** |
| Add compatible behavior to an existing call without changing public API | **B2** |
| Intentionally change previously correct behavior incompatibly | **B1** |
| Drop a supported installation target or break a supported distribution workflow | **C1** |
| Add a usable installation target, platform, interpreter version, or distribution artifact | **C2** |
| Migrate packaging without changing installation compatibility | **C3** |
| Cache, optimize, or refactor internals without changing results or signatures | **C3** |
| Reorganize tests or tooling without a user-visible effect | **C3** |
| Change documentation only | **C3** |

A new compatible feature is digit **2**, not digit **1**. A bug fix is also digit **2** when it changes an incorrect result but preserves previously correct usage. A changed result is digit **1** only when previously correct behavior becomes incompatible.

If digit categories overlap, use the precedence **1 before 2 before 3**.

## Assemble the entry

1. Copy the supplied version and date exactly into `## [version] - YYYY-MM-DD`.
2. Leave one blank line after the heading.
3. Set `Impact` to the lowest digit appearing in any bullet, regardless of its letter.
4. Leave one blank line after the `Impact` line.
5. Write exactly one concise bullet for every pending change. Do not omit changes, combine unrelated changes, or invent details.
6. Begin every bullet with its code in square brackets.
7. Sort bullets in this exact order: **A1, A2, A3, B1, B2, B3, C1, C2, C3**.
8. Preserve the supplied order among changes with the same code.
9. Leave one blank line after the final bullet.
10. End with exactly `<!-- stl-impact: v1 -->`. It must be the final line.