---
name: impact-log
description: Use this skill when writing release notes, changelog entries, or version history for this project, so that entries follow the team's house impact-log format and downstream tooling can parse them.
---

# Release notes

Given a version, release date, and list of pending changes, produce one release-notes entry. Include every pending change exactly once as a separate bullet.

Each bullet must begin with an impact code in square brackets, made of one letter and one digit. Choose the letter and digit independently.

## Choose the letter

Use the first applicable letter:

1. `A` — The public API contract changes. This includes adding exported names or changing exported signatures, accepted argument types, return types, or other published types. Compatible API additions and expansions are still `A`.
2. `B` — Package import or runtime code changes without changing the public API contract. This includes bug fixes, performance changes, caches, runtime refactors, and other internal runtime implementation changes, even when signatures and results remain unchanged.
3. `C` — The change is confined to build configuration, packaging, distributed metadata, tooling, tests, or documentation.

If more than one letter applies, use `A` before `B` before `C`.

## Choose the digit

Use the first applicable digit:

1. `1` — Breaking: previously correct, supported usage can now fail or behave incompatibly.
2. `2` — Compatible and observable: capability is added, incorrect behavior is fixed, performance is explicitly improved, or users, developers, or packagers otherwise receive a visible change.
3. `3` — Unobservable: no change is stated to the public contract, results, performance, distributed artifacts, installation behavior, or documented workflows.

If more than one digit applies, use `1` before `2` before `3`.

A compatible bug fix is `2`, even though affected inputs now produce a corrected result. Do not classify it as `1` merely because its result changed.

Classify only effects stated in the pending change. An internal cache, refactor, or optimization is `B3` when no observable effect is claimed. It is `B2` when the change explicitly promises an observable runtime or import-time improvement.

Visible documentation and distributed-package changes are `C2`. Tests and internal migrations explicitly stated to leave artifacts, installation, and workflows unchanged are `C3`.

## Format the entry

Use this exact structure:

`## [X.Y.Z] - YYYY-MM-DD`  
`Impact: N`  
one bullet per pending change  
`<!-- stl-impact: v1 -->`

Use the supplied three-part version in square brackets and the supplied date in `YYYY-MM-DD` format.

Write each bullet concisely in the past tense and preserve important identifiers in backticks. Do not combine changes or invent effects.

Sort bullets by their complete codes in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple bullets have the same code, preserve their order from the supplied pending-change list.

Set `Impact` to the lowest digit used by any bullet, regardless of its letter.

Place `<!-- stl-impact: v1 -->` on the final line.