---
name: impact-log
description: Use this document when converting a release version, date, and pending-change list into a classified, sorted, parser-compatible release notes entry.
---

# Release notes

Produce exactly one entry using this structure:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Concise change summary.
- [CODE] Concise change summary.

<!-- stl-impact: v1 -->

Formatting requirements:

- Replace `VERSION` with the supplied three-part numeric version, without backticks.
- Replace `YYYY-MM-DD` with the supplied zero-padded date.
- Include every pending change exactly once.
- Preserve every blank line shown in the structure.
- The trailer must be exactly `<!-- stl-impact: v1 -->`.
- The trailer must be the final line; write nothing after it.

## Classify each change

Assign each change one code consisting of a letter and a digit. Determine the letter and digit independently.

### Choose the letter

Apply these rules in order and stop at the first match:

1. Use `A` if the public API surface changes. This includes:
   - adding, removing, or renaming an exported name;
   - changing a public function or method signature;
   - changing accepted argument types or return types;
   - allowing an additional type in an existing public API.

   An additive API or compatible type widening is still `A`, not `B`.

2. Otherwise, use `B` if an existing public call retains the same API surface but produces observably different runtime behavior. A compatible correction to an incorrect result is normally `B`.

3. Otherwise, use `C`. This includes:
   - internal implementation changes with unchanged public results;
   - performance optimizations with unchanged results and signatures;
   - build, packaging, and distribution work;
   - tooling, tests, and documentation.

   A new installation target or distributable artifact uses `C` because it does not change the package's public API or an existing call's runtime behavior.

Letter precedence is therefore `A`, then `B`, then `C`.

### Choose the digit

Apply these rules in order and stop at the first match:

1. Use `1` only for a breaking change: previously valid caller code can fail or receive an incompatible result.

   Do not use `1` merely because a compatible bug fix changes a previously incorrect result.

2. Otherwise, use `2` for a compatible change that users can observe. This includes:
   - adding a public API;
   - widening the accepted types of a public API;
   - compatibly correcting runtime behavior;
   - adding a supported installation target or distributable artifact.

3. Otherwise, use `3` when callers cannot observe the change. This includes:
   - internal caching or optimization with unchanged results;
   - internal refactoring;
   - test or documentation changes;
   - packaging migrations that leave installation behavior unchanged.

Digit precedence is therefore `1`, then `2`, then `3`.

The letter does not determine the digit. Use these mappings as checks:

- Additive or widened public API: `A2`
- Compatible runtime correction with unchanged API: `B2`
- New installation target or distribution artifact: `C2`
- Unchanged-result internal optimization: `C3`
- Test rearrangement or behavior-preserving packaging migration: `C3`

## Order and summarize the bullets

Sort the bullets using this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Multiple changes may share a code. For changes with the same code, preserve their relative order from the pending-change list.

Write a concise summary of only the supplied change. Put identifiers in backticks where appropriate. Do not invent compatibility, behavior, or API claims that the pending-change information does not support.

## Set the impact summary

Set `Impact` to the smallest digit appearing in any bullet code, regardless of letter:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Before returning the entry, verify that every pending change appears exactly once, every code follows both classification rules, bullets use the required order, `Impact` contains the smallest bullet digit, all required blank lines are present, and the exact trailer is the final line.