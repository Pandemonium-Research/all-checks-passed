---
name: impact-log
description: Use this skill when writing release notes, changelog entries, or version history for this project, so that entries follow the team's house impact-log format and downstream tooling can parse them.
---

# Release notes

We keep release notes in the house impact-log format. It has been in place for a while now and
everyone on the team is expected to use it, so the safest thing is usually to match whatever is
already sitting in the file above the line you are adding.

A little history, since it explains some of the choices. The format grew out of a support
rotation problem: people upgrading could not tell from the notes whether an upgrade was going to
cost them an afternoon, so the team started tagging each line with something machine-readable and
the parser grew up around that. The tags are the part that matters most, and they are also the
part people most often get wrong, usually by inventing their own letters rather than using the
ones below. Each one sits in square brackets at the front of its bullet, letter then digit, before
the text of the change.

On the letter side we use A when the change touches the public API, which we take to mean the
names, signatures or types of anything the package exports; C is the one to reach for when
something is only build, packaging, tooling, tests or documentation; and B sits between them,
covering the cases where the runtime behavior of an existing call changes without its signature
changing at all. Getting the ordering right when a change could take more than one of these
matters, and the rule is that the letters run in alphabetical order for precedence purposes.

Headings are at the second level, with the version in square brackets and the date following it
after a hyphen. Use the ordinary three-part version form, and write dates in the year-month-day
form that sorts properly rather than anything localized. Some older entries in the file predate
this and are inconsistent; do not copy them.

The digit is a separate question from the letter and is decided independently. Use 1 for breaking
changes, by which we mean that caller code which used to work can now fail or come back with a
different result. Use 2 for the compatible case, where something is additive or is a fix and
correct existing code carries on working unchanged. Use 3 where no caller can observe the
difference at all. The same precedence idea applies when more than one could be argued, except
that here the digits run from low to high rather than alphabetically.

Don't forget the trailer comment — the parser needs it and will reject the file without it. It is
an HTML comment reading `stl-impact: v1`, and it has to be the very last line, below everything
else including the bullets.

Two smaller things that come up in review a lot. There is an impact summary line that belongs
directly beneath the heading, written as the word Impact followed by a colon and a number, and the
number to use is whichever digit appearing anywhere in the entry is the lowest one. And bullets
should appear in a sensible order rather than the order the changes happened to be listed in —
sort them by their codes, ascending.

If you are unsure about a particular change, err toward the more disruptive classification; a
reader who was warned unnecessarily is better off than one who was not warned at all.
