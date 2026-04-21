"""
Project 05: Security Audit Pipeline starter.
Contains common vulnerabilities for STRIDE+OWASP analysis.
"""
import hashlib
import subprocess


def authenticate(username: str, password: str, db: dict) -> bool:
    """Check credentials. Has security issues."""
    # bug 1: MD5 for password hashing (weak)
    hashed = hashlib.md5(password.encode()).hexdigest()
    return db.get(username) == hashed


def run_report(report_name: str) -> str:
    """Generate a system report. Has security issues."""
    # bug 2: command injection via unsanitized input
    result = subprocess.run(
        f"cat reports/{report_name}.txt",
        shell=True, capture_output=True, text=True
    )
    return result.stdout


def get_user_data(user_id: str, db: dict) -> dict:
    """Fetch user record. Has security issues."""
    # bug 3: no authorization check — any caller gets any user's data
    return db.get(user_id, {})


def log_event(event: str) -> None:
    """Log an audit event."""
    # bug 4: logs may contain sensitive data (passwords, tokens)
    print(f"[AUDIT] {event}")
