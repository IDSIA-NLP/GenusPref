# Language Fidelity Distribution Analysis by Genus

[![License: CC-BY-SA 4.0](https://img.shields.io/badge/License-CC--BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Dataset Version](https://img.shields.io/badge/version-1.0-blue)]()
[![Paper](https://img.shields.io/badge/Paper-LREC%202025-green)](https://lrec2026.info/)

This repository contains supplementary code for analyzing language fidelity patterns in multilingual language models, as presented in our LREC paper.

## Overview

This project analyzes how well language models maintain language consistency when processing multilingual inputs. Languages are grouped by their linguistic genus according to the World Atlas of Language Structures (WALS) classification, allowing us to identify cross-linguistic patterns in model behavior.

The analysis consists of two main components:

1. **Language Fidelity Analysis** - Analyzes how well models detect and maintain language identity across multilingual inputs
2. **Cross-Linguistic Transfer Analysis** - Examines whether correct answers in one language genus predict correct answers in another genus (cross-linguistic transfer patterns)


## Citation
If you use this code, please cite our paper:

```bibtex
@misc{mitrović2025llmscapablemaintaininglanguage,
      title={Are the LLMs Capable of Maintaining at Least the Language Genus?}, 
      author={Sandra Mitrović and David Kletz and Ljiljana Dolamic and Fabio Rinaldi},
      year={2025},
      eprint={2510.21561},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2510.21561}, 
}
```

### Dependencies


**Required packages:**
- `pandas` (≥1.3.0) 
- `numpy` (≥1.20.0)
- `matplotlib` (≥3.4.0)
- `seaborn` (≥0.11.0)
- `joblib` (≥1.0.0)

## Data 

The script requires the following local modules (should be included in your repository):

```
data/
  └── multiq/                           # Contains language fidelity results
         ├── Llama-2-7b-chat-hf.csv     # Llama-2-7b language fidelity results
         ├── Llama-2-70b-chat-hf.csv    # Llama-2-70b language fidelity results
         ...
         └──Qwen1.5-7B-Chat.csv         # Qwen1.5-7B language fidelity results
```



## Usage

### Component 1: Cross-Linguistic Transfer Analysis

Run the script from the command line:

```bash
python fidelity.py
```


**Output:**

The script generates plots :

```
fidelity_distribution_by_genus_{MODEL_NAME}.png
```

**Parameters:**
```python
THRESHOLD = 20  # Minimum number of correct answers required per language
```


Each plot shows:
- **X-axis:** Input language genera (from `configs.GENERA`)
- **Y-axis:** Proportion of model responses (0-1)
- **Stacked bars:** Distribution of detected output language genera
- **Legend:** All genera that appear in the data

### Component 2: Language Fidelity Analysis (Original)


```bash
python switch.py
```


## Configuration

### Adjusting Parameters

You can modify the following parameters at the top of the script:

```python
# Set random seed for reproducible color assignment
RANDOM_SEED = 1

# Threshold for grouping rare genera into "Other" category
OTHER_THRESHOLD = 0.05  # 5% of total occurrences

# Color palette for visualization
COLORMAP = cm.get_cmap("Set3")
```

## License

This project is licensed under the MIT License


## Acknowledgments
### Data

This analysis uses data from the **MultiQ** benchmark:

> Holtermann, Carolin, Röttger, Paul, Dill, Timm, and Lauscher, Anne. 2024. 
> "Evaluating the Elementary Multilingual Capabilities of Large Language Models with MultiQ." 
> In *Findings of the Association for Computational Linguistics: ACL 2024*, 
> pages 4476–4494, Bangkok, Thailand. Association for Computational Linguistics.
> https://aclanthology.org/2024.findings-acl.265/

```bibtex
@inproceedings{holtermann-etal-2024-evaluating,
    title = "Evaluating the Elementary Multilingual Capabilities of Large Language Models with {M}ulti{Q}",
    author = {Holtermann, Carolin  and
              R{\"o}ttger, Paul  and
              Dill, Timm  and
              Lauscher, Anne},
    editor = "Ku, Lun-Wei  and
              Martins, Andre  and
              Srikumar, Vivek",
    booktitle = "Findings of the Association for Computational Linguistics: ACL 2024",
    month = aug,
    year = "2024",
    address = "Bangkok, Thailand",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-acl.265/",
    doi = "10.18653/v1/2024.findings-acl.265",
    pages = "4476--4494"
}
```

### Language Classification

This work uses the World Atlas of Language Structures (WALS) classification:

> Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013. 
> The World Atlas of Language Structures Online. 
> Leipzig: Max Planck Institute for Evolutionary Anthropology. 
> (Available online at http://wals.info)
