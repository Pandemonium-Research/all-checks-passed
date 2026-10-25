---
name: impact-log
description: Use this document to turn a supplied release version, date, and list of pending project changes into one classified, sorted release-nototes entry with an overall impact value.
---

# Release notes

Create exactly one release entry. Include every pending change exactly once, using one bullet per change.

Do not combine changes, split a change into multiple bullets, omit supplied facts, or invent compatibility or user-impact claims.

## Required format

```text
## VERSION - YYYY-MM-DD
Impact: LOWEST_DIGIT

- [LETTERDIGIT] Description of one pending change.
- [LETTERDIGIT] Description of another pending change.

<!-- stl-impact: v1 -->
```

Replace:

- `VERSION` with the supplied three-part version, without a `v` prefix.
- `YYYY-MM-DD` with the supplied date.
- `LETTERDIGIT` with the change's marker.
- `LOWEST_DIGIT` with the lowest digit used in any marker.

The heading must start with exactly two `#` characters. Write the summary exactly as `Impact: N`.

## Process each change

For every pending change:

1. Choose one letter based on what changed.
2. Choose one digit independently based on its effect on supported users.
3. Write one bullet preserving all meaningful supplied facts.
4. Sort the completed bullets by marker.
5. Set `Impact` to the lowest marker digit.

Each bullet must begin in this form:

```text
- [A2] Description.
```

Use inline code formatting for literal code-related names, including API names, calls, arguments, types, modules, files, dependencies, and command-line values. For example, write `` `function()` ``, `` `argument` ``, or `` `filename.ext` `` rather than leaving those names unformatted.

If more than one letter applies, use the earliest applicable letter in the order `A`, `B`, `C`. If more than one digit applies, use the lowest applicable digit in the order `1`, `2`, `3`.

Classify only from the supplied facts. Do not infer that a change is breaking because callers might have depended on a bug or implementation detail.

## Choose the marker letter

### A — Public interface or shipped typing

Use `A` if the change alters the public interface used by code or type checkers, including:

- Adding, removing, renaming, or relocating an exported name.
- Changing a public import path.
- Changing a public function or method signature.
- Adding, removing, or changing parameters or declared return types.
- Changing public annotations or stubs.
- Making shipped annotations newly discoverable to type checkers.

A compatible public API or shipped-typing addition is normally `A2`. An incompatible public interface change is normally `A1`.

Do not use `A` merely because an existing function returns a different result or accepts an additional runtime value. If its public signature and shipped typing surface are unchanged, evaluate it as `B`.

### B — Runtime behavior through an unchanged interface

Use `B` if calls through an unchanged public interface behave differently, including changes to:

- Returned values or generated output.
- Accepted or rejected input values.
- Parsing, counting, formatting, or validation results.
- Exceptions, side effects, or other observable call behavior.

A user-visible bug correction through an unchanged interface is normally `B2`, even though the corrected output differs from the old output. Use `B1` only when the supplied facts explicitly establish that the new behavior incompatibly breaks a supported contract or supported use.

Accepting an additional input value through an otherwise unchanged interface is normally `B2`.

### C — Environment support, internals, and supporting material

Use `C` when neither the public interface nor runtime call behavior changes. This includes:

- Adding or removing supported interpreters, platforms, wheels, or installation environments.
- Build-system and packaging implementation.
- Dependency management or vendoring.
- Documentation and docstring-only edits.
- Tests and development tooling.
- Performance-only work with unchanged results.
- Internal refactoring or implementation replacement.

Environment availability always uses `C` unless the same change also alters a public API or runtime behavior:

- Added interpreter, platform, wheel, or installation support: `C2`.
- Removed supported interpreter, platform, wheel, or installation support: `C1`.
- Packaging rearrangement with unchanged installation support: `C3`.

Dependency, packaging, and internal changes are `C3` when supported installation and runtime behavior remain unchanged. Do not infer a behavior change solely because an implementation or dependency changed.

## Choose the marker digit

### 1 — Breaking supported use

Use `1` when the supplied facts explicitly state or necessarily establish that previously supported code or environments can no longer work as supported.

Examples include:

- Removing or incompatibly changing a public interface.
- Adding a required argument to an existing call.
- Removing supported input.
- Intentionally changing a documented or supported result incompatibly.
- Dropping a supported interpreter, platform, wheel, or installation method.
- Introducing an explicitly incompatible exception or side effect.

A changed result is not automatically `1`. A change described as a bug fix, correction, or newly correct handling defaults to `2` unless the supplied facts explicitly identify a broken supported contract. Never assume that reliance on erroneous behavior was supported.

### 2 — Compatible, externally observable improvement

Use `2` when the change adds a compatible capability, adds supported environment availability, or corrects user-visible behavior while supported existing use remains valid.

Examples include:

- Adding a public API.
- Adding an optional parameter or compatible public type.
- Adding or exposing shipped typing support.
- Accepting an additional input through an unchanged interface.
- Correcting erroneous runtime output.
- Adding support for an interpreter, platform, wheel, or installation environment.

Digit `2` does not apply merely because something was added. Added documentation, tests, internal code, caches, build files, or packaging files use `3` when they do not add public capability, runtime behavior, or supported environment availability.

### 3 — No supported user-facing change

Use `3` when public API, runtime results, and supported installation or environment availability remain unchanged.

Normally use `3` for:

- Documentation or docstring-only changes.
- Tests and development-tool changes.
- Internal refactors.
- Output-preserving performance improvements.
- Dependency vendoring with unchanged supported behavior.
- Packaging or build-system rearrangements that preserve supported installation.
- Moving internal files without changing supported use.

## Classification checks

Use these combinations to verify each marker:

- Compatible public API or shipped-typing addition: `A2`.
- Removed or incompatibly changed public API: `A1`.
- Compatible bug correction through an unchanged interface: `B2`.
- Additional accepted runtime input through an unchanged interface: `B2`.
- Explicitly incompatible supported behavior change: `B1`.
- Added interpreter, platform, wheel, or installation support: `C2`.
- Removed interpreter, platform, wheel, or installation support: `C1`.
- Documentation, tests, internal refactoring, or output-preserving optimization: `C3`.
- Dependency or packaging rearrangement with unchanged behavior and support: `C3`.

## Calculate Impact

Set `Impact` to the lowest digit among all bullet markers.

For markers containing digits `2`, `1`, and `3`, write:

```text
Impact: 1
```

Count only marker digits. Ignore numbers in the version, date, descriptions, measurements, and identifiers.

## Sort the bullets

Sort by the complete marker in exactly this order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

For changes with the same marker, preserve their supplied order.

## Add the trailer

Leave one blank line after the final bullet, then add this exact final line:

```text
<!-- stl-impact: v1 -->
```

Do not add content after the trailer.

## Final check

Before submitting, verify that:

- The heading is exactly `## VERSION - YYYY-MM-DD`.
- The version has no `v` prefix.
- The summary is exactly `Impact: N`.
- The number of bullets equals the number of supplied changes.
- Every pending change appears exactly once.
- No change was combined, split, omitted, or supplemented with invented facts.
- Literal code-related names use inline code formatting.
- Public interface and shipped-typing changes use `A`.
- Runtime changes through unchanged interfaces use `B`.
- Compatible user-visible bug corrections use `B2` unless explicit supported breakage is supplied.
- Environment and wheel availability changes use `C`.
- Added environment support uses `C2`; removed support uses `C1`.
- Documentation, tests, internal refactors, and output-preserving work use `C3`.
- Bullets follow the required marker order.
- Changes sharing a marker retain their supplied order.
- `Impact` is the lowest marker digit.
- The trailer is present and is the final line.