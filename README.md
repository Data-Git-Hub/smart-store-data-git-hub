# smart-store-data-git-hub
P1. BI Python - Initial Step Up

''' shell
python scripts/bi_analysis.py

# Project File Organization

```plaintext
smart-store-data-git-hub
|
|- data/
|   | - raw
        |- customers_data.csv
        |- products_data.csv
        |- sales_data.csv
    | - processed
        |- P1_B1_Python,txt  
|- logs/
|   |- project_log.log
|- scripts/
    |- bi_analysis.py
    |- data_prep.py
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

### Optional: Verify .venv Setup

```shell
py -m datafun_venv_checker.venv_checker
```

### Run the initial project script

```shell
py scripts/data_prep.py
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
