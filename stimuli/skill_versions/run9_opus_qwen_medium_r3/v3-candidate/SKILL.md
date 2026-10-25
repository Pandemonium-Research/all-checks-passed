---
name: impact-log
description: Use this skill whenever you write a release-notes or changelog entry for this project. It defines the house impact-log format and the exact procedure for producing an entry — the version heading, the `Impact:` summary line, the `[letter+digit]` tag on every bullet, the tag-only sort with given-order tie-breaking, and the required HTML-comment trailer that downstream tooling parses.
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
- [T] <description of the change>
- [T] <description of the change>
<!-- stl-impact: v1 -->
```

Blank lines between the four parts are optional and change nothing.

## The procedure

**Step 0 — Number the pending changes as they were handed to you.** Write `1, 2, 3, …` down the list in the order you received it, before you think about tags at all. That order is arbitrary and means nothing on its own, but it is the tie-breaker in step 3, so capture it first.

**Step 1 — Write one bullet per change,** leaving them in the given order for now and keeping each change's number attached to its bullet.

**Step 2 — Tag every bullet** with a letter and a digit.

**Step 3 — Sort the bullets by tag only,** breaking ties with the step-0 numbers.

**Step 4 — Write the `Impact:` line** from the tags you assigned.

**Step 5 — Add the trailer** as the last line.

## 1. Heading

Second-level heading. Version in square brackets, three numeric parts, then a space, a hyphen, a space, then the date in `YYYY-MM-DD` form. Never a localized date.

## 2. Impact line

The word `Impact`, a colon, a space, and a single digit: **the lowest digit that appears on any bullet in this entry**. Lower means more severe, so this line reports the worst change in the release. Write this line only after you have tagged every bullet.

## 3. Bullets

One bullet per change — always exactly one. Never merge two pending changes into a single bullet, even when they touch the same function or the same file, and never split one change across two bullets. When you are done, the number of bullets must equal the number of pending changes you were handed, with none dropped.

Each bullet begins with a tag in square brackets — one letter, then one digit, no space between them — followed by a space and the description. A description is normally one sentence; a short second sentence saying what callers do *not* have to do is fine.

### Choosing the letter

Ask what kind of thing changed.

- **A — the public API.** The names, signatures, or types of anything the package exports changed. This includes adding a new export, removing or renaming one, adding or reordering parameters, changing a default, and **widening or narrowing which types a parameter accepts or a function returns**. A type change is still an A even when it is fully backward compatible.
- **B — runtime behavior only.** An existing call keeps exactly the same name, signature, and accepted/returned types, but what it *does* changed in a way a caller can observe: a different return value, a different error raised, a different visible side effect. Bug fixes to the logic of an existing function normally land here.
- **C — everything a caller never imports.** Build, packaging, tooling, CI, tests, documentation, and internal refactors that leave the public surface and its behavior untouched. Work done *inside* a function callers do import is still C when the caller cannot observe it: caching that returns identical results, a rewritten internal algorithm with identical outputs, moved private helpers.

If a change fits more than one letter, take the earliest letter alphabetically: A beats B, B beats C. A new exported function whose body also does something clever is an A, not a B.

### Choosing the digit

The digit is decided independently of the letter — any letter can carry any digit. Ask what happens to code that already exists and already works.

- **1 — breaking.** Caller code that used to work can now fail, or can come back with a different result. Removals, renames, required-parameter additions, and behavior or bug fixes that change the value returned for inputs that previously returned something all belong here.
- **2 — compatible.** Nothing that already worked changes. Purely additive work is the common case: a new exported function, a new optional parameter, a newly accepted argument type. A fix is a 2 only when it affects cases that were already failing or raising, so that no previously-working call sees a new result.
- **3 — unobservable.** No caller can tell the difference at all: internal caching that returns identical results, refactors, packaging, tooling, tests, docs.

If a change fits more than one digit, take the lowest.

Adding something new is never a 1. "New" and "breaking" are different questions: a brand-new export is `A2`, because no existing call can be affected by a name that did not exist before.

A fix that returned a wrong value is a 1, not a 2. If the old call returned something — even something bad — a caller was getting that value and will now get a different one. Only a fix to calls that used to raise, crash, or hang is a 2.

### Sorting

**The sort key is the tag and nothing else.** The words in the description are never part of the sort key.

Work it like this:

1. Walk the tag values in ascending order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
2. For each tag, scan your step-0 numbered list from top to bottom and emit every bullet carrying that tag as you meet it.

That makes the sort stable: bullets sharing a tag come out in the order the changes were handed to you. If change #6 and change #2 both end up `C3`, the entry shows #6 first.

Do not sort the finished lines as text. A text sort looks like it works — it does put `A` before `B` — but it silently reorders bullets that share a tag into alphabetical order by description, and that is wrong. Inside a tag group, nothing about the bullet's wording may move it: not alphabetical order, not putting all the "Added …" bullets first, not which change seems more important, not grouping related functions or related files together, not making the group read better.

## 4. Trailer

The last line of the entry is an HTML comment, written out in full, including the angle brackets and dashes:

```
<!-- stl-impact: v1 -->
```

The bare text `stl-impact: v1` is not valid and the parser rejects the file. Nothing may come after this line — not a bullet, not a blank note, nothing.

## Worked example

Given version `2.1.0`, date `2026-05-14`, and these pending changes in the arbitrary order they arrived. Number them first:

1. `retry()` no longer retries on `KeyboardInterrupt`; it propagates the exception instead
2. rewrote the internal scheduler; timings and results are identical
3. added an optional `backoff_jitter` keyword to `retry()`
4. `Policy.max_attempts` now accepts `None` as well as `int`
5. switched CI from Travis to GitHub Actions

Tag each one where it stands:

- #1 — same name, same signature, same types, but an existing call now raises where it used to return: `B1`.
- #2 — internal rewrite with identical observable results: `C3`.
- #3 — a new optional parameter is a signature change (`A`) that no existing call can notice (`2`): `A2`.
- #4 — a widened parameter type is still an API change (`A`), and nothing that worked stops working (`2`): `A2`.
- #5 — CI only: `C3`.

Now walk the tags in ascending order, taking each group in numbered order — `A2` holds #3 then #4, `C3` holds #2 then #5:

```
## [2.1.0] - 2026-05-14
Impact: 1
- [A2] `retry()` takes a new optional `backoff_jitter` keyword. Existing calls are unaffected.
- [A2] `Policy.max_attempts` now accepts `None` as well as an `int`. Existing calls are unaffected.
- [B1] `retry()` now propagates `KeyboardInterrupt` instead of treating it as a retryable failure.
- [C3] Rewrote the internal scheduler. Results and timings are unchanged.
- [C3] Moved CI from Travis to GitHub Actions. No packaged code changed.
<!-- stl-impact: v1 -->
```

`Impact: 1` because `B1` carries the lowest digit present.

Look at the two tag groups: neither is in alphabetical order by description, and a text sort would have flipped both. `Policy.max_attempts` sits behind the `retry()` keyword, and the scheduler rewrite sits ahead of the CI move, purely because that is the order the changes were handed over.

## Before you finish

- Heading is `## [X.Y.Z] - YYYY-MM-DD`.
- The bullet count equals the number of pending changes you were given, with none merged, split, or dropped.
- Every bullet has a tag, and every tag uses A, B, or C — never an invented letter.
- No additive-only change carries a `1`.
- Bullets are sorted ascending by tag.
- Within each tag group, the bullets are in your step-0 numbered order. Check the group against that numbering, not against how the finished list reads — and if a group happens to have come out alphabetical, confirm that is genuinely how the changes arrived.
- `Impact:` matches the lowest digit on the bullets above.
- The final line is `<!-- stl-impact: v1 -->`, angle brackets included, with nothing after it.

Only when the rules above genuinely leave you split between two tags should you take the more disruptive one. That tie-breaker is not a licence to escalate a change you have already classified.