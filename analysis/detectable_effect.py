#!/usr/bin/env python3
"""Recompute the smallest detectable effects (paper §7, Figure 1's grey bars, Appendix E, Table E1)
from data/ and check them against results/scorers/minimum_detectable_effect.csv.

For every estimated partial Spearman test, the smallest correlation it detects with 80% power,
two-sided, at alpha = 0.05 and at the Holm first step (alpha divided by the family size):

- selection (17 variants per model): simulated. Draw trivariate normal samples with correlation
  rho between score and outcome, apply the same partial Spearman test, and find the rho that
  reaches 80% power by bisection (4,000 simulations per step, tolerance 0.005). The Fisher-z
  approximation with the Spearman variance factor 1.06 is given beside it (analytic_*);
- execution: (z_0.975 + z_0.80) times the lineage-bootstrap standard error, capped at 1 (with
  --bootstrap). The Fisher-z values at the number of versions and of lineages (naive_*) show what
  ignoring the clustering, or discarding the versions, would give.

usage: python3 analysis/detectable_effect.py [--bootstrap]
Exits non-zero if any value differs from results/.
"""

from __future__ import annotations

import argparse
import math
import sys

import numpy as np
from scipy.stats import norm

from reproduce import (ACTORS, DATA, EXECUTION_BASELINES, EXECUTION_SCORERS, RESULTS,
                       SELECTION_BASELINES, SELECTION_SCORERS, Checker, bootstrap_draws, complete,
                       execution_versions, family, num, partial_spearman, rates_from, read,
                       selection_rows, t_pvalue)

POWER, ALPHA = 0.80, 0.05
SIMULATIONS, SIMULATION_SEED, SIMULATION_TOLERANCE = 4_000, 20261001, 0.005
ROUNDED = 5e-5 + 1e-9  # results/ holds four decimals


def analytic_mde(n: int, alpha: float) -> float:
    critical = norm.ppf(1.0 - alpha / 2.0) + norm.ppf(POWER)
    return float(math.tanh(critical * math.sqrt(1.06 / (n - 4))))


def bootstrap_mde(se: float, alpha: float) -> float:
    return min(1.0, float((norm.ppf(1.0 - alpha / 2.0) + norm.ppf(POWER)) * se))


def simulated_power(n: int, rho: float, alpha: float, rng: np.random.Generator) -> float:
    covariance = np.array([[1.0, rho, 0.0], [rho, 1.0, 0.0], [0.0, 0.0, 1.0]])
    rejections = 0
    for s in rng.multivariate_normal(np.zeros(3), covariance, size=(SIMULATIONS, n)):
        p = t_pvalue(partial_spearman(s[:, 0], s[:, 1], s[:, 2]), n)
        rejections += p is not None and p < alpha
    return rejections / SIMULATIONS


def simulated_mde(n: int, alpha: float) -> float:
    rng = np.random.default_rng(SIMULATION_SEED)
    low, high = 0.0, 0.99
    if simulated_power(n, high, alpha, rng) < POWER:
        return high
    while high - low > SIMULATION_TOLERANCE:
        midpoint = (low + high) / 2.0
        if simulated_power(n, midpoint, alpha, rng) >= POWER:
            high = midpoint
        else:
            low = midpoint
    return high


def scopes():
    """(corpus, scope, rows, outcome, scorers, baselines, group) for each Holm family."""
    rates = rates_from(read(DATA / "selection/claude_code_cells.csv"), "triggered")
    for actor in ACTORS:
        yield ("B", f"invocation:{actor}", selection_rows(rates, actor), "outcome_invocation_rate",
               SELECTION_SCORERS, SELECTION_BASELINES, "variant")
    versions = execution_versions()
    for outcome, scope in (("outcome_heldout_mean", "execution:held-out"),
                           ("outcome_train_mean", "execution:train")):
        yield ("A", scope, [r for r in versions if num(r[outcome]) is not None], outcome,
               EXECUTION_SCORERS, EXECUTION_BASELINES, "run")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", action="store_true")
    args = parser.parse_args()
    chk = Checker()
    expected = {(r["scope"], r["scorer"], r["control"]): r
                for r in read(RESULTS / "scorers/minimum_detectable_effect.csv")}
    simulated: dict[tuple[int, float], float] = {}
    n_estimated = 0

    for corpus, scope, rows, outcome, scorers, baselines, group in scopes():
        partial, _ = family(rows, outcome, scorers, baselines, group)
        family_size = sum(p["p_value"] is not None for p in partial)
        holm_alpha = ALPHA / family_size
        for p in partial:
            if p["partial_spearman"] is None:  # a constant score has no test
                assert (scope, p["scorer"], p["control"]) not in expected
                continue
            n_estimated += 1
            e = expected[(scope, p["scorer"], p["control"])]
            key = f"{scope} {p['scorer']}|{p['control']}"
            sub = complete(rows, p["scorer"], outcome, p["control"])
            n, n_groups = len(sub), len({r[group] for r in sub})
            chk.close(f"{key} n", n, e["n"], 1e-9)
            chk.close(f"{key} n_groups", n_groups, e["n_groups"], 1e-9)
            chk.close(f"{key} holm_family_size", family_size, e["holm_family_size"], 1e-9)
            chk.close(f"{key} rho", p["partial_spearman"], e["partial_spearman"], ROUNDED)
            if corpus == "B":
                for threshold in (ALPHA, holm_alpha):
                    if (n, threshold) not in simulated:
                        simulated[(n, threshold)] = simulated_mde(n, threshold)
                mde = simulated[(n, ALPHA)]
                chk.close(f"{key} mde", mde, e["mde_alpha05"], ROUNDED)
                chk.close(f"{key} mde holm", simulated[(n, holm_alpha)], e["mde_holm_first_step"], ROUNDED)
                chk.close(f"{key} analytic", analytic_mde(n, ALPHA), e["analytic_mde_alpha05"], ROUNDED)
                chk.close(f"{key} analytic holm", analytic_mde(n, holm_alpha),
                          e["analytic_mde_holm_first_step"], ROUNDED)
            else:
                chk.close(f"{key} naive versions", analytic_mde(n, ALPHA),
                          e["naive_mde_versions_alpha05"], ROUNDED)
                chk.close(f"{key} naive lineages", analytic_mde(n_groups, ALPHA),
                          e["naive_mde_lineages_alpha05"], ROUNDED)
                if not args.bootstrap:
                    continue
                x, y, z = (np.array([num(r[c]) for r in sub]) for c in (p["scorer"], outcome, p["control"]))
                se = float(np.std(bootstrap_draws(x, y, z, np.array([r[group] for r in sub])), ddof=1))
                mde = bootstrap_mde(se, ALPHA)
                chk.close(f"{key} se", se, e["se"], ROUNDED)
                chk.close(f"{key} mde", mde, e["mde_alpha05"], ROUNDED)
                chk.close(f"{key} mde holm", bootstrap_mde(se, holm_alpha), e["mde_holm_first_step"], ROUNDED)
            chk.same(f"{key} detectable", abs(p["partial_spearman"]) >= mde, e["abs_rho_ge_mde_alpha05"])
    assert n_estimated == len(expected), (n_estimated, len(expected))

    print(f"{chk.passed} values match results/")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
