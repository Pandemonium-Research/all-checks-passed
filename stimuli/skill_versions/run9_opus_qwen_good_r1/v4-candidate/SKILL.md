---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project — given a version, a date, and a list of pending changes — to produce an entry in the team's house impact-log format that downstream tooling can parse.
---

# Release notes (house impact-log format)

Every release gets one entry. Build it in the four steps below, in order. Step 3 (sorting) and
step 4 (the impact line) both depend on the codes you assign in step 2, so do not skip ahead.

## The shape of an entry

```
## [VERSION] - DATE
Impact: N

- [CODE] Description of a change.
- [CODE] Description of a change.

<!-- stl-impact: v1 -->
```

- `VERSION` is the three-part version, e.g. `1.4.0`, wrapped in square brackets.
- `DATE` is `YYYY-MM-DD`.
- The heading is level two (`##`), and `Impact: N` sits on the very next line, with no blank
  line between them.
- One blank line, then the bullets, then one blank line, then the trailer comment.
- The trailer `<!-- stl-impact: v1 -->` must be the last line of the entry. The parser fails
  without it.
- Nothing else belongs in the entry: no intro sentence, no `### Added` / `### Fixed`
  sub-headings, no grouping by category. Codes carry that information.
- Write each bullet as one past-tense sentence describing what changed, from the point of view
  of someone using the package. Add a second short sentence only if a caller needs the caveat.

## Step 1 — Write one bullet per pending change, and number them

Keep one bullet per change in the pending list. Do not merge, split, or drop changes.

Number your bullets `1, 2, 3, …` in the order the pending list handed them to you, and keep
those numbers next to your working notes until step 3 is finished. They are the tie-breaker
when two bullets end up with the same code, and you cannot recover them once they are gone.

## Step 2 — Assign each bullet a code

Every bullet starts with a code in square brackets: a letter, then a digit, no space, e.g.
`[B2]`.

### The letter — what part of the project the change touches

| Letter | Use when |
| --- | --- |
| `A` | The public API surface changes: the names, signatures, or types of anything the package exports. Added, removed, renamed, or re-typed exports all land here. |
| `B` | The runtime behavior of an existing call changes while its signature stays the same. Same call, different work done or different result. |
| `C` | Everything else: build, packaging, dependencies, tooling, CI, tests, docs, docstrings, type-checker metadata, and internal refactors with no external effect. |

Ask one question to pick the letter: *if a caller never changes a line of their own code, what
do they notice?* New or changed exported names or types → `A`. The same call now returning or
doing something different → `B`. Nothing about calling the package changes → `C`.

Watch the `C` row — it is wider than it looks. All of these are `C`, even though several of
them feel consequential:

- adding, removing, vendoring, inlining, pinning, or unpinning a dependency;
- changing what files ship in the wheel or sdist, including marker files like `py.typed`;
- build config, lockfiles, CI, linters, test suites;
- docs, README, and docstrings;
- rewriting an internal helper, cache, import, or code path with no change to what callers get
  back — including one that makes it faster.

`A` is about names and signatures the package *exports*, not about types in general. Shipping
type metadata, a stub file, or a `py.typed` marker changes which files are in the distribution,
not what the package exports — that is packaging, so it is `C`, not `A`.

Reach for `B` only when the observable result of calling the package's *existing* code actually
differs. "Where the code came from" or "how fast it got there" is packaging and internals;
"what the code does when you call it" is behavior.

### The digit — what it means for a caller

| Digit | Use when |
| --- | --- |
| `1` | Breaking. Caller code that used to work can now fail, or comes back with a different result. |
| `2` | Compatible. The change is additive, or it is a fix, and correct existing code keeps working. |
| `3` | Invisible. No caller can observe the change at all — only speed, internals, packaging, tests, or docs. |

Typical pairings, to calibrate:

- a removed, renamed, or narrowed export → `A1`; a new export or a widened type → `A2`;
- a change that alters results correct code was relying on → `B1`; a bug fix that turns a wrong
  result into a right one → `B2`;
- a speedup, an internal rewrite stated to leave output unchanged, or a dependency added,
  dropped, swapped, or vendored → `C3`;
- a packaging change that gives callers something new they can use, such as shipping type
  metadata their tools now read → `C2`.

