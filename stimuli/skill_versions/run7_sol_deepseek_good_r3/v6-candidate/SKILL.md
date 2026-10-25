---
name: impact-log
description: Use this skill when given a version number, release date, and pending project changes to produce one complete, correctly classified, parser-compatible release-nototes entry in the team's house impact-log format.
---

# Release notes

Produce exactly one entry containing every pending change. Use this exact structure, including all blank lines:

## [version] - YYYY-MM-DD

Impact: N

- [code] Change description.
- [code] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders with the supplied version, date, impact digit, codes, and descriptions. Add no introduction, conclusion, extra heading, or content after the trailer.

## Classify every change

Assign each change a two-character code consisting of one letter followed by one digit. Choose the letter and digit independently.

### Choose the letter

Use the first applicable category:

- **A — Public API:** The change adds, removes, renames, or modifies an exported name, public signature, parameter, return type, accepted input type, or other public type.
- **B — Runtime behavior:** The public API remains unchanged, but an existing call can produce different behavior or results.
- **C — Non-API work:** The change affects implementation internals, performance, builds, packaging, distribution, supported installation environments, tooling, tests, or documentation without changing the public API or an existing call's behavior.

Apply these rules:

- Adding an exported function, class, method, constant, or other public name is **A**.
- Adding an optional or required public parameter is **A**.
- Broadening or narrowing accepted inputs is **A**, even if the written signature is unchanged.
- Removing, renaming, or incompatibly modifying public API is **A**.
- Changing or fixing only the behavior or result of an existing call is **B**.
- Caching, optimizing, or refactoring with unchanged public results and signatures is **C**.
- Packaging, distribution, installation-target, test, tooling, and documentation changes are **C**.

If more than one letter appears applicable, use the precedence **A before B before C**.

### Choose the digit

Use the first applicable category:

- **1 — Breaking:** Previously valid, correct, supported usage can now fail, become invalid, lose support, or intentionally produce an incompatible result.
- **2 — Compatible and observable:** The change adds a usable capability, expands support or compatibility, or corrects faulty behavior while previously correct and supported usage continues to work.
- **3 — Unobservable:** The change adds no user capability or compatibility and changes no public behavior or result.

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
| Intentionally make previously correct behavior incompatible | **B1** |
| Drop a supported installation target or break a supported distribution workflow | **C1** |
| Add a usable installation target, platform, interpreter version, or distribution artifact | **C2** |
| Migrate packaging without changing installation compatibility | **C3** |
| Cache, optimize, or refactor internals without changing results or signatures | **C3** |
| Reorganize tests or tooling without a user-visible effect | **C3** |
| Change documentation only | **C3** |

A new compatible feature is digit **2**, not digit **1**. A broadened accepted-input type is also digit **2**. A bug fix is digit **2** when it corrects faulty output while preserving previously correct usage. Use digit **1** only when previously correct and supported usage becomes incompatible.

If more than one digit appears applicable, use the precedence **1 before 2 before 3**.

## Assemble the entry

1. Copy the supplied version and date exactly into `## [version] - YYYY-MM-DD`.
2. Leave exactly one blank line after the heading.
3. Write `Impact: N`, replacing `N` with the lowest digit used by any bullet, regardless of letter.
4. Leave exactly one blank line after the `Impact` line.
5. Write exactly one concise bullet for every pending change.
6. Do not omit a change, combine unrelated changes, split one change into multiple bullets, or invent details.
7. Begin every bullet with its code in square brackets.
8. Sort bullets in this exact order: **A1, A2, A3, B1, B2, B3, C1, C2, C3**.
9. Preserve the supplied order among changes assigned the same code.
10. Leave exactly one blank line after the final bullet.
11. End with exactly `<!-- stl-impact: v1 -->`. The trailer must be the final line.