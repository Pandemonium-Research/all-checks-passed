#!/usr/bin/env python3
"""Recompute the trailing-newline sensitivity check (paper §5, Figure 1, Table G1) from data/ and
check it against results/execution/sensitivity_newline.csv and the paper.

skill-check's file category deducts 5 points when a skill lacks a single trailing newline (rule
file.trailing_newline_single). The refinement loop wrote every rewrite without one, so the rule
fires on all 449 refined versions and on none of the 68 seeds. This adds the 5 points back and
repeats skill-check's execution statistics: the out-of-sample gain in R^2 over each baseline and
the partial Spearman correlation controlling for it.

usage: python3 analysis/newline.py
Exits non-zero if any value differs.
"""

from __future__ import annotations

import sys

import numpy as np

from reproduce import (DATA, EXECUTION_BASELINES, RESULTS, Checker, complete, cv_r2,
                       execution_versions, num, partial_spearman, read)

NEWLINE_RULE = "file.trailing_newline_single"
NEWLINE_POINTS = 5
OUTCOMES = (("outcome_train_mean", "execution:train"), ("outcome_heldout_mean", "execution:held-out"))
ROUNDED = 5e-5 + 1e-9  # results/ holds four decimals


def fires(row: dict) -> bool:
    return NEWLINE_RULE in (row["sc_rule_ids"] or "")


def report(chk: Checker) -> None:
    print(f"{chk.passed} values match {chk.source}")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))


def main() -> None:
    chk, paper = Checker(), Checker(source="the paper")

    # The rule fires on every refined version (all 517, including second copies) and on no seed.
    scores = {(r["run"], r["artifact"]): r for r in read(DATA / "execution/independent_scores.csv")}
    roles = [(r["artifact_role"] == "seed", fires(scores[(r["run"], r["artifact"])]))
             for r in read(DATA / "execution/versions.csv")]
    paper.close("refined versions missing the newline", sum(f for s, f in roles if not s), "449", 1e-9)
    paper.close("refined versions", sum(not s for s, _ in roles), "449", 1e-9)
    paper.close("seeds missing the newline", sum(f for s, f in roles if s), "0", 1e-9)
    paper.close("seeds", sum(s for s, _ in roles), "68", 1e-9)

    expected = {(r["scope"], r["baseline"], r["scorer"]): r
                for r in read(RESULTS / "execution/sensitivity_newline.csv")}
    versions = execution_versions()
    for outcome, scope in OUTCOMES:
        sub = complete(versions, outcome)
        y = np.array([num(r[outcome]) for r in sub])
        groups = np.array([r["run"] for r in sub])
        variants = {
            "sc_score": np.array([num(r["sc_score"]) for r in sub]),
            "sc_score_newline_adjusted": np.array(
                [num(r["sc_score"]) + (NEWLINE_POINTS if fires(r) else 0) for r in sub]),
        }
        for baseline in EXECUTION_BASELINES:
            b = np.array([num(r[baseline]) for r in sub])
            r2_base = cv_r2(b[:, None], y, groups)
            for name, x in variants.items():
                e = expected[(scope, baseline, name)]
                key = f"{scope} {name}|{baseline}"
                chk.close(f"{key} n", len(y), e["n"], 1e-9)
                chk.close(f"{key} n_distinct", len(set(x.tolist())), e["n_distinct"], 1e-9)
                chk.close(f"{key} dR2", cv_r2(np.column_stack([b, x]), y, groups) - r2_base,
                          e["delta_r2_adding_scorer"], ROUNDED)
                chk.close(f"{key} rho", partial_spearman(x, y, b), e["partial_spearman"], ROUNDED)

    report(chk)
    report(paper)
    if chk.failed or paper.failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