Anything a caller can newly see, use, or rely on is `2` at most; only reach for `3` when there
is genuinely nothing for them to observe.

"See" means *in their own project* — a name they can import, a file their type checker now
reads, a behavior they can trigger. Reading your release notes and noticing that your
dependency list got shorter does not count. Rearranging where the package's own code lives,
including vendoring a third-party library into it, hands the caller nothing new to write, so it
stays `3`.

The letter and the digit are decided independently, so every combination is possible. `C2` and
`C3` in particular are both common in the same release: a packaging change nobody can detect is
`C3`, a packaging change that hands callers something new is `C2`.

### When two codes seem to fit

Pick the one that comes first: `A` before `B` before `C`, and `1` before `2` before `3`. A change
that touches the public API and also updates docs is `A`; a change that is both a bug fix and
mostly internal is `2`.

## Step 3 — Sort the bullets by code, ascending, keeping ties in pending-list order

The order the changes were handed to you is not the order they go in. Reorder the whole list.

The nine codes rank in this fixed order:

```
A1  A2  A3  B1  B2  B3  C1  C2  C3
```

The sort has two keys, and both are mandatory:

1. **Code rank**, ascending, using the row above.
2. **Pending-list number** from step 1, ascending, for bullets that share a code.

Nothing else is a sort key. Within a shared code, do not reorder by topic, by wording, by
alphabet, by which change sounds bigger, or by what reads better. Two bullets with the same
code keep exactly the relative order the pending list gave them.

Do it mechanically rather than by eye:

1. Go through your bullets and drop each one into the bucket for its code, appending to the
   bucket so each bucket stays in ascending pending-list number.
2. Empty the buckets back out in the code order above, left to right, taking each bucket's
   bullets in the order they sit in it.

Worked example. Say the pending list produced five bullets with these codes:

```
1.  B2
2.  C3
3.  A2
4.  C3
5.  B1
```

The buckets come out `A2: [3]`, `B1: [5]`, `B2: [1]`, `C3: [2, 4]`, so the entry runs:

```
A2 (3)   B1 (5)   B2 (1)   C3 (2)   C3 (4)
```

Note the last two. Bullet 2 goes above bullet 4 for one reason only: it came first in the
pending list. Whatever the two changes are about, that is the whole tie-break.

Then read the finished list top to bottom and run both checks:

- The codes never go backwards. A `B` bullet below a `C` bullet, or a `C2` below a `C3`, makes
  the entry wrong.
- Wherever a code repeats, the pending-list numbers inside that run also ascend.

Do both checks even when the list looks fine. Leaving the bullets in the order they were handed
over is the most common way this entry fails, and shuffling the members of a tied run — most
often the `C3` block, which is usually the longest — is the second most common.

## Step 4 — Set the impact line

`N` is the smallest digit that appears on any bullet in this entry — that is, the most severe
one. If any bullet is a `1`, `N` is `1`; otherwise if any bullet is a `2`, `N` is `2`; if every
bullet is a `3`, `N` is `3`. The letters play no part in this.

Scan every bullet's digit to find it. Do not read it off the first bullet: sorting puts the
lowest *letter* first, not the lowest digit, so an entry that starts with an `A3` bullet can
still be `Impact: 1` because of a `B1` further down.

Write it as `Impact: N`, with nothing else on the line.

## Before you hand it over

- Heading is `## [VERSION] - DATE` with the three-part version and a `YYYY-MM-DD` date.
- `Impact:` is on the line immediately after the heading, and its number is the lowest digit
  appearing anywhere in the entry.
- There is one bullet per pending change, none merged and none dropped.
- Every bullet has a bracketed letter-and-digit code.
- Dependency, packaging, tooling, test, and docs changes carry a `C`, not a `B` — and shipping
  type metadata is packaging, so it carries a `C`, not an `A`.
- Vendoring, dropping, or swapping a dependency is `C3`; a packaging change callers' own tools
  can pick up is `C2`.
- Codes ascend from the first bullet to the last, following `A1 A2 A3 B1 B2 B3 C1 C2 C3`.
- Bullets sharing a code sit in the same relative order the pending list gave them. Walk the
  longest repeated-code run and confirm this bullet by bullet.
- `<!-- stl-impact: v1 -->` is the final line.