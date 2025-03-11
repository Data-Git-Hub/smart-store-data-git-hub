# smart-store-data-git-hub

## Project File Organization

```plaintext
smart-store-data-git-hub
|
|- data/
|   |- prepared
|       |- customers_data_prepared.csv
|       |- products_data_prepared.csv
|       |- sales_data_prepared.csv
|   | - processed
|       |- P1_B1_Python.txt  
|   | - raw
|       |- customers_data.csv
|       |- products_data.csv
|       |- sales_data.csv
|- logs/
|   |- project_log.log
|- scripts/
|   |- bi_analysis.py
|   |- data_prep_m2.py
|   |- data_prep_m3.py
|   |- data_scrubber.py
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

### On Windows:
```shell
py scripts/bi_analysis.py
```

### On macOS/Linux:
```shell
python3 scripts/bi_analysis.py
```

## P2. BI Python w/External Packages

### On Windows:
```shell
py scripts/data_prep_m2.py
```

### On macOs/Linux:
```shell
python2 scripts/data_prep_m2.py
```

## D3.1 Data Collection

### On Windows:
```shell
py scripts/data_prep_m3.py
```

### On macOS/Linux:
```shell
python3 scripts/data_prep_m3.py
```
