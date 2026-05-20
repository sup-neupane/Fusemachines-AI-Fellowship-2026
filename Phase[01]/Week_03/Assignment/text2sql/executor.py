import json
import os
from datetime import datetime
from database import get_connection
from validator import validate_sql, clean_sql

LOG_FILE = "logs/query_log.json"

def load_logs():
    """Load existing logs from file."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_log(log_entry: dict):
    """Append a log entry to the log file."""
    logs = load_logs()
    logs.append(log_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2, default=str)

def execute_sql(sql: str, question: str, retry_count: int = 0) -> dict:
    """
    Execute a SQL query against PostgreSQL.
    Returns a structured result dict.
    """
    # Clean the SQL first
    sql = clean_sql(sql)

    # Validate before executing
    validation = validate_sql(sql)
    if not validation["is_valid"]:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "sql": sql,
            "status": "blocked",
            "error": validation["reason"],
            "retry_count": retry_count,
            "result": []
        }
        save_log(log_entry)
        return log_entry

    # Execute the query
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)

        # Fetch results
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        # Convert to list of dicts
        result = [dict(zip(columns, row)) for row in rows]

        cur.close()
        conn.close()

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "sql": sql,
            "status": "success",
            "error": None,
            "retry_count": retry_count,
            "result": result[:5]  # Log first 5 rows only
        }
        save_log(log_entry)
        return log_entry

    except Exception as e:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "sql": sql,
            "status": "failed",
            "error": str(e),
            "retry_count": retry_count,
            "result": []
        }
        save_log(log_entry)
        return log_entry


if __name__ == "__main__":
    result = execute_sql(
        'SELECT "customerName", "city" FROM customers LIMIT 3;',
        "Get customer names and cities"
    )
    print(f"Status : {result['status']}")
    print(f"Error  : {result['error']}")
    print(f"Results: {result['result']}")