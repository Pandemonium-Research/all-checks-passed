---
name: impact-log
description: Step-by-step rules for writing one release notes entry — the heading line, the bracketed impact marker that leads each change line, the Impact summary, the required line order, and the parser trailer. Read this before adding notes for any new version.
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

### Step 2a — Pick the letter

Work down this list and stop at the **first** one that matches. That ordering is also the tie-break:
when a change could be argued into two letters, the earlier letter wins.

- **A — the exported surface changed.** Any change to what the package exports: a new public
  function, class, or constant; a renamed or removed export; a changed parameter list, default
  value, accepted type, or return type. If callers can see a difference by reading the signature,
  it is A.
- **B — the surface is identical, but existing calls behave differently at runtime.** Same names,
  same signatures, different results: corrected output, a different exception, different ordering,
  a fixed edge case.
- **C — everything else.** Build, packaging, CI, tooling, tests, documentation, and internal-only
  refactors or optimizations that no caller can detect.

Only A, B, and C exist. Inventing another letter makes the parser reject the file.

### Step 2b — Pick the digit

The digit is decided independently of the letter. Any letter can pair with any digit. Work down
this list and stop at the first match; as with letters, the lower digit wins a genuine tie.

- **1 — breaking.** Caller code that was correct and working can now fail, or can now get a
  different result. Removals, renames, narrowed or reordered parameters, changed defaults, changed
  behavior that correct code was relying on.
- **2 — compatible and observable.** Callers can notice the change, but correct existing code keeps
  working. This covers additions (new functions, newly accepted types, new optional arguments) and
  bug fixes. **A bug fix is 2, not 1**, even though output changes for code that was hitting the
  bug: the digit describes what happens to *correct* existing code.
- **3 — invisible.** No caller can observe any difference in behavior or result. Packaging, tests,
  docs, tooling, internal caching, and refactors land here.

Note the common pairings that catch people out: a newly added export is `A2`, not `A1` — adding
something breaks nobody. A widened accepted type on an existing argument is also `A2`, because the
signature changed but old calls still work. A behavior fix with an untouched signature is `B2`. A
packaging or test-layout change is `C3`.

If a change is genuinely ambiguous after applying the rules above, choose the more disruptive
reading — which is the same thing as choosing the lower letter and the lower digit. A reader warned
unnecessarily is better off than one not warned at all. This only settles real ties; it never
overrides an explicit rule above.

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

The finished entry:

```
## [2.1.0] - 2025-06-02
Impact: 1
- [A1] Removed the deprecated `Client.fetch_all()` alias; use `Client.fetch()` instead.
- [A2] Added a `timeout` keyword argument to `Client.__init__()`, defaulting to the previous behavior.
- [B2] `Client.get()` now retries on 503 responses.
- [C3] Moved the CI configuration from Travis to GitHub Actions.
<!-- stl-impact: v1 -->
```

The removal is `A1` (surface change, breaks callers). The new keyword argument is `A2` (surface
change, but old calls still work). The retry behavior is `B2` (same signature, different runtime
behavior, and it is a fix). The CI move is `C3`. The lines are sorted ascending by marker, and
`Impact` is `1` because `A1` is the lowest digit present.

## Final check before you commit

- Heading has `[version]`, a space-hyphen-space, and a `YYYY-MM-DD` date.
- `Impact:` line is directly under the heading and equals the lowest marker digit.
- Every change line starts `- [` and the marker is bracketed, two characters, letter then digit.
- Letters are only A, B, or C; digits are only 1, 2, or 3.
- One line per pending change — none merged, none split, none dropped.
- Lines sorted ascending by marker.
- `<!-- stl-impact: v1 -->` is the last line of the entry.