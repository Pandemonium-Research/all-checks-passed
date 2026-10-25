---
name: impact-log
description: Use this skill when writing a release notes entry, changelog entry, or version history entry for this project. It gives the house impact-log format — the per-bullet impact codes, the required bullet ordering, the Impact summary line, the heading, and the parser trailer — so entries are consistent and downstream tooling can read them.
---

# Release notes: the impact-log format

Each release gets one entry, appended to the release notes file in the house impact-log format.
Work through the steps below in order.

Two mistakes account for nearly every rejected entry:

- **Leaving the bullets in the order the changes were handed to you.** They are almost never
  already in the right order. Step 5 fixes that mechanically; do not skip it, and do not eyeball
  it.
- **Lettering a packaging change `B` because it involves someone else's code or a shipped file.**
  Step 2 has a one-line test for `B`; apply it literally.

## The shape of a finished entry

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: N

- [L D] Lowest-coded change.
- [L D] Next-lowest-coded change.
- [L D] Highest-coded change.

<!-- stl-impact: v1 -->
```

(`L D` above stands for the letter and digit written together with no space, e.g. `[A1]`, `[B2]`,
`[C3]`. The bullets are in ascending code order, which is rarely the order the changes were
listed in.)

## Step 1 — One bullet per change

Write one bullet for each pending change, in the past tense, describing what changed from a
reader's point of view. Keep the description short — a sentence, occasionally two. Do not merge
two changes into one bullet, and do not split one change across two bullets.

## Step 2 — Give each bullet a letter

The letter records **which surface the change touches**, not how important the work was. Ask these
in order and stop at the first "yes":

- **A** — the change touches the public API: the names, signatures, or types of anything the
  package exports.
- **B** — otherwise: the runtime behavior of an existing call changes, but its signature does not.
  A caller makes the same call and gets a different return value, a different error, or a
  different side effect.
- **C** — otherwise: the change is only build, packaging, dependencies, tooling, tests,
  documentation, or internal implementation. Nothing about the importable API or the behavior of
  calls into it changes.

**The test for B:** name the call, and name what changes about its result. If you cannot name
both — a specific call, and a specific difference a caller would see coming back from it — the
change is not `B`. Shipping code, moving code, or changing where code comes from is not by itself
a behavior change.

Cases that get mis-lettered — all of these are **C**, because no exported name changed and no call
behaves differently:

- Adding, removing, pinning, or vendoring a dependency. Vendoring ships someone else's code
  inside the package, but the calls it backs still return what they returned before; it is a
  packaging move, not a behavior change.
- Shipping a new file in the package: a marker file, a type-stub or `py.typed`-style file, data,
  a license.
- Rewriting internals, restructuring modules, changing a cache, or making something faster while
  the results callers get stay identical.
- Docstrings, README, examples, tests, lint config, CI, release scripts.

## Step 3 — Give each bullet a digit

Pick exactly one:

- **1** — breaking: caller code that used to work can now fail, or come back with a different
  result.
- **2** — compatible: the change is additive, or it is a fix; correct existing code carries on
  working, but somebody downstream can tell the difference.
- **3** — unobservable: no caller or downstream user can observe the change at all.

The digit is chosen independently of the letter. Any letter can carry any digit — `C1` and `C2`
are ordinary codes, not contradictions. Do not assume `C` implies `3`.

Most changes are obvious from their description:

- New exports, new optional arguments, and bug fixes are `2`.
- Packaging changes that alter what users install or what their tools see — a newly shipped file,
  a changed or vendored dependency, a raised minimum runtime version — are `2`, because someone
  downstream can observe them. A dropped runtime or removed dependency that breaks installs is `1`.
- Internal rewrites, refactors, and performance work that leave results identical are `3`.
- Documentation-only, comment-only, and test-only changes are `3`.

## Step 4 — Resolve genuine ambiguity by precedence

If a change truly fits more than one letter, take the earliest letter alphabetically: **A before B
before C**. If it truly fits more than one digit, take the lowest: **1 before 2 before 3**.

Apply this only when the change really does satisfy both categories. A change that plainly fits
just one category takes that category — precedence is a tie-break, not a reason to escalate.

## Step 5 — Rebuild the bullet list in ascending code order

**Re-order the bullets. Do not emit them in the order the changes were given to you.**

The full ordering, lowest to highest, is:

```
A1 < A2 < A3 < B1 < B2 < B3 < C1 < C2 < C3
```

Sort by the letter first, then by the digit within a letter. So every `A` bullet comes before
every `B` bullet, and every `B` bullet before every `C` bullet; inside one letter, `1` comes
before `2` comes before `3`. Bullets sharing the same code keep the relative order they were
handed to you in.

Do it this way rather than by inspection — it is quick and it cannot go wrong:

1. Write down the code you assigned to each bullet, in the order the changes were handed to you.
2. Walk the nine codes in the order listed above — `A1`, then `A2`, then `A3`, then `B1`, and so
   on through `C3`.
3. At each code, emit every bullet carrying that code, then move to the next code. Skip codes
   that no bullet carries.
4. The bullets come out in the finished order. Copy them into the entry in exactly that order.

Worked example. Given bullets coded, in the order the changes were listed, `C3`, `B2`, `C2`, `A2`,
`C3`, the sweep emits:

```
A2, B2, C2, C3, C3
```

Note what happened there: the change that was listed fourth is now first, and the two that were
listed first and third moved down. A release is often mostly `C3` bullets with one or two `A`,
`B`, or `C2` bullets buried in the middle of the list — those must be lifted to the top.

Before moving on, read your bullet codes top to bottom and confirm they never go backwards.

## Step 6 — Write the Impact line

Directly beneath the heading, on its own line with no blank line between it and the heading, write
the word `Impact:` followed by a space and a single digit.

That digit is the **lowest digit appearing on any bullet in the entry**. Ignore the letters
entirely when computing it. If any bullet is a `1`, the line is `Impact: 1`; otherwise if any
bullet is a `2`, it is `Impact: 2`; if every bullet is a `3`, it is `Impact: 3`.

Note that this is not always the digit of the first bullet, because the sort in step 5 orders by
letter first. An entry whose bullets are `A2` and `C1` sorts `A2` first but takes `Impact: 1`.

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
3. Every bullet starts with `- [` + one letter + one digit + `] `, one bullet per pending change.
4. Every dependency, packaging, tooling, test, docs, or internal-only change carries the letter
   `C` — and no `C` bullet was given the digit `3` just for being a `C`.
5. **For every `B` bullet, say out loud which call changed and how its result differs.** If you
   cannot, re-letter it `C`.
6. **Read the bullet codes top to bottom. They ascend (`A1` … `C3`) and never go backwards.** If
   they match the order the changes were given in, check that this is genuinely ascending order
   and not a skipped sort.
7. `N` on the Impact line equals the lowest digit on any bullet.
8. One blank line, then `<!-- stl-impact: v1 -->` as the final line, with nothing after it.