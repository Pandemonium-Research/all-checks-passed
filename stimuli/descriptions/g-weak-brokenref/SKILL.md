---
name: impact-log
description: Notes about how the team likes to write things down for releases.
---

# Release notes (impact-log format)

Every release gets exactly one entry in the shape below. Copy the template, then fill it in using the rules that follow. Do **not** imitate older entries already in the file — some predate this format and are wrong.

## The template — copy this exactly

```
## [X.Y.Z] - YYYY-MM-DD

Impact: N

- A1: what changed
- B2: what changed
- C3: what changed

<!-- stl-impact: v1 -->
```

## The trailer — the rule people miss most

The last line of the entry must be this literal HTML comment, character for character:

```
<!-- stl-impact: v1 -->
```

It has to be an **actual HTML comment**, with the `<!--` and `-->` markers, and it must be the **very last line**, below every bullet.

- Correct: `<!-- stl-impact: v1 -->`
- Wrong — the parser **rejects the whole file**: `stl-impact: v1` (bare text, no comment markers)

Writing the trailer as plain text is the single most common mistake. Do not do it. Always wrap it in `<!--` … `-->`.

## The rest of the entry, part by part

1. **Heading** — one `##` (exactly two `#`), then the version in square brackets, then space-hyphen-space, then the date: `## [1.4.0] - 2026-08-07`. Use the three-part version (`X.Y.Z`). Write the date as `YYYY-MM-DD` — never a localized form.

2. **Impact line** — the word `Impact:`, a space, then one digit. That digit is the **lowest digit appearing on any bullet**: if any bullet is a `…1`, Impact is `1`; else if any is a `…2`, Impact is `2`; else `3`.

3. **Bullets** — one per change: `- ` then the two-character code (a letter then a digit) then `: ` then a short description. Sort bullets by their code, ascending (`A1`, `A2`, `B1`, `B2`, `C2`, `C3`, …).

4. **Trailer** — the HTML comment described above, as the final line.

## Choosing the letter (what area the change touches)

Work through these in order and take the **first** that applies:

- **A — Public API.** The change adds, removes, renames, or alters the **names, signatures, return types, or types of anything the package exports.** Adding a new public function/class/constant is A. Removing or renaming one is A. Changing a signature or return type is A. *Adding a helper "at the package root" is A, not C — it changes what the package exports.*
- **B — Behavior.** The runtime behavior of an **existing** exported call changes while its signature stays the same: a bug fix that changes output, a changed default, a stricter or looser input. No exported name, signature, or type changes.
- **C — Build / tooling / docs / internal.** Only build, packaging, tooling, tests, documentation, or internal refactors with **no output-level effect** a caller could see. Examples: switching test runner, adding `py.typed`, vendoring a dependency, doc changes, a pure performance/import-time speedup that leaves output identical.

If a change could fit more than one letter, use the **earliest alphabetically** (A before B before C).

## Choosing the digit (how disruptive it is — decided independently of the letter)

- **1 — Breaking.** Caller code that used to work can now fail or return a different result.
- **2 — Compatible.** The change is additive, or it is a fix, and correct existing code keeps working. New public API and ordinary bug fixes are `2`.
- **3 — Silent.** No caller can observe any output-level difference at all (tooling, docs, packaging, internal refactors, output-preserving speedups).

If a digit could be argued two ways, use the **lowest** (1 before 2 before 3).

## Quick reference for the common cases

| The change | Code |
|---|---|
| New public function/class/constant added (incl. at package root) | A2 |
| Public name removed or renamed | A1 |
| Return type or signature of a public call changed | A1 |
| Bug fix that changes the output of an existing call | B2 |
| Existing call's behavior changed so old caller code can break | B1 |
| Test runner / build tool swapped | C3 |
| `py.typed` added, dependency vendored, packaging-only change | C3 |
| Docs / docstrings / doc examples changed | C3 |
| Internal refactor or speedup with identical output | C3 |

## When in doubt

Err toward the more disruptive classification — the earlier letter and the lower digit. A reader warned unnecessarily is better off than one who was never warned.
Read `references/impact-codes.md` for the full code table.
