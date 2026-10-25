---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one correctly classified, stably sorted, machine-parseable impact-log release-notes entry.
---

# Release notes

Create exactly one release entry containing every pending change exactly once. Classify each change by its stated effect on users, not by the files changed, implementation effort, or wording of older entries.

## Required output

Output only the entry, without a code fence or introductory text:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->

Follow these rules exactly:

- Use the supplied version and date.
- Begin the heading with `## ` and enclose the three-part version in square brackets.
- Format the date as `YYYY-MM-DD`.
- Put `Impact: DIGIT` directly below the heading.
- Write one bullet per pending change; do not combine, split, omit, or duplicate changes.
- Begin each bullet with exactly one classification code in square brackets.
- Preserve the supplied meaning. Do not invent behavior, compatibility, or performance effects.
- Sort bullets in this order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
- For changes with the same code, preserve their order from the pending-change list.
- Make `<!-- stl-impact: v1 -->` the final line, with nothing after it.

## Classify each change

Each code contains one letter and one digit. Determine the letter first, then determine the digit independently.

### Step 1: Choose the letter

Apply these tests in order and stop at the first match:

1. Choose `A` if the supported public API contract changes. This includes exported names, public signatures, accepted argument types, return types, or public type definitions.
2. Otherwise, choose `B` if execution of existing runtime functionality changes in behavior or performance.
3. Otherwise, choose `C`.

Use these boundaries:

- A new exported function, class, method, or constant is `A`.
- Widening or narrowing a public function's accepted arguments is `A`.
- Correcting the result of an existing function is `B` when its public API contract is unchanged.
- Runtime performance work is `B`, including changes to import time, startup time, caching, CPU use, memory use, or latency, even when results and signatures are unchanged.
- Documentation for a public API is `C`; describing an API does not change it.
- Metadata that makes already-existing annotations visible to type checkers is `C`; it does not change the annotations themselves.
- Adding, dropping, or changing supported runtimes, operating systems, or platforms is `C`.
- Dependency, packaging, build, tooling, test, and internal refactoring work is `C` unless the pending change explicitly states a runtime behavior or performance effect.
- Changing how a dependency is obtained, including vendoring or replacement, is `C` when supported runtime behavior remains unchanged.
- Migrating build or packaging configuration is `C` when installation support and behavior remain unchanged.

### Step 2: Choose the digit

Apply these tests in order and stop at the first match:

1. Choose `1` if previously supported callers or environments must change, can fail, lose support, or receive incompatible behavior.
2. Otherwise, choose `2` if users gain a compatible supported capability, corrected behavior, or newly supported environment, packaging, installation, or type-checking functionality.
3. Otherwise, choose `3` because supported results and usage remain unchanged.

The digit measures compatibility and supported caller-facing effect, not whether work was added, improved, or difficult.

Use these mappings:

- Removed, narrowed, or incompatibly changed public API: `A1`.
- New or compatibly expanded public API: `A2`.
- Incompatible change to existing runtime behavior: `B1`.
- Correction of faulty runtime behavior without invalidating correct existing usage: `B2`.
- Runtime performance change with unchanged results and API: `B3`.
- Dropped runtime, operating system, platform, or environment support: `C1`.
- Added compatible environment, packaging, installation, or type-checking support: `C2`.
- Documentation-only changes: `C3`.
- Dependency maintenance with no supported behavior change: `C3`.
- Build or packaging migration with unchanged installation support and behavior: `C3`.
- Tests, tooling, refactoring, and internal reorganization with no supported caller-facing effect: `C3`.

Do not choose digit `2` merely because something was added or improved. In particular:

- Added documentation remains `C3`.
- Dependency vendoring or replacement remains `C3` when behavior is unchanged.
- Packaging modernization remains `C3` when support and installation behavior are unchanged.
- Metadata that enables type checkers to discover shipped annotations is `C2`.
- A runtime optimization with unchanged results is `B3`, not `C3`.

If one pending change explicitly contains multiple effects, use the most disruptive applicable classification: prefer `A` over `B` over `C`, and prefer `1` over `2` over `3`.

## Compute the impact summary

Set `Impact` to the lowest digit used by any bullet, regardless of letter:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

## Final verification

Before returning the entry, confirm that:

- The version and date match the supplied values.
- Every pending change appears exactly once.
- Each letter follows the ordered `A`, then `B`, then `C` tests.
- Each digit reflects compatibility and supported capability, not implementation effort.
- Runtime performance changes are `B3` when results are unchanged.
- Compatible support additions are `C2`.
- Documentation, dependency maintenance, and unchanged-support packaging migrations are `C3`.
- Bullets follow the required code order and same-code ties retain input order.
- `Impact` equals the lowest bullet digit.
- The heading, impact line, bullet prefixes, and final HTML comment exactly match the required format.