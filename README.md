# Ontology Matching

Graph Search Algorithm Based Prompt Generation for Ontology Matching.

Note: The repository consists of source codes of the paper "Exploring  Prompt Generation utilizing Graph Search Algorithms for Ontology Matching" submitted to Semantics 2024.
## Folder Hierarchy 
```bash
├── data
├── results
└── src
    ├── AlignmentFormat.py
    ├── accronyms.json
    ├── batch_loaders
    │   ├── alignment.py
    │   ├── ontology_parsing
    │   └── random_walk.py
    ├── config.json
    ├── configMatcher.json
    ├── configMatcherImport.py
    ├── globals.py
    ├── llms
    ├── maximum_bipartite_matching
    ├── prompt_template_generator
    ├── run_matcher.py
    ├── track.py
    ├── utilsODS.py
    └── verbalizer

```


## Requirements
use Python version >=3.10
```bash
$ pip install -r requirements.txt
```
## Dataset Folder:
update dataset paths at ```src/config.json```
## Configuration:
adjust the pipeline tasks and algorithm configurations at ```src/configMatcher.json```

## How to run
```bash
$ git clone https://github.com/JulianSampels/OntoMatch.git
```

download this [file](https://emckclac-my.sharepoint.com/:u:/g/personal/k20036346_kcl_ac_uk/EbL1yTauXtpEqs4Izc97WNIBhumczrDGTNQb47uYGzXqsg?e=I9B5pR) and extract it to `src/verbalizer/graph2text/outputs/t5-base_13881/`
```python
$ cd src
$ python3 run_matcher.py

```
