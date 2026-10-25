---
name: impact-log
description: The house "impact-log" format for this project's release notes — the exact heading, impact summary line, per-bullet impact codes (letter + digit), sort order, blank-line layout, and parser trailer. Use it whenever you are asked to write a release notes entry, changelog entry, or version history entry for a release of this project.
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
| `A` | The **public API surface** changes: the names, signatures, parameters, return types, or exceptions of anything the package exports. | Adding, removing, or renaming an exported function, class, method, module, or attribute; adding or removing a parameter; widening or changing an accepted argument type; changing a return type. |
| `B` | The **runtime behavior of an existing call** changes while its name and signature stay the same. | Different return value for the same input; a bug fix in existing logic; a changed exit code or emitted output from the CLI. |
| `C` | The change is **build, packaging, dependencies, supported platforms, shipped metadata, CI, tooling, tests, or documentation**. Callers' code and the API surface are untouched. | Dependency pins, bumps, removals, and vendoring; build-backend and wheel/metadata changes; adding or dropping a supported interpreter, runtime, or OS version; internal refactors; test and docs work. |

Three judgement calls to make the same way every time:

- **Dropping or raising a supported platform/runtime version is `C`, not `A` or `B`.** It is
  packaging metadata: no exported name changes and no call behaves differently. It is still
  breaking, so it usually lands on `C1`.
- **An internal rewrite or optimization with identical observable output is `C`**, even when it
  lives inside a public function's body.
- **Starting to ship a new file or metadata alongside the package is `C`, not `A`** — nothing new
  is exported and nothing importable changed. If outside tooling can pick the artifact up, the
  digit is `2`.

### The digit

| Digit | Meaning | Test to apply |
| --- | --- | --- |
| `1` | Breaking | Code that was already getting the intended result can now fail or come back different. Removals, renames, signature changes, redefinitions of correct behavior, and dropped platform support all land here. |
| `2` | Compatible | The change is additive, or it repairs a defect — inputs that used to raise, crash, hang, or come back with a wrong answer. Callers that were already getting correct results are unaffected. |
| `3` | Invisible | No user can observe any difference at all: internal refactors, performance work with identical output, tests, docs, dev-only dependency changes. |

#### The `1` vs `2` line — where most mistakes happen

Both a redefinition and a bug fix can be described as "changing what a call returns", so the
wording of the pending change will not settle it. Ask one question:

> **Was the old result a bug?**

- **Yes — the old output was wrong, corrupted, truncated, mangled, mis-parsed, crashing, or
  hanging.** The fix is `2`. This holds *even when the old call returned normally with no error*.
  "Worked before" means **returned the answer the function was meant to return**, not merely "did
  not raise". A function that quietly handed back a wrong value was not working, so correcting it
  breaks nothing.
- **No — the old output was legitimate and you are changing the rule.** A new normalization,
  a new rounding or sorting policy, a changed default, a stricter validation: the code is `1`,
  even if the new behavior is better, more correct, or was the original intent.
- **Both — the change repairs broken inputs and also shifts results that were already correct.**
  Precedence gives `1` (see below).

Phrases like "fixed", "now handles … correctly", "no longer drops/mangles/misparses", and "was
returning the wrong X" are defect repairs: `2`. Phrases like "now lowercases", "now sorts by",
"now defaults to", and "now rejects" are redefinitions: `1`.

A repair stays a `2` however it is worded. "Now handles X correctly" describes broken inputs being
made to work, not a new rule, so do not let the word "now" — or the fact that some output changed
— pull it to `1`.

#### The digit on a `C` change

Apply the same three digits by asking what a **user** — installing, importing, or running their
tooling against the package — can observe:

- `C1` — existing installs or supported setups can break: dropped platform/runtime support, a
  raised minimum on a runtime dependency, a removed extra.
- `C2` — users can observe the difference but nothing breaks: dependency sets added, relaxed,
  removed, or vendored; a newly supported interpreter or OS; new wheels or platform tags; newly
  shipped files or metadata that user tooling reads.
- `C3` — nothing outside the repo can tell: build-backend or config-format migrations that
  produce an equivalent install, internal refactors and speed-ups, dev/test/lint dependency
  pins, CI configuration, tests, docs.

A packaging change described as leaving installation unchanged for users is `C3`, not `C2`.

