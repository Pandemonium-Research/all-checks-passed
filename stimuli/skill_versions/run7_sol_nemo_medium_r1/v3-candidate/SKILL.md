---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one classified, stably sorted, machine-parseable impact-log release-notes entry.
---

# Release notes

Create exactly one release entry. Include every pending change exactly once. Classify the stated effect of each change; do not classify it from filenames, implementation details, or older release entries.

## Required output

Render the entry exactly as follows, without a code fence or introductory text:

## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->

Requirements:

- Begin the heading with `## `.
- Put the supplied three-part version inside square brackets.
- Write the supplied date as `YYYY-MM-DD`.
- Put `Impact: DIGIT` immediately below the heading.
- Use one bullet for each pending change. Do not combine or split changes.
- Begin every bullet with exactly one code in square brackets.
- Preserve each change's supplied meaning and do not invent effects, compatibility claims, or performance claims.
- Sort bullets in this order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
- When multiple bullets have the same code, retain their order from the pending-change list.
- Make `<!-- stl-impact: v1 -->` the final line, with nothing after it.

## Classify each change

A code contains one letter and one digit. Choose them independently.

### Choose the letter

Apply these tests in order:

1. Use `A` when the supported public API contract changes. This includes adding or removing exported names, changing public signatures, widening or narrowing accepted argument types, changing return types, or changing public type definitions.
2. Otherwise, use `B` when execution of existing runtime functionality changes in behavior or performance.
3. Otherwise, use `C` for packaging, environment support, dependencies, build configuration, tooling, tests, documentation, and internal work that does not affect runtime behavior or performance.

Important boundaries:

- Adding an exported function or compatibly accepting another argument type is `A`.
- Fixing the result produced by an existing function is `B`, not `A`, when its public contract is unchanged.
- Runtime optimizations are `B` when they improve startup, import time, caching, CPU use, memory use, or other runtime performance, even if results and signatures are unchanged.
- A refactor without a stated runtime behavior or performance effect is `C`.
- Documentation for a public function is `C`; documenting an API does not change the API.
- Packaging metadata that makes already-shipped annotations discoverable to type checkers, such as adding `py.typed`, is `C`, not `A`.
- Adding, removing, or changing supported runtimes, operating systems, or platforms is `C`, not `A`.
- Migrating build or packaging configuration is `C` when installation support and behavior remain unchanged.
- Adding, removing, updating, or vendoring a dependency is `C` unless the pending change states that supported runtime behavior or performance changes.

### Choose the digit

Apply these tests in order:

1. Use `1` when previously supported callers or environments must change, can fail, lose support, or receive incompatible behavior.
2. Otherwise, use `2` when users gain a compatible supported capability, corrected behavior, or newly supported environment, packaging, or type-checking functionality.
3. Otherwise, use `3` when supported results and usage remain unchanged.

The digit measures compatibility and supported caller-facing effect, not the amount of work performed.

Common combinations:

- `A1` — Public API is removed, narrowed, or incompatibly changed.
- `A2` — Public API is added or compatibly expanded.
- `B1` — Existing runtime behavior changes incompatibly.
- `B2` — Faulty runtime behavior is corrected without invalidating valid existing usage.
- `B3` — Runtime performance changes while results and the public API remain unchanged.
- `C1` — A supported runtime, operating system, platform, or environment is dropped.
- `C2` — Compatible environment, packaging, installation, or type-checking support is added.
- `C3` — Documentation, tests, tooling, dependency maintenance, build migration, or internal reorganization has no supported caller-facing effect.

Do not use digit `2` merely because something was added, modernized, or improved:

- Documentation examples remain `C3`.
- Dependency vendoring or replacement remains `C3` when supported behavior is unchanged.
- A packaging migration remains `C3` when installation support is unchanged.
- Type-checker metadata that enables existing annotations to be recognized is `C2`.
- A runtime optimization with unchanged results is `B3`.

If one pending change explicitly contains multiple effects, select the most disruptive applicable classification: prefer `A` over `B` over `C`, and prefer `1` over `2` over `3`.

## Compute the impact summary

Set `Impact` to the lowest digit appearing in any bullet, regardless of letter:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

## Final verification

Before returning the entry, confirm that:

- The supplied version and date are correct.
- Every pending change appears exactly once.
- Each letter reflects the change's stated effect.
- Each digit reflects compatibility and supported capability, not implementation effort.
- Runtime optimizations are `B3`, compatible support additions are `C2`, and maintenance-only changes are `C3`.
- Bullets follow the required code order and same-code ties retain input order.
- `Impact` equals the lowest bullet digit.
- The heading, impact line, bullet prefixes, and final HTML comment exactly match the required format.