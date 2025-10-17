import pandas as pd


def load_multiq_data(path : str) -> tuple[pd.DataFrame, list[str]]:
    """
    Load fidelity data for MultiQ for a given multilingual model.

    Args:
        model_name (str): Name of the model (must match CSV filename).

    Returns:
        tuple:
            - DataFrame containing fidelity information.
            - List of ISO-639-3 codes for all unique languages.
    """

    df = pd.read_csv(path)
    language_iso_codes = df["iso_639_3"].unique().tolist()
    return df, language_iso_codes
