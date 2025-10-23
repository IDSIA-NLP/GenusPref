def compare_with_language(source_lg: str, answers: dict[str, dict[str, bool]], languages :  list[str] ) -> (dict[str, int], dict[str, float]):
    """
    Compare the results with the languages and return a dictionary with the counts of each language.
    """
    pool_questions = [question for question in answers if answers[question][source_lg]]
    result_language = {}
    result_language_prop = {}

    for target_lg in languages:
        count = sum(
            1 for question in pool_questions if answers[question][target_lg]
        )

        result_language[target_lg] = count
        result_language_prop[target_lg] = (
            count / len(pool_questions) if pool_questions else 0
        )

    return result_language, result_language_prop





def get_language_comparisons(list_lg_ab_thresh, results):
    """Compare results across languages."""
    result_language = {}
    result_language_prop = {}

    for language in list_lg_ab_thresh:
        r_lg, r_lg_prop = compare_with_language(language, results, list_lg_ab_thresh)
        result_language[language] = r_lg
        result_language_prop[language] = r_lg_prop

    return result_language, result_language_prop