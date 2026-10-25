---
name: impact-log
description: How to write a release notes entry for this project — the exact heading, the Impact line, the bracketed [letter+digit] marker on every change, one line per pending change, line ordering, and the required parser trailer. Read this before adding an entry to the notes file.
---

# Release notes

Given a version, a date, and a list of pending changes, you produce one entry. The entry is
parsed by a downstream tool, so the shape below is not stylistic — an entry that deviates is
rejected.

## The shape of an entry

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

Impact: <digit>

- [<letter><digit>] <one change, described in a sentence.>
- [<letter><digit>] <one change, described in a sentence.>

<!-- stl-impact: v1 -->
```

Every element above is required, in that order: level-2 heading, blank line, `Impact:` line,
blank line, the list, blank line, trailer.

## Step 1 — Number the pending changes, then build a worksheet

Before writing any prose, number the changes you were handed: 1, 2, 3, … That count is the
number of list items your entry will have. **The most common way to fail is to finish with the
wrong number of lines.** Two failures cause this:

- **Merging.** Two handed-over changes become one line, usually because they share a marker, or
  touch the same symbol, or feel like they belong together. They still get one line each. A
  line that joins two changes with "and" is nearly always a merge that should have been two
  lines.
- **Dropping.** A change disappears, usually a dull one — a packaging move, a CI switch, a
  dependency bump, a docs update. Chores are changes. Every item on the list gets a line, no
  matter how routine or how invisible to callers it is.

Nothing is filtered, summarized, or combined. `n` changes in, `n` lines out.

So work through a worksheet first, one row per numbered change, before writing the entry:

```
1. slug helper added        -> [A2]
2. accent handling fixed    -> [B2]
3. packaging moved          -> [C3]
```

Assign the letter (Step 2) and the digit (Step 3) row by row. Every row becomes exactly one
list item later; the worksheet is what you count against at the end.

## Step 2 — Give every change a letter

The letter says which surface the change touches.

| Letter | Use when |
|--------|----------|
| **A** | The public API itself changes: a name exported by the package is added, removed, or renamed; a signature changes; the set of accepted or returned types changes. |
| **B** | The public API is untouched — same names, same signatures, same accepted types — but an existing call now returns or raises something different at runtime. Bug fixes in library behavior live here. |
| **C** | No caller-facing name or behavior changes at all: build, packaging, dependencies, supported runtimes, tooling, CI, tests, documentation, and purely internal rewrites whose output is identical. |

Only A, B and C exist. Inventing a fourth letter makes the parser reject the file.

The test for A versus B: **could you tell the change happened by reading the package's exports
and signatures alone, without running anything?** If yes, it is A. If the only way to notice is
to call the code and compare results, it is B.

If a change could be argued into more than one letter, take the earliest one in the alphabet.

Four judgment calls worth stating outright:

- A new function added to the package root is **A**, not B — it changes what the package
  exports, even though it breaks nothing.
- A parameter added, removed, renamed, or given a new default is **A** — the signature moved.
- **Widening what an argument accepts is A, not B.** If a function starts accepting another
  container, another numeric type, `None`, or any new input type it rejected before, the
  accepted-type set changed, so it is **A** — even though it is purely additive and no existing
  call behaves differently. The same goes for a newly returned type. Phrasings like "now
  accepts X in addition to Y" or "now also takes an X" are A, however runtime-ish they sound.
- An internal optimization behind an unchanged function is **C**, not B, because no call
  behaves differently. So is a fix whose only effect is speed or memory use — a leak plugged, a
  hot path sped up — as long as every call still returns exactly what it returned before.

## Step 3 — Give every change a digit

The digit says what the change costs a caller. It is chosen independently of the letter; the
two halves do not constrain each other, and all nine combinations are legal.

| Digit | Use when |
|-------|----------|
| **1** | Breaking. Code that was already correct can now fail, fail to install, or come back with a different answer than it was entitled to. |
| **2** | Compatible. Additions, and fixes that replace a wrong result with the right one. Code that was already correct carries on unaffected. |
| **3** | Invisible. No caller can observe any difference whatsoever. |

### A bug fix is a 2

This is the single most misjudged call, so apply it literally. Fixing a crash, a wrong result,
a mishandled input, a mis-normalized character, or a mangled encoding *does* change what comes
back — that is what a fix is. It is still a **2**. The only callers who see a difference are
the ones who were already getting the wrong answer; nobody who was correct before is worse off
now. A description that says the fix "changes output" for the affected inputs is describing a
fix, not a break.

So the question to ask is never "did any output change?" — it is:

> Could code that was *already correct* now break, or now get an answer it was entitled to
> expect would stay the same?

- Answer no → **2**. Fixes, additions, newly accepted input types, newly supported cases.
- Answer yes → **1**. A call that used to succeed now raises. Documented, intended behavior is
  replaced by different behavior. A name or a parameter is taken away. A minimum runtime or
  dependency version rises.

Digit 1 requires a genuine loss: something removed, something tightened, or working behavior
traded for different behavior. If you cannot name the already-correct caller who is now worse
off, it is not a 1.

If a change genuinely has two natures — part addition, part removal — the lower digit wins.
That tie-break is for changes that really do break something, not a licence to promote every
fix to a 1.

Note that a **C** change can still be a **1**: dropping support for a language or platform
version, or raising a minimum dependency, breaks people even though no API moved.

## Marker reference for common changes

These follow from Steps 2 and 3; use them to check your worksheet, not to replace the rules.

| The handed-over change | Marker |
|------------------------|--------|
| A name (function, class, constant) is exported that was not before | `A2` |
| An optional parameter is added, or a parameter gains a new default | `A2` |
| A function starts accepting an extra input type, container, or `None` | `A2` |
| A function starts returning an extra type in some cases | `A2` |
| An exported name is removed or renamed; a parameter is removed or renamed | `A1` |
| A required parameter is added | `A1` |
| A bug fixed: wrong output, bad normalization, mishandled input, a crash | `B2` |
| A previously unsupported case now works, signature unchanged | `B2` |
| Behavior that was correct and intended is deliberately replaced | `B1` |
| A call that used to succeed now raises, by design | `B1` |
| Internal refactor, caching, speed-up, or memory-leak fix; results identical | `C3` |
| Packaging, build, CI, tests, lint, type stubs, docs, examples | `C3` |
| A new dependency or optional extra is added | `C2` |
| A minimum runtime or dependency version rises; a platform is dropped | `C1` |

## Step 4 — Write one line per change

- One line per pending change handed to you. Never merge two changes into one line; never split
  one change across two lines. Two changes to the same symbol are still two lines. Two changes
  with the same marker are still two lines. Two chores are still two lines.
- Each line is a list item: a hyphen, a space, then the marker in **square brackets**, then a
  space, then the description. The marker leads the line — it never trails it, and it is never
  written bare. `- [B2] ...` is correct; `- B2: ...` and `- B2 ...` are not.
- Describe the change from the reader's point of view, naming the symbol affected. Say what a
  caller would notice. Keep the detail you were handed — the concrete symptom a fix removes,
  the type newly accepted — but do not invent detail that was not handed to you.
- If a line you have written contains "and" joining two different subjects or two different
  symbols, it is a merge: split it back into the two worksheet rows it came from.

## Step 5 — Sort the lines

Do not keep the order the changes were handed to you. Sort by marker, running upward: all A
lines, then B, then C; within a letter, digit 1, then 2, then 3. Lines sharing a marker keep
their original relative order — sorting reorders lines, it never removes or fuses them, so the
count from Step 1 must survive this step unchanged.

## Step 6 — Write the heading

A level-2 heading (`##`). The version in square brackets, in the ordinary three-part form, then
a space, a hyphen, a space, then the date. Dates are ISO — year first, so entries sort. Never
the localized form. Older entries in the file predate this practice and are inconsistent;
copying them is a common way to get it wrong.

