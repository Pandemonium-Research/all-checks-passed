---
name: impact-log
description: Use when given a release version, release date, and pending-change list to produce exactly one classified, stably sorted, machine-parseable release-notes entry in the project's impact-log format.
---

# Release notes

Produce exactly one release entry. Output only the entry, without commentary or a Markdown code fence.

Treat each supplied pending-change item as one indivisible unit:

- Create exactly one bullet for each item.
- Do not merge, split, omit, or duplicate items.
- Preserve every material fact from the item.
- Do not invent effects, compatibility claims, or causes.

## Required layout

Use this exact layout:

    ## [VERSION] - YYYY-MM-DD
    Impact: DIGIT

    - [CODE] Change description.
    - [CODE] Change description.

    <!-- stl-impact: v1 -->

Apply these formatting rules:

- Copy the supplied version exactly inside square brackets. Never infer or alter it based on impact.
- Copy the supplied date in `YYYY-MM-DD` form.
- Put `Impact: DIGIT` immediately below the heading.
- Begin every bullet with exactly one code in square brackets.
- Leave one blank line after the impact line and one blank line before the trailer.
- Use `<!-- stl-impact: v1 -->` exactly.
- Make the trailer the final line, with nothing after it.

## Classify each item

Consider every effect described by the item, then select its letter and digit independently:

1. Select the first applicable letter in this order: `A`, `B`, `C`.
2. Select the lowest applicable digit in this order: `1`, `2`, `3`.
3. Combine them into one code, such as `[A2]`.

Do not copy the release-level impact digit onto every bullet. The effects determining the letter and digit may be different.

### Select the letter

Use `A` if any part of the item changes the public API or typing surface. This includes:

- Public names, modules, functions, classes, or exception types.
- Signatures, parameters, defaults, return types, return shapes, or eager-versus-lazy evaluation behavior.
- Public annotations or metadata that exposes shipped types to type checkers.

Additive public exposure still uses `A`. For example, adding a public module, public exception type, optional parameter, or typing metadata is an API change even when existing calls continue to work.

Otherwise, use `B` if any part changes observable runtime behavior. This includes:

- Results, exceptions, exit status, or side effects.
- Execution or import time.
- Memory use, cache growth, or other resource behavior.

Use `B` for an internal implementation change that alters performance or resource use even when functional output is unchanged. Bounding a cache, reducing memory growth, or deferring work is not an unobservable refactor.

Otherwise, use `C` for changes limited to:

- Internals with unchanged behavior, performance, and resource use.
- Build or packaging configuration.
- Dependencies.
- Tooling, tests, or CI.
- Documentation.

Packaging and dependency changes remain `C`; their digit records whether consumers can observe an installation or distribution effect.

For every item, enforce this letter precedence:

`A` before `B` before `C`.

Therefore, an item that adds an optional public parameter and also improves performance uses `A`, not `B`.

### Select the digit

Use `1` if any part is breaking: previously supported, correct usage can now fail, become invalid, or produce a different result. This includes:

- Renaming or removing public API.
- Adding a required argument.
- Making an incompatible type or return-shape change.
- Changing the result for valid, supported input.

Treat a changed result for valid, supported input as breaking even when the new result sounds preferable. Use `2` instead only when the supplied item explicitly says the previous behavior was a bug, defect, error, or unsupported behavior. Do not infer that merely from wording such as “now,” “no longer,” or a stated benefit.

Otherwise, use `2` if consumers can observe a compatible change while supported, correct existing usage retains the same meaning. This includes:

- An additive public API or typing feature.
- An optional parameter whose default preserves existing behavior.
- An explicitly identified defect correction.
- A nonbreaking performance, timing, memory, cache, or resource change.
- A consumer-visible installation or distribution change.

Additive exposure of public names, modules, exception types, or shipped typing information is normally `A2`, not `A1`. An explicitly identified correction to an erroneous exit status, result, or exception is normally `B2`, not `B1`.

Otherwise, use `3` when supported consumers cannot observe the change. This normally includes:

- Documentation-only changes, including docstrings and examples.
- Test-only or CI-only changes.
- Development-only dependency changes.
- Behavior-preserving refactoring with no performance, resource, typing, installation, or distribution effect.

Do not select `3` merely because functional output is unchanged. Timing, memory, cache behavior, installation, distribution, and typing exposure are observable.

For every item, enforce this digit precedence:

`1` before `2` before `3`.

## Classification checks for common edge cases

Apply these mappings before sorting:

- Additive public API, public type exposure, or typing metadata: `A2`.
- Public rename, removal, or incompatible return-shape change: `A1`.
- Optional public parameter with an unchanged default behavior: `A2`.
- API addition combined with a performance improvement: `A2`.
- Changed result for valid supported input, with no explicit defect statement: `B1` unless an `A` effect also applies.
- Explicit correction of erroneous runtime behavior: `B2` unless an `A` effect also applies.
- Observable execution-time, import-time, memory, or cache change: `B2` when nonbreaking.
- Consumer-visible runtime dependency, packaging, installation, or distribution change: `C2`.
- Documentation-only or development-only change: `C3`.

## Sort the bullets

After assigning every code, sort the bullets by this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For items with the same code, preserve their relative order from the supplied pending-change list.

## Calculate the impact summary

Set `Impact` to the lowest digit present in any bullet code:

- If any bullet ends in `1`, write `Impact: 1`.
- Otherwise, if any bullet ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore the letters when calculating `Impact`.

## Final verification

Before returning the entry, verify that:

- The version and date exactly match the supplied values.
- Every supplied item appears exactly once in one bullet.
- Every material fact from each item is preserved.
- Every bullet begins with exactly one valid code.
- Public API and typing effects take precedence over runtime and internal effects.
- Additive public API and typing changes normally use `A2`.
- Observable performance and resource changes use `B`, not `C`.
- Changed results for valid supported input use digit `1` unless the old behavior was explicitly identified as erroneous or unsupported.
- Explicit defect corrections use digit `2` when supported, correct existing usage is unaffected.
- Consumer-visible packaging and dependency changes use `C2`.
- Documentation-only and development-only changes use `C3`.
- Bullets follow the required code order and remain stable within each code.
- `Impact` equals the lowest digit used by any bullet.
- The exact trailer is the final line.