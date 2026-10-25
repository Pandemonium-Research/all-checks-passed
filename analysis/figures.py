#!/usr/bin/env python3
"""Draw the paper's two figures from results/.

- Figure 1 (fig_forest.pdf): each score's partial Spearman correlation with selection and with
  execution, controlling for description word count, with the execution lineage-bootstrap
  intervals and each row's undetectable range at 80% power. Reads results/scorers/
  partial_spearman.csv and minimum_detectable_effect.csv, and results/execution/
  sensitivity_newline.csv for the row with skill-check's newline rule removed.
- Figure 2 (fig_markers.pdf): body signals within lineages, between lineages, and between
  lineages with arms centred, with the arm-centred 95% intervals. Reads results/execution/
  within_between_arm.csv; our own features are checked against clustered_associations.csv.

The paper sets the figures in Open Sans. It is used if installed, or if --fonts names a folder
holding its .ttf files; otherwise matplotlib's default sans-serif is used.

usage: python3 analysis/figures.py [--fonts DIR] [--out DIR]   (needs matplotlib; writes to figures/)
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib import font_manager
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

INK = "#0b0b0b"
MUTED = "#52514e"
GRID = "#e1e0d9"
MDE_FILL = "#e9e7df"
WHITE = "#ffffff"

# Okabe--Ito colours; marker shape and fill provide redundant encodings.
COLOURS = {
    "qwen": "#0072B2",
    "deepseek": "#D55E00",
    "execution:train": "#009E73",
    "execution:held-out": "#CC79A7",
}
MARKERS = {
    "qwen": "o",
    "deepseek": "s",
    "execution:train": "o",
    "execution:held-out": "s",
}

SELECTION_ROWS = [
    ("Incumbent", "conformance_overall"),
    ("skill-check total", "sc_score"),
    ("skill-check description", "sc_description"),
    ("skillcheck description quality", "mk_description_quality"),
    ("skillscore total", "ss_total"),
]

EXECUTION_ROWS = [
    ("Incumbent", "conformance_overall", False),
    ("skill-check total", "sc_score", False),
    ("skill-check, newline rule removed†", "sc_score_newline_adjusted", True),
    ("skill-check body", "sc_body", False),
    ("skillscore total", "ss_total", False),
    ("skillscore instruction quality", "ss_instruction_quality", False),
    ("skillscore structure", "ss_structure_progressive_disclosure", False),
    ("skill-validator imperative ratio", "sv_imperative_ratio", False),
    ("skill-validator information density", "sv_information_density", False),
    ("skill-validator instruction specificity", "sv_instruction_specificity", False),
]

# Figure 2. Shape and fill are redundant encodings for greyscale.
PARTS = [
    ("within_lineage", "within a lineage", "#009E73", "o", True),
    ("between_lineage", "between lineages", "#D55E00", "o", False),
    ("between_lineage_within_arm", "between lineages, arms centred", "#0072B2", "D", True),
]
OURS = [
    ("numbered steps", "has_numbered_steps"),
    ("body line count", "body_line_count"),
    ("imperative openers", "imperative_opener_count"),
    ("worked example", "has_worked_example"),
    ("code block", "has_code_block"),
]
# The external body signals that rise within lineages (skillscore's structure category falls).
EXTERNAL = [
    ("skillscore instruction quality", "ss_instruction_quality"),
    ("skill-validator instruction specificity", "sv_instruction_specificity"),
    ("skill-validator imperative ratio", "sv_imperative_ratio"),
    ("skill-validator information density", "sv_information_density"),
]
SPLITS = [("Held-out instances", "outcome_heldout_mean", "execution:held-out"),
          ("Training instances", "outcome_train_mean", "execution:train")]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"required input is missing: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def exactly_one(rows: list[dict[str, str]], *, source: str, **wanted: str) -> dict[str, str]:
    matches = [row for row in rows if all(row.get(key) == value for key, value in wanted.items())]
    if len(matches) != 1:
        description = ", ".join(f"{key}={value!r}" for key, value in wanted.items())
        raise RuntimeError(
            f"expected exactly one row in {source} for {description}; found {len(matches)}"
        )
    return matches[0]


def number(row: dict[str, str], field: str, *, source: str) -> float:
    raw = row.get(field, "")
    if raw == "":
        raise RuntimeError(f"missing {field!r} in {source} row: {row}")
    try:
        return float(raw)
    except ValueError as exc:
        raise RuntimeError(f"invalid {field!r}={raw!r} in {source} row: {row}") from exc


def register_fonts(font_dir: Path | None) -> None:
    if font_dir is not None:
        for font_path in sorted(font_dir.rglob("OpenSans*.ttf")):
            font_manager.fontManager.addfont(str(font_path))
    installed = any(f.name == "Open Sans" for f in font_manager.fontManager.ttflist)
    plt.rcParams.update(
        {
            "font.family": "Open Sans" if installed else "sans-serif",
            "font.size": 8,
            "text.color": INK,
            "axes.labelcolor": MUTED,
            "axes.titlecolor": INK,
            "xtick.color": MUTED,
            "ytick.color": INK,
            "pdf.fonttype": 42,
        }
    )


def set_axis_style(ax: plt.Axes) -> None:
    ax.set_xlim(-1, 1)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xticklabels(["−1", "−0.5", "0", "0.5", "1"])
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.65, zorder=0)
    ax.axvline(0, color=MUTED, linewidth=0.8, linestyle=(0, (3, 2)), zorder=1)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0)


def forest(out: Path) -> None:
    partial_all = read_csv(RESULTS / "scorers/partial_spearman.csv")
    mde_all = read_csv(RESULTS / "scorers/minimum_detectable_effect.csv")
    sensitivity_all = read_csv(RESULTS / "execution/sensitivity_newline.csv")

    # The main inputs use `control`; the sensitivity file calls the same field `baseline`.
    partial = [row for row in partial_all if row.get("control") == "description_word_count"]
    mde_rows = [row for row in mde_all if row.get("control") == "description_word_count"]
    sensitivity = [
        row for row in sensitivity_all if row.get("baseline") == "description_word_count"
    ]

    fig, (left, right) = plt.subplots(1, 2, figsize=(6.4, 2.4))
    set_axis_style(left)
    set_axis_style(right)

    # Selection: one common band for the 17 variants, verified rather than assumed.
    selection_mdes: set[float] = set()
    selection_y = list(range(len(SELECTION_ROWS) - 1, -1, -1))
    selection_offsets = {"qwen": 0.12, "deepseek": -0.12}
    for (label, scorer), y in zip(SELECTION_ROWS, selection_y):
        for actor in ("qwen", "deepseek"):
            scope = f"invocation:{actor}"
            prow = exactly_one(partial, source="partial_spearman.csv", corpus="B", scope=scope,
                               actor=actor, scorer=scorer)
            mrow = exactly_one(mde_rows, source="minimum_detectable_effect.csv", corpus="B",
                               scope=scope, actor=actor, scorer=scorer)
            if prow.get("status") != "estimated":
                raise RuntimeError(f"selection row is not estimated: {prow}")
            rho = number(prow, "partial_spearman", source="partial_spearman.csv")
            p_holm = number(prow, "p_holm", source="partial_spearman.csv")
            mde = number(mrow, "mde_alpha05", source="minimum_detectable_effect.csv")
            selection_mdes.add(mde)
            filled = p_holm < 0.05
            colour = COLOURS[actor]
            left.plot(
                rho,
                y + selection_offsets[actor],
                marker=MARKERS[actor],
                markersize=4.4,
                markerfacecolor=colour if filled else WHITE,
                markeredgecolor=colour,
                markeredgewidth=1.25,
                linestyle="none",
                zorder=4,
            )

    if len(selection_mdes) != 1:
        raise RuntimeError(f"expected one common selection MDE; found {sorted(selection_mdes)}")
    selection_mde = selection_mdes.pop()
    left.axvspan(-selection_mde, selection_mde, color=MDE_FILL, zorder=0.25)
    left.text(
        0,
        -0.53,
        "below detectable effect (80% power)",
        color=MUTED,
        fontsize=5.8,
        fontstyle="italic",
        ha="center",
        va="center",
        zorder=5,
        bbox=dict(facecolor=MDE_FILL, edgecolor="none", pad=0.6),
    )
    left.set_ylim(-0.72, 4.55)
    left.set_yticks(selection_y)
    left.set_yticklabels([label for label, _ in SELECTION_ROWS], fontsize=6.5)
    left.set_title("Selection (invocation rate; 17 variants per model)", fontsize=7.4, pad=4)

    # Execution: scope-specific intervals and MDE bands; the sensitivity row is point-only.
    execution_y = list(range(len(EXECUTION_ROWS) - 1, -1, -1))
    execution_offsets = {"execution:train": 0.13, "execution:held-out": -0.13}
    for (label, scorer, point_only), y in zip(EXECUTION_ROWS, execution_y):
        if point_only:
            for scope in ("execution:train", "execution:held-out"):
                srow = exactly_one(sensitivity, source="sensitivity_newline.csv", scope=scope,
                                   scorer=scorer)
                rho = number(srow, "partial_spearman", source="sensitivity_newline.csv")
                colour = COLOURS[scope]
                right.plot(
                    rho,
                    y + execution_offsets[scope],
                    marker=MARKERS[scope],
                    markersize=4.4,
                    markerfacecolor=WHITE,
                    markeredgecolor=colour,
                    markeredgewidth=1.25,
                    linestyle="none",
                    zorder=4,
                )
            continue

        entries = [(scope, exactly_one(partial, source="partial_spearman.csv", corpus="A",
                                       scope=scope, actor="", scorer=scorer))
                   for scope in ("execution:train", "execution:held-out")]

        if all(prow.get("status") != "estimated" for _, prow in entries):
            right.text(
                -0.97,
                y,
                "n/a (constant)",
                color=MUTED,
                fontsize=6.0,
                fontstyle="italic",
                ha="left",
                va="center",
                zorder=4,
            )
            continue

        for scope, prow in entries:
            if prow.get("status") != "estimated":
                right.text(
                    -0.97,
                    y + execution_offsets[scope],
                    "n/a (constant)",
                    color=MUTED,
                    fontsize=6.0,
                    fontstyle="italic",
                    ha="center",
                    va="center",
                    zorder=4,
                )
                continue

            mrow = exactly_one(mde_rows, source="minimum_detectable_effect.csv", corpus="A",
                               scope=scope, actor="", scorer=scorer)
            rho = number(prow, "partial_spearman", source="partial_spearman.csv")
            low = number(prow, "bootstrap_ci_low", source="partial_spearman.csv")
            high = number(prow, "bootstrap_ci_high", source="partial_spearman.csv")
            if low > rho or rho > high:
                raise RuntimeError(f"estimate is outside its interval: {prow}")
            mde = number(mrow, "mde_alpha05", source="minimum_detectable_effect.csv")
            filled = low > 0 or high < 0
            ypos = y + execution_offsets[scope]
            colour = COLOURS[scope]
            right.barh(
                ypos,
                2 * mde,
                left=-mde,
                height=0.22,
                color=MDE_FILL,
                edgecolor="none",
                zorder=0.5,
            )
            right.errorbar(
                rho,
                ypos,
                xerr=[[rho - low], [high - rho]],
                fmt=MARKERS[scope],
                markersize=4.4,
                markerfacecolor=colour if filled else WHITE,
                markeredgecolor=colour,
                markeredgewidth=1.25,
                ecolor=colour,
                elinewidth=0.9,
                capsize=1.8,
                capthick=0.9,
                linestyle="none",
                zorder=4,
            )

    right.set_ylim(-0.55, 9.55)
    right.set_yticks(execution_y)
    right.set_yticklabels([label for label, _, _ in EXECUTION_ROWS], fontsize=6.5)
    right.set_title("Execution (versions in 68 lineages)", fontsize=7.4, pad=4)

    fig.text(
        0.59,
        0.205,
        "partial Spearman ρ, controlling for description word count",
        ha="center",
        va="center",
        color=MUTED,
        fontsize=7.2,
    )

    handles = [
        Line2D(
            [],
            [],
            marker=MARKERS[key],
            markerfacecolor=WHITE,
            markeredgecolor=COLOURS[key],
            markeredgewidth=1.25,
            color="none",
            markersize=4.4,
            label=label,
        )
        for key, label in [
            ("qwen", "qwen"),
            ("deepseek", "deepseek"),
            ("execution:train", "training"),
            ("execution:held-out", "held-out"),
        ]
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.085),
        ncol=4,
        frameon=False,
        fontsize=6.5,
        handletextpad=0.35,
        columnspacing=1.0,
    )
    fig.text(
        0.5,
        0.04,
        "filled = Holm p < 0.05 (selection) or 95% lineage-bootstrap interval excludes 0 (execution)",
        ha="center",
        va="center",
        color=MUTED,
        fontsize=6.0,
    )

    fig.subplots_adjust(left=0.21, right=0.985, top=0.88, bottom=0.33, wspace=0.78)
    fig.savefig(out, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def marker_rows(outcome: str, scope: str) -> list[tuple[str, dict | None]]:
    arm = read_csv(RESULTS / "execution/within_between_arm.csv")
    clustered = read_csv(RESULTS / "execution/clustered_associations.csv")
    rows = []
    for label, scorer in OURS:
        row = exactly_one(arm, source="within_between_arm.csv", scope=scope, scorer=scorer)
        reference = exactly_one(clustered, source="clustered_associations.csv", outcome=outcome,
                                scorer=scorer, control="conformance_overall")
        for field in ("within_lineage", "between_lineage", "between_lineage_within_arm"):
            if round(float(row[field]), 4) != round(float(reference[field]), 4):
                raise RuntimeError(f"{scope} {scorer} {field} disagrees with clustered_associations.csv")
        rows.append((label, row))
    for label, scorer in EXTERNAL:
        row = exactly_one(arm, source="within_between_arm.csv", scope=scope, scorer=scorer)
        rows.append((label, row if row["status"] == "estimated" else None))
    return rows


def markers(out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.4), sharey=True)
    n = len(OURS) + len(EXTERNAL)
    ys = list(range(n - 1, -1, -1))
    offsets = {"within_lineage": 0.2, "between_lineage": 0.0, "between_lineage_within_arm": -0.2}
    for ax, (title, outcome, scope) in zip(axes, SPLITS):
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(length=0, labelsize=6.5)
        ax.tick_params(axis="y", colors=MUTED)
        ax.grid(axis="x", color=GRID, linewidth=0.65, zorder=0)
        ax.axvline(0, color=MUTED, linewidth=0.9, linestyle=(0, (3, 2)), zorder=1)
        ax.axhline(len(EXTERNAL) - 0.5, color=GRID, linewidth=0.8, zorder=0)
        for (label, row), y in zip(marker_rows(outcome, scope), ys):
            if row is None:
                continue
            for field, _, colour, marker, filled in PARTS:
                x = float(row[field])
                if field == "between_lineage_within_arm":
                    low, high = float(row["arm_ci_low"]), float(row["arm_ci_high"])
                    ax.plot([low, high], [y + offsets[field]] * 2, color=colour, linewidth=0.9,
                            solid_capstyle="butt", zorder=2)
                ax.plot(x, y + offsets[field], marker=marker, markersize=4.2,
                        markerfacecolor=colour if filled else WHITE, markeredgecolor=colour,
                        markeredgewidth=1.2, linestyle="none", zorder=3)
        ax.set_xlim(-1, 1)
        ax.set_xticks([-1, -0.5, 0, 0.5, 1])
        ax.set_xticklabels(["−1", "−0.5", "0", "0.5", "1"])
        ax.set_ylim(-0.6, n - 0.2)
        ax.set_title(title, fontsize=7.4, pad=4)
    axes[0].set_yticks(ys)
    axes[0].set_yticklabels([label for label, _ in OURS + EXTERNAL], fontsize=6.5)
    # Group labels sit inside the left panel, just above each group's first row.
    axes[0].text(-0.97, n - 0.5, "our features", fontsize=5.8, color=MUTED, fontstyle="italic",
                 ha="left", va="bottom")
    axes[0].text(-0.97, len(EXTERNAL) - 0.48, "external tools", fontsize=5.8, color=MUTED,
                 fontstyle="italic", ha="left", va="bottom")
    fig.text(0.6, 0.155, "Spearman ρ with performance", ha="center", va="center", color=MUTED,
             fontsize=7.2)
    handles = [Line2D([], [], marker=marker, markersize=4.2, color="none", markeredgewidth=1.2,
                      markerfacecolor=colour if filled else WHITE, markeredgecolor=colour, label=text)
               for _, text, colour, marker, filled in PARTS]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.6, 0.0), ncol=3,
               frameon=False, fontsize=6.5, handletextpad=0.35, columnspacing=1.2)
    fig.subplots_adjust(left=0.27, right=0.985, top=0.9, bottom=0.26, wspace=0.1)
    fig.savefig(out, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fonts", type=Path, help="folder holding the Open Sans .ttf files")
    parser.add_argument("--out", type=Path, default=ROOT / "figures")
    args = parser.parse_args()
    register_fonts(args.fonts)
    args.out.mkdir(parents=True, exist_ok=True)
    forest(args.out / "fig_forest.pdf")
    markers(args.out / "fig_markers.pdf")
    print(f"wrote {args.out / 'fig_forest.pdf'} and {args.out / 'fig_markers.pdf'}")


if __name__ == "__main__":
    main()
