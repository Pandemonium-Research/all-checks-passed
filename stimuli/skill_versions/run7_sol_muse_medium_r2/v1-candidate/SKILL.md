---
name: impact-log
description: Use this skill to turn a version number, release date, and list of pending project changes into a correctly classified, sorted, and machine-parseable release-notes entry in the team's impact-log format.
---

# Release notes

Create one entry containing every pending change exactly once.

Use this structure:

`## [<version>] - <YYYY-MM-DD>`  
`Impact: <lowest digit used by any bullet>`  
`- [<letter><digit>] <change description>`  
`<!-- stl-impact: v1 -->`

Use the supplied three-part version number and date. The trailer must be the final line of the entry.

## Classify each change

Choose the letter first, then choose the digit independently. Do not infer effects that are not stated or implied by the pending change.

### Choose the letter

Apply these tests in order:

1. Use **A** if the change affects the public API. This includes exported names, signatures, accepted argument types, return types, public annotations, and metadata that exposes shipped types to downstream type checkers.
2. Otherwise, use **B** if the change affects code executed when consumers import the package or call it. This includes algorithms, returned results, raised exceptions, performance, lazy imports, and internal runtime caches. Runtime implementation changes remain B even when signatures and results are unchanged.
3. Otherwise, use **C** for build configuration, packaging, dependency distribution, tooling, tests, or documentation.

If more than one letter applies, use the earliest letter: **A before B before C**.

### Choose the digit

Apply these tests in order:

1. Use **1** if an existing supported call can now fail or produce a different result. This includes incompatible API changes and fixes that change the result for an input that previously completed successfully.
2. Otherwise, use **2** if the change is externally observable but backward compatible. Examples include additive APIs, newly accepted input types, exposed typing information, stated performance improvements, and changes to installed dependencies.
3. Otherwise, use **3** if no consumer-facing effect is identified. Use this for runtime refactors whose signatures, results, and documented behavior are unchanged, and for documentation, tooling, packaging, or build changes explicitly described as leaving consumer behavior or installation unchanged.

If more than one digit applies, use the lowest digit: **1 before 2 before 3**. When uncertain, select the more disruptive applicable classification.

## Calculate the impact

Set `Impact` to the lowest digit used by any bullet, regardless of its letter.

For example, an entry containing codes ending in 2 and 3 has `Impact: 2`; an entry containing any code ending in 1 has `Impact: 1`.

## Order and format the bullets

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the pending-change order for bullets with the same code. Begin every bullet with its code in square brackets, followed by one clear past-tense description of the change. Do not omit, duplicate, or merge pending changes.