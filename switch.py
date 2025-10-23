import pandas as pd
from joblib import load, dump

from utils.read_answer import read_answer
from utils.compare_with_language import compare_with_language
import matplotlib.pyplot as plt


import seaborn as sns


from utils.other_data import supp_dic_iso_to_genus

import os



threshold = 20


# # Load maps


maps_wals2genus: dict[str, str] = load("data/maps/mapping_wals_genus.joblib")
maps_iso2wals: dict[str, str] = load("data/maps/iso_to_wals.joblib")

path_fidelity: str = f"data/multiQ/language_fidelity/Llama-2-13b-chat-hf.csv"

list_models = [
    "Llama-2-70b-chat-hf",
    "Llama-2-13b-chat-hf",
    "Llama-2-7b-chat-hf",
    "Mixtral-8x7B-Instruct-v0.1",
    "Mistral-7B-Instruct-v0.1",
    "Qwen1.5-7B-Chat",
    "Apertus-8B",
]


for name_model in list_models:
    path_switch: str = f"data/multiQ/{name_model}.csv"
    df_switch: pd.DataFrame = pd.read_csv(path_switch)
    #TODO : gpt4_eval
    df_fidelity: pd.DataFrame = pd.read_csv(path_fidelity)
    df_fidelity["id_lg"] = df_fidelity["id"].astype(str).str.cat(df_fidelity["language"].astype(str), sep=";")

    df_switch["id_lg"] = df_switch["id"].astype(str).str.cat(df_switch["language"].astype(str), sep=";")

    df_eval = df_fidelity.merge(
        df_switch[["id_lg", "eval_completion", "prompt", "prompt_en"]],  # keep only needed columns from df2
        on="id_lg",
        how="left"  # keeps all rows from df1
    )
    prompt_en: list[str] = df_eval["prompt_en"].unique().tolist()  # all questions (in en version)
    languages: list[str] = df_eval["iso_639_3"].unique().tolist()

    results = {k: {} for k in prompt_en}

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

    nb_corr_answ_lg = {lg: 0 for lg in languages}
    for question in results:
        for lg_q in results[question]:
            if results[question][lg_q]:
                nb_corr_answ_lg[lg_q] += 1

    list_lg_ab_thresh = [lg for lg in nb_corr_answ_lg if nb_corr_answ_lg[lg] >= threshold]

    # get total nb questions
    tot_nb_questions = 0
    for lg in list_lg_ab_thresh:
        tot_nb_questions += nb_corr_answ_lg[lg]
    print(tot_nb_questions)

    result_language = {}
    result_language_prop = {}
    for language in list_lg_ab_thresh:
        r_lg, r_lg_prop = compare_with_language(language, results, list_lg_ab_thresh)
        result_language[language] = r_lg
        result_language_prop[language] = r_lg_prop

    # # Convert to genus

    result_output_genus = {}
    nb_questions_input_genus = {}
    for lg_input in result_language:
        result_output_genus[lg_input] = {}
        nb_questions_input_genus[lg_input] = {}
        for lg_output in result_language[lg_input]:
            if lg_output in maps_iso2wals:
                wals_lg_output = maps_iso2wals[lg_output]
                if type(wals_lg_output) == str:
                    output_genus = maps_wals2genus[wals_lg_output]

                elif maps_wals2genus[wals_lg_output[0]] == maps_wals2genus[wals_lg_output[1]]:
                    output_genus = maps_wals2genus[wals_lg_output[0]]
            else:
                output_genus = supp_dic_iso_to_genus[lg_output]

            if output_genus not in result_output_genus[lg_input]:
                result_output_genus[lg_input][output_genus] = 0
                nb_questions_input_genus[lg_input][output_genus] = 0

            result_output_genus[lg_input][output_genus] += result_language[lg_input][lg_output]
            nb_questions_input_genus[lg_input][output_genus] += nb_corr_answ_lg[lg_input]

    result_genus = {}
    nb_questions_genus = {}
    for lg_input in result_output_genus:
        if lg_input in maps_iso2wals:
            wals_lg_input = maps_iso2wals[lg_input]
            if type(wals_lg_input) == str:
                if wals_lg_input in maps_wals2genus:
                    input_genus = maps_wals2genus[wals_lg_input]

            elif maps_wals2genus[wals_lg_input[0]] == maps_wals2genus[wals_lg_input[1]]:
                    input_genus = maps_wals2genus[wals_lg_input[0]]


        else:

            input_genus = supp_dic_iso_to_genus[lg_input]

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
                #print(output_genus, input_genus)
                if output_genus in nb_questions_genus[input_genus]:
                    nb_questions_genus[input_genus][output_genus] += nb_questions_input_genus[lg_input][output_genus]
                else:
                    nb_questions_genus[input_genus][output_genus] = nb_questions_input_genus[lg_input][output_genus]


    #dividing by number of questions
    for input_genus in result_genus:
        for output_genus in result_genus[input_genus]:
            if nb_questions_genus[input_genus][output_genus] == 0:
                print(f"{input_genus}: {output_genus}")
            result_genus[input_genus][output_genus] /= nb_questions_genus[input_genus][output_genus]

    # Convert the nested dictionary to a DataFrame
    df = pd.DataFrame(result_genus).T  # Transpose so rows and columns align correctly

    fig, ax = plt.subplots(figsize=(20, 15))
    sns.heatmap(df, annot=False, cmap="coolwarm", cbar=True, square=True, vmin=0, vmax=1, ax=ax)

    # title/labels
    # ax.set_title(f"Threshold: {threshold} avail. questions", fontsize=24, fontweight='bold', pad=20)
    ax.set_xlabel("Target Genus", fontsize=25)
    ax.set_ylabel("Source Genus", fontsize=25)

    # x ticks
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=25)

    # y ticks: rotate about the anchor and align so long labels don't slide down
    ax.set_yticklabels(ax.get_yticklabels(), rotation=-45,
                       ha="right", va="center", fontsize=25, rotation_mode='anchor')

    # give extra left margin so labels don't get clipped
    plt.subplots_adjust(left=0.30)

    # ensure layout and save
    plt.tight_layout()

    if not os.path.exists(f"results/{name_model}"):
        os.makedirs(f"results/{name_model}")

    plt.savefig(f"results/{name_model}/genus_th_{threshold}.png", dpi=300, bbox_inches='tight')






