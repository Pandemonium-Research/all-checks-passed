---
name: impact-log
description: Use this guide when given a release version, release date, and pending changes to produce one correctly formatted, classified, and sorted release-notes entry.
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

Replace every placeholder with the supplied release information. Do not include the code fence or any text before the heading or after the trailer.

## Procedure

1. Write the heading as `## [VERSION] - YYYY-MM-DD`.
   - Keep the supplied version inside square brackets.
   - Put one space on each side of the hyphen.
   - Use a three-part version such as `1.4.0`.
   - Write the supplied date in year-month-day order.

2. Create exactly one bullet for each pending change.
   - Do not omit, combine, or split changes.
   - Start every bullet with `- [LD] `, where `L` is the impact letter and `D` is the impact digit.
   - Preserve the meaning of the supplied change.
   - Put the marker before the description.
   - End the description with a period.
   - Classify all changes before sorting the bullets.

3. Assign each change an impact letter. Test the categories in this order: `A`, then `B`, then `C`.

   - `A`: The public programming or typing interface changes. This includes:
     - adding or removing exported modules, names, functions, classes, or constants;
     - changing parameters, signatures, or accepted input types;
     - changing an actual or declared return type, such as returning a collection where a scalar was returned previously;
     - adding, removing, or changing public type information exposed to type checkers;
     - adding a packaging mechanism whose effect is to expose shipped public annotations to type checkers.
   - `B`: An existing supported call behaves differently, but its public programming and typing interface is unchanged. This includes changes to output content, returned values, exceptions, side effects, or handling of an existing input when no public type changes.
   - `C`: Neither the public interface nor the functional behavior of an existing call changes. Use `C` for:
     - internal refactoring, caching, or dependency implementation choices;
     - speed, memory, or import-time improvements with unchanged functional behavior;
     - documentation, examples, tests, tooling, or CI;
     - builds, distribution metadata, ordinary packaging, or dependency management;
     - changes to supported Python, operating-system, platform, or installation versions.

   Classify by the change’s effect, not the file or mechanism used to implement it. If more than one letter applies, use the earliest letter: `A` before `B` before `C`. The letter does not indicate severity; dropping a supported environment is `C`, even though it is breaking.

4. Assign the impact digit independently of the letter.

   - `1`: Breaking. Use this when a previously valid, supported, working use can fail, become unsupported, or produce a different result. This includes incompatible API changes, changed established output, and removal of supported runtime, platform, or installation support.
   - `2`: Compatible and functionally observable. Use this when consumers can use or observe the change while correct existing uses continue working. This includes additive public API or typing changes and fixes for previously failing or incorrect cases.
   - `3`: Not functionally observable. Use this when public signatures, accepted inputs, results, exceptions, side effects, and supported workflows remain unchanged. Documentation, internal refactoring, internal dependency substitutions, and behavior-equivalent performance work are normally `3`.

   Performance differences alone do not make a change digit `2`. If more than one digit applies, use the lowest digit: `1` before `2` before `3`.

   Common combinations are:
   - `A1`: incompatible public programming or typing interface change;
   - `A2`: compatible public programming or typing interface addition;
   - `B1`: incompatible behavior change with an unchanged interface;
   - `B2`: compatible behavior fix;
   - `C1`: removal of supported environment or installation support;
   - `C2`: compatible packaging, environment, or installation capability;
   - `C3`: internal, documentation, dependency, tooling, or behavior-equivalent performance work.

5. Sort the bullets by their complete markers in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the supplied order only among changes with identical markers. Do not sort solely by digit: every `C1` bullet belongs after all `B` bullets and before every `C2` or `C3` bullet.

6. Write `Impact:` followed by the numerically lowest digit used in any bullet marker.
   - If any marker ends in `1`, write `Impact: 1`.
   - Otherwise, if any marker ends in `2`, write `Impact: 2`.
   - Otherwise, write `Impact: 3`.
   - Consider only digits inside impact markers.
   - Do not use digits from the version, date, API names, descriptions, or trailer.
   - This value is neither the number of changes nor the most frequent marker digit.

7. Add `<!-- stl-impact: v1 -->` as the exact final line after all bullets.

When classification remains genuinely ambiguous, choose the more disruptive classification: the earlier letter and the lower digit.