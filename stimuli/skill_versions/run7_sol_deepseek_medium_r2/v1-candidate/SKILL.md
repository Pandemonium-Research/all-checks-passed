---
name: impact-log
description: Write parseable release notes, changelog entries, and version-history entries from a supplied version, date, and list of pending changes using the project's impact-log format.
---

# Release notes

Create exactly one release entry from the supplied version, date, and pending changes. Do not invent, omit, or merge changes.

Use this exact structure:

```text
## [X.Y.Z] - YYYY-MM-DD
Impact: N

- [LD] Description of one change.
- [LD] Description of another change.

<!-- stl-impact: v1 -->
```

Replace the placeholders with the supplied values and classified changes. Preserve the spacing shown:

- Put `Impact` immediately after the heading, with no blank line between them.
- Put one blank line before the bullets.
- Do not put blank lines between bullets.
- Put one blank line before the trailer.
- Make `<!-- stl-impact: v1 -->` the entry's final line.

Use a three-part version number and an ISO date in `YYYY-MM-DD` form.

## Classify each change

Prefix every bullet with one code in the form `[LD]`. Choose the letter and digit independently. A letter never implies a particular digit.

### Choose the letter

Use the first applicable category in this precedence order:

1. `A` — The public contract changes. This includes exported names or import paths, callable signatures, accepted argument types, return types, supported runtime versions, and consumer-visible type information.
2. `B` — The functional runtime behavior of an existing public call changes without changing its public contract. This includes changed output values, parsing or formatting behavior, and raised errors.
3. `C` — Only implementation or maintenance details change. This includes internal refactors, caches, performance-only rewrites with identical functional behavior, dependencies, build or packaging internals, tooling, tests, and documentation.

Classify by user-visible effect, not by the file that changed. For example, a packaging change that drops a supported runtime is `A`, while a packaging migration that leaves installation and support unchanged is `C`.

### Choose the digit

Use the first applicable severity:

1. `1` — Breaking. Existing supported caller code can stop working, stop importing, raise a new error, or receive an incompatible result. Removing or renaming public API, narrowing accepted inputs, changing a return type incompatibly, and dropping a supported runtime are breaking.
2. `2` — Compatible. The change is additive or corrects behavior while supported correct usage continues to work. New public API, broader accepted inputs, compatible public type information, and bug fixes are compatible.
3. `3` — Non-observable maintenance. The public contract and functional runtime results are unchanged. Internal refactors, cache substitutions, unchanged packaging internals, tests, and documentation normally use `3`.

A correction to documented or intended behavior is normally `2`, even though callers relying on the bug may see a different result.

Common combinations include:

- New exported functionality: `A2`
- Removed public functionality: `A1`
- Broadened accepted argument types: `A2`
- Incompatible return-type change: `A1`
- Compatible runtime bug fix with unchanged API: `B2`
- Incompatible output change with unchanged API: `B1`
- Internal change with identical public behavior: `C3`

## Calculate and order the entry

Set `Impact` to the lowest digit used by any bullet. Thus any `1` makes the summary `Impact: 1`; otherwise any `2` makes it `Impact: 2`; use `Impact: 3` only when every bullet has digit `3`.

Sort bullets by the complete code, comparing the letter first and the digit second:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Keep the supplied order for changes with the same code.

Before returning the entry, verify that:

- Every pending change has exactly one bullet.
- Every bullet begins with a valid `[A1]` through `[C3]` code.
- Letters and digits were selected independently.
- `Impact` equals the lowest bullet digit.
- Bullets follow the required code order.
- The heading and blank lines match the template.
- The trailer is present and is the final line.