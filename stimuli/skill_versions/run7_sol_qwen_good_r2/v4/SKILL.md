---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one complete, correctly classified, ordered, and machine-parseable impact-log release-notes entry.
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

Assign each change one letter and one digit. Determine them independently: the letter identifies what changed, while the digit identifies its compatibility or visibility.

### Choose the letter

Apply the following rules in order. Stop at the first match:

1. `A` — The public API or public type information changes.
2. `B` — The public API is unchanged, but the observable runtime behavior of an existing call changes.
3. `C` — Neither the public API nor the observable runtime behavior of an existing call changes.

Use `A` for any change that:

- adds or removes an exported name, including an export at the package root;
- changes a public signature;
- broadens or narrows the inputs accepted by an exported callable, even if its written signature is unchanged;
- changes the output types promised by a public API;
- changes public annotations or other information exposed to type checkers;
- makes shipped annotations discoverable to type checkers.

Use `B` when an existing call can produce different runtime behavior without a public API change. Compatible bug fixes that correct previously wrong results are `B`.

Use `C` for internal implementation work and for build, dependency, packaging, tooling, test, or documentation changes that do not alter the public API or an existing call’s runtime behavior.

Classify by the effect of the change, not the subsystem or file involved. Packaging work that exposes public typing information is `A`; dependency or packaging work with no API or runtime-result change remains `C`.

If more than one letter appears applicable, use this precedence:

```text
A before B before C
```

### Choose the digit

Apply the following rules in order. Stop at the first match:

1. `1` — Breaking.
2. `2` — Externally visible and backward-compatible.
3. `3` — Externally invisible.

Use `1` only when software that correctly followed the previous public contract can now fail, become invalid, or receive an incompatible result. A result changing because a bug was corrected is not breaking when the corrected behavior remains compatible with the public contract.

Use `2` when the change is externally visible but existing correct usage remains valid. This includes:

- additive public APIs;
- broader accepted input types;
- compatible bug fixes;
- newly exposed or changed public typing information;
- user-visible documentation additions;
- externally visible build, packaging, or dependency changes.

Use `3` only when external consumers cannot observe the change. This includes internal optimizations and refactors. A build, dependency, or packaging change is `3` only when its description establishes that users, installation behavior, the public contract, and runtime results are unchanged.

An additive API is `2`, not `1`. A compatible bug fix is `2`, not `1`, merely because the corrected result differs from the old incorrect result.

If more than one digit appears applicable, use this precedence:

```text
1 before 2 before 3
```

Before writing the entry, verify each classification independently:

- New export or newly discoverable public typing information: letter `A`.
- Changed result from an existing call with no API change: letter `B`.
- No API or existing-call runtime change: letter `C`.
- Breaks previously correct usage: digit `1`.
- Visible while preserving previously correct usage: digit `2`.
- Invisible outside the project: digit `3`.

## Write and order the bullets

Write one bullet for each pending change:

```text
- [LETTERDIGIT] Concise past-tense description.
```

Preserve the material facts supplied for the change. Do not invent compatibility, visibility, or behavior claims.

Sort all bullets by the complete code in this exact letter-first order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Do not sort primarily by digit and do not retain the original order across different codes. For changes with the same code, preserve their order from the pending-change list.

## Set the impact summary

After classifying all bullets, set `Impact` to the lowest digit appearing in any bullet code:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore the letters when calculating `Impact`. Recalculate it from the final sorted bullets rather than inferring it from the version number or type of release.

## Finish the entry

End with exactly:

```text
<!-- stl-impact: v1 -->
```

The trailer must be the final line. Do not add commentary or any other text after it.