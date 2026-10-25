---
name: impact-log
description: Use when turning a supplied release version, date, and pending-change list into one classified, stably ordered, parser-compatible impact-log release-nototes entry.
---

# Release notes

Produce exactly one release entry. Output only the entry, with no introduction or explanation.

## Required format

Use exactly this structure:

1. `## [X.Y.Z] - YYYY-MM-DD`
2. `Impact: N`
3. One `- [LN] Description` bullet for each pending change
4. `<!-- stl-impact: v1 -->`

Replace only the version, date, impact number, codes, and descriptions. The trailer is always the literal text `<!-- stl-impact: v1 -->`; `v1` does not change with the release version or impact number.

Use the supplied version and date exactly. The trailer must be the final line.

## Process every pending change

For each pending change:

1. Record its position in the supplied list.
2. Choose its letter.
3. Choose its digit independently.
4. Write exactly one bullet that accurately describes the change.
5. After classifying all changes, sort the bullets as specified below.

Do not combine, duplicate, or omit changes.

## Choose the letter

Use the first applicable letter:

- `A` — The declared public interface or public typing contract changed. Use `A` for added or removed exports, changed public signatures, widened or narrowed accepted parameter types, changed return types or annotations, and packaging metadata that makes shipped type information available to type checkers.
- `B` — The public interface and typing contract are unchanged, but callers can observe a runtime difference. Use `B` for changed results or errors, bug fixes affecting behavior, and improvements or regressions in speed, memory use, or other runtime resources.
- `C` — Callers cannot observe the change through the public interface, typing contract, installation, or runtime behavior. Use `C` for documentation and docstrings, tests, CI, development tooling, internal refactoring, and dependency, packaging, or build changes that do not affect users.

Apply these rules before considering the digit:

- A new public function or newly accepted public argument type is `A`.
- Making existing shipped annotations discoverable by type checkers is `A`.
- A different result from an existing call is `B`, not `A`, unless the public interface or typing contract also changed.
- A runtime optimization is `B`, even when results and signatures are unchanged.
- Documentation text, examples, and docstrings are `C`.
- An internal implementation, dependency, packaging, or build change is `C` only when interface, typing, installation, results, errors, performance, and resource use remain unchanged.

If multiple letters apply, select the earliest: `A` before `B` before `C`.

## Choose the digit

Use the first applicable digit:

- `1` — Existing caller-visible behavior is incompatible. Use `1` if previously working caller code can fail, a public capability is removed, or the same existing call can return a different result or raise a different error.
- `2` — The change is compatible but observable. Use `2` when existing correct calls retain the same results while callers gain a public capability, broader accepted types, newly usable typing information, or improved performance or resource use.
- `3` — The change is unobservable to callers and affects only project internals, documentation, tests, CI, packaging, build processes, dependencies, or development tooling.

A behavior-changing bug fix is digit `1`, even when the old behavior was incorrect and the new behavior is desirable. Do not call such a fix compatible merely because it corrects a bug.

If multiple digits apply, select the lowest: `1` before `2` before `3`.

## Calculate the summary

Set `Impact: N` to the lowest digit used by any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Letters do not affect the summary.

## Sort the bullets

Sort bullets by this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For bullets with the same code, preserve their relative order from the supplied pending-change list.

## Final verification

Before returning the entry, verify that:

- The heading begins with `##` and uses the supplied version and date exactly.
- Every pending change appears exactly once.
- Every bullet begins with one code in the form `[LN]`.
- Public-interface and public-typing changes use `A`.
- Result- or error-changing fixes to existing calls use digit `1`.
- Runtime and resource-use changes use `B`.
- Documentation-only changes use `C3`.
- Unobservable dependency, packaging, and internal changes use `C3`.
- `Impact: N` contains the lowest digit found in the bullets.
- Bullets follow the required code order.
- Equal-code bullets retain their supplied order.
- The final line is exactly `<!-- stl-impact: v1 -->`.