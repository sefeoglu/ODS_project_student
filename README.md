# Ontology Matching
A Ontology Matcher utilizing Graph Search Algorithms and Prompt Generation for LLMs.

Note: The repository consists of source codes of the paper "Exploring Prompt Generation utilizing Graph Search Algorithms for Ontology Matching" submitted to Special Track of ESWC 2024.

## Requirements
use Python version >=3.10
```xml
pip install -r requirements.txt
```
## Dataset Folder:
update dataset paths at ```src/config.json```
## Configuration:
adjust the pipeline tasks and algorithm configurations at ```src/configODS.json```

## How to run
```xml
git clone https://github.com/sefeoglu/ODS_project_student.git
```

download this [file](https://emckclac-my.sharepoint.com/:u:/g/personal/k20036346_kcl_ac_uk/EbL1yTauXtpEqs4Izc97WNIBhumczrDGTNQb47uYGzXqsg?e=I9B5pR) and extract it to `src/verbalizer/graph2text/outputs/t5-base_13881/`
```python
cd src
python3 ProjectODS.py

```
