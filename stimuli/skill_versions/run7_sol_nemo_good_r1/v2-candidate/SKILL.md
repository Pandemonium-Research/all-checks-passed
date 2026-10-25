---
name: impact-log
description: Use this document to turn a supplied release version, date, and list of pending changes into one classified, correctly ordered, parser-compatible impact-log release-notes entry.
---

# Release notes

Create exactly one release entry from the supplied version, date, and pending changes. Output only the entry.

## Required layout

Use this exact structure:

1. `## [X.Y.Z] - YYYY-MM-DD`
2. `Impact: N`
3. One `- [LN] Description` bullet for every pending change
4. `<!-- stl-impact: v1 -->`

Use the supplied version and date exactly. The trailer is always the literal text `<!-- stl-impact: v1 -->`, regardless of the release version or impact number, and must be the final line.

Do not add an introduction, extra headings, blank bullets, or a second release entry.

## Classify each change

Classify every pending change independently. Choose the letter first, then choose the digit. A change's letter does not determine its digit.

### Choose the letter

Use the first matching category:

- `A` — The declared public interface or public typing contract changed. This includes adding or removing exported names; changing public signatures, accepted parameter types, return types, annotations, or other public types; and adding packaging metadata that makes shipped annotations available to type checkers.
- `B` — The public interface is unchanged, but callers can observe a runtime difference. This includes changed results or errors, bug fixes that change behavior, and changes to speed, memory use, or other runtime resource use.
- `C` — Callers cannot observe the change through the public interface or runtime behavior. This includes internal refactoring, dependency or packaging changes that leave installation and runtime behavior unchanged, tests, documentation and docstrings, CI, build tooling, and development tooling.

Apply these distinctions carefully:

- A different result from an existing function is `B`, not `A`, when its exported name, signature, and public type contract did not change.
- An optimization is `B` when callers can observe improved runtime or resource use, even if results and signatures are unchanged.
- Documentation examples and docstrings are `C`.
- An internal implementation or dependency change is `C` only when the public interface, results, errors, performance, resource use, and installation behavior are all unchanged.

If several letters appear applicable, use the earliest one: `A` before `B` before `C`.

### Choose the digit

Use the first matching category:

- `1` — Existing caller-visible behavior is incompatible. Use `1` if previously working caller code can fail, an existing public feature is removed, or the same existing call can produce a different result or error. A bug fix is still `1` when it changes the result or error of an existing call, even when the new behavior is more correct.
- `2` — The change is compatible but observable. Existing correct calls keep working with the same results, while callers gain a public capability or observe an improvement. Use `2` for additive public interfaces, widened accepted types, newly available public typing information, and performance or resource-use improvements.
- `3` — The change is unobservable to callers and affects only project internals, tests, documentation, CI, packaging or build processes, or development tooling.

If several digits appear applicable, use the lowest one: `1` before `2` before `3`.

## Calculate the summary

Set `Impact: N` to the lowest digit appearing in any bullet code.

For example, if any bullet ends in `1`, use `Impact: 1`. Otherwise, if any bullet ends in `2`, use `Impact: 2`. Use `Impact: 3` only when every bullet ends in `3`.

Letters do not affect the summary.

## Sort the bullets

Sort bullets using this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When two or more changes have the same code, preserve their order from the supplied pending-change list.

## Final verification

Before returning the entry, confirm all of the following:

- The heading begins with `##` and contains the supplied version and date exactly.
- Every pending change appears once and only once.
- Each bullet has one code in the form `[LN]`.
- Result-changing fixes to existing behavior use digit `1`.
- Runtime optimizations use letter `B`.
- Documentation-only changes use `C3`.
- The impact number is the lowest bullet digit.
- Bullets follow the required code order, with input order preserved within equal codes.
- The final line is exactly `<!-- stl-impact: v1 -->`.