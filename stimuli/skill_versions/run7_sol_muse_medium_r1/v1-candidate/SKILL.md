---
name: impact-log
description: Use this skill to turn a version, release date, and list of pending changes into a correctly classified, sorted, and machine-parseable release-notes entry in the project's impact-log format.
---

# Release notes

Create one entry using this exact structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace the placeholders and add one bullet for every pending change. Do not omit the trailer or add anything after it.

## Procedure

For each change:

1. Choose its letter using the rules below.
2. Choose its digit independently using the rules below.
3. Combine them as `[A1]`, `[B2]`, and so on.
4. Sort all bullets by letter first and digit second: A1, A2, A3, B1, B2, B3, C1, C2, C3.
5. Set `Impact` to the lowest digit used by any bullet.

When several classifications could apply, use the earliest letter—A before B before C—and the lowest digit—1 before 2 before 3.

## Choose the letter

Use **A** when the change affects the public API or public type-checking interface. This includes:

- Exported names, signatures, parameters, defaults, or return types.
- Public classes, methods, attributes, constants, or protocols.
- Shipped annotations, stubs, or markers that cause type checkers to recognize those annotations.
- Any build or packaging change whose meaningful effect is to expose or alter public typing information.

Use **B** when the public API remains the same but runtime behavior or implementation changes. This includes:

- Different results, exceptions, validation, or handling of inputs.
- Performance, memory use, import behavior, or caching changes.
- Runtime refactors and implementation changes, even when results remain unchanged.

Use **C** only for non-API project infrastructure and supporting material. This includes:

- Builds, packaging, dependencies, and distribution artifacts.
- CI, developer tooling, tests, and test layout.
- Documentation, examples, comments, and docstrings.

Classify by the change's user-facing effect, not merely by the file modified. For example, a packaging file that exposes shipped types is A, while a new distribution artifact that expands installation support is C.

## Choose the digit

Use **1** when previously successful caller code may break, fail, or receive a different result. This includes corrected bugs that change the returned value for an existing successful call. Do not automatically classify a change as 2 merely because it is described as a fix.

Use **2** for a compatible but observable change. This includes:

- Additive public APIs or typing information.
- Fixes that make a previously failing case succeed without changing successful existing cases.
- Observable performance or import-time improvements.
- Packaging or distribution changes that add installation support or alter installed dependencies.

Use **3** when the release consumer cannot observe a functional difference. This includes:

- Runtime implementation refactors with unchanged public behavior.
- Test-only changes.
- Documentation, example, comment, and docstring changes.
- Tooling or layout changes that do not affect installation or use.

The letter and digit answer different questions. A runtime refactor with unchanged results can therefore be B3, while an added distribution artifact can be C2.

## Formatting requirements

- Use a level-two heading exactly as `## [VERSION] - YYYY-MM-DD`.
- Use the provided three-part version and ISO date.
- Put `Impact: DIGIT` directly below the heading.
- Start every change with `- [CODE]`.
- Write each change as a concise past-tense sentence.
- Sort bullets by code, regardless of the order in which changes were supplied.
- If multiple bullets have the same code, preserve their input order.
- Put `<!-- stl-impact: v1 -->` on the final line of the entry.
- Do not place blank text, bullets, or comments after the trailer.