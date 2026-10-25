---
name: impact-log
description: Use this guide to turn a release version, date, and pending-change list into a correctly formatted, classified, sorted release notes entry.
---

# Release notes

## Required output

Return only the release entry in this format:

    ## [<version>] - <YYYY-MM-DD>
    Impact: <lowest bullet-marker digit>
    - [<letter><digit>] <change description>
    <!--stl-impact: v1-->

Use the supplied version and date exactly. Create exactly one bullet for every pending change. Do not merge, split, omit, or duplicate changes. Keep each supplied change description intact.

Do not add introductory text, summaries, category headings, explanations, or closing text.

## Classify every change

Each bullet marker contains a letter and a digit. Choose them independently from the effects explicitly stated in the change description. Do not assume effects that are not stated.

### Choose the letter

Apply these rules in order and stop at the first match:

1. **A — Public interface:** Use A when the change affects an exported name, signature, parameter, accepted input type, return type, annotation, or shipped static-typing information.
2. **B — Runtime behavior:** Otherwise, use B when importing or using the package has an observable runtime difference. This includes corrected or changed results, different errors, side effects, performance, memory or resource use, and import behavior.
3. **C — Project or implementation detail:** Otherwise, use C. This includes behavior-preserving implementation work, builds, packaging, dependencies, tooling, tests, and documentation.

When more than one letter applies, use the alphabetically earliest: A before B before C.

Apply these distinctions exactly:

- Adding an exported API is A.
- Widening the accepted inputs of an exported API is A, even if its written signature is unchanged.
- Shipping information used by type checkers is A, even if runtime behavior is unchanged.
- Fixing runtime behavior without changing the public interface is B.
- Improving import time or execution performance is B.
- Documentation and docstring changes are C, including documentation for exported APIs.
- An internal refactor or cache change is C when the description states that signatures, results, and observable behavior are unchanged.
- Packaging, dependency, or vendoring work is C when no installation, public-interface, or runtime difference is stated.

### Choose the digit

Apply these rules in order and stop at the first match:

1. **1 — Breaking:** Use 1 when previously supported, correct caller code can become invalid, fail, or receive different intended behavior. Examples include removing an API, narrowing accepted inputs, adding a required argument, or intentionally changing established behavior.
2. **2 — Compatible and observable:** Otherwise, use 2 when package users or their development tools can observe the change. This includes additive APIs, widened input support, shipped typing information, compatible bug fixes, and compatible performance improvements.
3. **3 — Unobservable:** Otherwise, use 3. This includes documentation, tests, tooling, behavior-preserving refactoring, internal cache changes with unchanged behavior, and behavior-preserving packaging or dependency work.

When more than one digit applies, use the lowest: 1 before 2 before 3.

A bug fix is normally digit 2. Do not use digit 1 merely because the incorrect result changes; incorrect behavior is not treated as supported behavior.

Compatibility alone does not make a change digit 2. If neither users nor their development tools can observe a difference, use digit 3.

## Sort the bullets

Sort bullets by their complete markers in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Preserve the supplied order among changes that receive the same marker.

## Calculate `Impact`

Set `Impact` to the numerically lowest digit used in any bullet marker.

Consider only the digits inside bullet markers. Ignore digits in the version, date, descriptions, and trailer.

## Add the trailer

Place this exact line immediately after the final bullet:

`<!--stl-impact: v1-->`

The trailer must be the final line.

## Final verification

Before returning the entry, verify that:

- The version and date exactly match the supplied values.
- Every pending change appears exactly once and remains intact.
- Every bullet starts with a valid marker containing A, B, or C followed by 1, 2, or 3.
- Each marker’s letter and digit were selected independently.
- Bullets follow the required marker order.
- `Impact` equals the lowest bullet-marker digit.
- The trailer is exact and is the final line.