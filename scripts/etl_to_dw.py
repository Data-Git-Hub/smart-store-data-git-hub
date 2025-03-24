import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.utils_logger import logger  # Custom logger

# Paths
DATA_DIR = PROJECT_ROOT / "data"
PREPARED_DATA_DIR = DATA_DIR / "prepared"
DW_DIR = DATA_DIR / "dw"
DW_DIR.mkdir(exist_ok=True)
DB_PATH = DW_DIR / "smart_sales.db"


def create_schema(cursor):
    logger.info("Creating tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            join_date TEXT,
            loyalty_points INTEGER,
            customer_segment TEXT,
            standard_datetime TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unit_price REAL,
            stock_quantity INTEGER,
            supplier TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            transaction_id INTEGER PRIMARY KEY,
            sale_date TEXT,
            customer_id INTEGER,
            product_id INTEGER,
            store_id INTEGER,
            campaign_id INTEGER,
            sale_amount REAL,
            discount_percent INTEGER,
            payment_type TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """)


def delete_existing_records(cursor):
    logger.info("Clearing existing records...")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM sales")


def insert_data(df, table_name, cursor):
    logger.info(f"Inserting data into {table_name} table...")
    df.to_sql(table_name, cursor.connection, if_exists="append", index=False)


def load_data_to_dw():
    logger.info("Connecting to SQLite database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        create_schema(cursor)
        delete_existing_records(cursor)

        logger.info("Reading prepared CSVs...")
        customers_df = pd.read_csv(PREPARED_DATA_DIR / "customers_data_prepared.csv")
        products_df = pd.read_csv(PREPARED_DATA_DIR / "products_data_prepared.csv")
        sales_df = pd.read_csv(PREPARED_DATA_DIR / "sales_data_prepared.csv")

        # Rename customer columns to match table schema
        customers_df.rename(columns={
            "CustomerID": "customer_id",
            "Name": "name",
            "Region": "region",
            "JoinDate": "join_date",
            "LoyaltyPoints": "loyalty_points",
            "CustomerSegment": "customer_segment",
            "StandardDateTime": "standard_datetime"
        }, inplace=True)

        # Rename product columns to match table schema
        products_df.rename(columns={
            "ProductID": "product_id",
            "ProductName": "product_name",
            "Category": "category",
            "UnitPrice": "unit_price",
            "StockQuantity": "stock_quantity",
            "Supplier": "supplier"
        }, inplace=True)

        # Rename sales columns to match table schema
        sales_df.rename(columns={
            "TransactionID": "transaction_id",
            "SaleDate": "sale_date",
            "CustomerID": "customer_id",
            "ProductID": "product_id",
            "StoreID": "store_id",
            "CampaignID": "campaign_id",
            "SaleAmount": "sale_amount",
            "DiscountPercent": "discount_percent",
            "PaymentType": "payment_type"
        }, inplace=True)

        insert_data(customers_df, "customers", cursor)
        insert_data(products_df, "products", cursor)
        insert_data(sales_df, "sales", cursor)

        conn.commit()
        logger.info("ETL process completed successfully.")
    except Exception as e:
        logger.error(f"ETL process failed: {e}")
    finally:
        conn.close()
        logger.info("Database connection closed.")


if __name__ == "__main__":
    load_data_to_dw()
