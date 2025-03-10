# smart-store-data-git-hub
P1. BI Python - Initial Step Up

# Project File Organization

```plaintext
smart-store-data-git-hub
|
|- data/
|   | - raw
        |- customers_data.csv
        |- products_data.csv
        |- sales_data.csv
    | - processed
        |- customer_average_transaction_size.png
        |- customer_average_transaction_size.txt
        |- customer_total_revenue_pie.png
        |- customer_total_revenue.txt  
        |- P1_B1_Python,txt  
|- logs/
|   |- project_log.log
|- scripts/
    |- bi_analysis.py
    |- customer_avg_transaction_size.py
    |- customer_total_revenue.py
|- utils/
|   |- utils_logger.py
|- .gitignore
|- README.md
|- requirements.txt
```

## P1.1 - CUSTOMER_AVERAGE_TRANSACTION_SIZE
Overview
Calculate the average transaction size for each customer. Understanding average transaction sizes can help inform upselling strategies or customer segmentation.

Required Data Columns
CustomerID: Unique identifier for each customer.
SaleAmount: The total value of each transaction.
Data Preparation Steps
Ensure each customer’s transactions are recorded accurately.
Calculation Instructions
Group transactions by CustomerID.
Sum SaleAmount for each customer.
Divide the total sales by the number of transactions to calculate the average transaction size per customer.
Expected Outcome
A list of customers and their respective average transaction sizes.

Data-Driven Decision (DDDM)
KPI: Average Transaction Value (Total sales per transaction).

Action: Focus upselling or promotional efforts on customers with lower transaction sizes, while offering personalized rewards to those with higher transaction sizes to encourage repeat business.

## P1.2 - CUSTOMER_TOTAL_REVENUE
Overview
Calculate the total revenue generated by each customer. Understanding which customers contribute the most to overall sales can help businesses target their most valuable customers for loyalty programs or personalized marketing.

Required Data Columns
CustomerID: Unique identifier for each customer.
SaleAmount: Total revenue from each sale.
Data Preparation Steps
Ensure that each transaction is associated with the correct customer.
Calculation Instructions
Group transactions by CustomerID.
Sum SaleAmount for each customer.
Expected Outcome
A list of customers and the total revenue they have generated.

Data-Driven Decision (DDDM)
KPI: Customer Lifetime Value (CLV) or Total Revenue per Customer.

Action: Identify high-revenue customers to target them for loyalty programs, upselling, or exclusive offers, while identifying low-revenue customers who may benefit from promotional incentives.

## P1.3 - PRODUCT_CATEGORY_REVENUE
Overview
Calculate the total revenue generated by each product category. This helps in understanding which categories are driving the most revenue and which might need additional focus or promotion.

Required Data Columns
ProductID: Unique identifier for each product.
SaleAmount: Total revenue from each product.
Category (if available or can be derived through lookup).
Data Preparation Steps
Ensure products are correctly categorized, either in the dataset or through a lookup table.
Calculation Instructions
Group sales by Category.
Sum SaleAmount for each product category.
Rank categories based on total revenue.
Expected Outcome
A list of product categories and their respective total revenues.

Data-Driven Decision (DDDM)
KPI: Revenue by Product Category (Total sales by product category).

Action: Consider focusing marketing efforts or inventory management on higher-revenue categories. For lower-performing categories, assess whether pricing adjustments, promotions, or discontinuation is needed.

## P1.4 - PRODUCT_TOP_SELLERS_BY_QUANTITY
Overview
Identify the products with the highest number of units sold. This helps to determine which products are the best sellers in terms of volume, guiding inventory management and marketing strategies.

Required Data Columns
ProductID: Unique identifier for each product.
Quantity: Number of units sold in each transaction.
Data Preparation Steps
Ensure that each transaction includes the correct product and quantity.
Calculation Instructions
Group transactions by ProductID.
Sum Quantity for each product to find total units sold.
Expected Outcome
A ranked list of products based on the total number of units sold.

Data-Driven Decision (DDDM)
KPI: Units Sold per Product.

Action: Use this information to optimize inventory levels for top sellers and ensure marketing efforts focus on products that are already popular, while identifying slow-moving products that may need promotion or discontinuation.

## P1.5 - SALES_LOW_REVENUE_DAYOFWEEK
Overview
Analyze sales data to determine which day of the week consistently shows the lowest sales revenue. This can help inform decisions about reducing operating hours or focusing marketing efforts on less profitable days.

Required Data Columns
SaleDate: Date of the transaction.
SaleAmount: Revenue generated from the transaction.
Data Preparation Steps
Extract the day of the week from SaleDate to categorize sales by weekday.
Calculation Instructions
Group transactions by the day of the week.
Sum SaleAmount for each day.
Identify the day with the lowest total revenue.
Expected Outcome
A clear ranking of sales revenue by day of the week, highlighting the least profitable day.

Data-Driven Decision (DDDM)
KPI: Daily Sales Revenue (Total sales for each day of the week).

Action: Consider reducing operating hours on the least profitable day to cut overhead costs or focus promotions and marketing efforts to boost sales on that day.

## P1.6 - SALES_LOW_REVENUE_MONTH
Overview
Identify the month with the lowest sales revenue. This can help the business plan promotions or special events during slower months to boost revenue.

Required Data Columns
SaleDate: Date of the transaction.
SaleAmount: Revenue generated from the transaction.
Data Preparation Steps
Extract the month from SaleDate to categorize sales by month.
Calculation Instructions
Group transactions by month.
Sum SaleAmount for each month.
Identify the month with the lowest total revenue.
Expected Outcome
A clear ranking of sales revenue by month, identifying the slowest month in terms of sales.

Data-Driven Decision (DDDM)
KPI: Monthly Sales Revenue (Total sales for each month).

Action: Plan promotions, discounts, or marketing campaigns during the month with the lowest sales to increase traffic and revenue during slower periods.
