---
name: impact-log
description: Use this skill to convert a supplied version, release date, and pending-change list into one correctly classified, ordered, and parser-compatible release-notes entry.
---

# Release notes

Create exactly one release-notes entry. Use the supplied version, date, and every pending change exactly once. Do not invent changes or alter the version or date.

The completed entry must have this structure:

`## [VERSION] - YYYY-MM-DD`

`Impact: DIGIT`

`- [CODE] Change description.`

`<!-- stl-impact: v1 -->`

Omit the backticks in the completed entry. Use a three-part version number, such as `1.4.0`.

## Classify each change

Each bullet begins with one code in square brackets. Determine its letter and digit independently from the effect stated in the pending change.

### Choose the letter

Use the first applicable category:

1. **A — Public API:** Adds, removes, renames, or modifies something callers use as public API. This includes exported names, signatures, parameters, defaults, accepted argument types, return types, and public type annotations.
2. **B — Observable runtime behavior:** Leaves the public API unchanged but changes something users can observe when importing or using the package. This includes results, errors, side effects, performance, memory use, cache behavior, retained-data use, and other resource use.
3. **C — Internal or project-only:** Does not change the public API or observable runtime behavior. This includes internal refactoring, build and packaging implementation, dependency vendoring, tooling, tests, and documentation.

Apply these distinctions exactly:

- A new exported API is **A**.
- Broadening or narrowing the accepted types or values of a public parameter is **A**.
- Changing the result of an existing call without changing its API is **B**.
- A stated improvement to execution speed, import time, memory use, or resource use is **B**, even when output is unchanged.
- Introducing a finite bound, size limit, or eviction policy for a runtime cache or other previously unbounded retained data is **B**, even when results or output are unchanged.
- An internal optimization is **C** only when the change states no caller-observable effect, performance effect, or runtime resource bound. Do not assume an effect that is not stated.
- Changing exported type annotations is **A**.
- Adding typing-discovery metadata without changing annotations is **C**.
- Documentation, tests, build configuration, dependency layout, and packaging implementation are **C** unless the change explicitly states a public-API or runtime effect.

If more than one letter applies, choose the earliest one: **A before B before C**.

### Choose the digit

Use the first applicable severity:

1. **1 — Breaking:** The pending change explicitly states that previously valid or supported usage becomes invalid, unsupported, or intentionally incompatible.
2. **2 — Compatible and observable:** Adds compatible capability, broadens supported usage, fixes caller-visible behavior, improves observable runtime behavior, establishes a useful runtime resource bound, or adds a useful capability for package-user tooling.
3. **3 — Unobservable to callers and their tools:** Changes only implementation or project-maintenance material without adding a user-visible or tool-visible capability.

Apply these distinctions exactly:

- Use digit **1** only when incompatibility is explicit. Examples include removing or renaming public API, narrowing accepted inputs, making an optional argument required, intentionally changing documented semantics, or dropping supported usage.
- Do not infer digit **1** merely because a result changes.
- A defect correction is digit **2** unless the pending change explicitly states that it introduces an incompatible contract change. This applies even when correcting the defect changes the result produced by existing code.
- A compatible new public API or broader accepted input is digit **2**, not digit 1.
- A stated performance or resource-use improvement is digit **2**.
- A new finite bound or eviction policy for a runtime cache or other retained data is digit **2**, even when output is unchanged.
- Typing-discovery metadata that enables user type checkers to consume shipped annotations is digit **2**.
- Internal refactoring, dependency vendoring, packaging migration, tests, and documentation are digit **3** when no user-visible or tool-visible capability is stated.
- Words such as “added,” “replaced,” or “migrated” do not by themselves make a change digit **2**.

If more than one digit applies, choose the lowest one: **1 before 2 before 3**. Digit **1** still requires explicitly stated incompatibility.

## Write the bullets

Write one concise, past-tense bullet for each pending change:

`- [CODE] Change description.`

Preserve material facts from the pending change, especially compatibility statements such as an unchanged signature, output, or installation experience. Do not add effects that were not supplied.

## Sort the bullets

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For bullets with the same code, preserve their order from the pending-change list.

## Calculate the impact summary

Set `Impact` to the lowest digit used by any bullet:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Calculate this after classifying every bullet. Do not derive the impact value from the version number.

## Validate the completed entry

Before returning the entry, verify all of the following:

- There is exactly one release heading.
- The heading is exactly `## [VERSION] - YYYY-MM-DD` with the supplied values.
- Every pending change appears exactly once.
- Every bullet has one valid impact code.
- No defect correction uses digit `1` unless the pending change explicitly states an incompatible contract change.
- Every stated runtime cache or retained-data bound uses code `B2`, unless a higher-priority public-API or explicitly breaking effect also applies.
- Bullets follow the required code order, with original order preserved for ties.
- The impact summary equals the lowest bullet digit.
- There is exactly one blank line between the heading, impact line, bullet list, and trailer.
- The trailer is exactly `<!-- stl-impact: v1 -->`.
- The trailer is the final line, with nothing after it.