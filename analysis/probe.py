#!/usr/bin/env python3
"""Recompute the cheap probe (paper §6, Appendix H) from data/ and check it against the paper.

The probe is the unrefined skill's training score v0; the refinement distance delta is the
lineage's plateau minus v0. There is no results table for the probe, so the values are checked
against Tables H1 and H2 and the cost paragraph of Appendix H, at the paper's precision.

- Table H1, one row per impact_log arm (refiner x actor), re-scored lineages only: lineages that
  accepted at least one rewrite, the Pearson correlation of v0 with delta and its square, the mean
  plateau, and the largest error of predicting delta as the mean plateau minus v0;
- Table H2: the docstring_api seeds' unrefined scores by seed quality, at 2 and 6 repetitions,
  which must separate good, medium and poor without overlap;
- cost: actor calls to score every analysed version on the 8 training instances.

usage: python3 analysis/probe.py
Exits non-zero if any value differs from the paper.
"""

from __future__ import annotations

import sys
from collections import defaultdict

import numpy as np

from reproduce import DATA, Checker, read

REFINERS = {"sol": "GPT-5.6", "opus": "Opus 5"}
TRAIN_INSTANCES = 8
# The refinement loop scored each candidate at 2 repetitions per instance, except in the
# Opus 5 x qwen arm, which used 3 (from the runs' configuration; Appendix H, Cost).
LOOP_REPS = {("opus", "qwen"): 3}
DEFAULT_LOOP_REPS = 2

# Table H1: lineages that moved, corr(v0, delta), R^2, mean plateau, largest error.
TABLE_H1 = {
    ("sol", "qwen"): (9, -0.874, 0.764, 0.883, 0.064),
    ("opus", "nemo"): (9, -0.941, 0.885, 0.909, 0.049),
    ("opus", "qwen"): (7, -0.736, 0.542, 0.857, 0.083),
    ("sol", "deepseek"): (3, -0.984, 0.969, 0.902, 0.048),
    ("sol", "muse"): (0, None, None, 0.899, None),
}
NOT_RESCORED = ("sol", "nemo")
# Table H2: (good, medium low, medium high, poor low, poor high) per refiner and repetitions.
TABLE_H2 = {
    ("sol", 2): (0.902, 0.856, 0.882, 0.658, 0.774),
    ("sol", 6): (0.904, 0.840, 0.852, 0.733, 0.802),
    ("opus", 2): (0.902, 0.862, 0.888, 0.690, 0.705),
    ("opus", 6): (0.886, 0.852, 0.862, 0.693, 0.759),
}
PAPER_COST_CALLS, PAPER_COST_PER_LINEAGE, PAPER_PROBE_CALLS = 7944, 117, 16
ROUNDED = 5e-4 + 1e-9  # the paper prints three decimals


def table_h1(chk: Checker) -> None:
    accepted = {r["run"]: int(r["n_accepted_improvements"])
                for r in read(DATA / "execution/lineage_termination.csv")}
    arms: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in read(DATA / "probe/impact_log_deltas.csv"):
        arms[(r["refiner"], r["actor"])].append(r)
    assert set(arms) == set(TABLE_H1) | {NOT_RESCORED}, sorted(arms)
    assert all(r["rescored"] == "False" for r in arms[NOT_RESCORED]), "GPT-5.6 x nemo was not re-scored"

    for arm, (moved, corr, r2, plateau, error) in TABLE_H1.items():
        rows = arms[arm]
        assert all(r["rescored"] == "True" for r in rows), arm
        label = f"H1 {REFINERS[arm[0]]} x {arm[1]}"
        v0 = np.array([float(r["v0_train_new"]) for r in rows])
        delta = np.array([float(r["delta_train_new"]) for r in rows])
        plateaus = np.array([float(r["plateau_train_new"]) for r in rows])
        n_moved = sum(accepted[r["lineage"]] > 0 for r in rows)
        # A lineage that accepted no rewrite ends where it started.
        assert all((accepted[r["lineage"]] > 0) == (float(r["delta_train_new"]) != 0) for r in rows), arm
        chk.close(f"{label} lineages", len(rows), "9", 1e-9)
        chk.close(f"{label} moved", n_moved, str(moved), 1e-9)
        chk.close(f"{label} mean plateau", float(plateaus.mean()), str(plateau), ROUNDED)
        if corr is None:  # nothing moved, so there is nothing to predict
            continue
        r = float(np.corrcoef(v0, delta)[0, 1])
        largest = float(np.max(np.abs((plateaus.mean() - v0) - delta)))
        chk.close(f"{label} corr", r, str(corr), ROUNDED)
        chk.close(f"{label} R2", r * r, str(r2), ROUNDED)
        chk.close(f"{label} largest error", largest, str(error), ROUNDED)


def table_h2(chk: Checker) -> None:
    seeds = read(DATA / "probe/rescored_lineages.csv")
    for (refiner, reps), expected in TABLE_H2.items():
        column = "v0_train_old" if reps == 2 else "v0_train_new"
        by_quality = {q: sorted(float(r[column]) for r in seeds
                                if r["refiner"] == refiner and r["seed_quality"] == q)
                      for q in ("good", "medium", "poor")}
        assert [len(v) for v in by_quality.values()] == [1, 3, 3], (refiner, by_quality)
        good, medium, poor = by_quality["good"], by_quality["medium"], by_quality["poor"]
        label = f"H2 {REFINERS[refiner]} reps {reps}"
        got = (good[0], medium[0], medium[-1], poor[0], poor[-1])
        for name, value, paper in zip(("good", "medium low", "medium high", "poor low", "poor high"),
                                      got, expected):
            chk.close(f"{label} {name}", value, str(paper), ROUNDED)
        chk.close(f"{label} no overlap", float(poor[-1] < medium[0] and medium[-1] < good[0]), "1", 1e-9)


def cost(chk: Checker) -> None:
    versions = [r for r in read(DATA / "execution/versions.csv") if r["analysis_eligible"] == "True"]
    calls = sum(TRAIN_INSTANCES * LOOP_REPS.get((r["refiner"], r["actor"]), DEFAULT_LOOP_REPS)
                for r in versions)
    lineages = len({r["run"] for r in versions})
    chk.close("cost probe calls", TRAIN_INSTANCES * DEFAULT_LOOP_REPS, str(PAPER_PROBE_CALLS), 1e-9)
    chk.close("cost loop calls", calls, str(PAPER_COST_CALLS), 1e-9)
    chk.close("cost calls per lineage", round(calls / lineages), str(PAPER_COST_PER_LINEAGE), 1e-9)


def main() -> None:
    chk = Checker(source="the paper")
    table_h1(chk)
    table_h2(chk)
    cost(chk)
    print(f"{chk.passed} values match the paper")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
