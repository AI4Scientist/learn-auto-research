"""Fixed app.py — all 3 bugs resolved."""

def parse_request(raw: dict) -> dict:
    user_id = raw.get("user_id", "anonymous")
    amount  = float(raw["amount"])
    if amount < 0:
        raise ValueError(f"amount must be non-negative, got {amount}")
    items   = raw.get("items", [])
    return {"user_id": user_id, "amount": amount, "items": items}


def process_payment(request: dict) -> dict:
    if request["amount"] <= 0:
        return {"status": "error", "message": "invalid amount"}
    return {"status": "ok", "charged": request["amount"]}


def handle(raw: dict) -> dict:
    req = parse_request(raw)
    return process_payment(req)
