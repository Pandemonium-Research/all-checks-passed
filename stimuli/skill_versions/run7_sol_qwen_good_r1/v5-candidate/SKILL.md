---
name: impact-log
description: Use when given a release version, release date, and list of pending changes to produce exactly one classified, stably sorted, machine-parseable release-notes entry in the project's impact-log format.
---

# Release notes

Produce exactly one release entry. Output only the entry, without commentary or a Markdown code fence.

Treat each supplied pending-change item as one unit:

- Create exactly one bullet for each item.
- Do not merge, split, omit, or duplicate items.
- Preserve every material fact in the item's description.
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

Select the letter and digit independently after considering every effect described by the item:

1. Select the first applicable letter in this order: `A`, `B`, `C`.
2. Select the lowest applicable digit in this order: `1`, `2`, `3`.
3. Combine them into one code, such as `[A2]`.

Do not copy the release-level impact digit onto each bullet.

### Select the letter

Use `A` if any part of the item changes the public API or typing surface. This includes:

- Public names, modules, functions, classes, or exception types.
- Signatures, parameters, defaults, return types, return shapes, or evaluation behavior such as returning an iterator instead of a collection.
- Public annotations or metadata that makes shipped types visible to type checkers.

Adding a public symbol, public module, optional parameter, or typing exposure is `A` even when existing calls continue to work.

Otherwise, use `B` if any part changes observable runtime behavior. This includes:

- Results, exceptions, exit status, or side effects.
- Execution or import time.
- Memory use, cache growth, or other resource behavior.

Use `B` for an internal implementation change that alters performance or resource use even when functional output is unchanged. For example, bounding a previously unbounded cache is a runtime resource change, not an unobservable internal change.

Otherwise, use `C` for changes limited to:

- Internals with unchanged functional, performance, and resource behavior.
- Build or packaging configuration.
- Dependencies.
- Tooling, tests, or CI.
- Documentation.

Packaging and dependency changes remain `C`; use the digit to record whether consumers can observe their installation or distribution effect.

For a compound item, apply letter precedence to the whole item:

`A`, then `B`, then `C`.

Thus, a compatible public-API addition that also improves performance uses `A`, not `B`.

### Select the digit

Use `1` if any part is breaking: previously supported, correct usage can now fail, become invalid, or produce a different result. This includes:

- Renaming or removing a public API.
- Adding a required argument.
- Making an incompatible type or return-shape change.
- Changing the result for valid, supported input.

Treat a changed result for valid, supported input as `1` even when the new result sounds preferable. Use `2` instead only when the supplied item explicitly identifies the old behavior as erroneous or unsupported.

Otherwise, use `2` if consumers can observe a compatible change while supported, correct existing usage retains the same meaning. This includes:

- An additive public API or typing feature.
- An optional parameter whose default preserves existing behavior.
- An explicitly identified defect correction.
- A performance, import-time, memory, cache, or other resource improvement.
- A consumer-visible installation or distribution change.

New public exposure of existing types is additive and therefore normally `A2`, not breaking. A corrected erroneous exit status or other explicitly identified defect is normally `B2`, not breaking.

Otherwise, use `3` when supported consumers cannot observe the change. This normally includes:

- Documentation-only changes.
- Test-only or CI-only changes.
- Development-only dependency changes.
- Behavior-preserving refactoring with no performance, resource, typing, installation, or distribution effect.

Do not select `3` merely because functional output is unchanged. Timing, memory use, installation, distribution, and typing exposure are observable effects.

For a compound item, select the lowest digit applicable to any of its effects:

`1`, then `2`, then `3`.

The effect that determines the digit may differ from the effect that determines the letter.

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
- Observable performance and resource changes use `B`, not `C`.
- Additive public API and typing changes normally use `A2`.
- Changed results for valid supported input use digit `1` unless the old behavior was explicitly erroneous or unsupported.
- Documentation-only and development-only changes use digit `3`.
- Consumer-visible packaging or dependency changes use `C2`; unobservable or development-only ones use `C3`.
- Bullets follow the required code order and remain stable within each code.
- `Impact` equals the lowest digit used by any bullet.
- The exact trailer is the final line.