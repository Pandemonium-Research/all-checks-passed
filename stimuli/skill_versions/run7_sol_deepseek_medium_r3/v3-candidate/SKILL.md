---
name: impact-log
description: Use this skill to turn a supplied version, date, and list of pending changes into a correctly classified, ordered, and parser-compatible release-notes entry for this project.
---

# Release notes

Produce exactly one entry in this structure:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Description of change.
- [CODE] Description of change.

<!-- stl-impact: v1 -->

Use the supplied three-part version number and date exactly. Write one bullet for every pending change. Do not add any other headings, prose, or comments. The trailer shown above must be the final line.

## Classify each change

Each code contains a letter followed by a digit. Choose the letter and digit independently:

- The letter describes what kind of project interface or behavior changed.
- The digit describes the compatibility impact.

Do not derive the digit from the letter. In particular, an added public API is compatible, while an existing call whose result changes may be breaking.

### Choose the letter

Apply these rules in order:

1. Use `A` when the public API surface changes. This includes:

   - Adding, removing, or renaming an exported name.
   - Changing a public function or method signature.
   - Broadening or narrowing accepted argument types.
   - Changing a documented return type.

2. Otherwise, use `B` when the runtime behavior of an existing public call changes without an API-surface change. This includes changes to returned values, exceptions, side effects, normalization, or formatting.

3. Otherwise, use `C`. This includes internal implementation and performance work with unchanged results, plus build, packaging, supported-environment, tooling, test, and documentation changes.

A change to a returned value is `B`, not `A`, unless the public signature or documented return type also changes. A supported runtime or installation environment is project support, not an exported API, so classify such a change as `C`.

### Choose the digit

Ask what happened to uses that were previously supported and completed successfully:

1. Use `1` if any such use can now fail, require caller changes, return a different value or type, or produce different side effects. This includes removals, narrowed input support, incompatible type changes, and behavior fixes that alter the result of an input that already completed successfully.

2. Otherwise, use `2` if the change adds or repairs capability. This includes new APIs, broader accepted inputs, and making a previously failing or unsupported use succeed.

3. Otherwise, use `3` if supported callers cannot observe a functional difference.

The word “added” does not automatically mean `1`, and the word “fixed” does not automatically mean `2`. Classify the actual before-and-after effect:

- A newly exported API is `A2`.
- A removed exported API is `A1`.
- A broadened accepted argument type is `A2`.
- A changed value for a previously successful call is `B1`.
- A formerly failing or unsupported call that now succeeds is `B2`.
- A removed supported environment is `C1`.
- An internal rewrite with identical behavior is `C3`.

Use only effects stated in the pending change. Do not invent possible incompatibilities.

## Compute the entry impact

Set `Impact` to the lowest digit used by any bullet. For example, an entry containing digits `2`, `2`, and `3` has `Impact: 2`.

## Order and write the bullets

Sort bullets by complete code in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes have the same code, keep their original relative order.

Write each description as a concise sentence stating what changed and, when relevant, how callers are affected. End every bullet with a period.