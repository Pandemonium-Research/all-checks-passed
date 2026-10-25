---
name: impact-log
description: Use this skill to convert a release version, release date, and pending changes into one correctly classified, sorted, machine-parseable impact-log release-not notes entry.
---

# Release notes

Produce exactly one release entry. Include every pending change exactly once, and output nothing before or after the entry.

Use this structure with no blank lines:

`## [<version>] - <YYYY-MM-DD>`  
`Impact: <digit>`  
`- [<letter><digit>] <change description>`  
`<!-- stl-impact: v1 -->`

Copy the supplied three-part version and date exactly. The trailer comment must be the final line.

## Classify every change

Assign each change one letter and one digit. Choose the letter and digit independently, using only effects stated or clearly implied by the change.

### Choose the letter

Apply these rules in order:

1. Use **A** if the public API changes. This includes:
   - adding or removing an exported name;
   - changing a public signature;
   - changing accepted argument types or declared return types;
   - changing public annotations; or
   - adding package metadata that makes shipped annotations visible to downstream type checkers.
2. Otherwise, use **B** if runtime code, runtime behavior, or runtime performance changes. This includes:
   - changed results or exceptions;
   - bug fixes;
   - algorithm changes;
   - import-time or lazy-loading changes; and
   - internal runtime caches or refactors, even when their results and signatures are unchanged.
3. Otherwise, use **C** for build configuration, packaging, dependency distribution, tooling, tests, or documentation.

If more than one letter applies, use the first applicable letter: **A before B before C**.

### Choose the digit

Apply these rules in order:

1. Use **1** only for an incompatible change to supported behavior. Assign 1 when previously correct caller code can now fail, become invalid, or receive a result incompatible with the documented contract.
2. Otherwise, use **2** for an externally observable, backward-compatible change. This includes:
   - an added API;
   - a newly accepted input;
   - a compatible bug fix that restores intended behavior;
   - newly exposed typing information;
   - a stated performance or import-time improvement; or
   - an observable change to installed or distributed dependencies.
3. Otherwise, use **3** because no consumer-facing effect is identified. This includes:
   - an internal runtime cache or refactor whose signature, results, exceptions, and documented behavior are unchanged;
   - documentation, test, or tooling changes; or
   - packaging or build changes explicitly described as leaving installation unchanged.

A result change caused by a compatible bug fix is **2**, not 1. Do not treat an erroneous result as supported behavior unless the pending change explicitly says callers relied on it or the documented contract is being broken.

The letter does not determine the digit. In particular:

- an internal runtime refactor with unchanged behavior is **B3**;
- a documentation-only change is **C3**;
- a distributed-dependency change is normally **C2**; and
- exposed package typing metadata is **A2**.

If a change has several stated effects, use the lowest applicable digit: **1 before 2 before 3**. If the supplied information genuinely leaves two classifications possible, choose the more disruptive one, but do not invent an incompatibility that is not stated or implied.

## Calculate the impact

Set `Impact` to the lowest digit used by any bullet:

- use `Impact: 1` if any bullet ends in 1;
- otherwise, use `Impact: 2` if any bullet ends in 2;
- otherwise, use `Impact: 3`.

## Sort and write the bullets

Sort bullets in this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes assigned the same code.

Write each bullet as:

`- [<code>] <clear past-tense description>`

Do not omit, duplicate, merge, or split pending changes.