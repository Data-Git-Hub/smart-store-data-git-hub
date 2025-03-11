"""
Module: Prepare Customers Data
File: scripts/data_preparation/prepare_customers_data.py

This script reads the dirty_customers_data.csv file from the data/dirty_data/ folder,
cleans it by removing duplicates, outliers, missing values, and mis-entered data,
and saves the cleaned data to the data/_prepared/ folder as customers_data_prepared.csv.

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
input_file = DIRTY_DATA_DIR / "dirty_customers_data.csv"
output_file = OUTPUT_DIR / "customers_data_prepared.csv"

# Expected valid values for cleaning
VALID_REGIONS = {"East", "West", "North", "South"}
CUSTOMERID_MIN = 1000
CUSTOMERID_MAX = 1100

def clean_customers_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the customers data DataFrame."""
    
    logger.info(f"Starting cleaning: original shape = {df.shape}")
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    logger.info(f"After duplicates removal: shape = {df.shape}")
    
    # Convert CustomerID to numeric (coerce errors to NaN) and drop rows with NaN CustomerID
    df['CustomerID'] = pd.to_numeric(df['CustomerID'], errors='coerce')
    before = df.shape[0]
    df = df.dropna(subset=['CustomerID'])
    logger.info(f"Dropped {before - df.shape[0]} rows due to non-numeric CustomerID")
    
    # Filter CustomerID outliers: keep only IDs between CUSTOMERID_MIN and CUSTOMERID_MAX
    before = df.shape[0]
    df = df[(df['CustomerID'] >= CUSTOMERID_MIN) & (df['CustomerID'] <= CUSTOMERID_MAX)]
    logger.info(f"Dropped {before - df.shape[0]} rows due to CustomerID outliers")
    
    # Clean Name: strip whitespace; drop rows with empty Name after stripping
    df['Name'] = df['Name'].astype(str).str.strip()
    before = df.shape[0]
    df = df[df['Name'] != ""]
    logger.info(f"Dropped {before - df.shape[0]} rows due to empty Name")
    
    # Clean Region: strip and standardize case; drop rows with Region not in VALID_REGIONS
    df['Region'] = df['Region'].astype(str).str.strip().str.capitalize()
    before = df.shape[0]
    df = df[df['Region'].isin(VALID_REGIONS)]
    logger.info(f"Dropped {before - df.shape[0]} rows due to invalid Region")
    
    # Convert JoinDate to datetime; drop rows where conversion fails
    df['JoinDate'] = pd.to_datetime(df['JoinDate'], errors='coerce', infer_datetime_format=True)
    before = df.shape[0]
    df = df.dropna(subset=['JoinDate'])
    logger.info(f"Dropped {before - df.shape[0]} rows due to invalid JoinDate")
    
    logger.info(f"Final cleaned data shape: {df.shape}")
    return df

def main():
    logger.info("Starting prepare_customers_data.py")
    
    try:
        df_dirty = pd.read_csv(input_file)
        logger.info(f"Loaded dirty customers data from {input_file} with shape {df_dirty.shape}")
    except Exception as e:
        logger.error(f"Error reading input file: {e}")
        return
    
    # Clean the data using our function
    df_clean = clean_customers_data(df_dirty)
    
    # Save the cleaned data
    try:
        df_clean.to_csv(output_file, index=False)
        logger.info(f"Cleaned customers data saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving cleaned data: {e}")

if __name__ == "__main__":
    main()
