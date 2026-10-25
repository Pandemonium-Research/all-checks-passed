---
name: impact-log
description: Write a parseable impact-log release-notes entry from a supplied version, date, and list of pending project changes.
---

# Release notes

Create exactly one release entry. Include every supplied change exactly once. Do not invent, omit, combine, or split changes.

Use this exact layout:

```text
## [X.Y.Z] - YYYY-MM-DD
Impact: N

- [LD] Description of one change.
- [LD] Description of another change.

<!-- stl-impact: v1 -->
```

Replace the placeholders with the supplied version, date, calculated impact, classifications, and change descriptions. Output only the completed entry.

Formatting is exact:

- Use the supplied three-part version number in the heading.
- Use the supplied ISO date in `YYYY-MM-DD` form.
- Put `Impact` immediately below the heading, with no blank line between them.
- Put exactly one blank line between `Impact` and the first bullet.
- Put no blank lines between bullets.
- Put exactly one blank line between the final bullet and the trailer.
- Write the trailer exactly as `<!-- stl-impact: v1 -->`.
- Make the trailer the final line.

## Classify each change

Start every bullet with one code in the form `[LD]`. Choose the letter and digit independently; a disruptive-sounding change does not automatically receive both the earliest letter and the lowest digit.

### 1. Choose the letter

Choose based on the change's consumer-visible effect, using this precedence: `A`, then `B`, then `C`.

#### `A` — Public contract change

Use `A` when the interface available to consumers changes, including:

- Adding, removing, or renaming public functionality
- Adding, removing, or changing an exported name or public import path
- Changing a callable signature
- Broadening or narrowing accepted argument types
- Changing a return type
- Changing supported runtime versions
- Adding or changing consumer-visible annotations, type stubs, or typing markers

A change can be `A` even when it is fully backward-compatible. For example, new public functionality and broader accepted inputs are `A2`, not `A1` or `B2`.

#### `B` — Runtime behavior change without a contract change

Use `B` when an existing public operation has the same public contract but produces different functional results, including:

- Changed returned values or rendered output
- Changed parsing, formatting, or normalization behavior
- Added, removed, or corrected runtime errors
- A bug fix to the behavior of an existing public operation

Do not use `B` merely because runtime implementation code changed. If inputs, outputs, errors, and other functional results remain identical, use `C`.

#### `C` — Implementation or maintenance only

Use `C` when neither the public contract nor functional runtime results change, including:

- Internal refactors, caches, and equivalent algorithm replacements
- Performance improvements with identical functional behavior
- Dependency or vendoring changes with no consumer-visible effect
- Build or packaging migrations that preserve installation and runtime support
- Tooling, tests, and documentation

Classify the effect, not the file modified. For example, a packaging change that drops a supported runtime is `A`, while a packaging migration that preserves support is `C`.

### 2. Choose the digit

Choose the digit separately from the letter.

#### `1` — Breaking

Use `1` when previously supported caller code can stop working, stop importing, raise a new error, or receive an incompatible result.

Examples include:

- Removing or renaming public API
- Narrowing accepted inputs
- Incompatibly changing a signature or return type
- Dropping a supported runtime
- Intentionally changing established behavior incompatibly

#### `2` — Compatible or corrective

Use `2` when the change is additive, broadens supported use, or corrects intended behavior while supported correct usage remains valid.

Examples include:

- Adding public API
- Broadening accepted inputs
- Adding compatible consumer-facing type information
- Fixing a runtime bug

A correction to documented or intended behavior is normally `2`, even if code relying on the bug observes a different result.

#### `3` — Non-observable maintenance

Use `3` only when the public contract and functional runtime results are unchanged.

Examples include internal refactors, equivalent cache replacements, performance-only rewrites, unchanged packaging internals, tests, and documentation.

Do not use `3` for a consumer-visible typing change merely because runtime output is unchanged.

Common classifications are:

- Added public functionality: `A2`
- Removed public functionality: `A1`
- Broadened accepted argument types: `A2`
- Narrowed accepted argument types: `A1`
- Incompatible return-type change: `A1`
- Compatible bug fix with unchanged API: `B2`
- Incompatible behavior change with unchanged API: `B1`
- Internal change with identical behavior: `C3`

## Calculate the impact

Set `Impact` to the lowest digit appearing in any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Calculate impact from the digits only. Do not derive it from the letters.

## Sort the bullets

Sort bullets by their complete code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

For changes with the same code, preserve their order from the supplied change list.

## Final verification

Before returning the entry, verify that:

- The supplied version and date are unchanged.
- Every supplied change appears in exactly one bullet.
- No unsupplied change was added.
- Every bullet starts with one valid `[A1]` through `[C3]` code.
- Each letter reflects the change's effect.
- Each digit reflects its severity independently.
- `Impact` equals the lowest digit used.
- Bullets follow the required code order.
- The heading, `Impact` line, bullets, blank lines, and trailer match the template exactly.
- The trailer is the entry's final line.