# Result tables

The tables behind the paper's statistics, derived from `data/`. Each entry gives what one row is,
the row count, the part of the paper the table supports, the columns that need explaining, and
whether `analysis/reproduce.py` recomputes it. Scorer prefixes, trivial baselines, body features,
model short names and `directness` are defined in [DATA_DICTIONARY.md](../DATA_DICTIONARY.md).

## Conventions

- `scope`: `invocation:<actor>` is selection on one model, with the variant as the unit (17).
  `execution:train` (465 versions) and `execution:held-out` (120 versions) are the two execution
  outcomes, with the lineage as the unit (68).
- `partial_spearman`: the Spearman correlation of a scorer with the outcome after one control
  (`control` or `baseline`) is regressed out of both ranks. `p_value` is two-sided, from the t
  approximation with n - 3 degrees of freedom. `p_holm` is Holm-corrected within the family each
  entry names.
- Out-of-sample R² (`r2_*`): least squares with an intercept, fitted with one variant or one lineage
  left out at a time and scored against the overall mean, so it can be negative.
  `delta_r2_adding_scorer` is `r2_both` minus `r2_baseline_only`; `delta_r2_adding_baseline` is
  `r2_both` minus `r2_scorer_only`.
- Lineage bootstrap: 10,000 draws, each resampling whole lineages with replacement; the 95% interval
  runs from the 2.5th to the 97.5th percentile.
- `n_groups`: the number of variants (selection) or lineages (execution) among the `n` rows.
- `detection` (Codex tables): `amended`, the rule the paper uses, or `original`, the pre-registered
  rule alone (see `triggered_amended` in the data dictionary).
- An empty statistic was not estimated, because a variable takes too few values.

## selection_claude_code/

### `associations.csv`: one row per model and scorer (44)

Supports §4 (the incumbent's partial ρ of +0.20 and +0.12; controlling for the incumbent,
`conformance_check_description_length` reaches +0.793 on `qwen` and +0.614 on `deepseek`), Table F1
(last row: word count given the incumbent, +0.84 and +0.74) and the text beside Table E1. The 22
scorers are the incumbent's overall score, description subtotal and eleven checks, and nine text
features: the four trivial baselines, `body_line_count`, `imperative_opener_count`,
`has_worked_example`, `description_trigger_cue_count` and `description_contains_release_note`.

| Column | Meaning |
|---|---|
| `association_direction` | `scorer_over_conformance`: the scorer's partial Spearman with the outcome, controlling for `conformance_overall`. `conformance_over_word_count`: the incumbent's, controlling for `description_word_count` (one row per model) |
| `spearman_rho`, `marginal_p_value` | Spearman correlation without a control, and its two-sided p-value |
| `partial_spearman_over_conformance` | Equals `partial_spearman` in `scorer_over_conformance` rows; empty otherwise |
| `n_unique_scorer`, `n_unique_outcome`, `n_unique_control` | Distinct values among the `n` variants |
| `p_holm` | Holm within one model |
| `control_zero_variance`, `outcome_zero_variance` | The control, or the outcome, takes one value |
| `status` | `estimated`, or `zero_variance_or_insufficient_data`: no estimate, because the scorer, outcome or control takes one value (for example a check every variant passes), or the control fully explains the scorer |
| `marginal_p_permutations`, `p_permutations` | Always empty: permutation tests apply only at n ≤ 9 |

Recomputed by `reproduce.py`: partly, `partial_spearman` in the two rows where `scorer` is
`description_word_count`.

### `incremental_validity_incumbent.csv`: one row per scope and baseline (10)

The incumbent alone against single baselines, in both directions. The selection baselines are
`description_word_count` and `description_contains_release_note`; the table also holds execution
rows, with baselines `has_numbered_steps`, `body_line_count` and `has_code_block`. Only the two
`description_word_count` rows are reported, in §4 and Table F1 (adding the incumbent to word count
changes out-of-sample R² by -0.02 and -0.08). The other eight rows are not reported.

| Column | Meaning |
|---|---|
| `r2_conformance_only`, `delta_r2_adding_conformance` | `r2_scorer_only` and `delta_r2_adding_scorer` with `conformance_overall` as the scorer |

Recomputed by `reproduce.py`: no. Its six rows with baseline `description_word_count`,
`has_numbered_steps` or `has_code_block` equal `conformance_overall` rows of
`scorers/incremental_validity.csv`, which it checks.