### A few more calls, made the same way every time

- A new optional parameter or keyword that defaults to the old behavior is `A2`.
- Accepting an additional input type while all existing calls behave identically is `A2`.
- Changing the **default value** of an existing parameter is `B1`: existing calls get a different
  result.
- Deprecating something without removing it is not breaking; if the name still works, it is `2`.
- A change confined to private or internal names nothing exports is `C`, not `A`.

### Quick reference for common phrasings

| The pending change reads like… | Code |
| --- | --- |
| Added a new exported function, class, module, or attribute | `A2` |
| Added an optional parameter or flag that defaults to the old behavior | `A2` |
| Widened an existing parameter to accept another type, existing calls unaffected | `A2` |
| Removed or renamed an exported name, or removed a deprecated module | `A1` |
| Changed a return type, removed a parameter, or changed the exception type raised | `A1` |
| Same call, same signature, different result on inputs that were already returning the intended answer (a new rule, not a repair) | `B1` |
| Changed the default value of an existing parameter | `B1` |
| Fixed a crash, hang, or wrong exit code | `B2` |
| Fixed a call that returned normally but gave a wrong, mangled, or incomplete answer for some inputs | `B2` |
| Dropped, raised, or removed a supported interpreter, runtime, or OS version | `C1` |
| Raised a runtime dependency's minimum such that existing installs can break | `C1` |
| Added support for a new interpreter, runtime, or OS version | `C2` |
| Bumped, relaxed, added, removed, or vendored a runtime dependency without breaking installs | `C2` |
| Started shipping a new file or metadata that user tooling reads | `C2` |
| Pinned or bumped a dev-, test-, or lint-only dependency | `C3` |
| Migrated build configuration or backend with the install unchanged for users | `C3` |
| Internal refactor, rewrite, cache change, or speed-up with identical output | `C3` |
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
at `1` by default. Read it off the bullets last, after every code is settled.

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
takes `A` over `C` and stays a single bullet. Note the two `B` bullets: lowercasing the host is a
new rule applied to hosts that were previously returned as intended, so `B1`; the double sleep
was a defect, so `B2`.

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

## Third worked example: silent wrong answers, and `C2` vs `C3`

Pending changes for 3.2.0, released 2026-07-15: `read_config()` silently discarded any key whose
value contained an `=` sign and now keeps it; `format_size()` switched from banker's rounding to
round-half-up; the build moved off `setup.py` onto a declarative config with an identical
resulting install; and wheels are now published for a new CPU architecture.

```
## [3.2.0] - 2026-07-15

Impact: 1

- [B1] `format_size()` now rounds halves up instead of to even, changing existing rounded output.
- [B2] Fixed `read_config()` silently discarding keys whose values contain an `=` sign.
- [C2] Published wheels for an additional CPU architecture.
- [C3] Moved the build off `setup.py` to declarative configuration. Installation is unchanged.

<!-- stl-impact: v1 -->
```

`read_config()` raised no error before — it just handed back a config missing entries, which is a
wrong answer, so the repair is `2`. `format_size()` was doing exactly what it was designed to do;
redefining the rule changes results callers were relying on, so it is `1`. The build move is
invisible to users (`C3`) while the new wheels are something users can see (`C2`).

## Before you hand the entry over

1. Heading starts with `## `, version in brackets, date outside them after ` - `, both exactly as
   you were given them.
2. Every bullet's code is in square brackets immediately after `- `, and nowhere else on the line.
3. Bullet count equals the number of pending changes — none dropped, merged, or split.
4. Every bullet that repairs a defect — including one that returned normally with a wrong answer —
   is a `2`, not a `1`. Only redefinitions of already-correct behavior are `1`.
5. Platform/packaging changes coded `C`, with the digit set by what users can observe: breaking
   installs `C1`, visible but safe `C2` (including newly shipped artifacts other tools read),
   invisible `C3` (including migrations that leave the install unchanged).
6. Bullets sorted `A1 → C3`.
7. `Impact:` line present, and its number equals the lowest digit used below — recomputed after
   any code you changed while checking items 4 and 5.
8. Blank lines exactly as in the skeleton: after the heading, after `Impact:`, before the trailer.
9. Final line is `<!-- stl-impact: v1 -->`, in HTML comment markers, with nothing after it.