"""
Are the LLMs Capable of Maintaining at Least the Language Genus?

This script computes and visualizes whether correct answers in one
language genus predict correct answers in another genus. It loads
language-level answers, maps ISO-639-3 codes to linguistic genera,
aggregates model correctness and produces heat-map of correctness by
model and by genus.

Usage:
    python switch.py

Output:
    Generates PNG files with heat-map of genus switch for each model.


Author: [David Kletz]
Affiliation: [IDSIA - Dalle Molle Institute for Artificial Intelligence]
Date: [2025-08-12]
"""



from utils.compare_with_language import get_language_comparisons
from utils.data_loading import load_data
from utils.read_answer import parse_answers
from utils.aggregation_computation import merge_dataframes
from utils.filtering import filter_languages_by_threshold
from utils.visualization import create_heatmap
from utils.language_to_genus import convert_to_genus_level
from utils.normalization import normalize_results
from configs import maps_wals2genus, maps_iso2wals, list_models, THRESHOLD



def process_model(model_name, maps_wals2genus, maps_iso2wals, threshold):
    """Process a single model: load data, analyze, and generate heatmap."""
    print(f"Processing model: {model_name}")

    # Load and merge data
    df_switch, df_fidelity = load_data(model_name)
    df_eval = merge_dataframes(df_switch, df_fidelity)

    # Parse answers
    results, nb_corr_answ_lg = parse_answers(df_eval)

    # Filter languages by threshold
    list_lg_ab_thresh = filter_languages_by_threshold(nb_corr_answ_lg, threshold)

    # Get language-level comparisons
    result_language, _ = get_language_comparisons(list_lg_ab_thresh, results)

    # Convert to genus level
    result_genus, nb_questions_genus = convert_to_genus_level(
        result_language, nb_corr_answ_lg, maps_iso2wals, maps_wals2genus
    )

    # Normalize results
    result_genus = normalize_results(result_genus, nb_questions_genus)

    # Create and save heatmap
    create_heatmap(result_genus, model_name, threshold)

    print(f"Completed: {model_name}\n")


def main():
    """Main entry point."""

    for model_name in list_models:
        process_model(model_name, maps_wals2genus, maps_iso2wals, THRESHOLD)


if __name__ == "__main__":
    main()
