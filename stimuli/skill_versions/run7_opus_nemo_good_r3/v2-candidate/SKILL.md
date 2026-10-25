---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project — given a version, a date, and a list of pending changes — to produce an entry in the team's house impact-log format, with the correct two-character code on every bullet, that downstream tooling can parse.
---

# Release notes (impact-log format)

Every release gets one entry. An entry is always these four parts, in this order:

1. a heading line
2. an `Impact:` line
3. one bullet per change, sorted
4. an HTML-comment trailer

## Exact shape

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

Impact: <digit>

- [XN] First change.
- [XN] Second change.

<!-- stl-impact: v1 -->
```

Rules for the fixed parts — these are checked by a parser, so match them literally:

- The heading is a **level-two Markdown heading**. It starts with `## `. Writing `[1.2.0] - 2026-01-31` with no `##` makes the entry invalid.
- The version goes in square brackets, three numeric parts, no leading `v`. Then a space, a hyphen, a space, then the date as `YYYY-MM-DD`. Use the version and date you were given; do not substitute today's date.
- The summary line is the word `Impact`, a colon, a space, and one digit. No period, no extra words.
- Each bullet is `- `, then the code in square brackets, then a space, then the change described in one line.
- The trailer is an **HTML comment**: `<!-- stl-impact: v1 -->`. It is mandatory on every entry, no matter how short. Two ways to lose it: forgetting it entirely once the bullets are written, and writing the bare text `stl-impact: v1` without the `<!--` and `-->` wrappers. Both are invalid. It goes after a blank line following the last bullet, and it must be the last line, with nothing after it.

The heading prefix and the trailer are the two parts that get dropped most often. Before you submit, look at the first line and the last line specifically.

## Assigning the code

Every bullet gets a two-character code: a letter, then a digit. Work the two axes **separately and in
order** — first "what part of the project did this touch," then "what does it do to a caller." The
answer on one axis never constrains the other.

### Step 1 — the letter: what changed

Ask these three questions in order. The first `yes` wins; stop there.

| Letter | Ask | Test |
| --- | --- | --- |
| `A` | Did the **exported surface itself** change — a public name added, removed or renamed; a signature or parameter list changed; a return type changed; an exported module, class, CLI command or CLI flag changed; the type information shipped for any of these changed? | You could see the difference by reading the API reference or the type stubs, without running anything. |
| `B` | Otherwise: did **shipped code that runs in the caller's process** change — its output, its errors, its speed, its memory use? | Same call, same signature, different runtime. |
| `C` | Otherwise: build config, packaging metadata, dependency declarations, CI, tests, documentation, docstrings, examples. | The library code a caller imports is untouched. |

Because you ask them in order, exactly one letter applies. There is no "it's really both."

Cases that are decided more often than you'd guess:

- **A new optional parameter is `A`.** Gaining, losing or reordering a parameter is a signature
  change, even when the default preserves the old behavior. That it is harmless is a fact about the
  digit, not the letter.
- **A behavior change behind an identical signature is `B`**, however visible or breaking it is. If
  the name, the parameters and the return type all read the same in the API reference, the surface
  did not change. Renaming or removing a function is `A`; changing what an unchanged function
  computes, returns, raises or prints is `B`.
- **Shipping or withdrawing type information is `A`**, even when the mechanism is a packaging file
  (a marker file, published stubs, added or removed annotations). Types are part of the exported
  surface.
- **Rewriting internal library code is `B`, not `C`** — an optimized loop, a swapped-out cache, a
  deferred import, a leak fix. `C` is for files that don't run in the caller's process. "It's just
  an internal detail" is a statement about the digit, not the letter.
- **For a CLI**, the commands and flags are exported surface (`A`); what it prints, and what it
  exits with, is runtime (`B`).

### Step 2 — the digit: what it does to a caller

| Digit | Use when |
| --- | --- |
| `1` | Breaking. Code that was correct before this release can now fail, or can now come back with a different value or different output. |
| `2` | Compatible. Purely additive, or a repair confined to inputs and paths that were already crashing or already producing wrong results. Code that was correct before behaves exactly as it did. |
| `3` | Invisible. No caller can observe the difference except as speed or memory. |

Read the change description and let it decide:

- If it says the change **alters the result, output or return value for input that already worked** —
  collapses something, normalizes something, returns a different shape — that is `1`. It is still `1`
  when the change is an improvement or long overdue. What makes something `2` is "correct code keeps
  working," not the word "fix."
