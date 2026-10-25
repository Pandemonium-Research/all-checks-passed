#!/usr/bin/env python3
"""Recompute the rest of the Codex CLI replication (paper §4, Appendices D and F) from data/ and
check it against results/selection_codex/.

reproduce.py covers the amended detection rule, which the paper uses. This adds:

- the original, pre-registered rule (Appendix F, "Two changes to the Codex replication"): the
  incremental-validity tests and the reverse word-count comparison under triggered_original;
- the rest of transfer.csv: the p-value and each harness's mean invocation rate;
- block_rates.csv: invocation per model, block and directness level, including the no-skill
  baseline and the positive control (Appendix D: 0 of 48 cells, and 16 of 16);
- listing.csv: whether Codex listed each malformed-name variant, and how often it invoked it.

usage: python3 analysis/codex.py
Exits non-zero if any value differs from results/.
"""

from __future__ import annotations

import sys
from collections import defaultdict

from scipy.stats import spearmanr

from reproduce import ACTORS, DATA, RESULTS, Checker, codex_selection, rates_from, read

ROUNDED = 5e-5 + 1e-9  # results/ holds four decimals


def main() -> None:
    chk = Checker()
    cells = read(DATA / "selection/codex_cells.csv")
    codex_selection(chk, cells, "original")

    # Transfer of the variant ordering between harnesses (amended detection).
    cx_rates = rates_from(cells, "triggered_amended")
    cc_rates = rates_from(read(DATA / "selection/claude_code_cells.csv"), "triggered")
    expected = {r["actor"]: r for r in read(RESULTS / "selection_codex/transfer.csv")}
    for actor in ACTORS:
        variants = sorted(v for a, v in cx_rates if a == actor)
        codex, claude = [cx_rates[(actor, v)] for v in variants], [cc_rates[(actor, v)] for v in variants]
        e = expected[actor]
        chk.close(f"transfer {actor} n_variants", len(variants), e["n_variants"], 1e-9)
        chk.close(f"transfer {actor} p", float(spearmanr(codex, claude).pvalue), e["p_value"], 5e-7 + 1e-12)
        chk.close(f"transfer {actor} mean codex", sum(codex) / len(codex), e["mean_rate_codex"], ROUNDED)
        chk.close(f"transfer {actor} mean claude code", sum(claude) / len(claude),
                  e["mean_rate_claude_code"], ROUNDED)

    # Invocation per model, block and directness level.
    counts: dict[tuple[str, str, str], list[int]] = defaultdict(lambda: [0, 0])
    for c in cells:
        key = (c["actor"], c["block"], c["directness"])
        counts[key][0] += c["triggered_amended"] == "True"
        counts[key][1] += 1
    expected_blocks = {(r["actor"], r["block"], r["directness"]): r
                       for r in read(RESULTS / "selection_codex/block_rates.csv")}
    assert set(counts) == set(expected_blocks), sorted(set(counts) ^ set(expected_blocks))
    for key, (invoked, total) in counts.items():
        e = expected_blocks[key]
        label = "block " + " ".join(key)
        chk.close(f"{label} invoked", invoked, e["invoked"], 1e-9)
        chk.close(f"{label} total", total, e["total"], 1e-9)
        chk.close(f"{label} rate", invoked / total, e["rate"], ROUNDED)

    # The malformed-name variants: listed in Codex's skill listing, and invoked.
    expected_listing = {(r["actor"], r["variant"]): r for r in read(RESULTS / "selection_codex/listing.csv")}
    nameformat = sorted({c["variant"] for c in cells
                         if c["variant"] and c["variant"].replace("-", "").endswith("nameformat")})
    assert len(nameformat) * len(ACTORS) == len(expected_listing), nameformat
    for actor in ACTORS:
        for variant in nameformat:
            group = [c for c in cells if c["actor"] == actor and c["variant"] == variant
                     and c["block"] == "corpus_b"]
            e = expected_listing[(actor, variant)]
            label = f"listing {actor} {variant}"
            chk.close(f"{label} cells", len(group), e["cells"], 1e-9)
            chk.close(f"{label} listed", sum(c["skill_listed"] == "True" for c in group), e["listed"], 1e-9)
            chk.close(f"{label} invoked", sum(c["triggered_amended"] == "True" for c in group),
                      e["invoked"], 1e-9)

    print(f"{chk.passed} values match results/")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
