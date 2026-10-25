---
name: impact-log
description: Use this document to turn a supplied version, date, and list of pending project changes into one correctly classified, sorted, and parseable impact-log release-nototes entry.
---

# Release notes

Produce exactly one release entry from the supplied version, date, and pending changes.

Include every supplied change exactly once. Do not invent, omit, combine, or split changes. Do not copy formatting or classifications from older entries; some are invalid.

Use this exact layout:

```text
## [X.Y.Z] - YYYY-MM-DD
Impact: N

- [LD] Description of one change.
- [LD] Description of another change.

<!-- stl-impact: v1 -->
```

Replace the placeholders with the supplied values and calculated classifications. Output only the completed entry, without a code fence or additional commentary.

## 1. Classify each change

Each bullet must begin with one `[LD]` code. Choose the letter and digit independently.

If one supplied change has several effects, use the earliest applicable letter (`A` before `B` before `C`) and lowest applicable digit (`1` before `2` before `3`).

### Choose the letter

Apply this decision process in order:

1. If the public contract changes, use `A`.
2. Otherwise, if an existing public operation has different functional runtime behavior, use `B`.
3. Otherwise, use `C`.

#### `A` — Public contract change

Use `A` when anything consumers can depend on as an interface changes, including:

- Adding, removing, or renaming public functionality
- Changing exported names or public import paths
- Changing a callable signature
- Broadening or narrowing accepted argument types
- Changing a return type
- Changing supported runtime versions
- Adding or changing public annotations, type stubs, typing markers, or other consumer-visible type information

These are contract changes even when backward-compatible. In particular:

- New public functionality is `A`, not `B`.
- Broader accepted inputs are `A`, not `B`.
- A return-type change is `A`, even if the written signature is otherwise unchanged.
- Consumer-visible typing support is `A`, even if runtime results are unchanged.

#### `B` — Runtime behavior change without a contract change

Use `B` when an existing public operation keeps the same contract but its functional result changes, including:

- Different returned values or rendered output
- Different parsing, formatting, or normalization
- A runtime error being added, removed, or corrected
- A bug fix to an existing public operation

Do not use `B` merely because runtime implementation code changed. If supported inputs, output types, functional results, and errors remain equivalent, use `C`.

#### `C` — Implementation or maintenance only

Use `C` when neither the public contract nor functional runtime results change, including:

- Internal refactors or cache changes
- Performance-only implementation changes
- Equivalent algorithm replacements
- Dependency or vendoring changes with no consumer-visible effect
- Build or packaging migrations that preserve installation and runtime support
- Tooling, tests, and documentation

Classify the effect, not the file modified. For example, packaging work that changes supported runtimes is `A`; packaging work that preserves installation and support is `C`.

### Choose the digit

Apply this decision process independently of the letter:

1. If previously supported correct caller code can become incompatible, use `1`.
2. Otherwise, if the change is additive, broadens support, or corrects intended behavior, use `2`.
3. Otherwise, use `3`.

#### `1` — Breaking

Use `1` when previously supported correct usage can stop working, stop importing, raise a new error, or receive an incompatible result.

Examples include:

- Removing or renaming public API
- Narrowing accepted inputs
- Incompatibly changing a signature or return type
- Dropping a supported runtime
- Intentionally changing established behavior incompatibly

#### `2` — Compatible or corrective

Use `2` when supported correct usage continues to work and the change is additive, broader, or corrective.

Examples include:

- Adding public API
- Broadening accepted inputs
- Adding compatible consumer-visible type information
- Fixing behavior that did not match its documented or intended result

A bug fix is normally `2`, even if callers relying on the bug observe a different result.

#### `3` — Non-observable maintenance

Use `3` only when the public contract and functional runtime results remain unchanged.

Examples include internal refactors, equivalent cache replacements, performance-only rewrites, unchanged packaging internals, tests, and documentation.

Do not use `3` for a consumer-visible contract, typing, or behavior change.

Common classifications:

- Added public functionality: `A2`
- Removed public functionality: `A1`
- Broadened accepted argument types: `A2`
- Narrowed accepted argument types: `A1`
- Incompatible return-type change: `A1`
- Compatible bug fix with unchanged API: `B2`
- Incompatible behavior change with unchanged API: `B1`
- Internal change with identical behavior: `C3`

## 2. Calculate the impact

Set `Impact` to the lowest digit used by any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Calculate impact from the digits only, not from the letters.

## 3. Sort the bullets

Sort bullets by their complete codes in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

When several changes have the same code, preserve their order from the supplied change list.

## 4. Apply exact formatting

- Copy the supplied three-part version into the heading without changing it.
- Copy the supplied ISO date in `YYYY-MM-DD` form without changing it.
- Put `Impact` immediately below the heading, with no blank line between them.
- Put exactly one blank line between `Impact` and the first bullet.
- Put no blank lines between bullets.
- Put exactly one blank line between the final bullet and the trailer.
- Write the trailer exactly as `<!-- stl-impact: v1 -->`.
- Make the trailer the final line.

Before returning the entry, verify that every supplied change appears in exactly one bullet, every code is correct, the bullets are stably sorted, `Impact` is the lowest digit used, and the layout exactly matches the template.