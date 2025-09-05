# src/utils.py
import re
from typing import Optional


def safe_parse_number(value) -> Optional[float]:
    """
    Try to convert a string like 'INR 1,23,456.78' or '1,234.56' or '12%' to a float.
    Returns None if not possible.
    """
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    if s == "":
        return None

    # Handle percentages
    is_percent = False
    if s.endswith("%"):
        is_percent = True
        s = s[:-1]

    # Remove currency symbols and commas
    s = re.sub(r"[£$€,₹]", "", s)
    s = s.replace(",", "")

    # Extract numeric part
    m = re.search(r"-?[0-9]+(\.[0-9]+)?", s)
    if not m:
        return None

    try:
        num = float(m.group(0))
        # Keep percentages as numeric (not divided by 100 — so 12% → 12.0)
        return num if is_percent else num
    except Exception:
        return None
