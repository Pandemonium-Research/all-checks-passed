---
name: impact-log
description: Use this skill when given a release version, release date, and pending project changes to write one complete, correctly classified, ordered, and machine-parseable impact-log release-nototes entry.
---

# Release notes

Produce exactly one release-notes entry. Include every pending change exactly once; do not omit, duplicate, or combine changes.

Use this exact layout, including blank lines:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT

- [CODE] Concise past-tense description.
- [CODE] Concise past-tense description.

<!-- stl-impact: v1 -->
```

Copy the supplied version and date exactly. Use a three-part numeric version and a `YYYY-MM-DD` date.

## Classify each change

Assign each change one letter and one digit. Determine them independently:

- The letter identifies what changed.
- The digit identifies whether the change is breaking, visible and compatible, or invisible.

Classify the actual effect described. Do not classify from the version number, filename, subsystem, or labels such as “fix,” “packaging,” “documentation,” or “internal.”

### Choose the letter

Apply these rules in order and stop at the first match:

1. `A` — The public API or public type information changes.
2. `B` — The public API is unchanged, but the observable runtime behavior of an existing call changes.
3. `C` — Neither the public API nor the observable runtime behavior of an existing call changes.

Use `A` for any change that:

- adds or removes an exported name, including an export at the package root;
- changes a public callable’s signature;
- broadens or narrows the inputs accepted by an exported callable, even if its written signature is unchanged;
- changes a public return type, result shape, or other promised output type;
- changes public annotations or other information exposed to type checkers;
- makes shipped annotations discoverable to type checkers.

A change from one promised result type or shape to another—for example, from a single joined value to a collection—is `A`, not `B`. Use digit `1` as well if the change is incompatible.

Use `B` only when the public API contract, including accepted inputs and promised output types and shapes, is unchanged but an existing call can produce a different value, side effect, exception, or other runtime behavior. A compatible bug fix that corrects a previously wrong result is `B`.

Use `C` when neither `A` nor `B` applies. This includes:

- internal implementation work;
- optimizations and refactors with unchanged results;
- supported-runtime or platform policy changes;
- build, dependency, packaging, tooling, and test changes;
- documentation changes, including examples in public docstrings.

A `C` change can still be externally visible or breaking. Determine its digit separately. In particular, documentation does not become invisible merely because it does not change runtime behavior, and dropping a supported runtime does not become nonbreaking merely because the public API is unchanged.

Packaging work that exposes public typing information is `A`. Other dependency or packaging work with no public API or existing-call runtime-result change is `C`.

If more than one letter appears applicable, use this precedence:

```text
A before B before C
```

### Choose the digit

Apply these rules in order and stop at the first match:

1. `1` — Breaking.
2. `2` — Externally visible and backward-compatible.
3. `3` — Externally invisible.

Use `1` when software, environments, or workflows that correctly followed the previous public contract or documented support policy can now fail, become invalid, or receive an incompatible result. This includes:

- removing or incompatibly changing a public API;
- narrowing previously supported inputs;
- incompatibly changing a promised return type or result shape;
- dropping a previously supported language runtime, operating system, platform, or environment.

Dropping support for a runtime or platform is `C1`: `C` because no public API or existing-call behavior changed, and `1` because a previously supported environment is no longer valid.

Use `2` when external consumers can observe the change but existing correct usage remains valid. This includes:

- additive public APIs;
- broader accepted inputs;
- compatible bug fixes;
- newly discoverable or changed public typing information;
- user-facing documentation additions or improvements;
- examples added to public callable docstrings;
- externally visible build, packaging, installation, or dependency changes.

Public docstrings and their examples are user-facing documentation. Classify their letter as `C` when they do not change the API or runtime behavior, but assign digit `2`, producing `C2`.

Use `3` only when external consumers cannot observe the change. Typical examples are internal refactors, tests, and optimizations whose public API and runtime results remain unchanged.

Do not assign digit `3` solely because a change concerns documentation, dependencies, packaging, build configuration, or runtime support. For those categories, decide whether the stated effect is breaking, visible and compatible, or truly invisible.

A build, dependency, or packaging change is `3` only when the supplied facts establish that installation behavior, supported environments, public contracts, and runtime results are unchanged.

A corrected bug result is not breaking solely because it differs from the old incorrect result. If the correction remains compatible with the previous public contract, use digit `2`.

If more than one digit appears applicable, use this precedence:

```text
1 before 2 before 3
```

Before writing the entry, verify these commonly confused classifications:

- Additive export: `A2`.
- Newly discoverable public typing information: `A2`.
- Incompatible public return-type or result-shape change: `A1`, not `B1`.
- Compatible changed result from an existing call with no API-contract change: `B2`.
- Public documentation or public docstring examples: `C2`, not `C3`.
- Dropped supported runtime or platform: `C1`, not `C3`.
- Internal optimization with identical external behavior: `C3`.

## Write and order the bullets

Write exactly one bullet for each pending change:

```text
- [LETTERDIGIT] Concise past-tense description.
```

Preserve all material facts supplied for the change. Do not invent claims about compatibility, visibility, supported environments, or unchanged behavior.

Sort all bullets by their complete code in this exact letter-first order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Do not sort primarily by digit. Do not retain the original order across different codes. When multiple changes have the same code, preserve their relative order from the pending-change list.

After sorting, confirm that every pending change appears once and only once.

## Set the impact summary

Calculate `Impact` from the digits in the final bullet codes:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore the letters. Recalculate `Impact` from the final bullets; do not infer it from the version number or release type.

## Finish the entry

End with exactly:

```text
<!-- stl-impact: v1 -->
```

The trailer must be the final line. Do not add commentary or any other text after it.