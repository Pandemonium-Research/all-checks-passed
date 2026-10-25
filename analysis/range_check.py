#!/usr/bin/env python3
"""Recompute how many distinct values each score takes (paper §5, Appendix F, Table G1, Figure 1)
from data/ and check it against results/scorers/range_check.csv.

A score with fewer than 5 distinct values in a scope is marked low-range: skill-check's description
category takes two values across the 17 selection variants, and its body category one value (the
full 20 points) across all execution versions, which Figure 1 shows as "n/a (constant)".

usage: python3 analysis/range_check.py
Exits non-zero if any value differs from results/.
"""

from __future__ import annotations

import sys

from reproduce import (ACTORS, DATA, EXECUTION_SCORERS, RESULTS, SELECTION_SCORERS, Checker,
                       execution_versions, num, rates_from, read, selection_rows)

LOW_RANGE = 5


def main() -> None:
    chk = Checker()
    expected = {(r["scope"], r["scorer"]): r for r in read(RESULTS / "scorers/range_check.csv")}
    rates = rates_from(read(DATA / "selection/claude_code_cells.csv"), "triggered")
    scopes = [(f"invocation:{actor}", selection_rows(rates, actor), SELECTION_SCORERS) for actor in ACTORS]
    versions = execution_versions()
    for outcome, scope in (("outcome_heldout_mean", "execution:held-out"),
                           ("outcome_train_mean", "execution:train")):
        scopes.append((scope, [r for r in versions if num(r[outcome]) is not None], EXECUTION_SCORERS))
    assert sum(len(s) for _, _, s in scopes) == len(expected)

    for scope, rows, scorers in scopes:
        for scorer in scorers:
            values = [num(r.get(scorer)) for r in rows]
            distinct = len({v for v in values if v is not None})
            low = distinct < LOW_RANGE
            e, key = expected[(scope, scorer)], f"{scope} {scorer}"
            chk.close(f"{key} n_rows", len(values), e["n_rows"], 1e-9)
            chk.close(f"{key} n_distinct_non_null", distinct, e["n_distinct_non_null"], 1e-9)
            chk.close(f"{key} null_count", sum(v is None for v in values), e["null_count"], 1e-9)
            chk.same(f"{key} low_range", low, e["low_range"])
            chk.same(f"{key} status", "low_range" if low else "available", e["status"])

    print(f"{chk.passed} values match results/")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
