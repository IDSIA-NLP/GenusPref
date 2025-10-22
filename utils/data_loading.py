import pandas as pd


def load_multiq_data(model_name: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Load language fidelity data for a specific model.

    Args:
        model_name: Name/identifier of the language model

    Returns:
        Tuple containing:
            - DataFrame with multiQ language fidelity data
            - List of unique ISO 639-3 input language codes
    """
    data_path : str = f"data/multiQ/language_fidelity/{model_name}.csv"
    df : pd.DataFrame = pd.read_csv(data_path)
    input_languages : list[str] = list(df["iso_639_3"].unique())
    return df, input_languages
