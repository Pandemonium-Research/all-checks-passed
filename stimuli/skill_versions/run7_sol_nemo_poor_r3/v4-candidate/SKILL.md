---
name: impact-log
description: Use this document to turn a supplied release version, date, and list of pending project changes into one correctly classified, sorted release-notes entry with an overall impact value.
---

# Release notes

Create exactly one release entry from the supplied version, date, and pending changes.

Include every pending change exactly once. Write one bullet per pending change: do not combine changes, split a change across bullets, omit supplied facts, or invent effects that were not supplied.

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
- `LOWEST_DIGIT` with the lowest digit used by any marker.

The heading must begin with exactly two `#` characters. Write the summary exactly as `Impact: N`.

## Process the pending changes

Before writing, make a one-to-one inventory of the supplied changes.

For each change:

1. Choose one letter using the letter rules.
2. Choose one digit independently using the digit rules.
3. Write one bullet that preserves all meaningful supplied facts.
4. Sort the completed bullets by marker.
5. Set `Impact` to the lowest marker digit.

Each bullet must begin in this form:

```text
- [A2] Description.
```

If several classifications apply to one change, use the earliest applicable letter in the order `A`, `B`, `C` and the lowest applicable digit in the order `1`, `2`, `3`.

Classify only from the supplied information. Do not infer compatibility, breakage, behavior changes, or user impact merely from how an implementation was changed.

## Choose the marker letter

Apply these questions in order.

### 1. Did the public interface or shipped typing surface change?

If yes, use `A`.

This includes:

- Adding, removing, renaming, or relocating an exported name.
- Changing a public import path.
- Changing a public function or method signature.
- Adding, removing, or changing parameters or return types.
- Changing public annotations or stubs shipped to type checkers.
- Making shipped annotations newly discoverable to type checkers.

A newly exported public function is `A`. Adding typing metadata that makes shipped annotations available to type checkers is also `A`.

Do not use `A` merely because an existing function returns a different result or accepts a different value. If its public signature and shipped typing surface are unchanged, continue to the next question.

### 2. Did calls through an unchanged public interface behave differently?

If yes, use `B`.

This includes changes to:

- Returned values or generated output.
- Accepted or rejected input values.
- Parsing, counting, formatting, or validation results.
- Raised exceptions.
- Side effects or other observable call behavior.

A bug correction that changes an existing function's result is `B`, not `A`, when the public interface and typing surface remain unchanged.

### 3. Otherwise, use `C`

Use `C` when neither the public interface nor runtime call behavior changes. This includes:

- Supported interpreter, platform, wheel, or installation availability.
- Build and packaging implementation.
- Dependency management or vendoring.
- Documentation and docstring-only edits.
- Tests and development tooling.
- Performance-only work with unchanged results.
- Internal refactoring or implementation replacement.

Installation and environment support changes use `C`, even though users can observe them. Use the digit to distinguish added support, removed support, and unchanged support.

If an internal, dependency, or packaging change is explicitly stated to change public runtime behavior, classify that behavior change as `B`. Do not infer such a change from the implementation alone.

## Choose the marker digit

Choose the digit from the stated effect on supported users.

### 1. Does the change break supported use?

If yes, use `1`.

Use `1` when the supplied information explicitly states or necessarily establishes that previously supported code or environments can no longer work as supported. Examples include:

- Removing or incompatibly changing a public interface.
- Adding a required argument to an existing call.
- Removing previously supported input.
- Intentionally changing a documented or supported result incompatibly.
- Dropping a supported interpreter, platform, wheel, or installation method.
- Introducing an explicitly incompatible exception or side effect.

A changed result is not automatically breaking. Do not use `1` merely because callers could have relied on erroneous behavior.

A change described as a correction or bug fix normally uses `2`. Use `1` for such a change only when the supplied information explicitly establishes that a supported contract or supported use is being broken.

### 2. Does the change add a compatible capability or correct user-visible behavior?

If yes, use `2`.

Use `2` for compatible, externally observable improvements such as:

- Adding a public API.
- Adding an optional parameter or compatible public type.
- Adding or exposing shipped typing support.
- Accepting an additional input through an unchanged interface.
- Correcting erroneous runtime behavior while supported use remains valid.
- Adding support for an interpreter, platform, wheel, or installation environment.

Words such as “fix,” “correct,” or “now handles correctly” indicate `2` unless the supplied information also explicitly identifies a breaking supported-contract change.

Digit `2` does not mean that every addition qualifies. Added documentation, tests, internal code, caches, build files, or packaging files use `3` when they do not add a public capability, runtime behavior, or supported environment.

### 3. Otherwise, use `3`

Use `3` when public API, runtime results, and supported installation or environment availability remain unchanged.

Normally use `3` for:

- Documentation or docstring-only changes.
- Tests and development-tool changes.
- Internal refactoring.
- Output-preserving performance improvements.
- Dependency vendoring with unchanged supported behavior.
- Packaging or build-system rearrangements that preserve supported installation.
- Moving internal files without changing supported use.

## Classification checks

Use these combinations to check each decision:

- Compatible public API or shipped typing addition: `A2`.
- Removed or incompatibly changed public API: `A1`.
- Compatible bug correction through an unchanged interface: `B2`.
- Additional accepted input through an unchanged interface: `B2`.
- Explicitly incompatible supported behavior change: `B1`.
- Added interpreter, platform, wheel, or installation support: `C2`.
- Removed interpreter, platform, wheel, or installation support: `C1`.
- Documentation, tests, internal refactoring, or output-preserving optimization: `C3`.
- Dependency or packaging rearrangement with unchanged behavior and support: `C3`.

## Calculate Impact

Set `Impact` to the lowest digit among all bullet markers.

For example, markers containing digits `2`, `1`, and `3` produce:

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
- The number of bullets equals the number of supplied pending changes.
- Every pending change appears exactly once.
- No pending change was combined, split, or supplemented with invented facts.
- Every bullet starts with a bracketed marker.
- Public interfaces and shipped typing changes use `A`.
- Runtime changes through unchanged interfaces use `B`.
- Installation and environment support changes use `C`.
- User-visible bug corrections use `2` unless breaking supported impact is explicitly established.
- Added environment support uses `C2`.
- Removed supported environments use `C1`.
- Documentation, tests, internal refactors, and output-preserving performance work use `C3`.
- Output-preserving dependency and packaging rearrangements use `C3`.
- Bullets follow the required marker order.
- Changes sharing a marker retain their supplied order.
- `Impact` is the lowest marker digit.
- The trailer is present and is the final line.