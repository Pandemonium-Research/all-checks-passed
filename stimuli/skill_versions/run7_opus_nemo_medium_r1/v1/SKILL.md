---
name: impact-log
description: Use this skill when writing release notes, changelog entries, or version history for this project. It gives the exact shape of a house impact-log entry — heading, impact line, coded bullets, trailer — plus the rules for choosing each code, so downstream tooling can parse the result.
---

# Release notes

Every release gets one entry in the house impact-log format. The format is strict because a parser
reads it. Build the entry from the template below rather than imitating older entries in the file —
some of them predate this format and are wrong.

## The template

An entry is exactly four parts, in this order, and nothing else:

```
## [VERSION] - DATE

Impact: N

- [XN] First change.
- [XN] Second change.

<!-- stl-impact: v1 -->
```

Filled in, a complete entry looks like this:

```
## [2.3.0] - 2025-11-04

Impact: 1

- [A1] Removed the deprecated `Session.connect_timeout` keyword; use `timeout=` instead.
- [A2] Added `Session.retry()` for bounded retries.
- [B1] `parse_url()` now lower-cases the host, changing results for mixed-case input.
- [B2] Fixed `encode()` raising on empty payloads; it now returns `b""`.
- [C2] Published wheels for musllinux.
- [C3] Replaced the internal buffer with a ring buffer; output is unchanged.

<!-- stl-impact: v1 -->
```

### The heading

- Starts with `## ` — a second-level heading. It is not a bare bracketed line.
- The square brackets wrap the version **and nothing else**. The date sits outside them.
- Separator between them is a space, a hyphen, a space: `] - `.
- Version is the three-part `MAJOR.MINOR.PATCH` form. Date is `YYYY-MM-DD`, never localized.
- Use the version and date you were given, verbatim. Do not invent or adjust them.

Correct: `## [0.9.2] - 2026-03-17`
Wrong: `[0.9.2 - 2026-03-17]`, `## 0.9.2 - 2026-03-17`, `## [0.9.2 - 2026-03-17]`, `## [0.9.2] (Mar 17, 2026)`

### The impact line

- The literal word `Impact`, a colon, a space, and one digit.
- It goes directly under the heading, above the bullets. It never goes at the bottom.
- The digit is **the lowest digit appearing on any bullet in the entry**. If any bullet is a 1,
  the impact line is `Impact: 1`. If the lowest is 2, it is `Impact: 2`. Read your finished
  bullets and take the minimum — do not judge the release as a whole.

### The bullets

- One bullet per change, each starting with `- ` (hyphen, space).
- Then the code in square brackets: one capital letter, one digit, no space, no separator, no
  second number. `[A1]`, `[B2]`, `[C3]`.
  Wrong: `[ A1 ]`, `[A-1]`, `[A1 2]`, `A1`, `[a1]`, `[D1]`, `[B4]`.
- Then a space, then the change described in one sentence, ending with a period.
- Cover every change you were given. Do not merge two changes into one bullet or drop any.

### The trailer

- The last line of the entry is exactly `<!-- stl-impact: v1 -->`.
- It must be an HTML comment. A bare `stl-impact: v1` line is rejected by the parser.
- Nothing goes after it — no bullets, no impact line, no blank-line-and-more-text.

## Choosing the letter

Walk these in order and stop at the first one that matches.

- **A — public API surface.** The change adds, removes, renames, or alters the signature or type
  of something the package exports.
- **B — behavior of an existing call.** The exported names and signatures are untouched, but
  calling existing code now does something different: different return value, different error,
  different side effect.
- **C — everything else.** Build, packaging, distribution, dependencies, CI, tooling, tests,
  documentation, docstrings, type-marker files, supported-version metadata, and internal
  implementation changes that no caller can see.

C is the fallback, not a "minor" label. A packaging or support-matrix change that breaks users is
still C — the letter says *where* the change lives, the digit says *how much it hurts*. `C1` is a
normal, valid code.

## Choosing the digit

Decided independently of the letter. Walk these in order and stop at the first match.

- **1 — breaking.** Code that worked before can now fail, or come back with a different result.
  Removals, renames, changed signatures or return types, changed defaults, changed output for
  inputs that previously produced output, dropped platform or interpreter support.
- **2 — compatible.** Purely additive, or a fix. Every previously *correct* usage keeps working
  the same way. New functions, new optional parameters, new wheels or platforms, and bug fixes
  where the old behavior was a crash or was plainly wrong.
- **3 — invisible.** No caller can observe any difference at all. Internal refactors, performance
  work that produces identical output, test moves, CI changes, comment and documentation edits.

Two traps that come up in review constantly:

- If the change says the output or behavior is **unchanged** — a rewrite, a cache swap, a speedup,
  an import deferral — the digit is **3**, no matter how substantial the work was.
- A "fix" that changes results for input that used to return something is **1**, not 2. Only call
  it 2 when the old behavior was an error or was unusable.

Documentation, docstring, and tooling changes are not breaking just because they sound important;
classify by what the change actually does to callers.

## When a change fits two rows

Some changes genuinely satisfy more than one row on either axis — take the earlier row. Letters
run in alphabetical precedence (A over B over C); digits run low to high (1 over 2 over 3). A
removal that is both an API change and a packaging change is A; a change that is both additive and
breaking for some callers is 1. This tie-break is for real double-matches only — do not escalate a
change out of vague unease.

## Ordering the bullets

Sort bullets by their code, ascending, regardless of the order the changes were handed to you:

`A1, A2, A3, B1, B2, B3, C1, C2, C3`

Letter first, then digit. Bullets sharing a code keep their original relative order.

## Before you finish

1. Heading is `## [X.Y.Z] - YYYY-MM-DD`, with brackets around the version only.
2. `Impact: N` sits directly under the heading, and N is the lowest digit on any bullet.
3. Every bullet starts `- [XN] ` with no spaces inside the brackets and no extra number.
4. Every letter is A, B, or C; every digit is 1, 2, or 3.
5. Bullets are sorted ascending by code.
6. The final line is `<!-- stl-impact: v1 -->`, and nothing follows it.