---
name: impact-log
description: Use this skill when given a version number, release date, and pending project changes to produce one correctly classified, sorted, and parser-compatible release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every pending change exactly once, with one bullet per change. Do not combine, omit, duplicate, or invent changes.

Use this exact structure, including the blank lines:

    ## [VERSION] - YYYY-MM-DD

    Impact: DIGIT

    - [CODE] Change description.
    - [CODE] Change description.

    <!-- stl-impact: v1 -->

Replace the placeholders with the supplied three-part version, date, impact digit, codes, and descriptions. Do not add text before the heading or after the trailer.

## Classify each change

Each code consists of one letter and one digit. Choose them independently from the actual effect of the change. Do not classify from labels such as “feature,” “fix,” “refactor,” or “breaking.”

### Choose the letter

Use the first matching category:

1. `A` — The exported public API contract changes.
   This includes adding or removing an exported name, changing a public signature, or changing accepted parameter or return types.
2. `B` — The exported public API contract is unchanged, but the result, error, or side effect of an existing call changes.
3. `C` — Neither the exported API contract nor an existing call's runtime behavior changes.
   This includes internal implementation, performance-only work, builds, packaging, distribution, tooling, tests, and documentation.

Apply these distinctions:

- Adding an exported function, class, method, or constant is `A`.
- Allowing a public parameter to accept an additional type is `A`, even if all formerly valid calls behave identically.
- Fixing behavior for an input already supported by the existing public API is `B`, not `A`.
- Changing only an internal implementation while preserving signatures, results, errors, and side effects is `C`.
- Build, installation, platform, interpreter, packaging, and distribution changes are `C`, even when they alter a supported user workflow.

If more than one letter applies to a single change, use this precedence:

`A` before `B` before `C`.

### Choose the digit

Evaluate these questions in order and stop at the first “yes”:

1. Did a previously successful operation or supported workflow become unsuccessful, or does it now produce a different result or side effect? Use `1`.
2. Otherwise, did the change add a compatible capability, or make a previously failing or unsupported operation or workflow succeed? Use `2`.
3. Otherwise, is there no externally observable difference to calls or supported workflows? Use `3`.

Apply these distinctions:

- Removing an API, rejecting formerly valid input, incompatibly changing a signature, or removing a supported environment or installation workflow is `1`.
- Any change to the value returned by a call that previously completed successfully is `1`, even when the new value corrects a bug.
- A compatible exported API addition is `2`.
- Accepting an additional argument type is `2` when existing valid calls remain unaffected.
- Making an already supported call stop raising an error is `2`.
- Adding support for a build target, platform, interpreter, installation method, or distribution artifact is `2`.
- Internal caching or optimization is `3` when signatures, results, errors, and side effects are unchanged.
- A packaging migration is `3` when supported installation behavior is unchanged.
- Test reorganization, tooling-only work, and documentation-only work are `3`.

Do not assume every bug fix is `2`. A fix that changes a previously returned value is `1`; a fix that makes a previously failing supported operation succeed is `2`.

If more than one digit applies to a single change, use this precedence:

`1` before `2` before `3`.

## Sort the bullets

Sort bullets in exactly this code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For bullets with the same code, preserve their order from the supplied pending-change list.

## Set the impact summary

Set `Impact` to the lowest numeric digit appearing in any bullet code, regardless of the letter, bullet order, or number of occurrences.

## Validate the entry

Before returning the entry, verify all of the following:

- The heading is exactly `## [VERSION] - YYYY-MM-DD` using the supplied values.
- A blank line follows the heading.
- The summary is exactly `Impact: DIGIT`.
- A blank line separates the summary from the bullets.
- Every pending change appears exactly once in its own bullet.
- Every bullet begins with `- [CODE]`.
- Every code follows the classification rules.
- The bullets follow the required code order.
- A blank line separates the final bullet from the trailer.
- The trailer is exactly `<!-- stl-impact: v1 -->`.
- The trailer is the final line.