"""
Module: Prepare Sales Data
File: scripts/data_preparation/prepare_sales_data.py

This script reads the dirty_sales_data.csv file from the data/dirty_data/ folder,
cleans it by removing duplicates, outliers, missing values, and mis-entered data,
and saves the cleaned data to the data/_prepared/ folder as sales_data_prepared.csv.

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
input_file = DIRTY_DATA_DIR / "dirty_sales_data.csv"
output_file = OUTPUT_DIR / "sales_data_prepared.csv"

# Expected valid values for cleaning
TRANSACTIONID_MIN = 500
TRANSACTIONID_MAX = 1000
SALEAMOUNT_MIN = 0.1  # Minimum valid sale amount
SALEAMOUNT_MAX = 10000  # Maximum reasonable sale amount

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the sales data DataFrame."""
    
    logger.info(f"Starting cleaning: original shape = {df.shape}")
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    logger.info(f"After duplicates removal: shape = {df.shape}")
    
    # Convert TransactionID to numeric (coerce errors to NaN) and drop rows with NaN TransactionID
    df['TransactionID'] = pd.to_numeric(df['TransactionID'], errors='coerce')
    before = df.shape[0]
    df = df.dropna(subset=['TransactionID'])
    logger.info(f"Dropped {before - df.shape[0]} rows due to non-numeric TransactionID")
    
    # Filter TransactionID outliers: keep only IDs between TRANSACTIONID_MIN and TRANSACTIONID_MAX
    before = df.shape[0]
    df = df[(df['TransactionID'] >= TRANSACTIONID_MIN) & (df['TransactionID'] <= TRANSACTIONID_MAX)]
    logger.info(f"Dropped {before - df.shape[0]} rows due to TransactionID outliers")
    
    # Convert SaleDate to datetime; drop rows where conversion fails
    df['SaleDate'] = pd.to_datetime(df['SaleDate'], errors='coerce', infer_datetime_format=True)
    before = df.shape[0]
    df = df.dropna(subset=['SaleDate'])
    logger.info(f"Dropped {before - df.shape[0]} rows due to invalid SaleDate")

    # Convert SaleAmount to numeric and filter reasonable values
    df['SaleAmount'] = pd.to_numeric(df['SaleAmount'], errors='coerce')
    before = df.shape[0]
    df = df.dropna(subset=['SaleAmount'])
    df = df[(df['SaleAmount'] >= SALEAMOUNT_MIN) & (df['SaleAmount'] <= SALEAMOUNT_MAX)]
    logger.info(f"Dropped {before - df.shape[0]} rows due to invalid SaleAmount values")

    logger.info(f"Final cleaned data shape: {df.shape}")
    return df

def main():
    logger.info("Starting prepare_sales_data.py")
    
    try:
        df_dirty = pd.read_csv(input_file)
        logger.info(f"Loaded dirty sales data from {input_file} with shape {df_dirty.shape}")
    except Exception as e:
        logger.error(f"Error reading input file: {e}")
        return
    
    # Clean the data using our function
    df_clean = clean_sales_data(df_dirty)
    
    # Save the cleaned data
    try:
        df_clean.to_csv(output_file, index=False)
        logger.info(f"Cleaned sales data saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving cleaned data: {e}")

if __name__ == "__main__":
    main()
