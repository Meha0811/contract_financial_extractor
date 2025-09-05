# src/db.py

import pymysql
import json
import os

# Get DB configs from environment variables (recommended)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "contracts_db")
DB_PORT = int(os.getenv("DB_PORT", 3306))


def get_connection(use_db=True):
    """Return a pymysql connection. If use_db is True, try to connect to DB_NAME.
    If DB doesn't exist, caller should call init_db() first.
    """
    if use_db:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    else:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )


def init_db():
    """Create the database and the `contract` table if they do not exist."""
    conn = get_connection(use_db=False)
    cur = conn.cursor()
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
    cur.close()
    conn.close()


def insert_contract(file_name: str, file_path: str, category: str, financials_json: dict):
    """Insert a single contract row."""
    conn = get_connection(use_db=True)
    cur = conn.cursor()
    sql = """
        INSERT INTO contract (file_name, file_path, category, financials_json)
        VALUES (%s, %s, %s, %s)
    """
    cur.execute(sql, (file_name, file_path, category, json.dumps(financials_json)))
    cur.close()
    conn.close()


def fetch_all_contracts():
    """Fetch all contract records."""
    conn = get_connection(use_db=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM contract ORDER BY contract_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
