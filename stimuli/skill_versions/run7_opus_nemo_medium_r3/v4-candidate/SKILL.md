---
name: impact-log
description: The house "impact-log" format for this project's release notes — the heading, the impact line, the `[letter+digit]` bullet tags and how to choose them, bullet ordering, and the required trailer. Reach for this whenever you write a changelog or release-notes entry for a new version, so every change is classified correctly and the parser accepts the file.
---

# Writing an impact-log entry

An entry has exactly four parts, in this order: a heading, an impact line, a list of tagged
bullets, and a trailer comment. Produce all four. The parser rejects entries that are missing any
of them or that vary the punctuation.

Do not imitate older entries already in the file — many of them predate this format.

## How to build one

Work in this order. The middle steps are where entries go wrong, and they are separate passes for
a reason:

1. **Split** the pending changes so that each bullet describes exactly one change (§3).
2. **Tag** every bullet with a letter and a digit (§2). Tag each change on its own merits.
3. **Sort** the bullets by tag (§4). Do this as its own pass, after tagging. The order the changes
   were handed to you is never the order they go in.
4. **Read** the digit off the now-first bullet; that digit is the `Impact:` number.
5. **Assemble** heading, impact line, sorted bullets, trailer.

## 1. The skeleton

Every entry looks exactly like this, with your own version, date, and changes substituted in:

```
## [1.4.0] - 2026-03-09

Impact: 1

- [A1] <one sentence describing the change; for a breaking change, say what breaks>
- [A2] <one sentence>
- [B2] <one sentence>
- [C3] <one sentence>

<!-- stl-impact: v1 -->
```

Details that people get wrong:

- The heading starts with `## ` (second level). The version is in square brackets, then a space,
  a hyphen, a space, then the date: `## [X.Y.Z] - YYYY-MM-DD`.
- Use the three-part version form (`1.4.0`, not `1.4`) and the year-month-day date form. Never a
  localized date.
- Nothing else goes on the heading line. The impact number does **not** go there.
- `Impact: N` sits on its own line directly beneath the heading. No brackets, no bullet marker, no
  bold.
- Every change is a bullet beginning with `- `.
- The last line is the literal HTML comment `<!-- stl-impact: v1 -->`. Writing the bare text
  `stl-impact: v1` without the `<!--` and `-->` wrappers is the single most common failure — the
  parser will not see it. It must be the very last line, below every bullet.

## 2. Tagging a bullet

Each bullet begins with one tag in **one** pair of square brackets: a letter immediately followed
by a digit, no space and no second bracket, then a space, then the text.

```
- [A1] ...     correct
- [A][1] ...   wrong — one bracket pair only
- [A 1] ...    wrong — no space inside the tag
- [a1] ...     wrong — the letter is uppercase
```

Use only the letters A, B, and C, and only the digits 1, 2, and 3. Do not invent other letters.

### The letter: what kind of thing changed

- **A — the public API.** The names, signatures, or types of anything the package exports changed.
  This covers adding, removing, or renaming an exported function, class, or module; adding or
  removing a parameter (even an optional one); and changing a return type or annotations on
  exported functions.
- **B — runtime behavior.** The shipped implementation changed while every exported signature
  stayed exactly the same. This covers changes a caller can notice (different results, different
  speed, different memory) *and* changes no caller can notice at all (an internal rewrite, a
  swapped algorithm, a replaced cache).
- **C — nothing that ships as logic.** Build and packaging files, dependency declarations, CI,
  developer tooling, tests, and documentation — including docstrings and comments, which are prose
  even though they ride along inside the package. A `C` change leaves every line of shipped logic
  exactly as it was.

**The B/C line is the one people cross.** Ask: *did I edit the implementation of code that users
import or run?* If yes, the letter is A or B — never C, no matter how invisible the effect is.
"Nobody can see it" is what the **digit 3** records; the letter still has to say that shipped logic
changed. So an internal cache, data-structure, or algorithm swap with byte-identical output is
`B3`, not `C3`.

If a change could be argued into more than one letter, take the **alphabetically earliest** one
that applies. So a change that both alters a signature and alters behavior is `A`, not `B`; a
change that adds an exported helper and also touches the docs is `A`, not `C`.

