#!/usr/bin/env python3
"""Recompute the paper's statistics from data/ and check them against results/.

Covers incremental validity (out-of-sample gain in R^2 and partial Spearman with Holm correction)
for selection on both harnesses and for execution, the reverse word-count comparison, the
cross-harness transfer of the variant ordering, and the naming-pair Cochran-Mantel-Haenszel tests.
The estimators follow the paper's Appendix E:

- partial Spearman: Pearson correlation of rank residuals after regressing each rank on an
  intercept and the rank of one control; two-sided p-value from the t approximation with n - 3
  degrees of freedom; Holm-corrected within one family (one model's selection rates, or one
  execution split, with every scorer-control pair);
- incremental validity: OLS with an intercept, predictions for each held-out group (a variant for
  selection, a lineage for execution), R^2 against the overall mean of the outcome;
- naming: Mantel-Haenszel risk difference with the Sato variance, and the CMH test without
  continuity correction over strata that are neither all-zero nor all-one.

usage: python3 analysis/reproduce.py [--bootstrap]
       --bootstrap also recomputes the 10,000-draw lineage-bootstrap intervals (several minutes).
Requires numpy and scipy. Exits non-zero if any value differs from results/.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.stats import chi2, norm, rankdata, spearmanr
from scipy.stats import t as student_t

ROOT = Path(__file__).resolve().parent.parent
DATA, RESULTS = ROOT / "data", ROOT / "results"
ACTORS = ("qwen", "deepseek")
LENGTHS = ("03", "12", "25", "44")

SELECTION_SCORERS = ("sc_score", "sc_description", "mk_description_quality", "ss_total",
                     "conformance_overall")
SELECTION_BASELINES = ("description_word_count",)
EXECUTION_SCORERS = ("sc_score", "sc_body", "sv_information_density", "sv_instruction_specificity",
                     "sv_imperative_ratio", "ss_total", "ss_structure_progressive_disclosure",
                     "ss_instruction_quality", "conformance_overall")
EXECUTION_BASELINES = ("description_word_count", "body_token_count", "has_code_block",
                       "has_numbered_steps")
BOOTSTRAP_DRAWS, BOOTSTRAP_SEED = 10_000, 20260828


# ----------------------------------------------------------------------------- reading

def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def num(value) -> float | None:
    if value is None or value == "":
        return None
    if value in ("True", "False"):
        return float(value == "True")
    return float(value)


# ----------------------------------------------------------------------------- estimators

def partial_spearman(x, y, z) -> float | None:
    if len(x) < 4 or min(len(set(x)), len(set(y)), len(set(z))) < 2:
        return None
    design = np.column_stack((np.ones(len(x)), rankdata(z)))
    rx, ry = rankdata(x), rankdata(y)
    ex = rx - design @ np.linalg.lstsq(design, rx, rcond=None)[0]
    ey = ry - design @ np.linalg.lstsq(design, ry, rcond=None)[0]
    if np.allclose(ex, 0) or np.allclose(ey, 0):
        return None
    return float(np.corrcoef(ex, ey)[0, 1])


def t_pvalue(rho: float | None, n: int) -> float | None:
    if rho is None or n < 4:
        return None
    if math.isclose(abs(rho), 1.0):
        return 0.0
    df = n - 3
    return float(2 * student_t.sf(abs(rho) * math.sqrt(df / (1.0 - rho * rho)), df))


def holm(rows: list[dict]) -> None:
    ordered = sorted(((i, r["p_value"]) for i, r in enumerate(rows) if r["p_value"] is not None),
                     key=lambda item: item[1])
    running, m = 0.0, len(ordered)
    for rank, (i, p) in enumerate(ordered):
        running = max(running, min(1.0, (m - rank) * p))
        rows[i]["p_holm"] = running


def cv_r2(x: np.ndarray, y: np.ndarray, groups: np.ndarray) -> float:
    predictions = np.empty(len(y))
    for group in np.unique(groups):
        test = groups == group
        train_design = np.column_stack([np.ones((~test).sum()), x[~test]])
        beta = np.linalg.lstsq(train_design, y[~test], rcond=None)[0]
        predictions[test] = np.column_stack([np.ones(test.sum()), x[test]]) @ beta
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 1.0 - float(np.sum((y - predictions) ** 2)) / ss_tot if ss_tot > 0 else float("nan")


def lineage_bootstrap(x, y, z, groups) -> tuple[float, float] | None:
    draws = bootstrap_draws(x, y, z, groups)
    if not draws:
        return None
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return float(lo), float(hi)


def bootstrap_draws(x, y, z, groups) -> list[float]:
    """Partial Spearman over resamples of whole lineages, drawn with replacement."""
    lineages: dict[str, list[int]] = defaultdict(list)
    for i, g in enumerate(groups):
        lineages[str(g)].append(i)
    keys = sorted(lineages)
    rng = random.Random(BOOTSTRAP_SEED)
    draws = []
    for _ in range(BOOTSTRAP_DRAWS):
        idx = np.array([i for _ in keys for i in lineages[rng.choice(keys)]], dtype=int)
        estimate = partial_spearman(x[idx], y[idx], z[idx])
        if estimate is not None and not np.isnan(estimate):
            draws.append(estimate)
    return draws


def complete(rows, *cols):
    return [r for r in rows if all(num(r.get(c)) is not None for c in cols)]


def family(rows, outcome, scorers, baselines, group, bootstrap=False) -> tuple[list, list]:
    """Partial Spearman (one Holm family) and incremental validity for one scope."""
    partial, incremental = [], []
    for scorer in scorers:
        for control in baselines:
            sub = complete(rows, scorer, outcome, control)
            x = np.array([num(r[scorer]) for r in sub])
            y = np.array([num(r[outcome]) for r in sub])
            z = np.array([num(r[control]) for r in sub])
            g = np.array([str(r[group]) for r in sub])
            rho = partial_spearman(x, y, z)
            row = {"scorer": scorer, "control": control, "n": len(sub), "partial_spearman": rho,
                   "p_value": t_pvalue(rho, len(sub)), "p_holm": None, "ci": None}
            if bootstrap and rho is not None:
                row["ci"] = lineage_bootstrap(x, y, z, g)
            partial.append(row)
            r2_base, r2_scorer = cv_r2(z[:, None], y, g), cv_r2(x[:, None], y, g)
            r2_both = cv_r2(np.column_stack([z, x]), y, g)
            ok = all(math.isfinite(v) for v in (r2_base, r2_scorer, r2_both))
            incremental.append({"scorer": scorer, "baseline": control,
                                "delta_r2_adding_scorer": r2_both - r2_base if ok else None,
                                "delta_r2_adding_baseline": r2_both - r2_scorer if ok else None})
    holm(partial)
    return partial, incremental


def mh_risk_difference(strata) -> tuple[float, float, float]:
    sum_w = numerator = sum_p = sum_q = Fraction(0)
    for a, n1, c, n0 in strata:
        n = n1 + n0
        sum_w += Fraction(n1 * n0, n)
        numerator += Fraction(a * n0 - c * n1, n)
        s1, s0 = Fraction(n1, n), Fraction(n0, n)
        sum_p += c * s1 ** 2 - a * s0 ** 2 + s1 * s0 * Fraction(n0 - n1, 2)
        sum_q += Fraction(a * (n0 - c) + c * (n1 - a), n)
    rd = numerator / sum_w
    half = float(norm.ppf(0.975)) * math.sqrt(float((rd * sum_p + sum_q / 2) / sum_w ** 2))
    return float(rd), float(rd) - half, float(rd) + half


def cmh_statistic(strata) -> float:
    num_, var = 0.0, 0.0
    for a, n1, c, n0 in strata:
        n, m1 = n1 + n0, a + c
        if m1 in (0, n):  # all-zero or all-one strata carry no information
            continue
        num_ += a - n1 * m1 / n
        var += n1 * n0 * m1 * (n - m1) / (n * n * (n - 1))
    return num_ * num_ / var if var > 0 else float("nan")


def cmh_p(strata) -> float:
    return float(chi2.sf(cmh_statistic(strata), 1))


# ----------------------------------------------------------------------------- checking

class Checker:
    def __init__(self, source: str = "results/") -> None:
        self.passed, self.failed, self.source = 0, [], source

    def close(self, label: str, got, expected: str, tol: float) -> None:
        exp = num(expected)
        if got is None or exp is None:
            ok = (got is None) == (exp is None)
        else:
            ok = abs(got - exp) <= tol * max(1.0, abs(exp)) if tol < 1e-3 else abs(got - exp) <= tol
        if ok:
            self.passed += 1
        else:
            self.failed.append(f"{label}: got {got!r}, {self.source} has {expected!r}")

    def same(self, label: str, got, expected: str) -> None:
        if str(got) == expected:
            self.passed += 1
        else:
            self.failed.append(f"{label}: got {got!r}, {self.source} has {expected!r}")


def check_family(chk, label, partial, incremental, exp_partial, exp_incremental):
    ep = {(r["scorer"], r["control"]): r for r in exp_partial}
    ei = {(r["scorer"], r["baseline"]): r for r in exp_incremental}
    for row in partial:
        e = ep[(row["scorer"], row["control"])]
        key = f"{label} {row['scorer']}|{row['control']}"
        chk.close(key + " rho", row["partial_spearman"], e["partial_spearman"], 1.5e-4)
        chk.close(key + " p_holm", row["p_holm"], e["p_holm"], 1e-5)
        if row["ci"] is not None:
            chk.close(key + " ci_low", row["ci"][0], e["bootstrap_ci_low"], 1.5e-4)
            chk.close(key + " ci_high", row["ci"][1], e["bootstrap_ci_high"], 1.5e-4)
    for row in incremental:
        e = ei[(row["scorer"], row["baseline"])]
        key = f"{label} {row['scorer']}|{row['baseline']}"
        chk.close(key + " dR2", row["delta_r2_adding_scorer"], e["delta_r2_adding_scorer"], 1.5e-4)
        chk.close(key + " dR2 reverse", row["delta_r2_adding_baseline"],
                  e["delta_r2_adding_baseline"], 1.5e-4)


def selection_rows(rates: dict, actor: str) -> list[dict]:
    """The 17 variants for one model: incumbent and baselines, independent scores, a rate."""
    scores = {r["variant"]: r for r in read(DATA / "selection/independent_scores.csv")}
    rows = []
    for r in read(DATA / "selection/claude_code_variants.csv"):
        if r["actor"] == actor:
            rows.append({**scores[r["variant"]], **r,
                         "outcome_invocation_rate": rates[(actor, r["variant"])]})
    return rows


def execution_versions() -> list[dict]:
    """The 465 analysed versions, each with its incumbent, baselines and independent scores."""
    scores = {(r["run"], r["artifact"]): r for r in read(DATA / "execution/independent_scores.csv")}
    return [{**scores[(r["run"], r["artifact"])], **r} for r in read(DATA / "execution/versions.csv")
            if r["analysis_eligible"] == "True"]


def rates_from(cells, field) -> dict:
    counts = defaultdict(lambda: [0, 0])
    for c in cells:
        if c["block"] == "corpus_b":
            counts[(c["actor"], c["variant"])][0] += c[field] == "True"
            counts[(c["actor"], c["variant"])][1] += 1
    assert all(n == 24 for _, n in counts.values()), "every variant has 24 cells"
    return {k: k_n[0] / k_n[1] for k, k_n in counts.items()}


def codex_selection(chk: Checker, cx_cells: list[dict], detection: str) -> dict:
    """Incremental validity and the reverse word-count comparison on Codex CLI, for one detection
    rule (`amended` or `original`); returns the invocation rates."""
    cx_rates = rates_from(cx_cells, f"triggered_{detection}")
    exp_p = [r for r in read(RESULTS / "selection_codex/partial_spearman.csv") if r["detection"] == detection]
    exp_i = [r for r in read(RESULTS / "selection_codex/incremental_validity.csv") if r["detection"] == detection]
    exp_w = {r["actor"]: r for r in read(RESULTS / "selection_codex/word_count.csv") if r["detection"] == detection}
    word = []
    for actor in ACTORS:
        rows = selection_rows(cx_rates, actor)
        scope = f"invocation:{actor}"
        p, i = family(rows, "outcome_invocation_rate", SELECTION_SCORERS, SELECTION_BASELINES, "variant")
        check_family(chk, f"codex {detection} {actor}", p, i, [r for r in exp_p if r["scope"] == scope],
                     [r for r in exp_i if r["scope"] == scope])
        sub = complete(rows, "description_word_count", "outcome_invocation_rate", "conformance_overall")
        rho = partial_spearman(*(np.array([num(r[c]) for r in sub]) for c in
                                 ("description_word_count", "outcome_invocation_rate", "conformance_overall")))
        word.append({"actor": actor, "partial_spearman": rho, "p_value": t_pvalue(rho, len(sub)), "p_holm": None})
    holm(word)
    for row in word:
        chk.close(f"codex {detection} {row['actor']} word count | incumbent rho", row["partial_spearman"],
                  exp_w[row["actor"]]["partial_spearman"], 1.5e-4)
        chk.close(f"codex {detection} {row['actor']} word count | incumbent p_holm", row["p_holm"],
                  exp_w[row["actor"]]["p_holm"], 1e-5)
    return cx_rates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", action="store_true")
    args = parser.parse_args()
    chk = Checker()

    # Selection, Claude Code: rates rebuilt from the cells must equal the per-variant table.
    cc_cells = read(DATA / "selection/claude_code_cells.csv")
    cc_rates = rates_from(cc_cells, "triggered")
    for r in read(DATA / "selection/claude_code_variants.csv"):
        chk.close(f"claude code rate {r['actor']} {r['variant']}", cc_rates[(r["actor"], r["variant"])],
                  r["outcome_invocation_rate"], 1e-9)
    exp_p, exp_i = read(RESULTS / "scorers/partial_spearman.csv"), read(RESULTS / "scorers/incremental_validity.csv")
    assoc = read(RESULTS / "selection_claude_code/associations.csv")
    for actor in ACTORS:
        rows = selection_rows(cc_rates, actor)
        scope = f"invocation:{actor}"
        p, i = family(rows, "outcome_invocation_rate", SELECTION_SCORERS, SELECTION_BASELINES, "variant")
        check_family(chk, f"claude code {actor}", p, i, [r for r in exp_p if r["scope"] == scope],
                     [r for r in exp_i if r["scope"] == scope])
        # Reverse comparison: description word count controlling for the incumbent.
        sub = complete(rows, "description_word_count", "outcome_invocation_rate", "conformance_overall")
        rho = partial_spearman(*(np.array([num(r[c]) for r in sub]) for c in
                                 ("description_word_count", "outcome_invocation_rate", "conformance_overall")))
        e = [r for r in assoc if r["analysis_scope"] == "actor" and r["actor"] == actor
             and r["scorer"] == "description_word_count" and r["control"] == "conformance_overall"][0]
        chk.close(f"claude code {actor} word count | incumbent rho", rho, e["partial_spearman"], 1.5e-4)

    # Selection, Codex CLI (amended detection, as in the paper).
    cx_cells = read(DATA / "selection/codex_cells.csv")
    cx_rates = codex_selection(chk, cx_cells, "amended")
    exp_t = {r["actor"]: r for r in read(RESULTS / "selection_codex/transfer.csv")}
    for actor in ACTORS:
        variants = sorted(v for a, v in cx_rates if a == actor)
        transfer = spearmanr([cx_rates[(actor, v)] for v in variants], [cc_rates[(actor, v)] for v in variants])
        chk.close(f"codex {actor} transfer rho", float(transfer.statistic),
                  exp_t[actor]["spearman_codex_vs_claude_code"], 1.5e-4)

    # Execution: 465 eligible versions, lineage as the unit.
    versions = execution_versions()
    exp_p, exp_i = read(RESULTS / "scorers/partial_spearman.csv"), read(RESULTS / "scorers/incremental_validity.csv")
    for outcome, scope in (("outcome_heldout_mean", "execution:held-out"), ("outcome_train_mean", "execution:train")):
        rows = [r for r in versions if num(r[outcome]) is not None]
        p, i = family(rows, outcome, EXECUTION_SCORERS, EXECUTION_BASELINES, "run", args.bootstrap)
        check_family(chk, scope, p, i, [r for r in exp_p if r["scope"] == scope],
                     [r for r in exp_i if r["scope"] == scope])

    # Naming pairs: Claude Code (triggered) and Codex CLI (amended detection).
    for label, cells, field, expected in (
        ("claude code", read(DATA / "naming/claude_code_cells.csv"), "triggered",
         read(RESULTS / "naming/claude_code_cmh.csv")),
        ("codex", [c for c in cx_cells if c["block"] == "e1"], "triggered_amended",
         [r for r in read(RESULTS / "naming/codex_cmh.csv") if r["detection"] == "amended"]),
    ):
        for actor in ACTORS:
            strata = []
            for length in LENGTHS:
                named = [c for c in cells if c["actor"] == actor and c["variant"] == f"e1-p{length}"]
                unnamed = [c for c in cells if c["actor"] == actor and c["variant"] == f"e1-n{length}"]
                strata.append((sum(c[field] == "True" for c in named), len(named),
                               sum(c[field] == "True" for c in unnamed), len(unnamed)))
            rd, lo, hi = mh_risk_difference(strata)
            e = [r for r in expected if r["actor"] == actor and r["row"] == "pooled"][0]
            chk.close(f"{label} naming {actor} risk difference", rd, e["rd_mh"], 1.5e-4)
            chk.close(f"{label} naming {actor} ci_low", lo, e["ci_low"], 1.5e-4)
            chk.close(f"{label} naming {actor} ci_high", hi, e["ci_high"], 1.5e-4)
            chk.close(f"{label} naming {actor} CMH p", cmh_p(strata), e["cmh_p"], 1e-3)

    print(f"{chk.passed} values match results/")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
