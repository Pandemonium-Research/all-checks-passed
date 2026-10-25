---
name: impact-log
description: Use when given a release version, release date, and pending changes to produce exactly one classified, stably sorted, machine-parseable release-notes entry in the project's impact-log format.
---

# Release notes

Produce exactly one release entry. Output only the entry, without commentary or a Markdown code fence.

Create exactly one bullet for each supplied pending-change item. Do not merge items, split an item into multiple bullets, omit an item, or repeat an item. Preserve every material fact from the supplied description.

## Required layout

Use this exact layout:

    ## [VERSION] - YYYY-MM-DD
    Impact: DIGIT

    - [CODE] Change description.
    - [CODE] Change description.

    <!-- stl-impact: v1 -->

Follow these formatting rules:

- Copy the supplied version exactly inside square brackets. Never infer or alter it based on impact.
- Copy the supplied date in `YYYY-MM-DD` form.
- Put `Impact: DIGIT` immediately below the heading.
- Start every bullet with exactly one code in square brackets.
- Leave one blank line after the impact line and one blank line before the trailer.
- Use `<!-- stl-impact: v1 -->` exactly.
- Make the trailer the final line, with nothing after it.

## Classify each pending-change item

Assign one letter and one digit to each item. Evaluate all effects described by that item before selecting its code.

Select the letter and digit independently:

1. Select the highest-precedence applicable letter: `A`, then `B`, then `C`.
2. Select the lowest applicable digit: `1`, then `2`, then `3`.
3. Combine them into one code, such as `[A2]`.

Do not assign a code based only on the item's implementation details, its most prominent sentence, or the release-level impact.

### Select the letter

- `A` — The item changes the public API surface seen by consumers or type checkers. This includes public names or modules, signatures, parameters, return types, public exception types, annotations, and typing metadata.
- `B` — The item changes observable runtime behavior of existing functionality without changing the public API surface. This includes results, exceptions, exit status, side effects, timing, memory use, and other resource behavior.
- `C` — The item affects only internals, build, packaging, dependencies, tooling, tests, CI, or documentation and has no `A` or `B` effect.

Apply these distinctions:

- Adding a public symbol, public module, optional parameter, or typing exposure is `A`, even when it is backward compatible.
- Renaming or removing a public symbol, or changing a public return type or shape, is `A`.
- A performance or memory-use change is `B`, even when returned output is unchanged and the implementation is internal.
- A packaging or dependency change is `C` unless it also changes the public API or runtime behavior.
- A documentation-only, test-only, or CI-only change is `C`.

If an item has multiple effects, use the first applicable letter in this order:

`A`, then `B`, then `C`.

For example, an item that both adds a public parameter and improves runtime performance uses `A`, because the public API effect takes precedence.

### Select the digit

- `1` — Breaking: supported, correct existing usage can now fail, become invalid, or produce a different result.
- `2` — Compatible and observable: the item adds capability, corrects erroneous or unsupported behavior, or improves an observable characteristic while supported, correct existing usage continues to work with the same meaning.
- `3` — Unobservable to consumers in supported use.

Apply these distinctions:

- A rename, removal, newly required argument, incompatible type change, or changed result for valid supported input is `1`.
- Treat a changed result for valid supported input as `1` even when the new result is described as more useful or more correct, unless the old result was explicitly erroneous or unsupported.
- An additive public API or typing feature is normally `2`.
- A defect correction involving invalid input or otherwise erroneous behavior is `2` when supported, correct existing usage is unaffected.
- A timing, performance, memory, installation, or other consumer-visible improvement is `2`, even when functional output is unchanged.
- A dependency or packaging change is `2` when consumers can observe an installation or distribution change; otherwise it is `3`.
- Documentation-only, test-only, CI-only, and behavior-preserving refactoring changes are normally `3`.

If an item has multiple impacts, use the lowest applicable digit:

`1`, then `2`, then `3`.

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

Before returning the entry, verify all of the following:

- The version and date exactly match the supplied values.
- There is exactly one bullet for each supplied pending-change item.
- Every bullet begins with exactly one valid code.
- Public API effects take precedence over runtime and internal effects.
- Observable performance and resource changes are classified as `B`, not `C`.
- Additive public API changes are classified as `A2`, not as runtime changes or breaking changes.
- Changed results for valid supported input are classified as breaking unless the prior behavior was explicitly erroneous or unsupported.
- Documentation-only changes use digit `3`.
- Bullets follow the required code order and remain stable within each code.
- `Impact` equals the lowest bullet-code digit.
- The exact trailer is the final line.