---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project — given a version, a date, and a list of pending changes — so the entry matches the team's house impact-log format and the parser accepts it.
---

# Release notes — impact-log format

Every release gets one entry in the impact-log format below. Follow this document, not the
older entries sitting in the file: some of them predate the format and are inconsistent.

## The shape of an entry

Copy this skeleton exactly, including the punctuation and the final HTML comment:

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: <digit>
- [<letter><digit>] <one change, one sentence or two>
- [<letter><digit>] <one change, one sentence or two>
<!-- stl-impact: v1 -->
```

Four required parts, in this order, with nothing else between them:

1. **Heading** — level two (`##`). Version in square brackets, three numeric parts, then a
   space-hyphen-space, then the date as `YYYY-MM-DD`. Never a localized date.
2. **Impact line** — directly beneath the heading, no blank line needed. The word `Impact`, a
   colon, a space, and one digit.
3. **Bullets** — one per change, each starting with its tag in square brackets.
4. **Trailer** — the literal line `<!-- stl-impact: v1 -->`, as the very last line of the entry,
   below the bullets. It must be a real HTML comment: the `<!--` and `-->` are part of it.
   Writing the bare text `stl-impact: v1` is the single most common mistake and the parser
   rejects the file for it.

## Tags

Each bullet starts with a tag: one capital letter, one digit, no space between them, wrapped in
square brackets, before the text. Only A, B, and C are valid letters; only 1, 2, and 3 are valid
digits. Do not invent other letters.

### The letter — what part of the project the change touches

| Letter | Use it when |
| --- | --- |
| **A** | The public API changes: anything the package exports is added, removed, renamed, or has its signature, accepted argument types, defaults, or return type changed. A brand-new exported function is an A. |
| **B** | The runtime behavior of an existing call changes while its signature stays identical: corrected results, a different exception or error message, a changed side effect. |
| **C** | Everything else: build, packaging, dependencies, tooling, CI, tests, documentation — and internal implementation work (refactors, caching, performance, import-time work) that leaves both the public API and its observable behavior alone. |

A performance or internal-refactor change is a **C**, not a B, when callers get the same results
as before. B is only for changes a caller can actually observe in what a call does.

### The digit — how much it can cost the person upgrading

| Digit | Use it when |
| --- | --- |
| **1** | Breaking. Caller code that was correct before can now fail, or return a different result for the same input: a removal, a rename, a narrowed or reordered signature, a changed default, changed semantics. |
| **2** | Compatible. Something is added, widened, fixed, or deprecated-with-warning, and correct existing code keeps working unchanged. Bug fixes are 2, even though the buggy output changes. Changes to what users install or receive are 2: a runtime dependency added, dropped, or vendored; a new file shipped inside the package; changed package metadata a user can inspect. |
| **3** | Invisible. Nothing an installed copy of the package contains, requires, or does is different: internal refactors, performance work, the test suite and the test runner, CI config, dev-only dependencies and dev tooling, docstrings and prose docs, packaging moves that leave installation and behavior identical. |

**Adding something new is a 2, never a 1.** A new exported function is `[A2]`. A widened accepted
type is `[A2]`. Only the removal or alteration of something callers already relied on is a 1.

#### Telling 2 from 3 on C-letter work

Ask one question: **does this change what an installed copy of the package contains or requires?**

- Yes → **2**. The user can see it in their installed tree or their dependency graph.
- No, it only touches the repository, the test suite, or the dev/CI environment → **3**. Work that
  a user never receives when they install the package is invisible, no matter how large it was.

So switching or upgrading a test runner, linter, or other dev-only tool is a `C3`, while changing a
dependency the package actually imports at runtime, or shipping a new file inside the package, is a
`C2`.

### When a change could take two tags

Precedence applies only when a change genuinely sits in two categories at once — not as an excuse
to escalate a change out of the category it plainly belongs in.

- Letters take precedence alphabetically: a change that is both an API change and a behavior
  change is tagged **A**.
- Digits take precedence low to high: a change that is arguably both compatible and invisible is
  tagged **2**.

Judge the letter and the digit independently; any of the nine combinations is legal.

## Ordering

**Sort the bullets by their tag, ascending**: A before B before C, and within a letter, 1 before 2
before 3. Do not leave them in the order the pending changes were handed to you. Bullets that share
the same tag keep the relative order they were given in.

## The impact line

The impact line reports the worst thing in the release. Because a lower digit means a more
disruptive change, **the worst thing in the release is the *lowest* digit that appears on any
bullet** — so the impact line is the minimum of the bullet digits, never the maximum.

Mechanically, after sorting: **copy the digit from the first bullet.** That bullet holds the lowest
digit by construction. There is no judgment involved, and the number is never the count of bullets
or the number of distinct tags.

Work through the digits present, ignoring letters:

- Any `1` anywhere → `Impact: 1`, even if every other bullet is a 2 or a 3.
- No `1`, but at least one `2` → `Impact: 2`. A release of, say, two `C2`s and three `C3`s reads
  `Impact: 2` — the 3s do not raise it, and the last bullet's digit is irrelevant.
- Every bullet is a `3` → `Impact: 3`. This is the only way the line reads 3.

## Writing the bullet text

One change per bullet. Say what changed and, where it matters, what the reader has to do or can
ignore — "Existing calls are unaffected", "Pass it as a keyword instead". Name the affected
functions in backticks. Keep it to a sentence or two.

## Worked example

Pending changes for version 2.4.0, released 2025-11-03: a rewritten internal tokenizer with
identical output; a new `parse_range()` helper exported at the package root; `parse_date()`
dropping positional `tz`; the `six` dependency removed; `format_date()` fixed to pad single-digit
days.

```
## [2.4.0] - 2025-11-03
Impact: 1
- [A1] `parse_date()` no longer accepts `tz` positionally. Pass it as a keyword argument.
- [A2] Added `parse_range()` for start/end pairs, exported at the package root.
- [B2] `format_date()` now zero-pads single-digit days, fixing output like `2025-1-4`.
- [C2] Dropped the `six` dependency.
- [C3] Rewrote the internal tokenizer. Output is unchanged.
<!-- stl-impact: v1 -->
```

The impact line is `1` because an `A1` is present — the four higher digits below it change nothing.

## Before you finish, check

- [ ] Heading is `## [x.y.z] - YYYY-MM-DD`.
- [ ] Every bullet has a bracketed letter-digit tag from A/B/C and 1/2/3.
- [ ] Additions are 2, not 1; unobservable internal or perf work is C3, not B.
- [ ] Dev-only tooling, test-runner, and CI changes are 3; changes to shipped files or runtime
      dependencies are 2.
- [ ] Bullets are sorted by tag, ascending.
- [ ] `Impact:` equals the **lowest** digit used in any bullet — the same digit as the first bullet
      after sorting. Re-read the bullets and confirm no smaller digit appears anywhere.
- [ ] The last line is `<!-- stl-impact: v1 -->`, comment markers included.