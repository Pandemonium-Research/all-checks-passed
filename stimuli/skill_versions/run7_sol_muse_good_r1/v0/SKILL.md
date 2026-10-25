---
name: impact-log
description: Use this skill when writing release notes, changelog entries, or version history for this project, so that entries follow the team's house impact-log format and downstream tooling can parse them.
---

# Release notes

We keep release notes in the house impact-log format. Everyone on the team is expected to use
it, and it has been in place for a while now, so please match what is already in the file.

The main thing is the impact codes. Each bullet gets a code in square brackets, made of a letter
and a digit. On the letter side we use A when the change touches the public API — that means the
names, signatures or types of anything the package exports — while B covers cases where the
runtime behavior of an existing call changes without its signature changing, and anything that is
only build, packaging, tooling, tests or documentation is C. The digit side works similarly: 1 is
for breaking changes, by which we mean caller code that used to work can now fail or come back
with a different result, 2 is the compatible case where something is additive or is a fix and
correct existing code carries on working, and 3 is for changes no caller can observe at all.
Use your judgement on which one applies; usually it is obvious from the change description.

Sometimes a change could arguably take more than one letter, or more than one digit. There is a
convention for resolving that, based on precedence, so pick the one that comes first — the
letters run in alphabetical order for this purpose and the digits run from low to high.

Entries are headed with the version and the date. We write the version in square brackets and
follow it with the date after a hyphen, at the second heading level, with the version in the
usual three-part form and the date in the year-month-day form that sorts properly. There is also
an impact summary line beneath the heading, written as the word Impact followed by a colon and a
number, and the number to use there is whichever digit in the entry is the lowest one. Bullets
should appear in a sensible order rather than the order the changes happened to be listed in;
sort them by their codes, ascending.

Don't forget the trailer comment at the end — the parser needs it, and it has to be the very last
line. It is an HTML comment reading `stl-impact: v1`.
