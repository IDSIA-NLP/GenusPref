import pandas as pd
from utils.other_data import supp_dic_iso_to_genus


def count_genus_occurrences(
    df: pd.DataFrame, input_languages: list[str], input_genus_map: dict[str, str], output_genus_map: dict[str, str]
) -> tuple[dict[str, int], dict[str, dict[str, int]]]:
    """
    Count occurrences of input and output genera.

    Args:
        df: DataFrame with columns 'iso_639_3' and 'detected_language'
        input_languages: List of input language ISO codes
        input_genus_map: Mapping from input ISO codes to genera

    Returns:
        Tuple containing:
            - Dictionary: input genus -> total occurrence count
            - Nested dictionary: input genus -> output genus -> count
    """
    input_genus_counts = {}
    output_genus_by_input = {}

    for iso_input in input_languages:
        genus_input = input_genus_map[iso_input]

        # Filter data for this input language
        df_input = df[df["iso_639_3"] == iso_input]

        # Count total occurrences for this input genus
        input_genus_counts[genus_input] = input_genus_counts.get(genus_input, 0) + len(
            df_input
        )

        # Initialize nested dictionary for output genera
        if genus_input not in output_genus_by_input:
            output_genus_by_input[genus_input] = {}

        # Count output genera for each detected language
        for iso_output in df_input["detected_language"]:
            genus_output = output_genus_map[iso_output]
            output_genus_by_input[genus_input][genus_output] = (
                output_genus_by_input[genus_input].get(genus_output, 0) + 1
            )

    return input_genus_counts, output_genus_by_input



def compute_genus_proportions(
    input_counts: dict[str, int],
    output_by_input: dict[str, dict[str, int]],
    threshold: float,
) -> dict[str, dict[str, float]]:
    """
    Calculate proportions of output genera for each input genus.

    Rare genera (below threshold) are grouped into "Other" category.

    Args:
        input_counts: Total counts per input genus
        output_by_input: Output genus counts per input genus
        threshold: Minimum proportion to be shown separately (default: 0.05)

    Returns:
        Nested dictionary: input genus -> output genus -> proportion
    """
    proportions = {}

    for genus_input, output_counts in output_by_input.items():
        total = input_counts[genus_input]

        # Calculate proportions
        genus_proportions = {
            genus_output: count / total for genus_output, count in output_counts.items()
        }

        # Group rare genera into "Other"
        other_sum = 0
        filtered_proportions = {}

        for genus_output, proportion in genus_proportions.items():
            if proportion < threshold:
                other_sum += proportion
            else:
                filtered_proportions[genus_output] = proportion

        # Add "Other" category if there are rare genera
        if other_sum > 0:
            filtered_proportions["Other"] = other_sum

        proportions[genus_input] = filtered_proportions

    return proportions


def extract_self_fidelity(
    proportions: dict[str, dict[str, float]], genera: list[str]
) -> dict[str, list[float]]:
    """
    Extract self-fidelity scores (same-genus accuracy) for each genus.

    Args:
        proportions: Genus proportion distributions
        genera: List of genera to analyze

    Returns:
        Dictionary mapping genus to list containing self-fidelity score
    """
    self_fidelity = {genus: [] for genus in genera}

    for genus_source in genera:
        distribution = proportions[genus_source]
        # Self-fidelity: proportion where output genus = input genus
        fidelity_score = distribution.get(genus_source, 0.0)
        self_fidelity[genus_source].append(fidelity_score)

    return self_fidelity





def merge_dataframes(df_switch, df_fidelity):
    """Merge switch and fidelity dataframes on id_lg."""
    df_fidelity["id_lg"] = df_fidelity["id"].astype(str).str.cat(
        df_fidelity["language"].astype(str), sep=";"
    )
    df_switch["id_lg"] = df_switch["id"].astype(str).str.cat(
        df_switch["language"].astype(str), sep=";"
    )

    df_eval = df_fidelity.merge(
        df_switch[["id_lg", "eval_completion", "prompt", "prompt_en"]],
        on="id_lg",
        how="left"
    )

    return df_eval
