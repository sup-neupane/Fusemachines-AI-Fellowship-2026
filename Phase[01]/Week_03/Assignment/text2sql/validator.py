import re

# Blocked SQL keywords - only SELECT is allowed
BLOCKED_KEYWORDS = [
    "DELETE", "DROP", "UPDATE", "INSERT",
    "TRUNCATE", "ALTER", "CREATE", "REPLACE",
    "GRANT", "REVOKE", "EXEC", "EXECUTE"
]

def validate_sql(sql: str) -> dict:
    """
    Validate the generated SQL query.
    Returns a dict with is_valid flag and reason.
    """
    if not sql:
        return {
            "is_valid": False,
            "reason": "Empty SQL query generated"
        }

    # Convert to uppercase for keyword checking
    sql_upper = sql.upper().strip()

    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return {
            "is_valid": False,
            "reason": f"Query must start with SELECT. Got: {sql[:50]}"
        }

    # Check for blocked keywords
    for keyword in BLOCKED_KEYWORDS:
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, sql_upper):
            return {
                "is_valid": False,
                "reason": f"Blocked keyword detected: {keyword}"
            }

    # Check for multiple statements
    if sql.count(";") > 1:
        return {
            "is_valid": False,
            "reason": "Multiple SQL statements detected"
        }

    return {
        "is_valid": True,
        "reason": "SQL is valid"
    }


def clean_sql(sql: str) -> str:
    """
    Clean the SQL query returned by the LLM.
    Removes markdown formatting if present.
    """
    # Remove markdown code blocks
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)

    # Remove leading/trailing whitespace
    sql = sql.strip()

    # Ensure it ends with semicolon
    if not sql.endswith(";"):
        sql = sql + ";"

    return sql



if __name__ == "__main__":
    test_queries = [
        'SELECT * FROM customers;',
        'DELETE FROM customers;',
        'SELECT * FROM orders; DROP TABLE orders;',
        'UPDATE products SET price = 0;',
        '',
    ]

    for q in test_queries:
        result = validate_sql(q)
        print(f"Query: {q[:40]}")
        print(f"Valid: {result['is_valid']} | Reason: {result['reason']}")
        print("---")