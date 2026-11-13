"""Field-level post-processing for Marrowfield OCR output."""

import re
from typing import Dict

_DATE_RE = re.compile(r"(\d{2})[/-](\d{2})[/-](\d{4})")
_AMOUNT_RE = re.compile(r"\$?\s*([0-9][0-9,]*\.?[0-9]{0,2})")


def normalize_date(text: str) -> str:
    match = _DATE_RE.search(text)
    if not match:
        return text.strip()
    day, month, year = match.groups()
    return f"{year}-{month}-{day}"


def extract_amount(text: str) -> float:
    match = _AMOUNT_RE.search(text.replace(",", ""))
    return float(match.group(1)) if match else 0.0


def extract_fields(lines) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for line in lines:
        lowered = line.text.lower()
        if "date" in lowered:
            fields["date"] = normalize_date(line.text)
        elif "total" in lowered:
            fields["total"] = f"{extract_amount(line.text):.2f}"
    return fields
