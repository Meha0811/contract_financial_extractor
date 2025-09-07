SYSTEM_PROMPT = (
    "You are an automated contract parser. ONLY return valid JSON that matches the requested schema.\n"
    "Do not add any explanation, commentary, or code fences.\n"
    "If a field is unavailable, return null.\n"
    "Use numeric values for amounts and percentages.\n"
    "If currency is not explicit, set currency to 'unknown'."
)

# Example JSON schema for a loan agreement
LOAN_SCHEMA = """
{
  "contract_type": "loan_agreement",
  "summary": null,
  "financials": {
    "money_in": {
      "total_annually": null,
      "total_monthly": null,
      "items": [
        {
          "label": null,
          "amount_monthly": null,
          "amount_annually": null,
          "notes": null
        }
      ]
    },
    "money_out": {
      "total_annually": null,
      "total_monthly": null,
      "items": [
        {
          "label": null,
          "amount": null,
          "notes": null
        }
      ]
    },
    "rates": {
      "interest_rate_percent": null,
      "service_fee_percent": null
    },
    "currency": null
  },
  "raw_extracted_fields": {
    "found_values": []
  }
}
"""

# Example JSON schema for a software licensing contract
SOFT_SCHEMA = """
{
  "contract_type": "software_licensing",
  "summary": null,
  "financials": {
    "money_in": {
      "total_annually": null,
      "total_monthly": null,
      "items": [
        {
          "label": "license_fee",
          "amount_monthly": null,
          "amount_annually": null,
          "notes": null
        }
      ]
    },
    "money_out": {
      "total_annually": null,
      "total_monthly": null,
      "items": [
        {
          "label": "support_cost_monthly",
          "amount": null,
          "notes": null
        }
      ]
    },
    "rates": {
      "interest_rate_percent": null,
      "service_fee_percent": null
    },
    "currency": null
  },
  "raw_extracted_fields": {
    "found_values": []
  }
}
"""
