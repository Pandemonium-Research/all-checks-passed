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
  formatting mistake.
- The date is always year-month-day, zero-padded (`2025-03-09`), never a localized form.

Older entries further down the file predate this practice and are inconsistent. Do not copy their
shape; follow the skeleton above.

## Step 2 — Write one line per change

One line per pending change, in the order you were given them for now (Step 3 reorders them). Never
merge two changes into one line, and never split one change across two lines.

Each line is a hyphen, a space, the marker in square brackets, a space, then the description:

```
- [A2] Added `retry_after()`, exported at the package root.
```

The marker **leads** the line — it comes immediately after the hyphen, before the words. It is never
placed at the end of the line, and it is never written bare (`A2 - ...` is wrong; `[A2]` is right).
Review comments call this marker a "tag", a "code", or an "impact marker" — all the same thing.

The description is the change stated in plain prose, one sentence or two, ending with a period.

### The letter and the digit answer different questions

This is the mistake that costs entries most often, so settle it before you tag anything:

- The **letter** says **what kind of thing changed** — the exported surface, runtime behavior, or
  everything else. It says nothing about how much it hurts.
- The **digit** says **how much it hurts callers** — breaking, compatible, or invisible. It says
  nothing about what kind of change it was.

They are chosen independently, and every one of the nine combinations is legal. A change can break
every user of the package and still be `C1`, because breaking is a digit, not a letter. Never
promote a change to `A` because it is severe, and never demote one to a higher digit because it is
"only" packaging.

### Step 2a — Pick the letter

Work down this list and stop at the **first** one that matches. Judge only *what changed*, never how
disruptive it is.

- **A — the exported surface changed.** Any change to what the package exports or to the shape of
  an export: a new public function, class, or constant; a renamed or removed export; a changed
  parameter list, default value, accepted type, **or return type**. If a caller can see a difference
  by reading the signature — including what comes back out of the call — it is A.

  The return side counts as surface. If a function keeps its name and its parameters but now hands
  back a different *kind* of object — a list where it used to return a string, an object where it
  used to return a dict, a tuple where it used to return a list, nothing where it used to return a
  value — that is A, not B. "The arguments didn't change" is not enough to make something B.

- **B — the surface is identical, but existing calls behave differently at runtime.** Same names,
  same parameters, same return type, different results: corrected values, a different exception,
  different ordering, a fixed edge case. Before choosing B, confirm that someone reading the full
  signature — arguments *and* return type — would see nothing new. A different value of the same
  type is B; a different type or shape is A.

- **C — everything else.** Build, packaging, CI, tooling, tests, documentation, and internal-only
  refactors or optimizations that no caller can detect.

  C also covers **what the project supports**: dropping or adding a supported language runtime or
  Python version, dropping a platform, raising a minimum dependency version, or changing install
  requirements. These live in packaging metadata, not in the exported surface, so the letter is C
  even when the change locks users out entirely — the harm is recorded by the digit (`C1`).

Only A, B, and C exist. Inventing another letter makes the parser reject the file.

### Step 2b — Pick the digit

Decide the digit on its own, after the letter, without letting the letter influence it. Work down
this list and stop at the first match; the lower digit wins a genuine tie.

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
| Function returns a different type or shape | `A1` | Return type is surface, and callers break. |
| Behavior fix, signature untouched | `B2` | Runtime-only, and fixes are 2. |
| Behavior change correct code relied on | `B1` | Runtime-only, but correct code changes result. |
| Dropped runtime/platform support, raised minimum dependency | `C1` | Packaging metadata, but it locks callers out. |
| CI, test layout, docs, internal refactor | `C3` | Nothing a caller can see. |

If a change is genuinely ambiguous after applying the rules above — and only then — pick the lower
**digit**, so a reader is warned rather than left unwarned. That tie-break applies to digits only.
The letter is never chosen for severity; it comes from the first matching entry in the Step 2a list.

## Step 3 — Sort the lines by marker, ascending

The lines are not left in the order the changes were handed to you. Sort them upward by marker:
letter first, then digit. So `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.

Lines sharing the same marker keep the relative order they were given in.

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
6. Raised the minimum supported Python version to 3.10.

The finished entry:

```
## [2.1.0] - 2025-06-02
Impact: 1
- [A1] Removed the deprecated `Client.fetch_all()` alias; use `Client.fetch()` instead.
- [A1] `Client.list_items()` returns a tuple rather than a list.
- [A2] Added a `timeout` keyword argument to `Client.__init__()`, defaulting to the previous behavior.
- [B2] `Client.get()` now retries on 503 responses.
- [C1] Raised the minimum supported Python version to 3.10.
- [C3] Moved the CI configuration from Travis to GitHub Actions.
<!-- stl-impact: v1 -->
```

Reading the markers back:

- The removal is `A1` — surface change, breaks callers.
- The tuple return is `A1`, not `B`-anything: the arguments are untouched, but the return type is
  part of the exported surface, and correct code that indexed or mutated the old list breaks.
- The new keyword argument is `A2` — surface change, old calls still work.
- The retry is `B2` — identical signature and return type, different runtime behavior, and it is
  a fix.
- The Python floor is `C1`, not `A1`: nothing about the exported surface moved, so the letter is C;
  callers on the old version are locked out, so the digit is 1.
- The CI move is `C3`.

The two `A1` lines keep the relative order they were given in (change 4 before change 5). `Impact`
is `1` because `1` is the lowest digit present.

## Final check before you commit

- Heading has `[version]`, a space-hyphen-space, and a `YYYY-MM-DD` date.
- `Impact:` line is directly under the heading and equals the lowest marker digit.
- Every change line starts `- [` and the marker is bracketed, two characters, letter then digit.
- Letters are only A, B, or C; digits are only 1, 2, or 3.
- Every letter was chosen from *what changed*, not from how bad it is — no change was tagged `A`
  just because it breaks callers, and no breaking packaging or support change was tagged anything
  but `C1`.
- Every `B` line has a signature *and* a return type that a caller would read as unchanged; any
  change to what a call returns is `A`.
- One line per pending change — none merged, none split, none dropped.
- Lines sorted ascending by marker, with same-marker lines in their original relative order.
- `<!-- stl-impact: v1 -->` is the last line of the entry.