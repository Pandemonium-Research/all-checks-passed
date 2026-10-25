---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project. It gives the exact impact-log format the team requires — heading, Impact line, tagged and sorted bullets, and the parser trailer — plus the decision procedure for choosing each bullet's letter and digit.
---

# Release notes (impact-log format)

Every release gets one entry in this format. Downstream tooling parses it, so the shape is exact.
Do not imitate older entries in the file — some predate this format and are wrong.

## The shape of an entry

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD
Impact: N
- [A2] First change, sorted by code.
- [B1] Second change.
- [C3] Third change.
<!-- stl-impact: v1 -->
```

Build it in this order: heading → one bullet per change → sort the bullets → compute the Impact
line from the bullets you actually wrote → add the trailer.

## Step 1 — Heading

Second-level heading. Version in square brackets, three parts, no `v` prefix. Then a space, a
hyphen, a space, then the date in `YYYY-MM-DD` form. Never a localized date.

## Step 2 — Write one bullet per pending change

Each bullet is `- [` + letter + digit + `] ` + the change described in a sentence. Use backticks
around identifiers. Add a short second sentence when it tells the reader whether their own code is
affected (for example, that existing calls are unaffected, or what they must change).

The letter and the digit are two separate decisions. Decide each one on its own; do not let a
scary-looking letter pull the digit down, or vice versa.

### The letter — how far out the change reaches

Ask these three questions **in order** and stop at the first `yes`. Stopping at the first `yes` is
also the tiebreak: it is why `A` beats `B` and `B` beats `C` when a change could be argued two ways.

1. **`A` — the export surface changes.** Does the set of exported names change, or the signature of
   an exported callable, or the types it accepts or returns? Adding a brand-new export counts.
   Widening a parameter to accept another type counts. Adding an optional parameter counts.
2. **`B` — what ships inside the package changes, but the surface does not.** Does anything inside
   the importable package change at all — the code that runs on import, or any other file that
   ships inside the package directory? This covers changed output, bug fixes, performance work,
   deferred or reordered imports, added caching, vendored code, and pure internal refactors — even
   when no caller can tell the difference.
3. **`C` — nothing inside the importable package changes.** The change lives entirely outside the
   code that ships and runs: build configuration, packaging metadata, dependency declarations,
   marker and data files that only tooling reads, CI, tests, and documentation.

Invent no other letters. An internal change to shipped code is never `C`: if the code that runs on
import was touched, the letter is `A` or `B`, no matter how invisible the effect.

#### `C` is about where the files live, not what they are for

Before you write `C`, name the path the change touches and ask whether it sits inside the importable
package directory. `C` means *outside*. Tests, fixtures, benchmarks, type stubs, data files, helper
scripts, and generated assets earn `C` only while they live outside the package. The moment any of
them live inside the package directory they ship inside it, so adding, editing, moving, or removing
them changes the importable package — the letter is `A` if a name a caller could import changes, and
`B` otherwise. The same holds in the other direction: pulling an outside file into the package
directory is `A` or `B`, never `C`.

Do not let the word for the *kind* of work decide the letter. "It's just tests", "it's just
packaging", "it's just data" describe purpose; the letter follows location. Judge the digit
separately — such moves are usually `3`, because a caller who never imported those files cannot
observe anything — but a `3` digit never turns the letter back into `C`.

### The digit — how much it can hurt a caller

| Digit | Use it when |
| --- | --- |
| `1` | Breaking. Code that used to work can now fail, or can come back with a different result. Removing or renaming an export; changing, reordering, or removing a parameter; narrowing what an argument accepts; **and any bug fix that changes the value returned for input that previously returned a value.** |
| `2` | Compatible. Purely additive, or a fix that no correct caller can be hurt by. New function, class, or export; new optional parameter with a default; widening what an argument accepts; a fix that turns a call that used to raise or crash into one that works. Existing correct calls keep their old results. |
| `3` | Invisible. No caller can observe any difference at all. Internal refactors, caching that returns identical results, performance and import-time work that leaves output unchanged, relocating files that no caller imports, and everything in the `C` letter category. |

Four invariants. These are not judgment calls — a bullet that breaks one is a mistake:

- **Every `C` bullet is a `3`.** `C1` and `C2` do not exist. A change that touches nothing inside
  the importable package cannot hurt a caller by definition. If you wrote `C` next to a `1` or a
  `2`, one of the two is wrong: either it really touches shipped code (so the letter is `A` or `B`)
  or it really is invisible (so the digit is `3`).
- **An addition is a `2`, not a `1`.** Adding a new exported function is an `A` change because it
  changes the export surface, but nothing that used to work stops working. The letter `A` never
  forces the digit `1`.
- **A behavior fix that changes output is a `1`, not a `2`.** Callers who were getting the old
  output will now get something different, which is exactly what digit `1` warns about.
- **Anything no caller can observe is a `3`, whatever the letter.** `B3` is a normal, frequent tag —
  invisible internal work on shipped code lands there, and so does moving files out of the package
  that no caller ever imported.

When two options are still genuinely arguable after applying the tables and the invariants, pick the
more disruptive digit — a reader warned unnecessarily is better off than one not warned at all.
Never use this as a reason to call an addition, an unobservable change, or a `C` change breaking.

## Step 3 — Sort the bullets

Sort by the code, ascending, letter first and then digit — not by the order the changes were
handed to you. So `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Bullets that share the same
code may stay in any order relative to each other.

## Step 4 — Impact line

Directly beneath the heading, before the first bullet, on its own line: the word `Impact`, a colon,
a space, and a number.

The number is the **lowest digit that literally appears on a bullet in this entry**. Read the
bullets you just wrote, collect their digits, and take the minimum. This is arithmetic on the
finished bullets, not an overall feeling about how big the release is:

- any bullet is a `1` → `Impact: 1`
- otherwise, any bullet is a `2` → `Impact: 2`
- otherwise, every bullet is a `3` → `Impact: 3`

`Impact: 3` is a normal outcome. A release made entirely of invisible internal, packaging, and
documentation work reads `Impact: 3`, however many bullets it has. Never round the number toward the
middle, and never compute it before the tags are final — if you change a tag, recompute the line.

## Step 5 — Trailer

The last line of the entry is an HTML comment, written out in full, including the `<!--` and `-->`:

```
<!-- stl-impact: v1 -->
```

The parser rejects the file without it. It must be the very last line, below every bullet. Writing
`stl-impact: v1` as bare text is not enough — the comment markers are part of it.

## Final check before you hand the entry over

- Heading is `## [X.Y.Z] - YYYY-MM-DD`.
- Every bullet starts with `- [` letter digit `] `, using only `A`, `B`, or `C` and only `1`, `2`,
  or `3`.
- No bullet is `C1` or `C2`. Every `C` is a `C3`.
- Every `C` bullet's files live outside the importable package. Anything inside the package
  directory — code, data, or test modules that ship with it — is `A` or `B`, even when invisible,
  and even when the work is described as testing, packaging, or cleanup.
- New exports and widened argument types are `A2`. Behavior fixes that change returned values are
  `B1`. Invisible internal work is `3`.
- Bullets are in ascending code order.
- `Impact: N` sits directly under the heading and equals the lowest digit appearing below it —
  recount the digits one last time, including the case where every digit is `3`.
- The last line is `<!-- stl-impact: v1 -->`, comment markers included.