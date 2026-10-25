#!/usr/bin/env python3
"""Recompute the incumbent's checks and our text features against selection and execution (paper
§4, §5, Appendix F) from data/ and check them against results/selection_claude_code/
associations.csv and results/execution/associations.csv.

Each row pairs one score with one outcome: the marginal Spearman correlation (asymptotic p-value)
and the partial Spearman correlation controlling for the incumbent, or, for the incumbent itself,
controlling for description word count (t approximation; Holm within each scope, outcome and
model or arm). The scores are the incumbent, its description subtotal and its eleven checks, and
our eight text features. §4 cites the description-length check (+0.793 on qwen, Holm p = 0.003;
+0.614 on deepseek) and the reverse comparison (+0.842 and +0.744).

- selection: the 17 Claude Code variants per model, plus whether the description contains
  "release note(s)";
- execution: the analysed versions pooled, per task family and per arm (actor x refiner).

usage: python3 analysis/associations.py
Exits non-zero if any value differs from results/.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.stats import spearmanr

from reproduce import (DATA, RESULTS, Checker, execution_versions, holm, num, partial_spearman, read,
                       t_pvalue)

CHECKS = ("yaml_frontmatter", "name_present", "name_format", "description_present",
          "description_length", "description_format", "line_count", "no_readme", "allowed_subdirs",
          "bundled_resources", "referenced_resources")
SCORES = ("description_word_count", "description_trigger_cue_count", "body_line_count",
          "body_token_count", "has_code_block", "has_numbered_steps", "has_worked_example",
          "imperative_opener_count", "conformance_overall", "conformance_description_subtotal",
          *(f"conformance_check_{c}" for c in CHECKS))
SELECTION_SCORES = (*SCORES, "description_contains_release_note")
OUTCOMES = ("outcome_train_mean", "outcome_heldout_mean")
FIELDS = ("n", "n_unique_scorer", "n_unique_outcome", "n_unique_control", "spearman_rho",
          "marginal_p_value", "partial_spearman", "p_value", "p_holm")
EXACT = 1e-9  # results/ holds full precision


def rho(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    value = float(spearmanr(xs, ys).statistic)
    return None if np.isnan(value) else value


def association(rows: list[dict], outcome: str, scorer: str) -> dict:
    control = "description_word_count" if scorer == "conformance_overall" else "conformance_overall"
    pairs = [(num(r[scorer]), num(r[outcome])) for r in rows
             if num(r[scorer]) is not None and num(r[outcome]) is not None]
    mx, my = [x for x, _ in pairs], [y for _, y in pairs]
    marginal = rho(mx, my)
    sub = [r for r in rows if all(num(r[c]) is not None for c in (scorer, outcome, control))]
    xs, ys, zs = ([num(r[c]) for r in sub] for c in (scorer, outcome, control))
    partial = partial_spearman(np.array(xs), np.array(ys), np.array(zs))
    return {"scorer": scorer, "control": control, "n": len(sub), "n_unique_scorer": len(set(xs)),
            "n_unique_outcome": len(set(ys)), "n_unique_control": len(set(zs)), "spearman_rho": marginal,
            "marginal_p_value": float(spearmanr(mx, my).pvalue) if marginal is not None else None,
            "partial_spearman": partial, "p_value": t_pvalue(partial, len(sub)), "p_holm": None,
            "status": "estimated" if partial is not None else "zero_variance_or_insufficient_data",
            "control_zero_variance": len(set(zs)) <= 1, "outcome_zero_variance": len(set(ys)) <= 1}


def check(chk: Checker, label: str, family: list[dict], expected: dict, key: tuple) -> None:
    holm(family)
    for row in family:
        e = expected[(*key, row["scorer"])]
        name = f"{label} {row['scorer']}"
        chk.same(f"{name} control", row["control"], e["control"])
        for field in FIELDS:
            chk.close(f"{name} {field}", row[field], e[field], EXACT)
        for field in ("status", "control_zero_variance", "outcome_zero_variance"):
            chk.same(f"{name} {field}", row[field], e[field])


def main() -> None:
    chk = Checker()

    expected = {(r["actor"], r["scorer"]): r for r in read(RESULTS / "selection_claude_code/associations.csv")}
    variants = [r for r in read(DATA / "selection/claude_code_variants.csv") if r["outcome_complete"] == "True"]
    for actor in sorted({r["actor"] for r in variants}):
        rows = [r for r in variants if r["actor"] == actor]
        family = [association(rows, "outcome_invocation_rate", s) for s in SELECTION_SCORES]
        check(chk, f"selection {actor}", family, expected, (actor,))
    assert len(expected) == 2 * len(SELECTION_SCORES)

    expected = {(r["analysis_scope"], r["actor"], r["refiner"], r["outcome"], r["scorer"]): r
                for r in read(RESULTS / "execution/associations.csv")}
    versions = execution_versions()
    groups = [("pooled", "", "", versions)]
    groups += [(f"family:{task}", "", "", [r for r in versions if r["task"] == task])
               for task in sorted({r["task"] for r in versions})]
    groups += [("arm", actor, refiner, [r for r in versions if (r["actor"], r["refiner"]) == (actor, refiner)])
               for actor, refiner in sorted({(r["actor"], r["refiner"]) for r in versions})]
    n_rows = 0
    for scope, actor, refiner, rows in groups:
        for outcome in OUTCOMES:
            family = [association(rows, outcome, s) for s in SCORES]
            check(chk, f"execution {scope} {actor} {refiner} {outcome}", family, expected,
                  (scope, actor, refiner, outcome))
            n_rows += len(family)
    assert n_rows == len(expected), (n_rows, len(expected))

    print(f"{chk.passed} values match results/")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed[:40]))
        sys.exit(1)


if __name__ == "__main__":
    main()
