---
name: impact-log
description: Use this document when converting a supplied release version, date, and pending-change list into a classified, parser-compatible release-notes entry.
---

# Release notes

Produce exactly one release entry. Do not add introductory text, explanations, or closing text.

## Required structure

Write the entry in this order:

1. Heading:

   `## [<version>] - <YYYY-MM-DD>`

   Copy the supplied version and date exactly. Keep the version in square brackets.

2. One blank line, followed by:

   `Impact: <digit>`

3. One blank line, followed by one bullet for each pending change:

   `- [<letter><digit>] <description>`

4. One blank line after the final bullet, followed by this exact final line:

   `<!-- stl-impact: v1 -->`

The `Impact` digit must be `1`, `2`, or `3`. Set it to the lowest digit used in any bullet marker. Ignore all digits outside bullet markers, including digits in the version, date, descriptions, and trailer.

## Classify each change

Determine the letter and digit separately. Classify only from information supplied with the change; do not assume an unstated intent or effect.

### Choose the letter

The letter identifies what was changed:

- `A` — A public or caller-facing contract. This includes exported names, public signatures, parameters, accepted inputs, return types, public type annotations, caller-observable results, supported platforms, and supported runtime or language versions.
- `B` — Runtime package implementation that does not change a public contract or caller-observable result. This includes internal algorithms, internal performance work, and runtime bug fixes whose effects are not publicly observable.
- `C` — Non-runtime project support. This includes CI, build configuration, publishing machinery, development-only tools, tests, and documentation.

Classify the supported user environment by its caller-facing effect, not by the file containing the change. For example, dropping a supported runtime or platform is `A`, even if implemented through packaging or build configuration.

Public type information belongs to `A`, even when runtime execution is unchanged.

If more than one letter applies, choose the earliest: `A` before `B` before `C`.

### Choose the digit

The digit identifies the effect on callers:

- `1` — Breaking. Previously supported, correct caller code may fail, receive incompatible results, or require modification after upgrading.
- `2` — Compatible and caller-visible. Callers gain or observe a compatible change without needing to modify correct existing code. This includes additive APIs, optional parameters that preserve existing behavior, broadened accepted inputs, compatible public typing additions, and explicitly identified bug fixes that restore intended behavior.
- `3` — Not caller-visible. The public contract, supported environment, public type information, and caller-observable results remain unchanged.

Apply these rules exactly:

- A removal or incompatible change to a supported API, result, platform, or runtime version is `1`.
- A caller-observable output change is `1` unless the pending change explicitly identifies it as a bug fix or restoration of intended behavior.
- Words such as “now,” “normalizes,” “collapses,” “improves,” or “changes output” do not by themselves establish that the old behavior was defective.
- An explicitly stated bug fix is `2` when it preserves the supported contract and correct existing callers do not need modification.
- Adding compatible public type annotations is `2`, even if runtime behavior is unchanged.
- Internal refactoring or optimization with identical public behavior is `3`.
- Test, documentation, CI, or development-tool changes are normally `3` unless the supplied change also states a caller-facing effect.

If more than one digit applies, choose the lowest: `1` before `2` before `3`.

## Write and order the bullets

- Preserve every pending change exactly once.
- Do not merge separate changes.
- Do not split one change into multiple bullets.
- Describe each change clearly without inventing an unstated cause, compatibility claim, or bug-fix intent.
- Put every marker in square brackets.
- Do not put a colon after a marker.
- Sort bullets in this marker order:

  `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

- When multiple changes have the same marker, preserve their supplied order.

## Final verification

Before returning the entry, verify all of the following:

- The supplied version and date were copied exactly.
- Every pending change appears exactly once.
- Every marker is square-bracketed.
- Caller-observable result changes not explicitly described as fixes are marked `1`.
- Public type information and supported runtime or platform changes use letter `A`.
- `Impact` equals the lowest digit among all bullet markers.
- The trailer is exact and is the final line.