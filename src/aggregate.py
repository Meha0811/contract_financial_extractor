# src/aggregate.py
"""
Read all rows from contract table, parse financials_json and compute totals per category and overall.
Run after `process_contracts.py` has populated the DB.
"""
import json
from collections import defaultdict
from src.db import fetch_all_contracts
from src.utils import safe_parse_number


def sum_financials(rows):
    by_category = defaultdict(lambda: {"money_in_annual": 0.0, "money_out_annual": 0.0})
    overall = {"money_in_annual": 0.0, "money_out_annual": 0.0}

    for r in rows:
        cat = r.get('category', 'unknown')
        fj = r.get('financials_json')
        if isinstance(fj, str):
            try:
                fj = json.loads(fj)
            except Exception:
                fj = None
        if not fj:
            continue
        # safe extraction
        fin = fj.get('financials', {})
        money_in = fin.get('money_in', {})
        money_out = fin.get('money_out', {})
        in_ann = safe_parse_number(money_in.get('total_annually')) or 0.0
        out_ann = safe_parse_number(money_out.get('total_annually')) or 0.0
        by_category[cat]['money_in_annual'] += in_ann
        by_category[cat]['money_out_annual'] += out_ann
        overall['money_in_annual'] += in_ann
        overall['money_out_annual'] += out_ann

    return by_category, overall


if __name__ == '__main__':
    rows = fetch_all_contracts()
    by_cat, overall = sum_financials(rows)
    print("\n=== Totals by category (annual) ===")
    for c, vals in by_cat.items():
        print(f"{c}: money_in_annual = {vals['money_in_annual']}, money_out_annual = {vals['money_out_annual']}")
    print("\n=== Overall totals (annual) ===")
    print(f"money_in_annual = {overall['money_in_annual']}")
    print(f"money_out_annual = {overall['money_out_annual']}")
