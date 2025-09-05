# src/sample_prompt_templates.py
"""
Schema examples and system prompt used to instruct the LLM to return strict JSON.
"""

SYSTEM_PROMPT = (
    "You are an automated contract parser. ONLY return valid JSON that matches the requested schema.\n"
    "Do not add any explanation, commentary, or code fences. "
    "If a field is unavailable, return null. "
    "Prefer numeric values where appropriate. "
    "If currency is not explicit, set currency to 'unknown'."
)

# Example JSON schema for a loan agreement
LOAN_SCHEMA = """
{
  "contract_type": "loan_agreement",
  "summary": "short text",
  "financials": {
    "money_in": {
      "total_annually": number,
      "total_monthly": number,
      "items": [
        {
          "label": "",
          "amount_monthly": number,
          "amount_annually": number,
          "notes": ""
        }
      ]
    },
    "money_out": {
      "total_annually": number,
      "total_monthly": number,
      "items": [
        {
          "label": "",
          "amount": number,
          "notes": ""
        }
      ]
    },
    "rates": {
      "interest_rate_percent": number,
      "service_fee_percent": null
    },
    "currency": "INR"
  },
  "raw_extracted_fields": {
    "found_values": ["..."]
  }
}
"""

# Example JSON schema for a software licensing contract
SOFT_SCHEMA = """
{
  "contract_type": "software_licensing",
  "summary": "short text",
  "financials": {
    "money_in": {
      "total_annually": number,
      "total_monthly": number,
      "items": [
        {
          "label": "license_fee",
          "amount_monthly": null,
          "amount_annually": number,
          "notes": ""
        }
      ]
    },
    "money_out": {
      "total_annually": number,
      "total_monthly": number,
      "items": [
        {
          "label": "support_cost_monthly",
          "amount": number,
          "notes": ""
        }
      ]
    },
    "rates": {
      "interest_rate_percent": null,
      "service_fee_percent": number
    },
    "currency": "INR"
  },
  "raw_extracted_fields": {
    "found_values": ["..."]
  }
}
"""
