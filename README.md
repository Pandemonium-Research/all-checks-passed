# All Checks Passed: data and results

Data release for **"All Checks Passed: Static Scores for Agent Skills Predict Neither Selection nor
Execution"** (Sampriti Saha and Pranav Hemanth, Pandemonium Research), Agent Evaluation Science
Symposium, Fall 2026 (non-archival).

The paper asks whether published static scores for agent skills predict either step of using a
skill, selection or execution, better than trivial text baselines such as description word count.
This release holds the per-cell and per-version data behind every statistic in the paper, the
derived result tables, the stimuli and the text of every skill version scored. Column definitions
are in [DATA_DICTIONARY.md](DATA_DICTIONARY.md); each result table, and the claim it supports, is
described in [results/README.md](results/README.md).

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
| §4 Selection, Claude Code (Figure 1, left; Appendix F) | `data/selection/claude_code_*.csv`, `independent_scores.csv` | `results/selection_claude_code/`, `results/scorers/` |
| §4 Naming pairs (Appendix F) | `data/naming/`; Codex: `data/selection/codex_cells.csv` (block `e1`) | `results/naming/` |
| §4 Second harness, Codex CLI (Appendix F) | `data/selection/codex_cells.csv` | `results/selection_codex/` |
| §5 Execution (Figures 1 right and 2; Appendix G) | `data/execution/versions.csv`, `independent_scores.csv`; `stimuli/skill_versions/` | `results/execution/`, `results/scorers/` |
| §6 Cheap probe (Appendix H) | `data/probe/`, `data/execution/lineage_termination.csv` | `results/execution/corpus_composition.json` |
| §7 Power (Appendix E) | | `results/scorers/minimum_detectable_effect.csv` |
| Appendix A, validator version | | `results/scorers/validator_version_check.csv` |

## Reproducing the statistics

```
pip install -r requirements.txt
python3 analysis/reproduce.py              # about 3 seconds
python3 analysis/reproduce.py --bootstrap  # adds the 10,000-draw lineage-bootstrap intervals
```

Each script in `analysis/` uses only `data/`, recomputes one part of the paper and exits non-zero
on any difference. Run each the same way. `--bootstrap`, where a script takes it, adds the
10,000-draw bootstrap intervals, which take from under a minute to several minutes.

| Script | Recomputes | Paper |
|---|---|---|
| `reproduce.py` | Incremental validity, the reverse word-count comparison, the cross-harness transfer, the naming-pair CMH tests | §4, §5 |
| `associations.py` | Each incumbent check and text feature against selection and execution | §4, §5, Appendix F |
| `incumbent_validity.py` | The incumbent's nested-model comparison with each trivial baseline | §4, Table F1 |
| `codex.py` | Codex results under the original detection rule; block rates; malformed-name listing | §4, Appendices D and F |
| `naming.py` | Every naming-pair stratum, the gaps by directness level, the drift anchors | §4, Appendix F, Table F3 |
| `within_between.py` | Associations within lineages, between lineages, and with arms centred | §5, Figure 2, Appendix E, Table G3 |
| `clustered.py` | Execution associations with lineage-bootstrap intervals | §5, Appendix E, Table G2 |
| `newline.py` | `skill-check` with its trailing-newline rule removed | §5, Figure 1, Table G1 |
| `probe.py` | The cheap probe: Tables H1 and H2 and the cost paragraph | §6, Appendix H |
| `composition.py` | The makeup of the execution corpus and how its lineages ended | §3, §6, Appendix C |
| `detectable_effect.py` | The smallest effect each test detects | §7, Figure 1, Table E1 |
| `range_check.py` | How many distinct values each score takes | §5, Appendix F, Table G1, Figure 1 |

Each script checks its values against `results/`; [results/README.md](results/README.md) names the
script for each table. The exceptions: `probe.py` checks against the paper, since no results table
holds the probe, and `reproduce.py` checks the 34 Claude Code invocation rates against
`data/selection/claude_code_variants.csv`. Two tables record runs of the scoring tools themselves
and cannot be recomputed from `data/`: `results/scorers/determinism.csv` and
`validator_version_check.csv`.

`figures.py` draws Figures 1 and 2 from `results/` into `figures/`. It needs matplotlib, and its
output matches the paper's when the Open Sans font is installed or given with `--fonts`.

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
