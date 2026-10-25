---
name: impact-log
description: Use when given a version number, release date, and pending changes to produce one classified, sorted, machine-parseable release-notes entry for this project.
---

# Release notes

Create exactly one release entry. Include every pending change once, preserving its technical meaning. Do not copy classifications or formatting from existing entries; older entries may be invalid.

Output only the completed entry, using this exact layout:

```text
## [X.Y.Z] - YYYY-MM-DD
Impact: N

- [LD] Description of one change.
- [LD] Description of another change.

<!-- stl-impact: v1 -->
```

## Classify each change

Start every bullet with one `[LD]` code. Choose the letter and digit independently.

If a change has multiple effects, use the earliest applicable letter (`A` before `B` before `C`) and the lowest applicable digit (`1` before `2` before `3`).

### Choose the letter

Use the first matching category:

1. `A` — The public API changes.
2. `B` — An existing public operation behaves differently at runtime, without a public API change.
3. `C` — The change concerns implementation, build, packaging, tooling, tests, or documentation.

#### `A` — Public API

Use `A` when a consumer-visible exported name, import path, callable signature, accepted argument type, return type, or exported type definition changes.

Typical classifications include:

- Adding public functionality: `A2`
- Removing or renaming public functionality: `A1`
- Broadening accepted argument types: `A2`
- Narrowing accepted argument types: `A1`
- Incompatibly changing a return type: `A1`

A compatible addition or broader input is still an API change, so use `A`, not `B`.

#### `B` — Runtime behavior

Use `B` when an existing public operation retains the same API but its functional result or error behavior changes.

Typical classifications include:

- Correcting an existing operation to produce its intended result: `B2`
- Intentionally changing established behavior incompatibly: `B1`

Do not use `B` for an internal runtime-code change when returned values, output, and errors remain equivalent.

#### `C` — Implementation and project maintenance

Use `C` for changes involving internal implementation, performance, caching, dependencies, build configuration, packaging, supported runtimes, tooling, tests, or documentation when no exported API or existing operation’s functional behavior changes.

Typical classifications include:

- Internal refactoring with identical behavior: `C3`
- Performance-only work with identical results: `C3`
- Dependency or vendoring changes with no consumer-visible effect: `C3`
- Packaging migrations that preserve installation and support: `C3`
- Documentation or test changes: `C3`

The letter and digit are independent. A build, packaging, or tooling change may therefore be `C1` if it breaks supported use or `C2` if it adds compatible support. For example, dropping a supported runtime is breaking even though it belongs to the build or packaging category.

Changing exported annotations or type definitions is `A`. Changing only packaging or tooling metadata, without changing those exported definitions, remains `C`.

### Choose the digit

Use the first matching severity:

1. `1` — Previously supported correct use can become incompatible.
2. `2` — The change adds compatible capability, broadens support, or corrects intended behavior.
3. `3` — No caller-observable API or functional runtime behavior changes.

Use `1` for removals, narrowed inputs, dropped support, incompatible return types, or intentional incompatible behavior changes.

Use `2` for compatible additions, broader inputs, added support, and bug fixes. A correction is normally `2` even if code relying on the bug observes a different result.

Use `3` for equivalent internal changes, performance work, unchanged packaging internals, tests, and documentation. Do not assign `3` merely because the implementation changed.

## Calculate impact

Set `Impact` to the lowest digit used by any bullet:

- If any bullet has digit `1`, use `Impact: 1`.
- Otherwise, if any bullet has digit `2`, use `Impact: 2`.
- Otherwise, use `Impact: 3`.

Calculate impact from the digits only.

## Sort the bullets

Sort by complete code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

When multiple changes have the same code, preserve their order from the pending-change list.

## Apply exact formatting

- Copy the supplied three-part version into the heading unchanged.
- Copy the supplied `YYYY-MM-DD` date unchanged.
- Put `Impact` immediately below the heading, with no blank line between them.
- Put exactly one blank line between `Impact` and the first bullet.
- Put no blank lines between bullets.
- Put exactly one blank line between the final bullet and the trailer.
- Write the trailer exactly as `<!-- stl-impact: v1 -->`.
- Make the trailer the final line.
- Do not include a code fence or commentary in the completed entry.

Before returning the entry, verify that every pending change appears exactly once, every code follows the rules above, the bullets are stably sorted, and `Impact` is the lowest digit present.