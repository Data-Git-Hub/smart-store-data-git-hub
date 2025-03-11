# smart-store-data-git-hub

## Project File Organization

```plaintext
smart-store-data-git-hub
|
|- data/
|   | - raw
        |- customers_data.csv
        |- products_data.csv
        |- sales_data.csv
    | - processed
        |- P1_B1_Python.txt  
|- logs/
|   |- project_log.log
|- scripts/
    |- bi_analysis.py
    |- data_prep_m2.py
    |- data_prep_m3.py
    |- data_scrubber.py
|- utils/
|   |- utils_logger.py
|- .gitignore
|- README.md
|- requirements.txt
```
### Create a Local Project Virtual Environment

```shell
py -m venv .venv
```

### Activate the Virtual Environment

```shell
.venv\Scripts\activate
```

### Install Packages

```shell
py -m pip install --upgrade -r requirements.txt
```
-----

## Initial Package List

- pip
- loguru
- ipykernel
- jupyterlab
- numpy
- pandas
- matplotlib
- seaborn
- plotly
- pyspark==4.0.0.dev1
- pyspark[sql]

---
## P1. BI Python - Project Script

```shell
python scripts/bi_analysis.py
```

## P2. BI Python w/External Packages

```shell
py scripts/data_prep_m2.py
```

