---
name: impact-log
description: Use this document when converting a release version, date, and list of pending project changes into one classified, sorted release-notes entry with an overall impact value.
---

# Release notes

Create exactly one release entry. Include every supplied pending change exactly once and do not add changes that were not supplied.

## Required format

```text
## VERSION - YYYY-MM-DD
Impact: LOWEST_DIGIT

- [LETTERDIGIT] Description of one pending change.
- [LETTERDIGIT] Description of another pending change.

<!-- stl-impact: v1 -->
```

Replace:

- `VERSION` with the supplied three-part version. Do not prefix it with `v`.
- `YYYY-MM-DD` with the supplied date.
- `LETTERDIGIT` with the marker assigned using the rules below.
- `LOWEST_DIGIT` with the lowest digit appearing in any assigned marker.

The heading must begin with exactly two `#` characters. Write the summary exactly as `Impact: N`.

## Process each change

For every pending change:

1. Choose its marker letter based on what changed.
2. Choose its marker digit based on the effect on supported users.
3. Write one bullet for it.
4. After classifying all changes, sort the bullets and calculate `Impact`.

Do not combine multiple pending changes into one bullet or split one pending change into multiple bullets.

Each bullet must begin exactly like this:

```text
- [A2] Description.
```

## Choose the marker letter

Use the earliest applicable letter in the order `A`, `B`, `C`.

### A — Public API surface

Use `A` when the change alters the public interface that code or type checkers use, including:

- Exported names or public import paths.
- Function or method signatures.
- Parameters or return types.
- Public annotations or shipped typing information.

Adding, removing, or changing a public API element is `A`.

Do not use `A` merely because an existing public function produces a different result. If its public interface is unchanged and only its runtime behavior changes, use `B`.

### B — Runtime behavior

Use `B` when calls through an unchanged public API behave differently at runtime, including changes to:

- Returned values or generated output.
- Parsing, counting, formatting, or validation results.
- Exceptions, side effects, or other observable call behavior.

A result change through an unchanged function signature is `B`, even when incompatible.

### C — Project internals and supporting material

Use `C` when neither the public API surface nor runtime call behavior changes. This includes:

- Build and packaging implementation.
- Dependency management or vendoring.
- Development tooling and test infrastructure.
- Documentation and docstring-only edits.
- Performance-only work with unchanged results.
- Internal refactoring or implementation replacement.

A supporting-file change remains `C` unless it also changes a public API or runtime behavior.

## Choose the marker digit

Choose the digit independently from the letter. Evaluate the effect of the entire change on supported users.

### 1 — Breaking

Use `1` when supported code or environments can fail, become invalid, or receive an incompatible result.

Examples include removing a supported public interface, making a signature incompatible, changing established results incompatibly, or dropping supported installation behavior.

### 2 — Compatible and externally observable

Use `2` when the change gives users a new compatible capability or intentionally corrects externally observable behavior while supported existing use remains valid.

Examples include adding a public interface, adding shipped typing support, adding supported runtime behavior, or making a compatible user-visible bug correction.

Digit `2` does not mean “something was added anywhere.” Documentation, tests, internal code, or packaging contents added without a user-facing API, behavior, or support change use `3`.

### 3 — No user-visible change

Use `3` when public API, runtime results, and supported installation behavior remain unchanged.

Normally use `3` for:

- Documentation-only additions or corrections.
- Test-runner or development-tool changes.
- Internal refactors.
- Performance improvements with unchanged output.
- Dependency vendoring or packaging rearrangement that preserves supported installation and runtime behavior.

If a documentation, tooling, dependency, packaging, performance, or internal change also affects supported users, select `1` or `2` according to that effect.

### Digit tie-breaker

If more than one digit genuinely applies, use the lowest digit:

```text
1 before 2 before 3
```

When uncertain, choose the more disruptive digit. A change described as a fix still uses `1` if it incompatibly changes results relied upon by supported callers.

## Calculate Impact

Set `Impact` to the lowest digit among all bullet markers.

For example, the digits in `A2`, `B1`, and `C3` produce:

```text
Impact: 1
```

Count only marker digits. Ignore numbers in the version, date, descriptions, performance measurements, and identifiers.

## Sort the bullets

Sort by the complete marker in exactly this order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

Keep the supplied order for changes that receive the same marker.

## Add the trailer

Leave one blank line after the final bullet, then add this exact final line:

```text
<!-- stl-impact: v1 -->
```

Do not add any content after the trailer.

## Final check

Before submitting, verify that:

- The heading is exactly `## VERSION - YYYY-MM-DD`.
- The version has no `v` prefix.
- The summary is exactly `Impact: N`.
- Every pending change appears exactly once.
- Every bullet starts with a bracketed marker.
- Runtime result changes with unchanged APIs use `B`, not `A`.
- Documentation, tests, internal refactors, and output-preserving performance work use `C3`.
- Output-preserving dependency or packaging rearrangements use `C3`.
- The bullets follow the required marker order.
- Changes sharing a marker retain their supplied order.
- `Impact` is the lowest marker digit.
- The trailer is present and is the final line.