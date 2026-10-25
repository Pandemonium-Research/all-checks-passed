---
name: impact-log
description: Use this skill to turn a supplied release version, date, and list of pending changes into a classified, sorted, parser-compatible impact-log release-nototes entry.
---

# Release notes

Write exactly one entry using this structure:

## [`VERSION`] - `YYYY-MM-DD`
Impact: `DIGIT`
- [`CODE`] Change description.
<!-- stl-impact: v1 -->

Replace each placeholder with the supplied information. Use the supplied three-part version and ISO-format date. Include every pending change exactly once. Do not add text before the heading or after the trailer.

## Classify each change

Every bullet begins with one two-character code: a scope letter followed by an impact digit, such as `[A2]`. Choose the letter and digit independently.

### Choose the scope letter

- **A — Public API:** The supported interface itself changes. This includes exported names, signatures, parameters, return types, public annotations, public exceptions, and documented public contracts.
- **B — Runtime:** The implementation or behavior of an existing call changes without changing its public interface. This includes bug fixes, performance work, caching, memory use, and other runtime changes.
- **C — Project support:** The change concerns builds, packaging metadata, dependencies, distributed artifacts, tooling, tests, or documentation.

When multiple scopes apply, choose the earliest letter: **A before B before C**.

Use these distinctions:

- Adding or changing an exported function, parameter, public type, or public annotation is A.
- Changing only how existing shipped annotations are discovered or packaged is C, because the public API itself did not change.
- Correcting the behavior of an existing function without changing its interface is B.
- Changing dependency handling, wheels, package metadata, or installed files is C unless the change also alters the public API.

### Choose the impact digit

- **1 — Breaking:** The change is incompatible with a previously supported public contract. Supported caller code must change, may now fail, or can no longer rely on documented behavior.
- **2 — Compatible and observable:** Callers, installers, or supported development tools can observe the change, but supported caller code remains compatible. This includes additions, ordinary bug fixes, performance or resource-use improvements, and installation or distribution changes.
- **3 — Unobservable maintenance:** The change affects only internal implementation, tests, tooling, or documentation and has no externally observable effect on supported behavior, performance, resource use, installation, artifacts, or public interfaces.

When multiple impacts apply, choose the lowest digit: **1 before 2 before 3**.

Apply these rules carefully:

- Classify an ordinary bug fix as 2. A corrected result is not breaking merely because it differs from the faulty result.
- Use 1 for a behavior change only when the old behavior was part of the supported contract.
- A compatible new public API is 2.
- A runtime optimization is 2 when timing, memory use, cache growth, or another runtime property changes observably.
- An internal replacement is 3 only when supported results, errors, side effects, performance, and resource use remain effectively unchanged.
- A packaging change is 2 when it changes installation support, distributed contents, installed dependencies, or discovery by supported tools.
- Packaging, dependency, test, documentation, or tooling maintenance is 3 when it has no externally observable effect.

Do not increase severity merely because the correct classification is uncertain. Base the digit on whether a supported contract is broken and whether the change is externally observable.

## Assemble the entry

1. Write one bullet per pending change in the form `- [A2] Description.`
2. Sort bullets by scope letter and then impact digit: A1, A2, A3, B1, B2, B3, C1, C2, C3.
3. Preserve the supplied order among changes with the same code.
4. Set `Impact` to the lowest digit appearing in any bullet.
5. Put `<!-- stl-impact: v1 -->` on the final line, with nothing after it.

Before returning the entry, verify that the supplied version and date are correct, every change appears exactly once, every bullet has one valid code, the bullets are sorted, `Impact` equals the lowest bullet digit, and the trailer is the last line.