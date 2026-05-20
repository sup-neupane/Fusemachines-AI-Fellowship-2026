SCHEMA_CONTEXT = """
You are a Text-to-SQL expert working with a PostgreSQL database called ClassicModels.

The database has the following tables and columns:

1. productlines(productLine, textDescription, htmlDescription, image)

2. products(productCode, productName, productLine, productScale, 
            productVendor, productDescription, quantityInStock, buyPrice, MSRP)

3. offices(officeCode, city, phone, addressLine1, addressLine2, 
           state, country, postalCode, territory)

4. employees(employeeNumber, lastName, firstName, extension, email, 
             officeCode, reportsTo, jobTitle)

5. customers(customerNumber, customerName, contactLastName, contactFirstName,
             phone, addressLine1, addressLine2, city, state, postalCode,
             country, salesRepEmployeeNumber, creditLimit)

6. payments(customerNumber, checkNumber, paymentDate, amount)

7. orders(orderNumber, orderDate, requiredDate, shippedDate, 
          status, comments, customerNumber)

8. orderdetails(orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)

Key Relationships:
- products.productLine → productlines.productLine
- employees.officeCode → offices.officeCode
- employees.reportsTo → employees.employeeNumber (self-join)
- customers.salesRepEmployeeNumber → employees.employeeNumber
- payments.customerNumber → customers.customerNumber
- orders.customerNumber → customers.customerNumber
- orderdetails.orderNumber → orders.orderNumber
- orderdetails.productCode → products.productCode

IMPORTANT RULES:
- All column names are case-sensitive and must be quoted with double quotes
- Example: "productName", "customerNumber", "orderDate"
- Only generate SELECT statements
- Never use DELETE, DROP, UPDATE, INSERT
"""

DECOMPOSITION_PROMPT = """
{schema}

Analyze this question and break it into structured components.

Question: {question}

Respond in exactly this format:
Intent: <what is being asked>
Tables: <comma separated table names>
Columns: <comma separated column names needed>
Filters: <any WHERE conditions or None>
Joins: <any JOIN conditions or None>
Aggregation: <any GROUP BY, COUNT, SUM, AVG, MAX, MIN or None>
"""

SQL_GENERATION_PROMPT = """
{schema}

Using this structured decomposition, generate a valid PostgreSQL SELECT query.

Decomposition:
{decomposition}

Original Question: {question}

Rules:
- Use double quotes around all column and table names
- Only generate a single SELECT statement
- Do not include any explanation
- Do not wrap in markdown code blocks
- Just return the raw SQL query
"""

SQL_FIX_PROMPT = """
{schema}

This SQL query failed with the following error:

SQL: {sql}
Error: {error}

Original Question: {question}

Please fix the SQL query and return only the corrected SQL.
Rules:
- Use double quotes around all column and table names
- Only return the raw SQL query
- No explanation, no markdown
"""