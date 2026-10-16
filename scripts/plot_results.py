
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cnsplots as cns


# =========================================================
# 1. COLOR PALETTES
# =========================================================

PALETTE = [
    "#355C7D",  # Navy blue
    "#278C87",  # Teal
    "#D9825B",  # Terracotta
    "#8172B2",  # Muted purple
    "#6C91BF",  # Steel blue
    "#929BA6",  # Slate gray
    "#C5A44D",  # Muted gold
    "#6A9F70",  # Soft green
    "#C76D83",  # Dusty rose
    "#52616B",  # Charcoal blue
]

ENCODING_PALETTE = {
    "pairwise": "#355C7D",
    "seqcounter": "#278C87",
    "ladder": "#8172B2",
    "commander": "#D9825B",
    "binary": "#6C91BF",
    "product": "#C5A44D",
}

SOLVER_PALETTE = {
    "SAT_SeqCounter": "#278C87",
    "CP-SAT": "#D9825B",
    "CPLEX_CP": "#8172B2",
    "MIP": "#355C7D",
    "CBC": "#6C91BF",
    "SCIP": "#6A9F70",
    "Gurobi": "#C76D83",
    "HiGHS": "#C5A44D",
}


# =========================================================
# 2. GLOBAL STYLE
# =========================================================

def configure_style():
    sns.set_theme(
        style="white",
        context="paper",
        font_scale=1.05,
        rc={
            # Background
            "figure.facecolor": "#FFFFFF",
            "axes.facecolor": "#FFFFFF",
            "savefig.facecolor": "#FFFFFF",
            "savefig.transparent": False,

            # Typography
            "font.family": "sans-serif",
            "font.size": 9,
            "text.color": "#263445",
            "axes.labelcolor": "#374151",
            "axes.titlecolor": "#263445",
            "axes.titleweight": "bold",

            # Axes
            "axes.edgecolor": "#D5DAE1",
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": False,

            # Ticks
            "xtick.color": "#596579",
            "ytick.color": "#596579",
            "xtick.major.size": 3,
            "ytick.major.size": 3,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,

            # Legend
            "legend.fontsize": 8,
            "legend.title_fontsize": 9,
        },
    )


# =========================================================
# 3. AXIS FORMATTING
# =========================================================

def prepare_axis(ax, title, xlabel, ylabel, log_y=False):
    ax.set_title(
        title,
        fontsize=11,
        fontweight="bold",
        loc="left",
        pad=12,
        color="#263445",
    )

    ax.set_xlabel(
        xlabel,
        fontsize=9,
        labelpad=7,
    )

    ax.set_ylabel(
        ylabel,
        fontsize=9,
        labelpad=7,
    )

    if log_y:
        ax.set_yscale("log")

    # Remove top and right borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Subtle left and bottom borders
    for side in ["left", "bottom"]:
        ax.spines[side].set_color("#D5DAE1")
        ax.spines[side].set_linewidth(0.8)

    # Clean ticks
    ax.tick_params(
        axis="both",
        which="major",
        direction="out",
        length=3,
        width=0.7,
        colors="#596579",
        labelsize=8,
    )

    # Hide minor tick marks
    ax.tick_params(
        axis="both",
        which="minor",
        length=0,
    )

    # Grid behind data
    ax.set_axisbelow(True)

    # Horizontal major grid only
    ax.grid(
        axis="y",
        which="major",
        color="#E6EAF0",
        linestyle="-",
        linewidth=0.7,
    )

    # Disable minor and vertical grids
    ax.grid(
        axis="y",
        which="minor",
        visible=False,
    )

    ax.grid(
        axis="x",
        which="both",
        visible=False,
    )

    # Small breathing space around data
    ax.margins(x=0.04, y=0.08)


# =========================================================
# 4. LEGEND FORMATTING
# =========================================================

