---
name: impact-log
description: Use this guide when converting a supplied release version, date, and pending-change list into one classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every pending change once and only once. Do not add commentary, a code fence, or an extra heading.

The finished entry must contain no blank lines and must use this exact layout:

## [VERSION] - YYYY-MM-DD
Impact: N
- [CODE] Change description.
<!-- stl-impact: v1 -->

Replace each placeholder with the supplied information.

## 1. Write the heading

Use exactly:

`## [VERSION] - YYYY-MM-DD`

- Keep the literal `##`.
- Copy the supplied version exactly and enclose it in square brackets.
- Copy the supplied date in `YYYY-MM-DD` format.
- Put `Impact: N` immediately on the next line.

## 2. Classify every pending change

Assign exactly one two-character code to each change. Choose its letter and digit independently:

- The letter identifies the area affected.
- The digit identifies the change’s impact.

Classify the actual effect, not labels such as “fix,” “internal,” “migration,” “optimization,” or “refactor.”

### Choose the letter

Apply these tests in order and stop at the first match:

1. Use `A` if the published public API shape changes.

   Public API shape includes exported names, public availability, signatures, parameters, documented accepted parameter types, return types, and other published types.

   Use `A` for changes such as:

   - Adding, removing, or renaming an exported name.
   - Adding or removing a parameter.
   - Broadening or narrowing a parameter’s documented accepted types.
   - Changing a published return type.

   Do not use `A` for a bug fix that only changes what an existing call returns or raises. That is `B`.

2. Otherwise, use `B` if runtime behavior or a runtime characteristic changes while the public API shape remains unchanged.

   This includes:

   - Returned values or raised errors.
   - Parsing, validation, or formatting behavior.
   - Additional runtime input syntax.
   - Execution speed, import or startup time, memory use, or caching behavior.
   - Runtime optimizations that preserve results and signatures.

   Runtime work remains `B` when described as internal, deferred, cached, optimized, or refactored. An output-preserving cache or import-time improvement is `B`, not `C`.

3. Otherwise, use `C` for packaging or project-support work.

   This includes:

   - Installation and dependency handling.
   - Vendored dependencies and distribution contents.
   - Typing metadata and other shipped package metadata.
   - Build and packaging configuration.
   - Documentation, docstrings, tests, development tooling, and maintenance work with no runtime effect.

If multiple letters seem applicable, use the first matching letter: `A` before `B` before `C`.

### Choose the digit

Apply these tests in order and stop at the first match:

1. Use `1` if an existing supported use can produce a different result, raise a different error, fail, or require caller changes.

   This includes:

   - Removing or incompatibly changing public API.
   - Narrowing previously supported inputs.
   - Behavior-changing bug fixes.
   - Any other result or error change for an existing supported call.
   - Incompatible installation, packaging, or dependency changes.

   A corrected result is still a different result. Therefore, a bug fix that changes an existing call’s result or error uses `1`.

2. Otherwise, use `2` if the change is compatible and externally observable.

   This includes:

   - A new public API or compatible capability.
   - Broader accepted inputs.
   - A compatible runtime extension.
   - A compatible installation or packaging fix.
   - A dependency-distribution change.
   - New or changed shipped artifacts, typing metadata, or package metadata.
   - Observable improvements to runtime speed, import time, memory use, or caching that preserve existing results.

3. Otherwise, use `3` if package callers cannot observe the change.

   This includes:

   - Documentation and docstring changes.
   - Tests and development-tooling changes.
   - Refactoring with no effect on results, errors, performance, memory, installation, or shipped artifacts.
   - Build-configuration migration that leaves installation and distribution contents unchanged.

Do not use `3` merely because a change is described as internal. Internal work affecting speed, import time, memory, or caching is observable and uses `2` when existing results remain unchanged.

Use the lowest applicable digit: `1` before `2` before `3`. When genuinely uncertain between digits, choose the lower digit.

### Classification reference

| Actual effect | Code |
|---|---|
| Remove or incompatibly change published API | `A1` |
| Add exported API or compatibly broaden documented parameter types | `A2` |
| Change an existing call’s result or error, including through a bug fix | `B1` |
| Compatibly extend runtime behavior without changing API shape | `B2` |
| Improve runtime, import, memory, or caching characteristics without changing results | `B2` |
| Break supported installation or dependency use | `C1` |
| Fix installation, redistribute a dependency, or add shipped metadata | `C2` |
| Change only documentation, tests, development tools, or non-observable build configuration | `C3` |

## 3. Write one bullet per change

Use exactly:

`- [CODE] Description.`

For each bullet:

- Begin with a hyphen and one space.
- Put the two-character code inside square brackets.
- Put one space after the closing bracket.
- Describe only that pending change.
- Preserve the supplied technical facts; do not invent effects.
- End the description with a period.
- Do not write forms such as `A1 Description`, `- A1 Description`, or `[A1]: Description`.
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

Ignore the letters when calculating impact. The value of `N` must be a digit that appears in at least one bullet code.

## 6. Add the trailer

Put this exact line immediately after the final bullet:

`<!-- stl-impact: v1 -->`

The trailer must be the final line. Do not insert a blank line before it or any content after it.

Before submitting, verify:

- There is exactly one release heading.
- `Impact: N` is directly below the heading.
- Every pending change appears in exactly one bullet.
- Every bullet uses `- [CODE] Description.`
- Every description ends with a period.
- The bullets follow the required code order.
- Equal-code bullets retain their original pending-change order.
- `N` is the lowest digit used by any bullet.
- The entry contains no blank lines.
- The trailer is the final line.