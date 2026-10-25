---
name: impact-log
description: Use this guide when given a release version, release date, and pending changes to produce one correctly formatted, impact-tagged, and sorted release-notes entry.
---

# Release notes

Create exactly one release entry using this structure:

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: LOWEST_MARKER_DIGIT
- [MARKER] Change description.
- [MARKER] Change description.
<!-- stl-impact: v1 -->
```

Replace the placeholders with the supplied release information. Do not include the code fence, introductory text, or text after the trailer.

## Procedure

1. Write the heading as `## [VERSION] - YYYY-MM-DD`.
   - Keep the supplied three-part version inside square brackets.
   - Put one space on each side of the hyphen.
   - Write the supplied date in year-month-day order.

2. Create exactly one bullet for each pending change.
   - Do not omit, combine, or split changes.
   - Start every bullet with `- [LD] `, where `L` is the impact letter and `D` is the impact digit.
   - Preserve the meaning of the pending change.
   - End the description with a period.
   - Classify every change before sorting the bullets.

3. Assign each change an impact letter. Test the categories in this order: `A`, then `B`, then `C`.

   - `A`: The public programming or typing interface changes. This includes exported names, signatures, parameters, accepted input types, return types or representations, public annotations, and mechanisms that expose shipped type information to type checkers.
     - Adding or removing a public name is `A`.
     - Changing a function from returning one representation or type to another is `A`, even if its name and parameters are unchanged.
     - A packaging marker that makes public annotations available to type checkers is `A`, because classification follows its public effect.
   - `B`: An existing supported call behaves differently, but its public programming and typing interface is unchanged. This includes changed output content, exceptions, side effects, or handling of an existing input.
   - `C`: Neither the public interface nor the functional behavior of an existing call changes. Use `C` for:
     - internal refactoring, caching, or dependency implementation choices;
     - speed, memory, or import-time improvements with unchanged results and behavior;
     - documentation, examples, tests, tooling, or CI;
     - builds, distribution metadata, packaging, dependency management, and supported Python, operating-system, or platform versions.

   If multiple categories apply, use the earliest applicable letter: `A` before `B` before `C`. The letter does not indicate severity; for example, dropping a supported runtime is `C`, even though it is breaking.

4. Assign the impact digit independently of the letter.

   - `1`: Breaking. A previously valid, supported, working use can fail, become unsupported, or produce a different result. This includes incompatible API or output changes and removal of supported runtime, platform, or installation support.
   - `2`: Compatible and observable. Consumers can use or observe the change while correct existing uses continue working. This includes additive API or typing changes and fixes for previously failing or incorrect cases.
   - `3`: Not functionally observable. Public signatures, accepted inputs, results, exceptions, side effects, and supported workflows remain unchanged. Documentation, internal refactoring, internal dependency substitutions, and output-equivalent performance work are normally `3`.

   If multiple digits apply, use the lowest digit: `1` before `2` before `3`. Do not infer the digit from the letter. Valid combinations include `A2` for an additive public interface, `B1` for changed behavior without an interface change, `C1` for dropped environment support, and `C3` for behavior-equivalent engineering work.

5. Sort the bullets by their complete markers in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the supplied order only among changes with identical markers. In particular, place every `C1` bullet before every `C2` and `C3` bullet.

6. Write `Impact:` followed by the numerically lowest digit used in any bullet marker.
   - If any marker ends in `1`, write `Impact: 1`.
   - Otherwise, if any marker ends in `2`, write `Impact: 2`.
   - Otherwise, write `Impact: 3`.
   - Consider only digits inside impact markers, not digits in the version, date, names, descriptions, or trailer.
   - This value is neither the number of changes nor the most frequent digit.

7. Add `<!-- stl-impact: v1 -->` as the exact final line after all bullets.

When classification remains genuinely ambiguous, choose the more disruptive classification: the earlier letter and the lower digit.