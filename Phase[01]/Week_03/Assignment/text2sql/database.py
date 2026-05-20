import psycopg2  #type:ignore
from dotenv import load_dotenv   #type:ignore
import os

load_dotenv()

def get_connection():
    """Create and return a PostgreSQL connection."""
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return connection

def test_connection():
    """Test the database conenction"""
    try:
        connection = get_connection()
        cur = connection.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"Connected to PostgreSQL {version[0]}")
        cur.close()
        connection.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()

