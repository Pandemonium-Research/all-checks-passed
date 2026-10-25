---
name: impact-log
description: Use this skill to turn a release version, date, and list of pending changes into a correctly classified, sorted, parser-compatible release-notes entry in the project's impact-log format.
---

# Release notes

Create one entry containing every pending change exactly once.

## Required format

Use this structure:

```text
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: LOWEST_DIGIT
- [CODE] Change description.
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Follow these requirements exactly:

- Use a level-two Markdown heading beginning with `##`.
- Write the version as three numeric components inside square brackets.
- Write the date as `YYYY-MM-DD`.
- Put `Impact: N` immediately below the heading.
- Begin every bullet with `- [CODE]`, placing the code before its description.
- End with the exact HTML comment `<!-- stl-impact: v1 -->`.
- Make the trailer comment the entry's final line. Do not put text, bullets, or another heading after it.

## Assigning impact codes

Each code consists of one letter and one digit. Classify the change's affected surface first, then its compatibility.

### Choose the letter

- `A` — The public API contract changes. This includes exported modules or names, function or method signatures, accepted or returned types, and public type definitions.
- `B` — Observable runtime behavior changes without changing the public API contract. This includes results, exceptions, side effects, timing, performance, or resource use.
- `C` — The change concerns packaging, supported environments, dependencies, builds, tooling, tests, documentation, or an internal implementation detail with no observable runtime effect.

Apply these distinctions consistently:

- Adding or removing an exported name is `A`.
- Changing a return type is `A`, even when it also changes runtime behavior.
- Changing the result of an existing call without changing its signature or types is `B`.
- Improving runtime or import performance is `B`, even when results are unchanged.
- Dropping support for a language or platform version is `C`, not `A`.
- Dependency vendoring and distribution metadata are `C`.
- Documentation-only and test-only changes are `C`.

If more than one letter applies, use the earliest letter: `A` before `B` before `C`.

### Choose the digit

- `1` — Breaking or incompatible. Something that previously worked on the affected surface can now fail, become unsupported, or produce a different result.
- `2` — Compatible but externally observable. This includes additions, bug fixes, performance improvements, and compatible packaging or tooling changes.
- `3` — Completely unobservable to users or consumers. Reserve this for purely internal or editorial work that changes no API, runtime behavior, supported environment, package metadata, or consumer-facing tooling behavior.

Do not use `3` merely because output is unchanged. Performance, resource usage, installation behavior, dependency changes, and type-checker behavior are observable and therefore use `2` unless they are breaking.

If more than one digit applies, use the lowest digit: `1` before `2` before `3`.

## Impact summary and ordering

Set the `Impact` value to the lowest digit used by any bullet in the entry.

Sort bullets by code in this exact order:

```text
A1, A2, A3, B1, B2, B3, C1, C2, C3
```

For bullets with the same code, preserve their order from the supplied pending-changes list.