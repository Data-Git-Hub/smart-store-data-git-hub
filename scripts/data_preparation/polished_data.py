"""
Module: Polished Data Runner
File: scripts/data_preparation/polished_data.py

This script runs all the data cleaning scripts:
- prepare_customers_data.py
- prepare_products_data.py
- prepare_sales_data.py

It ensures all raw data is cleaned and saved in the `_prepared` folder.
"""

import sys
import pathlib
import subprocess

# Define project root dynamically
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

# Add project root to Python path (so utils can be found)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now import the logger
from utils.utils_logger import logger

# Define script paths
DATA_PREP_SCRIPTS_DIR = PROJECT_ROOT / "scripts" / "data_preparation"

# Define cleaning script paths
CLEANING_SCRIPTS = [
    DATA_PREP_SCRIPTS_DIR / "prepare_customers_data.py",
    DATA_PREP_SCRIPTS_DIR / "prepare_products_data.py",
    DATA_PREP_SCRIPTS_DIR / "prepare_sales_data.py",
]

def run_script(script_path):
    """Run a Python script as a subprocess."""
    try:
        logger.info(f"Running script: {script_path}")
        result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
        logger.info(f"Script {script_path.name} completed successfully.")
        logger.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running script {script_path.name}: {e.stderr}")

def main():
    logger.info("Starting polished_data.py - Running all data cleaning scripts.")
    
    for script in CLEANING_SCRIPTS:
        run_script(script)

    logger.info("All data cleaning scripts completed successfully.")

if __name__ == "__main__":
    main()
