---
name: impact-log
description: Use this document when given a version, date, and pending project changes to produce one classified, sorted, machine-parseable release-notes entry.
---

# Release notes

Create exactly one release entry from the supplied version, date, and pending changes. Include exactly one bullet for each pending change.

Use this structure exactly:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace every placeholder. Return only the finished entry: no code fence, explanation, or other text.

## 1. Classify each change

Each code consists of one letter and one digit. Choose them independently:

- The letter identifies what changed.
- The digit identifies compatibility or visibility.

Classify every change before sorting the bullets.

### Choose the letter

Apply these rules in order. When more than one category applies, use the first matching letter: **A before B before C**.

- **A — Public interface or typing contract**
  - Adds, removes, or renames an exported name.
  - Changes a public signature, parameter, return contract, accepted input type, exception contract, or annotation.
  - Expands the kinds of input a public operation supports.
  - Adds or changes shipped typing information, including marking the distributed package as typed.

- **B — Package runtime behavior or implementation**
  - Fixes a runtime bug without changing the public interface contract.
  - Changes the result or behavior of an existing operation.
  - Changes performance, memory use, caching, cache eviction, import timing, or another runtime characteristic.
  - Refactors code that runs as part of the package.

- **C — Work outside the package runtime**
  - Changes builds, packaging, dependencies, installation metadata, development tooling, tests, or documentation.
  - Does not change the public interface contract or package runtime behavior.

Important distinctions:

- A newly exported operation is **A**, not B.
- Supporting an additional public input type is **A**, even if the signature text is unchanged.
- A runtime bug fix, optimization, or cache change is **B**, not C.
- A packaging migration is **C** when it does not change the public contract or package runtime behavior.

### Choose the digit

Apply these rules in order. When several effects apply, use the lowest applicable digit: **1 before 2 before 3**.

- **1 — Breaking**
  - Previously supported caller code must change, can now fail, receives different supported results, or loses a public guarantee.
  - A public name, parameter, accepted input, return guarantee, exception guarantee, or documented behavior is removed or changed incompatibly.
  - A deprecated public interface is removed.
  - Results or semantics change for inputs that were already supported, unless the pending change explicitly identifies the old result as a bug and the new result as a compatible correction.

- **2 — Compatible and observable**
  - Public functionality or supported input is added without breaking existing callers.
  - An explicitly identified bug is fixed while the supported public contract remains compatible.
  - Users can observe a compatible change in results, behavior, performance, memory use, caching, cache eviction, import timing, resource use, installation, dependencies, tooling, tests, or documentation.
  - A cache policy changes, even when returned values are unchanged.

- **3 — Unobservable**
  - Every externally observable property remains unchanged.
  - Public interfaces, typing, supported inputs, results, exceptions, documented behavior, performance, memory use, caching, cache eviction, import timing, resource use, installation, dependencies, and user or contributor workflows all remain unchanged.

Classify compatibility against the supported public contract, not every accidental behavior of the old implementation:

- A compatible exported addition is `A2`.
- Expanding supported public inputs is `A2`.
- Removing a public API, including a deprecated API, is `A1`.
- Changing results for previously supported input is `B1` unless explicitly described as a compatible bug fix.
- A compatible runtime bug fix is `B2`.
- A runtime performance, memory, import-timing, or cache-policy change is `B2`, even if output is unchanged.
- A purely structural runtime refactor with no observable runtime effect is `B3`.
- An observable documentation, dependency, tooling, or test change is `C2`.
- A purely structural build or packaging migration with no observable effect is `C3`.

Do not infer that a result change is a bug fix merely because the new result seems preferable. The pending change must explicitly identify it as a bug fix or contract-restoring correction.

## 2. Calculate the impact summary

Set `Impact:` to the lowest digit appearing in any bullet:

- If any bullet has digit `1`, write `Impact: 1`.
- Otherwise, if any bullet has digit `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Calculate the summary from the digits only. Letters do not affect it.

## 3. Sort the bullets

After classifying every change, sort the bullets in this exact order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

All A bullets must precede all B bullets, and all B bullets must precede all C bullets. When multiple changes have the same code, preserve their order from the supplied pending-change list.

## 4. Validate the finished entry

Before returning the entry, confirm all of the following:

- The heading is exactly `## [VERSION] - YYYY-MM-DD`, using the supplied version and date.
- `Impact: DIGIT` is immediately below the heading.
- Every pending change appears exactly once.
- Every bullet begins with `- [CODE]`.
- Every code contains one valid letter and one valid digit.
- Deprecated public API removal is `A1`.
- Changed semantics for previously supported input are digit `1` unless explicitly described as a compatible bug fix.
- Performance, memory, cache, cache-eviction, and import-timing changes are digit `2`, even when output is unchanged.
- Bullets follow the exact code order `A1` through `C3`.
- Changes with the same code retain their supplied order.
- The impact summary equals the lowest bullet digit.
- The final line is exactly `<!-- stl-impact: v1 -->`.
- The trailer includes both `<!--` and `-->`; plain `stl-impact: v1` is invalid.
- Nothing appears after the trailer.