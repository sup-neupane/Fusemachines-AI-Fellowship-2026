-- List all products
SELECT "productCode", "productName", "productLine", "productVendor"
FROM products
LIMIT 5;

-- Get all customers
SELECT "customerNumber", "customerName", "city", "country"
FROM customers
LIMIT 5;


-- Show all orders
SELECT "orderNumber", "orderDate", "status", "customerNumber"
FROM orders
LIMIT 5;


-- List all employees
SELECT "employeeNumber", "firstName", "lastName", "jobTitle"
FROM employees;


-- Get all offices
SELECT "officeCode", "city", "country", "territory"
FROM offices;


-- Show all product lines
SELECT "productLine", "textDescription"
FROM productlines;


-- List all payments
SELECT "customerNumber", "checkNumber", "paymentDate", "amount"
FROM payments
LIMIT 5;



-- Get product names and prices
SELECT "productName", "buyPrice", "MSRP"
FROM products
LIMIT 5;


-- Get customer names and cities
SELECT "customerName", "city"
FROM customers
LIMIT 5;


-- List employee first and last names
SELECT "firstName", "lastName"
FROM employees;



-- Get all order dates
SELECT "orderNumber", "orderDate", "requiredDate", "shippedDate"
FROM orders
LIMIT 5;


-- Show product vendor list
SELECT DISTINCT "productVendor"
FROM products
ORDER BY "productVendor";


-- Get all product codes
SELECT "productCode"
FROM products;


-- List all countries from offices
SELECT DISTINCT "country"
FROM offices
ORDER BY "country";


-- Show all order statuses
SELECT DISTINCT "status"
FROM orders
ORDER BY "status";


-- Get all payment amounts
SELECT "customerNumber", "checkNumber", "paymentDate", "amount"
FROM payments
ORDER BY "amount" DESC
LIMIT 5;



-- List all job titles
SELECT DISTINCT "jobTitle"
FROM employees
ORDER BY "jobTitle";


-- Get customer phone numbers
SELECT "customerName", "phone"
FROM customers
ORDER BY "customerName"
LIMIT 5;


-- Show product MSRP values
SELECT "productName", "MSRP"
FROM products
ORDER BY "MSRP" DESC
LIMIT 5;


-- List order numbers
SELECT "orderNumber"
FROM orders
ORDER BY "orderNumber"
LIMIT 5;



-- Get orders with customer names
SELECT o."orderNumber", o."orderDate", o."status", c."customerName"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber"
LIMIT 5;


-- Get employees with office city
SELECT e."firstName", e."lastName", e."jobTitle", o."city" AS "officeCity"
FROM employees e
JOIN offices o ON e."officeCode" = o."officeCode"
ORDER BY o."city";


-- Get payments with customer names
SELECT p."checkNumber", p."paymentDate", p."amount", c."customerName"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber"
ORDER BY p."amount" DESC
LIMIT 5;



-- Get order details with product names
SELECT od."orderNumber", p."productName", od."quantityOrdered", od."priceEach"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode"
LIMIT 5;



-- Get products with product line description
SELECT p."productName", p."productLine", pl."textDescription"
FROM products p
JOIN productlines pl ON p."productLine" = pl."productLine"
LIMIT 5;


-- Get customers with sales rep names
SELECT c."customerName", c."country",
       e."firstName" || ' ' || e."lastName" AS "salesRepName"
FROM customers c
LEFT JOIN employees e ON c."salesRepEmployeeNumber" = e."employeeNumber"
ORDER BY c."customerName"
LIMIT 5;


-- Get orders with customer city
SELECT o."orderNumber", o."orderDate", o."status",
       c."customerName", c."city" AS "customerCity"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber"
ORDER BY c."city"
LIMIT 5;


-- Get employees and their manager
SELECT e."firstName" || ' ' || e."lastName" AS "employeeName",
       e."jobTitle",
       m."firstName" || ' ' || m."lastName" AS "managerName"
