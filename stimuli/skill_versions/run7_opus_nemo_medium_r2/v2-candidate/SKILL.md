---
name: impact-log
description: Use this skill when writing the release notes / changelog entry for this project. It gives the exact house impact-log format — heading, impact line, coded bullets, trailer — and the ordered tests for assigning each change its letter (A/B/C) and digit (1/2/3), including the three calls people get wrong most often: bug fixes, invisible build work, and the order of bullets that share a code.
---

# Release notes: the impact-log format

Every release gets one entry in this format. Produce exactly the structure below and nothing
else — no extra headers, no "Version:" or "Date:" labels, no notes to the reader.

## The exact shape of an entry

```
## [X.Y.Z] - YYYY-MM-DD

Impact: N

- [A1] Description of the change.
- [B2] Description of the change.
- [C3] Description of the change.

<!-- stl-impact: v1 -->
```

Five literal requirements, in order:

1. **Heading.** Second level (`##`). Square brackets go around the version **only**, then a
   space, a hyphen, a space, then the date unbracketed. Version is the ordinary three-part form
   (`1.4.0`). Date is ISO year-month-day (`2026-08-14`), never localized.
   Correct: `## [1.4.0] - 2026-08-14`
   Wrong: `## [1.4.0 - 2026-08-14]`, `[1.4.0] - 2026-08-14`, `## [1.4] - Aug 14, 2026`
2. **Impact line.** Blank line, then `Impact: ` followed by a single digit. See below for which.
3. **Bullets.** Blank line, then one `- ` bullet per change. Each bullet starts with its code in
   square brackets — letter immediately followed by digit, no space, no colon — then a space,
   then a sentence describing the change. Correct: `- [B2] ...`. Wrong: `- B: ...`,
   `- [B] [2] ...`, `[B2] ...` with no bullet marker.
4. **Trailer.** Blank line, then the last line of the entry is the HTML comment
   `<!-- stl-impact: v1 -->`, exactly as written, angle brackets and all. A bare `stl-impact: v1`
   is not accepted — the parser rejects the file without the comment form.
5. Nothing after the trailer.

One bullet per change you were given: never merge two changes into one bullet, never split one
change across two bullets, and never invent a change that was not in the list.

Older entries in the file predate this format and are inconsistent. Follow this document, not
the file.

## Choosing the letter

Ask the three questions in order and stop at the first "yes". That ordering is the precedence
rule: when a change could honestly be argued into more than one bucket, the alphabetically
earlier letter wins.

- **A — public API.** Does the change alter the names, signatures, or types of anything the
  package exports? Adding, removing, renaming, or changing the parameters or return type of a
  public name is A.
- **B — behavior.** Signatures are untouched, but an existing call now does something
  observably different: different return value, different error, different side effect.
- **C — everything else.** Internal implementation, performance, build, packaging,
  dependencies, supported runtimes, tooling, tests, documentation. C is the fallback: if a
  change is invisible in both the API surface and the observable behavior of a call, it is C.

## Choosing the digit

Decided **independently of the letter**, by the same kind of ordered test. Ask in order and stop
at the first "yes".

- **1 — breaking.** The release deliberately takes something away or changes a promise: a public
  name removed or renamed, a parameter or return type changed incompatibly, documented behavior
  intentionally changed, a supported runtime or published artifact dropped. Code that was
  correct before this release can now fail, or quietly do something else.
- **2 — compatible.** Additive or corrective. Something new that callers can reach (a public
  name, a newly accepted argument type, a newly published artifact, a newly supported runtime),
  **or a bug fix** that makes an existing call finally do what it was always meant to do. Code
  that was correct before is still correct.
- **3 — unobservable.** Nobody outside the repository can tell the difference: same names, same
  return values, same errors, same published artifacts, same install steps.

Every combination from `A1` to `C3` is legal and gets used. A packaging or tooling change can be
breaking (`C1`) — dropping a supported runtime or removing a distributed artifact is C by letter
and 1 by digit. A new public name that nobody's existing code can be affected by is `A2`. Do not
let the letter pull the digit along with it, or the other way round.

### A bug fix is a 2, not a 1

A fix changes what a call returns, which sounds like the wording of 1. It is not. Digit 1 is for
breaking **correct** code; code that depended on the buggy output was depending on a defect.
Correcting mishandled input, a wrong result, a spurious exception, a dropped character, an
off-by-one — all of these are digit 2, with the letter chosen by the normal test (usually `B2`,
or `A2` if the fix also adds or widens a public name).

The only time a fix carries a 1 is when shipping it also required a deliberate incompatible
change — removing a parameter, say — and then it is that removal, not the fix, that earns the 1.
A deliberate redesign is different from a fix: `parse()` swapped from raising `ValueError` to
raising `ParseError` on purpose is `B1`, because working code that caught `ValueError` now fails.

