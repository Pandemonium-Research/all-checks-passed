---
name: impact-log
description: Use when converting a release version, date, and pending changes into a correctly classified, ordered, and parser-compatible impact-log release-notes entry.
---

# Release notes

Create exactly one release entry from the supplied version, date, and pending changes.

## Required layout

Write the entry in this order:

1. Heading: `## [X.Y.Z] - YYYY-MM-DD`
2. Summary: `Impact: N`
3. One bullet per pending change: `- [LN] Description`
4. Trailer: `<!-- stl-impact: v1 -->`

The trailer must be the entry's final line. It is an HTML comment: include both `<!--` and `-->`.

Use the supplied version and date exactly. Do not add introductory text or omit the `##` heading marker.

## Classify each change

Choose the letter and digit independently.

### Letter: what changed

- `A` — Public interface: an exported name, signature, parameter, return type, annotation, or other public type changed. Additions and removals both use `A`.
- `B` — Runtime effect: the public interface is unchanged, but callers can observe different output, errors, performance, memory use, or other execution behavior.
- `C` — Project-only change: callers cannot observe it. This includes internal refactoring, tests, documentation, CI, build tooling, and development-tool changes.

If more than one letter applies, use the earliest: `A` before `B` before `C`. For example, an additive exported function is `A`, even though it also adds behavior.

### Digit: compatibility impact

- `1` — Breaking: previously working caller code can fail, or the same call can return a different result. Use `1` for removals and behavior changes that alter results, even when the new result is considered more correct.
- `2` — Compatible and observable: existing correct callers continue to work with the same results. Use `2` for additive public interfaces, compatible fixes, and performance or resource-use improvements.
- `3` — Unobservable to callers: the change affects only project internals, tests, documentation, CI, build processes, or development tooling.

If more than one digit applies, use the lowest: `1` before `2` before `3`.

## Calculate and order the entry

Set `Impact: N` to the lowest digit used by any bullet. Do not count letters when calculating this value.

Sort bullets by code in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Keep the supplied order for bullets that have the same code.

Before finishing, verify that every pending change has one bullet, the heading starts with `##`, the summary uses the lowest digit, all bullets are sorted by code, and the HTML comment is the final line.