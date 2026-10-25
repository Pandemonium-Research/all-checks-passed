---
name: impact-log
description: Use this skill when given a release version, release date, and pending changes to produce one classified, sorted, machine-parseable release-notes entry in the project's impact-log format.
---

# Release notes

Produce exactly one release entry containing every supplied change once. Output only the entry, without commentary or a Markdown code fence.

## Required layout

Use this exact layout:

    ## [VERSION] - YYYY-MM-DD
    Impact: DIGIT

    - [CODE] Change description.
    - [CODE] Change description.

    <!-- stl-impact: v1 -->

Formatting requirements:

- Copy the supplied version exactly inside square brackets. Do not infer or change the version based on impact.
- Copy the supplied date in `YYYY-MM-DD` form.
- Put `Impact: DIGIT` immediately below the heading.
- Begin every bullet with one code in square brackets. Never put the code at the end.
- Leave one blank line after the impact line and one blank line before the trailer.
- Use `<!-- stl-impact: v1 -->` exactly as shown.
- Make the trailer the final line; put nothing after it.

## Classify each change independently

Each code contains one letter and one digit. The letter identifies what the change affects; the digit identifies its compatibility impact.

### Choose the letter

- `A` — Public API surface: exported names, signatures, parameters, return types, public types, annotations, or typing metadata exposed to consumers and type checkers.
- `B` — Observable runtime behavior of existing functionality without a public API-surface change. This includes changes to results, exceptions, side effects, timing, memory use, or other resource behavior.
- `C` — Internals, build, packaging, dependencies, tooling, tests, CI, or documentation, provided the change does not qualify as `A` or `B`.

Choose by effect, not implementation. An internal implementation change that observably changes runtime performance or resource use is `B`, not `C`.

If more than one letter applies, use the first in this precedence order:

`A`, then `B`, then `C`.

### Choose the digit

- `1` — Breaking: previously supported, working usage can now fail, become invalid, or produce a different result.
- `2` — Compatible and observable: the change adds capability, fixes a defect, or provides an observable improvement while correct existing usage continues to work.
- `3` — Unobservable: consumers cannot observe the change in supported use.

Documentation, test, CI, and behavior-preserving refactoring changes are normally `3`. Do not use `3` merely because output is unchanged when timing, memory, installation, typing, or another supported consumer-visible effect changes.

If more than one digit applies, use the lowest digit:

`1`, then `2`, then `3`.

Combine the selected letter and digit, such as `[A2]`. Do not copy the release-level impact digit onto every bullet.

## Order the bullets

After classifying all changes, sort the bullets by this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Preserve the supplied relative order only among changes with the same code.

## Calculate the impact summary

Set `Impact` to the lowest digit used by any bullet:

- If any bullet ends in `1`, write `Impact: 1`.
- Otherwise, if any bullet ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore the letters when calculating the summary.

## Final verification

Before returning the entry, confirm that:

- The supplied version and date are unchanged.
- Every supplied change appears exactly once.
- Every bullet begins with one valid code.
- The bullets follow the required code order.
- `Impact` is the lowest bullet-code digit.
- The exact trailer is present as the final line.