# Data dictionary

## Conventions

- Booleans are `True` / `False`. An empty field is a missing value, never 0: a tool that fails on a
  skill, or an outcome not measured (held-out scores exist only for seeds and accepted versions).
- `directness`: how plainly the selection prompt asks for release notes. `L1` names the skill (the
  positive control); `L2` asks for release notes outright; `L3` asks less directly; `L4` never
  mentions release notes. The prompts are in `stimuli/prompts/`.
- `instance_id`: task instance, `train-01` to `train-08` for selection.

### Models

| Short name | Model | Role |
|---|---|---|
| `qwen` | `qwen3.6-35b` | selection and execution actor |
| `deepseek` | `deepseek-v4-flash` | selection and execution actor |
| `muse` | `meta/muse-glimmer-30b` | execution actor |
| `nemo` | `nvidia/nvidia-nemotron-nano-9b-v2` | execution actor |
| `llama` | `meta/llama-3.1-8b-instruct` | execution actor (`docstring_api` only) |
| `sol` | GPT-5.6 (`gpt-5.6-sol`) | refiner |
| `opus` | Claude Opus 5 (`claude-opus-5`) | refiner |

Harnesses: Claude Code (selection grid 2.1.231; naming pairs 2.1.285) and Codex CLI 0.155.1.

### Scorers and column prefixes

| Prefix | Tool | Version | Notes |
|---|---|---|---|
| `conformance_` | Skilldex validator (the incumbent) | 1.1.2 | Version 1.5.6, listed in the paper, gives identical scores and check outcomes on all 542 skills (`results/scorers/validator_version_check.csv`) |
| `sc_` | `skill-check` | 1.2.0 | `sc_file` includes the trailing-newline check discussed in the paper |
| `mk_` | `skillcheck` | 1.5.0 | Scores the description only |
| `ss_` | `skillscore` | 0.10.0 | Category points; `ss_total` is the aggregate |
| `sv_` | `skill-validator` | 1.6.2 | Body metrics; no aggregate score |

Trivial baselines and our body features (no prefix): `description_word_count` (whitespace-delimited
words in the frontmatter description), `body_token_count` (body length in `cl100k_base` tokens,
excluding frontmatter), `has_code_block` (a fenced code block), `has_numbered_steps` (a Markdown
numbered-list item), `body_line_count` (physical body lines, including blanks),
`imperative_opener_count` (sentences or list items opening with a listed imperative verb; a lexical
heuristic), `has_worked_example` (an example-labelled heading or sentence),
`description_trigger_cue_count` (explicit when-to-use phrases in the description).

---

## data/selection/

### `claude_code_cells.csv`: one row per Claude Code cell (864)

816 grid cells (17 variants x 24 cells x 2 models) and 48 no-skill baseline cells.

