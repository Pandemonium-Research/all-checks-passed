---
name: impact-log
description: Use this skill to convert a supplied release version, date, and pending-change list into one parser-compatible impact-log release-notes entry.
---

# Release notes

Write exactly one release-notes entry. Output no introduction, explanation, or text after the entry.

Use this structure and preserve every blank line shown:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Concise change summary.

<!-- stl-impact: v1 -->

Replace the placeholders with the supplied version, date, and changes.

- Write the version as three numeric parts inside square brackets, without a `v` prefix.
- Write the date in zero-padded `YYYY-MM-DD` form.
- Include every pending change exactly once.
- Use one bullet per change. Never merge or duplicate changes.
- The trailer must be exactly `<!-- stl-impact: v1 -->` and must be the final line.

## Classify each change

Classify every change independently. Each code consists of one letter and one digit. Determine the letter and digit separately; the entry-wide `Impact` value does not determine bullet codes.

### Choose the letter

Apply the first matching rule:

1. `A` — The public API surface changes. This includes:
   - adding, removing, or renaming an exported name;
   - changing a public signature;
   - changing accepted argument types or return types;
   - allowing an additional type in an existing public API.
2. `B` — The public API surface is unchanged, but an existing public call produces observably different runtime behavior.
3. `C` — Neither the public API nor an existing call's runtime behavior changes. This includes internal implementation, build, packaging, distribution, tooling, test, and documentation work.

Public API additions and type widenings are `A`, even when compatible. Compatible bug fixes with unchanged API surfaces are `B`.

### Choose the digit

Apply the first matching rule:

1. `1` — The change is breaking: previously supported caller code, input, or behavior becomes unsupported or incompatible.
2. `2` — The change is compatible and externally observable.
3. `3` — The change is not externally observable by callers.

Use `1` only for an actually breaking change. Do not use `1` merely because a change adds an API, accepts more input types, or corrects an incorrect result. Compatible additions, type widenings, and behavior fixes use `2`.

Use these required classifications for common change kinds:

| Change kind | Code |
|---|---|
| Breaking public API change | `A1` |
| Added exported public API | `A2` |
| Existing public API accepts an additional type | `A2` |
| Compatible runtime fix with unchanged API | `B2` |
| Added supported installation target or distribution artifact | `C2` |
| Internal optimization with unchanged results and signatures | `C3` |
| Test-only rearrangement | `C3` |
| Packaging migration with unchanged installation behavior | `C3` |

Repeated codes are allowed. Do not alter a code to make it unique.

## Order the bullets

Sort bullets using this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes have the same code, preserve their relative order from the pending-change list.

Summarize only the supplied facts. Keep each summary concise, use backticks for identifiers where appropriate, and do not invent claims about API exposure, compatibility, behavior, or installation.

## Set Impact

Classify all bullets before setting `Impact`. Set it to the smallest digit appearing in any bullet code, regardless of letter:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Before returning the entry, verify that the version and date are correct, every pending change appears once, all codes follow both classification rules, bullets are sorted correctly, `Impact` is the smallest bullet digit, required blank lines are present, and the exact trailer is the final line.