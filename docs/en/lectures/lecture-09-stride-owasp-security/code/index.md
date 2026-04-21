# L09 Code — STRIDE+OWASP Security Audit

> **Goal**: Generate a STRIDE threat matrix for any component, then run the OWASP Top-10 checklist and see which items pass, fail, or need review.

Run it:

```sh
cd docs/en/lectures/lecture-09-stride-owasp-security/code
python stride_matrix.py "REST API gateway"
python owasp_checklist.py
```

---

## Tool 1: STRIDE Threat Matrix Generator

### Step 1: Define the six STRIDE categories

```python
import sys, textwrap

STRIDE = [
    {
        "letter": "S", "threat": "Spoofing",
        "description": "Attacker impersonates a legitimate user or component.",
        "questions": [
            "Can an attacker forge identity tokens or session cookies?",
            "Is mutual TLS or strong auth enforced on all endpoints?",
        ],
        "mitigations": ["Strong authentication (MFA, JWT signing)", "Certificate pinning"],
    },
    # ... T, R, I, D, E follow the same structure
]
```

**Key line**: Each STRIDE entry has `questions` (what to ask about this component) and `mitigations` (what to do if the threat is real). The questions are generic — they apply to any component you pass in.

---

### Step 2: Generate and print the threat matrix

```python
def generate(component: str) -> None:
    print(f"STRIDE Threat Matrix — Component: {component}")
    for item in STRIDE:
        print(f"\n[{item['letter']}] {item['threat']}")
        print(f"    {item['description']}")
        print(f"\n    Threat questions for '{component}':")
        for q in item["questions"]:
            print(f"      • {textwrap.fill(q, 66, subsequent_indent='        ')}")
        print(f"\n    Mitigations:")
        for m in item["mitigations"]:
            print(f"      ✓ {m}")
    print("\nAction: Rate residual risk (low/medium/high) for each category.")
    print("        Create a ticket for any 'high' item before shipping.")
```

**Key line**: `textwrap.fill(q, 66, ...)` — wraps long questions to fit terminal width. The output is designed to be printed and used as a checklist in a meeting or code review.

---

## Tool 2: OWASP Top-10 Checklist Formatter

### Step 3: Define the checklist with pass/fail status

```python
OWASP_TOP_10 = [
    ("A01", "Broken Access Control",
     "Every request checks authorisation; no IDOR paths exposed."),
    ("A02", "Cryptographic Failures",
     "Secrets in env vars; TLS 1.2+ everywhere; no MD5/SHA-1 for passwords."),
    # ... A03-A10
]

STATUS = {
    "A01": "pass",
    "A02": "partial",
    "A05": "fail",
    "A09": "fail",
    # ...
}
```

**Key line**: The `STATUS` dict is what you edit — not the checklist itself. Fill it in during your audit. `"partial"` means the control exists but has gaps; `"fail"` means it's missing entirely.

---

### Step 4: Print results and flag failures

```python
ICONS = {"pass": "[PASS]", "fail": "[FAIL]", "partial": "[PART]", "n/a": "[ -- ]"}

def main():
    fails = []
    for code, name, check in OWASP_TOP_10:
        status = STATUS.get(code, "?")
        icon   = ICONS.get(status, "[????]")
        print(f"{code:<5} {icon:<8} {name:<40} {check}")
        if status == "fail":
            fails.append((code, name))

    if fails:
        print(f"[ACTION REQUIRED] {len(fails)} failing item(s):")
        for code, name in fails:
            print(f"  {code} — {name}")
```

**Key line**: `"patterns"` field (in `stride_matrix.py`) and the `check` description here are designed to be grep-able — copy the check text into a code search to find matching patterns in your codebase.

---

## Try Changing It

1. Run `stride_matrix.py "user authentication service"` — which STRIDE category has the most relevant questions for an auth service?
2. In `owasp_checklist.py`, change `STATUS["A05"]` from `"fail"` to `"pass"` — how does the output change?
3. The Insider Threat persona from the lecture "assumes the attacker has read access to the codebase." Which STRIDE category maps most directly to insider threats?
4. Take one endpoint from a project you've built — fill in `STATUS` for all 10 OWASP categories based on your actual knowledge of that endpoint.
