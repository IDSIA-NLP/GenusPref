from utils.mappings import get_input_genus, get_output_genus

def convert_to_genus_level(result_language, nb_corr_answ_lg, maps_iso2wals, maps_wals2genus):
    """Convert language-level results to genus-level results."""
    result_output_genus = {}
    nb_questions_input_genus = {}

    # First pass: convert to output genus
    for lg_input in result_language:
        result_output_genus[lg_input] = {}
        nb_questions_input_genus[lg_input] = {}

        for lg_output in result_language[lg_input]:
            output_genus = get_output_genus(lg_output, maps_iso2wals, maps_wals2genus)

            if output_genus not in result_output_genus[lg_input]:
                result_output_genus[lg_input][output_genus] = 0
                nb_questions_input_genus[lg_input][output_genus] = 0

            result_output_genus[lg_input][output_genus] += result_language[lg_input][lg_output]
            nb_questions_input_genus[lg_input][output_genus] += nb_corr_answ_lg[lg_input]

    # Second pass: aggregate by input genus
    result_genus = {}
    nb_questions_genus = {}

    for lg_input in result_output_genus:
        input_genus = get_input_genus(lg_input, maps_iso2wals, maps_wals2genus)

        if input_genus not in result_genus:
            result_genus[input_genus] = result_output_genus[lg_input]
            nb_questions_genus[input_genus] = nb_questions_input_genus[lg_input]
        else:
            for output_genus in result_output_genus[lg_input]:
                if output_genus in result_genus[input_genus]:
                    result_genus[input_genus][output_genus] += result_output_genus[lg_input][output_genus]
                else:
                    result_genus[input_genus][output_genus] = result_output_genus[lg_input][output_genus]

            for output_genus in nb_questions_input_genus[lg_input]:
                if output_genus in nb_questions_genus[input_genus]:
                    nb_questions_genus[input_genus][output_genus] += nb_questions_input_genus[lg_input][output_genus]
                else:
                    nb_questions_genus[input_genus][output_genus] = nb_questions_input_genus[lg_input][output_genus]

    return result_genus, nb_questions_genus
