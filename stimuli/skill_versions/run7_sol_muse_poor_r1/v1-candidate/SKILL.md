---
name: impact-log
description: Use this guide when converting a release version, date, and list of pending changes into a correctly formatted release notes entry with impact markers.
---

# Release notes

## Required format

Write the entry in exactly this structure:

## [<version>] - <YYYY-MM-DD>
Impact: <lowest marker digit>
- [<letter><digit>] <change description>
<!--stl-impact: v1-->

Use a three-part version number. Write the date as year-month-day.

Create exactly one bullet for each pending change. Do not combine changes or split one change across multiple bullets.

## Classify each change

Choose the letter and digit independently.

### Choose the letter

Use the first applicable category:

- **A — Public interface:** The change affects exported names, signatures, parameters, accepted input types, return types, annotations, or shipped type-checking metadata such as `py.typed`.
- **B — Runtime behavior:** The public interface is unchanged, but an existing use can observe different runtime behavior. This includes changes to results, errors, correctness, side effects, performance, resource use, or import behavior.
- **C — Project internals:** The change affects only implementation details, builds, packaging, dependencies, tooling, tests, or documentation, with no change to the public interface or runtime behavior.

If more than one letter applies, use the alphabetically earliest letter: A before B before C.

Examples of the distinction:

- Adding an exported function is A.
- Expanding the accepted type of an argument is A.
- Fixing runtime behavior without changing the signature is B.
- Improving import or execution performance is B.
- Replacing an internal cache while preserving results and behavior is C.
- Changing tests or documentation only is C.

### Choose the digit

- **1 — Breaking:** Previously supported, correct caller code can now fail, become invalid, or produce a different correct result. Examples include removing an API, narrowing accepted inputs, or adding a required argument.
- **2 — Compatible and observable:** The change is visible to callers but does not break correct existing code. This includes additive APIs, widened input support, newly shipped type information, bug fixes, and compatible performance improvements.
- **3 — Unobservable to callers:** Callers see no difference in the public interface or runtime behavior. This includes documentation, tests, internal refactoring, and internal caching changes whose signatures and results remain unchanged.

A bug fix is normally digit 2 when it corrects previously incorrect behavior while leaving correct existing code unaffected. Do not mark it as breaking merely because the buggy result changes.

If a change has effects at multiple digit levels, use the lowest digit: 1 before 2 before 3.

## Calculate the summary

Set `Impact` to the lowest digit used in the change markers.

Consider only the digit portion of each bullet's marker. Ignore digits in the version, date, descriptions, and trailer.

## Order the bullets

Sort bullets by their complete markers in this order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Keep the supplied order for changes with identical markers.

## Add the trailer

Place this exact HTML comment after the final bullet:

<!--stl-impact: v1-->