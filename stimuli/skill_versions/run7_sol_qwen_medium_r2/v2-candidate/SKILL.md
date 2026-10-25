---
name: impact-log
description: Use this document to classify pending project changes and write a correctly formatted, machine-parseable release-notes entry for a supplied version and date.
---

# Release notes

Create one release entry from the supplied version, date, and pending changes. Include exactly one bullet for each pending change.

Use this structure exactly:

```text
## [VERSION] - YYYY-MM-DD
Impact: DIGIT
- [CODE] Change description.
<!-- stl-impact: v1 -->
```

Replace every placeholder. Do not include the code fence in the finished entry.

## 1. Classify each change

Each code consists of one letter and one digit. Choose them independently: the letter identifies what changed, while the digit identifies its compatibility or visibility.

### Choose the letter

Apply these rules in order. When more than one category applies, use the first matching letter: **A before B before C**.

- **A — Public interface or typing contract**
  - Adds, removes, or renames an exported name.
  - Changes a public signature, parameter, return value, accepted input type, exception contract, or annotation.
  - Expands the kinds of input a public operation supports.
  - Adds or changes shipped typing information, including marking the package as typed.

- **B — Package runtime behavior or implementation**
  - Fixes a runtime bug without changing the public interface contract.
  - Changes the behavior of an existing operation.
  - Changes performance, caching, import timing, or another runtime characteristic.
  - Refactors an internal runtime implementation, even if callers cannot observe a difference.

- **C — Work outside the package runtime**
  - Changes builds, packaging, dependencies, development tooling, tests, or documentation.
  - Does not change the public interface contract or package runtime behavior.

Important distinctions:

- A newly exported operation is **A**, not B.
- Supporting an additional public input type is **A**, even if the signature text is unchanged.
- A runtime bug fix or internal runtime optimization is **B**, not C.
- A packaging migration is **C** when installation behavior and runtime behavior remain unchanged.

### Choose the digit

Apply these rules in order. When several effects apply, use the lowest applicable digit: **1 before 2 before 3**.

- **1 — Breaking**
  - Previously supported caller code must change, can now fail, or loses behavior guaranteed by the public contract.
  - A public name, parameter, accepted input, return guarantee, or documented behavior is removed or changed incompatibly.

- **2 — Compatible and observable**
  - Public functionality or supported input is added without breaking existing callers.
  - A bug is fixed while valid existing caller code remains compatible.
  - Users can observe a compatible change in results, performance, installation, dependencies, tooling, or documentation.

- **3 — Unobservable**
  - The change produces no externally observable difference.
  - Public signatures, supported inputs, results, installation behavior, and documented behavior remain unchanged.

Classify compatibility against the supported public contract, not against every accidental behavior of the old implementation:

- A compatible addition is digit **2**, not 1.
- Expanding accepted inputs is digit **2**, not 1.
- A bug fix is digit **2** unless it also breaks a supported contract.
- An internal cache or refactor with unchanged observable behavior is digit **3**.

Examples of resulting code patterns:

- Compatible exported API addition: `A2`
- Compatible expansion of an accepted public input type: `A2`
- Compatible runtime bug fix: `B2`
- Observable runtime performance improvement: `B2`
- Unobservable internal runtime refactor: `B3`
- Observable documentation or dependency change: `C2`
- Unobservable build or packaging migration: `C3`

## 2. Calculate the impact summary

Set `Impact:` to the lowest digit appearing in any bullet.

For example:

- Digits 1, 2, and 3 produce `Impact: 1`.
- Digits 2 and 3 produce `Impact: 2`.
- Only digit 3 produces `Impact: 3`.

Calculate the summary from the digits only. Letters do not affect it.

## 3. Sort the bullets

Sort bullets by code in this exact ascending order:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

When multiple changes have the same code, preserve their supplied order.

## 4. Validate the finished entry

Before returning the entry, confirm all of the following:

- The heading is exactly `## [VERSION] - YYYY-MM-DD`, using the supplied version and date.
- `Impact: DIGIT` is immediately below the heading.
- Every pending change appears once.
- Every bullet begins with `- [CODE]`.
- Every code contains one valid letter and one valid digit.
- Bullets are sorted by code.
- The impact summary equals the lowest bullet digit.
- The final line is exactly `<!-- stl-impact: v1 -->`.
- The trailer includes both `<!--` and `-->`; plain `stl-impact: v1` is invalid.
- Nothing appears after the trailer.