---
name: impact-log
description: Use this skill when writing a release notes or changelog entry for this project. It gives the exact impact-log format the team requires — heading, Impact line, tagged and sorted bullets, and the parser trailer — plus the rules for choosing each bullet's tag.
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
line → add the trailer.

## Step 1 — Heading

Second-level heading. Version in square brackets, three parts, no `v` prefix. Then a space, a
hyphen, a space, then the date in `YYYY-MM-DD` form. Never a localized date.

## Step 2 — Write one bullet per pending change

Each bullet is `- [` + letter + digit + `] ` + the change described in a sentence. Use backticks
around identifiers. Add a short second sentence when it tells the reader whether their own code is
affected (for example, that existing calls are unaffected, or what they must change).

The letter and the digit are two separate decisions. Decide each one on its own; do not let a
scary-looking letter pull the digit down, or vice versa.

### The letter — what part of the project the change touches

| Letter | Use it when |
| --- | --- |
| `A` | The public API surface changes: the names, signatures, or types of anything the package exports. Adding a new export counts. |
| `B` | The runtime behavior of an existing call changes while its signature stays the same. |
| `C` | Only build, packaging, tooling, tests, or documentation changes — nothing inside the importable package changes for anyone. |

Invent no other letters. If a change could be argued into two of these, take the one that comes
first alphabetically: `A` beats `B`, `B` beats `C`.

### The digit — how much it can hurt a caller

| Digit | Use it when |
| --- | --- |
| `1` | Breaking. Code that used to work can now fail, or can come back with a different result. Removing or renaming an export; changing, reordering, or removing a parameter; narrowing what an argument accepts; **and any bug fix that changes the value returned for input that previously returned a value.** |
| `2` | Compatible. Purely additive, or a fix that no correct caller can be hurt by. New function, class, or export; new optional parameter with a default; widening what an argument accepts; a fix that turns a call that used to raise or crash into one that works. Existing correct calls keep their old results. |
| `3` | Invisible. No caller can observe any difference at all. Internal refactors, caching that returns identical results, and everything in the `C` letter category. |

If a change could be argued into two digits, take the lower one.

Two mistakes that come up in review:

- **An addition is a `2`, not a `1`.** Adding a new exported function is an `A` change because it
  changes the export surface, but nothing that used to work stops working, so the digit is `2`.
  The letter `A` never forces the digit `1`.
- **A behavior fix that changes output is a `1`, not a `2`.** Callers who were getting the old
  output will now get something different, which is exactly what digit `1` warns about.

When two options are still genuinely arguable after applying the tables, pick the more disruptive
digit — a reader warned unnecessarily is better off than one not warned at all. Never use this as
a reason to call an addition or a `C` change breaking.

## Step 3 — Sort the bullets

Sort by the code, ascending, letter first and then digit — not by the order the changes were
handed to you. So `A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`. Bullets that share the same
code may stay in any order relative to each other.

## Step 4 — Impact line

Directly beneath the heading, before the first bullet, on its own line: the word `Impact`, a colon,
a space, and a number. The number is the **lowest digit appearing on any bullet in the entry**. If
any bullet is a `1`, the line reads `Impact: 1`; if the lowest is a `2`, it reads `Impact: 2`.

## Step 5 — Trailer

The last line of the entry is an HTML comment, written out in full, including the `<!--` and `-->`:

```
<!-- stl-impact: v1 -->
```

The parser rejects the file without it. It must be the very last line, below every bullet. Writing
`stl-impact: v1` as bare text is not enough — the comment markers are part of it.

## Final check before you hand the entry over

- Heading is `## [X.Y.Z] - YYYY-MM-DD`.
- `Impact: N` sits directly under the heading and equals the lowest digit used below.
- Every bullet starts with `- [` letter digit `] `, using only `A`, `B`, or `C` and only `1`, `2`,
  or `3`.
- New exports are `2`, not `1`. Behavior fixes that change returned values are `1`, not `2`.
- Bullets are in ascending code order.
- The last line is `<!-- stl-impact: v1 -->`, comment markers included.