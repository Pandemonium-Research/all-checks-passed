---
name: impact-log
description: Use this guide when converting a release version, date, and pending-change list into a correctly formatted, classified, and sorted release notes entry.
---

# Release notes

## Required output

Return only the release entry in this exact structure:

    ## [<version>] - <YYYY-MM-DD>
    Impact: <lowest marker digit>
    - [<letter><digit>] <change description>
    <!--stl-impact: v1-->

Use the supplied three-part version and date. Add exactly one bullet per pending change. Do not merge, split, omit, or duplicate changes. Do not add an introduction, summary, category heading, or closing text.

Keep each supplied change description intact. Classification must be based only on effects stated in that description; do not invent possible consequences.

## Classify each change

A marker consists of a letter and a digit. Select them independently: the letter identifies the affected surface, while the digit identifies compatibility and observability.

### Select the letter

Apply these rules in order and stop at the first match:

1. **A — Public interface:** The change affects an exported name, signature, parameter, accepted input type, return type, annotation, or shipped static-typing information.
2. **B — Runtime behavior:** Otherwise, importing or using the package has an observable runtime difference, such as corrected or changed results, different errors, side effects, performance, memory use, resource use, or import behavior.
3. **C — Project or implementation detail:** Otherwise, the change concerns internal implementation, caching with unchanged behavior, builds, packaging, dependencies, tooling, tests, or documentation.

Use A before B before C when a change has multiple effects.

Important distinctions:

- A new exported API is A.
- Widening the inputs accepted by an existing API is A, even when its written signature is unchanged.
- Information shipped for type checkers is A, even when runtime behavior is unchanged.
- A correctness fix that does not alter the public interface is B.
- An import-time or runtime performance change is B.
- Documentation and docstring changes are C, even when they describe exported functions.
- An internal refactor or cache replacement is C when results, signatures, and other observable behavior are stated to be unchanged.
- Packaging, dependency, or vendoring work is C when no installation or runtime difference is stated.

### Select the digit

Apply these rules in order and stop at the first match:

1. **1 — Breaking:** Previously supported, correct use can now become invalid, fail, or receive different intended behavior. Examples include removing an API, narrowing accepted inputs, adding a required argument, or intentionally changing established behavior.
2. **2 — Compatible but observable:** Otherwise, package users or their development tools can observe the change. This includes additive APIs, widened input support, shipped typing information, bug fixes, and compatible performance improvements.
3. **3 — Unobservable:** Otherwise, users and their tools cannot observe a difference. This includes documentation, tests, tooling, behavior-preserving refactoring, internal cache changes with unchanged behavior, and behavior-preserving packaging or dependency work.

Use 1 before 2 before 3 when multiple digits appear applicable.

Do not mark a bug fix as breaking merely because its incorrect result changes. Incorrect behavior is not treated as supported behavior; a compatible bug fix is digit 2.

Do not use digit 2 merely because a change is non-breaking. If the description states that observable behavior is unchanged, use digit 3.

## Sort the bullets

Sort bullets by their complete markers in exactly this order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

When multiple changes have the same marker, preserve their order from the supplied pending-change list.

## Calculate `Impact`

Set `Impact` to the numerically lowest digit appearing in a bullet marker.

Consider only marker digits. Ignore all other digits, including those in the version, date, descriptions, and trailer.

## Add the trailer

Place this exact line immediately after the final bullet:

`<!--stl-impact: v1-->`

## Final verification

Before returning the entry, confirm that:

- The version and date exactly match the supplied values.
- Every pending change appears exactly once.
- Every bullet begins with `- [`, followed by A, B, or C and then 1, 2, or 3.
- Each letter and digit was classified independently from the stated effects.
- Bullets follow the required marker order.
- `Impact` equals the lowest bullet-marker digit.
- The trailer is the final line and is exactly `<!--stl-impact: v1-->`.