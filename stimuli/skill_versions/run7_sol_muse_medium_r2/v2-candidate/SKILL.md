---
name: impact-log
description: Use this skill to turn a release version, date, and pending changes into a classified, sorted, machine-parseable release-notes entry in the project's impact-log format.
---

# Release notes

Create one release entry containing every pending change exactly once.

Use this exact structure, with no blank lines:

`## [<version>] - <YYYY-MM-DD>`  
`Impact: <digit>`  
`- [<letter><digit>] <change description>`  
`<!-- stl-impact: v1 -->`

Use the supplied three-part version and date. The trailer comment must be the final line.

## Classify each change

Assign each change one letter and one digit. Choose them independently and classify only effects stated or clearly implied by the change.

### Choose the letter

Apply these rules in order:

1. Use **A** for changes to the public API. This includes exported names, signatures, accepted argument types, return types, public annotations, and package metadata that exposes shipped typing information.
2. Otherwise, use **B** for runtime changes. This includes result or exception changes, bug fixes, algorithms, performance, import-time behavior, lazy loading, and internal runtime caches. A runtime implementation change remains B when its public signature and results are unchanged.
3. Otherwise, use **C** for build configuration, packaging, dependency distribution, tooling, tests, or documentation.

When several letters apply, use the earliest one: **A before B before C**.

### Choose the digit

Apply these rules in order:

1. Use **1** for an incompatible change to supported behavior: correct existing caller code can now fail or receive an incompatible result.
2. Otherwise, use **2** for an externally observable but backward-compatible change. This includes additive APIs, newly accepted inputs, bug fixes that restore intended behavior, exposed typing information, stated performance improvements, and changes to installed dependencies.
3. Otherwise, use **3** when no consumer-facing effect is identified. This includes runtime refactors whose signatures, results, and documented behavior are unchanged, documentation or tooling changes, and packaging or build changes explicitly described as leaving installation unchanged.

A corrected erroneous result is normally a compatible bug fix and therefore digit **2**, unless the change explicitly says that supported behavior is being broken.

When several digits apply, use the lowest one: **1 before 2 before 3**. If the supplied information leaves genuine uncertainty, choose the more disruptive applicable digit.

## Calculate the impact

Set `Impact` to the lowest digit assigned to any bullet, regardless of its letter.

For example, if the entry contains digits 2 and 3, use `Impact: 2`. If any bullet has digit 1, use `Impact: 1`.

## Order and write the bullets

Sort bullets in this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the pending-change order among bullets with the same code. Begin each bullet with its code in square brackets, followed by a clear past-tense description. Do not omit, duplicate, or combine pending changes.