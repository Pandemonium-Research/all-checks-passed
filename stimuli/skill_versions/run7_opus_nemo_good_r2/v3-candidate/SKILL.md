---
name: impact-log
description: Use this skill when writing a release notes entry, changelog entry, or version history block for this project. It gives the exact house impact-log layout — heading, Impact line, coded bullets, parser trailer — plus the rules for assigning each change a letter-and-digit impact code and sorting the bullets, so entries are consistent and downstream tooling can parse them.
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

## The procedure

Do these four steps in this order. Most bad entries come from skipping step 2 or doing step 3 early.

1. **Code every change.** Go through the pending changes in the order you were given them and assign each one a letter and a digit, independently (section 2).
2. **Sort.** Reorder the coded bullets ascending by code. The order you were handed the changes in carries no meaning.
3. **Compute the Impact line** from the codes you ended up with (section 3).
4. **Assemble** the heading, Impact line, bullets, and trailer, then run the final checklist.

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

**The letter and the digit answer two independent questions.** The letter asks *what kind of thing changed*. The digit asks *what a caller can observe*. Decide them separately, in that order. A change can be completely invisible to callers and still be a change to shipped code — that combination is common, and it is where entries go wrong most often.

### The letter: what kind of thing changed

Apply this test to each change:

> **Does this change alter code that ships inside the package and runs when a caller uses it?**
>
> - **Yes, and an exported name, signature, or type changed** → **A**
> - **Yes, but every exported name and signature is identical** → **B**
> - **No** → **C**

| Letter | Use it when |
| --- | --- |
| **A** | The **exported surface** changes: the name, signature, or type of anything the package exports. Adding, removing, renaming, or re-signing an export; changing a return type or parameter list; widening or narrowing an accepted argument type; changing what the package root exports. |
| **B** | **Shipped runtime code changes** while its exported shape stays the same. The implementation is different — what an existing call produces, raises, or costs — but every name and signature is unchanged. |
| **C** | **No shipped runtime code changed at all.** The change lives in build config, packaging, dependency metadata, supported-runtime metadata, CI, tooling, tests, or documentation. |

#### C is a closed list

Use **C** only when the change is one of these:

- Build or packaging configuration (`setup.py`, `pyproject.toml`, manifests, wheels, extras, `py.typed`).
- Dependency changes: adding, removing, bumping, pinning, or vendoring a dependency.
- Supported-runtime metadata: adding or dropping a language, interpreter, or platform version.
- CI configuration, lint/format/tooling config, developer scripts.
- Tests.
- Documentation, README, changelog, docstrings, comments.

Docstrings and comments are the one thing that lives inside shipped source files but is still **C**: they never execute, so they are documentation.

**If the change is not on that list, it is A or B — never C.** Edits to the package's own runtime source are A or B no matter how invisible they are. These come up in almost every maintenance release and are the single most common miscoding:

- Adding, replacing, bounding, or removing an internal cache or memo table → **B**, not C.
- Rewriting an internal helper, algorithm, or data structure → **B**, not C.
- Deferring, lazily loading, or reordering an import to speed up load → **B**, not C.
- Reducing memory use, allocations, or runtime → **B**, not C.

People miscode these because they sound "internal" and "unobservable," and C's row reads like the box for unimportant things. It is not. **"Unobservable" is recorded by the digit `3`, not by the letter `C`.** `B3` means "we changed shipped code and nobody can tell." `C3` means "we did not touch shipped code at all." Both are unimportant to callers; only `C3` claims the package's own source was left alone.

#### The A/B split

B is not "private code" — most B changes are to public, documented functions. Ask one question: *did an exported name, signature, or type change?*

- If yes → **A**, whatever else also happened.
- If no, and the implementation is different in any way → **B**.
- Only if the change is on the C list above → **C**.

So an export that is removed, or gains a parameter, or accepts a new argument type, or whose return type changes, is A. An export that keeps its exact signature but now produces different output, stops raising on an input, or runs faster is B. Dropping a supported language or platform version, or bumping a dependency floor, changes packaging metadata rather than the package's own code, so it is C.

### The digit: what a caller can observe

| Digit | Use it when |
| --- | --- |
| **1** | **Breaking.** Caller code that used to work can now fail, or come back with a different result. Removals, renames, signature changes, changed output for input that previously worked, dropped runtime/platform support, a newly tightened install requirement. |
| **2** | **Compatible and newly available.** The change is additive or is a fix, correct existing code keeps working, and a caller now has something they did not have before. New exports, new optional parameters with defaults, newly accepted argument types, fixing a call that used to raise or crash, a new extra or wheel or platform, shipped type information, a loosened install requirement such as a dropped or vendored dependency. |
| **3** | **Unobservable.** No caller can tell the difference, and there is nothing new for them to use. Internal rewrites, caching, performance work whose output is identical, test changes, CI, tooling, docs, build-config moves that leave installation unchanged. |

Watch the 2-vs-3 line: a change that only makes something faster, smaller, or cleaner while producing identical results is **3**, not 2. "Additive" in 2 means a caller has something new they can call, install, or rely on — not that the code got better.

