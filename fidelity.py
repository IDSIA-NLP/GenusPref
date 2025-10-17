"""
Supplementary code for LREC paper:
    Are the LLMs Capable of Maintaining at Least the Language Genus?

This script computes and visualizes the fidelity of multilingual models
with respect to linguistic genus. It loads language-level fidelity data,
maps ISO-639-3 codes to linguistic genera, aggregates model predictions,
and produces genus-level stacked bar charts.

Author: [David Kletz]
Affiliation: [IDSIA - Dalle Molle Institute for Artificial Intelligence]
Date: [2025-08-24]
"""

import matplotlib.cm as cm

from random import seed
from utils.other_data import supp_dic_iso_to_genus
from configs import list_models, maps_wals2genus, maps_iso2wals
from utils.data_loading import load_multiq_data
from utils.mappings import map_iso_to_genus
from utils.aggregation_computation import compute_fidelity_distribution
from utils.visualization import plot_genus_fidelity_distribution



# Plot settings
seed(1)
cmap = cm.get_cmap("Set3")
COLOR_LIST = [cmap(i) for i in range(cmap.N)]
GENUS_COLORS: dict[str, tuple] = {}  # Maps genus → color



def main() -> None:
    """Main entry point for fidelity analysis and visualization."""
    for model in list_models:
        print(f"Processing model: {model}")
        path: str = f"../multiQ/data/language_fidelity/{model}.csv"
        df, iso_codes = load_multiq_data(path)
        iso_to_genus = map_iso_to_genus(iso_codes, maps_iso2wals, maps_wals2genus, COLOR_LIST, GENUS_COLORS)
        distributions = compute_fidelity_distribution(df, iso_to_genus)
        plot_genus_fidelity_distribution(distributions, model, GENUS_COLORS)

        print(f"✓ Saved figure for {model}\n")


if __name__ == "__main__":
    main()
