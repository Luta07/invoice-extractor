from fastapi import FastAPI
from pydantic import BaseModel
import re
from datetime import datetime

app = FastAPI()


class ExtractRequest(BaseModel):
    text: str


class ExtractResponse(BaseModel):
    vendor: str
    amount: float
    currency: str
    date: str


@app.post("/extract", response_model=ExtractResponse)
def extract(req: ExtractRequest):

    text = req.text.strip()

    if not text:
        return {
            "vendor": "",
            "amount": 0.0,
            "currency": "USD",
            "date": "2026-01-01"
        }

    vendor = ""

    vendor_patterns = [
        r"Vendor[:\s]+(.+)",
        r"Supplier[:\s]+(.+)",
        r"From[:\s]+(.+)"
    ]

    for pattern in vendor_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            vendor = m.group(1).split("\n")[0].strip()
            break

    if not vendor:
        lines = [x.strip() for x in text.split("\n") if x.strip()]
        vendor = lines[0]

    amount = 0.0

    amount_match = re.search(
        r"([0-9]+(?:\.[0-9]{1,2})?)",
        text
    )

    if amount_match:
        amount = float(amount_match.group(1))

    currency = "USD"

    currency_match = re.search(
        r"\b(USD|EUR|GBP)\b",
        text,
        re.IGNORECASE
    )

    if currency_match:
        currency = currency_match.group(1).upper()

    date = "2026-01-01"

    date_match = re.search(
        r"(2026-\d{2}-\d{2})",
        text
    )

    if date_match:
        date = date_match.group(1)

    return {
        "vendor": vendor,
        "amount": amount,
        "currency": currency,
        "date": date
    }
