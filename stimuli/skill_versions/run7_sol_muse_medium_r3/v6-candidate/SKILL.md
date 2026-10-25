---
name: impact-log
description: Use this skill when given a release version, date, and pending changes to write one correctly classified and parser-compatible release-notes entry.
---

# Release notes

Return exactly one release entry with no code fence or surrounding commentary:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Use the supplied version and date. Include every pending change exactly once.

## Classify each change

Each bullet begins with one code containing a scope letter and an impact digit, such as `[B2]`. Choose the letter and digit independently.

### Scope letter

- **A — Public API:** An exported name, signature, parameter, return type, or exported type annotation is added, removed, or changed.
- **B — Runtime:** The behavior or implementation of an existing call changes without changing its public API. This includes bug fixes, performance changes, caching, and memory or resource-use changes.
- **C — Project support:** The change affects builds, packaging, dependencies, installation artifacts, tooling, tests, or documentation.

When multiple scopes apply, use the earliest letter: **A before B before C**.

Use these distinctions:

- A compatible new exported API is A.
- A bug fix in an existing function is B if its public interface is unchanged.
- Changing exported annotations is A.
- Changing how existing annotations are packaged or discovered is C.
- Dependency, wheel, package-metadata, and installed-file changes are C.
- Test, tooling, and documentation changes are C.

### Impact digit

- **1 — Breaking:** The change violates a previously supported public contract. Supported users must change their code, may now fail, or lose behavior they were documented to rely on.
- **2 — Compatible and observable:** Users, installers, or supported development tools can observe the change, but it does not break a supported contract.
- **3 — Unobservable maintenance:** The change affects only internals, tests, tooling, or documentation, with no observable effect on supported behavior, performance, resource use, installation, distributed artifacts, or public interfaces.

When multiple impacts apply, use the lowest digit: **1 before 2 before 3**.

Apply these rules:

- An ordinary bug fix is 2, not 1. Use 1 only when the corrected behavior breaks a previously supported contract.
- A compatible public API addition is 2.
- A performance improvement is 2 because execution time is observable.
- A cache or memory-management change is 2 when it changes memory use, cache growth, eviction, or another runtime characteristic, even if returned values are unchanged.
- An internal replacement is 3 only when behavior, errors, side effects, performance, and resource use remain effectively unchanged.
- A dependency arrangement, typing marker, wheel, installed file, or other observable packaging change is 2.
- Tests, documentation, and internal tooling changes are 3 when they have no externally observable effect.
- Classify only the stated effect. Uncertainty is not a reason to choose a more disruptive digit.

## Assemble the entry

1. Write one bullet for each pending change as `- [CODE] Change description.`
2. Sort bullets in this exact order: A1, A2, A3, B1, B2, B3, C1, C2, C3.
3. Preserve the supplied order among changes assigned the same code.
4. Set `Impact` to the lowest digit used by any bullet.
5. Put `<!-- stl-impact: v1 -->` on the final line, with nothing after it.

Before returning the entry, verify that the supplied version and date are unchanged, every pending change appears exactly once, every bullet has one valid code, the bullets are sorted, `Impact` equals the lowest bullet digit, and the trailer is the final line.