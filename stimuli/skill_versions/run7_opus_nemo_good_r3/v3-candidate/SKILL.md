---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project — given a version, a date, and a list of pending changes — to produce an entry in the team's house impact-log format: a `## [version] - date` heading, an `Impact:` line, one correctly coded and sorted bullet per change, and the `<!-- stl-impact: v1 -->` trailer that downstream tooling parses.
---

# Release notes (impact-log format)

Every release gets one entry. An entry is always these four parts, in this order:

1. a heading line
2. an `Impact:` line
3. one bullet per change, sorted by code
4. an HTML-comment trailer

## How to work

Do it in this order. Most bad entries come from writing the bullets straight out in the order the
changes arrived and coding them by feel.

1. For each change, decide the **letter** — what part of the project changed.
2. Then, separately, decide the **digit** — what it does to a caller.
3. Sort the bullets by the finished codes.
4. Compute the `Impact:` line from the finished codes.
5. Write the heading, the `Impact:` line, the sorted bullets, and the trailer.

Keep one bullet per change you were given: don't merge two changes into one bullet or split one
into two, and describe each change in the terms you were given.

## Exact shape

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

Impact: <digit>

- [XN] First change.
- [XN] Second change.

<!-- stl-impact: v1 -->
```

Rules for the fixed parts — a parser checks these, so match them literally:

- The heading is a **level-two Markdown heading**. It starts with `## `. Writing `[1.2.0] - 2026-01-31` with no `##` makes the entry invalid.
- The version goes in square brackets, three numeric parts, no leading `v`. Then a space, a hyphen, a space, then the date as `YYYY-MM-DD`. Use the version and date you were given; do not substitute today's date.
- The summary line is the word `Impact`, a colon, a space, and one digit. No period, no extra words.
- Each bullet is `- `, then the code in square brackets, then a space, then the change described in one line.
- The trailer is an **HTML comment**: `<!-- stl-impact: v1 -->`. It is **mandatory on every entry**, however short the entry is. It sits after a blank line following the last bullet and must be the last line, with nothing after it. Two ways to lose it: finishing the bullets and forgetting it, and writing the bare text `stl-impact: v1` without the `<!--` and `-->` wrappers. Both make the entry invalid.

The `## ` prefix on the first line and the trailer on the last line are the two parts dropped most
often. Before you submit, look at the first line and the last line specifically.

## Assigning the code

Every bullet gets a two-character code: a letter, then a digit. The two axes are **independent**.
Work them separately and in order; the answer on one never constrains the other.

### Step 1 — the letter: what changed

Ask these three questions in order. The first `yes` wins; stop there.

| Letter | Ask | Test |
| --- | --- | --- |
| `A` | Did the **exported surface itself** change — a public name added, removed or renamed; a signature or parameter list changed; a return type changed; an exported module, class, CLI command or CLI flag changed; the type information shipped for any of these changed? | You could see the difference by reading the API reference or the type stubs, without running anything. |
| `B` | Otherwise: did **shipped code that runs in the caller's process** change — its output, its errors, its exit status, its speed, its memory use? | Same call, same signature, different runtime. |
| `C` | Otherwise: build config, packaging metadata, dependency declarations, CI, tests, repo layout, documentation, docstrings, examples. | The library code a caller imports is untouched. |

Because you ask them in order, exactly one letter applies. There is no "it's really both."

Letter calls that are decided more often than you'd guess:

- **A new optional parameter or flag is `A`.** Gaining, losing or reordering a parameter is a
  signature change, even when the default preserves the old behavior. That it is harmless is a fact
  about the digit, not the letter.
- **A behavior change behind an identical signature is `B`**, however visible or breaking it is. If
  the name, the parameters and the return type all read the same in the API reference, the surface
  did not change. Renaming or removing a function is `A`; changing what an unchanged function
  computes, returns, raises or prints is `B`.
- **Shipping or withdrawing type information is `A`**, even when the mechanism is a packaging file
  or a bulk edit (a marker file, published stubs, annotations added across existing functions).
  Types are part of the exported surface, so this is `A` and not `C`.
- **Rewriting internal library code is `B`, not `C`** — an optimized loop, a swapped-out cache, a
  deferred import, a leak fix. `C` is for files that never run in the caller's process. "It's just
  an internal detail" is a statement about the digit, not the letter.
- **For a CLI**, the commands and flags are exported surface (`A`); what it prints and what it exits
  with is runtime (`B`).
- **Dependency declarations are `C`**, including pins, floors and extras — that is packaging
  metadata, not code that runs in the caller's process.
- If one bullet names two effects ("gained a flag *and* got faster"), the letter follows the
  strongest thing it touched: a surface change makes it `A` even when the rest is runtime.

### Step 2 — the digit: what it does to a caller

| Digit | Use when |
| --- | --- |
| `1` | Breaking. Code that was correct before this release can now fail, or can now come back with a different value or different output. |
| `2` | Compatible. Purely additive, or a repair confined to inputs and paths that were already crashing or already producing wrong results. Code that was correct before behaves exactly as it did. |
| `3` | Invisible. No caller can observe the difference except as speed or memory. |

