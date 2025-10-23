"""
Are the LLMs Capable of Maintaining at Least the Language Genus?

This script computes and visualizes the fidelity of multilingual models
with respect to linguistic genus. It loads language-level fidelity data,
maps ISO-639-3 codes to linguistic genera, aggregates model predictions,
and produces genus-level stacked bar charts.

Usage:
    python fidelity.py

Output:
    Generates PNG files with fidelity distribution plots for each model.


Author: [David Kletz]
Affiliation: [IDSIA - Dalle Molle Institute for Artificial Intelligence]
Date: [2025-08-24]
"""


from random import seed

# Local imports

from utils.data_loading import load_multiq_data
from utils.mappings import build_genus_mapping, build_output_genus_mapping
from utils.aggregation_computation import count_genus_occurrences, compute_genus_proportions, extract_self_fidelity
from utils.visualization import create_fidelity_plot
from configs import list_models, name_models, GENERA





# =============================================================================
# CONFIGURATION
# =============================================================================

# Set random seed for reproducible color assignment
RANDOM_SEED = 1
seed(RANDOM_SEED)




# Threshold for grouping rare genera into "Other" category
OTHER_THRESHOLD = 0.05  # 5% of total occurrences



# =============================================================================
# MAIN ANALYSIS PIPELINE
# =============================================================================

def analyze_model_fidelity(model_id: str, model_display_name: str) -> None:
    """
    Run complete fidelity analysis for a single model.

    Args:
        model_id: Internal identifier for the model
        model_display_name: Display name for the model in plots
    """
    print(f"\nProcessing model: {model_display_name}")

    # Load data
    df, input_languages = load_multiq_data(model_id)
    print(f"  Loaded {len(df)} samples across {len(input_languages)} input languages")

    # Build language-to-genus mappings
    input_genus_map = build_genus_mapping(input_languages)
    output_genus_map = build_output_genus_mapping(df)

    # Count occurrences
    input_counts, output_by_input = count_genus_occurrences(
        df, input_languages, input_genus_map, output_genus_map
    )

    # Calculate proportions
    proportions = compute_genus_proportions(input_counts, output_by_input, OTHER_THRESHOLD)

    # Extract self-fidelity scores (optional: could be used for further analysis)
    self_fidelity = extract_self_fidelity(proportions, GENERA)

    # Generate visualization
    output_filename = f"fidelity_distribution_by_genus_{model_display_name}.png"
    create_fidelity_plot(proportions, GENERA, model_display_name, output_filename)


def main():
    """
    Main entry point: analyze all models and generate plots.
    """
    print("=" * 70)
    print("Language Fidelity Analysis by Genus")
    print("=" * 70)

    for model_id in list_models:
        model_display_name = name_models[model_id]
        analyze_model_fidelity(model_id, model_display_name)

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
