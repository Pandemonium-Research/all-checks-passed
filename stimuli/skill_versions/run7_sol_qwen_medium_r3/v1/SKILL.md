---
name: impact-log
description: Use this skill to turn a version, release date, and list of pending project changes into a correctly classified, sorted, and machine-parseable impact-log release-notes entry.
---

# Release notes

Create one entry containing every pending change exactly once. Do not invent changes or copy formatting from older entries; some older entries use obsolete syntax.

Use this exact structure:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace the placeholders as follows:

- `VERSION` is the supplied three-part version number.
- `YYYY-MM-DD` is the supplied date in ISO format.
- Each pending change becomes one bullet.
- `CODE` is one letter followed by one digit, selected using the rules below.
- `DIGIT` is the lowest digit used by any bullet.
- The trailer must be exactly `<!-- stl-impact: v1 -->`. It must be the final line, with no content after it.

## Choose the letter

Choose the first applicable letter:

1. `A` — The public API contract changes. This includes exported names, function or method signatures, parameters, accepted argument types, return types, or other public types. Both additions and removals belong here.
2. `B` — The observable runtime behavior of an existing public call changes without changing its public API contract. This includes results, exceptions, side effects, or an explicitly user-facing performance change.
3. `C` — The change is limited to build configuration, packaging, dependencies, tooling, tests, documentation, type-checker integration, or internal implementation details.

If more than one letter appears applicable, use the earliest letter: `A` before `B` before `C`.

Important distinctions:

- Broadening an existing API to accept another public input type is `A`, because the accepted-type contract changed.
- A correction to an existing call's behavior is `B` when its signature and public types are unchanged.
- Shipped type-checker metadata is `C` unless it changes the actual declared public types.
- A build-system or dependency change is `C`, even when installation still succeeds.
- An implementation-only refactor is `C` when the public API and runtime behavior are unchanged.

## Choose the digit

Choose the digit independently of the letter:

1. `1` — Breaking. Supported caller code or a supported external workflow must change, can now fail, or no longer receives the behavior promised by the public contract.
2. `2` — Externally visible but backward-compatible. Use this for additions, compatible fixes, documented performance improvements, documentation changes, type-checker integration, and compatible build, packaging, or dependency changes.
3. `3` — Strictly internal and externally unobservable. Use this only when the public API, runtime results, exceptions, side effects, supported workflows, shipped artifacts, documentation, and user-facing performance claims are all unchanged.

A bug fix is normally digit `2`, even though it changes an incorrect result. Use digit `1` only when the fix breaks supported or documented behavior, not merely because the old buggy result was different.

Packaging, dependency, documentation, and tooling changes are externally visible and therefore normally digit `2`. Reserve digit `3` for changes that users and downstream tools cannot observe.

If two digits remain genuinely applicable after applying these definitions, choose the lower, more disruptive digit.

## Write and order the bullets

Write each bullet as:

```text
- [LETTERDIGIT] Concise description of the change.
```

Preserve the facts supplied for the pending change. State compatibility or unchanged behavior only when the input supports that claim.

Sort bullets by code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

For bullets with the same code, preserve their order from the pending-changes list.

## Calculate the summary

Set `Impact` to the lowest digit appearing in any bullet, regardless of its letter.

For example, if an entry contains digits `2`, `2`, and `3`, write:

```text
Impact: 2
```

Place the `Impact` line immediately below the release heading. Place the exact HTML trailer immediately after the final bullet, and ensure it remains the last line.