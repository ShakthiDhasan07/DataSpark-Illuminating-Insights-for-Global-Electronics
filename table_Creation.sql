create database dataspark;
use dataspark;
select * from video;
show tables;
select * from product_data;
show tables;
select channel_name as channelname,AVG(duration) as averageduration from video group by channel_name;
show databases;
drop table channel;
drop table global_electronics;
select * from exchange_data;
select * from comments;
select * from sales_data;
drop table sales_data;
select * from video;
select gender from customer;
select * from Global_Electronics limit 10;
SELECT COUNT(*) FROM Global_Electronics;
#This query will provide the distribution of customers by gender.
SELECT Gender, COUNT(*) AS Customer_Count
FROM customer_data
GROUP BY Gender;
#Age Distribution:
#This query calculates the age of customers from their birthdate and groups them into age ranges for better analysis.
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
select * from sales_data;
#Geographic Distribution:
#This query analyzes the customer distribution by country, state, and city.

SELECT Cust_Country, Cust_State, Cust_City, COUNT(*) AS Customer_Count
FROM customer_data
GROUP BY Cust_Country, Cust_State, Cust_City;

#2. Purchase Patterns
#a. Average Order Value:
#This query calculates the average order value by dividing the total sales by the number of orders.
SELECT
  AVG(s.Quantity * p.UnitPriceUSD) AS Average_Order_Value
FROM sales_data s
JOIN product_data p ON s.ProductKey = p.ProductKey;
#b. Frequency of Purchases:
#This query calculates the number of purchases each customer has made, providing insight into customer loyalty and frequency of purchases.
SELECT CustomerKey, COUNT(*) AS Purchase_Frequency
FROM sales_data
GROUP BY CustomerKey
ORDER BY Purchase_Frequency DESC;


#c. Preferred Products:
#This query identifies the top-selling products based on the quantity sold.

SELECT p.ProductName, SUM(s.Quantity) AS Total_Quantity_Sold
FROM sales_data s
JOIN product_data p ON s.ProductKey = p.ProductKey
GROUP BY p.ProductName
ORDER BY Total_Quantity_Sold DESC
LIMIT 10;

#3. Sales Analysis
#a. Overall Sales Performance:
#This query calculates the total sales over time, grouped by month or year, to identify trends and seasonality.

SELECT
  YEAR(s.OrderDate) AS Year,
  MONTH(s.OrderDate) AS Month,
  SUM(s.Quantity * p.UnitPriceUSD) AS Total_Sales
FROM sales_data s
JOIN product_data p ON s.ProductKey = p.ProductKey
WHERE YEAR(s.OrderDate) = 2020
GROUP BY YEAR(s.OrderDate), MONTH(s.OrderDate)
ORDER BY Year, Month;

#Sales by Product:
#This query evaluates the top-performing products in terms of quantity sold and revenue generated.

SELECT 
  p.ProductName, 
  SUM(s.Quantity) AS Total_Quantity_Sold,
  SUM(s.Quantity * p.UnitPriceUSD) AS Total_Revenue
FROM sales_data s
JOIN product_data p ON s.ProductKey = p.ProductKey
GROUP BY p.ProductName
ORDER BY Total_Revenue DESC
LIMIT 10;


#c. Sales by Store:
#This query assesses the performance of different stores based on sales data.

SELECT 
  st.Store_Country, 
  st.Store_State, 
  SUM(s.Quantity * p.UnitPriceUSD) AS Store_Sales
FROM sales_data s
JOIN store_data st ON s.StoreKey = st.StoreKey
JOIN product_data p ON s.ProductKey = p.ProductKey
GROUP BY st.Store_Country, st.Store_State
ORDER BY Store_Sales DESC;

#4. Product Analysis
#a. Product Popularity:
#This query identifies the most and least popular products based on the quantity sold.

SELECT p.ProductName, SUM(s.Quantity) AS Total_Quantity_Sold
FROM sales_data s
JOIN product_data p ON s.ProductKey = p.ProductKey
GROUP BY p.ProductName
ORDER BY Total_Quantity_Sold DESC;

#b. Profitability Analysis:
#This query calculates the profitability of products by comparing the unit cost and unit price.

SELECT p.ProductName,
       SUM(s.Quantity * (p.UnitPriceUSD - p.UnitCostUSD)) AS Total_Profit
FROM sales_data s
JOIN product_data p ON s.ProductKey = p.ProductKey
GROUP BY p.ProductName
ORDER BY Total_Profit DESC;

#5. Store Analysis
#a. Store Performance:
#This query evaluates store performance based on sales, size (square meters), and operational data (open date).

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

#b. Geographical Sales Analysis:

#This query analyzes sales by store location to identify high-performing regions.

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




