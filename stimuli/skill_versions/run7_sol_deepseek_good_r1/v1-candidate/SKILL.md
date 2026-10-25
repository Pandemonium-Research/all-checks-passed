---
name: impact-log
description: Use this skill to turn a release version, date, and list of pending changes into a correctly classified, sorted, parser-compatible release notes entry in the project's impact-log format.
---

# Release notes

Create one entry using this exact structure:

## [`VERSION`] - `YYYY-MM-DD`

Impact: `DIGIT`

- [`CODE`] Change summary.
- [`CODE`] Change summary.

<!-- stl-impact: v1 -->

Replace the placeholders as follows:

- `VERSION` must have three numeric parts, such as `1.4.0`.
- The date must be zero-padded and use year-month-day order.
- `DIGIT` must be the lowest digit used by any bullet.
- Each `CODE` consists of one letter and one digit, classified independently using the rules below.
- Include every pending change exactly once.
- Keep the blank lines shown in the structure.
- The trailer must be exactly `<!-- stl-impact: v1 -->` and must be the entry's final line.

## Classify the letter

Apply these rules in order:

1. Use `A` when the public API surface changes. This includes:
   - adding, removing, or renaming an exported name;
   - changing a public function or method signature;
   - changing accepted argument types or return types;
   - widening a public API to accept an additional type.

   Public API additions and compatible type widenings are still `A`; they are usually `A2`, not `A1`.

2. Otherwise, use `B` when an existing public call keeps the same API surface but its observable runtime behavior changes. Bug fixes that change an incorrect result are normally `B2`.

3. Otherwise, use `C`. This includes:
   - internal implementation changes whose results and public API remain unchanged;
   - build and packaging work;
   - tooling, tests, and documentation.

If more than one letter applies, use the earliest letter: `A` before `B`, and `B` before `C`.

## Classify the digit

Choose the digit separately from the letter:

1. Use `1` for a breaking change: previously valid caller code can fail, or can receive a different result that is not a compatible bug fix.

2. Use `2` for a compatible, externally observable improvement. This includes:
   - additive public APIs;
   - widening accepted public types;
   - compatible bug fixes;
   - newly supported installation targets or distributable artifacts.

3. Use `3` when callers cannot observe the change. This includes internal refactoring, unchanged-result optimizations, test rearrangement, documentation work, and packaging migrations that do not alter installation behavior.

If several digits could apply, use the lowest digit: `1` before `2`, and `2` before `3`.

The letter does not determine the digit. Codes such as `A2`, `B2`, and `C2` are valid and common.

## Order and summarize the bullets

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Multiple bullets may have the same code. Keep their original relative order when their codes are equal.

Write each bullet as a concise description of the change. Put identifiers in backticks when appropriate. Do not add compatibility claims that are not supported by the pending-change information.

Before finishing, verify that:

- every pending change appears once;
- every code follows the classification rules;
- the bullets are sorted by code;
- the `Impact` value equals the lowest bullet digit;
- the trailer is exact and no content follows it.