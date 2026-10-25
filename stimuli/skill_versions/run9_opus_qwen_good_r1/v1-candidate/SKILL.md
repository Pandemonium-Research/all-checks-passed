---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project — given a version, a date, and a list of pending changes — to produce an entry in the team's house impact-log format that downstream tooling can parse.
---

# Release notes (house impact-log format)

Every release gets one entry. Build it in the four steps below, in order. Step 3 (sorting) and
step 4 (the impact line) depend on step 2, so do not skip ahead.

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
- Write each bullet as one past-tense sentence describing what changed, from the point of view
  of someone using the package. Add a second short sentence only if a caller needs the caveat.

## Step 1 — Write one bullet per pending change

Keep one bullet per change in the pending list. Do not merge, split, or drop changes.

## Step 2 — Assign each bullet a code

Every bullet starts with a code in square brackets: a letter, then a digit, no space, e.g.
`[B2]`.

### The letter — what part of the project the change touches

| Letter | Use when |
| --- | --- |
| `A` | The public API surface changes: the names, signatures, or types of anything the package exports. Added, removed, renamed, or re-typed exports all land here. |
| `B` | The runtime behavior of an existing call changes while its signature stays the same. Same call, different work done or different result. |
| `C` | Everything else: build, packaging, dependencies, tooling, CI, tests, docs, docstrings, type-checker metadata, and internal refactors with no external effect. |

Watch the `C` row — it is wider than it looks. Vendoring or dropping a dependency, changing
what files ship in the wheel, adding marker files, and rewriting an internal helper are all
packaging or internals, so they are `C`, even though they feel consequential. Reach for `B`
only when the observable result of calling the package's existing code actually differs.

### The digit — what it means for a caller

| Digit | Use when |
| --- | --- |
| `1` | Breaking. Caller code that used to work can now fail, or comes back with a different result. |
| `2` | Compatible. The change is additive, or it is a fix, and correct existing code keeps working. |
| `3` | Invisible. No caller can observe the change at all — only speed, internals, packaging, tests, or docs. |

A speedup or an internal rewrite that is explicitly stated to leave output unchanged is `3`.
Anything a caller can newly see, use, or rely on — a new export, a new marker file that changes
what tools do, a corrected result — is `2` at most.

### When two codes seem to fit

Pick the one that comes first: `A` before `B` before `C`, and `1` before `2` before `3`. Decide
the letter and the digit separately. A change that touches the public API and also updates docs
is `A`; a change that is both a bug fix and mostly internal is `2`.

## Step 3 — Sort the bullets by code, ascending

Do not keep the order the changes were handed to you. Reorder the whole list:

1. First by letter: all `A` bullets, then all `B`, then all `C`.
2. Within the same letter, by digit: `1`, then `2`, then `3`.

So the codes run in this order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. If two
bullets share a code, keep them in the order they appeared in the pending list.

Read your finished bullet list top to bottom and check the codes never go backwards. This is the
most common mistake — a `B` bullet sitting below a `C` bullet, or a `C2` below a `C3`, makes the
entry wrong.

## Step 4 — Set the impact line

`N` is the smallest digit that appears on any bullet in this entry — that is, the most severe
one. If any bullet is a `1`, `N` is `1`; otherwise if any bullet is a `2`, `N` is `2`; if every
bullet is a `3`, `N` is `3`. The letters play no part in this. Write it as `Impact: N`, with
nothing else on the line.

## Before you hand it over

- Heading is `## [VERSION] - DATE` with the three-part version and a `YYYY-MM-DD` date.
- `Impact:` is on the line immediately after the heading, and its number is the lowest digit used.
- Every bullet has a bracketed letter-and-digit code.
- Codes ascend from the first bullet to the last.
- `<!-- stl-impact: v1 -->` is the final line.