## selection_codex/

Selection on Codex CLI. Tables without a `detection` column use amended detection.

### `partial_spearman.csv`: one row per detection rule, model and scorer (20)

Supports §4 (the Codex paragraph) and Table F1 (Codex columns); the `original` rows support
Appendix F, "Two changes to the Codex replication" (the incumbent at -0.01 and +0.27). Columns as in
`scorers/partial_spearman.csv`, for the Codex invocation rate. The scorers are `sc_score`,
`sc_description`, `mk_description_quality`, `ss_total` and `conformance_overall`, each controlling
for `description_word_count`. `p_holm` is Holm within one detection rule and model. The bootstrap
columns are empty.

Recomputed by `reproduce.py`: partly, `partial_spearman` and `p_holm` in the 10 `amended` rows; not
the `original` rows.

### `incremental_validity.csv`: one row per detection rule, model and scorer (20)

Supports §4 (the Codex paragraph) and Table F1 (Codex columns). Columns as in
`scorers/incremental_validity.csv`, with the same scorers and `description_word_count` as the
baseline. The `original` rows are not reported.

Recomputed by `reproduce.py`: partly, `delta_r2_adding_scorer` and `delta_r2_adding_baseline` in the
10 `amended` rows; not the `original` rows.

### `word_count.csv`: one row per detection rule and model (4)

Supports §4 (word count predicts the Codex rate beyond the incumbent, +0.71 and +0.78) and Table F1
(last row, Codex columns); the `original` rows support Appendix F, "Two changes to the Codex
replication" (+0.73 and +0.63). Description word count controlling for `conformance_overall`.
`p_holm` is Holm across the two models within one detection rule.

Recomputed by `reproduce.py`: partly, `partial_spearman` and `p_holm` in the two `amended` rows; not
the `original` rows.

### `transfer.csv`: one row per model (2)

Supports §4 (the variant ordering carries over, Spearman 0.72 and 0.97) and Appendix F. The
Spearman correlation between the 17 variants' Codex rates and their Claude Code rates, its p-value
(rounded to six decimals), and each harness's mean rate.

Recomputed by `reproduce.py`: partly, `spearman_codex_vs_claude_code` in both rows.

### `block_rates.csv`: one row per model, block and directness level (20)

Supports Appendix D, measurement integrity (with no skill installed, 0 of 48 Codex cells invoke
one; the L1 positive control invokes it in 16 of 16). `invoked` / `total` = `rate` for each `block`
of `data/selection/codex_cells.csv`: `corpus_b` (136 cells per level), `e1` (64), `baseline` (8)
and `positive_control` (8, L1 only).

Recomputed by `reproduce.py`: no.

### `listing.csv`: one row per model and malformed-name variant (8)