- Removing or renaming an export, tightening a signature, dropping a supported runtime or platform,
  raising a dependency floor: `1`.
- Adding something optional: `2`. Repairing a specific broken case — a call that used to raise, or a
  particular input that came back mangled or wrong — so that only that case changes: also `2`. The
  distinction against `1` is scope: a `2` fix moves inputs that were already wrong; a `1` change
  moves inputs that were already right.
- If the description says the output, results or behavior are **unchanged / identical / equivalent**,
  or the only effect is that something is faster or uses less memory: `3`, never `2`.
- Packaging and CI work is not automatically `3`. Ask the same question you'd ask of code: can a
  caller observe it? Newly published artifacts, a newly supported platform or interpreter, a new
  optional extra are `C2`; withdrawing any of those is `C1`. Test runners, CI providers, internal
  docs and lint config are `C3`.

### Don't let one axis pull the other

The two most common mis-codes both come from collapsing the axes:

- `A1` is not the code for "a serious break." A breaking runtime change behind an unchanged
  signature is `B1`. A breaking packaging change is `C1`.
- `B2` is not the code for "a harmless addition." A new optional parameter or a new exported name is
  `A2`; a new wheel or extra is `C2`.

Every letter pairs with every digit. `A3` (types or annotations shipped, runtime identical) and `C1`
(support withdrawn) are ordinary codes, not exotic ones.

### When two digits both genuinely fit

Only if a single bullet truly does two things at once — say it both removes one name and adds
another — take the lower digit: `1` before `2` before `3`. This tiebreak is for real overlap within
one bullet. If the change fits exactly one definition, apply that definition; do not fall back to
precedence to avoid choosing. The letter axis needs no tiebreak: the ordered questions in Step 1
already settle it.

## The `Impact:` line

It is the **lowest digit that appears on any bullet in the entry** — `1` if any bullet is breaking,
otherwise `2` if any bullet is compatible, otherwise `3`. Compute it after you have finalized every
code, and recompute it if you revise one.

## Bullet order

Sort bullets by their code, ascending — all `A` before all `B` before all `C`, and within a letter
`1` before `2` before `3`. So: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Bullets sharing
a code keep the relative order they were given in. Sort last, after every code is final — never emit
them in the order the changes happened to arrive.

## Worked example

For version `2.3.0` released on `2025-11-04`:

```
## [2.3.0] - 2025-11-04

Impact: 1

- [A1] `open_store()` no longer accepts the `retries` argument.
- [A2] `Store` gained an optional `timeout` parameter; omitting it keeps the previous behavior.
- [A3] Shipped a `py.typed` marker so the existing annotations reach type checkers.
- [B1] `resolve()` now returns absolute paths, changing the result for relative inputs.
- [B2] Fixed `count()` raising instead of returning `0` for an empty store.
- [B3] Replaced the internal index with a hash map. Results are unchanged.
- [C2] Added an optional `cli` extra that installs the command-line dependencies.
- [C3] Moved the test suite to a new runner.

<!-- stl-impact: v1 -->
```

Note the pairs that are easy to confuse: `A1` changes a signature, `B1` changes a result behind an
unchanged signature; `A2` adds to the surface, `B2` repairs a path that was already broken; `B3`
leaves every result identical; `B3` is internal library code, `C3` is code that never ships to a
caller, and `C2` is a packaging change a caller can still notice.

## Before you submit

- [ ] First line starts with `## `, version in brackets, ` - `, date as `YYYY-MM-DD`.
- [ ] Every bullet has a letter-and-digit code in square brackets.
- [ ] Letter chosen by the ordered test: surface changed → `A`; else shipped code changed → `B`; else `C`.
- [ ] Every behavior-only change sits under `B`, even the breaking ones; every parameter or type change sits under `A`, even the harmless ones.
- [ ] Every bullet describing a changed result for previously-working input is a `1`.
- [ ] Every bullet saying output is unchanged, or that only cites speed or memory, is a `3`.
- [ ] Packaging bullets a caller can observe are `2` or `1`, not `3`.
- [ ] `Impact:` equals the lowest digit present.
- [ ] Bullets sorted ascending by code, sorted after the codes were final.
- [ ] Last line is exactly `<!-- stl-impact: v1 -->`, comment markers included, nothing after it.