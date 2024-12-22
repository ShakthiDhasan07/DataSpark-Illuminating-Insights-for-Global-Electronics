import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

# Load CSV files into DataFrames
df_sales = pd.read_csv("Cleaned_sales.csv")
df_stores = pd.read_csv("Cleaned_store.csv")
df_customer = pd.read_csv("Cleaned_customer.csv")
df_product = pd.read_csv("Cleaned_product.csv")
df_exchange = pd.read_csv("Cleaned_exchange.csv")

# Connect to MySQL using the connector (for other database operations)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shakthi07",
    database="DataSpark"
)
my_cursor = conn.cursor()

# Create SQLAlchemy engine to interact with MySQL using pandas' to_sql method
engine = create_engine('mysql+mysqlconnector://root:shakthi07@localhost/DataSpark')

# Table creation (if not exists) can be done through SQLAlchemy when using to_sql
# You can also manually create tables in MySQL if needed.

# Insert data into the sales_data table using pandas' to_sql
df_sales.to_sql(name='sales_data', con=engine, if_exists='replace', index=False)

print("Inserted successfully using pandas to_sql")

# Similarly, for other dataframes (stores, customer, product, and exchange data), you can do:

df_stores.to_sql(name='store_data', con=engine, if_exists='replace', index=False)
print("Store data inserted successfully")

df_customer.to_sql(name='customer_data', con=engine, if_exists='replace', index=False)
print("Customer data inserted successfully")

df_product.to_sql(name='product_data', con=engine, if_exists='replace', index=False)
print("Product data inserted successfully")

df_exchange.to_sql(name='exchange_data', con=engine, if_exists='replace', index=False)
print("Exchange data inserted successfully")
