---
name: impact-log
description: Use this guide when given a release version, release date, and pending changes to produce one correctly formatted, impact-classified, and sorted release-notes entry.
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

Replace the placeholders with the supplied release information. Output no code fence, introduction, or text after the trailer.

## Procedure

1. Write the heading as `## [VERSION] - YYYY-MM-DD`.
   - Keep the supplied version inside square brackets.
   - Put one space on each side of the hyphen.
   - Write the supplied date in year-month-day order.

2. Create exactly one bullet for each pending change.
   - Do not omit, combine, or split changes.
   - Start each bullet with `- [LD] `, where `L` is the impact letter and `D` is the impact digit.
   - Preserve the meaning of the supplied change.
   - End each description with a period.
   - Classify all changes before sorting them.

3. Assign each change an impact letter:

   - `A`: The public programming interface changes. This includes exported names, signatures, parameters, accepted input types, return types, and return representations.
     - Adding or removing a public name is `A`.
     - Changing from one return type or representation to another is `A`, even when the function name and parameters are unchanged.
   - `B`: An existing supported call behaves differently, but its public programming interface is unchanged. This includes changed output content, exceptions, side effects, or handling of an existing input.
   - `C`: Neither the public programming interface nor the functional result of an existing call changes. Use `C` for:
     - internal refactoring or caching;
     - performance and import-time improvements with unchanged results;
     - internal dependency substitutions or vendoring;
     - documentation, examples, tests, tooling, or CI;
     - builds, packaging, distribution metadata, and supported runtime or platform changes;
     - packaging metadata that exposes already-shipped annotations to type checkers.

   If multiple letters appear applicable, use the earliest one: `A` before `B` before `C`. The letter and digit are independent: a breaking environment-support change is still `C`.

4. Assign the impact digit independently of the letter:

   - `1`: Breaking. A previously valid, supported use can fail, become unsupported, or produce a different result. This includes incompatible interface or output changes and dropping a supported runtime, platform, or installation environment.
   - `2`: Compatible and caller-observable. Consumers gain a capability or a previously failing or incorrect case is fixed while correct existing uses continue working.
   - `3`: No functional change. Public interfaces, accepted inputs, results, exceptions, side effects, and supported workflows remain unchanged.

   Use `3`, not `2`, for documentation, examples, internal refactoring, internal dependency changes, and output-equivalent performance or import-time improvements. Use `C2` for a compatible packaging capability that consumers can newly use, such as making shipped annotations discoverable. If multiple digits apply, use the lowest digit: `1` before `2` before `3`.

5. Sort bullets by their complete markers in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the supplied order only among changes with identical markers. Do not sort only by digit. In particular, `C1` comes after every `A` and `B` marker but before `C2` and `C3`.

6. Write `Impact:` followed by the numerically lowest digit used in any bullet marker.
   - If any marker ends in `1`, write `Impact: 1`.
   - Otherwise, if any marker ends in `2`, write `Impact: 2`.
   - Otherwise, write `Impact: 3`.
   - Consider only digits inside impact markers, not digits in the version, date, descriptions, or trailer.
   - This value is neither the number of changes nor the most frequent digit.

7. Add `<!-- stl-impact: v1 -->` as the exact final line after all bullets.

When classification remains genuinely ambiguous, choose the more disruptive classification: the earlier letter and the lower digit.