def configure_legend(ax, title, outside=False):
    if outside:
        legend = ax.legend(
            title=title,
            loc="upper left",
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0,
            frameon=False,
            fontsize=8,
            title_fontsize=9,
            handlelength=2.0,
            labelspacing=0.6,
        )
    else:
        legend = ax.legend(
            title=title,
            loc="best",
            frameon=True,
            facecolor="#FFFFFF",
            edgecolor="#E1E5EB",
            framealpha=0.95,
            fontsize=8,
            title_fontsize=9,
            borderpad=0.7,
            labelspacing=0.5,
            handlelength=2.0,
        )

    if legend is not None:
        legend.get_title().set_color("#263445")

        for text in legend.get_texts():
            text.set_color("#374151")

    return legend


# =========================================================
# 5. GENERIC LINE PLOT
# =========================================================

def plot_line_comparison(
    data,
    x,
    y,
    hue,
    palette,
    title,
    xlabel,
    ylabel,
    output_path,
    legend_title,
    log_y=False,
    legend_outside=False,
):
    if data.empty:
        print(f" -> Skipped empty chart: {output_path}")
        return

    # Keep only rows with valid plotting values
    plot_df = data.dropna(subset=[x, y, hue]).copy()

    if plot_df.empty:
        print(f" -> Skipped chart with no valid data: {output_path}")
        return

    # Use only colors for categories actually present
    categories = plot_df[hue].unique()

    if isinstance(palette, dict):
        plot_palette = {
            category: palette[category]
            for category in categories
            if category in palette
        }

        missing = [
            category
            for category in categories
            if category not in plot_palette
        ]

        for i, category in enumerate(missing):
            plot_palette[category] = PALETTE[i % len(PALETTE)]
    else:
        plot_palette = palette

    # Create CNSPlots figure
    cns.figure(300, 200, color_cycle="ECharts")
    ax = plt.gca()

    sns.lineplot(
        ax=ax,
        data=plot_df,
        x=x,
        y=y,
        hue=hue,
        style=hue,
        palette=plot_palette,
        markers=True,
        dashes=False,
        linewidth=2.0,
        markersize=5.5,
        markeredgecolor="#FFFFFF",
        markeredgewidth=0.8,
        estimator=None,
        errorbar=None,
        sort=True,
    )

    prepare_axis(
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        log_y=log_y,
    )

    configure_legend(
        ax=ax,
        title=legend_title,
        outside=legend_outside,
    )

    # Reserve space for an external legend
    if legend_outside:
        plt.tight_layout(rect=[0, 0, 0.78, 1])
    else:
        plt.tight_layout()

    # Save through CNSPlots
    cns.save(output_path)
    plt.close()

    print(f" -> Exported: {output_path}")


# =========================================================
# 6. MAIN FUNCTION
# =========================================================

