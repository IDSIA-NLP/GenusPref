def read_answer(answer: str) -> bool:
    lower_answer = answer.lower().strip()
    if lower_answer in ["no", "false", "n", "f", "no."]:
        return False
    elif lower_answer in ["yes", "true", "yes."]:
        return True

    else:
        if lower_answer.startswith("yes"):
            return True
        elif lower_answer.startswith("no"):
            return False
        else:
            raise ValueError(
                f"Unexpected answer format: {answer}. Expected 'yes' or 'no'."
            )



def parse_answers(df_eval):
    """Parse answers from evaluations and organize by question and language."""
    prompt_en = df_eval["prompt_en"].unique().tolist()
    languages = df_eval["iso_639_3"].unique().tolist()

    results = {k: {} for k in prompt_en}
    nb_corr_answ_lg = {lg: 0 for lg in languages}

    for i, row in df_eval.iterrows():
        current_en_prompt = row["prompt_en"]
        current_language = row["iso_639_3"]

        try:
            answer = read_answer(row["eval_completion"])
        except Exception as e:
            print(f"Error reading answer for row {i}: {e}")
            results[current_en_prompt][current_language] = None
            continue

        results[current_en_prompt][current_language] = answer
        if answer:
            nb_corr_answ_lg[current_language] += 1

    return results, nb_corr_answ_lg
