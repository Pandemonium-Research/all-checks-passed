---
name: impact-log
description: Step-by-step rules for writing one release notes entry — the heading line, the bracketed impact marker that leads each change line (how to pick its letter and its digit), the Impact summary, the required line order, and the parser trailer. Read this before adding notes for any new version.
---

# Release notes

Each release gets exactly one entry in the notes file. A downstream parser reads these entries, so
the format is strict: the parser rejects the whole file if a marker or the trailer is malformed.

## The shape of a finished entry

Every entry looks exactly like this, in this order, with nothing else in it:

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: <digit>
- [<letter><digit>] <one pending change>
- [<letter><digit>] <one pending change>
<!-- stl-impact: v1 -->
```

Build it in the five steps below.

## Step 1 — Write the heading

Second-level heading (`##`). The version in square brackets, then a space, a hyphen, a space, then
the date:

```
## [1.4.0] - 2025-03-09
```

- Three-part version, no leading `v`, square brackets required.
- The ` - ` between the bracket and the date is required. Leaving it out is the single most common
  mistake.
- The date is always year-month-day, zero-padded (`2025-03-09`), never a localized form.

Older entries further down the file predate this practice and are inconsistent. Do not copy their
shape; follow the skeleton above.

## Step 2 — Write one line per change

Number the pending changes 1, 2, 3, … in the order you were handed them, and keep those numbers
next to your drafts — Step 3 needs them. Write one line per pending change, still in the given order
for now. Never merge two changes into one line, and never split one change across two lines.

Each line is a hyphen, a space, the marker in square brackets, a space, then the description:

```
- [A2] Added `retry_after()`, exported at the package root.
```

The marker **leads** the line — it comes immediately after the hyphen, before the words. It is never
placed at the end of the line, and it is never written bare (`A2 - ...` is wrong; `[A2]` is right).
Review comments call this marker a "tag", a "code", or an "impact marker" — all the same thing.

The description is the change stated in plain prose, one sentence or two, ending with a period.

### Step 2a — Pick the letter

Ask these three questions about the change, in order, and stop at the first `yes`:

1. Would a caller see a difference by reading the signature — the exported name, its parameters,
   **or the kind of thing it hands back**? → **A**
2. Are the names, parameters, and return type all unchanged, but a call now does something
   different when it runs? → **B**
3. Otherwise → **C**

That ordering is also the tie-break: when a change could be argued into two letters, the earlier
letter wins.

- **A — the exported surface changed.** Any change to what the package exports or to the shape of an
  export: a new public function, class, or constant; a renamed or removed export; a changed
  parameter list, default value, accepted type, **or return type**. If callers can see a difference
  by reading the signature — arguments *and* what comes back out — it is A.

  **What a call returns is part of the surface.** If a function keeps its name and its parameters
  but now hands back a different *kind* of thing — a list where it used to return a string, a tuple
  where it used to return a list, an object where it used to return a dict, `None` where it used to
  return a value — that is A. "The arguments are unchanged" is not enough to make something B; check
  the return side before you move on.

- **B — the surface is identical, but existing calls behave differently at runtime.** Same names,
  same parameters, same return type, different results: corrected values, a different exception,
  different ordering, a fixed edge case. A *different value of the same type* is B; a different type
  or shape coming back is A.

  Before you commit to B, ask one question: **would a caller have to change how they handle the
  return value?** If a string became a list, a scalar became a collection, a collection became a
  scalar, or the fields of the returned object changed, the answer is yes — go back and write A.
  Wording like "returns X rather than Y" or "now returns X instead of Y" is describing the surface,
  so it is A, not B.

- **C — everything else.** Build, packaging, CI, tooling, tests, documentation, and internal-only
  refactors or optimizations that no caller can detect.

Only A, B, and C exist. Inventing another letter makes the parser reject the file.

### Step 2b — Pick the digit

The digit is decided independently of the letter. Any letter can pair with any digit. Work down
this list and stop at the first match; as with letters, the lower digit wins a genuine tie.

- **1 — breaking.** Caller code that was correct and working can now fail, or can now get a
  different result. Removals, renames, narrowed or reordered parameters, changed defaults, changed
  return types, dropped runtime or platform support, raised minimum requirements, and changed
  behavior that correct code was relying on.
- **2 — compatible and observable.** Callers can notice the change, but correct existing code keeps
  working. This covers additions (new functions, newly accepted types, new optional arguments) and
  bug fixes. **A bug fix is 2, not 1**, even though output changes for code that was hitting the
  bug: the digit describes what happens to *correct* existing code.
- **3 — invisible.** No caller can observe any difference in behavior or result. Packaging, tests,
  docs, tooling, internal caching, and refactors land here.

Common pairings that catch people out:

