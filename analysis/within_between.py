#!/usr/bin/env python3
"""Recompute the within- and between-lineage decomposition (paper §5, Figure 2, Appendix E,
Table G3) from data/ and check it against results/execution/.

For each score and execution outcome (training or held-out mean), over the analysed versions:

- within-lineage: centre the score and the outcome on their lineage's mean, then take the Spearman
  correlation of what remains (how performance moves as the refiner changes a skill);
- between-lineage: the Spearman correlation of the 68 lineage means;
- arm-centred between-lineage: centre the lineage means on their arm's mean (actor x refiner)
  before correlating, so that differences between arms drop out;
- with --bootstrap, a 95% percentile interval for the arm-centred value: lineages are resampled
  with replacement within their own arm (10,000 draws) and each arm is re-centred in every draw.

within_between.csv repeats each score once per baseline, because a row needs the baseline as well
as the score and the outcome to be present; the values are the same.

usage: python3 analysis/within_between.py [--bootstrap]
Exits non-zero if any value differs from results/.
"""

from __future__ import annotations

import argparse
import sys

import numpy as np
from scipy.stats import spearmanr

from reproduce import (BOOTSTRAP_DRAWS, BOOTSTRAP_SEED, EXECUTION_BASELINES, EXECUTION_SCORERS,
                       RESULTS, Checker, complete, execution_versions, num, read)

SCOPES = (("outcome_heldout_mean", "execution:held-out"), ("outcome_train_mean", "execution:train"))
# Our own body features, decomposed the same way for Figure 2.
OUR_FEATURES = ("has_numbered_steps", "body_line_count", "imperative_opener_count",
                "has_worked_example", "has_code_block")
ROUNDED = 5e-5 + 1e-9  # results/ holds four decimals
LOW_RANGE = 5  # fewer distinct values than this marks a score as low-range


def spearman(x: np.ndarray, y: np.ndarray) -> float | None:
    if len(x) < 2 or np.allclose(x, x[0]) or np.allclose(y, y[0]):
        return None
    value = float(spearmanr(x, y).statistic)
    return None if np.isnan(value) else value


def lineage_means(rows: list[dict], outcome: str, scorer: str, *also: str):
    """Versions grouped by lineage (sorted), with each lineage's arm and mean score and outcome."""
    sub = complete(rows, scorer, outcome, *also)
    x = np.array([num(r[scorer]) for r in sub])
    y = np.array([num(r[outcome]) for r in sub])
    lineages: dict[str, list[int]] = {}
    for i, r in enumerate(sub):
        lineages.setdefault(r["run"], []).append(i)
    keys = sorted(lineages)
    arms = np.array([f"{sub[lineages[k][0]]['actor']}|{sub[lineages[k][0]]['refiner']}" for k in keys])
    return x, y, [lineages[k] for k in keys], arms


def centre(mean_x: np.ndarray, mean_y: np.ndarray, arms: np.ndarray) -> float | None:
    cx, cy = mean_x.copy(), mean_y.copy()
    for arm in set(arms):
        mask = arms == arm
        if mask.sum() > 1:
            cx[mask] = mean_x[mask] - mean_x[mask].mean()
            cy[mask] = mean_y[mask] - mean_y[mask].mean()
    return spearman(cx, cy)


def decompose(rows: list[dict], outcome: str, scorer: str, *also: str) -> dict:
    x, y, groups, arms = lineage_means(rows, outcome, scorer, *also)
    within_x = np.concatenate([x[g] - x[g].mean() for g in groups])
    within_y = np.concatenate([y[g] - y[g].mean() for g in groups])
    mean_x = np.array([x[g].mean() for g in groups])
    mean_y = np.array([y[g].mean() for g in groups])
    within, between = spearman(within_x, within_y), spearman(mean_x, mean_y)
    status = "estimated"
    if within is None and between is None:
        status = "uninformative (low range)" if len(set(x)) < LOW_RANGE else "uninformative"
    return {"n": len(x), "n_lineages": len(groups), "n_arms": len(set(arms)), "within_lineage": within,
            "between_lineage": between, "between_lineage_within_arm": centre(mean_x, mean_y, arms),
            "status": status, "means": (mean_x, mean_y, arms)}


def arm_interval(mean_x: np.ndarray, mean_y: np.ndarray, arms: np.ndarray) -> tuple[float, float, int]:
    members = [np.flatnonzero(arms == arm) for arm in sorted(set(arms))]
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    draws = []
    for _ in range(BOOTSTRAP_DRAWS):
        picked = np.concatenate([rng.choice(idx, size=len(idx), replace=True) for idx in members])
        value = centre(mean_x[picked], mean_y[picked], arms[picked])
        if value is not None:
            draws.append(value)
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return float(lo), float(hi), len(draws)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", action="store_true")
    args = parser.parse_args()
    chk = Checker()
    versions = execution_versions()
    by_control = {(r["scope"], r["scorer"], r["control"]): r
                  for r in read(RESULTS / "execution/within_between.csv")}
    by_arm = {(r["scope"], r["scorer"]): r for r in read(RESULTS / "execution/within_between_arm.csv")}
    assert len(by_control) == len(SCOPES) * len(EXECUTION_SCORERS) * len(EXECUTION_BASELINES)
    assert len(by_arm) == len(SCOPES) * (len(EXECUTION_SCORERS) + len(OUR_FEATURES))

    for outcome, scope in SCOPES:
        rows = [r for r in versions if num(r[outcome]) is not None]
        for scorer in EXECUTION_SCORERS:
            for control in EXECUTION_BASELINES:
                got, e = decompose(rows, outcome, scorer, control), by_control[(scope, scorer, control)]
                key = f"{scope} {scorer}|{control}"
                for field in ("n", "n_lineages", "within_lineage", "between_lineage"):
                    chk.close(f"{key} {field}", got[field], e[field], ROUNDED)
                chk.same(f"{key} status", got["status"], e["status"])

        for scorer in EXECUTION_SCORERS + OUR_FEATURES:
            got, e = decompose(rows, outcome, scorer), by_arm[(scope, scorer)]
            key = f"{scope} {scorer} arm"
            chk.same(f"{key} status", got["status"], e["status"])
            if got["status"] != "estimated":  # a constant score has nothing to decompose
                continue
            for field in ("n", "n_lineages", "n_arms", "within_lineage", "between_lineage",
                          "between_lineage_within_arm"):
                chk.close(f"{key} {field}", got[field], e[field], ROUNDED)
            if args.bootstrap:
                lo, hi, draws = arm_interval(*got["means"])
                chk.close(f"{key} ci_low", lo, e["arm_ci_low"], ROUNDED)
                chk.close(f"{key} ci_high", hi, e["arm_ci_high"], ROUNDED)
                chk.close(f"{key} draws", draws, e["arm_ci_draws"], 1e-9)

    print(f"{chk.passed} values match results/")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
