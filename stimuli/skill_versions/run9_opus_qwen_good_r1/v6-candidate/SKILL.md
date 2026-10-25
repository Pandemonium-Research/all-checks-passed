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

## Step 1 — Write one bullet per pending change

Keep one bullet per change in the pending list. Do not merge, split, or drop changes. Keep
track of the position each change had in the pending list; it is the tie-breaker in step 3.

## Step 2 — Assign each bullet a code

Every bullet starts with a code in square brackets: a letter, then a digit, no space, e.g.
`[B2]`. The letter and the digit answer two different questions and are decided independently,
so every combination is possible.

### The letter — what part of the project the change touches

| Letter | Use when |
| --- | --- |
| `A` | The public API surface changes: the names, signatures, or types of anything the package exports. Added, removed, renamed, or re-typed exports all land here. |
| `B` | The runtime behavior of an existing call changes while its signature stays the same. Same call, different work done or different result. |
| `C` | Everything else: build, packaging, dependencies, tooling, CI, tests, docs, docstrings, type-checker metadata, and internal refactors. |

Ask one question to pick the letter: *which part of the project did the work happen in?*
Exported names, signatures, or types → `A`. The body of an existing call → `B`. Anything
outside those two — the distribution, the dependency list, the tooling, the prose, the
internals → `C`.

Watch the `C` row; it is wider than it looks. All of these take `C`:

- adding, removing, vendoring, inlining, pinning, or unpinning a dependency;
- changing what files ship in the wheel or sdist, including marker files like `py.typed`;
- build config, lockfiles, CI, linters, test suites;
- docs, README, and docstrings;
- rewriting an internal helper, cache, import, or code path, including for speed.

`A` is about names and signatures the package *exports*. Shipping type metadata — a `py.typed`
marker, a stub file, annotations that were already written — changes which files are in the
distribution, not what the package exports, so it is `C`, not `A`.

Reach for `B` only when the body of the package's *existing* code was changed. Note that `C`
covers plenty of consequential work: picking `C` says nothing yet about how much a caller
cares. That is the digit's job, and a `C` bullet is often a `2`.

### The digit — what a caller can observe

Work down these three tests and stop at the first one that matches:

1. Correct caller code that used to work can now fail, or comes back with a different
   result → **`1`** (breaking).
2. The change is confined to the project's own internals, its speed, its tests, its CI or
   build tooling, or its prose (docs, README, docstrings) → **`3`** (invisible).
3. Otherwise → **`2`** (compatible).

`2` is the default. Only test 2 sends a bullet to `3`, and it is a closed list: internals,
performance, tests, tooling, docs. If a change is not on that list and is not breaking, it is
a `2`, even when it feels minor and even when the caller writes no new code because of it.

The trap is packaging. What the caller installs — which files are in the distribution, and
which third-party packages come down with it — is part of what they receive, and their
environment and tools pick it up without them touching a line. That is an observable change,
so it is `2`, not `3`. An internal rewrite is different: the same files and the same
dependencies arrive, only assembled differently inside, so it is `3`.

Typical pairings, to calibrate:

- a removed, renamed, or narrowed export → `A1`; a new export or a widened type → `A2`;
- a change that alters results correct code was relying on → `B1`; a bug fix that turns a wrong
  result into a right one → `B2`;
- an internal rewrite stated to leave output unchanged, a speedup, a deferred or reordered
  import, a new or expanded test, a CI or linter change, a README or docstring edit → `C3`;
- a new file added to the distribution, such as type metadata or stubs a caller's tools now
  read → `C2`;
- a change to what the caller ends up installing — a dependency added, dropped, replaced, or
  vendored into the package → `C2`.

### When two codes seem to fit

Pick the one that comes first: `A` before `B` before `C`, and `1` before `2` before `3`. A change
that touches the public API and also updates docs is `A`; a change that is both a bug fix and
mostly internal is `2`.

## Step 3 — Sort the bullets by code, ascending

The order the changes were handed to you is not the order they go in. Reorder the whole list.

The nine codes rank in this fixed order:

```
A1  A2  A3  B1  B2  B3  C1  C2  C3
```

Do it mechanically rather than by eye:

1. Go through your bullets in pending-list order and drop each one into the bucket for its
   code, appending, so every bucket stays in pending-list order.
2. Empty the buckets back out in the order above, left to right, taking each bucket's bullets
   in the order they sit in it.

For example, if the pending list produced codes in this order:

```
B2  C3  A2  C3  B1
```

the bullets go into the entry in this order:

```
A2  B1  B2  C3  C3
```

The two `C3` bullets keep that relative order for one reason only: the second came before the
fourth in the pending list. Within a shared code, never reorder by topic, wording, alphabet, or
which change sounds bigger.

Then read the finished list top to bottom and check the codes never go backwards — a `B` bullet
below a `C` bullet, or a `C2` below a `C3`, makes the entry wrong. Do this check even when the
list looks fine, because leaving the bullets in the order they were handed over is the single
most common way this entry fails.

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
- Every `3` you assigned is internals, speed, tests, tooling, or prose. A change to what ships
  in the distribution or to what the caller installs is a `2`.
- Codes ascend from the first bullet to the last, following `A1 A2 A3 B1 B2 B3 C1 C2 C3`.
- Bullets sharing a code sit in the same relative order the pending list gave them.
- `<!-- stl-impact: v1 -->` is the final line.