| Column | Meaning |
|---|---|
| `actor` | `qwen` or `deepseek` |
| `block` | `corpus_b` (the 17-variant grid) or `baseline` (no skill installed; `variant` empty) |
| `variant` | Description variant; texts in `stimuli/descriptions/` |
| `directness`, `instance_id` | See Conventions |
| `rep` | Repetition index (one repetition per cell) |
| `skill_invoked` | The harness log records a non-errored call of the skill |
| `triggered` | **The selection outcome**: the trigger verdict, true when the execution trace (the agent reading the skill's file) or the harness log is positive; the fingerprint breaks ties. It agrees with `skill_invoked` in every released cell |
| `fingerprint` | The agent's output carried the trailer string defined only in the skill |
| `wrote_artifact` | The agent wrote the requested release-notes file |
| `task_score` | Rubric score of that file (not used for selection) |
| `source_run` | Which run produced the cell (`hoisted`, `perturb` or `grid` arm, and level) |

### `claude_code_variants.csv`: one row per variant and model (34)

| Column | Meaning |
|---|---|
| `family`, `structural_perturbation` | Description family, and the conformance defect added, if any (broken file reference, malformed name, extra subdirectory) |
| `description_contains_release_note` | The description contains "release note(s)" |
| `outcome_skill_invoked_count`, `outcome_cell_count`, `outcome_expected_cells` | Invoked cells, completed cells, expected cells (24) |
| `outcome_invocation_rate` | Invoked / 24; the selection outcome analysed |
| `outcome_complete`, `outcome_read_errors` | All 24 cells complete; unreadable cell records (0 throughout) |
| `conformance_overall` | The incumbent's score, 0 to 100 |
| `conformance_check_*` | One pass indicator (1 = pass) per check, eleven checks |
| `conformance_description_subtotal` | Points from the three description checks, 0 to 33 |
| other columns | Trivial baselines and body features (see Conventions) |

### `codex_cells.csv`: one row per Codex CLI cell (1,264)

| Column | Meaning |
|---|---|
| `block` | `corpus_b` (17-variant grid), `e1` (naming pairs), `baseline` (no skill), `positive_control` (L1 prompt names the skill) |
| `triggered_amended` | **The selection outcome used in the paper**: the pre-registered trace rule plus reads detected from captured command output (24 cells changed, each checked by hand) |
| `triggered_original` | The pre-registered rule alone; gives the same verdicts |
| `exec_trace`, `output_trace` | Trigger evidence from command paths and from captured command output |
| `attempted_trace`, `attempted_selection_amended` | The agent tried to read the installed skill's file under any root (secondary measure) |
| `skill_listed` | The installed skill appeared in Codex's skill listing (in every cell with a skill) |
| `fingerprint`, `wrote_artifact`, `score` | As for Claude Code |

### `independent_scores.csv`: the four independent tools on the 17 variants (17)

Same columns as `data/execution/independent_scores.csv`.

## data/naming/

### `claude_code_cells.csv`: one row per Claude Code naming cell (480)

Columns as in `data/selection/claude_code_cells.csv`; `block` is `e1`. Variants `e1-pNN` name
"release notes" and `e1-nNN` use the skill's own term, "impact log", at the same length `NN`
(3, 12, 25 or 44 words), body and conformance; `q-weak` and `q-nearempty` are anchors.

### `claude_code_counts.csv` (80)

`invoked` / `total` = `rate` per `actor`, `variant` and `level` (`L2`, `L3`, `L4`, or `all`).

## data/execution/

### `versions.csv`: one row per skill version (517)

| Column | Meaning |
|---|---|
| `run` | Lineage ID (refiner, actor, seed quality, replicate) |
| `refiner`, `actor`, `seed_quality`, `replicate`, `task` | Arm and seed; `task` is `impact_log` or `docstring_api` |
| `artifact`, `iteration` | Version within the lineage (`v0` is the seed; `vN-candidate` a rewrite) |
| `artifact_role` | `seed`, `accepted`, `rejected_candidate`, or `accepted_candidate_duplicate` (a second copy of an accepted version, excluded) |
| `accepted`, `rejection_reason` | Whether the paired test accepted the rewrite; `worse` or `indistinguishable` |
| `duplicate_of`, `analysis_eligible` | Second copies are not eligible; 465 versions are |
| `content_sha256` | Hash of the version's `SKILL.md` |
| `outcome_train_mean` | **Execution outcome**: mean rubric score on the 8 training instances |
| `outcome_heldout_mean` | Mean rubric score on the 8 held-out instances (seeds and accepted versions only) |
| `scoring_reps`, `rescored` | Repetitions per instance behind the outcome (2, or 6 where re-scored) |
| other columns | Incumbent checks, trivial baselines and body features, as for selection |

### `independent_scores.csv`: the four independent tools on the 517 versions (517)

| Column | Meaning |
|---|---|
| `skill_id`, `corpus`, `variant`, `run`, `artifact`, `content_sha256` | Join keys (`corpus` A = execution, B = selection) |
| `frontmatter_name`, `staged_as_placeholder` | Name used to stage the skill for scoring; placeholder only if the name is missing or unusable (never, here) |
| `sc_*` | `skill-check` score and categories; `sc_rule_ids` lists the rules that fired |
| `mk_*` | `skillcheck` description-quality score and components |
| `sv_*` | `skill-validator` body metrics |
| `ss_*` | `skillscore` total and categories |
| `*_status` | `ok`, or why the tool failed (`skillcheck` cannot parse the 10 versions whose frontmatter is not valid YAML) |

### `lineage_termination.csv`: one row per lineage (68)

`last_iteration`, `n_accepted_improvements`, `last_accepted_iteration`, and `quiet_tail` (rounds
since the last accepted rewrite).

## data/probe/

### `impact_log_deltas.csv`: one row per `impact_log` lineage (54)

Starting score `v0`, plateau and refinement distance `delta` (plateau minus `v0`) on training
instances, before (`_old`, 2 repetitions) and after (`_new`, 6 repetitions) re-scoring.
`rescored = False` marks the GPT-5.6 x `nemo` arm, which was not re-scored.

### `rescored_lineages.csv` (14) and `rescored_versions.csv` (23)

The `docstring_api` seeds and endpoints re-scored at 6 repetitions, with training and held-out
scores before and after; used for the claim that `v0` orders the seeds by quality without overlap.

## stimuli/

### `descriptions/<variant>/`

The 25 description variants as installed: the 17 selection variants and the 8 naming-pair variants
(`e1-*`). Each folder holds the variant's `SKILL.md`; variants with a structural defect also hold
the extra file that creates it (a renamed reference file, or a placeholder in an extra
subdirectory).

### `prompts/L1.md` to `L4.md`

The selection prompts at each directness level (see Conventions). Placeholders filled per task
instance: `{version}` and `{changes}` (the pending changes) in every prompt, and `{artifact}` (the
file to write) in L1 and L2.

### `skill_versions/<run>/<artifact>/SKILL.md`

The text of each of the 517 execution-corpus versions. `<run>` and `<artifact>` are the
`run` and `artifact` columns of `data/execution/versions.csv`, and each file's SHA-256 equals that
row's `content_sha256`.