### Invisible plumbing is a 3, not a 2

Refactors, internal caching, moved files, reorganized tests, CI changes, a switched build backend
or config format, dependency bumps with no user-facing effect — these are digit 3 even though
they are real improvements and even though they *add* things inside the repository. "Additive" in
digit 2 means additive to something a user can reach.

The test: could someone outside the repository write a command or a program whose result differs
before and after this change? If no, it is a 3. Migrating build machinery while the install
command and the published artifacts stay the same is `C3`. Publishing a wheel for a Python
version that previously had none is `C2`, because someone can now install where they could not.

### Boundaries

For letters, take the earlier letter when a change genuinely straddles two.

For digits, apply the tests literally; do not round down "to be safe". Choose 1 only when you can
name the correct, working code that this release breaks. If every change in a release is additive,
corrective, or invisible, the release simply has no 1 in it — and the entry should say so.

## The impact line

`N` is the **lowest digit that appears anywhere in the entry**, regardless of letter. If any
bullet is a `1`, the line reads `Impact: 1`. If the lowest digit present is `2`, it reads
`Impact: 2`. If every bullet is a `3`, it reads `Impact: 3`. Compute it after you have coded
every bullet, not before — and re-read it after any recode.

## Bullet order

Do this mechanically:

1. Number the changes 1, 2, 3 … in the order you were handed them.
2. Code each one.
3. Sort by code ascending — letter first, then digit:
   `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`
4. Break ties by the original number, ascending. Two `C3` bullets appear in the order the changes
   were given to you.

Never emit the bullets in the order the changes happened to be listed, and never reorder
same-code bullets on any other basis — not by importance, not by size, not by how the sentences
read next to each other.

## Writing the descriptions

One sentence per change. Name the affected symbol, module, or artifact in backticks. Describe the
change itself in the past tense (`Added …`, `Fixed …`, `Switched …`) or state the new behavior
with `now` (`` `parse()` now raises … ``). Say what changed and, where it is not obvious, what it
means for a caller. Keep any "results are unchanged" style reassurance in the same sentence
rather than adding a second bullet.

## Worked example: a release with a breaking change

Given version `2.1.0`, date `2026-03-09`, and these pending changes in the order listed:

1. `parse()` now raises `ParseError` instead of `ValueError` on malformed input → same signature,
   deliberate change, existing callers can fail → `B1`
2. test suite now runs on Windows → tests only, nobody outside observes → `C3`
3. added a `parse_span()` helper to the package root → new public name, nobody breaks → `A2`
4. switched the internal token buffer to a preallocated array, output identical → invisible → `C3`

Lowest digit is 1. The two `C3` bullets keep their given order: tests (2) before buffer (4).

```
## [2.1.0] - 2026-03-09

Impact: 1

- [A2] Added `parse_span()` at the package root.
- [B1] `parse()` now raises `ParseError` rather than `ValueError` on malformed input.
- [C3] Extended the test suite to run on Windows.
- [C3] Switched the internal token buffer to a preallocated array. Output is identical.

<!-- stl-impact: v1 -->
```

## Worked example: a release with no breaking change

Given version `2.1.1`, date `2026-04-02`, and these pending changes in the order listed:

1. `parse()` no longer drops a trailing separator, which it was never meant to drop → a fix, not
   a redesign → `B2`
2. switched the build backend from `setuptools` to `hatchling`; install command and published
   wheel are unchanged → nobody outside can tell → `C3`
3. wheels are now published for the newest Python release → users can install where they could
   not → `C2`
4. added a `strict=` keyword to `parse()`, defaulting to the old behavior → signature grew,
   nothing breaks → `A2`

No bullet is a 1, so the lowest digit present is 2.

```
## [2.1.1] - 2026-04-02

Impact: 2

- [A2] Added a `strict=` keyword to `parse()`, defaulting to the previous behavior.
- [B2] `parse()` no longer drops a trailing separator.
- [C2] Published wheels for the newest Python release.
- [C3] Switched the build backend to `hatchling`. Installation and the published wheel are unchanged.

<!-- stl-impact: v1 -->
```

## Before you hand it off

- Heading is `## [version] - date`, brackets on the version only, ISO date.
- Every bullet begins `- [` letter digit `] `, one bullet per given change.
- Letters and digits were chosen by their own ordered tests, independently.
- Every bug fix is a 2. Every change no outsider can detect is a 3.
- Any bullet coded 1 has a namable piece of correct code that it breaks.
- `Impact:` equals the lowest digit actually present in the bullets.
- Bullets sorted ascending by code; same-code bullets still in the order you were given them.
- Final line is `<!-- stl-impact: v1 -->`, with nothing after it.