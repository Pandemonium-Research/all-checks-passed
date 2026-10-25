---
name: impact-log
description: Use this skill to turn a release version, date, and list of pending changes into a classified, sorted, parser-compatible release-notes entry in the project's impact-log format.
---

# Release notes

Write exactly one entry in this structure:

## [`VERSION`] - `YYYY-MM-DD`
Impact: `DIGIT`
- [`CODE`] Change description.
<!-- stl-impact: v1 -->

Replace the placeholders with the supplied values. The version must have three numeric parts, and the date must use ISO `YYYY-MM-DD` format. Include no text before the heading or after the trailer.

## Classify every change

Each bullet begins with one code consisting of a scope letter and an impact digit, such as `[A2]`. Choose the letter and digit independently.

### Scope letter

- **A — Public API:** Anything users import or rely on as part of the public interface. This includes exported names, signatures, parameters, return types, exceptions, annotations, and whether shipped type information is discoverable by type checkers.
- **B — Runtime:** Runtime code or the implementation of existing calls when the public API itself is unchanged. This includes bug fixes, performance improvements, caching, and other internal runtime changes.
- **C — Project support:** Builds, packaging, dependencies, installation artifacts, release infrastructure, tooling, tests, or documentation.

If multiple scopes apply, use the earliest letter: **A before B before C**.

Important distinctions:

- Adding an exported function or other public name is **A**, not B.
- Adding `py.typed` or otherwise exposing shipped annotations to type checkers is **A**, even though a packaging file is involved.
- Fixing an existing function without changing its public interface is **B**.
- Adding wheels, changing vendored dependencies, or otherwise changing distributed or installed artifacts is **C**, unless the change exposes part of the public API.

### Impact digit

- **1 — Breaking:** Previously supported caller code must change, can now fail, or receives behavior incompatible with the documented contract.
- **2 — Compatible and observable:** The change is additive, corrects faulty behavior, improves observable performance, or makes an observable packaging or installation change without breaking supported callers.
- **3 — Unobservable to callers:** Only internal implementation, tests, tooling, or documentation changes, with no change to supported results, errors, side effects, performance, installation, or public behavior.

If multiple impacts apply, use the lowest digit: **1 before 2 before 3**.

Important distinctions:

- An ordinary bug fix is **2**, not 1. A corrected result is breaking only if callers were entitled to rely on the old behavior as part of the documented contract.
- A new compatible public API is **2**.
- A runtime performance improvement is **2** when callers can observe it.
- Replacing an internal implementation while preserving behavior and performance is **3**.
- Publishing an additional wheel or changing another installation artifact is **2**, not 3.
- Moving tests or improving documentation without changing caller-visible behavior is **3**.

Do not classify a change as breaking merely because its output differs from buggy, undocumented behavior. Use impact 1 only when supported callers lose compatibility.

## Assemble the entry

1. Write exactly one bullet for each pending change.
2. Format every bullet as `- [A2] Description.`
3. Sort bullets by code: A before B before C, then 1 before 2 before 3. Preserve the supplied order among bullets with the same code.
4. Set `Impact` to the lowest digit used by any bullet.
5. Put `<!-- stl-impact: v1 -->` on the final line.

Before returning the entry, verify that:

- The heading contains the supplied three-part version and ISO date.
- Every pending change appears exactly once.
- Every bullet has exactly one valid two-character code.
- Scope and impact were classified independently.
- Bullets are sorted by letter and then digit.
- `Impact` equals the lowest bullet digit.
- The trailer is present and is the final line.