---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one correctly classified, sorted, and machine-parseable impact-log release-notes entry.
---

# Release notes

Create one release entry containing every pending change exactly once. Classify each change by its effect, not by the files or implementation involved. Do not imitate older entries; follow only the rules below.

## Required output

Use exactly this structure:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->

Requirements:

- Begin the heading with `## `.
- Put the three-part version inside square brackets.
- Write the date as `YYYY-MM-DD`.
- Put `Impact: DIGIT` immediately below the heading.
- Write one pending change per bullet.
- Begin every bullet with its classification code in square brackets.
- Sort bullets in this order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
- For bullets with the same code, preserve their order from the pending-change list.
- Make `<!-- stl-impact: v1 -->` the final line, with nothing after it.

## Classify each change

Each code contains one letter and one digit. Select the letter and digit independently.

### Select the letter

Use the first applicable category:

1. `A` — The supported public API changes: exported names, public signatures, accepted argument types, return types, or public type definitions.
2. `B` — Existing runtime functionality changes in behavior or performance, without changing the public API.
3. `C` — The change affects neither the public API nor existing runtime behavior or performance. This includes packaging, supported environments, dependencies, tooling, tests, and documentation.

Apply these boundaries carefully:

- Documentation about a public function is still `C`; describing an API does not change it.
- Type-checker or packaging metadata that makes existing annotations discoverable is `C`, not `A`.
- An implementation optimization that changes runtime performance is `B`, even when results and signatures remain unchanged.
- A refactor with no supported behavioral or performance effect is `C`.
- Changing how a dependency is supplied is `C` unless it changes supported runtime behavior.
- Reorganizing or migrating build and packaging configuration is `C`.
- Adding an exported function or widening a public function's accepted argument types is `A`.
- Dropping support for a runtime, operating system, or platform is `C`, not `A`.

### Select the digit

Use the first applicable category:

1. `1` — Breaking: previously supported caller code or environments must change, can fail, or receive incompatible behavior.
2. `2` — Compatible caller-facing capability: the change adds supported capability or corrects faulty behavior while valid existing usage remains valid.
3. `3` — No supported caller-facing semantic change: results and supported usage remain unchanged.

Apply these boundaries carefully:

- New or compatibly expanded public API is `A2`.
- Removed or incompatibly changed public API is `A1`.
- A correction to erroneous runtime results is `B2`.
- An incompatible change to existing runtime results is `B1`.
- A runtime performance optimization with unchanged results and API is `B3`.
- Added compatible environment, packaging, or type-checking support is `C2`.
- Dropped environment or platform support is `C1`.
- Documentation-only work is `C3`.
- Dependency maintenance with no supported caller-facing change is `C3`.
- Build or packaging migration with unchanged installation support and behavior is `C3`.
- Tests, tooling, and internal reorganization with no supported caller-facing effect are `C3`.

Do not assign `2` merely because work was added or improved. Use `2` only when users gain compatible supported capability or corrected behavior. Otherwise use `3`.

When multiple effects are described in one pending change, classify the most disruptive effect: `A` before `B` before `C`, and `1` before `2` before `3`.

## Compute the impact summary

Set `Impact` to the lowest digit used by any bullet, regardless of letter:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Before returning the entry, verify:

- Every pending change appears once.
- Each letter reflects the change's actual effect.
- Each digit reflects caller-facing compatibility, not implementation effort.
- Bullets are sorted by code while ties retain pending-list order.
- The impact equals the lowest bullet digit.
- The heading, impact line, bullet prefixes, and final HTML comment exactly match the required format.