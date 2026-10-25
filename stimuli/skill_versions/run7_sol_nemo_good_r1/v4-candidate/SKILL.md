---
name: impact-log
description: Use when turning a supplied release version, date, and pending-change list into one correctly classified, stably ordered, parser-compatible impact-log release-notes entry.
---

# Release notes

Produce exactly one release entry. Output only the entry, with no introduction or explanation.

## Required format

Use exactly this structure:

1. `## [X.Y.Z] - YYYY-MM-DD`
2. `Impact: N`
3. One `- [LN] Description` bullet for each pending change
4. `<!-- stl-impact: v1 -->`

Use the supplied version and date exactly. Replace `N`, each code, and each description as required.

The trailer is always the literal text `<!-- stl-impact: v1 -->`. Its `v1` does not change with the release version or impact number. The trailer must be the final line.

## Process every pending change

For each pending change:

1. Record its position in the supplied list.
2. Choose its letter.
3. Choose its digit independently.
4. Write exactly one accurate bullet for it.
5. After classifying every change, sort the bullets as specified below.

Do not combine, duplicate, or omit changes.

## Choose the letter

Use the first applicable letter:

- `A` — The declared public interface or public typing contract changed. Use `A` for added or removed exported names; changed public signatures, parameters, return types, or annotations; widened or narrowed accepted argument types; and packaging metadata that makes shipped annotations available to type checkers.
- `B` — The public interface and typing contract are unchanged, but callers can observe a runtime difference. Use `B` for changed results or errors, behavior-changing bug fixes, and changes to speed, memory use, or other runtime resources.
- `C` — Callers cannot observe the change through the public interface, typing contract, installation, or runtime behavior. Use `C` for documentation and docstrings, tests, CI, development tooling, internal refactoring, and dependency, packaging, or build changes that do not affect users.

Apply these rules carefully:

- A new exported function, a newly accepted public argument type, or a changed public annotation is `A`.
- Metadata that makes existing shipped annotations discoverable by type checkers is `A`.
- A changed result or error from an existing call is `B`, not `A`, unless the declared public interface or typing contract also changed.
- A runtime or resource-use optimization is `B`, even when results and signatures are unchanged.
- Documentation text, documentation examples, and docstrings are `C`.
- An internal cache, dependency, packaging, or build change is `C` only if the interface, typing, installation, results, errors, performance, and resource use remain unchanged.

If multiple letters apply, select the earliest: `A` before `B` before `C`.

## Choose the digit

Use the first applicable digit:

- `1` — Existing caller-visible behavior is incompatible. Use `1` if previously working caller code can fail, a public capability is removed, or the same existing call can return a different result or raise a different error.
- `2` — The change is compatible but observable. Use `2` when existing correct calls retain the same results while callers gain a public capability, a broader accepted type, newly usable typing information, or improved performance or resource use.
- `3` — The change is unobservable to callers and affects only project internals, documentation, tests, CI, dependencies, packaging, build processes, or development tooling.

A bug fix that changes the result or error of an existing call is digit `1`, even if the previous behavior was incorrect and the new behavior is desirable. Digit `2` applies to a fix only when existing correct calls keep the same results and errors.

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

- The heading begins with `##` and contains the supplied version and date exactly.
- Every pending change appears exactly once.
- Every bullet begins with one code in the form `[LN]`.
- Public-interface and public-typing changes use `A`.
- Changed results or errors from existing calls use `B1` unless the public contract also changed.
- Runtime and resource-use improvements use `B2`.
- Documentation and docstring changes use `C3`.
- Unobservable internal, dependency, packaging, and build changes use `C3`.
- `Impact: N` contains the lowest bullet digit.
- Bullets follow the required code order.
- Equal-code bullets retain their supplied order.
- The final line is exactly `<!-- stl-impact: v1 -->`.