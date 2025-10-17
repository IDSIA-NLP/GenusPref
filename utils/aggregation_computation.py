
import pandas as pd

def compute_fidelity_distribution(df: pd.DataFrame, iso_to_genus: dict[str, str]) -> dict[str, dict[str, float]]:
    """
    Compute fidelity distribution for each genus.

    Args:
        df (pd.DataFrame): Fidelity data containing columns like 'iso_639_3' and 'answer_genus'.
        iso_to_genus (dict[str, str]): Mapping from ISO → genus.

    Returns:
        dict[str, dict[str, float]]: Nested dict {input_genus: {output_genus: proportion}}.
    """
    genus_distributions = {}

    for iso_input in df["iso_639_3"].unique():
        if iso_input not in iso_to_genus:
            continue

        input_genus = iso_to_genus[iso_input]
        subset = df[df["iso_639_3"] == iso_input]
        output_genus_counts = subset["answer_genus"].value_counts(normalize=True)
        genus_distributions[input_genus] = output_genus_counts.to_dict()

    return genus_distributions


