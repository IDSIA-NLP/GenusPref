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


