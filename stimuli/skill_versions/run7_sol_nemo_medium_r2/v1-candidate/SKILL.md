---
name: impact-log
description: Use this guide to turn a release version, date, and list of pending changes into a correctly classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Create exactly one entry using this structure:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Follow these steps.

1. Write the heading as `## [VERSION] - YYYY-MM-DD`.

   - Include the literal `##`.
   - Put the three-part version number in square brackets.
   - Use the supplied date in year-month-day format.

2. Write one bullet for every pending change.

   - Use exactly `- [CODE] Description.`
   - Do not replace the brackets with a colon or put the code outside the brackets.
   - Assign one letter and one digit to each change.

3. Choose the letter by what the change affects.

   - `A` — Public API: exported names, availability, signatures, parameters, return types, or other published types. Adding a public helper is `A`; removing or incompatibly changing one is also `A`.
   - `B` — Runtime behavior or runtime characteristics of an existing call, including returned values, errors, parsing rules, performance, memory use, or caching, when the public API shape is unchanged.
   - `C` — Build, installation, packaging, distribution artifacts, typing metadata, development tooling, tests, or documentation.

   If more than one letter applies, use the earliest letter: `A` before `B` before `C`.

4. Choose the digit independently from the letter.

   - `1` — Breaking: previously supported caller code can fail, require modification, raise a different error, or receive a different result. A behavior-changing bug fix is still `1` if an existing call now returns something different.
   - `2` — Compatible but observable: the change adds capability, fixes installation or packaging, adds supported artifacts or metadata, or observably improves runtime characteristics without changing existing results.
   - `3` — Unobservable to package callers: only internal development work, tests, documentation, or an implementation detail with no externally observable effect changes.

   If more than one digit applies, use the lowest digit: `1` before `2` before `3`. When uncertain, choose the lower, more disruptive digit.

5. Sort the bullets by code in this exact order:

   `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

   Preserve the pending-change order when multiple bullets have the same code.

6. Write `Impact: N` directly below the heading, where `N` is the lowest digit used by any bullet. Determine this from the digits only; the letters do not affect the summary.

7. End the entry with exactly:

   `<!-- stl-impact: v1 -->`

   This comment must be the final line. Do not place bullets, blank lines, or other text after it.

Before submitting, verify that the entry has the `##` heading, one bracketed code per bullet, all bullets sorted by code, the correct lowest impact digit, and the trailer on the final line.