---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one correctly classified, stably sorted, machine-parseable impact-log release-notes entry.
---

# Release notes

Create exactly one release entry. Include every pending change exactly once. Classify each change from its stated user-facing effect, not from implementation effort, filenames, or older release entries.

## Required output

Output only the entry, without a code fence or introductory text:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->

Follow these rules exactly:

- Use the supplied three-part version and date.
- Put the version in square brackets.
- Format the date as `YYYY-MM-DD`.
- Put `Impact: DIGIT` directly below the heading.
- Write one bullet per pending change. Do not combine, split, omit, or duplicate changes.
- Begin every bullet with exactly one classification code in square brackets.
- Preserve the supplied meaning. Do not invent compatibility, behavior, or performance effects.
- Sort bullets in this order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
- Preserve input order among changes with the same code.
- Make `<!-- stl-impact: v1 -->` the final line, with nothing after it.

## Classify each change

Each code contains one letter and one digit. Choose the letter and digit independently.

### Step 1: Choose the letter

Apply these tests in order:

1. Choose `A` when the supported public API contract changes. This includes adding or removing exported names, changing public signatures, widening or narrowing accepted argument types, changing return types, or changing public type definitions.
2. Otherwise, choose `B` when the behavior or runtime performance of existing functionality changes.
3. Otherwise, choose `C` for packaging, environment support, dependencies, build configuration, tooling, tests, documentation, and other work without a runtime behavior or performance effect.

Use these boundaries:

- Adding an exported function, class, method, or constant is `A`.
- Compatibly accepting an additional argument type is `A`.
- Correcting an existing function's result is `B` when its public API contract is unchanged.
- Any runtime optimization is `B`, even when results and signatures are unchanged. This includes changes to caching, deferred or lazy imports, startup time, import time, CPU use, memory use, or latency.
- An internal refactor without a stated runtime behavior or performance effect is `C`.
- Documentation or examples for a public API are `C`; describing an API does not change it.
- Metadata that exposes already-shipped annotations to type checkers is `C`; it does not change the public type definitions.
- Adding or dropping support for a runtime, operating system, platform, or environment is `C`.
- Dependency, packaging, and build changes are `C` unless the pending change explicitly states a runtime behavior or performance effect.
- Vendoring, replacing, adding, removing, or updating a dependency is `C` when supported behavior remains unchanged.
- Migrating packaging or build configuration is `C` when installation support and behavior remain unchanged.

Do not classify runtime caching or import optimizations as `C` merely because their implementation is internal.

### Step 2: Choose the digit

Apply these tests in order:

1. Choose `1` when previously supported callers or environments must change, can fail, lose support, or receive incompatible behavior.
2. Otherwise, choose `2` when users gain a compatible supported capability, corrected behavior, or newly supported environment, packaging, installation, or type-checking functionality.
3. Otherwise, choose `3` when supported results and usage remain unchanged.

The digit measures compatibility and supported caller-facing capability, not whether work was added, improved, modernized, or difficult.

Use these mappings:

- Removed, narrowed, or incompatibly changed public API: `A1`.
- New or compatibly expanded public API: `A2`.
- Incompatible change to existing runtime behavior: `B1`.
- Correction of faulty runtime behavior that preserves valid existing usage: `B2`.
- Runtime performance change with unchanged results and public API: `B3`.
- Dropped runtime, operating system, platform, or environment support: `C1`.
- Added compatible environment, packaging, installation, or type-checking support: `C2`.
- Documentation-only work: `C3`.
- Dependency maintenance with no supported behavior change: `C3`.
- Packaging or build migration with unchanged installation support and behavior: `C3`.
- Tests, tooling, refactoring, or internal reorganization with no supported caller-facing effect: `C3`.

Apply these distinctions exactly:

- API documentation and docstring examples are `C3`, not `A2` or `C2`.
- Metadata that makes existing annotations discoverable to type checkers is `C2`, not `A2` or `C3`.
- Dependency vendoring or replacement with unchanged supported behavior is `C3`, not `C2`.
- Packaging modernization with unchanged installation support and behavior is `C3`, not `C2`.
- A runtime caching change or deferred import with unchanged results is `B3`, not `C3`.
- Do not choose digit `2` merely because something was added or improved.

If a single pending change explicitly states multiple effects, choose the most disruptive applicable letter and digit: prefer `A` over `B` over `C`, and prefer `1` over `2` over `3`.

## Compute the impact summary

Set `Impact` to the lowest digit appearing in any bullet, regardless of letter:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

## Final verification

Before returning the entry, confirm that:

- The version and date exactly match the supplied values.
- Every pending change appears exactly once.
- Public API changes are `A`, runtime behavior or performance changes are `B`, and other project work is `C`.
- Documentation is `C3`, type-checker discoverability metadata is `C2`, unchanged-behavior dependency work is `C3`, unchanged-support packaging migration is `C3`, and runtime optimizations are `B3`.
- Bullets follow the required code order, with input order preserved for ties.
- `Impact` equals the lowest bullet digit.
- The heading, impact line, bullet prefixes, and final HTML comment exactly match the required format.