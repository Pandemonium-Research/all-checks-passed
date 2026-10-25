---
name: impact-log
description: Use this skill to turn a supplied version, release date, and list of pending project changes into a classified, sorted, and parser-compatible release-not notes entry.
---

# Release notes

Write one release entry. Include every pending change exactly once, using one bullet for each change.

The finished entry must have this exact structure:

    ## [VERSION] - YYYY-MM-DD

    Impact: DIGIT

    - [CODE] Change description.
    - [CODE] Change description.

    <!-- stl-impact: v1 -->

Use the supplied three-part version and date. Preserve the blank lines shown. Do not add text before the heading or after the trailer.

## Classify each change

Each code contains one letter and one digit. Determine them independently.

### Choose the letter

- `A` — The exported public API changes. This includes adding or removing an exported name, changing a public signature, or changing accepted argument or return types.
- `B` — The public API contract stays the same, but the runtime behavior of an existing call changes, including its result, error, or side effect.
- `C` — Neither the exported API nor an existing call's runtime behavior changes. Use this for internal implementation, builds, packaging, distribution, tooling, tests, and documentation.

Apply these rules:

- A newly exported function, class, method, or constant is `A`.
- Expanding the types accepted by a public parameter is `A`, even when existing calls are unaffected.
- Fixing an implementation for an input that the public API already supported is `B`.
- An optimization that preserves signatures, results, errors, and side effects is `C`.
- Installation and distribution changes are `C`, even when they add or remove a supported installation capability.

If several letters appear applicable, use this precedence: `A`, then `B`, then `C`.

### Choose the digit

Ask these questions in order:

1. Did a previously successful operation or supported workflow become unsuccessful or produce a different result? Use `1`.
2. Otherwise, did the change add a compatible capability or make a previously failing or unsupported operation or workflow succeed? Use `2`.
3. Otherwise, is there no externally observable difference? Use `3`.

Important distinctions:

- A compatible public API addition is normally `A2`.
- A newly accepted argument type is normally `A2`.
- Correcting the wrong result of a call that previously completed successfully is `B1`, not `B2`.
- Making an already supported call stop failing is normally `B2`.
- Adding a build, installation, or distribution capability is normally `C2`.
- Internal caching, packaging migrations with unchanged installation behavior, and test reorganization are normally `C3`.

If several digits appear applicable, use this precedence: `1`, then `2`, then `3`.

## Sort and summarize

Sort bullets in this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For bullets with the same code, preserve their order from the pending-change list.

Set `Impact` to the lowest numeric digit used by any bullet, regardless of its letter.

Write the trailer exactly as `<!-- stl-impact: v1 -->`. It must be the final line.