---
name: impact-log
description: Use this skill when given a version, release date, and pending changes and you need to produce one correctly formatted, classified, sorted, and parser-compatible release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every pending change exactly once, with one bullet per change.

Use this exact structure and preserve every blank line:

    ## [VERSION] - YYYY-MM-DD

    Impact: DIGIT

    - [CODE] Change description.
    - [CODE] Change description.

    <!-- stl-impact: v1 -->

Replace the placeholders with the supplied values. Use the supplied three-part numeric version and date. Do not write anything before the heading or after the trailer.

## Classify each change

Each code contains a letter and a digit. Determine the letter and digit independently from what changed, not from labels such as “feature,” “fix,” or “refactor.”

### Choose the letter

Use the first matching category:

1. `A` — The exported public API contract changes.
   This includes adding or removing an exported name, changing a public signature, or changing accepted argument or return types.
2. `B` — The public API contract is unchanged, but an existing call changes its result, error, or side effect.
3. `C` — Neither the exported API contract nor an existing call's runtime behavior changes.
   This includes internal implementation, builds, packaging, distribution, tooling, tests, and documentation.

Therefore:

- A newly exported function, class, method, or constant is `A`.
- Allowing a public parameter to accept an additional type is `A`, not `B`.
- Fixing behavior for an input already covered by the public API is `B`.
- An optimization that preserves signatures, results, errors, and side effects is `C`.
- Installation and distribution changes are `C`, even when users can observe a new supported installation option.

If multiple letters apply, use this precedence: `A`, then `B`, then `C`.

### Choose the digit

Evaluate these questions in order and stop at the first “yes”:

1. Did something that previously succeeded now fail, or now produce a different result or side effect? Use `1`.
2. Otherwise, was a compatible capability added, or did something previously failing or unsupported become successful or supported? Use `2`.
3. Otherwise, is there no externally observable change to calls, installation, distribution, or supported workflows? Use `3`.

Apply these rules carefully:

- A compatible public API addition is `A2`, not `A1`.
- Accepting an additional argument type is `A2` when existing valid calls are unaffected.
- Removing an API, rejecting formerly valid input, or incompatibly changing a signature is `A1`.
- Correcting a wrong result from a call that previously completed successfully is `B1`, even when described as a bug fix.
- Making an existing supported call stop raising an error is `B2`.
- Adding support for a new build, platform, interpreter, installation method, or distribution artifact is `C2`.
- Internal caching is `C3` when results, errors, side effects, and signatures are unchanged.
- A packaging migration is `C3` when installation behavior and supported environments are unchanged.
- Moving or reorganizing tests is `C3`.

If multiple digits apply, use this precedence: `1`, then `2`, then `3`.

## Sort the bullets

Sort bullets by code in exactly this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple bullets have the same code, preserve their order from the pending-change list.

Do not omit, combine, duplicate, or invent changes.

## Set the impact summary

Set `Impact` to the lowest numeric digit appearing in any bullet code, regardless of its letter.

For example, if an entry contains digits `2`, `1`, and `3`, write `Impact: 1`.

## Validate the finished entry

Before returning it, confirm that:

- The heading is exactly `## [VERSION] - YYYY-MM-DD`.
- There is a blank line after the heading.
- The summary is exactly `Impact: DIGIT`.
- There is a blank line before the first bullet.
- Every pending change appears once in its own bullet.
- Every bullet begins with `- [CODE]`.
- The bullets follow the required code order.
- There is a blank line before the trailer.
- The trailer is exactly `<!-- stl-impact: v1 -->`.
- The trailer is the final line.