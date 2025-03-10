"""
Process a CSV file to determine the average transaction size per customer,
compute an overall average, and generate a bar graph.
"""

#####################################
# Adjust sys.path to include the project root
#####################################

import sys
import pathlib

# Determine the project root (one level up from the scripts folder)
project_root = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

#####################################
# Import Modules
#####################################

import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Import the logger from the utils module (note: file name is utils_logger.py)
from utils.utils_logger import logger

#####################################
# Declare Global Variables
#####################################

# Folder paths for input and output
raw_data_folder: str = "data/raw"  # Now contains the CSV files (customers_data.csv, products_data.csv, sales_data.csv)
processed_data_folder: str = "data/processed"  # Output folder for processed files

#####################################
# Define Functions
#####################################

def get_customer_average_transaction_size(file_path: pathlib.Path) -> tuple:
    """
    Analyze the CSV file to calculate the average transaction size per customer and overall average.
    
    Args:
        file_path (pathlib.Path): Path to the sales CSV file.
        
    Returns:
        tuple: A tuple containing:
            - List of tuples (CustomerID, average transaction size).
            - Overall average transaction size (float).
    """
    try:
        # Dictionaries to store total sales and number of transactions per customer
        customer_totals = defaultdict(float)
        customer_counts = defaultdict(int)
        
        with file_path.open('r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            # Normalize column names
            csv_reader.fieldnames = [col.strip().replace("\xa0", "") for col in csv_reader.fieldnames]
            
            # Verify that required columns are present
            if "CustomerID" not in csv_reader.fieldnames or "SaleAmount" not in csv_reader.fieldnames:
                logger.error(f"CSV missing required columns. Found headers: {csv_reader.fieldnames}")
                return ([], 0)
            
            for row in csv_reader:
                customer_id = row.get("CustomerID", "").strip()
                sale_amount = row.get("SaleAmount", "").strip()
                if customer_id and sale_amount:
                    try:
                        sale_amount_value = float(sale_amount)
                        customer_totals[customer_id] += sale_amount_value
                        customer_counts[customer_id] += 1
                    except ValueError:
                        logger.warning(f"Invalid sale amount for customer {customer_id}: {sale_amount}")
                        continue
        
        # Calculate per-customer average transaction size
        average_transaction_sizes = []
        for customer, total in customer_totals.items():
            count = customer_counts[customer]
            average = total / count if count != 0 else 0
            average_transaction_sizes.append((customer, average))
        
        # Calculate overall average transaction size across all transactions
        overall_total = sum(customer_totals.values())
        overall_count = sum(customer_counts.values())
        overall_average = overall_total / overall_count if overall_count != 0 else 0

        return average_transaction_sizes, overall_average

    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
        return ([], 0)


def produce_bar_graph(customer_averages: list, output_path: pathlib.Path):
    """
    Produce a bar graph of customer average transaction sizes and save to a file.
    
    Args:
        customer_averages (list): List of tuples (CustomerID, average transaction size).
        output_path (pathlib.Path): File path to save the bar graph image.
    """
    if not customer_averages:
        logger.error("No data available for bar graph.")
        return

    # Extract customer IDs and average values
    customers = [cust for cust, _ in customer_averages]
    averages = [avg for _, avg in customer_averages]

    plt.figure(figsize=(10, 6))
    plt.bar(customers, averages)
    plt.xlabel("CustomerID")
    plt.ylabel("Average Transaction Size ($)")
    plt.title("Average Transaction Size per Customer")
    plt.xticks(rotation=45, ha='right')

    # Set y-axis ticks in increments of $200
    max_value = max(averages)
    y_max = (int(max_value // 200) + 1) * 200
    plt.yticks(np.arange(0, y_max + 1, 200))

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def process_csv_file():
    """
    Process the sales CSV file to calculate and save the average transaction sizes,
    and generate a bar graph of the results.
    """
    input_file = pathlib.Path(raw_data_folder, "sales_data.csv")
    output_txt = pathlib.Path(processed_data_folder, "customer_average_transaction_size.txt")
    output_img = pathlib.Path(processed_data_folder, "customer_average_transaction_size.png")
    
    # Ensure the processed data folder exists
    output_txt.parent.mkdir(parents=True, exist_ok=True)
    
    customer_averages, overall_average = get_customer_average_transaction_size(input_file)
    
    with output_txt.open('w', encoding='utf-8') as file:
        file.write("Customer Average Transaction Size:\n")
        file.write("=" * 50 + "\n")
        file.write(f"{'CustomerID':<20}{'Avg Transaction Size'}\n")
        file.write("=" * 50 + "\n")
        for customer, avg in customer_averages:
            file.write(f"{customer:<20}{avg:.2f}\n")
        file.write("=" * 50 + "\n")
        file.write(f"{'OVERALL AVERAGE':<20}{overall_average:.2f}\n")
    
    logger.info(f"Processed CSV file: {input_file}, results saved to: {output_txt}")

    # Produce the bar graph and save it to a file
    produce_bar_graph(customer_averages, output_img)
    logger.info(f"Bar graph saved to: {output_img}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting processing of customer average transaction size...")
    process_csv_file()
    logger.info("Processing complete.")
