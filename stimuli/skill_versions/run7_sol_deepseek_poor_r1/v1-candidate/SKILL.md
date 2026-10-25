---
name: impact-log
description: Use this document to turn a release version, date, and list of pending changes into a correctly classified, parser-compatible release-notes entry.
---

# Release notes

Create one entry using this exact structure:

## Entry structure

1. Write the heading as:

   `## [<version>] - <YYYY-MM-DD>`

   Use the supplied version and date exactly. Keep the version in square brackets.

2. Leave one blank line, then write:

   `Impact: <digit>`

   The digit must be `1`, `2`, or `3`. It is the lowest digit used in any change marker. Consider only change markers; ignore digits in the version, date, descriptions, and trailer.

3. Leave one blank line, then write one bullet for every pending change:

   `- [<letter><digit>] <description>`

   The square brackets are required. Do not put a colon after the marker.

4. Leave one blank line after the final bullet, then add this exact trailer:

   `<!-- stl-impact: v1 -->`

Do not add introductory or closing text.

## Classify each change

Classify the letter and digit independently.

### Choose the letter

The letter identifies the part of the project changed:

- `A` — Public API or caller-facing contract: exported names, function or method signatures, accepted argument types, return types, or other supported interfaces.
- `B` — Package runtime implementation without a public API change. This includes runtime bug fixes, algorithm changes, and internal performance work.
- `C` — Non-runtime project support: build configuration, packaging, development tools, tests, or documentation.

If a change affects more than one category, use the earliest letter: `A` before `B` before `C`.

### Choose the digit

The digit identifies the effect on callers:

- `1` — Breaking. Correct code using the previously supported contract may fail, produce incompatible results, or require modification after upgrading.
- `2` — Compatible and caller-visible. This includes additive APIs, broadened accepted inputs, and bug fixes that restore intended behavior without requiring correct existing callers to change.
- `3` — Not caller-visible. The public contract and caller-observable results remain unchanged.

Do not classify every changed result as breaking. A correction to defective behavior is `2` when the supported contract remains compatible; use `1` when previously supported, correct caller code must change.

If more than one digit could apply, choose the lower digit: `1` before `2` before `3`.

## Write and order the bullets

- Preserve every pending change exactly once.
- Do not merge separate pending changes.
- Do not split one pending change into multiple bullets.
- Describe the change clearly without inventing effects not present in the input.
- Sort bullets by marker: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
- Preserve the supplied order when multiple changes have the same marker.

Before finishing, verify that every marker is square-bracketed, the `Impact` value equals the lowest marker digit, and the trailer is the final line.