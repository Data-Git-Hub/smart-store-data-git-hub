"""
Module: Prepare Products Data
File: scripts/data_preparation/prepare_products_data.py

This script reads the dirty_products_data.csv file from the data/dirty_data/ folder,
cleans it by removing duplicates, outliers, missing values, and mis-entered data,
and saves the cleaned data to the data/_prepared/ folder as products_data_prepared.csv.

It tests for all different possible errors in the dirty dataset.
"""

import sys
import pathlib
import pandas as pd

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import logger from our utils module
from utils.utils_logger import logger

# Define folder paths
DIRTY_DATA_DIR = PROJECT_ROOT / "data" / "dirty_data"
OUTPUT_DIR = PROJECT_ROOT / "data" / "_prepared"  # Output folder for cleaned data

# Create the output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# File paths
input_file = DIRTY_DATA_DIR / "dirty_products_data.csv"
output_file = OUTPUT_DIR / "products_data_prepared.csv"

# Expected valid values for cleaning
VALID_CATEGORIES = {"Electronics", "Clothing", "Sports"}
PRODUCTID_MIN = 100  # Minimum valid ProductID
PRODUCTID_MAX = 200  # Maximum valid ProductID
UNITPRICE_MIN = 0.1   # Minimum valid price (no free products)
UNITPRICE_MAX = 10000  # Maximum reasonable price


def clean_products_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the products data DataFrame."""
    
    logger.info(f"Starting cleaning: original shape = {df.shape}")
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    logger.info(f"After duplicates removal: shape = {df.shape}")
    
    # Convert ProductID to numeric (coerce errors to NaN) and drop rows with NaN ProductID
    df['ProductID'] = pd.to_numeric(df['ProductID'], errors='coerce')
    before = df.shape[0]
    df = df.dropna(subset=['ProductID'])
    logger.info(f"Dropped {before - df.shape[0]} rows due to non-numeric ProductID")
    
    # Filter ProductID outliers: keep only IDs between PRODUCTID_MIN and PRODUCTID_MAX
    before = df.shape[0]
    df = df[(df['ProductID'] >= PRODUCTID_MIN) & (df['ProductID'] <= PRODUCTID_MAX)]
    logger.info(f"Dropped {before - df.shape[0]} rows due to ProductID outliers")
    
    # Clean ProductName: strip whitespace; drop rows with empty ProductName after stripping
    df['ProductName'] = df['ProductName'].astype(str).str.strip()
    before = df.shape[0]
    df = df[df['ProductName'] != ""]
    logger.info(f"Dropped {before - df.shape[0]} rows due to empty ProductName")
    
    # Clean Category: strip and standardize case; drop rows with Category not in VALID_CATEGORIES
    df['Category'] = df['Category'].astype(str).str.strip().str.capitalize()
    before = df.shape[0]
    df = df[df['Category'].isin(VALID_CATEGORIES)]
    logger.info(f"Dropped {before - df.shape[0]} rows due to invalid Category")
    
    # Convert UnitPrice to numeric and filter reasonable price range
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
    before = df.shape[0]
    df = df.dropna(subset=['UnitPrice'])
    df = df[(df['UnitPrice'] >= UNITPRICE_MIN) & (df['UnitPrice'] <= UNITPRICE_MAX)]
    logger.info(f"Dropped {before - df.shape[0]} rows due to invalid UnitPrice values")

    logger.info(f"Final cleaned data shape: {df.shape}")
    return df


def main():
    logger.info("Starting prepare_products_data.py")
    
    try:
        df_dirty = pd.read_csv(input_file)
        logger.info(f"Loaded dirty products data from {input_file} with shape {df_dirty.shape}")
    except Exception as e:
        logger.error(f"Error reading input file: {e}")
        return
    
    # Clean the data using our function
    df_clean = clean_products_data(df_dirty)
    
    # Save the cleaned data
    try:
        df_clean.to_csv(output_file, index=False)
        logger.info(f"Cleaned products data saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving cleaned data: {e}")


if __name__ == "__main__":
    main()