FROM employees e
LEFT JOIN employees m ON e."reportsTo" = m."employeeNumber"
ORDER BY m."lastName" NULLS LAST;


-- Get orderdetails with product vendor
SELECT od."orderNumber", p."productName", p."productVendor",
       od."quantityOrdered", od."priceEach"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode"
ORDER BY p."productVendor"
LIMIT 5;


-- Get payments with customer country
SELECT p."checkNumber", p."paymentDate", p."amount",
       c."customerName", c."country"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber"
ORDER BY c."country", p."amount" DESC
LIMIT 5;


-- Count customers per country
SELECT "country", COUNT(*) AS "customerCount"
FROM customers
GROUP BY "country"
ORDER BY "customerCount" DESC;


-- Total payments per customer
SELECT c."customerName",
       SUM(p."amount") AS "totalPayments",
       COUNT(p."checkNumber") AS "paymentCount"
FROM customers c
JOIN payments p ON c."customerNumber" = p."customerNumber"
GROUP BY c."customerName"
ORDER BY "totalPayments" DESC
LIMIT 5;


-- Number of orders per status
SELECT "status", COUNT(*) AS "orderCount"
FROM orders
GROUP BY "status"
ORDER BY "orderCount" DESC;


-- Products per product line
SELECT "productLine", COUNT(*) AS "productCount"
FROM products
GROUP BY "productLine"
ORDER BY "productCount" DESC;


-- Employees per office
SELECT o."city" AS "officeCity", o."country",
       COUNT(e."employeeNumber") AS "employeeCount"
FROM offices o
LEFT JOIN employees e ON o."officeCode" = e."officeCode"
GROUP BY o."officeCode", o."city", o."country"
ORDER BY "employeeCount" DESC;



-- Total stock per product vendor
SELECT "productVendor", SUM("quantityInStock") AS "totalStock"
FROM products
GROUP BY "productVendor"
ORDER BY "totalStock" DESC;


-- Average buy price per product line
SELECT "productLine",
       ROUND(AVG("buyPrice"), 2) AS "avgBuyPrice"
FROM products
GROUP BY "productLine"
ORDER BY "avgBuyPrice" DESC;


-- Orders per customer
SELECT c."customerName", COUNT(o."orderNumber") AS "orderCount"
FROM customers c
LEFT JOIN orders o ON c."customerNumber" = o."customerNumber"
GROUP BY c."customerName"
ORDER BY "orderCount" DESC
LIMIT 5;


-- Max MSRP per product line
SELECT "productLine", MAX("MSRP") AS "maxMSRP"
FROM products
GROUP BY "productLine"
ORDER BY "maxMSRP" DESC;


-- Min buy price per vendor
SELECT "productVendor", MIN("buyPrice") AS "minBuyPrice"
FROM products
GROUP BY "productVendor"
ORDER BY "minBuyPrice" ASC;


-- Total number of customers
SELECT COUNT(*) AS "totalCustomers"
FROM customers;


-- Total number of products
SELECT COUNT(*) AS "totalProducts"
FROM products;


-- Total revenue from payments
SELECT ROUND(SUM("amount"), 2) AS "totalRevenue"
FROM payments;


-- Average product price
SELECT ROUND(AVG("buyPrice"), 2) AS "avgBuyPrice",
       ROUND(AVG("MSRP"), 2) AS "avgMSRP"
FROM products;


-- Max payment amount
SELECT MAX("amount") AS "maxPayment"
FROM payments;


-- Min payment amount
SELECT MIN("amount") AS "minPayment"
FROM payments;


-- Count total orders
SELECT COUNT(*) AS "totalOrders"
FROM orders;


-- Total quantity in stock
SELECT SUM("quantityInStock") AS "totalStock"
FROM products;


-- Average MSRP
SELECT ROUND(AVG("MSRP"), 2) AS "avgMSRP"
FROM products;


-- Number of employees
SELECT COUNT(*) AS "totalEmployees"
FROM employees;
