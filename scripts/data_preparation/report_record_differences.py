"""
Module: Report Record Differences
File: scripts/data_preparation/report_record_differences.py

This script reads the cleaned (prepared) and raw (dirty) CSV files for customers, products,
and sales. It calculates the record count for each pair and writes a report detailing:
- Raw records count
- Prepared records count
- Difference (i.e., number of records removed during cleaning)

The report is saved as "answers.txt" in the data/processed/ folder.
"""

import pathlib
import pandas as pd

# Define project root (adjust based on your folder structure)
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

# Define file paths for customers
DIRTY_CUSTOMERS = PROJECT_ROOT / "data" / "dirty_data" / "dirty_customers_data.csv"
PREPARED_CUSTOMERS = PROJECT_ROOT / "data" / "_prepared" / "customers_data_prepared.csv"

# Define file paths for products
DIRTY_PRODUCTS = PROJECT_ROOT / "data" / "dirty_data" / "dirty_products_data.csv"
PREPARED_PRODUCTS = PROJECT_ROOT / "data" / "_prepared" / "products_data_prepared.csv"

# Define file paths for sales
DIRTY_SALES = PROJECT_ROOT / "data" / "dirty_data" / "dirty_sales_data.csv"
PREPARED_SALES = PROJECT_ROOT / "data" / "_prepared" / "sales_data_prepared.csv"

# Load CSV files and count rows
df_dirty_customers = pd.read_csv(DIRTY_CUSTOMERS)
df_prepared_customers = pd.read_csv(PREPARED_CUSTOMERS)
dirty_customers_count = df_dirty_customers.shape[0]
prepared_customers_count = df_prepared_customers.shape[0]

df_dirty_products = pd.read_csv(DIRTY_PRODUCTS)
df_prepared_products = pd.read_csv(PREPARED_PRODUCTS)
dirty_products_count = df_dirty_products.shape[0]
prepared_products_count = df_prepared_products.shape[0]

df_dirty_sales = pd.read_csv(DIRTY_SALES)
df_prepared_sales = pd.read_csv(PREPARED_SALES)
dirty_sales_count = df_dirty_sales.shape[0]
prepared_sales_count = df_prepared_sales.shape[0]

# Compute differences (raw minus prepared)
diff_customers = dirty_customers_count - prepared_customers_count
diff_products = dirty_products_count - prepared_products_count
diff_sales = dirty_sales_count - prepared_sales_count

# Prepare output text
report_text = f"""Record Count Differences Report

Customers:
  Raw records count: {dirty_customers_count}
  Prepared records count: {prepared_customers_count}
  Difference: {diff_customers} records removed

Products:
  Raw records count: {dirty_products_count}
  Prepared records count: {prepared_products_count}
  Difference: {diff_products} records removed

Sales:
  Raw records count: {dirty_sales_count}
  Prepared records count: {prepared_sales_count}
  Difference: {diff_sales} records removed
"""

# Define output file path (answers.txt in the processed folder)
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "answers.txt"

# Write the report to the text file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(report_text)

print("Report written to:", OUTPUT_FILE)
