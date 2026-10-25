---
name: impact-log
description: Use when given a version number, release date, and pending changes to write a parser-compatible release-notes or changelog entry in the project's impact-log format.
---

# Release notes

Write exactly one entry containing every pending change exactly once.

## Format

Use this exact structure:

`## [X.Y.Z] - YYYY-MM-DD`  
`Impact: N`  
one bullet per pending change  
`<!-- stl-impact: v1 -->`

Use the supplied three-part version without a leading `v` and the supplied date in `YYYY-MM-DD` format. Write each bullet as `- [A1] Description`, replacing `A1` with the appropriate impact code. The trailer comment must be the final line.

## Choose each impact code

Choose the letter and digit independently. If more than one applies, use the earliest letter (`A` before `B` before `C`) and the lowest digit (`1` before `2` before `3`).

### Letter

- `A` — The public API changes. This includes adding or removing exported names, changing exported signatures or return types, and expanding or narrowing accepted argument types.
- `B` — Package import or runtime code changes without changing the public API. This includes bug fixes, performance changes, caches, and internal runtime refactors. Use `B` for runtime implementation changes even when results and signatures are unchanged.
- `C` — The change is confined to build configuration, packaging, distributed package contents or metadata, tooling, tests, or documentation.

Packaging metadata that exposes existing annotations to type checkers is `C`, not `A`. Replacing or vendoring a dependency without changing the public API is also `C`.

### Digit

- `1` — Breaking: previously correct, supported use of the public contract can now fail or produce an incompatible result.
- `2` — Compatible and observable: the change adds capability, fixes incorrect behavior, explicitly improves performance, visibly changes documentation, changes distributed package contents, or changes installation or a supported workflow.
- `3` — Unobservable: the public contract, results, stated performance, distributed artifacts, installation behavior, and documented workflows remain unchanged.

A compatible bug fix is `2`, even when affected inputs now return a different, corrected result. Do not mark a bug fix as `1` merely because its output changed.

Classify only effects stated in the pending change:

- An internal cache or runtime refactor with unchanged results and no claimed performance improvement is `B3`.
- An explicitly stated runtime or import-time improvement is `B2`.
- Added or visibly changed documentation is `C2`.
- A change to distributed package contents or dependencies is `C2`.
- A packaging, tooling, test, or build migration explicitly stated to leave artifacts, installation, and workflows unchanged is `C3`.

## Write and order the bullets

Write one concise, past-tense bullet for each pending change. Preserve important identifiers in backticks. Do not omit changes, combine unrelated changes, or invent effects.

Sort bullets by complete code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When bullets have the same code, preserve their order from the supplied pending-change list.

## Calculate the impact summary

Set `Impact` to the lowest digit used by any bullet, regardless of its letter.

Before returning the entry, verify that every pending change appears exactly once, every impact code follows these rules, the bullets are correctly ordered, the impact summary is the minimum bullet digit, and `<!-- stl-impact: v1 -->` is the final line.