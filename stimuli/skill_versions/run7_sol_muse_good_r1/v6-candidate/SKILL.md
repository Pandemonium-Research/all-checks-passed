---
name: impact-log
description: Use this skill when writing release notes, changelog entries, or version history for this project, so that entries follow the team's house impact-log format and downstream tooling can parse them.
---

# Release notes

Given a version, release date, and list of pending changes, write one release-nototes entry. Include every pending change exactly once, using one bullet per change.

Each bullet begins with an impact code in square brackets. Choose its letter and digit independently.

## Choose the letter

- `A` — The change adds, removes, or modifies the public API, including exported names, signatures, accepted types, or return types.
- `B` — The change affects package import, runtime behavior, or an internal runtime implementation without changing the public API. Internal caches and runtime refactors are `B` even when signatures and results are unchanged.
- `C` — The change is confined to build configuration, packaging, tooling, tests, or documentation.

If multiple letters apply, use the first in this order: `A`, `B`, `C`.

## Choose the digit

- `1` — Breaking: previously correct, supported caller code can now fail or produce an incompatible result.
- `2` — Compatible and observable: the change adds a capability, fixes incorrect behavior, or explicitly improves runtime or import-time performance.
- `3` — Unobservable: callers receive no stated change to the public API, results, or performance.

A compatible bug fix is `2`, even when affected inputs now produce a different, corrected result. Do not classify it as `1` merely because its output changed.

An internal cache or runtime refactor is `B3` when results and signatures are unchanged and no performance improvement is claimed. It is `B2` only when the pending change explicitly states an observable performance improvement.

If multiple digits apply, use the first in this order: `1`, `2`, `3`.

## Format and order the entry

Use this exact structure:

`## [X.Y.Z] - YYYY-MM-DD`  
`Impact: N`  
one coded bullet per pending change  
`<!-- stl-impact: v1 -->`

Use the supplied three-part version and date. Write each bullet concisely in the past tense, preserving important identifiers in backticks. Do not combine changes or invent effects.

Sort bullets by their complete codes in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple bullets have the same code, preserve their order from the supplied pending-change list.

Set `Impact` to the lowest digit used by any bullet, regardless of its letter.

Place `<!-- stl-impact: v1 -->` on the final line.