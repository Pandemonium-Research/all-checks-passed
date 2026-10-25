---
name: impact-log
description: Use this guide to turn a release version, date, and list of pending changes into a correctly formatted release notes entry with impact markers.
---

# Release notes

## Output format

Write only the release entry, using this exact structure:

## [<version>] - <YYYY-MM-DD>
Impact: <lowest bullet-marker digit>
- [<letter><digit>] <change description>
<!--stl-impact: v1-->

Requirements:

- Use the supplied three-part version number.
- Use the supplied date in `YYYY-MM-DD` format.
- Create exactly one bullet for each pending change.
- Do not merge changes or split one change into multiple bullets.
- Begin every bullet with `- ` followed by its bracketed marker.
- Place the trailer immediately after the final bullet.
- Do not add introductions, category headings, summaries, or other text.

## Assign each marker

Every marker contains one letter and one digit. Choose them independently from the actual effect of the change.

### Choose the letter

Apply these tests in order and use the first match:

1. **A — Public interface:** Use A if the change affects an exported name, signature, parameter, accepted input type, return type, annotation, or shipped static-typing information.
2. **B — Runtime behavior:** Otherwise, use B if importing or using the package can produce an observable runtime difference. This includes correctness fixes, changed results or errors, side effects, performance, memory or resource use, and import behavior.
3. **C — Project or implementation detail:** Otherwise, use C. This includes internal refactoring, internal caches with unchanged observable behavior, builds, packaging, dependencies, tooling, tests, and documentation.

Important distinctions:

- Adding an exported API or widening an accepted input type is A, not B.
- Adding or changing information consumed by type checkers is A.
- Correcting behavior without changing the public interface is B.
- A stated import-time or runtime performance improvement is B.
- An internal implementation change is C when no caller-visible effect is stated.
- Packaging or dependency work is C when installation and runtime behavior remain unchanged.

When several letters appear applicable, precedence is A before B before C.

### Choose the digit

Apply these tests in order:

1. **1 — Breaking:** Use 1 if previously supported, correct use can become invalid, fail, or produce a different intended result. Removing an API, narrowing accepted inputs, or adding a required argument is breaking.
2. **2 — Compatible but observable:** Otherwise, use 2 if package users or their tools can observe the change. Additive APIs, widened input support, new type-checking information, bug fixes, and compatible performance improvements are digit 2.
3. **3 — Unobservable:** Otherwise, use 3. Documentation, tests, tooling, internal refactoring, and behavior-preserving packaging or implementation changes are digit 3.

Do not classify a bug fix as breaking merely because the erroneous result changes. Previously incorrect behavior does not count as a supported result. A bug fix is normally digit 2 when correct existing uses remain valid.

When a change has several effects, use the lowest applicable digit: 1 before 2 before 3.

## Sort the bullets

Sort all bullets by their complete markers in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

For bullets with the same marker, preserve their order from the supplied change list.

## Calculate `Impact`

Set `Impact` to the lowest digit appearing in any bullet marker.

Use only marker digits for this calculation. Ignore every other digit, including digits in the version, date, descriptions, and trailer.

For example, if the markers contain digits 2 and 3, write `Impact: 2`.

## Final check

Before returning the entry, verify that:

- The version and date match the supplied values.
- Every pending change appears exactly once.
- Each marker contains only A, B, or C followed by 1, 2, or 3.
- Letters and digits were classified separately.
- Bullets follow the required marker order.
- `Impact` equals the lowest bullet-marker digit.
- The final line is exactly `<!--stl-impact: v1-->`.