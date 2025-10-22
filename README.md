# Language Fidelity Distribution Analysis by Genus


This repository contains supplementary code for analyzing language fidelity patterns in multilingual language models, as presented in our LREC paper.
Overview

This script analyzes how well language models maintain language consistency when processing multilingual inputs. Languages are grouped by their linguistic genus according to the World Atlas of Language Structures (WALS) classification, allowing us to identify cross-linguistic patterns in model behavior.

The analysis produces stacked bar charts showing, for each input language genus, the distribution of detected output language genera across the model's responses


## Citation
If you use this code, please cite our paper:

```bibtex
[To ADD]
```

### Dependencies

```bash
pip install pandas numpy matplotlib
```

**Required packages:**
- `pandas` (≥1.3.0) - Data manipulation and analysis
- `numpy` (≥1.20.0) - Numerical computing
- `matplotlib` (≥3.4.0) - Visualization

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



### Input Data



Each CSV file should contain at least the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `iso_639_3` | str | ISO 639-3 code of the input language |
| `detected_language` | str | ISO 639-3 code of the detected/output language |


## Usage

### Basic Usage

Run the script from the command line:

```bash
python language_fidelity_analysis.py
```


### Output

The script generates plots :

```
fidelity_distribution_by_genus_{MODEL_NAME}.png
```

Each plot shows:
- **X-axis:** Input language genera (from `configs.GENERA`)
- **Y-axis:** Proportion of model responses (0-1)
- **Stacked bars:** Distribution of detected output language genera
- **Legend:** All genera that appear in the data

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
