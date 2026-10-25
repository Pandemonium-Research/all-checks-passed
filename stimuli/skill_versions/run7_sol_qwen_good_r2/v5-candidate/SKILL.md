---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one complete, correctly classified, ordered, and machine-parseable impact-log release-notes entry.
---

# Release notes

Produce exactly one release-notes entry. Include every pending change exactly once. Do not omit, duplicate, or combine changes.

Use this exact layout and blank-line placement:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT

- [CODE] Concise past-tense description.
- [CODE] Concise past-tense description.

<!-- stl-impact: v1 -->
```

Copy the supplied version and date exactly. The version must be a three-part numeric version, and the date must use `YYYY-MM-DD`.

## Classify each change

Assign each change one letter and one digit. Choose the letter and digit independently:

- The letter identifies the kind of effect.
- The digit identifies compatibility or visibility.

Do not classify from the version number, filename, subsystem, or labels such as “fix,” “packaging,” or “internal.” Classify the actual effect described.

### Choose the letter

Apply these rules in order and stop at the first match:

1. `A` — Public API or public type information changes.
2. `B` — The public API is unchanged, but an existing call can behave differently at runtime.
3. `C` — Neither the public API nor the runtime behavior of an existing call changes.

Use `A` when the change:

- adds or removes an exported name;
- adds or removes a package-root export;
- changes a public callable’s signature;
- broadens or narrows the accepted inputs of an exported callable, even if its written signature is unchanged;
- changes a public return type, return shape, or other promised output type;
- changes public annotations or information exposed to type checkers;
- makes shipped annotations discoverable to type checkers.

A change to what a public call returns is `A` when it changes the promised type or shape of the result. Do not classify such a change as `B` merely because callers observe it at runtime.

Use `B` only when the public API contract, including its accepted inputs and promised output types, is unchanged, but an existing call can produce a different value, side effect, exception, or other runtime behavior. A compatible bug fix that corrects a previously wrong result is `B`.

Use `C` for changes outside the public API and existing-call runtime behavior, including:

- internal implementation work;
- optimizations and refactors with unchanged results;
- supported-runtime or platform policy changes;
- build, dependency, packaging, tooling, test, or documentation changes.

A `C` change can still be visible or breaking. The letter `C` does not imply digit `3`.

When multiple letters appear applicable, use:

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

Use `2` when external consumers can observe the change, but existing correct usage remains valid. This includes:

- additive public APIs;
- broader accepted inputs;
- compatible bug fixes;
- newly discoverable or changed public typing information;
- user-facing documentation additions or improvements;
- externally visible build, dependency, installation, or packaging changes.

Documentation intended for users is externally visible and therefore uses digit `2`, even when it does not change code behavior.

Use `3` only when external consumers cannot observe the change. Typical examples are internal refactors, tests, and optimizations whose public API and runtime results remain unchanged.

Do not assign digit `3` merely because a change belongs to documentation, dependencies, packaging, build configuration, or runtime support. For those categories, determine whether the effect is breaking, externally visible and compatible, or truly invisible.

A build, dependency, or packaging change uses digit `3` only when the supplied facts establish that installation behavior, supported environments, public contracts, and runtime results are unchanged.

A corrected bug result is not breaking solely because it differs from the old incorrect result. If the correction remains compatible with the previous public contract, use digit `2`.

When multiple digits appear applicable, use:

```text
1 before 2 before 3
```

### Verify every code

Before writing the entry, check each change against this table:

| Effect | Letter |
|---|---|
| Export, signature, accepted-input contract, promised output type or shape, or public typing changes | `A` |
| Existing call behaves differently without changing its public API contract | `B` |
| Neither of the above, including documentation, dependencies, packaging, internals, or support policy | `C` |

| Compatibility or visibility | Digit |
|---|---|
| Previously correct usage or a previously supported environment becomes invalid | `1` |
| External consumers can observe the change while existing correct usage remains valid | `2` |
| External consumers cannot observe the change | `3` |

In particular, verify these commonly confused cases:

- An incompatible public return-type or return-shape change is `A1`, not `B1`.
- A compatible change to the value produced by an existing call is `B2`.
- User-facing documentation is visible and therefore ends in `2`.
- Dropping a supported runtime or platform is breaking and therefore ends in `1`.
- Internal work with identical external behavior is `C3`.

## Write and order the bullets

Write exactly one bullet for each pending change:

```text
- [LETTERDIGIT] Concise past-tense description.
```

Preserve all material facts supplied for the change. Do not invent claims about compatibility, visibility, supported environments, or unchanged behavior.

Sort the bullets by their complete code in this exact letter-first order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Do not sort primarily by digit. Do not preserve the original order between different codes. When multiple changes have the same code, preserve their relative order from the pending-change list.

After sorting, confirm that every pending change appears once and only once.

## Set the impact summary

Calculate `Impact` from the digits in the final bullet codes:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore the letters. Recalculate the value from the final bullets; do not infer it from the version number or release type.

## Finish the entry

End with exactly:

```text
<!-- stl-impact: v1 -->
```

The trailer must be the final line. Do not add commentary or any other text after it.