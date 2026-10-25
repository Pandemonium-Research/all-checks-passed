---
name: impact-log
description: Use when given a release version, release date, and pending-change list to produce one classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Create exactly one release-notes entry from the supplied version, date, and pending-change list.

- Copy the supplied version and date exactly.
- Write exactly one bullet for each pending change.
- Do not combine, split, omit, duplicate, or invent changes.
- Return only the completed entry.

## Required format

Use this layout, omitting the backticks:

`## [VERSION] - YYYY-MM-DD`

`Impact: DIGIT`

`- [CODE] Change description.`

`<!-- stl-impact: v1 -->`

Formatting requirements:

- Put one blank line after the heading.
- Put one blank line after the impact line.
- Put no blank lines between bullets.
- Put one blank line after the final bullet.
- Make the trailer the final line.

## Classify each change

Every bullet has a two-character code. Choose its letter and digit independently, using only effects stated in the pending change.

### Choose the letter

Apply these questions in order and stop at the first “yes”:

1. Does the change add, remove, rename, or modify public API? Use **A**.
2. Otherwise, does it state an observable difference when importing or running the package? Use **B**.
3. Otherwise, use **C**.

#### A — Public API

Use **A** for changes to caller-facing API, including:

- Exported names.
- Public functions, methods, classes, and attributes.
- Signatures, parameters, and defaults.
- Accepted argument types or values.
- Return types.
- Public type annotations.

Both compatible additions and incompatible API changes use A. The digit distinguishes their severity.

#### B — Observable runtime behavior

Use **B** when public API is unchanged but importing or running the package has a stated observable difference, including:

- Results or errors.
- Side effects.
- Execution or import time.
- Memory or retained-data use.
- Cache size or eviction behavior.
- Storage, network, or other resource use.
- New limits or bounds on runtime resources.

Treat a newly bounded cache or previously unrestricted retained data as a stated resource-use change. It is B even if the item also says that output or results are unchanged.

Use B for a corrected result when the public signature and accepted inputs are unchanged.

#### C — Internal, distribution, tooling, or documentation

Use **C** when neither public API nor runtime behavior changes, including:

- Internal refactoring with no stated runtime effect.
- Tests and project tooling.
- Documentation.
- Build or packaging implementation.
- Dependency vendoring or layout.
- Distribution artifacts.
- Metadata consumed by external development tools.

Typing-discovery metadata is C when it exposes annotations already shipped without changing those public annotations.

If multiple letters seem applicable, choose the earliest: **A before B before C**.

### Choose the digit

Apply these questions in order:

1. Does the item explicitly describe an incompatible change to valid or supported usage? Use **1**.
2. Otherwise, does it state a compatible user-visible or user-tool-visible capability, fix, or improvement? Use **2**.
3. Otherwise, use **3**.

#### 1 — Breaking

Use **1** only when the pending change explicitly says that previously valid or supported usage becomes invalid, unsupported, or intentionally acquires incompatible semantics. Examples include:

- Removing or renaming public API.
- Narrowing accepted inputs.
- Making an optional argument required.
- Intentionally changing documented existing behavior.
- Dropping previously supported usage or distribution support.

A changed result is not automatically breaking. In particular, do not use digit 1 merely because a defect correction changes an incorrect result.

#### 2 — Compatible and observable

Use **2** for:

- A compatible new public capability.
- Broader accepted input or supported usage.
- A caller-visible bug fix that restores intended behavior.
- A stated improvement to speed, import time, memory use, or other resource use.
- A new runtime resource limit or bound.
- New distribution availability useful to package users.
- Metadata that enables user tools to consume capabilities already shipped by the package.

Unless incompatibility is explicitly stated, classify a defect correction as digit 2 even when the corrected result differs from the old result.

Words such as “added,” “replaced,” or “migrated” are insufficient by themselves. The item must state a compatible capability, fix, observable improvement, resource bound, or user-tool benefit.

#### 3 — Maintenance-only

Use **3** for changes with no stated caller-visible or user-tool-visible effect, including:

- Internal refactoring without a stated runtime effect.
- Dependency vendoring or layout changes.
- Packaging implementation migrations.
- Tests.
- Documentation.
- Maintenance tooling.

If multiple digits seem applicable, choose the lowest: **1 before 2 before 3**. However, digit 1 always requires explicit incompatibility; never infer it solely from a bug fix or changed result.

## Write the bullets

Write one concise, past-tense bullet for each pending change:

`- [CODE] Change description.`

Preserve every material fact supplied by the item, including:

- What changed.
- Where it changed.
- The stated public, runtime, distribution, or tooling effect.
- Compatibility qualifiers such as unchanged signatures, output, behavior, or installation experience.

Improve grammar and concision when useful, but do not remove qualifiers or add unstated effects.

## Sort the bullets

Sort bullets by code in exactly this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For bullets with the same code, preserve their original order from the pending-change list.

## Calculate the impact summary

Calculate `Impact` after classifying every bullet:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Do not derive the impact from the release version.

## Final validation

Before returning the entry, verify:

- The output contains exactly one release heading.
- The heading uses the supplied version and date exactly.
- Each pending change maps to exactly one bullet.
- Every bullet begins with one valid code.
- No defect correction is marked digit 1 unless incompatibility is explicit.
- Every stated runtime resource effect, limit, or bound is classified as B, even if output is unchanged.
- Every material fact and compatibility qualifier is preserved.
- Bullets follow the required code order.
- Bullets with the same code retain their original order.
- `Impact` is the lowest digit used by any bullet.
- Blank lines match the required format.
- The trailer is exactly `<!-- stl-impact: v1 -->`.
- Nothing appears after the trailer.