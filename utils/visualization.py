
import pandas as pd
from configs import name_models, GENERA
import matplotlib.pyplot as plt
import numpy as np


def plot_genus_fidelity_distribution(
    genus_distributions: dict[str, dict[str, float]],
    model_name: str,
    GENUS_COLORS : dict[str, tuple]
) -> None:
    """
    Plot stacked bar chart showing distribution of answers by genus.

    Args:
        genus_distributions (dict): {input_genus: {output_genus: proportion}}
        model_name (str): Identifier for the model (used in saved figure name).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    all_observed_genera = set()

    # Plot each genus as a stacked bar
    for idx, input_genus in enumerate(GENERA):
        output_distribution = genus_distributions.get(input_genus, {})
        output_genera = list(output_distribution.keys())
        proportions = list(output_distribution.values())
        colors = [GENUS_COLORS.get(gen, "gray") for gen in output_genera]

        # Track all represented genera
        all_observed_genera.update(output_genera)

        ax.bar(
            [idx],
            proportions,
            color=colors,
            edgecolor="white",
            width=0.5,
            bottom=np.cumsum([0] + proportions[:-1]),
        )

    # Axis formatting
    ax.set_ylabel("Proportion of answers")
    ax.set_xticks(range(len(GENERA)))
    ax.set_xticklabels(GENERA, rotation=45, ha="right")
    ax.set_ylim(0, 1)
    ax.grid(True, color="lightgray", linestyle="--", linewidth=0.5)
    ax.set_facecolor("white")

    # Legend
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=GENUS_COLORS[g])
        for g in all_observed_genera
    ]
    ax.legend(
        legend_handles,
        list(all_observed_genera),
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
    )

    # Save figure
    output_path = f"fidelity_distribution_by_genus_{name_models[model_name]}.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()