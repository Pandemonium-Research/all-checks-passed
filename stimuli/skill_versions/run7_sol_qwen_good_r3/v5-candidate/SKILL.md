---
name: impact-log
description: Use this skill when given a release version, release date, and pending-change list to produce one classified, sorted, and parser-compatible release-notes entry.
---

# Release notes

Create exactly one release-notes entry. Copy the supplied version and date exactly, and represent every pending change exactly once. Do not combine, split, omit, duplicate, or invent changes.

The completed entry must have this structure:

`## [VERSION] - YYYY-MM-DD`

`Impact: DIGIT`

`- [CODE] Change description.`

`<!-- stl-impact: v1 -->`

Omit the backticks in the completed entry.

Formatting requirements:

- Put exactly one blank line after the heading.
- Put exactly one blank line after the impact line.
- Put no blank lines between bullets.
- Put exactly one blank line between the final bullet and the trailer.
- Make the trailer the final line.

## Classify each change

Each bullet begins with one code in square brackets. Determine its letter and digit independently, using only effects stated in the pending change.

### Choose the letter

Use the first applicable category:

1. **A — Public API:** Adds, removes, renames, or modifies something callers use as public API. This includes exported names, signatures, parameters, defaults, accepted argument types or values, return types, and public type annotations.
2. **B — Observable runtime behavior:** Leaves the public API unchanged but changes something observable when importing or running the package. This includes results, errors, side effects, performance, memory use, cache behavior, and other resource use.
3. **C — Internal or project-only:** Does not change public API or observable runtime behavior. This includes internal refactoring, build and packaging implementation, dependency vendoring, tooling, tests, and documentation.

Apply these distinctions exactly:

- A new exported API is **A**.
- Broadening or narrowing the accepted types or values of a public parameter is **A**.
- Changing the result of an existing call without changing its API is **B**.
- A stated improvement to execution speed, import time, memory use, or other resource use is **B**, even when output is unchanged.
- A new finite limit on a runtime cache, retained data, memory, storage, network use, or another runtime resource is **B**. Treat replacing previously unrestricted retention with a bound as a stated resource-use change, even if results are unchanged.
- An internal optimization is **C** only when no caller-observable runtime effect or resource bound is stated. Do not infer an effect that the pending change does not state.
- Changing exported type annotations is **A**.
- Adding typing-discovery metadata without changing annotations is **C**.
- Documentation, tests, build configuration, dependency layout, and packaging implementation are **C** unless the change explicitly states a public-API or runtime effect.
- Distribution artifacts and availability, such as support for an additional interpreter or platform package, are **C** unless they change public API or runtime behavior.

If more than one letter applies, choose the earliest one: **A before B before C**.

### Choose the digit

Use the first applicable severity:

1. **1 — Breaking:** The pending change explicitly makes previously valid or supported usage invalid, unsupported, or intentionally incompatible.
2. **2 — Compatible and observable:** Adds a compatible capability, broadens supported usage, fixes caller-visible behavior, improves observable runtime behavior, establishes a useful runtime resource bound, or adds a capability for package-user tooling.
3. **3 — Unobservable to callers and their tools:** Changes only implementation or project-maintenance material without adding a user-visible or tool-visible capability.

Apply these distinctions exactly:

- Use digit **1** only when incompatibility is explicit. Examples include removing or renaming public API, narrowing accepted inputs, making an optional argument required, intentionally changing documented semantics, or dropping previously supported usage.
- A changed result is not by itself breaking.
- A defect correction is digit **2** unless the pending change explicitly says it introduces an incompatible contract change. This remains true when correcting the defect changes the result produced by existing code.
- A compatible new public API or broader accepted input is digit **2**.
- A stated performance or resource-use improvement is digit **2**.
- A new runtime resource limit or bound is digit **2**, including a finite cache or retention bound, even when output or results remain unchanged.
- New distribution availability useful to package users is digit **2**.
- Typing-discovery metadata that enables user type checkers to consume shipped annotations is digit **2**.
- Internal refactoring, dependency vendoring, packaging migration, tests, and documentation are digit **3** when no user-visible or tool-visible capability is stated.
- Words such as “added,” “replaced,” or “migrated” do not by themselves make a change digit **2**.

If more than one digit applies, choose the lowest one: **1 before 2 before 3**. However, digit **1** always requires explicitly stated incompatibility; never infer it merely from a changed result or a bug fix.

## Write the bullets

Write one concise, past-tense bullet for each pending change:

`- [CODE] Change description.`

Preserve every material fact from the pending change, especially:

- What changed and where.
- The stated public, runtime, distribution, or tooling effect.
- Compatibility statements such as an unchanged signature, output, behavior, or installation experience.

You may improve grammar and concision, but do not remove qualifiers or add effects that were not supplied.

## Sort the bullets

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For bullets with the same code, preserve their order from the pending-change list.

## Calculate the impact summary

Set `Impact` to the lowest digit used by any bullet:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Calculate the impact after classifying every bullet. Do not derive it from the release version.

## Validate the completed entry

Before returning the entry, verify all of the following:

- There is exactly one release heading.
- The heading is exactly `## [VERSION] - YYYY-MM-DD` using the supplied version and date.
- Every pending change appears exactly once.
- Every bullet begins with one valid impact code.
- No defect correction uses digit `1` unless incompatibility is explicit.
- Every stated runtime resource effect, limit, or bound uses letter `B`, even if output is unchanged.
- A new runtime resource bound uses digit `2`.
- Bullets follow the required code order, with original order preserved for ties.
- The impact summary equals the lowest digit used by any bullet.
- Blank lines match the required format.
- The trailer is exactly `<!-- stl-impact: v1 -->`.
- Nothing appears after the trailer.