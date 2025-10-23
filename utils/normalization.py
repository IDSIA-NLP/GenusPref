
def normalize_results(result_genus, nb_questions_genus):
    """Normalize results by dividing by the number of questions."""
    for input_genus in result_genus:
        for output_genus in result_genus[input_genus]:
            if nb_questions_genus[input_genus][output_genus] == 0:
                print(f"{input_genus}: {output_genus}")
            else:
                result_genus[input_genus][output_genus] /= nb_questions_genus[
                    input_genus
                ][output_genus]

    return result_genus