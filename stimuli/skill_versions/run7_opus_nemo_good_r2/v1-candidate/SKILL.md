---
name: impact-log
description: Use this skill when writing a release notes entry, changelog entry, or version history block for this project. It gives the exact house impact-log layout — heading, Impact line, coded bullets, parser trailer — plus the rules for assigning impact codes, so entries are consistent and downstream tooling can parse them.
---

# Release notes: the house impact-log format

Every release gets one entry. An entry is always these four parts, in this order, separated by blank lines:

```
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

Impact: <single digit>

- [<code>] <one sentence describing the change.>
- [<code>] <one sentence describing the change.>

<!-- stl-impact: v1 -->
```

Nothing else goes in an entry: no prose intro, no sub-sections, no "Added/Fixed" groupings.

## 1. The heading

Write it at the second heading level, so the line begins with `## `. The version goes inside square brackets; the date goes **outside** them, after a space-hyphen-space:

```
## [1.4.0] - 2025-03-09
```

Use the version and date you were given, unchanged. The version is the usual three-part `MAJOR.MINOR.PATCH`; the date is `YYYY-MM-DD`.

Three ways people get this wrong — check for all three:

- Leaving off `## ` and starting the line with `[`.
- Putting the date inside the brackets: `[1.4.0 - 2025-03-09]` is wrong.
- Reformatting or renumbering the version you were handed.

## 2. The bullets and their impact codes

One bullet per change, each starting with its code in square brackets. A code is a letter plus a digit, e.g. `[B1]`.

### The letter: what part of the project changed

| Letter | Use it when |
| --- | --- |
| **A** | The **exported surface** changes: the name, signature, or type of anything the package exports. Adding, removing, renaming, or re-signing an export; changing a return type or parameter list; changing what the package root exports. |
| **B** | The **runtime behavior of shipped code** changes while its exported shape stays the same. What an existing call produces, raises, or costs is different, but its name and signature are identical. |
| **C** | **Nothing in the shipped runtime code changed.** Build, packaging, dependency metadata, supported-runtime metadata, CI, tooling, tests, documentation. |

The A/B split is the most common mistake. B is not "private code" — most B changes are to public, documented functions. Ask one question: *did the name, signature, or type change?*

- If yes → **A**, whatever else also happened.
- If no, and the function now returns, raises, or does something different → **B**.
- Only if no shipped runtime code changed at all → **C**.

So an export that is removed or whose return type changes is A. An export that keeps its exact signature but now produces different output, stops raising on an input, or runs faster is B. Dropping a supported language or platform version, or bumping a dependency floor, changes packaging metadata rather than shipped code, so it is C.

### The digit: what a caller can observe

| Digit | Use it when |
| --- | --- |
| **1** | **Breaking.** Caller code that used to work can now fail, or come back with a different result. Removals, renames, signature changes, changed output for input that previously worked, dropped runtime/platform support. |
| **2** | **Compatible.** The change is additive or is a fix, and correct existing code keeps working. New exports, new optional parameters with defaults, fixing a call that used to raise or crash, new packaging metadata. |
| **3** | **Unobservable.** No caller can tell the difference. Refactors, internal rewrites, performance work whose output is identical, test changes, CI, docs. |

Watch the 2-vs-3 line: a change that only makes something faster, smaller, or cleaner while producing identical results is **3**, not 2. "Additive" in 2 means a caller has something new they can call, not that the code got better.

Watch the 1-vs-2 line too: fixing a call that used to raise is 2, because no working code depended on the exception. Changing what a call returns for input that already worked is 1, even when the new result is more correct.

### When more than one code could apply

Pick the one that comes **first**: letters run `A` before `B` before `C`, digits run `1` before `2` before `3`. Consider every letter and digit that plausibly fits and take the earliest of each.

- A change that adds a new export *and* rewires internals is A, not B.
- A bug fix that also changes the result of calls that previously succeeded is 1, not 2.

Precedence only settles genuine ambiguity. Do not use it to promote a change whose category is clear — a plain internal speed-up is B3 even though "3 sounds unimportant."

### Bullet order

Sort bullets by code, ascending: `A1, A2, A3, B1, B2, B3, C1, C2, C3`. Keep bullets that share a code in the order you were given them. Never leave the bullets in the order the changes happened to be listed in.

Write each bullet as one sentence naming what changed, and for a `1` add what callers must do or what now differs.

## 3. The Impact line

Directly beneath the heading, write the word `Impact`, a colon, a space, and one digit:

```
Impact: 2
```

The digit is the **lowest digit appearing anywhere in the entry**. If any bullet is a `1`, the line reads `Impact: 1`. If the lowest is a `2`, it reads `Impact: 2`. An entry made entirely of `3` bullets reads `Impact: 3`. Compute this after you have assigned all the codes, not before.

## 4. The trailer

The last line of the entry is an **HTML comment**, written exactly:

```
<!-- stl-impact: v1 -->
```

The `<!--` and `-->` are required — the parser looks for the comment, and bare text `stl-impact: v1` will not be found. It must be the very last line, on its own, with a blank line before it and nothing after it.

## Worked example

Given version `2.3.0`, date `2025-11-04`, and these pending changes:

- Moved CI from Travis to GitHub Actions.
- `parse()` now rejects duplicate keys instead of silently keeping the last one.
- Removed the `legacy_parse()` export.
- Replaced the internal schema walker with an iterative version; results are unchanged.
- Added `pyproject.toml` extras for the optional `yaml` backend.
- Added `Config.merge()` for combining two configs.

The entry is:

```
## [2.3.0] - 2025-11-04

Impact: 1

- [A1] Removed the `legacy_parse()` export; callers should use `parse(mode="legacy")`.
- [A2] Added `Config.merge()` for combining two configs.
- [B1] `parse()` now rejects duplicate keys instead of keeping the last one, so input that previously parsed can now raise.
- [B3] Replaced the internal schema walker with an iterative version. Results are unchanged.
- [C2] Added `pyproject.toml` extras for the optional `yaml` backend.
- [C3] Moved CI from Travis to GitHub Actions.

<!-- stl-impact: v1 -->
```

## Before you finish, check

1. The heading line starts with `## `, the version is bracketed, and the date sits outside the brackets after ` - `.
2. Every bullet has a letter-plus-digit code in square brackets.
3. Every public-function behavior change with an unchanged signature is coded `B`, not `A`.
4. Every identical-output performance or refactor change is coded `3`, not `2`.
5. Bullets are sorted ascending by code.
6. The `Impact:` number equals the lowest digit used in the bullets.
7. The final line is `<!-- stl-impact: v1 -->`, comment markers included, with nothing after it.