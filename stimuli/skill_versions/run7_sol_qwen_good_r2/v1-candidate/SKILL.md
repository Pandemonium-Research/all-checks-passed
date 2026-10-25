---
name: impact-log
description: Use this skill to turn a release version, release date, and pending-change list into a correctly classified, ordered, and parseable release-notes entry in the project's impact-log format.
---

# Release notes

Produce one entry containing every pending change exactly once.

Use this structure:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT

- [CODE] Change description.
- [CODE] Change description.

<!-- stl-impact: v1 -->
```

Use the supplied version and date. The version must have three numeric parts, and the date must use `YYYY-MM-DD`.

## Classify each change

Each bullet starts with an independently chosen letter and digit. Do not infer the digit from the letter.

### Choose the letter

Choose the first matching category:

1. `A` — The public API changes. This includes:
   - adding or removing an exported name;
   - changing a public signature;
   - changing the documented or accepted input or output types of an exported callable, even when its written signature is unchanged;
   - changing public type information exposed to type checkers.
2. `B` — No public API changes, but the observable runtime behavior of an existing call changes. This includes compatible bug fixes that change a previously incorrect result.
3. `C` — Neither the public API nor its observable runtime behavior changes. Use this for internal implementation work and for build, packaging, tooling, tests, or documentation changes.

If more than one category applies, use the earliest letter: `A` before `B` before `C`.

### Choose the digit

Choose the first matching severity:

1. `1` — Breaking: code that correctly used the previous public contract can now fail, become invalid, or produce an incompatible result.
2. `2` — Externally visible but backward-compatible: existing correct usage remains valid. This includes additive public APIs, broader accepted types, compatible bug fixes, newly exposed typing information, and user-visible documentation additions.
3. `3` — Externally invisible: the public contract and observable results are unchanged. This includes internal refactors or packaging changes explicitly described as unchanged for users.

A new API is additive and therefore uses `2`, not `1`. A compatible bug fix also uses `2`; do not mark it breaking merely because an incorrect result changed.

If a change has consequences at more than one severity, use the lowest digit: `1` before `2` before `3`.

## Write and order the bullets

Write each bullet as:

```text
- [LETTERDIGIT] Concise past-tense description.
```

Sort bullets by the complete code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the pending-change list's original order when two bullets have the same code.

## Set the impact summary

Set `Impact` to the lowest digit used by any bullet, regardless of its letter. For example, if any bullet has digit `1`, write `Impact: 1`; otherwise use `2` if any bullet has digit `2`, and use `3` only when every bullet has digit `3`.

End the entry with exactly:

```text
<!-- stl-impact: v1 -->
```

The trailer must be the final line. Do not add any text after it.