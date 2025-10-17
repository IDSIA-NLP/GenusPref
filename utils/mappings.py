from random import shuffle


def map_iso_to_genus(iso_codes: list[str], maps_iso2wals : dict[str, str], maps_wals2genus : dict[str, str], COLOR_LIST, GENUS_COLORS : dict[str, tuple]) -> dict[str, str]:
    """
    Map ISO-639-3 language codes to their linguistic genus using WALS mappings.

    Args:
        iso_codes (list[str]): List of ISO language codes.

    Returns:
        dict[str, str]: Dictionary mapping ISO → genus.
    """
    iso_to_genus = {}
    for iso in iso_codes:
        if iso in maps_iso2wals:
            wals_code = maps_iso2wals[iso]
            if isinstance(wals_code, str):
                genus = maps_wals2genus.get(wals_code)
                if genus:
                    iso_to_genus[iso] = genus

    assign_genus_colors(iso_to_genus, COLOR_LIST, GENUS_COLORS)
    return iso_to_genus


def assign_genus_colors(genus_dict: dict[str, str], COLOR_LIST, GENUS_COLORS) -> None:
    """
    Assign a unique color to each genus for consistent plotting.

    Args:
        genus_dict (dict[str, str]): Mapping of ISO → genus.
    """
    all_genera = sorted(set(genus_dict.values()))
    shuffle(COLOR_LIST)
    for i, genus in enumerate(all_genera):
        GENUS_COLORS[genus] = COLOR_LIST[i % len(COLOR_LIST)]
