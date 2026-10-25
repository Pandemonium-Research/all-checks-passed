---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project. It gives the exact house impact-log format — heading, impact line, tagged bullets, trailer — plus the rules for assigning each change its letter/digit code, so downstream tooling can parse the entry.
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

Older entries in the file predate this format and are inconsistent. Follow this document, not
the file.

## Choosing the letter

Ask the three questions in order and stop at the first "yes". That ordering is the precedence
rule: when a change could be argued into more than one bucket, the alphabetically earlier letter
wins.

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
at the first "yes"; the lowest applicable digit wins.

- **1 — breaking.** Caller code that used to work can now fail, or come back with a different
  result.
- **2 — compatible.** Additive, or a fix. Correct existing code keeps working unchanged.
- **3 — unobservable.** No caller can tell the difference at all.

Because the two axes are independent, every combination from `A1` to `C3` is legal and gets
used. A packaging or tooling change can still be breaking (`C1`) — dropping a supported runtime
or removing a distributed artifact is C by letter and 1 by digit. A new public name that nobody's
existing code can be affected by is `A2`. Do not let the letter pull the digit along with it, or
the other way round.

When a change genuinely sits on a boundary after these tests, take the earlier letter and the
lower digit. A reader warned unnecessarily is better off than one not warned at all.

## The impact line

`N` is the **lowest digit that appears anywhere in the entry**, regardless of letter. If any
bullet is a `1`, the line reads `Impact: 1`. If the lowest digit present is `2`, it reads
`Impact: 2`. Compute it after you have coded every bullet, not before.

## Bullet order

Sort bullets by code ascending — letter first, then digit:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Bullets sharing a code keep the relative order they were given to you. Never emit the bullets in
the order the changes happened to be listed.

## Writing the descriptions

One sentence per change, present tense, naming the affected symbol, module, or artifact in
backticks. Say what changed and, where it is not obvious, what it means for a caller. Keep any
"output is unchanged" style reassurance in the same sentence rather than adding a second bullet.

## Worked example

Given version `2.1.0`, date `2026-03-09`, and these pending changes, listed in arbitrary order:

- added a `parse_span()` helper to the package root → new public name, nobody breaks → `A2`
- `parse()` now raises `ParseError` instead of `ValueError` on malformed input → same signature,
  different observable result, existing callers can fail → `B1`
- switched the internal token buffer to a preallocated array, output identical → invisible → `C3`
- test suite now runs on Windows → tests only, nobody observes → `C3`

```
## [2.1.0] - 2026-03-09

Impact: 1

- [A2] Added `parse_span()` at the package root.
- [B1] `parse()` now raises `ParseError` rather than `ValueError` on malformed input.
- [C3] Switched the internal token buffer to a preallocated array. Output is identical.
- [C3] Extended the test suite to run on Windows.

<!-- stl-impact: v1 -->
```

## Before you hand it off

- Heading is `## [version] - date`, brackets on the version only, ISO date.
- Every bullet begins `- [` letter digit `] `.
- Letters and digits were chosen by their own ordered tests, independently.
- `Impact:` equals the lowest digit in the entry.
- Bullets sorted ascending by code.
- Final line is `<!-- stl-impact: v1 -->`, with nothing after it.