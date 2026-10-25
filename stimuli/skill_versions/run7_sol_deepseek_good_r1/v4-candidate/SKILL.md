---
name: impact-log
description: Use this document to convert a supplied release version, date, and pending-change list into one correctly classified, sorted, parser-compatible release notes entry.
---

# Release notes

Produce exactly one entry with this structure, replacing the uppercase placeholders:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Concise change summary.
- [CODE] Concise change summary.

<!-- stl-impact: v1 -->

Formatting requirements:

- Write the supplied version as three numeric parts, such as `1.4.0`, inside square brackets.
- Write the supplied date in zero-padded `YYYY-MM-DD` form.
- Preserve every blank line shown in the structure.
- Include every pending change exactly once. Do not omit, duplicate, or combine changes.
- End with exactly `<!-- stl-impact: v1 -->`. Write nothing after it.

## Classify each change

Assign each change a two-character code: one letter followed by one digit. Choose the letter and digit independently.

### Choose the letter

Apply these rules in order:

1. Use `A` when the public API surface changes. This includes:
   - adding, removing, or renaming an exported name;
   - changing a public signature;
   - changing accepted argument types or return types;
   - allowing an additional type in an existing public API.

   Additions and type widenings are `A` even when fully compatible.

2. Otherwise, use `B` when the public API surface is unchanged but an existing public call produces observably different runtime behavior. Compatible bug fixes normally use `B`.

3. Otherwise, use `C`. This includes internal implementation work, build and packaging changes, distribution artifacts, tooling, tests, and documentation.

Letter precedence is `A`, then `B`, then `C`.

### Choose the digit

Apply these rules in order:

1. Use `1` only when the change is breaking: code using a previously supported API can fail, stop compiling, or receive an incompatible result.

   Never use `1` merely because a change adds an API, accepts more input types, or corrects previously incorrect behavior. A changed result from a compatible bug fix is not automatically breaking.

2. Otherwise, use `2` when the change is compatible and externally observable. This includes:
   - adding a public API;
   - widening the accepted types of a public API;
   - compatibly correcting runtime behavior;
   - adding a supported installation target or distributable artifact.

3. Otherwise, use `3` when callers cannot observe the change. This includes:
   - caching or optimization with unchanged results and signatures;
   - internal refactoring;
   - test or documentation changes;
   - packaging migrations that leave installation behavior unchanged.

Digit precedence is `1`, then `2`, then `3`.

Use these mappings as classification checks:

| Change kind | Code |
|---|---|
| Breaking public API change | `A1` |
| Added public API | `A2` |
| Public API accepts an additional type | `A2` |
| Compatible runtime correction with unchanged API | `B2` |
| New supported distribution artifact | `C2` |
| Unchanged-result internal optimization | `C3` |
| Test rearrangement or behavior-preserving packaging migration | `C3` |

Do not choose a bullet's digit from the entry-wide `Impact` value. Classify all bullets first, then calculate `Impact`.

## Order and summarize

Sort bullets in this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Repeated codes are allowed. When multiple changes have the same code, preserve their relative order from the pending-change list.

Summarize only the supplied facts. Keep each summary concise, format identifiers with backticks where appropriate, and do not invent API, behavior, or compatibility claims.

## Set Impact

Set `Impact` to the lowest digit appearing in any bullet code, regardless of letter:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Before returning the entry, verify that every pending change appears exactly once, every code follows both classification rules, the bullets are correctly sorted, `Impact` is the lowest bullet digit, all required blank lines are present, and the trailer is the final line.