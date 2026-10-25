---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one complete, correctly classified, ordered, and machine-parseable impact-log release-not notes entry.
---

# Release notes

Produce exactly one entry containing every pending change exactly once. Do not omit, duplicate, split, or combine changes.

Use this exact layout, including blank lines:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT

- [CODE] Concise past-tense description.
- [CODE] Concise past-tense description.

<!-- stl-impact: v1 -->
```

Copy the supplied version and date without altering them. The version must have three numeric parts, such as `1.4.0`, and the date must use `YYYY-MM-DD`.

## Classify each change

Assign each change one letter and one digit. Choose them independently: the letter identifies the kind of change, while the digit identifies its severity or visibility.

### Choose the letter

Apply these rules in order:

1. `A` — The public API or public type information changes.
2. `B` — The public API is unchanged, but an existing call's observable runtime behavior changes.
3. `C` — Neither the public API nor an existing call's observable runtime behavior changes.

Use `A` when a change:

- adds or removes an exported name;
- changes a public signature;
- broadens or narrows accepted input types;
- changes returned output types;
- changes public annotations or other typing information;
- makes shipped annotations discoverable to type checkers.

A change to accepted or returned types is `A` even when the written function signature is unchanged.

Use `B` for behavior changes under an unchanged public API, including compatible bug fixes that correct a previously wrong result.

Use `C` for internal implementations, performance work, build configuration, dependencies, packaging, tooling, tests, or documentation when they do not change the public API or runtime results.

Classify by effect, not by the file or subsystem changed. For example, packaging work that exposes public typing information is `A`, while packaging work that leaves the public API and runtime results unchanged is `C`.

If multiple letters appear applicable, use the earliest:

```text
A before B before C
```

### Choose the digit

Apply these rules in order:

1. `1` — Breaking.
2. `2` — Externally visible and backward-compatible.
3. `3` — Externally invisible.

Use `1` only if code that correctly followed the previous public contract can now fail, become invalid, or produce an incompatible result.

Use `2` when existing correct usage remains valid but users, type checkers, documentation readers, installers, or other external consumers can observe the change. This includes:

- additive public APIs;
- broader accepted input types;
- compatible bug fixes;
- newly exposed public typing information;
- user-visible documentation additions;
- externally visible build, packaging, or dependency changes.

Use `3` only when the public contract, runtime results, and other externally visible behavior remain unchanged. Internal refactors and optimizations are `3`; build or packaging changes are `3` only when the pending change explicitly says their effect is unchanged for users.

An additive API is `2`, not `1`. A compatible bug fix is `2`, not `1`, merely because its previously incorrect result changes.

If multiple digits appear applicable, use the lowest:

```text
1 before 2 before 3
```

## Write and order the bullets

Write one bullet for each pending change:

```text
- [LETTERDIGIT] Concise past-tense description.
```

Preserve the change's material facts. Do not add unsupported claims about compatibility, visibility, or behavior.

Sort the bullets by the complete code in this exact letter-first order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Do not sort primarily by digit. When multiple changes have the same code, preserve their order from the pending-change list.

## Set the impact summary

After classifying every bullet, set `Impact` to the lowest digit used anywhere in the entry:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore the letters when calculating `Impact`.

## Finish the entry

End with exactly:

```text
<!-- stl-impact: v1 -->
```

The trailer must be the final line. Do not add commentary or any other text after it.