---
name: impact-log
description: Use when converting a version number, release date, and list of pending project changes into a correctly classified, ordered, and parser-compatible release-notes entry.
---

# Release notes

Create one entry using this exact structure:

`## [X.Y.Z] - YYYY-MM-DD`  
`Impact: N`  
one bullet for each pending change  
`<!-- stl-impact: v1 -->`

Use the supplied three-part version without a leading `v`. Use the supplied date in `YYYY-MM-DD` format. The trailer comment must be the final line.

## Classify each change

Prefix every bullet with exactly one impact code: `- [A1]`, for example. Determine the letter and digit independently.

### Choose the letter

Use the first applicable letter in this precedence order:

1. `A` — The change modifies the public API contract: exported names, signatures, accepted argument types, return types, or other published types. New public API is also `A`.
2. `B` — The change affects package import or the runtime behavior or implementation of existing calls without changing their public API contract. Runtime-only refactors, caches, and other internal execution changes are `B` even when their result is unobservable.
3. `C` — The change is confined to build configuration, packaging, tooling, tests, or documentation.

Changing an exported type contract is `A`. Merely making existing, unchanged type information discoverable to development tools is `C`.

If one change spans multiple categories, use the earliest applicable letter: `A` before `B`, and `B` before `C`.

### Choose the digit

Use the first applicable digit in this precedence order:

1. `1` — Breaking: code that correctly used the previous public contract can now fail or produce a different result.
2. `2` — Compatible and externally noticeable: the change adds capability, fixes incorrect behavior, improves stated performance, or otherwise has a visible effect while correct existing usage continues to work.
3. `3` — Unobservable: no externally visible result, contract, artifact, installation behavior, or documented workflow changes.

A bug fix is `2` when it corrects behavior that was already wrong and does not break correct usage. Do not classify it as `1` merely because affected inputs now produce the corrected result.

Classify only the impact stated in the pending change. Do not infer an observable performance improvement merely because an internal cache or optimization was added. If the description promises a measurable improvement, use `2`; if it only says that internal implementation changed while results and signatures remain unchanged, use `3`.

For `C` changes, use `2` when users, packagers, or developers receive a compatible visible change, such as added documentation or changed installation contents. Use `3` for tests or internal migrations explicitly stated to leave installation, artifacts, and workflows unchanged.

If more than one digit seems applicable, use the lowest digit: `1` before `2`, and `2` before `3`.

## Write and order the bullets

Write one concise, past-tense bullet for each pending change. Preserve important identifiers in backticks. Do not merge unrelated changes or invent effects that were not supplied.

Sort bullets by their complete code in ascending order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.

When multiple bullets have the same code, preserve their order from the supplied pending-change list.

## Calculate the impact summary

Set `Impact` to the lowest digit used by any bullet, regardless of its letter. For example, an entry containing digits `2`, `2`, and `3` has `Impact: 2`.

Before returning the entry, verify that every pending change appears once, the bullets are stably sorted by code, the impact number is the minimum bullet digit, and `<!-- stl-impact: v1 -->` is the final line.