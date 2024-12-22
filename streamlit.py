import streamlit as st
import mysql.connector
import pandas as pd

# Establishing the connection to the database
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",       # e.g., "localhost"
        user="root",       # e.g., "root"
        password="shakthi07",
        database="dataspark"    # The database you're using
    )
    return conn

# Function to execute the query and return the result as a DataFrame
def execute_query(query):
    conn = create_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit UI elements
st.title("Data Analysis Dashboard")

# Create a list of query options
query_options = [
    "Customer Distribution by Gender",
    "Age Distribution",
    "Customer Geographic Distribution",
    "Average Order Value",
    "Frequency of Purchases per Customer",
    "Preferred Products",
    "Overall Sales Performance (2020)",
    "Sales by Product",
    "Store Sales Analysis",
    "Product Popularity",
    "Profitability Analysis",
    "Store Performance Analysis",
    "Geographical Sales Analysis (2020-2023)"
]

# Let the user select a query to run
selected_query = st.selectbox("Select a query to display:", query_options)

# Define the SQL queries for each option
queries = {
    "Customer Distribution by Gender": """
        SELECT Gender, COUNT(*) AS Customer_Count
        FROM customer_data
        GROUP BY Gender;
    """,
    "Age Distribution": """
        SELECT
          CASE 
            WHEN TIMESTAMPDIFF(YEAR, Birthday, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
            WHEN TIMESTAMPDIFF(YEAR, Birthday, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
            WHEN TIMESTAMPDIFF(YEAR, Birthday, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
            WHEN TIMESTAMPDIFF(YEAR, Birthday, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
            ELSE '55+'
          END AS Age_Range,
          COUNT(*) AS Customer_Count
        FROM customer_data
        GROUP BY Age_Range;
    """,
    "Customer Geographic Distribution": """
        SELECT Cust_Country, Cust_State, Cust_City, COUNT(*) AS Customer_Count
        FROM customer_data
        GROUP BY Cust_Country, Cust_State, Cust_City;
    """,
    "Average Order Value": """
        SELECT AVG(s.Quantity * p.UnitPriceUSD) AS Average_Order_Value
        FROM sales_data s
        JOIN product_data p ON s.ProductKey = p.ProductKey;
    """,
    "Frequency of Purchases per Customer": """
        SELECT CustomerKey, COUNT(*) AS Purchase_Frequency
        FROM sales_data
        GROUP BY CustomerKey
        ORDER BY Purchase_Frequency DESC;
    """,
    "Preferred Products": """
        SELECT p.ProductName, SUM(s.Quantity) AS Total_Quantity_Sold
        FROM sales_data s
        JOIN product_data p ON s.ProductKey = p.ProductKey
        GROUP BY p.ProductName
        ORDER BY Total_Quantity_Sold DESC
        LIMIT 10;
    """,
    "Overall Sales Performance (2020)": """
        SELECT
          YEAR(s.OrderDate) AS Year,
          MONTH(s.OrderDate) AS Month,
          SUM(s.Quantity * p.UnitPriceUSD) AS Total_Sales
        FROM sales_data s
        JOIN product_data p ON s.ProductKey = p.ProductKey
        WHERE YEAR(s.OrderDate) = 2020
        GROUP BY YEAR(s.OrderDate), MONTH(s.OrderDate)
        ORDER BY Year, Month;
    """,
    "Sales by Product": """
        SELECT 
          p.ProductName, 
          SUM(s.Quantity) AS Total_Quantity_Sold,
          SUM(s.Quantity * p.UnitPriceUSD) AS Total_Revenue
        FROM sales_data s
        JOIN product_data p ON s.ProductKey = p.ProductKey
        GROUP BY p.ProductName
        ORDER BY Total_Revenue DESC
        LIMIT 10;
    """,
    "Store Sales Analysis": """
        SELECT 
          st.Store_Country, 
          st.Store_State, 
          SUM(s.Quantity * p.UnitPriceUSD) AS Store_Sales
        FROM sales_data s
        JOIN store_data st ON s.StoreKey = st.StoreKey
        JOIN product_data p ON s.ProductKey = p.ProductKey
        GROUP BY st.Store_Country, st.Store_State
        ORDER BY Store_Sales DESC;
    """,
    "Product Popularity": """
        SELECT p.ProductName, SUM(s.Quantity) AS Total_Quantity_Sold
        FROM sales_data s
        JOIN product_data p ON s.ProductKey = p.ProductKey
        GROUP BY p.ProductName
        ORDER BY Total_Quantity_Sold DESC;
    """,
    "Profitability Analysis": """
        SELECT p.ProductName,
               SUM(s.Quantity * (p.UnitPriceUSD - p.UnitCostUSD)) AS Total_Profit
        FROM sales_data s
        JOIN product_data p ON s.ProductKey = p.ProductKey
        GROUP BY p.ProductName
        ORDER BY Total_Profit DESC;
    """,
    "Store Performance Analysis": """
        SELECT 
          st.StoreKey, 
          st.Store_Country, 
          st.Store_State, 
          st.SquareMeters, 
          st.OpenDate,
          SUM(s.Quantity * p.UnitPriceUSD) AS Store_Sales
        FROM store_data st
        JOIN sales_data s ON st.StoreKey = s.StoreKey
        JOIN product_data p ON s.ProductKey = p.ProductKey
        GROUP BY st.StoreKey, st.Store_Country, st.Store_State, st.SquareMeters, st.OpenDate
        ORDER BY Store_Sales DESC;
    """,
    "Geographical Sales Analysis (2020-2023)": """
        SELECT 
          st.Store_Country, 
          st.Store_State, 
          SUM(s.Quantity * p.UnitPriceUSD) AS Sales
        FROM sales_data s
        JOIN store_data st ON s.StoreKey = st.StoreKey
        JOIN product_data p ON s.ProductKey = p.ProductKey
        WHERE s.OrderDate BETWEEN '2020-01-01' AND '2023-12-31'
        GROUP BY st.Store_Country, st.Store_State
        ORDER BY Sales DESC;
    """
}

# Execute the selected query and display the result
if selected_query:
    query = queries[selected_query]
    query_result = execute_query(query)
    st.dataframe(query_result)