Read the change description and let it decide:

- The `1`/`2` line is **scope, not sentiment**: ask which inputs behave differently now. Any input
  that was already producing the right answer → `1`. Only inputs that were already failing, hanging
  or coming back wrong → `2`. A change is still `1` when it is an improvement, a correction, or long
  overdue; "it's a fix" does not make it `2`.
- Altering the result, output, return shape or exception for input that already worked — collapsing
  something, normalizing something, returning a generator instead of a list: `1`.
- Removing or renaming an export, tightening a signature, dropping a supported runtime or platform,
  raising a dependency floor: `1`.
- Adding something optional — a new function, module, parameter, flag or extra: `2`. Nothing that
  used to work changed.
- Repairing one specific broken case — a call that used to raise, or a particular input that came
  back mangled — so that only that case changes: `2`.
- If the description says the output, results or behavior are **unchanged / identical / equivalent**,
  or the only effect is that something is faster or uses less memory: `3`, never `2`. `2` means a
  caller can see something new; `3` means they cannot see anything.
- Packaging and CI work is not automatically `3`. Ask the same question you'd ask of code: can a
  caller observe it? Newly published artifacts, a newly supported platform or interpreter, a new
  optional extra are `2`; withdrawing any of those is `1`. Test runners, CI providers, repo layout,
  lint config, internal docs and development-only dependency pins are `3`.

### The nine codes

Every letter pairs with every digit. Use this as a check on the pair you just built — none of these
cells is exotic.

| Code | Shape of change |
| --- | --- |
| `A1` | A public name removed or renamed; a parameter removed or made required; a declared return type changed. |
| `A2` | A new public function, class, module, parameter, flag or command, with old calls unaffected. |
| `A3` | Type information shipped or reshaped where the description says runtime behavior is unchanged. |
| `B1` | An unchanged call now returns, prints or raises something different for input that already worked. |
| `B2` | A path that already raised, hung or returned a wrong value now behaves correctly; nothing else moves. |
| `B3` | Internal library rewrite, cache, lazy import, leak fix or speedup — results identical. |
| `C1` | A published artifact, platform, interpreter or extra withdrawn; a runtime dependency floor raised. |
| `C2` | New wheels, a newly supported interpreter or platform, a new optional extra — caller-visible packaging. |
| `C3` | Tests, CI, repo layout, lint, docs, development-only dependencies — invisible to any caller. |

### Don't let one axis pull the other

The two most common mis-codes both come from collapsing the axes:

- `A1` is not the code for "a serious break." A breaking runtime change behind an unchanged
  signature is `B1`. A breaking packaging change is `C1`.
- `B2` is not the code for "a harmless addition." A new optional parameter or a new exported name is
  `A2`; a new wheel or extra is `C2`.

### When two digits both genuinely fit

Only if a single bullet truly does two things at once — say it both removes one name and adds
another — take the lower digit: `1` before `2` before `3`. This tiebreak is for real overlap inside
one bullet. If the change fits exactly one definition, apply that definition; do not fall back to
precedence to avoid choosing. The letter axis needs no tiebreak: the ordered questions in Step 1
already settle it.

## The `Impact:` line

It is the **lowest digit that appears on any bullet in the entry** — `1` if any bullet is breaking,
otherwise `2` if any bullet is compatible, otherwise `3`. Compute it after every code is final, and
recompute it if you revise one.

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
- [C3] Moved the test suite to a new runner and pinned the linter in the dev extra.

<!-- stl-impact: v1 -->
```

Note the pairs that are easy to confuse: `A1` changes a signature, `B1` changes a result behind an
unchanged signature; `A2` adds to the surface, `B2` repairs a path that was already broken; `A3`
ships types with runtime untouched, `B3` leaves every result identical; `B3` is internal library
code, `C3` is work that never ships to a caller, and `C2` is packaging a caller can still notice.

## Before you submit

- [ ] First line starts with `## `, version in brackets, ` - `, date as `YYYY-MM-DD`, taken from the input.
- [ ] Every bullet has a letter-and-digit code in square brackets.
- [ ] Letter chosen by the ordered test: surface changed → `A`; else shipped code changed → `B`; else `C`.
- [ ] Every parameter, flag or type change is `A`, even the harmless ones; every behavior-only change is `B`, even the breaking ones; every dependency, CI, test or layout change is `C`.
- [ ] Every bullet describing a changed result for previously-working input is a `1`; every bullet repairing only an already-broken path is a `2`.
- [ ] Every bullet saying output is unchanged, or citing only speed or memory, is a `3`.
- [ ] Packaging bullets a caller can observe are `2` or `1`, not `3`.
- [ ] `Impact:` equals the lowest digit present.
- [ ] Bullets sorted ascending by code, sorted after the codes were final.
- [ ] Last line is exactly `<!-- stl-impact: v1 -->`, comment markers included, blank line before it, nothing after it.