from configs import maps_wals2genus, maps_iso2wals
import pandas as pd
from utils.other_data import supp_dic_iso_to_genus


def map_iso_to_genus(iso_code: str) -> str:
    """
    Map an ISO 639-3 language code to its linguistic genus.

    Args:
        iso_code: ISO 639-3 language code
        use_wals: Whether to use WALS classification (default: True)

    Returns:
        Genus name according to WALS classification
    """
    if iso_code in maps_iso2wals:
        wals_code = maps_iso2wals[iso_code]
        # Handle both single codes and lists of codes
        if isinstance(wals_code, str):
            return maps_wals2genus[wals_code]
        else:
            return maps_wals2genus[wals_code[0]]
    else:
        return supp_dic_iso_to_genus[iso_code]


def build_genus_mapping(iso_codes: list[str]) -> dict[str, str]:
    """
    Build a mapping dictionary from ISO codes to genera for a list of languages.

    Args:
        iso_codes: List of ISO 639-3 language codes

    Returns:
        Dictionary mapping ISO codes to genus names
    """
    return {iso_code: map_iso_to_genus(iso_code) for iso_code in iso_codes}


def build_output_genus_mapping(df: pd.DataFrame) -> dict[str, str]:
    """
    Build genus mapping for detected output languages in the dataset.

    Excludes certain problematic language codes (e.g., 'rop', 'nzi').

    Args:
        df: DataFrame containing 'detected_language' column

    Returns:
        Dictionary mapping output ISO codes to genus names
    """
    output_languages = list(df["detected_language"].unique())
    genus_map = {}

    for iso_code in output_languages:
        genus_map[iso_code] = map_iso_to_genus(iso_code)

    return genus_map
