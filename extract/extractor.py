import os
import openai
import PyPDF2
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define JSON schema for contracts
JSON_SCHEMA = {
    "category": "",  # "loan_agreement" or "software_licensing"
    "financials": {
        "incoming": {},  # revenue, EMI, etc.
        "outgoing": {}   # license fee, support cost, loan amount etc.
    }
}

def read_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_financials_from_text(text: str, category: str) -> dict:
    """
    Send contract text to ChatGPT and extract financials in JSON format.
    """
    prompt = f"""
You are a contract analyzer. 
The contract category is: {category}.
Extract only the financial obligations into this JSON format:

{{
  "category": "{category}",
  "financials": {{
    "incoming": {{
        "example_key": "value"
    }},
    "outgoing": {{
        "example_key": "value"
    }}
  }}
}}

Incoming = money coming INTO the company (revenue, EMI received, interest).
Outgoing = money going OUT (loan amount given, license fee, support cost).

Make sure output is ONLY valid JSON, no explanation, no extra text.
Here is the contract text:
{text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    # Raw text from ChatGPT
    result = response["choices"][0]["message"]["content"]

    # Ensure it’s clean JSON
    try:
        import json
        financials = json.loads(result)
    except Exception:
        financials = {"error": "Invalid JSON returned"}
    
    return financials
