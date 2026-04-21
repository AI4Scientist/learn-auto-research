"""Correctness tests for app.py — do not modify."""
from app import parse_request, process_payment, handle

def test_parse_normal():
    r = parse_request({"user_id": "u1", "amount": "9.99", "items": ["a"]})
    assert r["user_id"] == "u1"
    assert r["amount"] == 9.99
    assert r["items"] == ["a"]

def test_parse_missing_items_returns_list():
    r = parse_request({"user_id": "u1", "amount": "5.00"})
    assert r["items"] == [], f"expected [], got {r['items']}"

def test_parse_missing_user_id_returns_default():
    r = parse_request({"amount": "5.00"})
    assert r["user_id"] == "anonymous"

def test_parse_negative_amount_raises():
    try:
        parse_request({"user_id": "u1", "amount": "-1.00"})
        assert False, "should have raised"
    except ValueError:
        pass

def test_process_ok():
    assert process_payment({"amount": 10.0})["status"] == "ok"

def test_handle_full():
    r = handle({"user_id": "u1", "amount": "20.00"})
    assert r["status"] == "ok"