### The digit: how much it can hurt a caller

Decide this **independently** of the letter — every letter can pair with every digit.

- **1 — breaking.** Caller code that used to work can now fail, or come back with a different
  result.
- **2 — compatible.** The change is additive or is a fix; correct existing code keeps working
  unchanged.
- **3 — invisible.** No caller can observe the difference at all.

If more than one digit could be argued, take the **lowest** one that applies.

### Common pairings

| The change | Tag |
|---|---|
| Exported name removed or renamed; parameter removed; return type changed | `A1` |
| New exported function, class, or module | `A2` |
| New optional parameter that defaults to the old behavior | `A2` |
| Type annotations added to exported functions, runtime unchanged | `A2` |
| Output of an existing call changes for the same input, signature unchanged | `B1` |
| Bug fix in existing behavior — wrong results become right, signature unchanged | `B2` |
| Performance, import-time, or memory fix in an existing call, results unchanged | `B2` |
| Internal rewrite of shipped code — new algorithm, cache, or data structure, results identical | `B3` |
| Supported runtime/dependency version dropped | `C1` |
| Runtime dependency added, relaxed, removed, or vendored; installs differ, behavior identical | `C2` |
| CI config, test changes, docs toolchain, and any pin or bound in a dev, test, or docs extra | `C3` |
| Docstrings, comments, README, or other prose only | `C3` |
| Packaging or build metadata that changes neither dependencies nor supported versions | `C3` |

The `C2`/`C3` line: `C2` is for the dependencies a user actually installs with the package. A
requirement that only maintainers install — anything living in a dev, test, lint, or docs extra —
is `C3`, however tightly it is pinned, because no user's install changes.

When you are genuinely unsure, err toward the more disruptive classification — the earlier letter
and the lower digit. A reader warned unnecessarily is better off than one who was not warned.

## 3. One change per bullet

Split anything joined by "and" that describes two separate changes; they usually classify
differently. A bullet that adds a parameter *and* speeds something up is two bullets, an `A2` and a
`B2`. Split them even when both halves land on the same tag — a rename plus a changed return type
is two `A1` bullets, not one. One bullet, one change.

Keep each bullet to a single sentence or two. For anything tagged with a `1`, say what a caller has
to do differently.

## 4. Ordering and the impact line

Once every bullet is tagged, reorder the whole list ascending by code — letter first, then digit:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

This is a mechanical re-sort of the finished bullets, not a preference. Changes arrive in whatever
order someone happened to list them, and that order is almost never sorted. For example, a set
tagged in the order handed over as

`B2`, `A1`, `C3`, `B1`, `A2`, `B2`

is written out as

`A1`, `A2`, `B1`, `B2`, `B2`, `C3`

Note that `B1` moves *above* both `B2` bullets even though it was handed over between them: within
a letter, the digits sort too. Repeated codes are fine; keep them together. Nothing about a
bullet's text affects its position — only its code does.

The `Impact:` number is the **lowest digit appearing anywhere in the entry**, ignoring the letters.
An entry whose lowest-digit bullet is `C1` has `Impact: 1`. An entry made entirely of `A2` and `C3`
bullets has `Impact: 2`. Because bullets are sorted, this is always the digit of the first bullet.

## Before you hand it over

1. Heading is `## [X.Y.Z] - YYYY-MM-DD` and holds nothing else.
2. `Impact: N` is on its own line right under the heading, unbracketed, and N is the lowest digit
   used below.
3. Every bullet starts with `- ` and one tag like `[B2]` — one bracket pair, uppercase letter,
   digit, no spaces inside.
4. No bullet describes two changes.
5. Every bullet that touches shipped code is tagged A or B; only build, packaging, dependency,
   tooling, test, and prose changes are tagged C.
6. Read the tags straight down the page: each one must be greater than or equal to the one above
   it, comparing the letter first and then the digit. If any line goes backwards, the list is
   unsorted — fix it and recheck the impact line.
7. The final line is exactly `<!-- stl-impact: v1 -->`, comment markers included.