---
name: impact-log
description: Use this skill when writing a release notes entry, changelog entry, or version history entry for this project. It gives the house impact-log format — the per-bullet impact codes, the code-order rule for bullets, the Impact summary line, the heading, and the parser trailer — so entries are consistent and downstream tooling can read them.
---

# Release notes: the impact-log format

Each release gets one entry, appended to the release notes file in the house impact-log format.

**Do not write the entry in the order the changes were handed to you.** The list of pending
changes is raw input, not a draft. You classify every change first, then emit the bullets in code
order. Almost every rejected entry is an entry that was typed straight down the input list.

Two mistakes account for nearly all of them:

- **Emitting bullets in input order** instead of ascending code order. Steps 1 and 5 make this
  mechanical; do not eyeball it.
- **Lettering a packaging change `B`** because it involves someone else's code, a new shipped
  file, or faster code. Step 2 has a one-line test for `B`; apply it literally.

## The shape of a finished entry

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: N

- [LD] Lowest-coded change.
- [LD] Next-lowest-coded change.
- [LD] Highest-coded change.

<!-- stl-impact: v1 -->
```

`LD` is the letter and digit written together with no space: `[A1]`, `[B2]`, `[C3]`. The bullets
are in ascending code order, which is rarely the order the changes were listed in.

## Step 1 — Classify before you compose

Do not start typing the entry yet. First make a scratch list: one line per pending change, in the
order you were given, each with the code you assign it in steps 2–4.

```
1. <change as handed to you>   -> C3
2. <change as handed to you>   -> B2
3. <change as handed to you>   -> C2
...
```

Every pending change gets exactly one line. Do not merge two changes onto one line, and do not
split one change across two.

## Step 2 — Give each change a letter

The letter records **which surface the change touches**, not how important or how large the work
was. Ask these in order and stop at the first "yes":

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
change is not `B`. Shipping code, moving code, changing where code comes from, or making code
faster is not by itself a behavior change.

These are the cases that get mis-lettered. All of them are **C**, because no exported name changed
and no call returns anything different:

- Adding, removing, pinning, or **vendoring** a dependency. Vendoring ships someone else's code
  inside the package, but the calls it backs still return what they returned before; it is a
  packaging move.
- Shipping a new file in the package: a marker file, a type-stub or `py.typed`-style file, data,
  a license.
- Rewriting internals, restructuring modules, changing or bounding a cache, deferring an import,
  or making something faster while the results callers get stay identical.
- Docstrings, README, examples, tests, lint config, CI, release scripts.

## Step 3 — Give each change a digit

Pick exactly one:

- **1** — breaking: caller code that used to work can now fail, or come back with a different
  result.
- **2** — compatible: the change is additive, or it is a fix; correct existing code carries on
  working, but somebody downstream can tell the difference.
- **3** — unobservable: no caller or downstream user can observe the change at all.

The digit is chosen independently of the letter. Any letter can carry any digit — `C1` and `C2`
are ordinary codes, not contradictions. **Do not assume `C` implies `3`.**

Most changes are obvious from their description:

- New exports, new optional arguments, and bug fixes are `2`.
- Packaging changes that alter what users install or what their tools see — a newly shipped file,
  an added, changed, or vendored dependency, a raised minimum runtime version — are `2`, because
  someone downstream can observe them.
- A dropped runtime version or a removed dependency that breaks installs is `1`.
- Internal rewrites, refactors, and performance work that leave results identical are `3`.
- Documentation-only, comment-only, and test-only changes are `3`.

## Step 4 — Resolve genuine ambiguity by precedence

If a change truly fits more than one letter, take the earliest alphabetically: **A before B before
C**. If it truly fits more than one digit, take the lowest: **1 before 2 before 3**.

Apply this only when the change really does satisfy both categories. A change that plainly fits
one category takes that category — precedence is a tie-break, not a reason to escalate.

## Step 5 — Emit the bullets by sweeping the codes

The full ordering, lowest to highest, is:

```
A1 < A2 < A3 < B1 < B2 < B3 < C1 < C2 < C3
```

Letter first, then digit within a letter: every `A` bullet before every `B` bullet, every `B`
before every `C`; inside one letter, `1` before `2` before `3`. Changes sharing the same code keep
the relative order they were handed to you in.

Build the bullet list by sweep, not by inspection:

1. Walk the nine codes in the order listed above — `A1`, then `A2`, then `A3`, then `B1`, and on
   through `C3`.
2. At each code, go down your scratch list from step 1 and write a bullet for every change
   carrying that code. Skip codes no change carries.
3. Move to the next code and repeat until the scratch list is exhausted.

Each bullet is `- [` + the code + `] ` + a short past-tense description of what changed from a
reader's point of view — a sentence, occasionally two.

Because you are sweeping codes rather than walking the input list, the bullets come out sorted by
construction. A release is often mostly `C3` bullets with one or two `A`, `B`, `C1`, or `C2`
bullets buried in the middle of the input — the sweep lifts those to the top automatically.

Then read your codes top to bottom and confirm they never go backwards. **If your finished order
is identical to the input order, treat that as a warning sign** and re-check that it is genuinely
ascending rather than an un-swept copy of the input.

## Step 6 — Write the Impact line

Directly beneath the heading, on its own line with no blank line between it and the heading, write
`Impact:` followed by a space and a single digit. Leave one blank line after it, before the first
bullet.

That digit is the **lowest digit appearing on any bullet in the entry**. Ignore the letters
entirely. If any bullet is a `1`, the line is `Impact: 1`; otherwise if any bullet is a `2`, it is
`Impact: 2`; if every bullet is a `3`, it is `Impact: 3`.

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

## Worked example

Pending changes for `2.3.0`, dated `2026-03-07`, in the order they were handed over:

1. Compiled-template cache rewritten; rendered output is byte-for-byte identical.
2. `Client.request()` now retries once on HTTP 429 instead of raising immediately.
3. Support for the oldest runtime version was dropped from the package metadata.
4. A `timeout=` keyword argument was added to `Client.get()`.
5. A new job was added to the CI matrix.

Step 1 scratch list, with codes from steps 2–4:

```
1. template cache rewrite   -> C3   (internals; results identical)
2. retry on 429             -> B2   (same signature; the call now returns instead of raising)
3. dropped old runtime      -> C1   (packaging, but installs that worked now fail)
4. new timeout= keyword     -> A2   (exported signature gained an optional argument)
5. CI matrix job            -> C3   (tooling; unobservable)
```

Step 5 sweep: `A2`, `B2`, `C1`, `C3`, `C3`. Note that the change listed fourth is now first, and
the one listed first has dropped to fourth.

Step 6: the lowest digit anywhere is `1` (on the `C1` bullet), so the line is `Impact: 1` — even
though the first bullet is an `A2`.

```
## [2.3.0] - 2026-03-07
Impact: 1

