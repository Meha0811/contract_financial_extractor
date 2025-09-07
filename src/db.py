# src/db.py

import pymysql
import json
import os

# Get DB configs from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "contract_db")   # ✅ keep consistent
DB_PORT = int(os.getenv("DB_PORT", 3306))


def get_connection(use_db=True):
    """Return a pymysql connection. If use_db is True, connect to DB_NAME."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME if use_db else None,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def init_db():
    """Create the database and the `contract` table if they do not exist."""
    conn = get_connection(use_db=False)
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`;")
        cur.execute(f"USE `{DB_NAME}`;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contract (
                contract_id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                file_path VARCHAR(1024) NOT NULL,
                category VARCHAR(64) NOT NULL,
                financials_json JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.close()


def insert_contract(file_name: str, file_path: str, category: str, financials_json: dict | None):
    """Insert a single contract row safely."""
    try:
        # normalize category
        category = category.lower().replace(" ", "_")

        conn = get_connection(use_db=True)
        with conn.cursor() as cur:
            sql = """
                INSERT INTO contract (file_name, file_path, category, financials_json)
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(sql, (
                file_name,
                file_path,
                category,
                json.dumps(financials_json) if financials_json is not None else None
            ))
    except Exception as e:
        print(f"[DB ERROR] insert_contract failed: {e}")
    finally:
        conn.close()


def fetch_all_contracts():
    """Fetch all contract records."""
    try:
        conn = get_connection(use_db=True)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM contract ORDER BY contract_id")
            rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"[DB ERROR] fetch_all_contracts failed: {e}")
        return []
    finally:
        conn.close()
