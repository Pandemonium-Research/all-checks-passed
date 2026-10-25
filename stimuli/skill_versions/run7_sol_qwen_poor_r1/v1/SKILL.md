---
name: impact-log
description: Use this guide to turn a release version, date, and list of pending changes into a correctly formatted, impact-tagged release notes entry.
---

# Release notes

Create one release entry using this exact structure:

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: LOWEST_MARKER_DIGIT
- [A1] Change description.
- [A2] Change description.
- [B2] Change description.
- [C3] Change description.
<!-- stl-impact: v1 -->
```

Replace the placeholders with the supplied release information. Do not include the code fence in the release notes.

## Procedure

1. Write the heading as `## [VERSION] - YYYY-MM-DD`.
   - Keep the version inside square brackets.
   - Put one space on each side of the hyphen.
   - Use a three-part version such as `1.4.0`.
   - Write the date in year-month-day order.

2. Create exactly one bullet for each pending change.
   - Do not combine changes.
   - Do not split one change into multiple bullets.
   - Start every bullet with `- [LD] `, where `L` is the impact letter and `D` is the impact digit.
   - Put the bracketed marker before the change description, never after it.

3. Assign each change an impact letter:
   - `A`: The public API surface changes. This includes exported names, function or method signatures, parameters, return types, accepted input types, and other public type changes.
   - `B`: An existing call behaves differently at runtime, but its public API surface is unchanged.
   - `C`: No caller-observable behavior changes. Use this for internal implementation work and changes limited to builds, packaging, tooling, tests, CI, or documentation.

   If more than one letter applies, use the earliest letter: `A` before `B` before `C`.

4. Assign the impact digit independently of the letter:
   - `1`: Breaking. Previously working caller code can now fail or produce a different result.
   - `2`: Compatible and caller-observable. This includes additive API changes and bug fixes that leave correct existing calls working.
   - `3`: Not caller-observable. Public signatures, accepted inputs, outputs, and runtime behavior are unchanged.

   If more than one digit could apply, use the lowest digit: `1` before `2` before `3`.

5. Sort the bullets by their complete markers in ascending order:
   - Sort letters as `A`, `B`, `C`.
   - Within the same letter, sort digits as `1`, `2`, `3`.
   - Preserve the supplied order for changes with identical markers.

6. Write `Impact:` followed by the lowest digit used in any bullet marker.
   - Consider only the digits inside impact markers.
   - Do not use digits from the version, date, API names, change descriptions, or trailer.
   - This value is not the number of changes and not the most frequent marker digit.

7. Add `<!-- stl-impact: v1 -->` as the final line, after all bullets.

When classification is genuinely ambiguous, choose the more disruptive classification: the earlier letter and the lower digit.