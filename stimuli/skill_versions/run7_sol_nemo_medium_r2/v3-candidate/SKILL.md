---
name: impact-log
description: Use this guide when converting a supplied release version, date, and pending-change list into one classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every pending change once and only once. Do not add an introduction, explanation, code fence, or second heading.

The completed entry must contain no blank lines and must use this exact layout:

## [VERSION] - YYYY-MM-DD
Impact: N
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace the placeholders with the supplied release information.

## 1. Write the heading

Use exactly:

`## [VERSION] - YYYY-MM-DD`

- Keep the literal `##`.
- Put the supplied version in square brackets.
- Copy the supplied date in `YYYY-MM-DD` format.
- Put `Impact: N` immediately on the next line.

## 2. Classify every pending change

Assign exactly one two-character code to each change. The letter and digit answer different questions:

- The letter identifies what changed.
- The digit identifies how disruptive or observable the change is.

Classify the actual effect, not words such as “fix,” “internal,” “migration,” or “refactor.”

### Choose the letter

Apply these tests in order and stop at the first match:

1. Use `A` if the published public API shape changes.

   Public API shape includes exported names, public availability, function or method signatures, parameters, accepted parameter types, return types, and other published types.

   Typical `A` changes include:

   - Adding, removing, or renaming an exported public name.
   - Adding or removing a parameter.
   - Widening or narrowing the documented types accepted by a parameter.
   - Changing a published return type.

   A bug fix that only changes the result of an existing call is not `A`; use `B`.

2. Otherwise, use `B` if an existing runtime operation or runtime characteristic changes.

   This includes:

   - Returned values, errors, parsing, validation, or formatting.
   - Support for additional runtime input syntax when the public API shape is unchanged.
   - Execution speed, import or startup time, memory use, and caching behavior.
   - Runtime optimizations whose results and signatures remain unchanged.

   Runtime work does not become `C` merely because its implementation is described as internal, deferred, cached, or refactored.

3. Otherwise, use `C` for packaging or project-support work.

   This includes:

   - Installation behavior, dependencies, vendored dependencies, and distribution contents.
   - Typing metadata and other shipped package metadata.
   - Build configuration and packaging configuration.
   - Documentation, docstrings, tests, development tooling, and maintenance work with no runtime effect.

If several letters appear applicable, precedence is `A` before `B` before `C`.

### Choose the digit independently

Apply these tests in order and stop at the first match:

1. Use `1` if an existing supported use can produce a different result, raise a different error, fail, or require caller changes.

   This includes behavior-changing bug fixes. A corrected result is still a changed result for an existing call, so it is `1`.

   It also includes incompatible public API, installation, or packaging changes.

2. Otherwise, use `2` if the change is compatible and externally observable.

   This includes:

   - A new public API or other compatible capability.
   - Broader accepted inputs.
   - A compatible installation or packaging fix.
   - New or changed shipped artifacts, typing metadata, or dependency distribution.
   - Observable improvements to execution speed, import time, memory use, or caching while existing results remain unchanged.

3. Otherwise, use `3` if package callers cannot observe the change.

   This includes:

   - Documentation and docstring changes.
   - Tests and development-tooling changes.
   - Refactoring with no effect on results, errors, performance, memory, installation, or shipped artifacts.
   - Build-configuration migration that leaves installation and distribution contents unchanged.

Do not use `3` solely because a change is called internal. Cache bounds, deferred imports, and similar implementation changes are `2` when they observably affect time or memory.

Use the lowest applicable digit: `1` before `2` before `3`. When genuinely uncertain between digits, choose the lower digit.

### Classification reference

| Change effect | Code |
|---|---|
| Remove or incompatibly change published API | `A1` |
| Add an exported API or compatibly widen accepted parameter types | `A2` |
| Change an existing call’s result or error, including a bug fix | `B1` |
| Compatibly extend runtime behavior without changing API shape | `B2` |
| Improve runtime, import, memory, or cache characteristics without changing results | `B2` |
| Break supported installation or dependency use | `C1` |
| Fix installation, change dependency distribution, or add shipped metadata | `C2` |
| Change only documentation, tests, development tools, or non-observable build configuration | `C3` |

## 3. Write one bullet per change

Use exactly:

`- [CODE] Description.`

For every bullet:

- Begin with a hyphen and one space.
- Put the two-character code inside square brackets.
- Put one space after the closing bracket.
- Describe only that pending change.
- End the description with a period.
- Do not use forms such as `A1 Description`, `[A1]: Description`, or `- A1 Description`.
- Do not omit, combine, or duplicate changes.

## 4. Sort the bullets

Sort by this fixed code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes receive the same code, preserve their original order from the pending-change list.

## 5. Calculate the impact summary

Set `N` to the lowest digit that appears in any bullet code.

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore the letters when calculating impact. The summary digit must appear in at least one bullet code.

## 6. Add the trailer

Put this exact line immediately after the final bullet:

`<!-- stl-impact: v1 -->`

The trailer must be the final line. Do not insert a blank line before it or any content after it.

Before submitting, verify:

- There is exactly one release heading.
- `Impact: N` is directly below the heading.
- Every pending change appears in exactly one bullet.
- Every bullet uses `- [CODE] Description.`
- Each description ends with a period.
- The bullets follow the required code order.
- Equal-code bullets retain their original order.
- `N` is the lowest digit used by any bullet.
- The entry contains no blank lines.
- The trailer is the final line.