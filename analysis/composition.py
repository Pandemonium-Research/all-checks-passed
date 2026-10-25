#!/usr/bin/env python3
"""Recompute what the execution corpus is made of and how its lineages ended (paper §3, §6,
Appendix C) from data/ and check it against results/execution/corpus_composition.json and
data/execution/lineage_termination.csv.

- composition: the 517 versions by role, the 465 analysed on training instances (seeds, accepted
  versions and rejected candidates; second copies of accepted versions are excluded) and the 120
  with held-out scores (seeds and accepted versions);
- termination, per lineage: the last round reached, the number of accepted rewrites, the round of
  the last one, and the quiet tail (rounds since it). §6 reports that 64 of 68 lineages reached the
  six-round cap and 67 of 68 had gone two or more rounds without an accepted rewrite.

usage: python3 analysis/composition.py
Exits non-zero if any value differs.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict

from reproduce import DATA, RESULTS, Checker, read

ROUND_CAP = 6


def flatten(prefix: str, value) -> dict:
    if isinstance(value, dict):
        return {k: v for key, sub in value.items() for k, v in flatten(f"{prefix}.{key}", sub).items()}
    return {prefix: value}


def main() -> None:
    chk = Checker()
    rows = read(DATA / "execution/versions.csv")
    eligible = [r for r in rows if r["analysis_eligible"] == "True"]
    heldout = [r for r in eligible if r["outcome_heldout_mean"] != ""]
    composition = {
        "all_versions": dict(Counter(r["artifact_role"] for r in rows)),
        "train_eligible": dict(Counter(r["artifact_role"] for r in eligible)),
        "heldout": dict(Counter(r["artifact_role"] for r in heldout)),
        "n_all": len(rows), "n_train": len(eligible), "n_heldout": len(heldout),
    }

    lineages: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        lineages[r["run"]].append(r)
    per_lineage = {}
    for run, versions in sorted(lineages.items()):
        last = max(int(v["iteration"]) for v in versions)
        accepted = sorted({int(v["iteration"]) for v in versions
                           if v["accepted"] == "True" and int(v["iteration"]) > 0})
        last_accepted = max(accepted) if accepted else 0
        head = versions[0]
        per_lineage[run] = {"actor": head["actor"], "refiner": head["refiner"],
                            "seed_quality": head["seed_quality"], "task": head["task"],
                            "last_iteration": last, "n_accepted_improvements": len(accepted),
                            "last_accepted_iteration": last_accepted, "quiet_tail": last - last_accepted}
    quiet = Counter(r["quiet_tail"] for r in per_lineage.values())
    termination = {
        "n_lineages": len(per_lineage),
        "quiet_tail_distribution": dict(sorted(quiet.items())),
        "accepted_improvements_distribution":
            dict(sorted(Counter(r["n_accepted_improvements"] for r in per_lineage.values()).items())),
        "at_least_1_quiet": sum(c for k, c in quiet.items() if k >= 1),
        "at_least_2_quiet": sum(c for k, c in quiet.items() if k >= 2),
        "at_least_4_quiet": sum(c for k, c in quiet.items() if k >= 4),
        "hit_iteration_cap": sum(r["last_iteration"] == ROUND_CAP for r in per_lineage.values()),
    }

    expected = json.loads((RESULTS / "execution/corpus_composition.json").read_text(encoding="utf-8"))
    got = flatten("", {"composition": composition, "termination": termination})
    want = flatten("", expected)
    assert set(got) == set(want), sorted(set(got) ^ set(want))
    for key, value in want.items():
        chk.close(f"composition{key}", got[key], str(value), 1e-9)

    released = {r["run"]: r for r in read(DATA / "execution/lineage_termination.csv")}
    assert set(released) == set(per_lineage)
    for run, row in per_lineage.items():
        for field, value in row.items():
            chk.same(f"termination {run} {field}", value, released[run][field])

    print(f"{chk.passed} values match results/ and data/execution/lineage_termination.csv")
    if chk.failed:
        print(f"{len(chk.failed)} differ:")
        print("\n".join("  " + f for f in chk.failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
