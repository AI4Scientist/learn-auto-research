"""
Starter: broken FastAPI-style request handler.
Contains 3 intentional bugs for the debugging project.
"""

def parse_request(raw: dict) -> dict:
    """Parse incoming API request. Has bugs."""
    user_id = raw["user_id"]          # bug 1: no default / KeyError on missing key
    amount  = float(raw["amount"])    # bug 2: no validation — accepts negative amounts
    items   = raw.get("items", None)  # bug 3: returns None instead of []
    return {"user_id": user_id, "amount": amount, "items": items}


def process_payment(request: dict) -> dict:
    """Process a payment request."""
    if request["amount"] <= 0:
        return {"status": "error", "message": "invalid amount"}
    return {"status": "ok", "charged": request["amount"]}


def handle(raw: dict) -> dict:
    req = parse_request(raw)
    return process_payment(req)
