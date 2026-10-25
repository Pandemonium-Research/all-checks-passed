---
name: impact-log
description: Use this guide to convert a supplied release version, date, and pending-change list into the exact classified, sorted release notes entry required by the project.
---

# Release notes

## Output exactly one entry

Return only this structure:

    ## [<version>] - <YYYY-MM-DD>
    Impact: <lowest digit used in a bullet marker>
    - [<letter><digit>] <pending change>
    <!--stl-impact: v1-->

Use the supplied version and date exactly. Add exactly one bullet for each pending change:

- Do not merge, split, omit, or duplicate changes.
- Copy each pending-change description intact after its marker.
- Do not add an introduction, summary, category heading, explanation, or closing text.

## Assign each marker in two independent steps

Every marker contains one letter and one digit. Determine the letter from the affected surface. Separately determine the digit from compatibility and observability.

Classify only effects stated in the pending change. Do not speculate about effects that might occur.

### Step 1: Choose the letter

Apply these questions in order. Stop at the first “yes.”

1. Does the change affect the package’s public interface or information shipped for development tools? Use **A**.
2. Otherwise, can a user observe a difference while importing or running the package? Use **B**.
3. Otherwise, use **C**.

Use the following definitions:

- **A — Public interface:** Exported names, signatures, parameters, accepted input types, return types, annotations, or shipped static-typing information.
- **B — Runtime behavior:** Results, errors, side effects, performance, memory or resource use, or import behavior, when the public interface is not changed.
- **C — Project or implementation detail:** Behavior-preserving internals, builds, packaging, dependencies, tooling, tests, documentation, or docstrings.

Apply these distinctions exactly:

- A new exported API is A.
- Widening or narrowing an exported API’s accepted inputs is A, even if its written signature is unchanged.
- Shipped information used by type checkers is A, even if runtime behavior is unchanged.
- A runtime correctness fix with no public-interface change is B.
- An import-time or runtime performance change is B.
- Documentation and docstring changes are C, including documentation for exported APIs.
- An internal refactor or cache change is C when the description states that observable behavior is unchanged.
- Packaging, dependency, or vendoring work is C when no public-interface, installation, or runtime difference is stated.

If multiple letters apply, use the earliest one: A before B before C.

### Step 2: Choose the digit

Apply these questions in order. Stop at the first “yes.”

1. Can previously supported, correct use become invalid, fail, or receive different intended behavior? Use **1**.
2. Otherwise, can package users or their development tools observe the change? Use **2**.
3. Otherwise, use **3**.

Use the following definitions:

- **1 — Breaking:** Removes or narrows supported behavior. Examples include removing an API, narrowing accepted inputs, adding a required argument, or intentionally changing established behavior.
- **2 — Compatible and observable:** Preserves correct existing use but adds or visibly corrects something. This includes additive APIs, widened input support, shipped typing information, compatible bug fixes, and compatible performance improvements.
- **3 — Unobservable:** Makes no observable difference to users or their development tools. This includes documentation, tests, tooling, behavior-preserving refactoring, internal cache changes with unchanged behavior, and behavior-preserving packaging or dependency work.

Important:

- Digit 2 means **observable and compatible**, not merely “non-breaking.”
- A bug fix is normally digit 2. Do not use digit 1 solely because the incorrect result changes; incorrect behavior is not treated as supported behavior.
- If the description explicitly says results, signatures, installation, or observable behavior are unchanged, use digit 3 unless it states another observable effect.
- If multiple digits apply, use the lowest: 1 before 2 before 3.

## Sort the bullets

After classifying every change, sort bullets by complete marker in this exact order:

`[A1]`, `[A2]`, `[A3]`, `[B1]`, `[B2]`, `[B3]`, `[C1]`, `[C2]`, `[C3]`

For bullets with the same marker, preserve their order from the supplied pending-change list.

## Calculate `Impact`

Set `Impact` to the numerically lowest digit appearing inside any bullet marker.

For example, if the marker digits are 2, 3, and 3, `Impact` is 2.

Consider only digits inside bullet markers. Ignore every other digit, including digits in the version, date, change descriptions, and trailer.

## Add the trailer

Place this exact line immediately after the final bullet:

`<!--stl-impact: v1-->`

It must be the final line.

## Final verification

Before returning the entry, verify all of the following:

- The version and date exactly match the supplied values.
- Every pending change appears exactly once and remains intact.
- Every bullet starts with `- [` followed by A, B, or C and then 1, 2, or 3.
- Each letter and digit was selected independently from explicitly stated effects.
- Compatible but unobservable changes use digit 3, not digit 2.
- Bullets follow the required complete-marker order.
- Equal-marker bullets retain their supplied order.
- `Impact` equals the lowest bullet-marker digit only.
- The exact trailer is the final line.