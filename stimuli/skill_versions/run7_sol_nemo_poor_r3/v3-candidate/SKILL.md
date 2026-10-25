---
name: impact-log
description: Use this document to classify, sort, and format a supplied version, date, and list of pending changes as one release-notes entry with an overall impact value.
---

# Release notes

Create exactly one release entry from the supplied inputs.

Include every pending change exactly once. Do not combine changes, split a change into multiple bullets, omit supplied facts, or invent facts about compatibility or user impact.

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

## Classify each change

For each pending change:

1. Select one letter using the letter decision tree.
2. Select one digit independently using the digit decision tree.
3. Write one bullet containing the supplied change's meaningful facts.
4. Sort all bullets by marker.
5. Set `Impact` to the lowest marker digit.

Each bullet must begin in this form:

```text
- [A2] Description.
```

If one pending change has several effects, assign it one marker. Use the earliest applicable letter in the order `A`, `B`, `C`, and the lowest applicable digit in the order `1`, `2`, `3`.

## Choose the marker letter

Apply these questions in order.

### 1. Did the public interface or shipped typing surface change?

If yes, use `A`.

Public-interface changes include:

- Adding, removing, renaming, or relocating an exported name.
- Changing a public import path.
- Changing a public function or method signature.
- Adding, removing, or changing parameters or return types.
- Changing public annotations, stubs, or other typing information shipped to type checkers.
- Making shipped annotations newly discoverable to type checkers.

An added public function is `A`. Shipped typing support is also `A`.

Do not use `A` merely because an existing function returns a different result. If its interface and shipped typing surface are unchanged, continue to the next question.

### 2. Did calls through an unchanged public interface behave differently?

If yes, use `B`.

Runtime-behavior changes include changes to:

- Returned values or generated output.
- Accepted or rejected input values when the signature and typing surface are unchanged.
- Parsing, counting, formatting, or validation results.
- Raised exceptions.
- Side effects or other observable call behavior.

A bug correction that changes an existing function's result is `B`, not `A`, unless the change also modifies its public interface or shipped typing surface.

### 3. Otherwise, use `C`

Use `C` when neither the public interface nor runtime call behavior changes. This includes:

- Supported installation, wheel, platform, or interpreter availability.
- Build and packaging implementation.
- Dependency management or vendoring.
- Documentation and docstring-only edits.
- Tests and development tooling.
- Performance-only work with unchanged results.
- Internal refactoring or implementation replacement.

Installation and environment support changes use `C`, even when they are user-visible. Their digit indicates whether support was added, removed, or left unchanged.

If an internal, dependency, or packaging change is explicitly described as changing public runtime results, classify that result change as `B`. Do not infer a runtime change merely because an implementation or dependency changed.

## Choose the marker digit

Choose the digit from the stated effect on supported users. Do not assume that a change is breaking merely because some output changed.

Apply these questions in order.

### 1. Does the change break supported use?

If yes, use `1`.

Use `1` when the supplied change says or clearly entails that previously supported code or environments can no longer work as supported. Examples include:

- Removing or incompatibly changing a public interface.
- Adding a required argument to an existing call.
- Removing accepted, supported input.
- Intentionally changing an established supported result incompatibly.
- Dropping a supported interpreter, platform, wheel, or installation method.
- Introducing an explicitly incompatible exception or side effect.

A result change is not automatically `1`. A correction to erroneous behavior normally uses `2`. Use `1` for a fix only when the supplied information establishes that the new behavior incompatibly changes a supported contract or supported reliance. Do not speculate that callers might have relied on a bug.

### 2. Does the change add a compatible capability or correct user-visible behavior?

If yes, use `2`.

Use `2` for compatible, externally observable improvements such as:

- Adding a public API.
- Adding an optional parameter or compatible public type.
- Adding shipped typing support.
- Accepting an additional input through an unchanged interface.
- Correcting erroneous runtime output while supported existing use remains valid.
- Adding support for an interpreter, platform, wheel, or installation environment.

A user-visible bug correction defaults to `2` unless the supplied change explicitly establishes breaking impact.

Digit `2` does not mean that anything added anywhere qualifies. Added tests, documentation, internal code, caches, or packaging files use `3` when they do not add public capability, runtime behavior, or supported environment availability.

### 3. Otherwise, use `3`

Use `3` when public API, runtime results, and supported installation or environment availability remain unchanged.

Normally use `3` for:

- Documentation or docstring-only changes.
- Tests and development-tool changes.
- Internal refactors.
- Output-preserving performance improvements.
- Dependency vendoring with unchanged supported behavior.
- Packaging or build-system rearrangements that preserve supported installation.
- Moving internal files without changing supported use.

## Common marker combinations

Use these combinations as classification checks:

- Public API or shipped typing added compatibly: `A2`.
- Public API removed or changed incompatibly: `A1`.
- Existing API produces a compatible bug-corrected result: `B2`.
- Existing API changes a supported result incompatibly: `B1`.
- New supported interpreter, platform, wheel, or installation availability: `C2`.
- Supported interpreter, platform, wheel, or installation availability removed: `C1`.
- Documentation, tests, internal refactoring, or output-preserving optimization: `C3`.
- Dependency or packaging rearrangement with unchanged support and behavior: `C3`.

## Calculate Impact

Set `Impact` to the lowest digit among all bullet markers.

For example, markers containing digits `2`, `1`, and `3` produce:

```text
Impact: 1
```

Count only marker digits. Ignore numbers in the version, date, descriptions, performance measurements, and identifiers.

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
- Every pending change appears exactly once.
- No supplied change was combined, split, or supplemented with invented claims.
- Every bullet starts with a bracketed marker.
- Public interface and shipped typing changes use `A`.
- Runtime result changes through unchanged interfaces use `B`.
- Installation and environment support changes use `C`.
- Compatible user-visible bug corrections use `2`, unless breaking impact is explicitly established.
- Added environment support uses `C2`; removed supported environments use `C1`.
- Documentation, tests, internal refactors, and output-preserving performance work use `C3`.
- Output-preserving dependency and packaging rearrangements use `C3`.
- Bullets follow the required marker order.
- Changes sharing a marker retain their supplied order.
- `Impact` is the lowest marker digit.
- The trailer is present and is the final line.