# All Checks Passed: data and results

Data release for **"All Checks Passed: Static Scores for Agent Skills Predict Neither Selection nor
Execution"** (Sampriti Saha and Pranav Hemanth, Pandemonium Research), Agent Evaluation Science
Symposium, Fall 2026 (non-archival).

The paper asks whether published static scores for agent skills predict either step of using a
skill, selection or execution, better than trivial text baselines such as description word count.
This release holds the per-cell and per-version data behind every statistic in the paper, the
derived result tables, the stimuli and the text of every skill version scored. Column definitions are in
[DATA_DICTIONARY.md](DATA_DICTIONARY.md).
Each result table, and the claim it supports, is described in [results/README.md](results/README.md).

## Contents

```
data/
  selection/   Claude Code cells and per-variant table; Codex CLI cells; independent tools' scores
  naming/      Claude Code naming-pair cells and counts (Codex naming cells are in selection/)
  execution/   517 skill versions in 68 lineages; independent tools' scores; lineage termination
  probe/       per-lineage starting score, plateau and refinement distance
results/       derived tables: associations, incremental validity, CMH tests, MDE, decompositions
stimuli/       the 25 description variants, the four selection prompts and the 517 skill versions
analysis/      scripts that recompute the paper's statistics from data/ and check them; figures.py
```

| Paper | Data | Results |
|---|---|---|
| §4 Selection, Claude Code (Figure 1, left; Appendix F) | `data/selection/claude_code_cells.csv`, `claude_code_variants.csv`, `independent_scores.csv` | `results/selection_claude_code/`, `results/scorers/` |
| §4 Naming pairs (Appendix F) | `data/naming/claude_code_cells.csv`, `claude_code_counts.csv`; Codex rows in `data/selection/codex_cells.csv` (block `e1`) | `results/naming/` |
| §4 Second harness, Codex CLI (Appendix F) | `data/selection/codex_cells.csv` | `results/selection_codex/` |
| §5 Execution (Figures 1 right and 2; Appendix G) | `data/execution/versions.csv`, `independent_scores.csv`; texts in `stimuli/skill_versions/` | `results/execution/`, `results/scorers/` |
| §6 Cheap probe (Appendix H) | `data/probe/`, `data/execution/lineage_termination.csv` | `results/execution/corpus_composition.json` |
| §7 Power (Appendix E) | | `results/scorers/minimum_detectable_effect.csv` |
| Appendix A, validator version | | `results/scorers/validator_version_check.csv` |

## Reproducing the statistics

```
pip install -r requirements.txt
python3 analysis/reproduce.py              # about 3 seconds
python3 analysis/reproduce.py --bootstrap  # adds the 10,000-draw lineage-bootstrap intervals
```

Each script in `analysis/` uses only `data/`, recomputes one part of the paper, compares every
value with the source named below, and exits non-zero on any difference. Run each the same way.
`--bootstrap`, where a script takes it, adds the 10,000-draw bootstrap intervals, which take from
under a minute to several minutes.

