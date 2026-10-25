---
name: impact-log
description: Use when given a version number, release date, and pending project changes to write a classified, ordered release-notes entry in the team's parser-compatible impact-log format.
---

# Release notes

Write exactly one release entry in this form:

`## [X.Y.Z] - YYYY-MM-DD`  
`Impact: N`  
one bullet for each pending change  
`<!-- stl-impact: v1 -->`

Use the supplied three-part version without a leading `v`. Use the supplied date in `YYYY-MM-DD` format. The trailer comment must be the final line.

## Assign each impact code

Prefix every bullet with exactly one letter-and-digit code, such as `- [B2]`. Choose the letter and digit independently.

### Choose the letter

Use the first applicable category in this order:

1. `A` — The public API changes. This includes adding or removing exported names, changing signatures, expanding or narrowing accepted argument types, changing return types, or changing other published types.
2. `B` — Package import or runtime execution changes without changing the public API. This includes bug fixes, performance changes, runtime refactors, caches, and other internal runtime implementation changes, even when results remain unchanged.
3. `C` — The change is confined to build configuration, packaging, distributed metadata, tooling, tests, or documentation.

If multiple categories apply, use `A` before `B` before `C`.

Changing an exported type contract is `A`. Adding packaging metadata that exposes otherwise unchanged annotations to type-checking tools is `C`.

### Choose the digit

Use the first applicable category in this order:

1. `1` — Breaking: previously correct use of the public contract can now fail or produce an incompatible result.
2. `2` — Compatible and observable: the change adds capability, fixes incorrect behavior, explicitly improves performance, or visibly changes documentation, distributed artifacts, installation, or a supported workflow.
3. `3` — Unobservable: the public contract, results, stated performance, distributed artifacts, installation behavior, and documented workflows remain unchanged.

If multiple categories apply, use `1` before `2` before `3`.

A compatible bug fix is `2`, even though the buggy inputs now produce corrected results. Do not mark a bug fix as `1` solely because its result changed.

Classify only effects stated in the pending change. An internal cache, refactor, or optimization is `3` if no observable effect is claimed. It is `2` if the description explicitly states an observable improvement, such as reduced execution or import time.

For `C` changes, added documentation or changed package contents are `2`. Tests and migrations explicitly stated to leave artifacts, installation, and workflows unchanged are `3`.

## Write and order the bullets

Write one concise, past-tense bullet for every pending change. Preserve important identifiers in backticks. Do not omit changes, combine unrelated changes, or invent effects.

Sort bullets by their complete code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For bullets with the same code, preserve their order from the supplied pending-change list.

## Calculate the impact summary

Set `Impact` to the lowest digit used by any bullet, regardless of its letter.

Before returning the entry, verify that every pending change appears exactly once, every code follows these rules, equal-code bullets retain their original order, the impact number is the minimum bullet digit, and `<!-- stl-impact: v1 -->` is the final line.