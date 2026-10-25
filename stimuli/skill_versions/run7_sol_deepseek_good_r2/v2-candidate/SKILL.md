---
name: impact-log
description: Use this skill to turn a version, release date, and list of pending project changes into a correctly classified, sorted, and parseable release-notes entry in the team's impact-log format.
---

# Release notes

Write one release entry. Include every pending change exactly once, with one bullet per change.

Use this exact layout and preserve every blank line:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Change description.
- [CODE] Change description.

<!-- stl-impact: v1 -->

Replace the placeholders with the supplied version, date, impact digit, codes, and descriptions.

Formatting requirements:

- Use a three-part numeric version such as `1.4.0`.
- Use a date in `YYYY-MM-DD` form.
- Leave one blank line after the heading, after the `Impact` line, and after the final bullet.
- Put no text before the heading or after the trailer.
- Write the trailer exactly as `<!-- stl-impact: v1 -->`.

## Assign each impact code

A code consists of one letter and one digit. Choose the letter and digit separately.

### Choose the letter

- `A` — The exported public API changes. This includes adding or removing an exported name, changing a public signature, or changing accepted argument or return types.
- `B` — The public API contract is unchanged, but the observable runtime behavior of an existing call changes.
- `C` — No caller-visible API or runtime behavior changes. This includes internal implementation work and changes limited to builds, packaging, tooling, tests, or documentation.

Important distinctions:

- A newly exported function, class, method, or constant is `A`, even though adding it is compatible.
- If an existing parameter now accepts an additional kind of value, its accepted public input types have changed, so use `A`.
- If the documented API already accepted an input but the implementation previously failed on it, fixing that behavior is `B`.
- An internal optimization that preserves signatures, outputs, and errors is `C`.

### Choose the digit

Apply these questions in order:

1. Did any previously successful caller-visible operation become unsuccessful or produce a different result? Use `1`.
2. Otherwise, did the change add a compatible capability or make a previously failing or unsupported operation work? Use `2`.
3. Otherwise, if callers cannot observe a difference, use `3`.

A bug fix is not automatically `2`. If a call previously completed successfully but returned an incorrect result, and the fix changes that result, use `1`. Use `2` when the affected operation previously failed or was unsupported and now works.

Do not infer the digit from the letter. In particular:

- A compatible public API addition is normally `A2`, not `A1`.
- A corrected result from an existing successful call is normally `B1`.
- A purely internal change with identical caller-visible behavior is `C3`, not `C2`.

If one pending change matches multiple categories, use the highest-precedence category it matches:

- Letter precedence: `A`, then `B`, then `C`.
- Digit precedence: `1`, then `2`, then `3`.

## Sort and summarize

Sort bullets by code in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple bullets have the same code, keep their original order from the pending-change list.

Set `Impact` to the lowest digit appearing in any bullet code, regardless of the letter.