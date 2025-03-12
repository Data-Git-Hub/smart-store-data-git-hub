"""
Script: schema_fact_table.py
Description: Generates a schema for the fact table from the sales_data_prepared.csv file.
Output: data/processed/schema_fact_tables.txt
"""

import pandas as pd
import pathlib
import sys

# Add project root to sys.path for logger import
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import logger
from utils.utils_logger import logger  

# File paths
DATA_DIR = PROJECT_ROOT / "data" / "prepared"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "schema_fact_tables.txt"

# Ensure processed folder exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load sales data
sales_file = DATA_DIR / "sales_data_prepared.csv"
try:
    df_sales = pd.read_csv(sales_file)
    logger.info(f"Loaded sales data from {sales_file}")
except Exception as e:
    logger.error(f"Error loading sales data: {e}")
    sys.exit(1)

# Generate schema
schema_lines = ["Schema for Fact Table: sales\n", "=" * 40 + "\n"]
for column in df_sales.columns:
    dtype = str(df_sales[column].dtype)
    schema_lines.append(f"{column}: {dtype}\n")

# Write schema to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(schema_lines)

logger.info(f"Schema for fact table saved to {OUTPUT_FILE}")

print(f"Schema for fact table written to: {OUTPUT_FILE}")
