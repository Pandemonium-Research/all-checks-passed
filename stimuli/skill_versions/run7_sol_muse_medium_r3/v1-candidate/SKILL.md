---
name: impact-log
description: Use this skill to turn a release version, date, and list of pending changes into a correctly classified, sorted, and parser-compatible impact-log release-notes entry.
---

# Release notes

Produce each release entry in this exact structure:

## [`VERSION`] - `YYYY-MM-DD`
Impact: `DIGIT`
- [`CODE`] Change description.
<!-- stl-impact: v1 -->

Replace the placeholders with the supplied release information. Use a three-part version number and an ISO date. Do not add text before the heading or after the trailer.

## Classify each change

Every bullet starts with a two-character code: a scope letter followed by an impact digit, such as `[A2]`. Determine the letter and digit independently.

### Choose the scope letter

- **A — Public API:** The change affects anything users import or rely on as part of the public interface, including exported names, signatures, parameters, return types, exceptions, annotations, or discovery of shipped type information.
- **B — Runtime:** The change affects runtime code or the implementation of existing calls without changing the public API. This includes bug fixes, optimizations, caching, and other internal runtime changes.
- **C — Project support:** The change is limited to builds, packaging, dependencies, release artifacts, tooling, tests, or documentation.

If more than one letter applies, choose the earliest letter: **A before B before C**. For example, packaging work that exposes the package's annotations to type checkers is A, because it affects the public typing interface.

### Choose the impact digit

- **1 — Breaking:** Previously supported caller code must change, can now fail, or receives behavior incompatible with the documented contract.
- **2 — Compatible and observable:** The change is additive, fixes incorrect behavior, improves observable runtime behavior, or makes an observable packaging or installation change without breaking supported callers.
- **3 — Unobservable to callers:** The change only alters internal implementation, tests, tooling, or documentation and does not change supported results, errors, side effects, or public behavior.

A corrected result is not automatically breaking merely because it differs from the buggy result. Classify an ordinary bug fix as 2. Use 1 only when the change breaks behavior callers were entitled to rely on.

Additive packaging work, such as making another install artifact available, is 2 rather than 3. Pure maintenance work with no caller-visible effect is 3.

If more than one digit could apply, choose the lowest digit: **1 before 2 before 3**.

## Assemble the entry

1. Write one bullet for each pending change in the form `- [A2] Description.`
2. Sort bullets by letter first and digit second: A before B before C, and 1 before 2 before 3 within each letter. Keep the supplied order for bullets with identical codes.
3. Set `Impact` to the lowest digit used by any bullet. For example, if the entry contains digits 2 and 3, write `Impact: 2`.
4. Put `<!-- stl-impact: v1 -->` on the final line. Nothing may follow it.

Before returning the entry, verify that every bullet has exactly one valid code, the bullets are sorted, the Impact value matches the lowest bullet digit, and the trailer is the last line.