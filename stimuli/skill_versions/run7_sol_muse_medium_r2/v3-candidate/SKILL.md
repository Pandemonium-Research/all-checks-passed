---
name: impact-log
description: Use this skill to convert a release version, release date, and list of pending project changes into a correctly classified, sorted, and machine-parseable impact-log release-notes entry.
---

# Release notes

Create one release entry containing every pending change exactly once. Return only the entry, without a code fence or additional text.

Use this exact structure with no blank lines:

`## [<version>] - <YYYY-MM-DD>`  
`Impact: <digit>`  
`- [<letter><digit>] <change description>`  
`<!-- stl-impact: v1 -->`

Use the supplied three-part version and date. Place the trailer comment on the final line.

## Classify each change

Assign one letter and one digit independently. Base the classification only on effects stated or clearly implied by the pending change; do not invent additional effects.

### Choose the letter

Apply these rules in order:

1. Use **A** for a public API change. This includes adding or removing exported names; changing signatures, accepted argument types, declared return types, or public annotations; and adding package metadata that exposes shipped typing information to downstream tools.
2. Otherwise, use **B** for a runtime implementation or behavior change. This includes changed results or exceptions, bug fixes, algorithms, performance, import-time behavior, lazy imports, and internal runtime caches. Use B for runtime refactors even when public signatures and results remain unchanged.
3. Otherwise, use **C** for build configuration, packaging, dependency distribution, tooling, tests, or documentation.

If several letters apply, use the earliest: **A before B before C**. A changed runtime return value is B unless the public API’s declared return type also changed.

### Choose the digit

Apply these rules in order:

1. Use **1** when the release breaks supported behavior: previously correct caller code can now fail, become invalid, or receive a result incompatible with the documented contract.
2. Otherwise, use **2** for an externally observable, backward-compatible change. This includes additive APIs, newly accepted inputs, compatible bug fixes that restore intended behavior, newly exposed typing information, stated performance improvements, and changes to installed or distributed dependencies.
3. Otherwise, use **3** when no consumer-facing effect is identified. This includes runtime refactors whose signatures, results, and documented behavior are unchanged; documentation, test, or tooling changes; and packaging or build changes explicitly described as leaving installation unchanged.

Do not assign digit 1 to a compatible bug fix merely because its corrected result differs from the erroneous result. An internal runtime change with unchanged behavior is **B3**, not C3. Documentation-only changes are **C3**. Dependency vendoring or another observable change to installed dependencies is **C2** unless the change explicitly says installation is unchanged.

If several digits apply, use the lowest: **1 before 2 before 3**. When the supplied information leaves genuine uncertainty between applicable classifications, choose the more disruptive digit.

## Calculate the impact

Set `Impact` to the lowest digit assigned to any bullet, regardless of its letter. If any bullet ends in 1, use `Impact: 1`; otherwise, if any bullet ends in 2, use `Impact: 2`; otherwise use `Impact: 3`.

## Order and write the bullets

Sort bullets in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the pending-change order among bullets with the same code. Begin each bullet with its code in square brackets followed by one clear, past-tense description. Do not omit, duplicate, or combine pending changes.