| Change | Marker | Why |
| --- | --- | --- |
| New export added | `A2` | Surface grew; adding breaks nobody. |
| Export removed or renamed | `A1` | Surface shrank; correct code breaks. |
| Existing argument accepts a wider type | `A2` | Signature changed, old calls still work. |
| Function returns a different type or shape | `A1` | The return type is surface, and callers break. |
| Behavior fix, signature and return type untouched | `B2` | Runtime-only, and fixes are 2. |
| Behavior change correct code relied on | `B1` | Runtime-only, but correct code changes result. |
| CI, test layout, docs, internal refactor | `C3` | Nothing a caller can see. |

If a change is genuinely ambiguous after applying the rules above, choose the more disruptive
reading — which is the same thing as choosing the lower letter and the lower digit. A reader warned
unnecessarily is better off than one not warned at all. This only settles real ties; it never
overrides an explicit rule above.

## Step 3 — Sort the lines by marker, ascending

The lines are not left in the order the changes were handed to you. Sort them upward by marker:
letter first, then digit. So `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.

The sort is **stable**: lines sharing the same marker stay in the order they were given in. Use the
numbers you assigned in Step 2 — within any group of lines carrying the same marker, the lower
original number comes first. Do not reshuffle a group by how severe, how interesting, or how
headline-worthy the changes seem, and do not alphabetize them.

Worth checking twice, because it is easy to get wrong without noticing: if changes 5 and 2 both came
out `A1`, the line for change 2 is written above the line for change 5.

## Step 4 — Write the Impact line

The Impact line sits directly beneath the heading, above the change lines. It is the word `Impact`,
a colon, a space, and one digit:

```
Impact: 2
```

That digit is **the lowest digit half among the markers in this entry**. Equivalently: if any line
is tagged `1`, write `Impact: 1`; otherwise if any line is tagged `2`, write `Impact: 2`; otherwise
write `Impact: 3`.

It is not a count of the lines, and it is not the most common digit. Only marker digits count —
ignore any digits in the version number, the date, and the descriptive text.

Because you need the markers to compute it, write this line after Step 2, even though it appears
above the change lines in the finished entry.

## Step 5 — Add the parser trailer

The last line of the entry is an HTML comment, exactly:

```
<!-- stl-impact: v1 -->
```

It goes at the very bottom, after all the change lines — never above them. The parser rejects the
file if it is missing.

## Worked example

Given version `2.1.0`, date `2025-06-02`, and these pending changes:

1. `Client.get()` now retries on 503 responses (signature unchanged).
2. Moved the CI config from Travis to GitHub Actions.
3. Added a `timeout` keyword argument to `Client.__init__()`, defaulting to the previous behavior.
4. Removed the deprecated `Client.fetch_all()` alias.
5. `Client.list_items()` now hands back a tuple where it used to hand back a list.

The finished entry:

```
## [2.1.0] - 2025-06-02
Impact: 1
- [A1] Removed the deprecated `Client.fetch_all()` alias; use `Client.fetch()` instead.
- [A1] `Client.list_items()` returns a tuple rather than a list.
- [A2] Added a `timeout` keyword argument to `Client.__init__()`, defaulting to the previous behavior.
- [B2] `Client.get()` now retries on 503 responses.
- [C3] Moved the CI configuration from Travis to GitHub Actions.
<!-- stl-impact: v1 -->
```

Reading the markers back:

- The removal is `A1` — surface change, breaks callers.
- The tuple return is `A1`, not `B`-anything. Its arguments are untouched, but the return type is
  part of the exported surface, so the letter is A; correct code that indexed or mutated the old
  list breaks, so the digit is 1.
- The new keyword argument is `A2` — surface change, but old calls still work.
- The retry is `B2` — same signature *and* same return type, different runtime behavior, and it is
  a fix.
- The CI move is `C3`.

The two `A1` lines keep the relative order they were given in: change 4 was handed over before
change 5, so it is written first, even though the return-type change may read as the bigger news.
`Impact` is `1` because `1` is the lowest digit present.

## Final check before you commit

- Heading has `[version]`, a space-hyphen-space, and a `YYYY-MM-DD` date.
- `Impact:` line is directly under the heading and equals the lowest marker digit.
- Every change line starts `- [` and the marker is bracketed, two characters, letter then digit.
- Letters are only A, B, or C; digits are only 1, 2, or 3.
- Every `B` line describes a call whose arguments *and* return type a caller would read as
  unchanged; any change to what a call hands back is `A`. Re-read each `B` line once with only this
  question in mind.
- One line per pending change — none merged, none split, none dropped.
- Lines sorted ascending by marker; within each marker group, the original given order is intact —
  compare the group against your Step 2 numbers rather than trusting your eye.
- `<!-- stl-impact: v1 -->` is the last line of the entry.