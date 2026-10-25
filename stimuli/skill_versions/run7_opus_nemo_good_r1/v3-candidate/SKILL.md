---
name: impact-log
description: The house "impact-log" format for this project's release notes — the exact heading, impact summary line, per-bullet impact codes, sort order, blank-line layout, and parser trailer. Use it whenever you are asked to write a release notes entry, changelog entry, or version history entry for a release of this project.
---

# Writing an impact-log release entry

An entry has exactly four parts, in this order: a heading, an impact summary line, coded
bullets, and a trailer comment. Nothing else — no `### Added` / `### Fixed` sections, no prose
paragraphs, no links section, no notes after the trailer. The impact codes carry all the
grouping information.

## 1. The skeleton

Produce exactly this shape, including the blank lines:

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
  space-hyphen-space. `## [1.4.0] - 2026-08-13` is right; `## [1.4.0 - 2026-08-13]` is wrong,
  and so is a heading with the version but no date.
- The version is three dot-separated numbers, exactly as given to you. The date is `YYYY-MM-DD`,
  exactly as given to you. Never substitute `Unreleased` or today's date for what you were given.
- `Impact: N` goes on its own line under the heading (see §4).
- Every bullet begins `- [` + code + `] `. The code comes **first**, before the description —
  never at the end of the line, never in parentheses, never both.
- The last line of the entry is the HTML comment `<!-- stl-impact: v1 -->`, complete with the
  `<!--` and `-->` markers. A bare `stl-impact: v1` line does not parse. Nothing may follow it.
- Layout: exactly one blank line after the heading, one after the `Impact:` line, and one before
  the trailer. No blank lines between bullets. Do not add trailing spaces to line ends.

## 2. One bullet per pending change

Every pending change you are given becomes exactly one bullet, and every bullet comes from
exactly one pending change. Do not drop a change because it seems minor, do not merge two changes
into one bullet, and do not split one change across two bullets — even when it touches several
things at once (see "When more than one code could apply" in §3).

## 3. Choosing the code

### The letter

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

### The digit

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

### A few more calls, made the same way every time

- A new optional parameter or keyword that defaults to the old behavior is `A2`.
- Changing the **default value** of an existing parameter is `B1`: existing calls get a different
  result.
- Deprecating something without removing it is not breaking; if the name still works, it is `2`.
- A change confined to private or internal names nothing exports is `C`, not `A`.

### Quick reference for common phrasings

| The pending change reads like… | Code |
| --- | --- |
| Added a new exported function, class, module, or attribute | `A2` |
| Added an optional parameter or flag that defaults to the old behavior | `A2` |
| Removed or renamed an exported name, or removed a deprecated module | `A1` |
| Changed a return type, removed a parameter, or changed the exception type raised | `A1` |
| Same call, same signature, different result for inputs that already worked | `B1` |
| Changed the default value of an existing parameter | `B1` |
| Fixed a crash, hang, wrong exit code, or plainly wrong answer on inputs that used to fail | `B2` |
| Dropped, raised, or removed a supported interpreter, runtime, or OS version | `C1` |
| Added support for a new interpreter, runtime, or OS version | `C2` |
| Raised a runtime dependency's minimum such that existing installs can break | `C1` |
| Bumped, relaxed, or added a runtime dependency without breaking existing installs | `C2` |
| Pinned or bumped a dev-, test-, or lint-only dependency | `C3` |
| Internal refactor, rewrite, or speed-up with identical output | `C3` |
| Tests, CI configuration, or documentation only | `C3` |

### When more than one code could apply

A single change sometimes fits two letters or two digits (for example, a new parameter that also
makes the function faster, or a rename that also changes the return type). Do not split it into
two bullets and do not stack two codes on one bullet. Resolve by precedence, taking whichever
comes first:

- Letters: `A` before `B` before `C`.
- Digits: `1` before `2` before `3`.

So a change that is both `A2` and `C3` is written `A2`; a change that is both breaking and
additive is `1`.

## 4. The impact summary line

`Impact:` followed by a space and the **lowest digit appearing on any bullet in the entry**. If
any bullet is a `1`, the line is `Impact: 1`; if the lowest is a `2`, it is `Impact: 2`; if every
bullet is a `3`, it is `Impact: 3`. Once the bullets are sorted (§5), this is just the digit of
the first bullet. It is not a count of changes and not a severity rating, and it is never fixed
at `1` by default.

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
removed; the minimum supported Python raised to 3.10; a `timeout` keyword added to `Client` that
also speeds up connection setup; and a fix for `retry()` sleeping twice as long as configured
after a failed attempt.

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

The `timeout` bullet shows precedence at work: it is both an API addition and a speed-up, so it
takes `A` over `C` and stays a single bullet.

## Second worked example: no breaking changes

Pending changes for 2.1.1, released 2026-05-02: a `Response.headers` property added; a fix for
the CLI printing a traceback instead of an error message on a malformed config; and the docs
build moved to a newer theme.

```
## [2.1.1] - 2026-05-02

Impact: 2

- [A2] Added a `Response.headers` property exposing the parsed response headers.
- [B2] Fixed the CLI printing a traceback instead of an error message for a malformed config.
- [C3] Moved the documentation build to a newer theme. Behavior is unchanged.

<!-- stl-impact: v1 -->
```

Nothing here is breaking, so the summary line is `Impact: 2` — the lowest digit present, not `1`.

## Before you hand the entry over

1. Heading starts with `## `, version in brackets, date outside them after ` - `, both exactly as
   you were given them.
2. `Impact:` line present, and its number equals the lowest digit used below.
3. Every bullet's code is in square brackets immediately after `- `, and nowhere else on the line.
4. Bullet count equals the number of pending changes — none dropped, merged, or split.
5. Platform/packaging changes coded `C`, not `A` or `B`.
6. Bullets sorted `A1 → C3`.
7. Blank lines exactly as in the skeleton: after the heading, after `Impact:`, before the trailer.
8. Final line is `<!-- stl-impact: v1 -->`, in HTML comment markers, with nothing after it.