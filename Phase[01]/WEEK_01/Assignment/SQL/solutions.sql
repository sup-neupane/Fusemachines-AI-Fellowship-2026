-- 1.	Show all the customers whose creditLimit is greater than 20000   

SELECT *
FROM customers
WHERE creditLimit > 20000;

-- 2.	Show the employees who report to VP Sales.

SELECT *
FROM employees e
JOIN employees mgr ON e.reportsTo = mgr.employeeNumber
WHERE mgr.jobTitle = 'VP Sales';



-- 3.	Find all the customers who have set their state while filling the forms and Lives in USA and credit limit is between 100000 and 200000.

SELECT *
FROM customers
WHERE state IS NOT NULL
  AND country = 'USA'
  AND creditLimit BETWEEN 100000 AND 200000;



-- 4.	Find all the employees who report to Sales Managers of all types.

SELECT *
FROM employees e
JOIN employees mgr ON e.reportsTo = mgr.employeeNumber
WHERE mgr.jobTitle LIKE '%Sales Manager%';


-- 5.	Find the average credit limit of customers of each country.

SELECT country, ROUND(AVG(creditLimit), 2) AS avg_credit_limit
FROM customers
GROUP BY country
ORDER BY avg_credit_limit DESC;

-- 6. Find the total no. of orders for each date and customer. Show only dates with total
-- number of orders greater than 10 for date and customer. 

SELECT orderDate, customerNumber, COUNT(*) AS total_orders
FROM orders
GROUP BY orderDate, customerNumber
HAVING COUNT(*) > 10;


-- 7. Find the name of the supervisor, job title of supervisor and total no. of supervisee using subquery. (With out using Join operation)

SELECT
    (SELECT CONCAT(firstName, ' ', lastName)
     FROM employees 
     WHERE employeeNumber = e.reportsTo) AS supervisor_name,
    (SELECT jobTitle 
     FROM employees 
     WHERE employeeNumber = e.reportsTo) AS supervisor_title,
    COUNT(*) AS total_supervisees
FROM employees e
WHERE e.reportsTo IS NOT NULL
GROUP BY e.reportsTo;



-- 8. Find the name of the supervisor, job title of supervisor and total no. of supervisee using subquery. (With using Join operation)
SELECT
    CONCAT(mgr.firstName, ' ', mgr.lastName) AS supervisor_name,
    mgr.jobTitle AS supervisor_title,
    COUNT(emp.employeeNumber) AS total_supervisees
FROM employees emp
JOIN employees mgr ON emp.reportsTo = mgr.employeeNumber
GROUP BY mgr.employeeNumber, mgr.firstName, mgr.lastName, mgr.jobTitle
ORDER BY total_supervisees DESC;


-- 9. Find all customers with a credit limit greater than average credit credit limit using WITH Clause.

WITH avg_credit AS (
    SELECT AVG(creditLimit) AS avg_limit
    FROM customers
)
SELECT customerNumber, customerName, creditLimit
FROM customers, avg_credit
WHERE creditLimit > avg_limit;



-- 10. Find the rank of customer. [Customer with highest credit limit have 1 rank and Customer with lowest credit limit have highest rank]. Then, find the customer with the third highest credit limit.

SELECT customerName, creditLimit,
       RANK() OVER (ORDER BY creditLimit DESC) AS credit_rank
FROM customers;
SELECT customerName, creditLimit, credit_rank
FROM (
    SELECT customerName, creditLimit,
           RANK() OVER (ORDER BY creditLimit DESC) AS credit_rank
    FROM customers
) ranked
WHERE credit_rank = 3;


-- 11. Generate a report that shows total no. of employees working in each office.
SELECT o.city, o.country, COUNT(e.employeeNumber) AS total_employees
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
GROUP BY o.city, o.country
ORDER BY total_employees DESC;



-- 12. Generate a report that shows total no. of customers visited each office.
SELECT o.city, o.country, COUNT(c.customerNumber) AS total_customers
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.city, o.country
ORDER BY total_customers DESC;


-- 13. Generate a report that shows total payment received by each office using payment tables and essential tables. The report should show the office name, state and country, along with total payments made.

SELECT
    o.city AS office_name,
    o.state,
    o.country,
    ROUND(SUM(p.amount), 2) AS total_payments
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN payments p ON c.customerNumber = p.customerNumber
GROUP BY o.officeCode, o.city, o.state, o.country
ORDER BY total_payments DESC;


-- 14. Generate a report that shows total sales(in amount) by each office using order details table and other essential tables.
SELECT
    o.city AS office_name,
    o.country,
    ROUND(SUM(od.quantityOrdered * od.priceEach), 2) AS total_sales
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber = ord.customerNumber
JOIN orderdetails od ON ord.orderNumber = od.orderNumber
GROUP BY o.officeCode, o.city, o.country
ORDER BY total_sales DESC;


-- 15. Generate a report that shows total payment pending for each office.
SELECT
    o.city AS office_name,
    o.country,
    ROUND(SUM(od.quantityOrdered * od.priceEach), 2) AS total_ordered,
    ROUND(SUM(COALESCE(p.amount, 0)), 2) AS total_paid,
    ROUND(
        SUM(od.quantityOrdered * od.priceEach) - SUM(COALESCE(p.amount, 0)),
        2
    ) AS payment_pending
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber = ord.customerNumber
JOIN orderdetails od ON ord.orderNumber = od.orderNumber
LEFT JOIN payments p ON c.customerNumber = p.customerNumber
GROUP BY o.officeCode, o.city, o.country
ORDER BY payment_pending DESC;



-- 16. Find the creditLimit of each person, proportion of creditLimit of each person in each country. [Proportion of person in USA = creditLimit of that person / sum(creditLimit of all person in USA]
SELECT
    customerName,
    country,
    creditLimit,
    ROUND(
        creditLimit / SUM(creditLimit) OVER (PARTITION BY country), 4
    ) AS proportion_in_country
FROM customers
WHERE creditLimit > 0
ORDER BY country, proportion_in_country DESC;

-- 17. Create a view showing the customer name, complete address, and their total number of orders.
CREATE VIEW customer_order_summary AS
SELECT
    c.customerName,
    CONCAT_WS(', ',
        c.addressLine1,
        c.addressLine2,
        c.city,
        c.state,
        c.postalCode,
        c.country
    ) AS full_address,
    COUNT(o.orderNumber) AS total_orders
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
GROUP BY c.customerNumber;

SELECT * FROM customer_order_summary;




-- 18. Update the country of a customer (use any one record).
-- Before update
SELECT customerNumber, customerName, country FROM customers WHERE customerNumber = 103;

-- Update
UPDATE customers
SET country = 'Germany'
WHERE customerNumber = 103;

-- Verify
SELECT customerNumber, customerName, country FROM customers WHERE customerNumber = 103;

-- 19. Delete all payments below 20,000.
-- Preview what will be deleted
SELECT * FROM payments WHERE amount < 20000;

-- Delete
DELETE FROM payments
WHERE amount < 20000;

-- Verify
SELECT COUNT(*) FROM payments;


-- 20. Add new payments manually for an existing customer.
INSERT INTO payments (customerNumber, checkNumber, paymentDate, amount)
VALUES
    (112, 'NEW001', '2025-01-15', 25000.00),
    (112, 'NEW002', '2025-02-20', 15000.00);

-- Verify
SELECT * FROM payments WHERE customerNumber = 112;

