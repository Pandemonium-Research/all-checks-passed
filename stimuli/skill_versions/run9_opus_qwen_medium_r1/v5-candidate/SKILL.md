---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project — given a version, a date, and a list of pending changes — so the entry matches the team's house impact-log format and the parser accepts it.
---

# Release notes — impact-log format

Every release gets one entry in the impact-log format below. Follow this document, not the
older entries sitting in the file: some of them predate the format and are inconsistent.

## Order of work

Write the entry in this order. The impact line depends on the bullets, so it cannot be written
first, even though it appears near the top.

1. Give every pending change **exactly one** bullet, and give every bullet a tag. Do not merge two
   changes into one bullet, do not drop a change because it looks minor, and do not invent changes
   that were not handed to you. The number of bullets equals the number of pending changes.
2. Sort the bullets by tag, ascending.
3. Copy the digit out of the now-first bullet into the `Impact:` line.
4. Add the heading above it and the trailer below the bullets.

## The shape of an entry

Copy this skeleton exactly, including the punctuation and the final HTML comment:

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: <digit copied from the first bullet>
- [<letter><digit>] <one change, one sentence or two>
- [<letter><digit>] <one change, one sentence or two>
<!-- stl-impact: v1 -->
```

Four required parts, in this order, with nothing else between them — no blank lines, no extra
prose, no `### Added` / `### Fixed` subsections:

1. **Heading** — level two (`##`). The version exactly as given, in square brackets, three numeric
   parts, then a space-hyphen-space, then the date exactly as given, as `YYYY-MM-DD`. Never a
   localized date.
2. **Impact line** — directly beneath the heading, no blank line needed. The word `Impact`, a
   colon, a space, and one digit.
3. **Bullets** — one per change, each starting with its tag in square brackets.
4. **Trailer** — the literal line `<!-- stl-impact: v1 -->`, as the very last line of the entry,
   below the bullets. It must be a real HTML comment: the `<!--` and `-->` are part of it.
   Writing the bare text `stl-impact: v1` is a common mistake and the parser rejects the file
   for it.

## Tags

Each bullet starts with a tag: one capital letter, one digit, no space between them, wrapped in
square brackets, before the text. Only A, B, and C are valid letters; only 1, 2, and 3 are valid
digits. Do not invent other letters.

### The letter — what part of the project the change touches

Ask the two questions in order, and stop at the first yes:

1. Does the set of exported names, or the signature of an exported name, change? → **A**
2. Otherwise, does an existing call do something different that a caller can observe? → **B**
3. Neither → **C**

| Letter | Use it when |
| --- | --- |
| **A** | The public API changes: anything the package exports is added, removed, renamed, or has its signature, accepted argument types, defaults, or return type changed. A brand-new exported function is an A. |
| **B** | The runtime behavior of an existing call changes while its signature stays identical: corrected results, changed rules for interpreting input, a different exception or error message, a changed side effect. |
| **C** | Everything else: build, packaging, dependencies, tooling, CI, tests, documentation — and internal implementation work (refactors, caching, performance, import-time work) that leaves both the public API and its observable behavior alone. |

A performance or internal-refactor change is a **C**, not a B, when callers get the same results
as before. B is only for changes a caller can actually observe in what a call does.

### The digit — how much it can cost the person upgrading

| Digit | Use it when |
| --- | --- |
| **1** | Breaking. Caller code that was correct before can now fail, or return a different result for the same input: a removal, a rename, a narrowed or reordered signature, a changed default, changed semantics or changed rules for interpreting input. |
| **2** | Compatible. Something is added, widened, deprecated-with-warning, or fixed where the old output was plainly wrong, and correct existing code keeps working unchanged. Changes to what a user installs or receives are 2: a runtime dependency added, dropped, or vendored; a new file shipped inside the package; changed package metadata a user can inspect. |
| **3** | Invisible. Nothing an installed copy of the package contains, requires, or does is different: internal refactors, performance work, the test suite and the test runner, CI config, dev-only dependencies and dev tooling, prose docs, packaging moves that leave installation and behavior identical. |

**Adding something new is a 2, never a 1.** A new exported function is `[A2]`. A widened accepted
type is `[A2]`. Only the removal or alteration of something callers already relied on is a 1.

#### Telling 1 from 2 on B-letter work

A B bullet changes what an existing call does, so the digit turns on one question: **was the old
result defensible?**

- The old result was plainly wrong — a crash, a malformed string, an off-by-one, a value nobody
  would have wanted — and the new one is the obviously intended answer → **2**. Nobody depended on
  the broken output.
- The old result was a reasonable answer under the old rules, and the release changes the rules so
  the same input now yields a different answer → **1**. Rewording it as an improvement does not
  change that: correct caller code gets a different result than it did yesterday.

Phrases like "now treats X as …", "now counts/splits/normalizes X differently", "so results change
for input containing X" describe a rules change, not a bug fix. Tag those `[B1]`. The give-away is
the sentence you just wrote about the change: if it has to warn the reader that output changes for
some inputs, the digit is 1.

The same test applies to a `1` arriving without any API change: a release can be `Impact: 1` on the
strength of a lone `B1`, with no `A1` anywhere.

