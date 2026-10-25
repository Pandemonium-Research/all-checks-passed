---
name: impact-log
description: Use this guide when given a release version, release date, and pending changes to produce one correctly formatted, classified, and sorted release-notes entry.
---

# Release notes

Produce exactly one release entry. Do not add an introduction, explanation, code fence, blank line, or text after the trailer.

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: LOWEST_MARKER_DIGIT
- [MARKER] Change description.
- [MARKER] Change description.
<!-- stl-impact: v1 -->
```

Replace every placeholder with the supplied release information.

## Procedure

### 1. Write the heading

Write `## [VERSION] - YYYY-MM-DD`.

- Keep the supplied three-part version inside square brackets.
- Put one space on each side of the hyphen.
- Write the supplied date in year-month-day order.

### 2. Create one bullet per pending change

Start every bullet with `- [LD] `, where `L` is the impact letter and `D` is the impact digit.

- Include exactly one bullet for every pending change.
- Do not combine separate changes.
- Do not split one change into multiple bullets.
- Preserve the meaning of the supplied change.
- Put the marker before the description.
- End the description with a period.

Classify every change before sorting any bullets.

### 3. Assign the impact letter

Test the categories in this order: `A`, then `B`, then `C`. If multiple categories apply, use the first applicable letter.

#### `A`: Public API or public typing surface

Use `A` when the public programming or typing interface changes, including changes to:

- exported modules, names, functions, classes, or constants;
- parameters, signatures, or accepted input types;
- return types or return representations;
- public annotations or type information exposed to type checkers.

Adding or removing a public name is `A`. Changing a return value from one type or representation to another is also `A`, even if the function name and parameters stay unchanged.

Classify a packaging file or mechanism as `A` when its effect is to expose the package’s public type information to consumers. Classify it by that public effect, not merely as packaging work.

#### `B`: Runtime behavior

Use `B` when the public API and typing surface are unchanged, but an existing supported call behaves differently. This includes changes to:

- output content or returned values without a public type change;
- raised exceptions;
- externally visible state or side effects;
- handling of an existing input.

A bug fix is normally `B` when it changes the behavior of an existing call without changing its public signature or types.

#### `C`: Engineering, packaging, or support work

Use `C` when neither the public API or typing surface nor the functional behavior of an existing call changes. This includes:

- internal refactoring, caching, or dependency implementation choices;
- speed, memory, or import-time improvements with identical behavior;
- documentation, examples, tests, tooling, or CI;
- builds, distribution metadata, dependency management, or packaging;
- supported Python, operating-system, platform, or installation versions.

The letter does not indicate severity. A supported-environment or installation change remains `C` even when it is breaking.

### 4. Assign the impact digit independently

Choose the digit after choosing the letter. Do not infer the digit from the letter.

#### `1`: Breaking

Use `1` when a previously valid, supported, working use can fail, become unsupported, or produce a different result. This includes:

- removing or incompatibly changing public API;
- changing established output for supported inputs;
- dropping a supported runtime, operating system, platform, or installation path.

#### `2`: Compatible and observable

Use `2` when consumers can observe or use the change, but correct existing uses continue to work. This includes:

- adding public API;
- making compatible public type information available;
- fixing a previously failing or incorrect case without changing successful supported cases;
- adding compatible packaging or platform capability.

#### `3`: Not functionally observable

Use `3` when public signatures, accepted inputs, results, exceptions, side effects, and supported workflows remain unchanged. Documentation, tests, CI, internal refactors, internal dependency substitutions, and output-equivalent performance work are normally `3`.

Common combinations are:

- `A1`: incompatible public API or public type change;
- `A2`: compatible public API or public type addition;
- `B1`: incompatible behavior change with the same API surface;
- `B2`: compatible behavior fix;
- `C1`: removal of supported environment or installation support;
- `C2`: compatible, observable packaging or support capability;
- `C3`: internal, documentation, tooling, or behavior-equivalent work.

When classification remains genuinely ambiguous, choose the more disruptive result: the earlier letter and the lower digit.

### 5. Sort the bullets

Sort by the complete marker in exactly this order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the supplied order only among changes with the same complete marker.

Do not sort solely by digit. For example, every `C1` bullet belongs after all `B` bullets but before every `C2` and `C3` bullet.

### 6. Calculate the overall impact

Write `Impact: LOWEST_MARKER_DIGIT`, replacing the placeholder with the numerically lowest digit used by any bullet.

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only digits from bullet markers. Do not use digits from the version, date, API names, descriptions, or trailer. The value is neither the number of changes nor the most frequent digit.

### 7. Add the trailer

After the final bullet, add this exact final line:

```text
<!-- stl-impact: v1 -->
```