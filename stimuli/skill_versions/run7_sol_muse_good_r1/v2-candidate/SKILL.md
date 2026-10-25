---
name: impact-log
description: Use when given a version number, release date, and pending project changes to produce a classified, ordered, and parser-compatible release-not notes entry.
---

# Release notes

Produce exactly one entry in this structure:

`## [X.Y.Z] - YYYY-MM-DD`  
`Impact: N`  
one bullet per pending change  
`<!-- stl-impact: v1 -->`

Use the supplied three-part version without a leading `v` and the supplied date in `YYYY-MM-DD` format. Return only the entry. Make the trailer comment the final line.

## Classify each change

Prefix every bullet with one code such as `- [A2]`. Choose the letter and digit independently.

### Choose the letter

Use the first applicable category:

1. `A` — The public API contract changes. This includes exported names, signatures, accepted argument types, return types, and other published types. New public API and compatible expansions of accepted types are also `A`.
2. `B` — Package import or runtime execution changes without changing the public API contract. Use `B` for bug fixes, performance changes, runtime refactors, caches, and other internal runtime implementation changes, even when results remain unchanged.
3. `C` — The change is confined to build configuration, packaging, tooling, tests, or documentation.

If multiple letters apply, use `A` before `B` before `C`.

Changing an exported type contract is `A`. Adding metadata that makes unchanged annotations discoverable to type-checking tools is `C`.

### Choose the digit

Use the first applicable category:

1. `1` — Breaking: previously correct, supported usage can now fail or behave incompatibly.
2. `2` — Compatible and externally noticeable: capability is added, incorrect behavior is fixed, stated performance improves, or users, developers, or packagers otherwise receive a visible change.
3. `3` — Unobservable: the public contract, results, performance, distributed artifacts, installation behavior, and documented workflows remain unchanged.

If multiple digits apply, use `1` before `2` before `3`.

A compatible bug fix is `2`, even though affected inputs now return corrected results. Do not mark it `1` solely because the result changed.

Classify only effects stated in the pending change. An internal optimization or cache is `3` when no observable effect is claimed; it is `2` when the change explicitly promises an observable performance improvement.

For `C` changes, visible documentation or distributed-package changes are `2`. Tests and internal migrations explicitly stated to leave artifacts, installation, and workflows unchanged are `3`.

## Write and order the bullets

Write one concise, past-tense bullet for every pending change. Preserve important identifiers in backticks. Do not omit or combine changes, and do not invent effects.

Sort bullets by their complete codes in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple bullets have the same code, preserve their order from the supplied pending-change list.

## Calculate the impact summary

Set `Impact` to the lowest digit used by any bullet, regardless of its letter.

Before returning the entry, verify that:

- Every pending change appears exactly once.
- Every bullet has the correct letter and digit.
- Bullets are stably sorted by complete code.
- `Impact` equals the lowest bullet digit.
- `<!-- stl-impact: v1 -->` is the final line.