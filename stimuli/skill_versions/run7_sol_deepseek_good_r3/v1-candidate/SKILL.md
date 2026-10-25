---
name: impact-log
description: Use this skill to turn a release version, release date, and list of pending project changes into a complete, correctly classified release-notes entry in the parseable house impact-log format.
---

# Release notes

Create one entry containing every pending change. Use this exact structure:

## `[version] - YYYY-MM-DD`

`Impact: N`

- `[code]` Change description.
- `[code]` Change description.

`<!-- stl-impact: v1 -->`

Do not include the backticks shown above. Leave one blank line after the heading, after the impact line, and before the trailer. The trailer must be the final line.

## Classify each change

Assign every bullet one two-character code. Determine the letter and digit independently.

### Choose the letter

- **A — Public API:** The change adds, removes, renames, or modifies an exported name, signature, parameter, return type, accepted input type, or other public type.
- **B — Runtime behavior:** The public API is unchanged, but an existing call can produce different runtime behavior or results.
- **C — Non-API work:** The change affects only implementation internals, performance-neutral refactoring, builds, packaging, distribution, tooling, tests, or documentation.

If multiple letters apply, use the earliest letter: **A before B before C**. For example, a compatible expansion of the input types accepted by a public function is A because it changes the public API, even though it also changes runtime behavior.

### Choose the digit

- **1 — Breaking:** Caller code that previously worked can now fail, become invalid, or return a different result that is not a bug fix.
- **2 — Compatible and observable:** The change is additive, fixes incorrect behavior, or otherwise provides a new caller-visible capability while correct existing caller code continues to work.
- **3 — Unobservable to callers:** The change has no caller-visible effect.

Important classification rules:

- Adding a public API is compatible, not breaking: use digit **2**.
- Broadening an accepted public input type is compatible: use digit **2**.
- Fixing incorrect runtime output without changing the API uses digit **2**.
- An implementation-only optimization or refactor with unchanged public behavior uses digit **3**.
- A compatible packaging or distribution improvement that users can take advantage of uses digit **2**.
- Test-suite or tooling reorganization with no caller-visible effect uses digit **3**.
- “New” does not automatically mean digit 1. Use digit 1 only when previously working caller code can break or receive a newly incorrect or intentionally incompatible result.

If multiple digits apply, use the lowest digit: **1 before 2 before 3**.

## Write and order the entry

- Use the supplied three-part version number and date exactly.
- Write one concise bullet for each pending change. Do not omit or merge unrelated changes.
- Begin every bullet with its code in square brackets, such as `[A2]`.
- Sort bullets by code in ascending letter-then-digit order. Preserve the supplied order among bullets with the same code.
- Set `Impact` to the lowest digit used by any bullet, regardless of its letter.
- Write the trailer exactly as `<!-- stl-impact: v1 -->`, with no text or blank lines after it.