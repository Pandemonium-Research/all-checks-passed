---
name: impact-log
description: Use this guide to turn a release version, date, and list of pending changes into a correctly classified, sorted, parser-compatible release-notes entry in the project’s impact-log format.
---

# Release notes

Create one entry using this exact structure:

## [`VERSION`] - `YYYY-MM-DD`
Impact: `DIGIT`
- [`CODE`] `Change description.`
<!-- stl-impact: v1 -->

Replace the placeholders with the supplied release information. Use a three-part version number, such as `1.4.0`, and an ISO date.

## Classify each change

Give every change exactly one impact code. The letter identifies what is affected:

- **A — Public API:** Exported names, signatures, accepted argument types, return types, or shipped type information visible to type checkers.
- **B — Runtime behavior:** The observable result, error behavior, or side effect of an existing call changes without changing its public API.
- **C — Internal or project-only:** Implementation, performance, caching, dependencies, packaging, build tooling, tests, or documentation changes that do not alter the public API or defined runtime behavior.

Do not classify an implementation change as B merely because it affects timing or resource use. If results, errors, side effects, and public API remain unchanged, use C. Packaging and dependency changes are also C when installation and supported usage remain unchanged.

The digit identifies compatibility:

- **1 — Breaking:** Supported caller code may stop working, or behavior that callers are entitled to rely on becomes incompatible.
- **2 — Compatible and observable:** The change adds supported capability or corrects behavior while preserving valid existing usage. Bug fixes are digit 2 unless they intentionally break supported behavior.
- **3 — Unobservable to callers:** The change has no effect on supported caller-visible API or behavior.

Examples of applying these rules:

- A new exported function or newly accepted argument type is A2.
- A compatible bug fix to an existing call is B2, even though the corrected result differs from the buggy result.
- A removed export or incompatible signature change is A1.
- An internal cache, deferred import, or performance optimization with unchanged results and API is C3.
- Documentation-only, test-only, or installation-neutral packaging work is C3.
- Making shipped public annotations newly available to type checkers is A2.

If a change spans multiple categories, use the highest-precedence applicable letter and digit:

- Letters: A before B before C.
- Digits: 1 before 2 before 3.

## Write and order the entry

Write each bullet as a concise past-tense description of the change and any important compatibility consequence.

Sort bullets by their complete codes in ascending precedence order: A1, A2, A3, B1, B2, B3, C1, C2, C3. Preserve a sensible order among bullets with the same code.

Set the `Impact:` value to the lowest digit used by any bullet. For example, an entry containing digits 2 and 3 has `Impact: 2`. Determine this value from the final codes; do not infer it from the version number.

Place `<!-- stl-impact: v1 -->` after the final bullet. It must be the final line, with no content after it.