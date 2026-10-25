---
name: impact-log
description: Use this skill to turn a release version, release date, and list of pending project changes into one correctly classified, sorted, machine-parseable impact-log release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every pending change exactly once. Output only the entry, with no code fence, introduction, or trailing text.

Use this exact structure, with no blank lines:

`## [<version>] - <YYYY-MM-DD>`  
`Impact: <digit>`  
`- [<letter><digit>] <change description>`  
`<!-- stl-impact: v1 -->`

Copy the supplied version and date exactly. The trailer comment must be the final line.

## Classify each change

Assign each pending change one letter and one digit. Choose the letter and digit independently, using only effects stated or clearly implied by the change.

### Choose the letter

Apply these rules in order. Stop at the first applicable rule:

1. Use **A** when the public API changes. This includes:
   - adding or removing an exported name;
   - changing a public signature;
   - accepting a new argument type;
   - changing a declared return type or public annotation; or
   - adding package metadata that exposes shipped annotations to downstream type checkers.
2. Otherwise, use **B** when runtime code, behavior, or performance changes. This includes:
   - changed results or exceptions;
   - bug fixes;
   - algorithm changes;
   - performance or import-time changes;
   - lazy imports; and
   - internal runtime caches or refactors, even when signatures and results remain unchanged.
3. Otherwise, use **C** for build configuration, packaging, dependency distribution, tooling, tests, or documentation.

When several letters apply, use the earliest: **A before B before C**.

A runtime result change is **B** unless the public API itself also changes. An internal runtime refactor is **B**, not C. Package typing metadata that exposes annotations is **A**, not C.

### Choose the digit

Apply these rules in order. Stop at the first applicable rule:

1. Use **1** only when supported behavior becomes incompatible. The pending change must state or clearly imply that previously valid caller code can now fail, become invalid, or receive a result that violates the documented contract.
2. Otherwise, use **2** for an externally observable, backward-compatible change. This includes:
   - an added API;
   - a newly accepted input;
   - a compatible bug fix that restores intended behavior;
   - newly exposed typing information;
   - a stated performance or import-time improvement; or
   - an observable change to installed or distributed dependencies.
3. Otherwise, use **3** because no consumer-facing effect is identified. This includes:
   - an internal runtime cache or refactor whose signature, results, exceptions, and documented behavior are unchanged;
   - documentation, tests, or tooling changes; and
   - packaging or build changes explicitly described as leaving installation unchanged.

Do not assign **1** merely because a bug fix changes an erroneous result. A compatible bug fix is **2** unless the change explicitly states or clearly implies that supported behavior is being broken.

Use these category checks:

- added or widened public API: **A2**
- compatible runtime bug fix: **B2**
- stated runtime performance improvement: **B2**
- unchanged-behavior runtime refactor: **B3**
- exposed package typing metadata: **A2**
- changed distributed dependencies: **C2**
- documentation-only change: **C3**
- packaging change with installation explicitly unchanged: **C3**

If one change has several stated effects, use the lowest applicable digit: **1 before 2 before 3**. Resolve genuine uncertainty toward the more disruptive digit, but never invent an incompatibility that is not stated or clearly implied.

## Calculate the impact

Set `Impact` to the lowest digit assigned to any bullet:

- Use `Impact: 1` if any bullet ends in 1.
- Otherwise, use `Impact: 2` if any bullet ends in 2.
- Otherwise, use `Impact: 3`.

## Sort and write the bullets

Sort bullets in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes assigned the same code.

Write each bullet as:

`- [<code>] <clear past-tense description>`

Do not omit, duplicate, combine, or split pending changes.