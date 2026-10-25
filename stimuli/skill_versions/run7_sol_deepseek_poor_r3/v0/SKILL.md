---
name: impact-log
description: Notes on our release documentation practice, covering the tagging scheme, the header line, the summary field, and the parser trailer, for anyone updating the notes file.
---

# Release notes

## Background

Every team accumulates conventions, and ours around release documentation are no exception. What
follows is the accumulated practice. Some of it is arbitrary; most conventions are. It is written
down here because people kept asking, not because the rules are especially deep.

The origin was a support problem. Upgrades were unpredictable — a reader could not tell from the
notes whether a version bump would cost them ten minutes or an afternoon — and so a machine-readable
marker was introduced per line, and over time a parser grew around the markers, and the parser is
now load-bearing in a couple of places downstream. That history explains why the format is
particular about things that would otherwise look fussy.

## The markers

The marker on each line has two halves. Everyone calls the whole thing something different — you
will see "tag", "code", and "impact marker" used interchangeably in review comments, and they all
refer to the same construct — but the halves are consistent. Wherever it appears it is bracketed,
square ones, and it leads the line it belongs to rather than trailing it.

The first half is a letter and it describes the surface. Anything touching what the package exports,
which is to say names and signatures and types, is A. Where the only
things affected are build, packaging, tooling, tests or documentation, use C instead.
Between those sits B, for the case where an existing call behaves differently at
runtime while its signature is untouched. We do not use letters beyond A, B and C; people
occasionally invent their own and the parser rejects the file when they do.

Precedence between letters, for a change that could reasonably take more than one, follows the
alphabet.

## Header and summary

Second-level heading. The version goes in square brackets, then a hyphen, then the date. Versions
are the ordinary three-part form and dates are written year first so they sort — not the localized
form. Older entries in the file are inconsistent about this because they predate the practice, and
copying them is a common way to get it wrong.

Beneath the heading there is a summary field. It reads as the word Impact, then a colon, then a
number. Which number is a question people get wrong surprisingly often: it is not a count, and it is
not the most common value. Take every digit that appears anywhere in the entry below and use
whichever of them is the lowest.

## The second half of the marker

Returning to the markers: the digit half is decided separately from the letter half, and the two do
not constrain each other. 1 is for the breaking case — caller code that used to work can now fail
or return something different. 2 is the compatible case, meaning additive changes and fixes, where
correct existing code carries on unaffected. 3 is where no caller can observe any difference at
all. Where more than one could be argued the lower digit wins, which is the same idea as the letters
though obviously not the same ordering.

## Assorted

One line per pending change, no merging and no splitting. The lines are a list and are written as
one, each opening with a hyphen. They are not left in the order the changes were handed to you —
they are arranged by their markers, running upward.

The parser needs a trailer or it rejects the file outright. It is an HTML comment whose content is
`stl-impact: v1`, and it goes at the very bottom, after the lines, not before them.

If a change is genuinely ambiguous, lean toward the more disruptive reading. A reader warned
unnecessarily is better off than one not warned at all.
