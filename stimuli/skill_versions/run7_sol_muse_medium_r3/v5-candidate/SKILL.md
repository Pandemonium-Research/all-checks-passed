---
name: impact-log
description: Use this skill when given a release version, date, and pending changes to produce one correctly classified, sorted, parser-compatible impact-log release-notes entry.
---

# Release notes

Produce exactly one entry in this format:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Use the supplied version and date without changing them. Write the date in `YYYY-MM-DD` format. Include every pending change exactly once. Do not add commentary before or after the entry.

## Classify each change

Each bullet begins with a two-character code: one scope letter followed by one impact digit, such as `[B2]`. Determine the letter and digit independently.

### Choose the scope letter

- **A — Public API:** An exported name, signature, parameter, return type, public exception, public annotation, or documented public contract is added, removed, or changed.
- **B — Runtime:** The implementation or behavior of an existing call changes without changing its public interface. This includes bug fixes, performance changes, caching, and memory or resource-use changes.
- **C — Project support:** The change concerns builds, packaging, dependencies, distributed artifacts, installation support, tooling, tests, or documentation.

If more than one scope applies, use the earliest letter: **A before B before C**.

Important distinctions:

- A new or changed exported function, parameter, public type, or public annotation is A.
- A fix to an existing function is B when its public interface is unchanged.
- Changing only how existing annotations are packaged or discovered is C.
- Dependency handling, wheels, package metadata, and installed files are C unless the change also modifies the public API.
- Test and documentation changes are C.

### Choose the impact digit

- **1 — Breaking:** The change is incompatible with a previously supported public contract. Supported code must change, may now fail, or can no longer rely on documented behavior.
- **2 — Compatible and observable:** The change can be observed by callers, installers, or supported development tools, but it does not break a supported contract. This includes compatible additions, ordinary bug fixes, performance or resource-use changes, and observable packaging or distribution changes.
- **3 — Unobservable maintenance:** The change affects only internals, tests, tooling, or documentation and does not observably change supported behavior, runtime characteristics, installation, distributed artifacts, or public interfaces.

If more than one impact applies, use the lowest digit: **1 before 2 before 3**.

Apply these rules:

- An ordinary bug fix is 2, even though the corrected result differs from the faulty result. Use 1 only if the old behavior was part of the supported contract.
- A compatible public API addition is 2.
- A runtime optimization or cache change is 2 when timing, memory use, cache growth, or another resource characteristic changes observably.
- An internal replacement is 3 only when supported results, errors, side effects, performance, and resource use remain effectively unchanged.
- A packaging change is 2 when it changes installation support, dependencies, distributed contents, installed files, or discovery by supported tools.
- Tests, documentation, tooling, or packaging work is 3 only when it has no externally observable effect.
- Do not choose a more disruptive digit merely because the classification is uncertain. Classify the stated effect using the rules above.

## Assemble the entry

1. Write one bullet for every pending change using `- [CODE] Change description.`
2. Sort bullets by code in this order: A1, A2, A3, B1, B2, B3, C1, C2, C3.
3. Preserve the supplied order among changes with the same code.
4. Set `Impact` to the lowest digit used by any bullet.
5. Put `<!-- stl-impact: v1 -->` on the final line, with nothing after it.

Before returning the entry, verify that the version and date match the supplied values, every pending change appears exactly once, every bullet has one valid code, the bullets are sorted, `Impact` equals the lowest bullet digit, and the trailer is the final line.