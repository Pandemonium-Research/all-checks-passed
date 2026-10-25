---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project. It defines the house impact-log format — the version heading, the Impact summary line, the [letter+digit] tag on every bullet, the bullet sort order, and the required HTML-comment trailer — so that downstream tooling can parse the entry.
---

# Release notes (impact-log format)

Every release gets one entry. An entry has exactly four parts, in this order:

1. A version heading
2. An `Impact:` line
3. One tagged bullet per change, sorted
4. The trailer comment, as the last line

Do not imitate older entries in the file; several predate this format and are wrong.

## The shape of an entry

```
## [X.Y.Z] - YYYY-MM-DD
Impact: N
- [T] <one sentence describing the change>
- [T] <one sentence describing the change>
<!-- stl-impact: v1 -->
```

Blank lines between the four parts are optional and change nothing.

## 1. Heading

Second-level heading. Version in square brackets, three numeric parts, then a space, a hyphen, a space, then the date in `YYYY-MM-DD` form. Never a localized date.

## 2. Impact line

The word `Impact`, a colon, a space, and a single digit: **the lowest digit that appears on any bullet in this entry**. Lower means more severe, so this line reports the worst change in the release. Write this line only after you have tagged every bullet.

## 3. Bullets

One bullet per change. Each begins with a tag in square brackets — one letter, then one digit, no space between them — followed by a space and the description.

### Choosing the letter

Ask what kind of thing changed.

- **A — the public API.** The names, signatures, or types of anything the package exports changed. This includes adding a new export, removing or renaming one, adding or reordering parameters, changing a default, and **widening or narrowing which types a parameter accepts or a function returns**. A type change is still an A even when it is fully backward compatible.
- **B — runtime behavior only.** An existing call keeps exactly the same name, signature, and accepted/returned types, but what it *does* changed: different return value, different error raised, different side effect. Bug fixes to the logic of an existing function normally land here.
- **C — everything a caller never imports.** Build, packaging, tooling, CI, tests, documentation, and internal refactors that leave the public surface and its behavior untouched.

If a change fits more than one letter, take the earliest letter alphabetically: A beats B, B beats C. A new exported function whose body also does something clever is an A, not a B.

### Choosing the digit

The digit is decided independently of the letter — any letter can carry any digit. Ask what happens to code that already exists and already works.

- **1 — breaking.** Caller code that used to work can now fail, or can come back with a different result. Removals, renames, required-parameter additions, and behavior or bug fixes that change the value returned for inputs that previously returned something all belong here.
- **2 — compatible.** Nothing that already worked changes. Purely additive work is the common case: a new exported function, a new optional parameter, a newly accepted argument type. A fix is a 2 only when it affects cases that were already failing or raising, so that no previously-working call sees a new result.
- **3 — unobservable.** No caller can tell the difference at all: internal caching that returns identical results, refactors, packaging, tooling, tests, docs.

If a change fits more than one digit, take the lowest.

Adding something new is never a 1. "New" and "breaking" are different questions: a brand-new export is `A2`, because no existing call can be affected by a name that did not exist before.

### Sorting

Sort bullets by their tag, ascending — letter first, then digit: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Do not leave them in the order the changes were handed to you. Bullets sharing a tag keep their given order relative to each other.

## 4. Trailer

The last line of the entry is an HTML comment, written out in full, including the angle brackets and dashes:

```
<!-- stl-impact: v1 -->
```

The bare text `stl-impact: v1` is not valid and the parser rejects the file. Nothing may come after this line — not a bullet, not a blank note, nothing.

## Worked example

Given version `1.4.0`, date `2026-03-02`, and these pending changes, listed in arbitrary order:

- fixed `parse_duration` so `"1h30m"` now returns 5400 instead of 3600
- moved the test suite from `unittest` to `pytest`
- added a new exported helper `parse_duration_list`
- `format_duration` now also accepts an `int` where it previously required a `float`

The entry is:

```
## [1.4.0] - 2026-03-02
Impact: 1
- [A2] Added `parse_duration_list()` for parsing several durations at once, exported at the package root.
- [A2] `format_duration` now accepts an `int` as well as a `float`. Existing calls are unaffected.
- [B1] `parse_duration` now counts the minutes component in compound values; `"1h30m"` returns 5400 rather than 3600.
- [C3] Moved the test suite to `pytest`. No packaged code changed.
<!-- stl-impact: v1 -->
```

Note how each tag was reached: the new helper is a new export (A) and additive (2); the widened argument type is a type change (A) that breaks nothing (2); the fix leaves the signature alone (B) but changes a value callers were already getting (1); the test move is invisible to callers (C, 3). `Impact: 1` because `B1` is the lowest digit present.

## Before you finish

- Heading is `## [X.Y.Z] - YYYY-MM-DD`.
- Every bullet has a tag, and every tag uses A, B, or C — never an invented letter.
- No additive-only change carries a `1`.
- Bullets are sorted ascending by tag.
- `Impact:` matches the lowest digit on the bullets above.
- The final line is `<!-- stl-impact: v1 -->`, angle brackets included, with nothing after it.

Only when the rules above genuinely leave you split between two tags should you take the more disruptive one. That tie-breaker is not a licence to escalate a change you have already classified.