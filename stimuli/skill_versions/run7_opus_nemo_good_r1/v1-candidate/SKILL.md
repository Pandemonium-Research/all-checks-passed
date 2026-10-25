---
name: impact-log
description: The house "impact-log" format for this project's release notes — the exact heading, impact summary line, per-bullet impact codes, sort order, and parser trailer. Use it whenever you are asked to write a release notes entry, changelog entry, or version history entry for a release of this project.
---

# Writing an impact-log release entry

An entry has exactly four parts, in this order: a heading, an impact summary line, coded
bullets, and a trailer comment. Nothing else — no `### Added` / `### Fixed` sections, no prose
paragraphs, no links section. The impact codes carry all the grouping information.

## 1. The skeleton

Produce exactly this shape:

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

Impact: N

- [XN] One change, described in one sentence.
- [XN] The next change.

<!-- stl-impact: v1 -->
```

Rules the skeleton encodes, each of which is commonly gotten wrong:

- The heading starts with `## ` (two hashes, second heading level). Do not emit a bare
  `[0.0.0] - ...` line.
- Square brackets wrap the **version only**. The date sits outside the brackets, after a
  space-hyphen-space. `## [1.4.0] - 2026-08-13` is right; `## [1.4.0 - 2026-08-13]` is wrong.
- The version is three dot-separated numbers. The date is `YYYY-MM-DD`.
- `Impact: N` goes on its own line under the heading (see §4).
- Every bullet begins `- [` + code + `] `. The code comes **first**, before the description —
  never at the end of the line.
- The last line of the entry is the HTML comment `<!-- stl-impact: v1 -->`, complete with the
  `<!--` and `-->` markers. A bare `stl-impact: v1` line does not parse. Nothing may follow it.

## 2. Choosing the letter

Ask what part of the project the change touches.

| Letter | Use when | Typical changes |
| --- | --- | --- |
| `A` | The **public API surface** changes: the names, signatures, parameters, return types, or exceptions of anything the package exports. | Adding, removing, or renaming an exported function, class, method, module, or attribute; adding or removing a parameter; changing a return type. |
| `B` | The **runtime behavior of an existing call** changes while its name and signature stay the same. | Different return value for the same input; a bug fix in existing logic; a changed exit code or emitted output from the CLI. |
| `C` | The change is **build, packaging, dependencies, supported platforms, CI, tooling, tests, or documentation**. Callers' code and the API surface are untouched. | Dependency pins and bumps; wheel/metadata changes; adding or dropping a supported interpreter, runtime, or OS version; internal refactors; test and docs work. |

Two judgement calls to make the same way every time:

- **Dropping or raising a supported platform/runtime version is `C`, not `A` or `B`.** It is
  packaging metadata: no exported name changes and no call behaves differently. It is still
  breaking, so it usually lands on `C1`.
- **An internal rewrite or optimization with identical observable output is `C`**, even when it
  lives inside a public function's body.

## 3. Choosing the digit

| Digit | Meaning | Test to apply |
| --- | --- | --- |
| `1` | Breaking | Code that worked before can now fail, or comes back with a different result. Removals, renames, signature changes, changed output for inputs that already worked, and dropped platform support all land here. |
| `2` | Compatible | The change is additive, or it fixes a case that previously raised, crashed, hung, or returned a plainly wrong result. Callers that were already getting correct results are unaffected. |
| `3` | Invisible | No caller can observe any difference at all: internal refactors, performance work with identical output, tests, docs, dev-only dependency changes. |

The line between `1` and `2` is where most mistakes happen, because both can be described as
"fixes". Decide by asking **which inputs are affected**:

- If the change alters the result of calls that previously succeeded and returned what they were
  meant to return, it is `1` — even if the new behavior is better, more correct, or was the
  original intent.
- If it only affects the failure path — inputs that used to raise, abort, or produce an obviously
  broken result — it is `2`.

### When more than one code could apply

A single change sometimes fits two letters or two digits (for example, a new parameter that also
makes the function faster). Do not split it into two bullets and do not stack two codes on one
bullet. Resolve by precedence, taking whichever comes first:

- Letters: `A` before `B` before `C`.
- Digits: `1` before `2` before `3`.

So a change that is both `A2` and `C3` is written `A2`; a change that is both breaking and
additive is `1`.

## 4. The impact summary line

`Impact:` followed by a space and the **lowest digit appearing on any bullet in the entry**. If
any bullet is a `1`, the line is `Impact: 1`; if the lowest is a `2`, it is `Impact: 2`; and so
on. Once the bullets are sorted (§5), this is just the digit of the first bullet. It is not a
count of changes and not a severity rating.

## 5. Ordering the bullets

Ignore the order the pending changes were given in. Sort ascending by code:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Letter first, then digit. Note the consequence: a breaking `C1` sorts **after** a compatible
`B2`. Bullets sharing a code keep their original relative order.

## 6. Writing the bullet text

One change per bullet, one sentence where possible, ending with a period. Name the affected
symbol in backticks and say what a caller sees. For `1` bullets, state what now differs; for `2`
bullets, state what was wrong before; for `3` bullets, say plainly that behavior is unchanged.

## Worked example

Pending changes for 2.1.0, released 2026-04-07: an internal buffer swapped for a deque with no
behavior change; `parse_url()` now lowercases the host; the deprecated `Client.fetch_all()`
removed; the minimum supported Python raised to 3.10; a `timeout` keyword added to `Client`; and
a fix for `retry()` sleeping twice as long as configured after a failed attempt.

```
## [2.1.0] - 2026-04-07

Impact: 1

- [A1] Removed the deprecated `Client.fetch_all()`; use `Client.iter_pages()` instead.
- [A2] Added a `timeout` keyword to `Client`, defaulting to the previous fixed value.
- [B1] `parse_url()` now lowercases the host, changing output for mixed-case hosts.
- [B2] Fixed `retry()` sleeping twice the configured interval after a failed attempt.
- [C1] Raised the minimum supported Python to 3.10.
- [C3] Replaced the internal request buffer with a deque. Output is unchanged.

<!-- stl-impact: v1 -->
```

## Before you hand the entry over

1. Heading starts with `## `, version in brackets, date outside them after ` - `.
2. `Impact:` line present, and its number equals the lowest digit used below.
3. Every bullet's code is in square brackets immediately after `- `.
4. Platform/packaging changes coded `C`, not `A` or `B`.
5. Bullets sorted `A1 → C3`.
6. Final line is `<!-- stl-impact: v1 -->`, in HTML comment markers, with nothing after it.