from joblib import load


GENERA = [
    "Slavic",
    "Germanic",
    "Romance",
    "Javanese",
    "Albanian",
    "Turkic",
    "Armenian",
    "Chinese",
]

THRESHOLD = 20

maps_wals2genus: dict[str, str] = load("data/maps/mapping_wals_genus.joblib")
maps_iso2wals: dict[str, str] = load("data/maps/iso_to_wals.joblib")


list_models = [
    "Llama-2-7b-chat-hf",
    "Llama-2-13b-chat-hf",
    "Llama-2-70b-chat-hf",
    "Mistral-7B-Instruct-v0.1",
    "Mixtral-8x7B-Instruct-v0.1",
    "Qwen1.5-7B-Chat",
    "Apertus-8B",
]


name_models = [
    "Llama-2-7b",
    "Llama-2-13b",
    "Llama-2-70b",
    "Mistral-7B-Instruct-v0.1",
    "Mixtral-8x7B",
    "Qwen1.5-7B",
    "Apertus-8B",
]

name_models = {list_models[i]: name_models[i] for i in range(len(list_models))}
