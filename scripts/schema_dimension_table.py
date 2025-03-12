import pathlib
import sys
import pandas as pd

# Get project root directory and add it to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now, import logger from utils
from utils.utils_logger import logger  

# Define file paths
DATA_DIR = PROJECT_ROOT / "data"
PREPARED_DIR = DATA_DIR / "_prepared"
PROCESSED_DIR = DATA_DIR / "processed"

# Ensure processed directory exists
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Define schema output file
SCHEMA_FILE = PROCESSED_DIR / "schema_dimension_tables.txt"

def get_schema(df, table_name):
    """Generates schema details from a DataFrame."""
    schema = [f"{col}: {str(dtype)}" for col, dtype in df.dtypes.items()]
    return f"Schema for {table_name}:\n" + "\n".join(schema) + "\n\n"

def main():
    logger.info("Generating schema for dimension tables...")

    # Load prepared CSVs
    customers_df = pd.read_csv(PREPARED_DIR / "customers_data_prepared.csv")
    products_df = pd.read_csv(PREPARED_DIR / "products_data_prepared.csv")
    sales_df = pd.read_csv(PREPARED_DIR / "sales_data_prepared.csv")

    # Generate schemas
    schema_text = ""
    schema_text += get_schema(customers_df, "customers")
    schema_text += get_schema(products_df, "products")
    schema_text += get_schema(sales_df, "sales")

    # Save to schema file
    with open(SCHEMA_FILE, "w", encoding="utf-8") as f:
        f.write(schema_text)

    logger.info(f"Schema saved to {SCHEMA_FILE}")

if __name__ == "__main__":
    main()
