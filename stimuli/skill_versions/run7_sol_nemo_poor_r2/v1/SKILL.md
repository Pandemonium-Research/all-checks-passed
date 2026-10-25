---
name: impact-log
description: Instructions for converting a release version, date, and list of pending changes into a correctly classified, sorted, parser-compatible release notes entry.
---

# Release notes

Create one entry using this exact structure:

## [VERSION] - YYYY-MM-DD
Impact: LOWEST_DIGIT

- [A1] Change description.
- [A2] Change description.
- [B2] Change description.
- [C3] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders and example lines with the supplied release information and pending changes.

## Procedure

1. Write the header as a second-level Markdown heading:

   `## [VERSION] - YYYY-MM-DD`

   Use the supplied three-part version number inside square brackets and the supplied date in year-month-day format.

2. Classify every pending change with one letter and one digit, using the rules below.

3. Write exactly one bullet for each pending change. Do not combine changes or split one change across multiple bullets.

4. Start every bullet with the marker in square brackets:

   `- [LETTERDIGIT] Change description.`

   Do not write the marker without brackets, and do not add a colon after it.

5. Sort the bullets by marker in ascending order: A before B before C, and within each letter, 1 before 2 before 3. Preserve the supplied order when multiple changes have the same marker.

6. Set `Impact` to the lowest digit assigned to any bullet. It is not the number of changes and does not depend on the letters.

7. Put `<!-- stl-impact: v1 -->` after the final bullet, at the very bottom of the entry.

## Choose the letter

Choose the letter according to the affected surface:

- `A` — The package's public API is affected, including exported names, function or method signatures, accepted argument types, return types, or shipped typing information.
- `B` — An existing public call behaves differently at runtime while its public API remains unchanged. This includes compatible bug fixes and observable performance or behavior changes.
- `C` — No caller-visible package behavior or public API is affected. This includes internal implementation changes, builds, packaging, distribution artifacts, tooling, tests, and documentation.

If more than one letter applies, use the earliest letter: `A` over `B` over `C`.

Adding a public function is `A`, even though it is compatible. Changing a documented accepted argument type is also `A`. Documentation-only work is `C`, and an internal refactor with unchanged results and signatures is `C`.

## Choose the digit

Choose the digit independently of the letter:

- `1` — Breaking: caller code that previously worked can now fail or return a different result.
- `2` — Compatible but caller-visible: the change is additive or fixes behavior while correct existing caller code remains unaffected.
- `3` — Unobservable to callers: no caller can observe a difference.

If more than one digit could apply, use the lowest digit: `1` over `2` over `3`.

An added public API normally uses digit `2`, not `1`. A compatible runtime bug fix uses digit `2`. Documentation, tests, packaging work, and behavior-preserving internal changes normally use digit `3`.

## Final check

Before submitting, verify all of the following:

- The header begins with `##`.
- The version is in square brackets.
- The date uses `YYYY-MM-DD`.
- `Impact` equals the lowest marker digit in the bullets.
- Every pending change appears exactly once.
- Every bullet begins with a bracketed marker such as `[A2]`.
- No marker is followed by a colon.
- The bullets are sorted by letter and then digit.
- The trailer is present exactly as written and is the final line.