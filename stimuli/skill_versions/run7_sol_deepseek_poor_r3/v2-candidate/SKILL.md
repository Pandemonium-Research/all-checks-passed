---
name: impact-log
description: Use this guide to turn a supplied release version, date, and list of pending project changes into one parser-ready release-notes entry with correctly classified impact markers, ordering, summary, and trailer.
---

# Release notes

Create exactly one release entry from the supplied version, date, and pending changes.

## Required structure

Write these elements in order:

1. `## [VERSION] - YYYY-MM-DD`
2. A blank line.
3. `Impact: DIGIT`
4. A blank line.
5. One list item for each pending change: `- [LETTERDIGIT] Description`
6. A blank line.
7. `<!-- stl-impact: v1 -->`

Use the supplied three-part version and ISO date exactly. Do not add introductory text, closing text, sections, or a colon after a marker.

## Classify each change

Choose the marker letter and digit independently. Classify the actual effect of the change, not its label or intent.

### Choose the letter

Use the first applicable category:

- `A` — The public interface or supported compatibility surface changes. This includes exported names, parameters, signatures, accepted or returned types, public type annotations, and supported runtime versions.
- `B` — The public interface is unchanged, but callers can observe different functional behavior, results, or errors.
- `C` — Neither the public interface nor functional results change. This includes internal implementation, performance or resource-use work, tests, documentation, tooling, and packaging work that preserves installation behavior.

When more than one letter applies, choose the earliest: `A` before `B` before `C`.

Examples of the distinction:

- Adding an optional public parameter is `A`, because the public interface changes.
- Changing results while retaining the same public signature is `B`.
- Replacing an internal algorithm while preserving its interface and results is `C`.

### Choose the digit

Determine whether supported existing callers remain compatible:

- `1` — Breaking. Existing supported code may fail, receive a differently typed value, produce incompatible results, encounter new errors, or require modification.
- `2` — Compatible but observable. The change adds usable functionality, broadens accepted inputs, or fixes a defect while preserving correct use of the existing supported contract.
- `3` — Caller-invisible. The supported runtime contract and functional results remain unchanged.

Use the lowest applicable digit: `1` before `2` before `3`.

Apply these rules carefully:

- Removing or narrowing a supported interface is `1`.
- Changing a public return type is `1`, even when the new type is considered an improvement.
- Changing output or error behavior for ordinary supported inputs is `1` when existing callers could rely on the previous behavior.
- Do not assign `2` merely because a change is described as a fix. Use `2` only when the old behavior was a defect outside the supported contract and correct existing code remains compatible.
- Adding an optional capability without changing existing behavior is `2`.
- A public metadata-only change, such as adding annotations without changing runtime behavior, can be `A3`.
- A performance or resource-use defect fix with unchanged interface and functional results can be `C2`.
- Pure refactoring, tests, documentation, or tooling changes are normally `C3`.

Common marker combinations include:

- `A1` — Breaking public-interface or compatibility change.
- `A2` — Compatible public-interface addition or broadening.
- `A3` — Public-interface metadata change with no runtime effect.
- `B1` — Breaking behavioral change with an unchanged interface.
- `B2` — Compatible behavioral fix or enhancement with an unchanged interface.
- `C2` — Observable non-functional improvement with unchanged interface and results.
- `C3` — Caller-invisible internal or project-maintenance change.

## Write and order the list

Represent every pending change exactly once. Do not combine separate pending changes or split one pending change into multiple items.

Write each item as:

`- [LETTERDIGIT] Concise description`

Use one of the valid markers `[A1]` through `[C3]`, followed by exactly one space and the description.

Sort items in this marker order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

Preserve the supplied order among items that receive the same marker.

## Calculate the summary

Set `Impact` to the lowest digit present in the list-item markers.

For example:

- Any marker ending in `1` makes the summary `Impact: 1`.
- Otherwise, any marker ending in `2` makes the summary `Impact: 2`.
- If every marker ends in `3`, write `Impact: 3`.

Consider only marker digits. Ignore all other numerals, including those in the version, date, descriptions, and trailer.

## Final check

Before returning the entry, verify that:

- The heading contains the supplied version and date exactly.
- Every pending change appears exactly once.
- Each item has the correct letter and digit based on its actual compatibility effect.
- Breaking return-type or supported-behavior changes use digit `1`.
- Compatible additions and contract-preserving fixes use digit `2`.
- Caller-invisible changes use digit `3`.
- Items are sorted by marker while ties retain their supplied order.
- `Impact` is the lowest list-marker digit.
- The trailer is the final line.