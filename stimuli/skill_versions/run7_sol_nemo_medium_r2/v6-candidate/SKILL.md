---
name: impact-log
description: Use this guide when given a release version, date, and pending-change list to produce one classified, sorted, parser-compatible release-not notes entry.
---

# Release notes

Produce exactly one release entry containing every pending change exactly once. Output no introduction, explanation, code fence, or extra heading.

The finished entry must contain no blank lines and must have this structure:

## [VERSION] - YYYY-MM-DD
Impact: N
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace the placeholders with the supplied release information.

## 1. Classify every change

Assign each pending change exactly one two-character code. Determine the letter and digit independently from the change's actual effect, not from words such as “fix,” “internal,” “migration,” “optimization,” or “refactor.”

### Choose the letter

Apply these tests in order. Stop at the first match.

1. Use `A` when the published public API shape changes.

   This includes changes to:

   - Exported public names or their availability.
   - Function or method signatures.
   - Parameters or their documented accepted types.
   - Published return types or other public types.

   Adding an exported helper or widening a parameter's documented accepted types is `A`. A bug fix that changes only the result or error of an existing call is not `A`; it is `B`.

2. Otherwise, use `B` when runtime behavior or a runtime characteristic changes.

   This includes changes to:

   - Returned values, raised errors, validation, parsing, or formatting.
   - Runtime input handling without a public API-shape change.
   - Execution speed, import or startup time, memory use, or caching.
   - Runtime implementation that observably changes performance while preserving results and signatures.

   Deferred imports, new caches, and cache-policy changes are `B`, even when described as internal or output-preserving.

3. Otherwise, use `C` for packaging or project-support work.

   This includes:

   - Installation and dependency handling.
   - Vendored dependencies and distribution contents.
   - Typing metadata and other shipped package metadata.
   - Build or packaging configuration.
   - Documentation, docstrings, tests, and development tooling.

If multiple letters appear applicable, use the earliest: `A` before `B` before `C`.

### Choose the digit

Apply these tests in order. Stop at the first match.

1. Use `1` when an existing supported use can break, require caller changes, raise a different error, or produce a different result.

   This includes:

   - Removing or incompatibly changing public API.
   - Narrowing supported inputs.
   - Changing the result or error of an existing supported call.
   - Behavior-changing bug fixes.
   - Incompatible installation, packaging, or dependency changes.

   A corrected result is still a different result. Therefore, a bug fix that changes an existing call's output or error uses `1`.

2. Otherwise, use `2` when the change is compatible and externally observable.

   This includes:

   - Adding public API or another compatible capability.
   - Broadening accepted inputs.
   - Compatibly extending runtime behavior.
   - Fixing installation or packaging.
   - Redistributing or vendoring a dependency.
   - Adding or changing shipped artifacts, typing metadata, or package metadata.
   - Changing runtime speed, import time, memory use, or caching while preserving existing results.

3. Otherwise, use `3` when package callers cannot observe the change.

   This includes:

   - Documentation or docstring changes.
   - Tests or development-tooling changes.
   - Refactoring with no effect on results, errors, performance, memory, installation, or shipped artifacts.
   - Build-configuration migration that leaves installation behavior and distribution contents unchanged.

Do not use `3` merely because a change is called internal. If internal work affects runtime speed, import time, memory, or caching, use `2` when it preserves existing results.

If multiple digits appear applicable, use the lowest: `1` before `2` before `3`. When genuinely uncertain, choose the lower digit.

### Classification reference

| Actual effect | Code |
|---|---|
| Remove or incompatibly change published API | `A1` |
| Add exported API or compatibly broaden a documented parameter type | `A2` |
| Change an existing call's result or error, including through a bug fix | `B1` |
| Compatibly extend runtime behavior without changing API shape | `B2` |
| Change runtime, import, memory, or caching characteristics while preserving results | `B2` |
| Break supported installation or dependency use | `C1` |
| Fix packaging, redistribute a dependency, or add shipped metadata | `C2` |
| Change only documentation, tests, development tools, or non-observable build configuration | `C3` |

## 2. Sort the changes

Sort all changes by this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes have the same code, retain their original order from the pending-change list.

## 3. Calculate the impact

Set `N` to the lowest digit used by any bullet:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only the code digits for this calculation. Letters do not affect the impact. The selected digit must appear in at least one bullet code.

## 4. Render the entry

Write the heading exactly as:

`## [VERSION] - YYYY-MM-DD`

- Keep the literal `##`.
- Copy the supplied version exactly and enclose it in square brackets.
- Copy the supplied date in `YYYY-MM-DD` format.
- Write `Impact: N` on the immediately following line.

Write one line per sorted change using exactly:

`- [CODE] Description.`

For every bullet:

- Begin with a hyphen followed by one space.
- Enclose the two-character code in square brackets.
- Put one space after the closing bracket.
- Describe only that pending change.
- Preserve the supplied technical facts and do not invent effects.
- End the description with a period.
- Do not omit, combine, or duplicate changes.
- Do not use forms such as `A1 Description`, `- A1 Description`, or `[A1]: Description`.

Immediately after the final bullet, write:

`<!-- stl-impact: v1 -->`

The trailer must be the final line. Do not insert a blank line before it or place any content after it.

## Final verification

Before submitting, confirm all of the following:

- There is exactly one release heading.
- The supplied version and date are copied correctly.
- `Impact: N` is directly below the heading.
- Every pending change appears in exactly one bullet.
- Every bullet uses `- [CODE] Description.`
- Every description ends with a period.
- The bullets follow the required code order.
- Equal-code bullets retain their original order.
- `N` is the lowest digit appearing in any bullet code.
- The entry contains no blank lines.
- The trailer is the final line.