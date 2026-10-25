---
name: impact-log
description: Use this guide to convert a supplied release version, date, and pending-change list into one correctly classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every pending change exactly once. Do not add an introduction, explanation, code fence, or extra heading.

The completed entry must contain no blank lines and must use this exact structure:

## [VERSION] - YYYY-MM-DD
Impact: N
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace the placeholders with the supplied release information.

## 1. Write the heading

Write:

`## [VERSION] - YYYY-MM-DD`

- Keep the literal `##`.
- Copy the supplied version exactly and enclose it in square brackets.
- Copy the supplied date in `YYYY-MM-DD` format.
- Write `Impact: N` immediately below the heading.

## 2. Classify every pending change

Assign exactly one two-character code to each change. Choose the letter and digit independently:

- The letter identifies what changed.
- The digit identifies whether the change is breaking, compatibly observable, or unobservable.

Classify the change's actual effect. Do not classify it from labels such as “fix,” “internal,” “migration,” “optimization,” or “refactor.”

### Choose the letter

Apply these tests in order. Stop at the first match.

1. Use `A` when the published public API shape changes.

   Public API shape includes:

   - Exported public names and their availability.
   - Function or method signatures.
   - Parameters and their documented accepted types.
   - Published return types and other public types.

   Examples include adding or removing an exported helper, adding or removing a parameter, and widening or narrowing a parameter's accepted types.

   A bug fix that changes only the result of an existing call is not `A`; use `B`.

2. Otherwise, use `B` when an existing runtime operation or runtime characteristic changes.

   This includes:

   - Returned values, raised errors, validation, parsing, or formatting.
   - Additional runtime input syntax without a public API-shape change.
   - Execution speed, import or startup time, memory use, or caching.
   - Runtime optimizations that preserve results and signatures.

   Deferred imports, new caches, and cache-policy changes are `B`, even when described as internal and even when output is unchanged.

3. Otherwise, use `C` for packaging or project-support changes.

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
   - Behavior-changing bug fixes.
   - Other changes to the result or error of an existing supported call.
   - Incompatible installation or packaging changes.

   A corrected result is still a different result, so a bug fix that changes an existing call's output is `1`.

2. Otherwise, use `2` when the change is compatible and externally observable.

   This includes:

   - Adding public API or other compatible capability.
   - Broadening accepted inputs.
   - Compatible runtime extensions.
   - Installation or packaging fixes.
   - Dependency-distribution changes.
   - New or changed shipped artifacts or typing metadata.
   - Runtime, import-time, memory, or caching improvements that preserve existing results.

3. Otherwise, use `3` when package callers cannot observe the change.

   This includes:

   - Documentation and docstring changes.
   - Tests and development-tooling changes.
   - Refactoring with no effect on results, errors, performance, memory, installation, or shipped artifacts.
   - Build-configuration migration that leaves installation and distribution contents unchanged.

Do not use `3` merely because a change is called internal. An internal change affecting runtime speed, import time, memory, or caching is observable and therefore uses `2` when existing behavior is preserved.

If multiple digits appear applicable, use the lowest: `1` before `2` before `3`. When genuinely uncertain, choose the lower digit.

### Classification reference

| Actual effect | Code |
|---|---|
| Remove or incompatibly change published API | `A1` |
| Add exported API or compatibly broaden documented parameter types | `A2` |
| Change an existing call's result or error, including through a bug fix | `B1` |
| Compatibly extend runtime behavior without changing API shape | `B2` |
| Improve runtime, import, memory, or caching characteristics without changing results | `B2` |
| Break supported installation or dependency use | `C1` |
| Fix installation, redistribute a dependency, or add shipped metadata | `C2` |
| Change only documentation, tests, development tools, or non-observable build configuration | `C3` |

## 3. Write one bullet per change

Use exactly:

`- [CODE] Description.`

For every bullet:

- Begin with a hyphen and one space.
- Put the two-character code inside square brackets.
- Put one space after the closing bracket.
- Describe only that pending change.
- Preserve the supplied technical facts; do not invent additional effects.
- End the description with a period.
- Do not use forms such as `A1 Description`, `- A1 Description`, or `[A1]: Description`.
- Do not omit, combine, or duplicate pending changes.

## 4. Sort the bullets

Sort by this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes have the same code, preserve their original order from the pending-change list.

## 5. Calculate the impact summary

Set `N` to the lowest digit appearing in any bullet code:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only the digits when calculating impact; letters do not affect it. The summary digit must appear in at least one bullet code.

## 6. Add the trailer

Place this exact line immediately after the final bullet:

`<!-- stl-impact: v1 -->`

The trailer must be the final line. Do not put a blank line before it or any content after it.

Before submitting, verify:

- There is exactly one release heading.
- `Impact: N` is directly below the heading.
- Every pending change appears in exactly one bullet.
- Every bullet uses `- [CODE] Description.`
- Every description ends with a period.
- The bullets follow the required code order.
- Changes with equal codes retain their original order.
- `N` is the lowest digit used by any bullet.
- The entry contains no blank lines.
- The trailer is the final line.