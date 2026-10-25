#!/usr/bin/env python3
"""Recompute the lineage-clustered execution associations (paper §5, Appendix E, Table G2) from
data/ and check them against results/execution/clustered_associations.csv.

Versions are nested in 68 refinement lineages, so per-version p-values overstate precision. For
each body signal controlled for the incumbent, and for the incumbent controlled for description
word count, on each execution outcome:

- per_version: the partial Spearman correlation over versions, which must equal the pooled row of
  results/execution/associations.csv (published);
- lineage_mean: the same correlation over the 68 lineage means;
- within_lineage, between_lineage and between_lineage_within_arm: plain Spearman correlations, as
  in within_between.py, without the control;
- between_x_vs_seed_quality: the lineage-mean score against seed quality (poor 0, medium 1, good 2);
- with --bootstrap, a 95% interval from 10,000 resamples of whole lineages (cluster_ci_lo/hi).

usage: python3 analysis/clustered.py [--bootstrap]
Exits non-zero if any value differs from results/.
"""

from __future__ import annotations

import argparse
import sys

import numpy as np

from reproduce import (RESULTS, Checker, complete, execution_versions, lineage_bootstrap, num,
                       partial_spearman, read)
from within_between import centre, spearman

# (score, control) as the pooled table pairs them; the last is the reverse comparison.
PAIRS = (
    ("has_numbered_steps", "conformance_overall"),
    ("body_line_count", "conformance_overall"),
    ("body_token_count", "conformance_overall"),
    ("has_code_block", "conformance_overall"),
    ("has_worked_example", "conformance_overall"),
    ("imperative_opener_count", "conformance_overall"),
    ("description_word_count", "conformance_overall"),
    ("description_trigger_cue_count", "conformance_overall"),
    ("conformance_overall", "description_word_count"),
)
OUTCOMES = ("outcome_train_mean", "outcome_heldout_mean")
SEED_RANK = {"poor": 0, "medium": 1, "good": 2}
ROUNDED = 5e-5 + 1e-9  # results/ holds four decimals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", action="store_true")
    args = parser.parse_args()
    chk = Checker()
    versions = execution_versions()
    expected = {(r["outcome"], r["scorer"]): r
                for r in read(RESULTS / "execution/clustered_associations.csv")}
    pooled = {(r["outcome"], r["scorer"], r["control"]): r
              for r in read(RESULTS / "execution/associations.csv") if r["analysis_scope"] == "pooled"}

    for outcome in OUTCOMES:
        for scorer, control in PAIRS:
            sub = complete(versions, scorer, outcome, control)
            x, y, z = (np.array([num(r[c]) for r in sub]) for c in (scorer, outcome, control))
            groups = np.array([r["run"] for r in sub])
            keys = sorted(set(groups))
            members = [groups == k for k in keys]
            xm, ym, zm = (np.array([v[m].mean() for m in members]) for v in (x, y, z))
            first = [sub[int(np.flatnonzero(m)[0])] for m in members]
            arms = np.array([f"{r['actor']}|{r['refiner']}" for r in first])
            quality = np.array([SEED_RANK.get(r["seed_quality"], -1) for r in first])
            within = spearman(np.concatenate([x[m] - x[m].mean() for m in members]),
                              np.concatenate([y[m] - y[m].mean() for m in members]))
            per_version = partial_spearman(x, y, z)

            e = expected[(outcome, scorer)]
            key = f"{outcome} {scorer}|{control}"
            chk.same(f"{key} control", control, e["control"])
            chk.close(f"{key} n_versions", len(sub), e["n_versions"], 1e-9)
            chk.close(f"{key} n_lineages", len(keys), e["n_lineages"], 1e-9)
            chk.close(f"{key} per_version", per_version, e["per_version"], ROUNDED)
            chk.close(f"{key} published", per_version,
                      pooled[(outcome, scorer, control)]["partial_spearman"], 5e-4)
            chk.close(f"{key} lineage_mean", partial_spearman(xm, ym, zm), e["lineage_mean"], ROUNDED)
            chk.close(f"{key} within_lineage", within, e["within_lineage"], ROUNDED)
            chk.close(f"{key} between_lineage", spearman(xm, ym), e["between_lineage"], ROUNDED)
            chk.close(f"{key} between_lineage_within_arm", centre(xm, ym, arms),
                      e["between_lineage_within_arm"], ROUNDED)
            chk.close(f"{key} between_x_vs_seed_quality", spearman(xm, quality),
                      e["between_x_vs_seed_quality"], ROUNDED)
            if args.bootstrap:
                lo, hi = lineage_bootstrap(x, y, z, groups)
                chk.close(f"{key} cluster_ci_lo", lo, e["cluster_ci_lo"], ROUNDED)
                chk.close(f"{key} cluster_ci_hi", hi, e["cluster_ci_hi"], ROUNDED)
                chk.same(f"{key} cluster_excludes_zero", lo > 0 or hi < 0, e["cluster_excludes_zero"])

        # Lineage-mean performance against seed quality.
        sub = complete(versions, outcome)
        groups = np.array([r["run"] for r in sub])
        y = np.array([num(r[outcome]) for r in sub])
        keys = sorted(set(groups))
        ym = np.array([y[groups == k].mean() for k in keys])
        quality = np.array([SEED_RANK.get(sub[int(np.flatnonzero(groups == k)[0])]["seed_quality"], -1)
                            for k in keys])
        chk.close(f"{outcome} performance vs seed quality", spearman(ym, quality),
                  expected[(outcome, "__lineage_mean_performance__")]["between_lineage"], ROUNDED)

    print(f"{chk.passed} values match results/")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
