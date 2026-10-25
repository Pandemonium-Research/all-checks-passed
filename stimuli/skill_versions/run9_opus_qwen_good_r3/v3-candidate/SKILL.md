---
name: impact-log
description: Use this skill when writing a release notes entry, changelog entry, or version history entry for this project. It gives the house impact-log format — how to code each bullet with a letter and a digit, the required ascending bullet order, the Impact summary line, the heading, and the parser trailer — so entries are consistent and downstream tooling can read them.
---

# Release notes: the impact-log format

Each release gets one entry, appended to the release notes file in the house impact-log format.
Work through the steps below in order.

Two mistakes account for almost every rejected entry:

- **Leaving the bullets in the order the changes were handed to you.** They are almost never
  already in the right order. Step 5 sorts them mechanically — do not skip it and do not eyeball
  it.
- **Picking the letter from what the change is *about* instead of from what surface it
  touches.** A packaging or dependency change is `C` even when it involves shipping code. Step 2
  is a cascade; follow it literally.

## The shape of a finished entry

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: N

- [LD] Lowest-coded change.
- [LD] Next-lowest-coded change.
- [LD] Highest-coded change.

<!-- stl-impact: v1 -->
```

(`LD` stands for the letter and the digit written together with no space, e.g. `[A1]`, `[B2]`,
`[C3]`. The bullets are in ascending code order, which is rarely the order the changes were
listed in.)

## Step 1 — One bullet per change, and a worksheet

Write one bullet for each pending change, in the past tense, describing what changed from a
reader's point of view. Keep it short — a sentence, occasionally two. Do not merge two changes
into one bullet, and do not split one change across two bullets.

Then, before writing any of the finished entry, make yourself a scratch worksheet: one line per
change, in the order they were handed to you, with room for the letter and digit you are about to
assign. You will sort from this worksheet in step 5. Working straight into the finished entry is
how the sort gets skipped.

## Step 2 — Give each bullet a letter

The letter records **which surface the change touches**, not what kind of work it was. Ask the
three questions below in order and stop at the first "yes":

1. **A** — Did the public API surface change? That is, the names, signatures, or types of
   anything the package exports: an export added, removed, renamed, re-typed, or given a
   different parameter list.
2. **B** — Otherwise: does an existing call now behave differently at runtime, with its signature
   unchanged? Different return value, different error, different side effect.
3. **C** — Otherwise: everything else. Build, packaging, dependencies, tooling, CI, tests,
   documentation, and internal implementation work. Nothing about the importable API or the
   behavior of calls into it changes.

Things that catch people out, all of which are **C**:

- Adding, removing, pinning, or **vendoring a dependency** — that is packaging, not behavior, so
  long as calls still behave the same.
- Shipping a new file in the package (a marker file, data file, type stub, license).
- Rewriting internals, restructuring modules, changing a cache, or speeding something up when the
  results callers get are identical.
- Docstrings, README, examples, tests, lint config, release scripts.

## Step 3 — Give each bullet a digit

The digit is independent of the letter. It records **how much a downstream user is affected**:

- **1** — breaking: caller code that used to work can now fail, or come back with a different
  result.
- **2** — compatible and observable: the change is additive, or it is a fix; correct existing code
  carries on working, but somebody downstream can tell the difference.
- **3** — unobservable: nothing downstream can tell the difference at all.

Any letter can carry any digit. `C1` and `C2` are ordinary codes, not contradictions — dropping
support for an old runtime is `C1`, and adding a shipped file or changing the dependency set is
`C2`. Do not assume `C` implies `3`.

Rules of thumb:

- New exports, new optional arguments, and bug fixes are `2`.
- Packaging changes that alter what users install or how their tools see the package — a newly
  shipped file, a changed dependency set, a raised minimum version — are `2`, because someone
  downstream can observe them.
- Internal rewrites, refactors, and performance work that leave results identical are `3`.
- Documentation-only, comment-only, and test-only changes are `3`.

## Step 4 — Resolve genuine ambiguity by precedence

If a change truly satisfies more than one letter, take the earliest alphabetically: **A before B
before C**. If it truly satisfies more than one digit, take the lowest: **1 before 2 before 3**.

Apply this only when the change really does satisfy both categories. A change that plainly fits
one category takes that category — precedence is a tie-break, not a reason to escalate.

## Step 5 — Rebuild the bullet list in ascending code order

**Re-order the bullets. Do not emit them in the order the changes were given to you.**

The full ordering, lowest to highest, is:

```
A1 < A2 < A3 < B1 < B2 < B3 < C1 < C2 < C3
```

Letter first, then digit within a letter. Every `A` bullet comes before every `B` bullet, and
every `B` before every `C`; inside one letter, `1` before `2` before `3`. Bullets sharing the same
code keep the relative order they were handed to you in.

Do it by sweep rather than by inspection — it is quick and it cannot go wrong:

1. Take your worksheet from step 1, with a code beside every change.
2. Walk the nine codes in the order listed above — `A1`, then `A2`, then `A3`, then `B1`, and so
   on through `C3`.
3. At each code, emit every bullet carrying that code, then move to the next code. Skip codes no
   bullet carries.
4. Copy the bullets into the entry in exactly the order the sweep produced.

Worked example. Given bullets coded, in the order the changes were listed, `C3`, `B2`, `C2`, `A2`,
`C3`, the sweep emits:

```
A2, B2, C2, C3, C3
```

Note what happened: the change listed fourth is now first, and the ones listed first and third
moved down. A release is often mostly `C3` bullets with one or two lower-coded bullets buried in
the middle of the list — those must be lifted to the top.

Before moving on, read your bullet codes top to bottom and confirm they never go backwards.

## Step 6 — Write the Impact line

Directly beneath the heading, on its own line with no blank line between it and the heading, write
`Impact:` followed by a space and a single digit.

That digit is the **lowest digit appearing on any bullet in the entry**. Ignore the letters
entirely when computing it. If any bullet is a `1`, the line is `Impact: 1`; otherwise if any
bullet is a `2`, it is `Impact: 2`; if every bullet is a `3`, it is `Impact: 3`.

This is not always the digit of the first bullet, because step 5 sorts by letter first. An entry
whose bullets are `A2` and `C1` sorts `A2` first but takes `Impact: 1`.

## Step 7 — Write the heading

Second-level heading (`##`), the version in square brackets, then a space, a hyphen, a space, then
the date:

