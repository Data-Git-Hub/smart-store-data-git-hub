"""
Script: clean_all_data.py

This script processes all CSV files in the 'data/raw' directory using the DataScrubber class.
It performs data cleaning and saves the cleaned files to 'data/actual_clean_data/' 
with a prefix 'clean_' added to the filenames.

Usage:
    Run this script from the root project directory with:
        py scripts/clean_all_data.py
"""

import pathlib
import sys
import pandas as pd

# Manually add the scripts folder to Python path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(SCRIPTS_DIR))

# Now import DataScrubber
from data_scrubber import DataScrubber  

# Define directories
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "actual_clean_data"

# Ensure the output directory exists
CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def process_file(file_path: pathlib.Path):
    """Reads, cleans, and saves a CSV file using the DataScrubber class."""
    try:
        df = pd.read_csv(file_path)  # Read raw data
        scrubber = DataScrubber(df)  # Create a DataScrubber object
        
        # Perform cleaning operations
        df = scrubber.handle_missing_data(fill_value="Unknown")
        df = scrubber.remove_duplicate_records()

        # Save the cleaned file with 'clean_' prefix
        clean_filename = f"clean_{file_path.name}"
        cleaned_path = CLEANED_DATA_DIR / clean_filename
        df.to_csv(cleaned_path, index=False)

        print(f"Cleaned file saved: {cleaned_path}")
    
    except Exception as e:
        print(f"Error processing {file_path.name}: {e}")

def main():
    """Processes all CSV files in the raw data folder."""
    print("Starting Data Cleaning Process")

    csv_files = list(RAW_DATA_DIR.glob("*.csv"))  # Get all CSV files in raw data folder
    if not csv_files:
        print("No CSV files found in raw data folder.")
        return

    for file in csv_files:
        print(f"Processing: {file.name}...")
        process_file(file)

    print("All files processed successfully!")

if __name__ == "__main__":
    main()
