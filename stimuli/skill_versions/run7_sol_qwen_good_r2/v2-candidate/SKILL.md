---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one complete, correctly classified, ordered, and machine-parseable impact-log release-notes entry.
---

# Release notes

Produce exactly one release-notes entry. Include every pending change exactly once; do not omit, duplicate, or combine changes.

Use this exact layout:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT

- [CODE] Concise past-tense description.
- [CODE] Concise past-tense description.

<!-- stl-impact: v1 -->
```

Copy the supplied version and date. The version must contain three numeric parts, such as `1.4.0`, and the date must use `YYYY-MM-DD`.

## Classify every change

Classify each change independently with one letter and one digit. Determine the letter and digit separately; a letter does not imply a particular digit.

### Choose the letter

Use the first matching rule:

1. `A` — The public API or public type information changes.
2. `B` — The public API is unchanged, but the observable runtime behavior of an existing call changes.
3. `C` — Neither the public API nor the observable runtime behavior of an existing call changes.

Use `A` for any change that:

- adds or removes an exported name;
- changes a public signature;
- broadens or narrows the accepted inputs or returned outputs of an exported callable, even if its written signature is unchanged;
- changes annotations or other public typing information exposed to type checkers;
- makes shipped annotations discoverable to type checkers.

Use `B` for behavior changes under an unchanged public contract, including compatible bug fixes that correct a previously wrong result.

Use `C` for internal implementation work and for build, dependency, packaging, tooling, test, or documentation changes when they do not change the public API or runtime results.

The subject of a change does not determine its letter by itself. For example, a packaging change that exposes public typing information is `A`, while a packaging migration explicitly described as unchanged for users is `C`.

If several letters appear applicable, use the earliest one:

```text
A before B before C
```

### Choose the digit

Use the first matching rule:

1. `1` — Breaking.
2. `2` — Externally visible and backward-compatible.
3. `3` — Externally invisible.

Use `1` only when code that correctly followed the previous public contract can now fail, become invalid, or produce an incompatible result.

Use `2` for changes visible to users that preserve existing correct usage, including:

- additive public APIs;
- broader accepted input types;
- compatible bug fixes;
- newly exposed public typing information;
- user-visible documentation additions.

Use `3` only when callers cannot observe a public-contract or runtime-result change, including internal optimizations, refactors, and packaging changes explicitly described as unchanged for users.

Do not classify an additive API as breaking. Do not classify a compatible bug fix as breaking merely because its previously incorrect result changes.

If several severities apply, use the lowest digit:

```text
1 before 2 before 3
```

## Write and order the bullets

Write one bullet per pending change:

```text
- [LETTERDIGIT] Concise past-tense description.
```

Sort by the entire code in exactly this order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

This is letter-first order, not severity-first order. For changes with the same code, preserve their order from the pending-change list.

## Set the impact summary

After classifying all bullets, set `Impact` to the lowest digit appearing in any code:

- write `Impact: 1` if any bullet has digit `1`;
- otherwise write `Impact: 2` if any bullet has digit `2`;
- otherwise write `Impact: 3`.

Ignore the letters when calculating `Impact`.

## Finish the entry

End with exactly:

```text
<!-- stl-impact: v1 -->
```

The trailer must be the final line. Do not add text after it.