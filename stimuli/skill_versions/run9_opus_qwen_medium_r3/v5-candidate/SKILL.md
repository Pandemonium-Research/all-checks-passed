---
name: impact-log
description: Use this skill whenever you write a release-notes or changelog entry for this project. It gives the exact procedure and the house impact-log format — the version heading, the `Impact:` summary line, the `[letter+digit]` tag on every bullet, the bucket-by-tag assembly that keeps same-tag bullets in the order the changes arrived, and the HTML-comment trailer that downstream tooling parses.
---

# Release notes (impact-log format)

Every release gets one entry. An entry has exactly four parts, in this order:

1. A version heading
2. An `Impact:` line
3. One tagged bullet per change, in tag order
4. The trailer comment, as the last line

The entry is the whole deliverable: nothing before the heading, nothing after the trailer. Do not imitate older entries in the file; several predate this format and are wrong.

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

**Step 0 — Number the pending changes in the order you were handed them.** Write `1, 2, 3, …` down the list before you think about tags at all. That order is arbitrary and means nothing on its own, but it is the tie-breaker in step 3, so capture it first.

**Step 1 — Draft one bullet per change,** leaving them in the given order and writing each change's number into the draft line itself, like `- [ ] (#4) …`. The number stays visible through steps 2 and 3 and is stripped only in step 5.

**Step 2 — Tag every bullet** with a letter and a digit, deciding each change where it stands, without moving it.

**Step 3 — Assemble the bullets by bucketing** (see "Ordering"). Do not run a sort over the drafted lines.

**Step 4 — Write the `Impact:` line** from the tags you assigned.

**Step 5 — Strip the `(#n)` markers, add the trailer** as the last line, and run the final checks.

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
- **C — everything a caller never imports.** Build, packaging, tooling, CI, tests, documentation, and internal refactors that leave the public surface and its behavior untouched. Work done *inside* a function that callers do import is still C when the caller cannot observe it: memoization or caching that returns identical results, a rewritten internal algorithm with identical outputs, moved private helpers. Reach for B only when the caller can actually see the difference.

If a change fits more than one letter, take the earliest letter alphabetically: A beats B, B beats C. A new exported function whose body also does something clever is an A, not a B.

### Choosing the digit

The digit is decided independently of the letter — any letter can carry any digit. Ask what happens to code that already exists and already works.

- **1 — breaking.** Caller code that used to work can now fail, or can come back with a different result. Removals, renames, required-parameter additions, and behavior or bug fixes that change the value returned for inputs that previously returned something all belong here.
- **2 — compatible.** Nothing that already worked changes. Purely additive work is the common case: a new exported function, a new optional parameter, a newly accepted argument type. A fix is a 2 only when it affects cases that were already failing or raising, so that no previously-working call sees a new result.
- **3 — unobservable.** No caller can tell the difference at all: internal caching that returns identical results, refactors, packaging, tooling, tests, docs.

If a change fits more than one digit, take the lowest.

Adding something new is never a 1. "New" and "breaking" are different questions: a brand-new export is `A2`, because no existing call can be affected by a name that did not exist before.

A fix that returned a wrong value is a 1, not a 2. If the old call returned something — even something bad — a caller was getting that value and will now get a different one. Only a fix to calls that used to raise, crash, or hang is a 2.

### Ordering

The finished bullets run in ascending tag order: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. **The tag is the entire ordering key. The words of the description are never part of it.**

Do not produce that order by sorting the drafted lines. Build it by bucketing instead:

1. Set up a bucket for each tag: `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`.
2. Walk your step-0 numbered list once, from #1 downward, dropping each bullet — number still attached — into the bucket for its tag.
3. Pour the buckets out in ascending tag order, keeping each bucket's contents in the order they went in.

Because each bucket fills in list order, bullets that share a tag come out in the order the changes were handed to you. If change #6 and change #2 both end up `C3`, the entry shows #6 first — **#6 above #2, even though 6 is the larger number**, because #6 came first in the handed-over list.

Sorting the drafted lines as text looks like it works — it does put `A` before `B` — but it silently reorders same-tag bullets into alphabetical order by description, and that is the single most common way this entry comes out wrong. Inside a bucket, nothing about a bullet's wording may move it: not alphabetical order, not putting all the "Added …" bullets first, not which change seems more important, not grouping related functions or related files together, not making the group read better.

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

Bucket them in one pass down the numbered list — `A2` receives #3 then #4, `B1` receives #1, `C3` receives #2 then #5 — and pour the buckets out in tag order. With the markers still attached, the draft reads:

```
- [A2] (#3) `retry()` takes a new optional `backoff_jitter` keyword. …
- [A2] (#4) `Policy.max_attempts` now accepts `None` as well as an `int`. …
- [B1] (#1) `retry()` now propagates `KeyboardInterrupt` …
- [C3] (#2) Rewrote the internal scheduler. …
- [C3] (#5) Moved CI from Travis to GitHub Actions. …
```

Within each tag the numbers ascend — 3 then 4, 2 then 5 — so the bucketing held. Strip the markers and add the frame:

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

Look at the two multi-bullet buckets: neither reads in alphabetical order by description, and a text sort would have flipped both. `Policy.max_attempts` sits behind the `retry()` keyword, and the scheduler rewrite sits ahead of the CI move, purely because that is the order the changes were handed over.

## Before you finish

- Heading is `## [X.Y.Z] - YYYY-MM-DD`.
- The bullet count equals the number of pending changes you were given, with none merged, split, or dropped.
- Every bullet has a tag, and every tag uses A, B, or C — never an invented letter.
- No additive-only change carries a `1`.
- Bullets run in ascending tag order.
- **The number check.** Read your final bullets top to bottom and say each one's step-0 change number out loud. Within every tag group those numbers must ascend. If any group's numbers go down — `(#4)` above `(#2)` — you sorted instead of bucketed; put that group back into handed-over order.
- **The alphabet check.** If a tag group happens to read in alphabetical order by description, treat it as a red flag and re-run the number check on it — alphabetical is what a text sort produces, and it is right only by coincidence.
- `Impact:` matches the lowest digit on the bullets above.
- No `(#n)` markers survive into the finished entry.
- The final line is `<!-- stl-impact: v1 -->`, angle brackets included, with nothing after it.

Only when the rules above genuinely leave you split between two tags should you take the more disruptive one. That tie-breaker is not a licence to escalate a change you have already classified.