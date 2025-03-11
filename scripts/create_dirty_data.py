"""
Create Dirty Data Script
This script reads the original CSV files from 'data/raw/', injects errors (outliers,
missing values, and mis-entered data) into each dataset without modifying the original files,
and writes the resulting "dirty" datasets to 'data/dirty_data/' with filenames prefixed by 'dirty_'.
Each dataset will have 5 rows added for each error type.
"""

import sys
import pathlib
import pandas as pd

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import logger from our utils module
from utils.utils_logger import logger

# Set up folder paths
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DIRTY_DATA_DIR = PROJECT_ROOT / "data" / "dirty_data"

# Create the dirty_data directory if it doesn't exist
DIRTY_DATA_DIR.mkdir(parents=True, exist_ok=True)
logger.info(f"Dirty data directory set to: {DIRTY_DATA_DIR}")

##############################
# Customers Data
##############################
logger.info("Processing customers_data.csv for dirty data injection")
df_customers = pd.read_csv(RAW_DATA_DIR / "customers_data.csv")
logger.info(f"Original customers data shape: {df_customers.shape}")

# --- Outliers (e.g., extreme CustomerID values, far-future JoinDate, unusual Region) ---
outliers_customers = pd.DataFrame({
    "CustomerID": [99999, 88888, 77777, 66666, 55555],
    "Name": ["OutlierCust1", "OutlierCust2", "OutlierCust3", "OutlierCust4", "OutlierCust5"],
    "Region": ["Outlier"] * 5,
    "JoinDate": ["12/31/2099"] * 5
})
logger.info("Created outlier rows for customers data")

# --- Missing Values (insert rows with some missing values) ---
missing_customers = pd.DataFrame({
    "CustomerID": [None] * 5,
    "Name": [None, "MissingName", None, "MissingName", None],
    "Region": [None, None, "MissingRegion", None, "MissingRegion"],
    "JoinDate": [None, "1/1/2020", None, None, "2/2/2020"]
})
logger.info("Created missing value rows for customers data")

# --- Mis-entered Data (wrong types, invalid dates, gibberish) ---
misentered_customers = pd.DataFrame({
    "CustomerID": ["ABC", "DEF", "GHI", "JKL", "MNO"],
    "Name": ["123", "???", "", "   ", "Name!"],
    "Region": ["123", "!", "???", "None", "Out!"],
    "JoinDate": ["notadate", "13-13-2020", "2020/02/30", "00/00/0000", "abcd"]
})
logger.info("Created mis-entered rows for customers data")

df_dirty_customers = pd.concat([df_customers, outliers_customers, missing_customers, misentered_customers], ignore_index=True)
logger.info(f"Dirty customers data shape: {df_dirty_customers.shape}")
df_dirty_customers.to_csv(DIRTY_DATA_DIR / "dirty_customers_data.csv", index=False)
logger.info(f"Dirty customers data saved to {DIRTY_DATA_DIR / 'dirty_customers_data.csv'}")

##############################
# Products Data
##############################
logger.info("Processing products_data.csv for dirty data injection")
df_products = pd.read_csv(RAW_DATA_DIR / "products_data.csv")
logger.info(f"Original products data shape: {df_products.shape}")

# --- Outliers (extremely high/low UnitPrice, extreme ProductID) ---
outliers_products = pd.DataFrame({
    "ProductID": [99999, 88888, 77777, 66666, 55555],
    "ProductName": ["OutlierProd1", "OutlierProd2", "OutlierProd3", "OutlierProd4", "OutlierProd5"],
    "Category": ["Outlier"] * 5,
    "UnitPrice": [9999.99, 8888.88, 7777.77, -100.0, 123456.78]  # note negative value as outlier
})
logger.info("Created outlier rows for products data")

# --- Missing Values ---
missing_products = pd.DataFrame({
    "ProductID": [None] * 5,
    "ProductName": [None, "MissingProd", None, "MissingProd", None],
    "Category": [None, None, "MissingCat", None, "MissingCat"],
    "UnitPrice": [None, 0, None, None, 0]
})
logger.info("Created missing value rows for products data")

# --- Mis-entered Data ---
misentered_products = pd.DataFrame({
    "ProductID": ["A", "B", "C", "D", "E"],
    "ProductName": ["123", "???", "%%%", "", "Prod!"],
    "Category": ["123", "???", "None", "!!!", "Out!"],
    "UnitPrice": ["notanumber", "abc", "123.45.67", "price", "0xFF"]
})
logger.info("Created mis-entered rows for products data")

df_dirty_products = pd.concat([df_products, outliers_products, missing_products, misentered_products], ignore_index=True)
logger.info(f"Dirty products data shape: {df_dirty_products.shape}")
df_dirty_products.to_csv(DIRTY_DATA_DIR / "dirty_products_data.csv", index=False)
logger.info(f"Dirty products data saved to {DIRTY_DATA_DIR / 'dirty_products_data.csv'}")

##############################
# Sales Data
##############################
logger.info("Processing sales_data.csv for dirty data injection")
df_sales = pd.read_csv(RAW_DATA_DIR / "sales_data.csv")
logger.info(f"Original sales data shape: {df_sales.shape}")

# --- Outliers (extreme SaleAmount, unusual dates, extreme TransactionID) ---
outliers_sales = pd.DataFrame({
    "TransactionID": [99999, 88888, 77777, 66666, 55555],
    "SaleDate": ["12/31/2099"] * 5,
    "CustomerID": [99999, 99999, 99999, 99999, 99999],
    "ProductID": [99999, 99999, 99999, 99999, 99999],
    "StoreID": [999, 999, 999, 999, 999],
    "CampaignID": [99, 99, 99, 99, 99],
    "SaleAmount": [99999.99, 88888.88, 77777.77, -100.0, 123456.78]
})
logger.info("Created outlier rows for sales data")

# --- Missing Values ---
missing_sales = pd.DataFrame({
    "TransactionID": [None] * 5,
    "SaleDate": [None, "1/1/2020", None, "2/2/2020", None],
    "CustomerID": [None, None, 1001, None, 1002],
    "ProductID": [None, 101, None, 102, None],
    "StoreID": [None, None, None, 404, None],
    "CampaignID": [None] * 5,
    "SaleAmount": [None, 0, None, 0, None]
})
logger.info("Created missing value rows for sales data")

# --- Mis-entered Data ---
misentered_sales = pd.DataFrame({
    "TransactionID": ["a", "b", "c", "d", "e"],
    "SaleDate": ["notadate", "13-13-2020", "2020/02/30", "00/00/0000", "abcd"],
    "CustomerID": ["x", "y", "z", "w", "v"],
    "ProductID": ["p", "q", "r", "s", "t"],
    "StoreID": ["store", "store", "store", "store", "store"],
    "CampaignID": ["camp", "camp", "camp", "camp", "camp"],
    "SaleAmount": ["notanumber", "abc", "123.45.67", "price", "0xFF"]
})
logger.info("Created mis-entered rows for sales data")

df_dirty_sales = pd.concat([df_sales, outliers_sales, missing_sales, misentered_sales], ignore_index=True)
logger.info(f"Dirty sales data shape: {df_dirty_sales.shape}")
df_dirty_sales.to_csv(DIRTY_DATA_DIR / "dirty_sales_data.csv", index=False)
logger.info(f"Dirty sales data saved to {DIRTY_DATA_DIR / 'dirty_sales_data.csv'}")

logger.info("Dirty data files created successfully.")
print("Dirty data files created successfully in", DIRTY_DATA_DIR)
