"""
Script to answer BI questions:
6. What looks like the most common customer region? 
7. What looks like the highest/lowest product price?
8. What looks like the estimated Average, Minimum, and Maximum sales?

The results are written to data/processed/P1_BI_Python.txt.
"""

import sys
import pathlib
import csv
from collections import Counter

# Enhance sys.path setup: determine the project root (one level up from the scripts folder)
project_root = pathlib.Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Now import the logger from the utils package
try:
    from utils.utils_logger import logger
except ModuleNotFoundError as e:
    print("ModuleNotFoundError: Ensure that your 'utils' folder contains an __init__.py file and is in the project root.")
    raise e

#####################################
# Setup folder paths
#####################################

raw_data_folder = project_root / "data" / "raw"
processed_data_folder = project_root / "data" / "processed"

#####################################
# Define Functions
#####################################

def get_most_common_customer_region():
    """
    Determines the most common customer region from customers_data.csv.
    Assumes a column named "Region" exists.
    """
    customers_file = raw_data_folder / "customers_data.csv"
    regions = []
    try:
        with customers_file.open('r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            if "Region" not in reader.fieldnames:
                msg = "Column 'Region' not found in customers_data.csv."
                logger.error(msg)
                return msg
            for row in reader:
                region = row.get("Region", "").strip()
                if region:
                    regions.append(region)
        if regions:
            region_counter = Counter(regions)
            most_common = region_counter.most_common(1)[0]
            result = f"{most_common[0]} (appears {most_common[1]} times)"
            logger.info(f"Most common customer region: {result}")
            return result
        else:
            msg = "No customer regions found."
            logger.warning(msg)
            return msg
    except Exception as e:
        error_msg = f"Error processing customers_data.csv: {e}"
        logger.error(error_msg)
        return error_msg


def get_highest_lowest_product_price():
    """
    Finds the highest and lowest product price from products_data.csv.
    Assumes a column named "UnitPrice" exists.
    """
    products_file = raw_data_folder / "products_data.csv"
    prices = []
    try:
        with products_file.open('r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            if "UnitPrice" not in reader.fieldnames:
                msg = "Column 'UnitPrice' not found in products_data.csv."
                logger.error(msg)
                return msg
            for row in reader:
                price_str = row.get("UnitPrice", "").strip()
                try:
                    price = float(price_str)
                    prices.append(price)
                except ValueError:
                    logger.warning(f"Invalid price value: {price_str}")
                    continue
        if prices:
            highest = max(prices)
            lowest = min(prices)
            result = (f"Highest product price: ${highest:.2f}\n"
                      f"Lowest product price:  ${lowest:.2f}")
            logger.info("Calculated highest and lowest product prices.")
            return result
        else:
            msg = "No valid product prices found."
            logger.warning(msg)
            return msg
    except Exception as e:
        error_msg = f"Error processing products_data.csv: {e}"
        logger.error(error_msg)
        return error_msg


def get_sales_statistics():
    """
    Calculates the average, minimum, and maximum sale amounts from sales_data.csv.
    Assumes a column named "SaleAmount" exists.
    """
    sales_file = raw_data_folder / "sales_data.csv"
    sales = []
    try:
        with sales_file.open('r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            if "SaleAmount" not in reader.fieldnames:
                msg = "Column 'SaleAmount' not found in sales_data.csv."
                logger.error(msg)
                return msg
            for row in reader:
                sale_str = row.get("SaleAmount", "").strip()
                try:
                    sale = float(sale_str)
                    sales.append(sale)
                except ValueError:
                    logger.warning(f"Invalid sale amount: {sale_str}")
                    continue
        if sales:
            avg_sale = sum(sales) / len(sales)
            min_sale = min(sales)
            max_sale = max(sales)
            result = (f"Average Sale: ${avg_sale:.2f}\n"
                      f"Minimum Sale: ${min_sale:.2f}\n"
                      f"Maximum Sale: ${max_sale:.2f}")
            logger.info("Calculated sales statistics.")
            return result
        else:
            msg = "No valid sales data found."
            logger.warning(msg)
            return msg
    except Exception as e:
        error_msg = f"Error processing sales_data.csv: {e}"
        logger.error(error_msg)
        return error_msg


def main():
    # Ensure the processed folder exists
    processed_data_folder.mkdir(parents=True, exist_ok=True)
    output_file = processed_data_folder / "P1_BI_Python.txt"
    
    # Get the answers
    common_region = get_most_common_customer_region()
    product_price_info = get_highest_lowest_product_price()
    sales_stats = get_sales_statistics()
    
    # Write results to output file
    try:
        with output_file.open('w', encoding='utf-8') as f:
            f.write("P1. BI Python Analysis Results\n")
            f.write("=" * 40 + "\n\n")
            f.write("6. Most Common Customer Region:\n")
            f.write(common_region + "\n\n")
            f.write("7. Highest and Lowest Product Price:\n")
            f.write(product_price_info + "\n\n")
            f.write("8. Sales Statistics (Average, Minimum, Maximum):\n")
            f.write(sales_stats + "\n")
        logger.info(f"Analysis complete. Results saved to: {output_file}")
        print(f"Analysis complete. Results saved to: {output_file}")
    except Exception as e:
        logger.error(f"Error writing output file: {e}")


if __name__ == "__main__":
    main()