#### Telling 2 from 3 on C-letter work

Ask one question: **does this change the code, data, or dependencies a user installs?**

- Yes → **2**. The user can see it in their installed tree or their dependency graph: a runtime
  dependency added, dropped, vendored, or replaced; a file the package now ships (a marker file
  like `py.typed`, bundled data, a certificate bundle); package metadata they can inspect.
- No — it only touches the repository, the test suite, or the dev/CI environment → **3**. Work a
  user never receives when they install the package is invisible, however large it was.

So switching or upgrading a test runner, linter, formatter, or other dev-only tool is a `C3`,
while changing a dependency the package imports at runtime, or shipping a new file inside the
package, is a `C2`.

Documentation is always a **3**, wherever it lives — README, docs pages, and docstrings or added
docstring examples inside shipped modules alike. Prose is not code, data, or a dependency: editing
it changes nothing the package requires or does.

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

The digit scale runs **downward**: 1 is the most disruptive, 3 the least. The impact line reports
the most disruptive thing in the release, so it is the **lowest** digit appearing on any bullet —
never the highest, never the last bullet's digit, and never a count of bullets or of distinct tags.

Mechanically, after sorting: **copy the digit from the first bullet.** That bullet holds the lowest
digit by construction. No judgment is involved.

To check by hand, read the digits and ignore the letters:

- Any `1` anywhere → `Impact: 1`, even if every other bullet is a 2 or a 3.
- No `1`, but at least one `2` → `Impact: 2`. One lone `2` among a dozen `3`s still makes the line
  read 2; the 3s never raise it.
- Every bullet is a `3` → `Impact: 3`.

`Impact: 3` is a strong claim — it says nothing a user installs, requires, or runs is different in
any way. A release that merely *feels* small or routine is not a 3 on that basis. If a single
shipped file, runtime dependency, bug fix, or addition appears anywhere in the list, the line is 2
at most.

## Writing the bullet text

One change per bullet. Say what changed and, where it matters, what the reader has to do or can
ignore — "Existing calls are unaffected", "Pass it as a keyword instead". Name the affected
functions in backticks. Keep it to a sentence or two.

## Worked examples

### A release containing a breaking API change

Pending changes for version 2.4.0, released 2025-11-03: a rewritten internal tokenizer with
identical output; a new `parse_range()` helper exported at the package root; `parse_date()`
dropping positional `tz`; the `six` runtime dependency removed; `format_date()` fixed to pad
single-digit days.

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

The line reads `1` because an `A1` is present; the four higher digits below it change nothing.
`format_date()` is a `B2` because `2025-1-4` was simply wrong — no caller wanted it.

### A release broken only by a behavior change

Pending changes for version 2.5.0, released 2026-01-14: `split_terms()` now treats underscores as
separators, so terms containing them split differently; the project moved from `unittest` to
`pytest`.

```
## [2.5.0] - 2026-01-14
Impact: 1
- [B1] `split_terms()` now treats underscores as separators, so input containing them splits into more terms than before.
- [C3] Switched the test runner from `unittest` to `pytest`.
<!-- stl-impact: v1 -->
```

The line reads `1` with no `A` bullet at all: the separator rule changed, so code that was correct
before now gets a different result. The test-runner swap is `C3` — users never install it.

### A quiet release with no breaking change

Pending changes for version 2.4.1, released 2025-11-20: a bundled CA certificate file now shipped
inside the package; the CI matrix extended to a new Python version; connection setup made lazy,
with identical results; new usage examples in the `connect()` docstring.

```
## [2.4.1] - 2025-11-20
Impact: 2
- [C2] Ship a bundled CA certificate file inside the package.
- [C3] Extended the CI matrix to the newest Python release.
- [C3] Connections are now opened lazily. Results are unchanged.
- [C3] Added usage examples to the `connect()` docstring.
<!-- stl-impact: v1 -->
```

The line reads `2`, not `3`, because a `C2` is present — even though nothing here breaks anyone and
the release is otherwise routine. The three `C3`s below it do not raise the line; the docstring
edit stays a 3 even though it ships, because it is prose.

## Before you finish, check

- [ ] Heading is `## [x.y.z] - YYYY-MM-DD`, with the version and date exactly as handed to you.
- [ ] One bullet per pending change — none merged, dropped, or invented.
- [ ] Every bullet has a bracketed letter-digit tag from A/B/C and 1/2/3.
- [ ] Additions are 2, not 1; unobservable internal or perf work is C3, not B.
- [ ] Any bullet whose text warns that results or output change for some input is a **1**, not a 2
      — unless the old output was plainly a bug.
- [ ] Dev-only tooling, test-runner, CI, and documentation changes (docstrings included) are 3;
      shipped files and runtime dependencies are 2.
- [ ] Bullets are sorted by tag, ascending.
- [ ] `Impact:` is the same digit as the first bullet after sorting. Re-read every bullet digit and
      confirm no smaller one appears further down — in particular, that the line is not 3 while a
      `2` sits somewhere in the list.
- [ ] The last line is `<!-- stl-impact: v1 -->`, comment markers included.