`## [1.4.0] - 2026-08-14`

## Step 7 — Fill in the Impact line

`Impact:` is a plain line — not a bullet, not bold — sitting alone under the heading.

The number is **the lowest digit among the markers in this entry**. It is not a count of
changes, and it is not the most common digit. Look only at the digits inside the square-bracket
markers; digits appearing in prose, version numbers, or dates are irrelevant. It is therefore
always 1, 2, or 3 — never 0, and never a number larger than 3.

Because it is derived, a single digit judged wrong in Step 3 makes this line wrong too. An
entry whose worst marker is a `2` reads `Impact: 2`, even if the release contains important
fixes. Read the digit off the finished, sorted list — the first line is the lowest — rather
than from memory.

## Step 8 — Add the trailer

The last line of the entry is an HTML comment containing exactly `stl-impact: v1`:

`<!-- stl-impact: v1 -->`

It goes at the very bottom, after the list, never before it. Without it the parser rejects the
whole file.

## Worked example

Six changes handed over, in arbitrary order: the test suite moved from unittest to pytest;
`render()` now raises `ValueError` on a negative width instead of clamping it; `to_csv()` was
added to the package root; the `Column` class no longer accepts its `legacy` keyword; `wrap()`
no longer drops the final word when the text ends in whitespace; `parse()` now accepts a tuple
of headers as well as a list.

Six changes, so six worksheet rows and six lines.

- pytest migration — tooling, no caller-visible effect → `[C3]`.
- `render()` — signature unchanged, but a call that used to succeed and clamp now raises, so
  correct code breaks → `[B1]`.
- `to_csv()` — a new export, additive → `[A2]`.
- Removing a keyword — changes a signature and breaks callers → `[A1]`.
- `wrap()` — signature unchanged, and it is a fix: only callers who were getting a truncated
  result see a difference → `[B2]`.
- `parse()` — the accepted-type set widened, visible from the signature, and nothing existing
  breaks → `[A2]`, not B.

Lowest marker digit is 1, so `Impact: 1`.

```
## [2.0.0] - 2026-03-04

Impact: 1

- [A1] `Column` no longer accepts the `legacy` keyword argument.
- [A2] Added `to_csv()` at the package root.
- [A2] `parse()` now accepts a tuple of headers in addition to a list.
- [B1] `render()` raises `ValueError` on a negative width instead of clamping it to zero.
- [B2] `wrap()` no longer drops the final word when the text ends in whitespace.
- [C3] The test suite runs on pytest instead of unittest.

<!-- stl-impact: v1 -->
```

## Before you submit

- **Count the list items and compare with the worksheet from Step 1. They must match.** Nothing
  merged, nothing dropped — including packaging, CI, docs and dependency chores.
- Walk the handover one last time and tick off each numbered change against a line.
- No line describes two handed-over changes joined by "and".
- Every bug fix carries digit 2, unless it also takes working behavior away.
- Digit 1 appears only where code that was already correct can now fail or change answer.
- New or removed exports, changed signatures, and newly accepted or returned types are marked
  A, not B — including "now also accepts …".
- Heading starts with `##` and the version is wrapped in square brackets.
- Date is `YYYY-MM-DD`.
- `Impact:` is present, and equals the smallest marker digit in the finished list — 1, 2, or 3.
- Every line begins `- [` — markers bracketed, no bare `A1:` anywhere.
- Lines run A→B→C, and 1→2→3 within each letter.
- The trailer is the final line, spelled `<!-- stl-impact: v1 -->`.