| Script | Paper | Checked against |
|---|---|---|
| `reproduce.py` | §4 and §5: incremental validity (out-of-sample gain in R², and partial Spearman with Holm correction) for selection on both harnesses and for execution; the reverse word-count comparison; the transfer of the variant ordering between harnesses; the naming-pair Mantel–Haenszel risk differences and CMH tests | `results/scorers/`, `results/selection_*/` and `results/naming/`; the 34 Claude Code invocation rates against `data/selection/claude_code_variants.csv` |
| `associations.py` | §4, §5 and Appendix F: each of the incumbent's checks and our text features against selection and execution, including the description-length check and the reverse comparison | `results/selection_claude_code/associations.csv`, `results/execution/associations.csv` |
| `incumbent_validity.py` | §4 and Table F1: the incumbent's nested-model comparison with each trivial baseline | `results/selection_claude_code/incremental_validity_incumbent.csv` |
| `codex.py` | §4, Appendices D and F: the Codex CLI results under the original detection rule, block rates (no-skill baseline and positive control) and the listing of malformed names | `results/selection_codex/` |
| `naming.py` | §4, Appendix F and Table F3: every naming-pair stratum on both harnesses, the gaps by directness level, the drift anchors and the registered decision rule | `results/naming/`, `data/naming/claude_code_counts.csv`, and the paper |
| `within_between.py` | §5, Figure 2, Appendix E and Table G3: each score's association with performance within lineages, between lineages, and between lineages with arms centred | `results/execution/within_between.csv`, `within_between_arm.csv` |
| `clustered.py` | §5, Appendix E and Table G2: the execution associations with lineage-bootstrap intervals | `results/execution/clustered_associations.csv`, and the pooled rows of `associations.csv` |
| `newline.py` | §5, Figure 1 (the † row) and Table G1: `skill-check` with its trailing-newline rule removed | `results/execution/sensitivity_newline.csv`, and the paper's counts (449 refined versions, 68 seeds) |
| `probe.py` | §6 and Appendix H: the cheap probe (Tables H1 and H2, and the cost paragraph) | the paper, since no results table holds the probe |
| `composition.py` | §3, §6 and Appendix C: the makeup of the execution corpus and how its lineages ended | `results/execution/corpus_composition.json`, `data/execution/lineage_termination.csv` |
| `detectable_effect.py` | §7, Figure 1 (the grey bars) and Table E1: the smallest effect each test detects | `results/scorers/minimum_detectable_effect.csv` |
| `range_check.py` | §5, Appendix F, Table G1 and Figure 1: how many distinct values each score takes | `results/scorers/range_check.csv` |

`figures.py` draws Figures 1 and 2 from `results/` into `figures/`. It needs matplotlib, and its
output matches the paper's when the Open Sans font is installed or given with `--fonts`.
[results/README.md](results/README.md) says, for each result table, which script recomputes it.
Two tables record runs of the scoring tools themselves and cannot be recomputed from `data/`:
`results/scorers/determinism.csv` and `validator_version_check.csv`.

To test another scorer, score the skills in `stimuli/skill_versions/<run>/<artifact>/SKILL.md` (or
`stimuli/descriptions/` for selection) and join on `run` and `artifact` (or `variant`).

## Units of analysis

Selection is analysed per **variant** (17 per model), not per cell: each variant's invocation rate
is the share of its 24 cells (8 task instances x 3 prompt-directness levels) in which the agent
invoked the skill. Execution is analysed per **lineage** (68): a seed skill and its successive
rewrites. The cell tables are released so that every rate can be recomputed.

## How the data were measured

A cell counts as selected only when the harness records the agent invoking the skill or reading its
file; a fingerprint string defined only in the skill cross-checks that record, and the agent's own
report never decides. With no skill installed, invocation is 0 of 24 cells per model in both
harnesses (the `baseline` rows). Execution outcomes are mean scores from a deterministic rubric,
never an LLM judge, on 8 training instances and, for seeds and accepted versions, 8 held-out
instances. Details are in the paper's §3 and Appendices C to E.

## What is not released

- Raw agent transcripts and harness logs, because they contain local paths and session metadata.
  The cell tables keep each cell's outcome fields.
- The task fixtures and the grading rubrics.

## Citation

```bibtex
@inproceedings{saha2026allcheckspassed,
  title     = {All Checks Passed: Static Scores for Agent Skills Predict Neither Selection nor Execution},
  author    = {Saha, Sampriti and Hemanth, Pranav},
  booktitle = {Agent Evaluation Science Symposium (non-archival)},
  year      = {2026}
}
```

## License

Code (`analysis/`): MIT, see [LICENSE](LICENSE). Data, results, stimuli and
documentation: CC BY 4.0, see [LICENSE-DATA](LICENSE-DATA).
