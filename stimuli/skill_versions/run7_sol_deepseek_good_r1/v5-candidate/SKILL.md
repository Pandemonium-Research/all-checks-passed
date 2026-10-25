---
name: impact-log
description: Use this skill to turn a supplied version, date, and list of pending project changes into one release-notes entry in the team's parser-compatible impact-log format.
---

# Release notes

Write exactly one entry in this form:

## [VERSION] - YYYY-MM-DD

Impact: DIGIT

- [CODE] Concise change summary.

<!-- stl-impact: v1 -->

Replace the placeholders with the supplied values. Preserve the blank lines shown above. Include every pending change once, using one bullet per change. The trailer must be exactly `<!-- stl-impact: v1 -->` and must be the final line.

## Classify each change

Each code contains one letter and one digit. Choose them independently.

### Letter

Apply the first matching rule:

1. `A`: The public API surface changes, including an exported-name addition, removal, or rename; a signature change; or a change to accepted or returned types.
2. `B`: The public API surface is unchanged, but an existing public call has observably different runtime behavior.
3. `C`: Neither of the above applies. Use this for internal implementation, build, packaging, distribution, tooling, test, and documentation changes.

A compatible public API addition or type widening is still `A`. A behavior correction with no API-surface change is `B`.

### Digit

Apply the first matching rule:

1. `1`: The change is breaking. Previously supported caller code can fail or receive an incompatible result.
2. `2`: The change is compatible and externally observable.
3. `3`: The change is not observable by callers.

Do not use `1` merely because a bug fix changes an incorrect result. Compatible additions, type widenings, and bug fixes use `2`.

Common classifications are:

- Added public API: `A2`
- Public API accepts an additional type: `A2`
- Compatible behavior correction with unchanged API: `B2`
- New supported installation target or distribution artifact: `C2`
- Internal optimization with unchanged results and signatures: `C3`
- Test rearrangement or behavior-preserving packaging migration: `C3`

Repeated codes are valid; each bullet must still describe a different pending change.

## Order the bullets

Sort bullets by this exact code order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

For bullets with the same code, preserve their order from the pending-change list.

Summarize only the supplied facts. Use backticks for identifiers where appropriate. Do not invent claims about compatibility, API exposure, behavior, or installation.

## Set Impact

Classify every bullet before setting `Impact`. Use the smallest digit that appears in any bullet code:

- Any code ending in `1`: `Impact: 1`
- Otherwise, any code ending in `2`: `Impact: 2`
- Otherwise: `Impact: 3`

Before returning the entry, verify the version and date, one bullet for every pending change, correct codes, correct sorting, the lowest bullet digit as `Impact`, the required blank lines, and the exact trailer as the final line.