---
name: impact-log
description: Use this document to turn a supplied release version, date, and list of pending changes into a correctly classified, parser-compatible release-notes entry.
---

# Release notes

Create exactly one entry using this structure.

## Entry structure

1. Write the heading as:

   `## [<version>] - <YYYY-MM-DD>`

   Copy the supplied version and date exactly. Keep the version in square brackets.

2. Leave one blank line, then write:

   `Impact: <digit>`

   The digit must be `1`, `2`, or `3`. Use the lowest digit appearing in any change marker. Ignore all other digits, including those in the version, date, descriptions, and trailer.

3. Leave one blank line, then write one bullet for every pending change:

   `- [<letter><digit>] <description>`

   Square brackets are required. Do not put a colon after the marker.

4. Leave one blank line after the final bullet, then add this exact trailer:

   `<!-- stl-impact: v1 -->`

Do not add introductory text, explanations, or closing text.

## Classify each change

Choose the letter and digit independently. Use only information stated in the pending change; do not assume that an output change is a bug fix or that an interface is unsupported.

### Choose the letter

The letter identifies what changed:

- `A` — A public or caller-facing contract. This includes exported names, public functions and methods, signatures, parameters, accepted inputs, return types, caller-observable results, public type annotations, supported platforms, and supported runtime or language versions.
- `B` — Runtime package implementation without a change to the public contract or caller-observable results. This includes internal algorithms, performance work, resource-use fixes, and other runtime implementation fixes.
- `C` — Non-runtime project support. This includes CI, build configuration, packaging or publishing machinery, development-only tools, tests, and documentation.

Classify a change by its effect, not by the file containing it. In particular:

- Adding or changing public type annotations is `A`, even when runtime behavior is unchanged.
- Adding, dropping, or changing support for a runtime, language version, operating system, or platform is `A`, even when implemented in build or packaging configuration.
- Changing a public function’s output or error behavior is `A`.
- CI-only and development-only changes are `C`.

If more than one letter applies, use the earliest letter: `A` before `B` before `C`.

### Choose the digit

The digit identifies the effect on callers:

- `1` — Breaking. Correct code using the previously supported contract may fail, receive incompatible results, lose a supported environment, or require modification after upgrading.
- `2` — Compatible and caller-visible. Callers gain or observe a compatible change without needing to modify correct existing code.
- `3` — Not caller-visible. The public contract, supported environment, public type information, and caller-observable results remain unchanged.

Apply these rules:

- Removing or incompatibly changing a supported API, parameter, result, platform, or runtime version is `1`.
- A caller-observable output or error-behavior change is `1` unless the pending change explicitly says it fixes defective behavior or restores intended behavior.
- Words such as “now,” “normalizes,” “collapses,” “improves,” or “changes output” do not establish that the previous behavior was defective.
- An explicitly identified bug fix is `2` when it preserves the supported contract and correct existing callers do not need modification.
- A compatible new API or optional parameter that preserves existing behavior is `2`.
- Compatible public type annotations are `2`, even when runtime behavior is unchanged.
- An internal refactor or optimization with identical public behavior is `3`.
- CI, tests, documentation, and development-tool changes are normally `3` unless the pending change states a caller-facing effect.

If more than one digit applies, use the lowest digit: `1` before `2` before `3`.

## Write and order the bullets

- Preserve every pending change exactly once.
- Do not merge separate pending changes.
- Do not split one pending change into multiple bullets.
- Describe each change clearly without inventing an unstated cause, compatibility guarantee, or bug-fix intent.
- Sort bullets in this marker order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
- Preserve the supplied order when multiple changes have the same marker.

Before finishing, verify that:

- The supplied version and date were copied exactly.
- Every pending change appears exactly once.
- Every marker is square-bracketed.
- Uncorrected caller-observable result changes are marked `A1`.
- Public type information and supported-environment changes use `A`.
- `Impact` equals the lowest digit among all bullet markers.
- The exact trailer is the final line.