---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one correctly classified, stably sorted, machine-parseable impact-log release-notes entry.
---

# Release notes

Create exactly one release entry containing every pending change exactly once. Classify each change from its stated effect, regardless of implementation location, effort, or wording in older release notes.

## Required output

Output only the release entry. Do not add a code fence, introduction, explanation, or text after the final comment.

Use this exact structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->

Requirements:

- Copy the supplied three-part version and release date exactly.
- Begin the heading with `## ` and enclose the version in square brackets.
- Format the date as `YYYY-MM-DD`.
- Put `Impact: DIGIT` immediately below the heading.
- Write exactly one bullet for each pending change. Do not combine, split, omit, or duplicate changes.
- Begin each bullet with exactly one code in square brackets.
- Preserve the supplied meaning. Do not invent API, compatibility, behavior, support, or performance effects.
- Sort bullets by code in this order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
- When multiple changes have the same code, preserve their order from the pending-change list.
- Make `<!-- stl-impact: v1 -->` the final line, with nothing after it.

## Classification procedure

A code contains one letter and one digit. Determine the letter first and the digit second. Do not infer the digit from the letter.

### Step 1: Choose the letter

Apply these tests in order and stop at the first match:

1. Choose `A` if the supported public API contract changes.
2. Otherwise, choose `B` if the behavior or runtime performance of existing functionality changes.
3. Otherwise, choose `C`.

Use `A` for changes such as:

- Adding or removing an exported function, class, method, constant, or other public name.
- Changing a public signature.
- Widening or narrowing accepted argument types.
- Changing return types or public type definitions.

Use `B` for changes such as:

- Correcting an existing function's result without changing its public API contract.
- Incompatibly changing existing runtime behavior without changing the public API.
- Changing runtime performance while results and public API remain unchanged.
- Adding or changing caching, lazy loading, or deferred imports to improve import time, startup time, CPU use, memory use, throughput, or latency.

Runtime optimizations are `B` even when their implementation is entirely internal.

Use `C` for changes such as:

- Adding or dropping runtime, operating-system, platform, or environment support.
- Packaging, installation, build configuration, dependency, tooling, test, documentation, or internal-reorganization work with no stated runtime behavior or performance effect.
- Documentation or examples that describe an existing public API.
- Metadata that makes already-shipped annotations discoverable by type checkers.
- Vendoring, replacing, adding, removing, or updating a dependency when supported behavior remains unchanged.
- Migrating packaging or build configuration when installation support and behavior remain unchanged.

Documentation about an API is not an API-contract change. Type-checker discovery metadata is not itself a public type-definition change.

### Step 2: Choose the digit

Apply these tests in order and stop at the first match:

1. Choose `1` if previously supported callers or environments must change, can fail, lose support, or receive incompatible behavior.
2. Otherwise, choose `2` if users gain compatible supported capability, corrected behavior, or newly supported environment, packaging, installation, or type-checking functionality.
3. Otherwise, choose `3`.

The digit measures compatibility and supported capability. It does not measure implementation effort, whether code was added, or whether the change is described as an improvement.

Use these mappings:

| Effect | Code |
|---|---|
| Removed, narrowed, or incompatibly changed public API | `A1` |
| New or compatibly expanded public API | `A2` |
| Incompatible change to existing runtime behavior | `B1` |
| Correction of faulty runtime behavior that preserves valid existing usage | `B2` |
| Runtime performance change with unchanged results and public API | `B3` |
| Dropped runtime, operating-system, platform, or environment support | `C1` |
| Added compatible environment, packaging, installation, or type-checking support | `C2` |
| Documentation-only work | `C3` |
| Dependency maintenance with no supported behavior change | `C3` |
| Packaging or build migration with unchanged installation support and behavior | `C3` |
| Tests, tooling, refactoring, or reorganization with no supported caller-facing effect | `C3` |

Apply these distinctions exactly:

- API documentation and docstring examples are `C3`, not `A2` or `C2`.
- Metadata that makes existing annotations discoverable to type checkers is `C2`, not `A2` or `C3`.
- Dependency vendoring or replacement with unchanged supported behavior is `C3`, not `C2`.
- Packaging modernization with unchanged installation support and behavior is `C3`, not `C2`.
- Runtime caching and deferred-import optimizations with unchanged results are `B3`, not `C3`.
- Do not choose digit `2` merely because something was added, improved, modernized, or made faster.

If one pending change explicitly contains multiple effects, use the most disruptive applicable classification: prefer `A` over `B` over `C`, and prefer digit `1` over `2` over `3`.

## Compute the impact summary

After classifying every bullet, set `Impact` to the lowest digit appearing in any code, regardless of letter:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

## Final verification

Before returning the entry, verify all of the following:

- The version and date exactly match the supplied values.
- Every pending change appears once and only once.
- Public API changes use `A`.
- Existing runtime behavior and performance changes use `B`.
- Other project work uses `C`.
- Documentation is `C3`.
- Type-checker discoverability metadata is `C2`.
- Unchanged-behavior dependency work is `C3`.
- Unchanged-support packaging migration is `C3`.
- Runtime optimizations are `B3` when results and public API are unchanged.
- Bullets follow the required code order and same-code ties retain input order.
- `Impact` equals the lowest digit used by any bullet.
- The heading, impact line, bullet prefixes, and final HTML comment exactly match the required format.