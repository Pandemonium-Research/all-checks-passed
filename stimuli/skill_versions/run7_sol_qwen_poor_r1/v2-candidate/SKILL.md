---
name: impact-log
description: Use this guide when given a release version, release date, and pending changes and you need to produce one correctly formatted, classified, and sorted release-notes entry.
---

# Release notes

Produce exactly one release entry. Do not add an introduction, explanation, code fence, or text after the trailer.

## Required format

```text
## [VERSION] - YYYY-MM-DD
Impact: LOWEST_MARKER_DIGIT
- [MARKER] Change description.
- [MARKER] Change description.
<!-- stl-impact: v1 -->
```

Replace every placeholder with the supplied release information. Include exactly one bullet per pending change and no blank lines within the entry.

## Procedure

### 1. Write the heading

Use:

```text
## [VERSION] - YYYY-MM-DD
```

- Keep the version inside square brackets.
- Use the supplied three-part version, such as `1.4.0`.
- Put one space on each side of the hyphen.
- Write the supplied date in year-month-day order.

### 2. Create one bullet per change

Start every bullet with `- [LD] `, where `L` is the impact letter and `D` is the impact digit.

- Do not combine separate pending changes.
- Do not split one pending change into multiple bullets.
- Preserve the meaning of the supplied change.
- Put the marker before the description.
- End each description with a period.

Classify every change before sorting the bullets.

### 3. Choose the impact letter

The letter identifies what kind of contract or implementation area changed. Test the categories in this order: `A`, then `B`, then `C`.

#### `A`: Public API surface

Use `A` when consumers see a change to the public programming or typing interface, including:

- exported modules, names, functions, classes, or constants;
- parameters, signatures, or accepted input types;
- return types or other public type declarations;
- public annotations or type information newly exposed to type checkers.

Adding or removing a public name is `A`. Changing a return value from one type or representation to another is also `A`, even when the function still has the same name.

A packaging mechanism that makes public type information visible is classified by its effect on the public typing interface, so it is `A`, not `C`.

#### `B`: Functional behavior

Use `B` when the public API surface is unchanged, but an existing supported call changes functionally. Functional changes include changes to:

- returned values or output content;
- raised exceptions;
- externally visible state or side effects;
- handling of an existing input.

A bug fix is normally `B` when it changes the behavior of an existing call without changing its public signature or types.

#### `C`: Engineering, packaging, or support work

Use `C` when neither the public API surface nor the functional behavior of an existing call changes. This includes:

- internal refactoring or caching;
- performance-only implementation work;
- documentation, examples, tests, tooling, or CI;
- builds, distribution metadata, dependency management, or packaging;
- supported Python, operating-system, or platform versions.

The letter does not indicate severity. A packaging or supported-environment change remains `C` even when it breaks users and therefore receives digit `1`.

A pure speed, memory, or import-time improvement is `C` when accepted inputs, results, exceptions, and side effects remain unchanged. An internal dependency or implementation change is also `C` when it does not alter the installed package’s public or functional contract.

If one change affects multiple categories, choose the earliest applicable letter: `A` before `B` before `C`.

### 4. Choose the impact digit independently

After choosing the letter, choose the digit without using the letter to infer it.

#### `1`: Breaking

Use `1` when a previously valid, supported, working use can fail, become unsupported, or produce a different result. Examples include:

- removing or incompatibly changing public API;
- changing established output for supported inputs;
- dropping a supported runtime, operating system, platform, or installation path.

#### `2`: Compatible and observable

Use `2` when the change is visible to consumers but leaves correct existing uses working. Examples include:

- adding public API or compatible public type information;
- fixing a previously failing or incorrect case without changing successful supported cases;
- adding compatible packaging or platform capability.

#### `3`: Not functionally observable

Use `3` when public signatures, accepted inputs, results, exceptions, side effects, and supported workflows remain unchanged. Documentation, tests, CI, internal refactors, and output-equivalent performance work are normally `3`.

Do not assume that `A` requires `1` or that `C` requires `3`. Common combinations include:

- `A1`: incompatible public API change;
- `A2`: compatible public API addition;
- `B1`: incompatible behavior change with the same API surface;
- `B2`: compatible behavior fix;
- `C1`: removal of supported environment or packaging support;
- `C2`: compatible, observable packaging or support improvement;
- `C3`: internal, documentation, tooling, or functionally equivalent work.

When classification remains genuinely ambiguous, choose the more disruptive result: the earlier letter and the lower digit.

### 5. Sort the bullets

Sort by the complete marker in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Preserve the supplied order only among changes that have the same complete marker.

Classify first and sort second. In particular, `C1` must appear before `C2` and `C3`, regardless of where those changes appeared in the supplied list.

### 6. Calculate the overall impact

Write:

```text
Impact: LOWEST_MARKER_DIGIT
```

Replace the placeholder with the numerically lowest digit used by any bullet.

- If any marker ends in `1`, write `Impact: 1`.
- Otherwise, if any marker ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Use only digits from the bullet markers. Do not use digits from the version, date, API names, descriptions, or trailer. The value is neither the number of changes nor the most frequent digit.

### 7. Add the trailer

After the final bullet, add this exact final line:

```text
<!-- stl-impact: v1 -->
```