def generate_plots():

    csv_path = os.path.join("..", "results", "benchmark_data.csv")
    results_dir = os.path.join("..", "results")

    if not os.path.exists(csv_path):
        csv_path = os.path.join("results", "benchmark_data.csv")
        results_dir = "results"

        if not os.path.exists(csv_path):
            print(
                f"Error: Could not find benchmark data at "
                f"'{csv_path}'. Please run run_benchmark.py first."
            )
            return

    os.makedirs(results_dir, exist_ok=True)

    print("=" * 60)
    print(" VISUALIZING EXPERIMENTAL RESULTS VIA CNSPLOTS")
    print(" STYLE: CLEAN SCIENTIFIC")
    print("=" * 60)

    configure_style()

    df = pd.read_csv(csv_path)

    # Keep successful results only
    df_opt = df[
        df["Status"].isin(["OPT", "FEAS"])
    ].copy()

    # -----------------------------------------------------
    # CHART 1: SAT ENCODINGS - SOLVING TIME
    # -----------------------------------------------------

    sat_df = df_opt[
        df_opt["Paradigm"] == "SAT"
    ].copy()

    if not sat_df.empty:
        plot_line_comparison(
            data=sat_df,
            x="N",
            y="Solving_Time",
            hue="Encoding",
            palette=ENCODING_PALETTE,
            title="SAT Encodings: Solving Time vs. Board Size",
            xlabel="Board Size (N x N)",
            ylabel="Solving Time (seconds, log scale)",
            output_path=os.path.join(
                results_dir,
                "sat_encodings_time_comparison.png",
            ),
            legend_title="AMO Encoding",
            log_y=True,
        )

    # -----------------------------------------------------
    # CHART 2: SAT ENCODINGS - CLAUSE COUNTS
    # -----------------------------------------------------

    if not sat_df.empty:
        plot_line_comparison(
            data=sat_df,
            x="N",
            y="Clauses",
            hue="Encoding",
            palette=ENCODING_PALETTE,
            title="SAT Encodings: Clause Count vs. Board Size",
            xlabel="Board Size (N x N)",
            ylabel="Number of CNF Clauses (log scale)",
            output_path=os.path.join(
                results_dir,
                "sat_clauses_count_comparison.png",
            ),
            legend_title="AMO Encoding",
            log_y=True,
        )

    # -----------------------------------------------------
    # CHART 3: CROSS-PARADIGM SOLVING TIME
    # -----------------------------------------------------

    best_sat = df_opt[
        (df_opt["Paradigm"] == "SAT")
        & (df_opt["Encoding"] == "seqcounter")
    ].copy()

    if not best_sat.empty:
        best_sat["Solver_Label"] = "SAT_SeqCounter"

    others = df_opt[
        df_opt["Paradigm"].isin(
            ["CP-SAT", "CPLEX_CP", "MIP"]
        )
    ].copy()

    if not others.empty:
        others["Solver_Label"] = others["Solver_Name"]

    cross_df = pd.concat(
        [best_sat, others],
        ignore_index=True,
    )

    # Create stable fallback colors for additional solver names
    solver_palette = dict(SOLVER_PALETTE)

    if not cross_df.empty:
        solver_names = sorted(
            cross_df["Solver_Label"].dropna().unique()
        )

        used_colors = set(solver_palette.values())

        available_colors = [
            color
            for color in PALETTE
            if color not in used_colors
        ]

        for solver in solver_names:
            if solver not in solver_palette:
                if available_colors:
                    solver_palette[solver] = available_colors.pop(0)
                else:
                    # Deterministic fallback for additional solvers
                    solver_palette[solver] = PALETTE[
                        len(solver_palette) % len(PALETTE)
                    ]

    if not cross_df.empty:
        plot_line_comparison(
            data=cross_df,
            x="N",
            y="Solving_Time",
            hue="Solver_Label",
            palette=solver_palette,
            title="Cross-Paradigm: Solving Time vs. Board Size",
            xlabel="Board Size (N x N)",
            ylabel="Solving Time (seconds, log scale)",
            output_path=os.path.join(
                results_dir,
                "cross_paradigm_time_comparison.png",
            ),
            legend_title="Solver Configuration",
            log_y=True,
            legend_outside=True,
        )

    # -----------------------------------------------------
    # CHART 4: PEAK MEMORY USAGE
    # -----------------------------------------------------

    if not cross_df.empty and "Peak_Memory_Bytes" in cross_df.columns:
        memory_df = cross_df.dropna(
            subset=["Peak_Memory_Bytes"]
        ).copy()

        memory_df["Peak_Memory_MB"] = (
            memory_df["Peak_Memory_Bytes"] / (1024 * 1024)
        )

        if not memory_df.empty:
            plot_line_comparison(
                data=memory_df,
                x="N",
                y="Peak_Memory_MB",
                hue="Solver_Label",
                palette=solver_palette,
                title="Peak Memory Consumption vs. Board Size",
                xlabel="Board Size (N x N)",
                ylabel="Peak Traced Memory (MB)",
                output_path=os.path.join(
                    results_dir,
                    "peak_memory_comparison.png",
                ),
                legend_title="Solver Configuration",
                log_y=False,
                legend_outside=True,
            )

    print("=" * 60)
    print(" PLOTTING COMPLETED!")
    print(f" Output directory: {os.path.abspath(results_dir)}")
    print("=" * 60)


if __name__ == "__main__":
    generate_plots()
