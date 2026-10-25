#!/usr/bin/env python3
"""Recompute the naming pairs in full (paper §4, Appendix F, Table F3) from data/ and check them
against results/naming/, data/naming/claude_code_counts.csv and the paper.

In each pair, one description names "release notes" and the other uses the skill's own term at the
same length (3, 12, 25 or 44 words), body and conformance. reproduce.py checks each model's pooled
risk difference, interval and CMH p-value. This adds:

- every stratum (one per length): invocations with and without the name, the difference, and
  whether the stratum is informative (strata in which all cells, or none, invoke are dropped);
- the pooled Sato standard error, the CMH statistic and the dropped strata, for Claude Code and for
  Codex CLI under both detection rules;
- the gap at each directness level (Table F3's L2 to L4 columns; §4 cites the L4 gaps);
- the anchors: the two weakest descriptions, re-run beside the pairs, against their counts in the
  selection grid (two-sided Fisher exact test), to check that invocation did not drift;
- the per-variant counts released in data/naming/claude_code_counts.csv;
- the decision rule registered before the run, which the paper reports as passed: qwen's pooled
  difference is positive with CMH p < 0.05, and deepseek's is not negative.

usage: python3 analysis/naming.py
Exits non-zero if any value differs.
"""

from __future__ import annotations

import math
import sys

from scipy.stats import chi2, fisher_exact, norm

from reproduce import ACTORS, DATA, LENGTHS, RESULTS, Checker, cmh_statistic, mh_risk_difference, read

LEVELS = ("L2", "L3", "L4")
ANCHORS = ("q-weak", "q-nearempty")
VARIANTS = tuple(v for length in LENGTHS for v in (f"e1-p{length}", f"e1-n{length}")) + ANCHORS
ROUNDED = 5e-5 + 1e-9  # results/ holds four decimals


def invoked(cells: list[dict], field: str) -> int:
    return sum(c[field] == "True" for c in cells)


def close_g(chk: Checker, label: str, got: float, expected: str) -> None:
    """Compare with a value printed to four significant figures."""
    exp = float(expected)
    ok = got < 1e-12 if exp == 0 else abs(got / exp - 1) <= 5e-4
    chk.close(label, exp if ok else got, expected, 1e-12)


def strata(cells: list[dict], field: str, actor: str) -> list[tuple[int, int, int, int]]:
    out = []
    for length in LENGTHS:
        named = [c for c in cells if c["actor"] == actor and c["variant"] == f"e1-p{length}"]
        unnamed = [c for c in cells if c["actor"] == actor and c["variant"] == f"e1-n{length}"]
        out.append((invoked(named, field), len(named), invoked(unnamed, field), len(unnamed)))
    return out


def check_cmh(chk: Checker, label: str, cells: list[dict], field: str, expected: list[dict]) -> dict:
    pooled_rd = {}
    for actor in ACTORS:
        table = strata(cells, field, actor)
        dropped = []
        for length, (a, n1, c, n0) in zip(LENGTHS, table):
            e = [r for r in expected if r["actor"] == actor and r["row"] == "stratum" and r["length"] == length][0]
            reason = "all_zero" if a + c == 0 else "all_one" if a + c == n1 + n0 else ""
            if reason:
                dropped.append(f"{length}:{reason}")
            key = f"{label} {actor} {length}"
            for name, value in (("with_invoked", a), ("with_total", n1), ("without_invoked", c),
                                ("without_total", n0)):
                chk.close(f"{key} {name}", value, e[name], 1e-9)
            chk.close(f"{key} with_rate", a / n1, e["with_rate"], ROUNDED)
            chk.close(f"{key} without_rate", c / n0, e["without_rate"], ROUNDED)
            chk.close(f"{key} rd", a / n1 - c / n0, e["rd"], ROUNDED)
            chk.same(f"{key} informative", "no" if reason else "yes", e["informative"])
            chk.same(f"{key} dropped_reason", reason, e["dropped_reason"])
        e = [r for r in expected if r["actor"] == actor and r["row"] == "pooled"][0]
        rd, lo, hi = mh_risk_difference(table)
        statistic = cmh_statistic(table)
        key = f"{label} {actor} pooled"
        chk.close(f"{key} rd_mh", rd, e["rd_mh"], ROUNDED)
        chk.close(f"{key} se_sato", (hi - rd) / float(norm.ppf(0.975)), e["se_sato"], ROUNDED)
        chk.close(f"{key} ci_low", lo, e["ci_low"], ROUNDED)
        chk.close(f"{key} ci_high", hi, e["ci_high"], ROUNDED)
        close_g(chk, f"{key} cmh_statistic", statistic, e["cmh_statistic"])
        close_g(chk, f"{key} cmh_p", float(chi2.sf(statistic, 1)), e["cmh_p"])
        chk.close(f"{key} n_informative_strata", len(LENGTHS) - len(dropped), e["n_informative_strata"], 1e-9)
        chk.same(f"{key} dropped_strata", ";".join(dropped) or "none", e["dropped_strata"])
        pooled_rd[actor] = (rd, float(chi2.sf(statistic, 1)))
    return pooled_rd


