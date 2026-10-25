---
name: impact-log
description: Use when given a release version, date, and pending changes to produce one classified, sorted, parser-compatible release-notes entry for this project.
---

# Release notes

Produce exactly one entry in this form:

    ## [VERSION] - YYYY-MM-DD
    Impact: DIGIT
    - [CODE] Past-tense description of one change.
    <!-- stl-impact: v1 -->

Use the supplied version and date. Include every pending change exactly once. Do not add text before the heading or after the trailer.

## Assign each code

Classify each change independently. Assign one letter and one digit.

### Choose the letter

Use the first applicable category:

1. `A` — The public API contract itself changes: exported names, call signatures, accepted argument types, return types, or declared public types.
2. `B` — The functional runtime behavior of an existing call changes without a public API change, including a different result, error, or side effect.
3. `C` — Only implementation or project details change, including performance, caching, import strategy, dependencies, vendoring, packaging metadata, build tooling, tests, or documentation.

Use `A` before `B` and `B` before `C` when more than one category applies.

Apply these boundaries:

- Adding a public export or accepting a new argument type is `A`.
- Packaging metadata that only makes unchanged, already-shipped annotations discoverable to type checkers is `C`, not `A`.
- Correcting an existing call's result, error, or side effect without changing its API is `B`.
- Timing, memory use, deferred imports, and internal cache strategy are `C` when results, errors, side effects, and public API remain unchanged.
- Dependency or packaging work is `C` when it does not cause an `A` or `B` change.
- Documentation-only and test-only work is `C`.

### Choose the digit

Use the first applicable level:

1. `1` — Breaking. Supported, valid existing usage may stop working or become incompatible.
2. `2` — Compatible and observable. A supported capability is added or incorrect behavior is fixed while valid existing usage remains supported.
3. `3` — No supported caller-visible API, functional behavior, or workflow changes.

Use `1` before `2` and `2` before `3` when more than one level applies.

Apply these boundaries:

- A compatible bug fix is `2`, even though the corrected result differs from the previous incorrect result.
- A compatible new public API capability is `2`.
- Packaging metadata that newly enables a supported development-tool capability is `2`, even when the runtime API is unchanged.
- Pure performance, import, caching, or other internal implementation changes are `3` when functional behavior is unchanged.
- Dependency or packaging reorganizations are `3` when supported installation and use remain unchanged.
- Documentation-only and test-only changes are `3`.

## Write and order the entry

Write one concise, past-tense bullet for each supplied change. Include compatibility information provided with the change, but do not invent consequences.

Sort bullets by complete code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied order among bullets with the same code unless one change clearly depends on another.

Set `Impact:` to the lowest digit used by any bullet. Derive it from the completed codes, not from the version number.

The final line must be exactly:

<!-- stl-impact: v1 -->