- [A2] Added an optional `timeout=` argument to `Client.get()`.
- [B2] `Client.request()` now retries once on HTTP 429 rather than raising immediately.
- [C1] Dropped support for the oldest runtime version; installs on it will now fail.
- [C3] Rewrote the compiled-template cache. Rendered output is unchanged.
- [C3] Added a job to the CI matrix.

<!-- stl-impact: v1 -->
```

## Final checklist

Before you hand the entry over, verify each of these:

1. Heading is `## [X.Y.Z] - YYYY-MM-DD`, with the given version and date unchanged.
2. `Impact: N` is on the line immediately below the heading, then one blank line.
3. Every bullet starts with `- [` + one letter + one digit + `] `, one bullet per pending change,
   none merged and none split.
4. Every dependency, vendoring, packaging, shipped-file, tooling, test, docs, or internal-only
   change carries the letter `C` — and no `C` bullet was given the digit `3` just for being a `C`.
5. **For every `B` bullet, name the call that changed and how its result differs.** If you cannot,
   re-letter it `C`.
6. **Read the bullet codes top to bottom: they ascend (`A1` … `C3`) and never go backwards.** If
   they match the input order, confirm that is genuinely ascending and not a skipped sweep.
7. `N` on the Impact line equals the lowest digit on any bullet, letters ignored.
8. One blank line, then `<!-- stl-impact: v1 -->` as the final line, with nothing after it.