Supports Appendix F, other notes (Codex listed the skill in all 192 cells). The four variants with
a malformed `name` (`*-nameformat` and `p-name-format`): `cells`, `listed` (cells in which the skill
appeared in Codex's skill listing) and `invoked`.

Recomputed by `reproduce.py`: no.

## naming/

The minimal pairs. `with_*` columns count the variants whose description says "release notes"
(`e1-pNN`), and `without_*` those that say "impact log" (`e1-nNN`). `invoked` / `total` = `rate`.

### `claude_code_cmh.csv`: one row per model and length, plus one pooled row per model (10)

Supports §4 (naming raises invocation by 0.56 and 0.78, CMH p < 10^-18) and Table F3.

| Column | Meaning |
|---|---|
| `row` | `stratum` (one description length: `length` is 03, 12, 25 or 44 words) or `pooled` |
| `rd` | `with_rate` minus `without_rate` |
| `informative`, `dropped_reason` | Whether the stratum enters the CMH test. A stratum in which no cell invoked the skill (`all_zero`) carries no information and is dropped from the test; the risk difference still uses all four strata |
| `rd_mh`, `se_sato`, `ci_low`, `ci_high` | Pooled rows: the Mantel–Haenszel risk difference, its standard error (Sato variance) and its 95% interval, `rd_mh` ± 1.96 `se_sato` |
| `cmh_statistic`, `cmh_p` | Pooled rows: the CMH chi-square (1 degree of freedom, no continuity correction) and its p-value. Both `cmh_p` values here are below 10^-18 and stored rounded to 0 |
| `n_informative_strata`, `dropped_strata` | Pooled rows: strata in the test, and those dropped (`none`, or `<length>:<reason>`) |

Recomputed by `reproduce.py`: partly, `rd_mh`, `ci_low`, `ci_high` and `cmh_p` in the two pooled
rows.

### `codex_cmh.csv`: one row per detection rule, model and length, plus pooled rows (20)

Supports §4 (on Codex, naming raises invocation by 0.34 and 0.16) and Table F3; the `original`
pooled rows support Appendix F, "Two changes to the Codex replication" (+0.33 and +0.24). Columns
as in `claude_code_cmh.csv`, plus `detection`.

Recomputed by `reproduce.py`: partly, `rd_mh`, `ci_low`, `ci_high` and `cmh_p` in the two pooled
`amended` rows; not the `original` rows.

### `claude_code_by_level.csv`: one row per model and directness level (6)

Supports §4 (the gap persists at L4, 0.44 and 0.59) and Table F3 (L2 to L4 columns). Counts pooled
over the four lengths (32 cells each side), and `gap`, `with_rate` minus `without_rate`. The L4
prompt never says "release notes".

Recomputed by `reproduce.py`: no.

### `codex_by_level.csv`: one row per model and directness level (6)

Supports Table F3 (Codex rows, L2 to L4 columns). As `claude_code_by_level.csv`, for Codex.

Recomputed by `reproduce.py`: no.

### `claude_code_anchors.csv`: one row per model and anchor variant (4)

Supports Appendix F, drift anchors (the smallest Fisher p is 0.29). `q-weak` and `q-nearempty` were
run again beside the naming pairs, to check that the models still behaved as they had in the
selection grid.

| Column | Meaning |
|---|---|
| `e1_invoked`, `e1_total`, `e1_rate` | The anchor in the naming-pair run |
| `a1_invoked`, `a1_total`, `a1_rate` | The same variant in the selection grid (`outcome_skill_invoked_count` in `data/selection/claude_code_variants.csv`) |
| `fisher_p` | Two-sided Fisher exact test of the two |

Recomputed by `reproduce.py`: no.

## execution/

### `associations.csv`: one row per scope, outcome and scorer (462)

Supports §5 only (the incumbent's partial ρ of -0.046 and -0.056, and the paragraph on body
signals). Columns as in `selection_claude_code/associations.csv`, for both execution outcomes
and 21 scorers (all but `description_contains_release_note`).

| Column | Meaning |
|---|---|
| `analysis_scope` | `pooled` (every eligible version), `family:<task>` (one task family), or `arm` (one `actor` and `refiner` pair; 8 arms) |
| `p_holm` | Holm within one scope (one arm, for `arm` rows) and outcome |

Recomputed by `reproduce.py`: no.

### `clustered_associations.csv`: one row per outcome and scorer, plus one seed-quality row per outcome (20)

Supports §5 (the 95% intervals), Appendix E (clustered intervals) and Table G2. The nine pooled
associations of `associations.csv` re-estimated with the lineage as the cluster: our eight text
features controlling for `conformance_overall`, and the incumbent controlling for
`description_word_count`.

| Column | Meaning |
|---|---|
| `per_version` | The partial Spearman with versions as rows |
| `published`, `reproduces_published` | The pooled `partial_spearman` in `associations.csv`, and whether `per_version` matches it within 0.0005 |
| `cluster_ci_lo`, `cluster_ci_hi`, `cluster_excludes_zero` | Lineage-bootstrap 95% interval of `per_version`, and whether it excludes 0 |
| `lineage_mean` | The partial Spearman on one row per lineage (the lineage means of scorer, outcome and control) |
| `within_lineage` | Spearman of scorer and outcome after centring both on each lineage's mean (no control) |
| `between_lineage` | Spearman of the lineage means of scorer and outcome (no control) |
| `between_lineage_within_arm` | `between_lineage` after centring each arm's lineage means on that arm's mean |
| `between_x_vs_seed_quality` | Spearman of the scorer's lineage mean with seed quality (poor 0, medium 1, good 2) |

In the `__lineage_mean_performance__` rows (`control` is `seed_quality`), only `between_lineage` is
filled: the Spearman of lineage-mean performance with seed quality.

Recomputed by `reproduce.py`: no.

### `within_between.csv`: one row per outcome, scorer and control (72)

Internal check. The nine scorers of `scorers/partial_spearman.csv`, each with the four trivial
baselines as controls. `within_lineage` and `between_lineage` are as in
`clustered_associations.csv` and take no control: the control only decides which rows are complete,
so the values repeat across the four controls. `status` is `estimated` or `uninformative (low
range)` (`sc_body`, which takes one value). `within_between_arm.csv` reproduces these values, and
the paper cites that table.

Recomputed by `reproduce.py`: no.

### `within_between_arm.csv`: one row per outcome and scorer (28)

Supports §5 (body signals mostly mark refinement), Figure 2, Appendix E (within and between
lineages) and Table G3. The nine scorers of `within_between.csv` and our five body features
(`has_numbered_steps`, `body_line_count`, `imperative_opener_count`, `has_worked_example`,
`has_code_block`), split into within-lineage, between-lineage and arm-centred between-lineage
parts, as in `clustered_associations.csv`.

| Column | Meaning |
|---|---|
| `n_arms` | Arms (actor and refiner pairs) among the lineages |
| `arm_ci_low`, `arm_ci_high` | 95% interval of `between_lineage_within_arm` from 10,000 draws that resample lineages within each arm |
| `arm_ci_draws` | Draws that gave an estimate (0 where there is none) |

Recomputed by `reproduce.py`: no.

### `sensitivity_newline.csv`: one row per outcome, baseline and scorer version (16)

Supports §5 (restoring the five points leaves no association), Figure 1 (the † row) and Table G1
(the newline row). `scorer` is `sc_score` or `sc_score_newline_adjusted`, which adds back the 5
points `skill-check` deducts for a missing trailing newline. `n_distinct` is the number of distinct
scores; `delta_r2_adding_scorer` and `partial_spearman` are against `baseline`.

Recomputed by `reproduce.py`: no.

### `corpus_composition.json`: the makeup of the execution corpus and how its lineages ended

Supports §3 (517 versions in 68 lineages, 465 scored on training instances, 120 held out), §6 (64
of 68 lineages stopped at the six-round cap; 67 had gone two or more rounds without an accepted
rewrite) and Appendix C.

| Key | Meaning |
|---|---|
| `composition` | Versions by `artifact_role`, among all versions, the training set and the held-out set, with their totals `n_all`, `n_train` and `n_heldout` |
| `termination.quiet_tail_distribution` | Lineages by the number of rounds since their last accepted rewrite |
| `termination.accepted_improvements_distribution` | Lineages by their number of accepted rewrites |
| `termination.at_least_1_quiet`, `at_least_2_quiet`, `at_least_4_quiet` | Lineages whose last 1, 2 or 4 rounds or more accepted no rewrite |
| `termination.hit_iteration_cap` | Lineages that reached round 6, the cap |

The termination counts follow from `data/execution/lineage_termination.csv`.

Recomputed by `reproduce.py`: no.

## scorers/

### `partial_spearman.csv`: one row per scope, scorer and control (82)

Supports §4, §5 (`skill-check`'s partial ρ of -0.38 to -0.55), Figure 1 (both panels; the
whiskers are the bootstrap columns) and Tables F1 and G1. Selection rows (`invocation:*`) use the
Claude Code rates and five scorers (`sc_score`, `sc_description`, `mk_description_quality`,
`ss_total`, `conformance_overall`), each controlling for `description_word_count`. Execution rows
use nine scorers, each controlling for each of the four trivial baselines.

| Column | Meaning |
|---|---|
| `p_holm` | Holm within one scope |
| `bootstrap_ci_low`, `bootstrap_ci_high` | Execution only: lineage-bootstrap 95% interval |
| `bootstrap_draws` | Draws that gave an estimate, out of 10,000 |
| `status` | `estimated`, or `uninformative (low range)`: no estimate for `sc_body`, which takes one value |
| `p_permutations` | Always empty: permutation tests apply only at n ≤ 9 |

Recomputed by `reproduce.py`: partly, `partial_spearman` and `p_holm` in every row. With
`--bootstrap` it also checks `bootstrap_ci_low` and `bootstrap_ci_high` in the 64 estimated
execution rows.

### `incremental_validity.csv`: one row per scope, scorer and baseline (82)

Supports §4, §5 (`skill-check`'s gain of up to +0.16 R²), Tables F1 and G1, and the paragraph after
Table G1 (the incumbent's execution gain of +0.03 to +0.04 over word count). The same scopes,
scorers and baselines as `partial_spearman.csv`.

Recomputed by `reproduce.py`: partly, `delta_r2_adding_scorer` and `delta_r2_adding_baseline` in
every row; not the three `r2_*` columns.

### `minimum_detectable_effect.csv`: one row per estimated row of `partial_spearman.csv` (74)

Supports §7 (the tests detect only partial correlations above 0.68 for selection and 0.16 to 0.33
for execution), Figure 1 (the grey bars) and Table E1. Each value is the smallest absolute partial
Spearman the test detects with 80% power, two-sided.

| Column | Meaning |
|---|---|
| `holm_family_size` | Tests in the row's Holm family |
| `method`, `se` | Selection: found by simulating the same test at n = 17. Execution: from `se`, the standard deviation of the 10,000 lineage-bootstrap draws |
| `mde_alpha05` | At α = 0.05. For execution, 2.80 × `se`, capped at 1 |
| `mde_holm_first_step` | At α / `holm_family_size`, the strictest Holm step |
| `analytic_mde_alpha05`, `analytic_mde_holm_first_step` | Selection only: the Fisher-z approximation, tanh((z(1 - α/2) + z(0.8)) × sqrt(1.06 / (n - 4))), with z the standard normal quantile |
| `naive_mde_versions_alpha05`, `naive_mde_lineages_alpha05` | Execution only: the same approximation at α = 0.05 with n = versions or n = lineages, ignoring the clustering |
| `abs_rho_ge_mde_alpha05` | The absolute `partial_spearman` is at least `mde_alpha05` |

Recomputed by `reproduce.py`: no.

### `range_check.csv`: one row per scope and scorer (28)

Supports Appendix F, other notes (`skill-check`'s description category takes two values across the
17 variants), Table G1 (the row for `skill-check`'s constant body category) and Figure 1 (its
"n/a (constant)" entries). `n_rows`, `n_distinct_non_null` and `null_count` count the values in
the scope; `low_range` is true below 5 distinct values, and `status` is then `low_range` rather
than `available`.

Recomputed by `reproduce.py`: no.

### `determinism.csv`: one row per tool, skill and output variable (540)

Supports Appendix D, scorer staging (a 20-skill subset scored three times gave identical values).
The four independent tools scored 20 skills drawn at random (4 selection variants, `B__<variant>`,
and 16 execution versions, `A__<run>__<artifact>`) three times: `run1` is the main scoring run and
`run2` and `run3` are repeats. `identical` is true in all 540 rows.

Recomputed by `reproduce.py`: no.

### `validator_version_check.csv`: one row per skill (542)

Supports Appendix A, version (validator 1.5.6 gives the same scores and check outcomes as 1.1.2),
and with it the version listed in Table 1. The 17 selection variants (`B__`), the 517 execution
versions (`A__`) and the 8 naming-pair variants (`E1__`).

| Column | Meaning |
|---|---|
| `same_score` | `score_1.1.2` equals `score_1.5.6` |
| `checks_compared` | Per-check outcomes compared: 10 for most skills, 1 for the 10 versions whose frontmatter fails to parse, 0 for the naming-pair variants, whose 1.1.2 check outcomes were not recorded |
| `check_differences`, `error` | Checks whose outcome differs, and any tool error (none in either) |

Recomputed by `reproduce.py`: no.

## The §6 probe

No table in `results/` holds the cheap probe. To compute Table H1's R² values from
`data/probe/impact_log_deltas.csv`, take, for each `refiner` and `actor` arm, the rows with
`rescored = True` and compute the Pearson correlation between `v0_train_new` and
`delta_train_new`. R² is its square.

| Arm | Correlation | R² |
|---|---|---|
| `sol` x `qwen` | -0.874 | 0.764 |
| `opus` x `nemo` | -0.941 | 0.885 |
| `opus` x `qwen` | -0.736 | 0.542 |
| `sol` x `deepseek` | -0.984 | 0.969 |

The `sol` x `muse` arm never moved (`delta_train_new` is 0 in all nine lineages), so it has no
correlation. The `sol` x `nemo` arm was not re-scored.
