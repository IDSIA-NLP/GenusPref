import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import seaborn as sns
import os

# Global color mapping for consistent genus colors across plots
GENUS_COLOR_MAP: dict[str, tuple] = {}


# Configure color palette for genus visualization
COLORMAP = cm.get_cmap("Set3")
COLORS_LIST = [COLORMAP(i) for i in range(COLORMAP.N)]



def assign_genus_color(genus: str) -> tuple:
    """
    Assign a consistent color to a genus for visualization.

    Uses global GENUS_COLOR_MAP to ensure consistency across plots.

    Args:
        genus: Name of the linguistic genus

    Returns:
        RGB color tuple
    """
    if genus not in GENUS_COLOR_MAP:
        GENUS_COLOR_MAP[genus] = COLORS_LIST[len(GENUS_COLOR_MAP)]
    return GENUS_COLOR_MAP[genus]


def create_fidelity_plot(
        proportions: dict[str, dict[str, float]],
        genera: list[str],
        model_name: str,
        output_filename: str
) -> None:
    """
    Create and save a stacked bar chart of language fidelity by genus.

    Args:
        proportions: Distribution of output genera for each input genus
        genera: Ordered list of genera for x-axis
        model_name: Display name of the model
        output_filename: Path for saving the figure
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Track all genera that appear in the plot for legend
    all_genera_present = set()

    # Create stacked bars for each input genus
    for i, genus_input in enumerate(genera):
        distribution = proportions[genus_input]

        labels = []
        sizes = []
        colors = []

        for genus_output, proportion in distribution.items():
            all_genera_present.add(genus_output)
            labels.append(genus_output)
            sizes.append(proportion)
            colors.append(assign_genus_color(genus_output))

        # Create stacked bar with cumulative bottoms
        bottoms = np.cumsum([0] + sizes[:-1])
        ax.bar(
            [i],
            sizes,
            color=colors,
            edgecolor="white",
            width=0.5,
            bottom=bottoms,
        )

    # Configure axes and labels
    ax.set_ylabel("Proportion of answers", fontsize=11)
    ax.set_xlabel("Input Language Genus", fontsize=11)
    ax.set_xticks(range(len(genera)))
    ax.set_xticklabels(genera, rotation=45, ha="right")
    ax.set_ylim(0, 1)

    # Add grid for readability
    ax.grid(True, color="lightgray", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.set_facecolor("white")

    # Create legend for all genera in plot
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=GENUS_COLOR_MAP[genus])
        for genus in sorted(all_genera_present)
    ]
    ax.legend(
        legend_handles,
        sorted(all_genera_present),
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
        fontsize=9
    )

    # Add title
    ax.set_title(
        f"Language Fidelity Distribution: {model_name}",
        fontsize=12,
        pad=15
    )

    # Save figure
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved plot: {output_filename}")





def create_heatmap(result_genus, model_name, threshold):
    """Create and save a heatmap visualization."""
    df = pd.DataFrame(result_genus).T

    fig, ax = plt.subplots(figsize=(20, 15))
    sns.heatmap(
        df, annot=False, cmap="coolwarm", cbar=True, square=True, vmin=0, vmax=1, ax=ax
    )

    ax.set_xlabel("Target Genus", fontsize=25)
    ax.set_ylabel("Source Genus", fontsize=25)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=25)
    ax.set_yticklabels(
        ax.get_yticklabels(),
        rotation=-45,
        ha="right",
        va="center",
        fontsize=25,
        rotation_mode="anchor",
    )

    plt.subplots_adjust(left=0.30)
    plt.tight_layout()

    output_dir = f"results/{model_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(f"{output_dir}/genus_th_{threshold}.png", dpi=300, bbox_inches="tight")
    plt.close()
