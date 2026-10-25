---
name: impact-log
description: Use when given a release version, release date, and pending-change list and you need one classified, sorted, parser-compatible release-notes entry.
---

# Release notes

Create exactly one release-notes entry from the supplied version, date, and pending-change list.

Use each supplied value exactly as given:

- Do not change the version or date.
- Create exactly one bullet for each pending-change item.
- Do not combine, split, omit, duplicate, or invent changes.

## Required output format

Return only the completed entry in this layout:

`## [VERSION] - YYYY-MM-DD`

`Impact: DIGIT`

`- [CODE] Change description.`

`<!-- stl-impact: v1 -->`

Omit the backticks. The completed entry must contain:

- One blank line after the heading.
- One blank line after the impact line.
- No blank lines between bullets.
- One blank line between the final bullet and the trailer.
- Nothing after the trailer.

Use the supplied version exactly, including all three numeric parts.

## Classify each pending change

Assign one code to every change. The code consists of a letter and a digit, such as `B2`.

Choose the letter and digit separately. Classify only effects stated by the pending change; do not invent consequences.

### Choose the letter

Ask these questions in order and stop at the first “yes”:

1. Does the change modify the public API contract? Use **A**.
2. Otherwise, does it modify observable runtime behavior? Use **B**.
3. Otherwise, use **C**.

#### A — Public API

Use **A** for changes to anything callers use as public API, including:

- Exported names.
- Public functions, methods, classes, or attributes.
- Signatures, parameters, or defaults.
- Accepted argument types or values.
- Return types.
- Public type annotations.

Compatible additions and incompatible changes can both use A; the digit records their severity.

#### B — Observable runtime behavior

Use **B** when the public API remains unchanged but importing or running the package has a stated observable difference, including:

- Results or errors.
- Side effects.
- Execution or import time.
- Memory, cache, storage, network, or other resource use.
- Explicit resource limits or bounds.

A mechanism can state a runtime effect without using words such as “performance improvement.” For example, introducing a finite bound for previously unrestricted retained data states a memory-resource effect and is B.

A statement that output or results are unchanged rules out a result change only. It does not cancel a separately stated timing, memory, or resource-use effect.

#### C — Internal, distribution, tooling, or documentation

Use **C** when neither the public API nor runtime behavior changes, including:

- Internal refactoring with no stated runtime effect.
- Tests and project tooling.
- Documentation.
- Build and packaging implementation.
- Dependency layout or vendoring.
- Distribution artifacts and platform-specific packages.
- Metadata used by external developer tools.

Use C for typing-discovery metadata when public annotations themselves do not change.

If several letters appear applicable, use the earliest: **A before B before C**.

### Choose the digit

Apply this decision in order:

1. Use **1** only for an explicitly incompatible change.
2. Otherwise, use **2** for a compatible user-visible or user-tool-visible capability, fix, or improvement.
3. Otherwise, use **3** for maintenance-only work.

#### 1 — Breaking

Use **1** when the pending change states that previously valid or supported usage becomes invalid, fails, or intentionally acquires incompatible semantics. Examples include:

- Removing or renaming public API.
- Narrowing accepted inputs.
- Making a previously optional argument required.
- Intentionally changing documented existing behavior.
- Dropping previously supported usage or distribution support.

Do not choose 1 merely because a bug fix changes an incorrect result. A fix that restores intended behavior is digit 2 unless the pending change explicitly identifies an incompatible contract change.

#### 2 — Compatible and observable

Use **2** for:

- A compatible new public capability.
- Broader accepted input or supported usage.
- A caller-visible bug fix that preserves correct existing usage.
- A stated speed, import-time, memory, or resource-use improvement.
- A newly stated resource bound.
- New distribution availability useful to package users.
- Metadata that enables user tools to consume capabilities already shipped by the package.

Words such as “added,” “replaced,” or “migrated” are not sufficient by themselves. There must be a stated compatible benefit, fix, observable improvement, or user-tool capability.

#### 3 — Maintenance-only

Use **3** when the change has no stated caller-visible or user-tool-visible effect, including:

- Internal refactoring without a stated runtime effect.
- Dependency vendoring or layout changes.
- Packaging implementation migrations.
- Tests.
- Documentation.
- Maintenance tooling.

If several digits appear applicable, use the lowest: **1 before 2 before 3**. However, digit 1 requires an explicitly incompatible change; do not infer incompatibility solely from a corrected result.

## Write the bullets

Write one concise, past-tense bullet for each pending-change item:

`- [CODE] Change description.`

Preserve every material fact supplied by the item, including:

- What changed.
- Where it changed.
- The stated user, runtime, packaging, or tooling effect.
- Compatibility qualifiers such as unchanged signatures, output, behavior, or installation experience.

You may improve grammar and concision, but do not remove qualifiers or add unstated effects.

## Sort the bullets

Sort bullets by code in exactly this order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple bullets have the same code, keep their original order from the pending-change list.

## Calculate the impact summary

Calculate the impact only after every bullet has been classified:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Do not derive the impact from the release version.

## Final validation

Before returning the entry, verify:

- The output contains exactly one release heading.
- The heading is exactly `## [VERSION] - YYYY-MM-DD` using the supplied values.
- Each pending-change item maps to exactly one bullet.
- Every bullet begins with one valid code.
- Each code follows the stated letter and digit decisions.
- A corrected defect was not marked breaking unless incompatibility was explicit.
- Every stated runtime resource effect was classified as B, even if output stayed unchanged.
- Every material fact and compatibility qualifier was preserved.
- Bullets follow the required code order.
- Bullets with the same code retain their original order.
- `Impact` equals the lowest digit used by any bullet.
- Blank lines match the required output format.
- The trailer is exactly `<!-- stl-impact: v1 -->`.
- The trailer is the final line.