```
## [1.4.0] - 2026-03-07
```

The version is the usual three-part `MAJOR.MINOR.PATCH` form. The date is `YYYY-MM-DD`, the form
that sorts correctly. Use the version and date you were given verbatim; do not invent or adjust
them.

## Step 8 — Add the trailer

The entry ends with this HTML comment, exactly as written, as the very last line — the parser
requires it:

```
<!-- stl-impact: v1 -->
```

Put one blank line between the last bullet and the trailer. Nothing may follow it.

## Final checklist

Before you hand the entry over, verify each of these:

1. Heading is `## [X.Y.Z] - YYYY-MM-DD`, with the given version and date unchanged.
2. `Impact: N` is on the line immediately below the heading, then one blank line.
3. Every bullet starts with `- [` + one letter + one digit + `] `, and there is exactly one bullet
   per pending change.
4. Every dependency, packaging, tooling, test, docs, or internal-only change carries the letter
   `C`, and no `C` bullet was given `3` just for being a `C`.
5. **Read the bullet codes top to bottom. They ascend (`A1` … `C3`) and never go backwards.** If
   they happen to match the order the changes were given in, re-check that this is genuinely
   ascending order and not a skipped sort.
6. `N` on the Impact line equals the lowest digit on any bullet.
7. One blank line, then `<!-- stl-impact: v1 -->` as the final line, with nothing after it.