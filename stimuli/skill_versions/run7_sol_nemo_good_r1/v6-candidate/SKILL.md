---
name: impact-log
description: Use when turning a supplied release version, date, and pending-change list into one correctly classified, stably ordered, parser-compatible impact-log release-notes entry.
---

# Release notes

Produce exactly one release entry. Output only the entry, with no introduction, explanation, or code fence.

## Required format

Use exactly this structure:

1. `## [X.Y.Z] - YYYY-MM-DD`
2. `Impact: N`
3. One `- [LN] Description` bullet for each pending change
4. `<!-- stl-impact: v1 -->`

Use the supplied version and date exactly. Write one accurate bullet for every pending change; do not combine, omit, duplicate, or invent changes.

The trailer is always the literal text `<!-- stl-impact: v1 -->`. Its `v1` is fixed and does not change with the release version or impact number. The trailer must be the final line.

## Classify every change

For each pending change:

1. Record its position in the supplied list.
2. Choose its letter.
3. Choose its digit independently.
4. Write exactly one bullet describing it.
5. Sort all bullets only after every change has been classified.

## Choose the letter

Apply these tests in order and use the first matching letter.

### `A` — The declared public interface or typing contract changed

Use `A` for:

- added or removed exported names;
- changed public signatures, parameters, return types, or annotations;
- widened or narrowed types accepted by a public operation;
- packaging metadata, such as `py.typed`, that makes shipped annotations available to type checkers.

A function being public does not by itself make a change `A`. If an existing public function keeps the same declared interface but changes its result or error, use `B`.

### `B` — Runtime behavior or resource use changed

Use `B` when the public interface and typing contract are unchanged, but callers can observe a change in:

- returned results or raised errors;
- runtime behavior;
- import or startup time;
- execution speed;
- memory use or another runtime resource.

Runtime caching, cache-bounding, and lazy-import changes are `B` when they affect speed or resource use, even if signatures and output remain unchanged. Calling an implementation “internal” does not make its performance or memory effects unobservable.

### `C` — No caller-observable effect

Use `C` only when the interface, typing contract, installation behavior, results, errors, performance, and runtime resource use are all unchanged.

Typical `C` changes include:

- documentation, examples, and docstrings;
- tests and CI configuration;
- development tooling;
- purely structural internal refactoring;
- dependency vendoring or replacement with no user-visible effect;
- packaging or build-system migrations that leave installation and shipped behavior unchanged.

If multiple letters apply, select the earliest: `A` before `B` before `C`.

## Choose the digit

Choose the digit separately from the letter. Apply these tests in order and use the first matching digit.

### `1` — Incompatible or behavior-changing

Use `1` if:

- previously working caller code can fail;
- a public capability is removed or narrowed;
- the same existing call can return a different result;
- the same existing call can raise a different error.

A bug fix that changes the result or error of an existing call is digit `1`, even if the old behavior was incorrect and the new behavior is desirable.

### `2` — Compatible but observable

Use `2` when existing correct calls retain the same results and errors, but users gain or observe something, including:

- a new public capability;
- a broader accepted public type;
- newly discoverable shipped typing information;
- improved import time, execution speed, memory use, or other resource use;
- another compatible runtime change.

A cache, bounded cache, or lazy-import optimization with unchanged results and errors is digit `2`.

### `3` — Unobservable to callers

Use `3` only when the change is limited to internals, documentation, tests, CI, dependencies, packaging, builds, or development tooling and has no public-contract, installation, result, error, performance, or runtime-resource effect.

If multiple digits apply, select the lowest: `1` before `2` before `3`.

## Common classifications

Apply these rules consistently:

- New exported public operation: `A2`.
- Broadened accepted public argument type: `A2`.
- Removed or narrowed public capability: `A1`.
- Existing operation returns a different result or error without a declared-interface change: `B1`.
- Runtime speed or resource improvement with unchanged results: `B2`.
- Runtime cache addition, replacement, or bounding with unchanged results: `B2`.
- Documentation, documentation examples, or docstrings: `C3`.
- `py.typed` or equivalent metadata exposing shipped annotations: `A2`.
- Dependency or packaging change with no installation or runtime effect: `C3`.

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

- The heading starts with `##` and contains the supplied version and date exactly.
- Every pending change appears exactly once.
- Every bullet begins with one code in the form `[LN]`.
- Public-interface and public-typing changes use `A`.
- Changed results or errors from existing calls use digit `1`.
- Runtime performance and resource-use changes use `B`.
- Documentation and docstring changes use `C3`.
- Unobservable dependency, packaging, build, and internal changes use `C3`.
- `Impact: N` is the lowest digit used by any bullet.
- Bullets follow the required code order.
- Equal-code bullets retain their supplied order.
- The final line is exactly `<!-- stl-impact: v1 -->`.