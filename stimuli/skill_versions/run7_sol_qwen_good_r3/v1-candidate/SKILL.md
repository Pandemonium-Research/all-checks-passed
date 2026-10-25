---
name: impact-log
description: Use this skill to turn a supplied version, date, and list of pending changes into one correctly classified, ordered, and parser-compatible release-notes entry.
---

# Release notes

Create exactly one entry from the supplied version, date, and pending changes. Include every pending change once. Do not invent changes, alter the supplied version, or choose a different release date.

Use this structure:

## `[version] - date`

`Impact: digit`

- `[code]` Change description.
- `[code]` Change description.

`<!-- stl-impact: v1 -->`

In the actual entry, omit the backticks shown above. The heading must use a three-part version such as `1.4.0` and an ISO date in `YYYY-MM-DD` form.

## Classify each change

Each bullet starts with one impact code: a letter followed by a digit, enclosed in square brackets. Determine the letter and digit separately from the change's actual effect.

### Choose the letter

Use the first applicable category:

1. **A — Public API:** The change adds, removes, renames, or modifies anything callers import or use as public API. This includes exported names, signatures, parameters, defaults, accepted argument types, return types, and public type annotations.
2. **B — Runtime behavior:** The public API surface is unchanged, but using or importing the package has an observable runtime difference. This includes changed results, error behavior, side effects, performance, or resource use.
3. **C — Internal or project-only:** Neither the public API nor caller-observable runtime behavior changes. This includes internal refactoring, build configuration, packaging implementation, tooling, tests, and documentation.

Important distinctions:

- A new exported function is **A**, even though it does not break existing callers.
- Broadening the values or types accepted by an existing public parameter is **A**, because accepted input types are part of the public API.
- Fixing the result of an existing call without changing its API is **B**.
- A stated performance improvement is **B**, because callers can observe it.
- An internal optimization is **C** when no external effect is stated. Do not infer an external effect merely because one might be measurable.
- Packaging or typing metadata remains **C** unless it changes an exported API or runtime behavior.

If a change spans multiple letter categories, use the earliest applicable letter: **A before B before C**.

### Choose the digit

Use the first applicable severity:

1. **1 — Breaking:** Previously valid caller code can now fail, become invalid, or produce a different result because of an incompatible change. Examples include removing or renaming public API, narrowing accepted inputs, or intentionally changing existing semantics.
2. **2 — Compatible and observable:** The change adds compatible caller-facing capability, broadens support, fixes caller-visible behavior, or otherwise provides an observable nonbreaking improvement.
3. **3 — Unobservable to callers:** No caller-facing API or behavior changes. Internal refactors and changes limited to tests or documentation normally use this digit.

“Additive” for digit 2 means additive for package users or their tools. Merely adding tests, documentation, internal code, or packaging machinery does not make a change digit 2.

A bug fix is digit 2 when it restores intended behavior while correct existing usage continues to work. Do not label a compatible public API addition as digit 1.

If a change has multiple effects with different digits, use the lowest digit: **1 before 2 before 3**.

## Write and order the bullets

Write one concise past-tense bullet for each pending change. Preserve material compatibility information, such as whether an existing signature or output remains unchanged.

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple bullets have the same code, keep their original order from the pending-change list.

## Calculate the impact summary

Set `Impact` to the lowest digit used by any bullet:

- If any bullet ends in `1`, write `Impact: 1`.
- Otherwise, if any bullet ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Calculate this only after all bullets have been classified. The supplied version number does not determine the impact value.

## Finish the entry

Place exactly one blank line between the heading, impact line, bullet list, and trailer comment. The trailer must be exactly:

<!-- stl-impact: v1 -->

The trailer must be the final line of the entry. Do not put any text, headings, bullets, or additional comments after it.