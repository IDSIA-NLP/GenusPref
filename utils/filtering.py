
def filter_languages_by_threshold(nb_corr_answ_lg, threshold):
    """Filter languages that have at least threshold correct answers."""
    return [lg for lg in nb_corr_answ_lg if nb_corr_answ_lg[lg] >= threshold]
