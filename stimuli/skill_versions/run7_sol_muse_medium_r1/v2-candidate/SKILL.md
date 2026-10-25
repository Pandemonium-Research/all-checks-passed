---
name: impact-log
description: Use this skill to turn a release version, date, and list of pending changes into a classified, sorted, machine-parseable release-notes entry in the project's impact-log format.
---

# Release notes

Write exactly one release entry in this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace the placeholders with the supplied version, date, impact digit, and changes. Include one bullet for every pending change.

## Classify each change

Each code contains a letter and a digit. Choose them independently.

### Letter: area affected

Use **A** for changes to the public API or public typing interface, including:

- Exported names, signatures, parameters, defaults, or return types.
- Public classes, methods, attributes, constants, or protocols.
- Shipped annotations, stubs, and typing marker files that make those annotations visible to type checkers.

Use **B** when the public API is unchanged but runtime behavior or implementation changes, including:

- Different results, exceptions, validation, or input handling.
- Performance, memory use, import behavior, or caching.
- Internal runtime refactors whose output remains unchanged.

Use **C** for project support material and infrastructure, including:

- Builds, packaging, dependencies, vendoring, and distribution artifacts.
- CI, developer tooling, tests, and test layout.
- Documentation, examples, comments, and docstrings.

Classify the effect of the change, not merely the file containing it. If several letters apply, use the earliest: A before B before C.

### Digit: consumer impact

Use **1** when a previously successful caller may now fail or receive a different result. A bug fix is digit 1 if it corrects the result of an existing successful call.

Use **2** for a compatible but observable change, including:

- An additive public API or newly exposed typing information.
- A fix that makes a previously failing case succeed without changing successful cases.
- An observable performance or import-time improvement.
- A packaging, dependency, or distribution change that affects installation or adds support for an environment.

Use **3** when release consumers cannot observe a functional difference, including:

- An internal runtime refactor with unchanged behavior.
- Test-only changes or test-suite reorganization.
- Documentation, examples, comments, and docstrings.

If several digits apply, use the lowest: 1 before 2 before 3. Do not assign digit 2 to every fix: decide whether an already successful call changes.

## Assemble the entry

1. Combine each change's letter and digit into a code such as `[A2]`.
2. Sort bullets by code in this order: A1, A2, A3, B1, B2, B3, C1, C2, C3.
3. Preserve the supplied order among changes with the same code.
4. Set `Impact` to the lowest digit used by any bullet.

## Formatting requirements

- Use the supplied three-part version and ISO date in `## [VERSION] - YYYY-MM-DD`.
- Put `Impact: DIGIT` immediately below the heading.
- Begin every change with `- [CODE]`.
- Describe each change with a concise past-tense sentence.
- Put `<!-- stl-impact: v1 -->` on the final line.
- Do not add any text, bullets, blank lines, or comments after the trailer.