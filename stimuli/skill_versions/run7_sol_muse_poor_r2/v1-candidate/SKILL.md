---
name: impact-log
description: Use this guide to turn a release version, date, and list of pending changes into a correctly classified, ordered, parser-compatible release notes entry.
---

# Release notes

Follow these steps for every release.

## 1. Write the heading

Use this exact format:

`## [VERSION] - YYYY-MM-DD`

The version must contain three numeric parts, such as `1.4.0`. Use the supplied date in year-month-day order.

## 2. Write one bullet for each pending change

Represent every pending change exactly once. Do not combine changes or split one change across multiple bullets.

Use this format:

`- [LD] Description of the change.`

`L` is the impact letter and `D` is the impact digit. Classify each change independently.

## 3. Choose the impact letter

Choose the first applicable letter:

- `A` — Public API or typing surface. Use this when the change adds, removes, or modifies exported names, call signatures, parameters, return types, public annotations, or the availability of shipped type information to type checkers.
- `B` — Runtime behavior. Use this when an existing public operation behaves differently without changing its public API or typing surface.
- `C` — Project internals and supporting material only. Use this for builds, packaging internals, tooling, tests, documentation, refactoring, or implementation changes that do not qualify for `A` or `B`.

If multiple letters appear applicable, use the earliest letter: `A` before `B` before `C`.

## 4. Choose the impact digit

Choose the first applicable digit:

- `1` — Breaking. Previously supported, correct caller code may now fail, become invalid, or produce a different result.
- `2` — Compatible and externally useful. This includes additive public APIs, newly supported platforms or installation targets, performance improvements callers can observe, and bug fixes that correct previously erroneous behavior while preserving correct existing usage.
- `3` — No caller-observable effect. Use this for documentation-only work, test organization, refactoring, cache or dependency implementation changes with unchanged behavior, and other maintenance invisible to callers.

A bug fix is not automatically `1`: use `2` when it changes only behavior that was previously incorrect and correct existing code remains valid.

A packaging change is not automatically `3`: use `2` when it adds or changes a supported way to install or run the package.

If more than one digit could apply, use the lowest digit: `1` before `2` before `3`.

Choose the letter and digit separately. Any valid letter may be paired with any valid digit.

## 5. Sort the bullets

Sort bullets by their complete marker in this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep the supplied order for bullets with the same marker.

## 6. Write the Impact summary

Immediately below the heading, write:

`Impact: D`

Replace `D` with the lowest digit used in any bullet marker. This is the minimum impact digit, not the number of changes and not the most frequent digit.

## 7. Add the parser trailer

After the final bullet, add this exact line, including the spaces inside the comment:

`<!-- stl-impact: v1 -->`

The complete entry must therefore have this structure:

## [VERSION] - YYYY-MM-DD
Impact: D
- [LD] First pending change.
- [LD] Second pending change.
<!-- stl-impact: v1 -->

Before submitting, verify that every pending change appears once, every bullet has a valid marker, the bullets are sorted by marker, the Impact value is the lowest marker digit, and the trailer matches exactly.