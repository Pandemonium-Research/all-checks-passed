---
name: impact-log
description: Use this skill when given a release version, date, and pending changes to produce one parser-compatible release-notes entry in the project's impact-log format.
---

# Release notes

Output exactly one release entry and no surrounding commentary:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Use the supplied three-part version and date. Format the date as `YYYY-MM-DD`. Include every pending change exactly once.

## Classify each change

Each bullet starts with one code containing a scope letter and an impact digit, such as `[B2]`. Choose the letter and digit independently.

### Scope letter

- **A — Public API:** The change adds, removes, or modifies an exported name, signature, parameter, return type, exception, or type annotation.
- **B — Runtime:** The behavior or implementation of an existing call changes without changing its public API. This includes bug fixes, performance work, caching, and memory-use changes.
- **C — Project support:** The change affects builds, packaging, dependencies, installation artifacts, tooling, tests, or documentation.

If more than one scope applies, choose the earliest letter: **A before B before C**.

Apply these distinctions:

- A compatible new exported function is A.
- A bug fix in an existing function is B when its public interface is unchanged.
- Changing actual exported annotations is A.
- Changing only how existing annotations are packaged or discovered, such as adding a typing marker, is C.
- Vendoring or changing a dependency is C.
- Publishing a new wheel or changing another distributed artifact is C.
- Moving tests or editing documentation is C.

### Impact digit

- **1 — Breaking:** The change violates a previously supported public contract. Supported callers must change their code, may now fail, or lose documented behavior on which they were entitled to rely.
- **2 — Compatible and observable:** The change is externally observable but does not break a supported contract. This includes compatible additions, ordinary bug fixes, performance or memory-use changes, cache-behavior changes, and installation or distribution changes.
- **3 — Unobservable maintenance:** The change affects only implementation, tests, tooling, or documentation, with no observable change to supported results, errors, side effects, runtime characteristics, installation, or distributed artifacts.

If more than one impact applies, choose the lowest digit: **1 before 2 before 3**.

Apply these distinctions:

- An ordinary bug fix is 2, not 1. Correcting faulty or undocumented behavior is breaking only when the old behavior was part of the supported contract.
- A compatible new public API is 2.
- A runtime optimization is 2 when callers can observe faster execution, lower memory use, bounded cache growth, or another changed runtime characteristic.
- An internal implementation replacement is 3 only when behavior, performance, memory use, and other observable runtime characteristics remain effectively unchanged.
- A new wheel, changed dependency arrangement, typing marker, or other observable installation or packaging change is 2.
- Test reorganization and documentation-only changes are 3.

Classify from the stated effect of the change. Do not increase the impact digit merely because the classification is uncertain.

## Assemble the entry

1. Write one bullet for each pending change in the form `- [A2] Description.`
2. Sort the bullets by scope letter and then impact digit: A1, A2, A3, B1, B2, B3, C1, C2, C3.
3. Preserve the supplied order among changes assigned the same code.
4. Set `Impact` to the lowest digit used by any bullet.
5. Put `<!-- stl-impact: v1 -->` on the final line, with nothing after it.

Before returning the entry, verify that:

- The heading contains the supplied version and date.
- Every pending change appears exactly once.
- Every bullet has exactly one valid code.
- Scope and impact were chosen independently.
- The bullets are sorted by code.
- `Impact` equals the lowest bullet digit.
- The trailer is present and is the final line.