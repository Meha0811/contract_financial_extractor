import os
import json
from db.db import get_connection
from extract.extractor import read_pdf, extract_financials_from_text

# Folder with contracts
CONTRACT_FOLDER = "data/"

# Map filenames to categories manually for now
CATEGORY_MAP = {
    "loan": "loan_agreement",
    "license": "software_licensing"
}

def get_category_from_filename(filename: str) -> str:
    for key, category in CATEGORY_MAP.items():
        if key in filename.lower():
            return category
    return "unknown"

def save_to_db(file_name, file_path, category, financials_json):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO contract_financials (file_name, file_path, category, financials_json)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (file_name, file_path, category, json.dumps(financials_json)))
        conn.commit()
    finally:
        conn.close()

def main():
    for file in os.listdir(CONTRACT_FOLDER):
        if file.endswith(".pdf"):
            file_path = os.path.join(CONTRACT_FOLDER, file)
            category = get_category_from_filename(file)

            print(f"Processing {file} ({category})...")
            text = read_pdf(file_path)
            financials = extract_financials_from_text(text, category)
            save_to_db(file, file_path, category, financials)

if __name__ == "__main__":
    main()
