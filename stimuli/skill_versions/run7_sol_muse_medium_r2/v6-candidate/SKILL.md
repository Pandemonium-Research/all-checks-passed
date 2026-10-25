---
name: impact-log
description: Convert a supplied release version, date, and list of pending project changes into one classified, sorted, machine-parseable impact-log release-notes entry. Use when adding a release, changelog, or version-history entry for this project.
---

# Release notes

Produce exactly one release entry containing every pending change exactly once. Output only the entry: no code fence, introduction, explanation, or trailing text.

Use this exact structure with no blank lines:

`## [<version>] - <YYYY-MM-DD>`  
`Impact: <digit>`  
`- [<letter><digit>] <change description>`  
`<!-- stl-impact: v1 -->`

Repeat the bullet line once per pending change. Copy the supplied version and date exactly. The trailer comment must be the final line.

## Classify each change

Assign one letter and one digit to each pending change. Determine them independently from effects stated or clearly implied by that change. Do not infer unstated compatibility, performance, or consumer effects.

### Choose the letter

Apply these rules in order and stop at the first applicable rule:

1. Use **A** when the public API changes. This includes:
   - adding, removing, or renaming an exported name;
   - changing a public signature, parameter, or default;
   - changing accepted argument types or declared return types;
   - changing public annotations; or
   - adding package metadata that exposes shipped annotations to downstream type checkers.
2. Otherwise, use **B** when runtime code, behavior, or performance changes. This includes:
   - changed results or exceptions;
   - bug fixes;
   - algorithm or runtime implementation changes;
   - import-time or lazy-loading changes; and
   - internal runtime caches or refactors, even when signatures, results, and documented behavior remain unchanged.
3. Otherwise, use **C** for build configuration, packaging, installed or vendored dependencies, tooling, tests, or documentation.

When several letters apply, use the earliest: **A before B before C**.

In particular:

- A changed runtime result is **B** unless the public API also changes.
- An unchanged-behavior runtime cache or refactor is **B**, not C.
- Metadata that exposes package typing is **A**, not C.
- A dependency-distribution change is **C** unless another stated effect requires A or B.
- Documentation and docstring examples are **C**.

### Choose the digit

Apply these rules in order and stop at the first applicable rule:

1. Use **1** only for an incompatible change to supported behavior. The change must state or clearly imply that previously valid caller code can now fail, become invalid, or receive a result incompatible with the documented contract.
2. Otherwise, use **2** for a backward-compatible consumer effect. This includes:
   - adding public API;
   - accepting a new input or widening an accepted type;
   - fixing a bug while preserving the supported contract;
   - exposing typing information to downstream tools;
   - a stated runtime or import-time improvement; or
   - changing installed, distributed, or vendored dependencies.
3. Otherwise, use **3** because no consumer-impacting effect is identified. This includes:
   - an internal runtime cache or refactor whose signature, results, exceptions, and documented behavior are unchanged;
   - documentation, tests, or tooling changes; and
   - packaging or build changes explicitly described as leaving installation unchanged.

A bug fix is **2**, not 1, merely because it corrects an erroneous result. Use **1** only when supported or documented behavior becomes incompatible.

Do not infer a performance improvement merely because a cache or algorithm changed. Without a stated consumer effect, an unchanged-behavior runtime change is **B3**.

Use these checks:

- incompatible public API change: **A1**
- added or widened public API: **A2**
- exposed package typing metadata: **A2**
- incompatible supported runtime behavior: **B1**
- compatible runtime bug fix: **B2**
- stated runtime performance or import-time improvement: **B2**
- unchanged-behavior runtime refactor or cache: **B3**
- changed distributed or vendored dependencies: **C2**
- documentation-only, test-only, or tooling-only change: **C3**
- packaging change with installation explicitly unchanged: **C3**

If one pending change states several effects, assign it one code. Use the earliest applicable letter and the lowest applicable digit: **1 before 2 before 3**. Resolve genuine uncertainty toward the more disruptive classification, but never invent an incompatibility or observable effect.

## Calculate the impact

Set `Impact` to the lowest digit assigned to any bullet:

- Use `Impact: 1` if any bullet ends in 1.
- Otherwise, use `Impact: 2` if any bullet ends in 2.
- Otherwise, use `Impact: 3`.

## Sort and write the bullets

Sort bullets in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among changes with the same code.

Write each bullet as:

`- [<code>] <clear past-tense description>`

Preserve technical facts and compatibility qualifications from the supplied change. Do not omit, duplicate, combine, or split pending changes.

Before returning the entry, verify that:

- the heading contains the supplied version and date;
- every pending change appears once;
- every bullet has exactly one valid code;
- `Impact` is the lowest bullet digit;
- bullets follow the required code order;
- there are no blank lines; and
- the trailer comment is the final line.