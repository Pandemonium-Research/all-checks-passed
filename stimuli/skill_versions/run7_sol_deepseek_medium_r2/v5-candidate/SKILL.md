---
name: impact-log
description: Use when given a version, release date, and pending project changes to produce one classified, sorted, machine-parseable impact-log release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every supplied change exactly once. Do not invent, omit, combine, or split changes. Preserve each change's technical meaning.

Output only the completed entry, without a code fence or commentary, using this exact layout:

```text
## [X.Y.Z] - YYYY-MM-DD
Impact: N

- [LD] Description of one change.
- [LD] Description of another change.

<!-- stl-impact: v1 -->
```

Replace every placeholder with the supplied version, supplied date, calculated impact, classification code, or change description.

## Classify each change

Begin every bullet with one `[LD]` code. Determine the letter and digit separately from the change's effects. Do not classify from how disruptive the wording sounds.

If one change has multiple effects, choose the earliest applicable letter (`A` before `B` before `C`) and the lowest applicable digit (`1` before `2` before `3`).

### Choose the letter

Apply these tests in order:

1. If the public contract changes, use `A`.
2. Otherwise, if the functional runtime behavior of an existing public operation changes, use `B`.
3. Otherwise, use `C`.

#### `A` — Public contract change

Use `A` for any change to the interface consumers can use or depend on, including:

- Adding, removing, or renaming public functionality
- Adding, removing, or changing an exported name or public import path
- Changing a callable signature
- Broadening or narrowing accepted inputs or argument types
- Changing a return type
- Adding, changing, or removing public annotations, type stubs, or typing markers such as `py.typed`
- Adding or dropping support for a runtime version

A contract change remains `A` when it is backward-compatible. New public functionality and broader accepted inputs are `A2`, not `B2`. A return-type change is `A`, even if the written parameters are unchanged.

#### `B` — Runtime behavior change without a contract change

Use `B` when an existing public operation retains the same contract but its functional result changes, including:

- Returning different values
- Producing different rendered or normalized output
- Changing parsing, formatting, or normalization behavior
- Adding, removing, or correcting a runtime error
- Fixing incorrect behavior in an existing public operation

Do not use `B` merely because runtime implementation code changed. If supported inputs, return types, results, and errors remain functionally equivalent, use `C`.

#### `C` — Implementation or maintenance only

Use `C` when neither the public contract nor functional runtime results change, including:

- Internal refactors, caches, or equivalent algorithm replacements
- Performance improvements with identical functional behavior
- Dependency or vendoring changes with no consumer-visible effect
- Build or packaging migrations that preserve installation behavior and runtime support
- Tooling, tests, and documentation

Classify effects, not filenames or work categories. Packaging work that drops runtime support is `A`; packaging work that preserves support is `C`.

### Choose the digit

Apply these tests independently of the letter:

1. If previously supported usage can become incompatible, use `1`.
2. Otherwise, if the change is additive, broadens support, or corrects intended behavior, use `2`.
3. Otherwise, use `3`.

#### `1` — Breaking

Use `1` when previously supported caller code can stop working, stop importing, raise a new error, or receive an incompatible result.

This includes:

- Removing or renaming public API
- Narrowing accepted inputs
- Incompatibly changing a signature or return type
- Dropping a supported runtime
- Intentionally changing established behavior incompatibly

#### `2` — Compatible or corrective

Use `2` when the change adds capability, broadens supported use, or corrects intended behavior without invalidating supported correct usage.

This includes:

- Adding public API
- Broadening accepted inputs
- Adding compatible consumer-visible typing information
- Fixing a runtime bug

A correction to documented or intended behavior is normally `2`, even when code that relied on the bug observes a different result.

#### `3` — Non-observable maintenance

Use `3` only when the public contract and functional runtime results are unchanged. Internal refactors, equivalent cache replacements, performance-only rewrites, unchanged packaging internals, tests, and documentation are `3`.

Do not use `3` for consumer-visible typing information merely because runtime output is unchanged.

The normal classifications are:

- Added public functionality: `A2`
- Removed public functionality: `A1`
- Broadened accepted inputs: `A2`
- Narrowed accepted inputs: `A1`
- Incompatible return-type change: `A1`
- Added compatible typing information or `py.typed`: `A2`
- Compatible bug fix with unchanged contract: `B2`
- Incompatible behavior change with unchanged contract: `B1`
- Internal or maintenance change with identical behavior: `C3`

## Calculate impact

Set `Impact` to the lowest digit appearing in any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Calculate impact from the digits only. Do not derive it from the letters or from the number of changes.

## Sort the bullets

Sort bullets by complete code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

For changes with the same code, preserve their order from the supplied change list.

## Apply exact formatting

- Copy the supplied three-part version into the heading unchanged.
- Copy the supplied ISO date in `YYYY-MM-DD` form unchanged.
- Put `Impact` immediately below the heading, with no blank line between them.
- Put exactly one blank line between `Impact` and the first bullet.
- Put no blank lines between bullets.
- Put exactly one blank line between the final bullet and the trailer.
- Write the trailer exactly as `<!-- stl-impact: v1 -->`.
- Make the trailer the final line.

Before returning the entry, verify that every supplied change appears exactly once, every classification follows the rules above, bullets are stably sorted, `Impact` is the lowest digit used, and the layout exactly matches the template.