def check_by_level(chk: Checker, label: str, cells: list[dict], field: str, expected: list[dict]) -> None:
    for actor in ACTORS:
        for level in LEVELS:
            at = [c for c in cells if c["actor"] == actor and c["directness"] == level]
            named = [c for c in at if c["variant"] in {f"e1-p{n}" for n in LENGTHS}]
            unnamed = [c for c in at if c["variant"] in {f"e1-n{n}" for n in LENGTHS}]
            e = [r for r in expected if r["actor"] == actor and r["level"] == level][0]
            key = f"{label} {actor} {level}"
            with_rate, without_rate = invoked(named, field) / len(named), invoked(unnamed, field) / len(unnamed)
            chk.close(f"{key} with_invoked", invoked(named, field), e["with_invoked"], 1e-9)
            chk.close(f"{key} with_total", len(named), e["with_total"], 1e-9)
            chk.close(f"{key} without_invoked", invoked(unnamed, field), e["without_invoked"], 1e-9)
            chk.close(f"{key} without_total", len(unnamed), e["without_total"], 1e-9)
            chk.close(f"{key} with_rate", with_rate, e["with_rate"], ROUNDED)
            chk.close(f"{key} without_rate", without_rate, e["without_rate"], ROUNDED)
            chk.close(f"{key} gap", with_rate - without_rate, e["gap"], ROUNDED)


def main() -> None:
    chk, paper = Checker(), Checker(source="the paper")
    cc = read(DATA / "naming/claude_code_cells.csv")
    cx = [c for c in read(DATA / "selection/codex_cells.csv") if c["block"] == "e1"]

    cc_pooled = check_cmh(chk, "claude code", cc, "triggered", read(RESULTS / "naming/claude_code_cmh.csv"))
    codex_cmh = read(RESULTS / "naming/codex_cmh.csv")
    for detection in ("amended", "original"):
        check_cmh(chk, f"codex {detection}", cx, f"triggered_{detection}",
                  [r for r in codex_cmh if r["detection"] == detection])

    check_by_level(chk, "claude code by level", cc, "triggered", read(RESULTS / "naming/claude_code_by_level.csv"))
    check_by_level(chk, "codex by level", cx, "triggered_amended", read(RESULTS / "naming/codex_by_level.csv"))

    # Anchors: re-run beside the pairs against the same descriptions in the selection grid.
    grid = [c for c in read(DATA / "selection/claude_code_cells.csv") if c["block"] == "corpus_b"]
    for e in read(RESULTS / "naming/claude_code_anchors.csv"):
        rerun = [c for c in cc if c["actor"] == e["actor"] and c["variant"] == e["anchor"]]
        first = [c for c in grid if c["actor"] == e["actor"] and c["variant"] == e["anchor"]]
        a, n, b, m = invoked(rerun, "triggered"), len(rerun), invoked(first, "triggered"), len(first)
        key = f"anchor {e['actor']} {e['anchor']}"
        for name, value in (("e1_invoked", a), ("e1_total", n), ("a1_invoked", b), ("a1_total", m)):
            chk.close(f"{key} {name}", value, e[name], 1e-9)
        chk.close(f"{key} e1_rate", a / n, e["e1_rate"], ROUNDED)
        chk.close(f"{key} a1_rate", b / m, e["a1_rate"], ROUNDED)
        close_g(chk, f"{key} fisher_p", float(fisher_exact([[a, n - a], [b, m - b]]).pvalue), e["fisher_p"])

    # The released per-variant counts.
    for e in read(DATA / "naming/claude_code_counts.csv"):
        group = [c for c in cc if c["actor"] == e["actor"] and c["variant"] == e["variant"]
                 and e["level"] in ("all", c["directness"])]
        key = f"counts {e['actor']} {e['variant']} {e['level']}"
        chk.close(f"{key} invoked", invoked(group, "triggered"), e["invoked"], 1e-9)
        chk.close(f"{key} total", len(group), e["total"], 1e-9)
        chk.close(f"{key} rate", invoked(group, "triggered") / len(group), e["rate"], ROUNDED)
    assert {e["variant"] for e in read(DATA / "naming/claude_code_counts.csv")} == set(VARIANTS)

    qwen_rd, qwen_p = cc_pooled["qwen"]
    passes = qwen_rd > 0 and math.isfinite(qwen_p) and qwen_p < 0.05 and cc_pooled["deepseek"][0] >= 0
    paper.close("Claude Code naming passes the registered decision rule", float(passes), "1", 1e-9)

    for c in (chk, paper):
        print(f"{c.passed} values match {c.source}")
        if c.failed:
            print(f"{len(c.failed)} differ:")
            print("\n".join("  " + f for f in c.failed))
    if chk.failed or paper.failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
