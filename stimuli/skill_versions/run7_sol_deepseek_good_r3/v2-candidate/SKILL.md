---
name: impact-log
description: Use this skill to turn a supplied version number, release date, and list of pending project changes into a correctly classified, parseable release-notes entry in the team's house impact-log format.
---

# Release notes

Create one entry containing every pending change, using this exact layout:

## [version] - YYYY-MM-DD

Impact: N

- [code] Change description.
- [code] Change description.

<!-- stl-impact: v1 -->

Use the supplied three-part version number and date exactly. Preserve the blank lines shown above. The trailer must be the final line, with nothing after it.

## Classify every change

Each bullet receives one letter and one digit. Choose them independently.

### Letter: what changed?

- **A — Public API:** An exported name, signature, parameter, return type, accepted input type, or other public type was added, removed, renamed, or modified.
- **B — Runtime behavior:** The public API is unchanged, but an existing call can produce different behavior or results.
- **C — Non-API work:** The change concerns implementation internals, performance, builds, packaging, distribution, tooling, tests, or documentation without changing the public API or an existing call's behavior.

If more than one letter seems applicable, use the earliest: **A before B before C**.

In particular:

- Adding a new exported function, class, method, or constant is **A**.
- Broadening or narrowing the inputs accepted by a public function is **A**, even if its written signature is unchanged.
- Correcting an existing function's output without changing its API is **B**.
- Internal caching or refactoring with identical public results is **C**.
- Publishing new distribution artifacts or changing packaging without changing the public API is **C**.

### Digit: how disruptive is it?

- **1 — Breaking:** Previously valid usage can now fail, become invalid, or intentionally produce an incompatible result.
- **2 — Compatible and observable:** The change adds a usable capability, expands compatibility, or fixes incorrect behavior while correct existing usage continues to work.
- **3 — Unobservable:** Users receive no new capability and observe no changed behavior or compatibility.

If more than one digit seems applicable, use the lowest: **1 before 2 before 3**.

Do not use **1** merely because a feature is new or a result changed. Apply these rules:

- Adding public API is compatible: **A2**, not A1.
- Expanding the accepted inputs of public API is compatible: **A2**, not A1.
- Fixing incorrect runtime behavior without an API change is **B2**, not B1.
- Intentionally changing previously correct runtime behavior incompatibly is **B1**.
- An internal optimization with unchanged results and signature is **C3**.
- A packaging or distribution addition that users can use, such as support for another installation target, is **C2**.
- A packaging migration with unchanged installation compatibility is **C3**.
- Moving or reorganizing tests or tooling with no user-visible effect is **C3**.

## Write and order the entry

- Write one concise bullet for each pending change.
- Do not omit changes or merge unrelated changes.
- Begin every bullet with its code in square brackets.
- Sort bullets by letter and then digit: A codes before B codes, and B codes before C codes. Within a letter, digit 1 precedes 2, which precedes 3.
- Preserve the supplied order for changes that receive the same code.
- Set `Impact` to the lowest digit appearing in any bullet, regardless of letter.
- Write the trailer exactly as `<!-- stl-impact: v1 -->`.