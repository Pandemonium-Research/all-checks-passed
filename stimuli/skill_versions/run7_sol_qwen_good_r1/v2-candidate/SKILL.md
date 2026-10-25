---
name: impact-log
description: Use this skill to convert a supplied release version, date, and list of pending changes into one correctly classified, sorted, and machine-parseable release-notes entry.
---

# Release notes

Produce exactly one release entry. Include every supplied change exactly once; do not add, omit, or combine changes.

## Output format

Write the entry in this exact layout:

    ## [VERSION] - YYYY-MM-DD
    Impact: DIGIT

    - [CODE] Change description.
    - [CODE] Change description.

    <!-- stl-impact: v1 -->

Formatting requirements:

- Replace `VERSION` with the supplied three-part version number.
- Replace `YYYY-MM-DD` with the supplied date.
- Do not put backticks around the heading, impact value, codes, or trailer.
- Put each impact code at the beginning of its bullet, before the description. Never put a code at the end.
- Leave one blank line after the impact line and one blank line before the trailer.
- Make `<!-- stl-impact: v1 -->` the final line, with nothing after it.

## Classify each change

Assign exactly one code to each change. A code contains one letter followed by one digit.

Choose the letter first:

- `A` — The public API surface changes, including exported names, function or method signatures, parameters, return types, or other public types.
- `B` — The runtime behavior of an existing call changes, but its public API surface does not.
- `C` — The change is limited to internals, build, packaging, dependencies, tooling, tests, or documentation.

Then choose the digit:

- `1` — Breaking: caller code that previously worked can now fail or produce a different result.
- `2` — Compatible: the change is additive or a fix, and correct existing caller code continues to work.
- `3` — Unobservable: callers cannot observe the change.

Combine the letter and digit, for example `[A2]`.

Apply these precedence rules when multiple classifications appear possible:

- Prefer `A` over `B`, and `B` over `C`.
- Prefer digit `1` over `2`, and `2` over `3`.

Classify every change independently. Do not copy the release-level impact digit onto every bullet.

## Sort the bullets

After assigning all codes, reorder the bullets by this exact sequence:

`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `C1`, `C2`, `C3`

Do not preserve the supplied change order when it conflicts with this sequence. Keep the supplied relative order only among changes that have the same code.

## Calculate the impact summary

Set `Impact` to the lowest digit present in any bullet:

- If any code ends in `1`, write `Impact: 1`.
- Otherwise, if any code ends in `2`, write `Impact: 2`.
- Otherwise, write `Impact: 3`.

Ignore the code letters when calculating this summary.

## Final check

Before returning the entry, verify that:

- The supplied version and date are unchanged.
- Every supplied change appears exactly once.
- Every bullet starts with one valid code.
- Bullets follow the required code sequence.
- `Impact` is the lowest digit used.
- The trailer is present and is the final line.