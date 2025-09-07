# src/process_contracts.py
"""
Main script to process a folder of PDFs, call LLM to extract a JSON financial summary, and save into MySQL.
Usage:
    python -m src.process_contracts --folder ./contracts --model gpt-3.5-turbo-16k

Note: The script will use the filename to guess category ("loan" -> loan_agreement, "license"/"licensing"/"software" -> software_licensing).
"""
import argparse
import time
import json
from tqdm import tqdm

from src.pdf_text import extract_texts_from_folder
from src.openai_client import call_chatgpt_system_user, extract_json_from_response
from src.sample_prompt_templates import SYSTEM_PROMPT, LOAN_SCHEMA, SOFT_SCHEMA
from src.db import init_db, insert_contract


def build_user_prompt(contract_type: str, schema_example: str, contract_text: str) -> str:
    prompt = f"""Contract type: {contract_type}\n\nExpected JSON schema:\n{schema_example}\n\nExtract the financials from the following contract text. Return ONLY JSON that follows the schema. Use null when unavailable. If you find amounts in a currency write the currency in the 'currency' field.\n\n--- CONTRACT TEXT START ---\n{contract_text}\n--- CONTRACT TEXT END ---"""
    return prompt


def guess_category_from_filename(fname: str) -> str:
    lower = fname.lower()
    if "loan" in lower:
        return "loan_agreement"
    if "license" in lower or "licensing" in lower or "software" in lower:
        return "software_licensing"
    # fallback
    return "software_licensing"


def process_folder(folder_path: str, model_name: str = None):
    init_db()
    items = extract_texts_from_folder(folder_path)
    if not items:
        print("No PDFs found in the folder. Put them in the 'contracts' folder and try again.")
        return

    for fname, fpath, txt in tqdm(items, desc="Processing PDFs"):
        print(f"\n--- Processing: {fname} ---")
        if not txt or txt.strip() == "":
            print(f"Warning: no text extracted from {fname}. Skipping.")
            continue

        category = guess_category_from_filename(fname)
        schema = LOAN_SCHEMA if category == "loan_agreement" else SOFT_SCHEMA

        # Build prompt (truncate very long docs to avoid input size issues)
        CHUNK_SIZE = 30000
        contract_text = txt if len(txt) <= CHUNK_SIZE else txt[:CHUNK_SIZE]
        user_prompt = build_user_prompt(category, schema, contract_text)

        # Call LLM with fallback
        try:
            resp = call_chatgpt_system_user(SYSTEM_PROMPT, user_prompt, model=model_name)
            text = resp['choices'][0]['message']['content']
        except Exception as e:
            print(f"⚠️ OpenAI call failed: {e}")
            # --- MOCK FALLBACK JSON ---
            text = json.dumps({
                "contract_type": category,
                "summary": "Mock summary due to API quota issue.",
                "financials": {
                    "money_in": {"total_annually": 100000, "total_monthly": 8000, "items": []},
                    "money_out": {"total_annually": 50000, "total_monthly": 4000, "items": []},
                    "rates": {"interest_rate_percent": None, "service_fee_percent": None},
                    "currency": "INR"
                },
                "raw_extracted_fields": {"found_values": ["Mock values"]}
            })

        parsed = extract_json_from_response(text)
        if parsed is None:
            print("Could not parse JSON from response. Saving fallback structure with raw text snippet.")
            parsed = {
                "contract_type": category,
                "summary": None,
                "financials": {
                    "money_in": {"total_annually": None, "total_monthly": None, "items": []},
                    "money_out": {"total_annually": None, "total_monthly": None, "items": []},
                    "rates": {"interest_rate_percent": None, "service_fee_percent": None},
                    "currency": None,
                },
                "raw_extracted_fields": {"found_values": [text[:1000]]},
            }

        # Save
        insert_contract(fname, fpath, category, parsed)
        print(f"Saved contract '{fname}' as category '{category}'")
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Folder containing PDF contracts")
    parser.add_argument("--model", required=False, help="OpenAI model name (overrides env var)")
    args = parser.parse_args()
    process_folder(args.folder, model_name=args.model)
