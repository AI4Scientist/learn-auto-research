# Project 05 — Security Audit Pipeline

[中文版本 →](/zh/projects/project-05-security-audit-pipeline/)

**Paired with**: [Lecture 09](/en/lectures/lecture-09-stride-owasp-security/) + [Lecture 10](/en/lectures/lecture-10-twelve-dimension-scenarios/)  
**Starter code**: [projects/project-05/starter/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-05/starter/)  
**Solution**: [projects/project-05/solution/](https://github.com/AI4Scientist/learn-auto-research/tree/main/projects/project-05/solution/)

---

## What You'll Build

Run a complete security audit pipeline on a vulnerable web API: scenario exploration to find edge cases, security audit to identify vulnerabilities, and fix loop to remediate findings.

## Learning Objectives

- Generate comprehensive test scenarios across 12 dimensions
- Run STRIDE + OWASP security audit with code-level evidence
- Chain scenario → security → fix
- Interpret severity ratings and prioritize remediation

## Starting Point

```
projects/project-05/starter/
├── api/
│   ├── main.py          ← FastAPI app with intentional vulnerabilities
│   ├── auth.py          ← Authentication (has issues)
│   ├── users.py         ← User management (has issues)
│   └── items.py         ← Item CRUD (has issues)
├── tests/
└── requirements.txt
```

The API has 3–5 intentional vulnerabilities seeded across the codebase.

## Step 1 — Scenario Exploration

```bash
/autoresearch:scenario
Scenario: User authenticates and manages their items
Domain: security
Format: threat-scenarios
Iterations: 20
```

This generates 20 threat scenarios across all 12 dimensions. The output feeds into the security audit.

## Step 2 — Security Audit

```bash
/autoresearch:security
Iterations: 15
```

The audit runs STRIDE modeling, OWASP sweep, and 4 red-team personas. Every finding includes file:line evidence.

## Step 3 — Fix Critical/High Findings

```bash
/autoresearch:fix
Guard: python -m pytest tests/
```

Fix the Critical and High severity findings identified in the audit.

## Expected Audit Findings

The starter API contains:
- SQL injection in user search (Critical)
- Missing authorization check on item deletion (High)
- Sensitive data in error responses (Medium)

(More may be found depending on the depth of analysis.)

## Verification

```bash
# Re-run security audit on fixed code
/autoresearch:security --diff

# Should show: no Critical findings, no High findings
```
