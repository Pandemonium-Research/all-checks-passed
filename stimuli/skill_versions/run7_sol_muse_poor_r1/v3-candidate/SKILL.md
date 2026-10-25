---
name: impact-log
description: Use this guide to convert a release version, date, and list of pending changes into a correctly formatted release notes entry with impact markers.
---

# Release notes

## Required format

Write only the release entry in this structure:

## [<version>] - <YYYY-MM-DD>
Impact: <lowest marker digit>
- [<letter><digit>] <change description>
<!--stl-impact: v1-->

Use the supplied three-part version number and date. Create exactly one bullet for each pending change; do not merge or split changes. Do not add introductions, category headings, summaries, or other text.

## Classify each change

Choose the marker’s letter and digit independently. Classify the change by its stated effects, not merely by whether its implementation concerns code, packaging, or documentation.

### Choose the letter

Apply these tests in order and use the first match:

1. **A — Public interface:** Use A if the change affects an exported name, signature, parameter, accepted input type, return type, annotation, or shipped static-typing metadata.
2. **B — Runtime behavior:** Otherwise, use B if package users can observe a runtime difference. This includes changed results or errors, correctness fixes, side effects, performance, resource use, and import behavior.
3. **C — Project internals:** Otherwise, use C. This includes behavior-preserving implementation changes, builds, packaging, dependencies, tooling, tests, and documentation.

Important distinctions:

- Adding an exported API or widening an accepted input type is A.
- Adding information used by type checkers is A, even if runtime behavior is unchanged.
- Fixing behavior without changing the public interface is B.
- Improving import time or execution performance is B.
- Replacing an internal cache is C when signatures, results, and other observable behavior remain unchanged.
- Packaging or dependency work is C when installation, the public interface, and runtime behavior remain unchanged.

If multiple letters apply, use the alphabetically earliest: A before B before C.

### Choose the digit

Apply these tests in order:

1. **1 — Breaking:** Use 1 if previously supported, correct caller code can now become invalid, fail, or receive different intended behavior. Examples include removing an API, narrowing accepted inputs, or adding a required argument.
2. **2 — Compatible and observable:** Otherwise, use 2 if users or their development tools can observe the change. This includes additive APIs, widened input support, newly shipped type information, bug fixes, and compatible performance improvements.
3. **3 — Unobservable:** Otherwise, use 3. This includes documentation, tests, tooling, internal refactoring, behavior-preserving caching, and behavior-preserving packaging or dependency changes.

A bug fix is normally digit 2. Do not use digit 1 merely because the erroneous result changes; incorrect behavior is not treated as supported behavior.

Do not use digit 2 merely because a change is compatible. If users and their tools cannot observe any difference, use digit 3.

If multiple digits apply, use the lowest: 1 before 2 before 3.

## Sort the bullets

Sort bullets by their complete markers in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Preserve the supplied order among changes with identical markers.

## Calculate `Impact`

Set `Impact` to the lowest digit used in any bullet marker.

Consider only the digits inside bullet markers. Ignore digits in the version, date, change descriptions, and trailer.

## Add the trailer

Place this exact line immediately after the final bullet:

<!--stl-impact: v1-->