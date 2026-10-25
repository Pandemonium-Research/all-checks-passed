---
name: impact-log
description: Use this document when converting a release version, date, and list of pending project changes into one classified, sorted release-notes entry with an overall impact value.
---

# Release notes

Create exactly one release entry. Include every supplied pending change exactly once and do not add facts or effects that were not supplied.

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
2. Choose its marker digit independently based on the stated effect on supported users.
3. Write one bullet that preserves all meaningful supplied facts.
4. After classifying all changes, sort the bullets and calculate `Impact`.

Do not combine multiple pending changes into one bullet or split one pending change into multiple bullets.

Each bullet must begin exactly like this:

```text
- [A2] Description.
```

Format literal code-related names with backticks. This includes functions, arguments, types, modules, files, dependencies, directories, and command-line values.

Classify only from the supplied facts. Do not infer breakage, compatibility, or behavior changes from implementation details or from the possibility that callers relied on a bug.

## Choose the marker letter

Use the earliest applicable letter in the order `A`, `B`, `C`.

### A — Public API or shipped typing surface

Use `A` when the change alters the public interface that code or type checkers use, including:

- Adding, removing, renaming, or relocating an exported name.
- Changing a public import path.
- Changing a function or method signature.
- Adding, removing, or changing parameters or declared return types.
- Changing public annotations or stubs.
- Making shipped annotations newly discoverable to type checkers.

Adding, removing, or changing a public API element is `A`.

Do not use `A` merely because an existing public function returns a different result or accepts a different runtime value. If its signature and shipped typing surface are unchanged, use `B`.

### B — Runtime behavior through an unchanged API

Use `B` when calls through an unchanged public API behave differently at runtime, including changes to:

- Returned values or generated output.
- Accepted or rejected input values.
- Parsing, counting, formatting, or validation results.
- Exceptions, side effects, or other observable call behavior.

A result change through an unchanged function signature is `B`. A bug correction remains `B` when it changes an existing function’s output without changing its public interface.

### C — Environment support, project internals, and supporting material

Use `C` when neither the public API surface nor runtime call behavior changes. This includes:

- Adding or removing support for interpreters, platforms, wheels, or installation environments.
- Build and packaging implementation.
- Dependency management or vendoring.
- Development tooling and test infrastructure.
- Documentation and docstring-only edits.
- Performance-only work with unchanged results.
- Internal refactoring or implementation replacement.

Interpreter, platform, wheel, and installation availability use `C`, not `A` or `B`. Use the digit to distinguish added support, removed support, and unchanged support.

A supporting-file or implementation change remains `C` unless the supplied facts state that it also changes a public API or runtime behavior.

## Choose the marker digit

Choose the digit independently from the letter. Evaluate only the stated effect on supported users.

### 1 — Breaking supported use

Use `1` only when the supplied facts explicitly state or necessarily establish that previously supported code or environments can no longer work as supported.

Examples include:

- Removing or incompatibly changing a supported public interface.
- Adding a required argument to an existing call.
- Removing previously supported input.
- Intentionally changing a documented or supported result incompatibly.
- Dropping support for an interpreter, platform, wheel, or installation method.
- Introducing an explicitly incompatible exception or side effect.

A changed result is not automatically breaking. Do not use `1` merely because callers might have relied on erroneous behavior.

A change described as a fix, correction, or newly correct handling normally uses `2`. Use `1` for such a change only when the supplied facts explicitly identify a broken supported contract or supported use.

### 2 — Compatible and externally observable

Use `2` when the change adds a compatible capability, adds supported environment availability, or corrects user-visible behavior while supported existing use remains valid.

Examples include:

- Adding a public interface.
- Adding an optional parameter or compatible public type.
- Adding or exposing shipped typing support.
- Accepting an additional input through an unchanged interface.
- Correcting erroneous runtime behavior.
- Adding support for an interpreter, platform, wheel, or installation environment.

Digit `2` does not mean “something was added anywhere.” Documentation, tests, internal code, caches, build files, or packaging files use `3` when they do not add a public capability, runtime behavior, or supported environment.

### 3 — No supported user-facing change

Use `3` when public API, runtime results, and supported installation or environment availability remain unchanged.

Normally use `3` for:

- Documentation-only additions or corrections.
- Test-runner or development-tool changes.
- Internal refactors.
- Performance improvements with unchanged output.
- Dependency vendoring with unchanged supported behavior.
- Packaging or build-system rearrangements that preserve supported installation.
- Moving internal files without changing supported use.

### Digit tie-breaker

If more than one digit genuinely applies, use the lowest digit:

```text
1 before 2 before 3
```

Do not choose a lower digit merely because the impact is uncertain. Use only effects established by the supplied facts.

## Classification reference

Use these common combinations to check each marker:

- Compatible public API or shipped typing addition: `A2`.
- Removed or incompatibly changed public API: `A1`.
- Compatible bug correction through an unchanged API: `B2`.
- Additional accepted runtime input through an unchanged API: `B2`.
- Explicitly incompatible supported behavior change: `B1`.
- Added interpreter, platform, wheel, or installation support: `C2`.
- Removed interpreter, platform, wheel, or installation support: `C1`.
- Documentation, tests, internal refactoring, or output-preserving optimization: `C3`.
- Dependency or packaging rearrangement with unchanged behavior and support: `C3`.

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
- The number of bullets equals the number of supplied pending changes.
- Every pending change appears exactly once.
- No change was combined, split, omitted, or supplemented with invented facts.
- Literal code-related names use inline code formatting.
- Public API and shipped typing changes use `A`.
- Runtime changes through unchanged APIs use `B`.
- User-visible bug corrections use `B2` unless explicit supported breakage is supplied.
- Interpreter, platform, wheel, and installation availability changes use `C`.
- Added environment support uses `C2`; removed support uses `C1`.
- Documentation, tests, internal refactors, and output-preserving performance work use `C3`.
- Output-preserving dependency or packaging rearrangements use `C3`.
- The bullets follow the required marker order.
- Changes sharing a marker retain their supplied order.
- `Impact` is the lowest marker digit.
- The trailer is present and is the final line.