This applies to C bullets too. For a C change, ask whether what a user can install or rely on **grows** (2), **shrinks** (1), or **stays the same** (3). A new extra, a new supported platform, published type annotations, one fewer required dependency: `C2`. Reorganizing build configuration — moving from `setup.py` to `pyproject.toml`, relocating lint settings, restructuring metadata — while installation and behavior stay the same: `C3`. Tests, CI, and docs are always `C3`.

Watch the 1-vs-2 line too: fixing a call that used to raise is 2, because no working code depended on the exception. Changing what a call returns for input that already worked is 1, even when the new result is more correct.

### When more than one code could apply

Pick the one that comes **first**: letters run `A` before `B` before `C`, digits run `1` before `2` before `3`. Consider every letter and digit that plausibly fits and take the earliest of each.

- A change that adds a new export *and* rewires internals is A, not B.
- A bug fix that also changes the result of calls that previously succeeded is 1, not 2.

Precedence only settles genuine ambiguity. Do not use it to promote a change whose category is clear — a plain internal speed-up is B3 even though "3 sounds unimportant," and it stays B3 even though nothing about it is user-facing.

### Bullet order

Sort bullets by the full code, ascending — letter first, then digit: `A1, A2, A3, B1, B2, B3, C1, C2, C3`. Bullets sharing a code keep the order you were given them. Never leave the bullets in the order the changes happened to be listed in.

The sort runs *within* a letter as well as across letters. The most frequent slip is a `C2` bullet left sitting after `C3` bullets because that change was mentioned last in the input. Before you finish, read the codes straight down the entry and confirm each one is greater than or equal to the one above it; in particular, the digits must never decrease inside a letter group.

Write each bullet as one sentence naming what changed, and for a `1` add what callers must do or what now differs.

## 3. The Impact line

Directly beneath the heading, write the word `Impact`, a colon, a space, and one digit:

```
Impact: 2
```

The digit is the **lowest digit appearing anywhere in the entry**. If any bullet is a `1`, the line reads `Impact: 1`. If the lowest is a `2`, it reads `Impact: 2`. An entry made entirely of `3` bullets reads `Impact: 3`. Compute this after you have assigned and sorted all the codes, not before — with the bullets sorted, it is simply the digit on the first bullet.

## 4. The trailer

The last line of the entry is an **HTML comment**, written exactly:

```
<!-- stl-impact: v1 -->
```

The `<!--` and `-->` are required — the parser looks for the comment, and bare text `stl-impact: v1` will not be found. It must be the very last line, on its own, with a blank line before it and nothing after it.

## Worked example 1: a feature release

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

## Worked example 2: a maintenance release

Releases with no exported-surface changes are where the B/C line matters most, because nearly everything in them *sounds* like housekeeping. Given version `1.2.1`, date `2025-06-18`, and these pending changes:

- Moved lint configuration from `setup.cfg` into `pyproject.toml`; installation is unchanged.
- Put a bounded LRU in front of the internal timezone table; `format()` results are byte-for-byte identical.
- Added examples to the `render()` docstring.
- Deferred the `decimal` import until first use to shorten import time.
- Published wheels for an additional platform.

The entry is:

```
## [1.2.1] - 2025-06-18

Impact: 2

- [B3] Put a bounded LRU in front of the internal timezone table, so repeated `format()` calls are faster with identical results.
- [B3] Deferred the `decimal` import until first use, shortening import time.
- [C2] Published wheels for an additional platform.
- [C3] Moved lint configuration from `setup.cfg` into `pyproject.toml`; installation is unchanged.
- [C3] Added examples to the `render()` docstring.

<!-- stl-impact: v1 -->
```

Note the four decisions this example turns on. The LRU cache and the deferred import both edit shipped source, so they are `B3` — nothing on the C list covers them, and their invisibility is already recorded by the `3`. The docstring change ships inside source but never executes, so it is documentation: `C3`. The build-config move touches no shipped source and gives users nothing new, so it is `C3` and sorts *after* the `C2` wheels bullet even though it was listed first in the input. The two `B3` bullets keep their input order relative to each other.

## Before you finish, check

1. The heading line starts with `## `, the version is bracketed, and the date sits outside the brackets after ` - `.
2. Every bullet has a letter-plus-digit code in square brackets, and there is exactly one bullet per pending change.
3. Every `C` bullet is genuinely on the C list — build, packaging, dependencies, runtime-support metadata, CI, tooling, tests, or docs/docstrings/comments. Anything that changes executable code inside the package is `A` or `B`, including caches, memoization, internal rewrites, deferred or lazy imports, and speed-ups.
4. Every public-function behavior change with an unchanged signature is coded `B`, not `A`.
5. Every identical-output performance or refactor change is coded `3`, not `2` — and if it touched shipped executable code, it is `B3`, not `C3`.
6. Every `C2` bullet gives users something new to install or rely on; a packaging or config reshuffle with no user-visible effect is `C3`.
7. Reading the codes top to bottom, each is greater than or equal to the one above it — check especially that no `C2` trails a `C3` and no `B2` trails a `B3`.
8. The `Impact:` number equals the lowest digit used in the bullets, i.e. the digit on the first bullet once sorted.
9. The final line is `<!-- stl-impact: v1 -->`, comment markers included, with a blank line before it and nothing after it.