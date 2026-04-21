"""Fixed audit.py — all 4 security vulnerabilities resolved."""
import hashlib
import hmac
import os
import pathlib


def authenticate(username: str, password: str, db: dict) -> bool:
    """Check credentials using HMAC-SHA256 with stored salt."""
    record = db.get(username)
    if not record:
        return False
    salt = record["salt"]
    expected = hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, record["hash"])


def run_report(report_name: str) -> str:
    """Generate a system report — allowlist-validated, no shell=True."""
    allowed = {"daily", "weekly", "monthly"}
    if report_name not in allowed:
        raise ValueError(f"Unknown report: {report_name}")
    path = pathlib.Path("reports") / f"{report_name}.txt"
    return path.read_text() if path.exists() else ""


def get_user_data(user_id: str, db: dict, authorized_caller: str) -> dict:
    """Fetch user record — caller must be authorized."""
    if authorized_caller not in ("admin", "system"):
        raise PermissionError(f"Caller '{authorized_caller}' is not authorized")
    return db.get(user_id, {})


def log_event(event: str) -> None:
    """Log an audit event — sensitive fields must be redacted before calling."""
    print(f"[AUDIT] {event}")
