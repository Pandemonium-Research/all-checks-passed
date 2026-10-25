#!/usr/bin/env python3
"""Recompute the incumbent's nested-model comparison (paper §4, Table F1) from data/ and check it
against results/selection_claude_code/incremental_validity_incumbent.csv.

For each pairing of the incumbent (conformance_overall) with a trivial baseline, the out-of-sample
R^2 of the baseline alone, the incumbent alone and both, and the gain from adding each to the
other. Selection uses the 17 Claude Code variants per model (one variant held out at a time), with
description word count or whether the description contains "release note(s)" as the baseline.
Execution uses the analysed versions (one lineage held out at a time), with numbered steps, body
line count or a code block as the baseline. The paper reports the word-count rows; the others are
released for completeness.

usage: python3 analysis/incumbent_validity.py
Exits non-zero if any value differs from results/.
"""

from __future__ import annotations

import sys

import numpy as np

from reproduce import ACTORS, DATA, RESULTS, Checker, cv_r2, execution_versions, num, read

SELECTION_BASELINES = ("description_word_count", "description_contains_release_note")
EXECUTION_BASELINES = ("has_numbered_steps", "body_line_count", "has_code_block")
ROUNDED = 5e-5 + 1e-9  # results/ holds four decimals


def compare(chk: Checker, expected: dict, scope: str, rows: list[dict], outcome: str,
            baseline: str, groups: np.ndarray) -> None:
    y = np.array([num(r[outcome]) for r in rows])
    conformance = np.array([num(r["conformance_overall"]) for r in rows])
    base = np.array([num(r[baseline]) for r in rows])
    r2_base, r2_conf = cv_r2(base[:, None], y, groups), cv_r2(conformance[:, None], y, groups)
    r2_both = cv_r2(np.column_stack([base, conformance]), y, groups)
    e = expected[(scope, baseline)]
    key = f"{scope} {baseline}"
    chk.close(f"{key} n", len(y), e["n"], 1e-9)
    chk.close(f"{key} n_groups", len(np.unique(groups)), e["n_groups"], 1e-9)
    for name, value in (("r2_baseline_only", r2_base), ("r2_conformance_only", r2_conf),
                        ("r2_both", r2_both), ("delta_r2_adding_conformance", r2_both - r2_base),
                        ("delta_r2_adding_baseline", r2_both - r2_conf)):
        chk.close(f"{key} {name}", value, e[name], ROUNDED)


def main() -> None:
    chk = Checker()
    expected = {(r["scope"], r["baseline"]): r
                for r in read(RESULTS / "selection_claude_code/incremental_validity_incumbent.csv")}
    variants = read(DATA / "selection/claude_code_variants.csv")
    for actor in ACTORS:
        rows = [r for r in variants if r["actor"] == actor]
        for baseline in SELECTION_BASELINES:
            compare(chk, expected, f"invocation:{actor}", rows, "outcome_invocation_rate", baseline,
                    np.arange(len(rows)))  # each variant is its own fold
    versions = execution_versions()
    for outcome, scope in (("outcome_heldout_mean", "execution:held-out"),
                           ("outcome_train_mean", "execution:train")):
        rows = [r for r in versions if num(r[outcome]) is not None]
        for baseline in EXECUTION_BASELINES:
            compare(chk, expected, scope, rows, outcome, baseline, np.array([r["run"] for r in rows]))
    assert chk.passed + len(chk.failed) == 7 * len(expected)

    print(f"{chk.passed} values match results/")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
