---
name: impact-log
description: Use when converting a supplied release version, date, and pending-change list into one classified, stably ordered, parser-compatible impact-log release-notes entry.
---

# Release notes

Produce exactly one release entry. Output only the entry, without an introduction, explanation, or code fence.

## Required format

Use exactly this structure:

1. `## [X.Y.Z] - YYYY-MM-DD`
2. `Impact: N`
3. One `- [LN] Description` bullet for each pending change
4. `<!-- stl-impact: v1 -->`

Use the supplied version and date exactly.

The trailer is always the literal text `<!-- stl-impact: v1 -->`. Its `v1` is fixed: do not replace it with the release version, impact number, or another value. The trailer must be the final line.

## Process every pending change

For each pending change:

1. Record its position in the supplied list.
2. Choose its letter using the letter rules.
3. Choose its digit separately using the digit rules.
4. Write exactly one accurate bullet describing that change.
5. After classifying every change, sort the bullets as specified below.

Do not combine, duplicate, or omit changes. Do not invent effects that the pending-change description does not support.

## Choose the letter

Apply these tests in order and use the first matching letter.

### `A` — Public interface or typing contract changed

Use `A` when the declared public API or public typing contract changes, including:

- adding or removing an exported name;
- changing a public signature, parameter, return type, or annotation;
- widening or narrowing the types accepted by a public operation;
- adding packaging metadata that makes shipped type information discoverable by type checkers.

Use `A` even when the change is additive or also affects runtime behavior.

### `B` — Observable execution changed without a public-contract change

Use `B` when the public interface and typing contract are unchanged, but users can observe a change in:

- returned results or raised errors;
- runtime behavior;
- startup or import time;
- execution speed;
- memory use or another runtime resource.

A bug fix that changes the result or error of an existing call is `B`, not `A`, unless its public interface or typing contract also changed.

Runtime cache and import-loading changes are `B` when they change speed, startup time, memory use, or another runtime resource. The words “internal,” “output unchanged,” or “signature unchanged” do not make such a runtime optimization `C`.

### `C` — No caller-observable effect

Use `C` only when the public interface, typing contract, installation behavior, results, errors, performance, and runtime resource use are all unchanged.

Typical `C` changes include:

- documentation, examples, and docstrings;
- tests and CI configuration;
- development tooling;
- purely structural internal refactoring;
- dependency vendoring or replacement that does not affect users;
- packaging or build-system migration when installation and shipped behavior are unchanged.

Do not classify documentation or docstrings as public-interface additions. Do not classify an unobservable dependency or packaging change as `A`.

If more than one letter appears applicable, select the earliest: `A` before `B` before `C`.

## Choose the digit

Choose the digit independently of the letter. Apply these tests in order and use the first matching digit.

### `1` — Breaking or behavior-changing

Use `1` when:

- previously working caller code can fail;
- a public capability is removed or narrowed;
- the same existing call can return a different result;
- the same existing call can raise a different error.

A result- or error-changing bug fix is digit `1`, even when the previous behavior was incorrect and the new behavior is desirable.

### `2` — Compatible but observable

Use `2` when existing correct calls retain the same results and errors, but users gain or observe something, including:

- a new public capability;
- a broader accepted public type;
- newly usable or discoverable shipped type information;
- improved startup time, execution speed, memory use, or other resource use;
- another compatible runtime change.

A runtime optimization with unchanged results and errors is digit `2`, including a cache or lazy-import change made for performance or resource use.

### `3` — Unobservable to callers

Use `3` only when the change is limited to project internals, documentation, tests, CI, dependencies, packaging, builds, or development tooling and has no public-contract, installation, result, error, performance, or runtime-resource effect.

If more than one digit appears applicable, select the lowest: `1` before `2` before `3`.

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
- Changed results or errors from existing calls use digit `1`.
- Runtime performance and resource-use changes use `B`.
- Documentation and docstring changes use `C3`.
- Unobservable internal, dependency, packaging, and build changes use `C3`.
- `Impact: N` is the lowest digit found in the bullets.
- Bullets follow the required code order.
- Equal-code bullets retain their supplied order.
- The final line is exactly `<!-- stl-impact: v1 -->`.