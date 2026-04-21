# Lecture 09 — STRIDE+OWASP Security Audit

[中文版本 →](/zh/lectures/lecture-09-stride-owasp-security/)

Code examples: [code/](./code/)  
Practice project: [Project 05 — Security Audit Pipeline](/en/projects/project-05-security-audit-pipeline/)

---

Security audits are traditionally expensive, slow, and subjective. `/autoresearch:security` makes them autonomous, evidence-based, and repeatable. Every finding requires code-level evidence — file, line, attack scenario, and proof of exploitability.

## STRIDE Threat Modeling

STRIDE is a systematic framework for categorizing threats. Before auditing specific vulnerabilities, the agent maps the codebase against all six STRIDE categories:

| Letter | Threat | Example |
|--------|--------|---------|
| **S**poofing | Attacker impersonates another entity | JWT without signature verification |
| **T**ampering | Attacker modifies data or code | Unsigned API responses, CSRF |
| **R**epudiation | User denies performing an action | Missing audit logs for sensitive operations |
| **I**nformation Disclosure | Sensitive data exposed | Stack traces in 500 responses, over-fetching |
| **D**enial of Service | Attacker makes service unavailable | Unbounded loops, missing rate limiting |
| **E**levation of Privilege | Attacker gains higher permissions | IDOR, missing authorization checks |

The STRIDE sweep produces an **asset inventory** (what data and capabilities exist) and a **trust boundary map** (where trust transitions occur). These become the basis for targeted OWASP scanning.

## OWASP Top 10 Sweep

After STRIDE mapping, the agent runs a systematic sweep against the OWASP Top 10:

1. **Broken Access Control** — missing authorization, IDOR, path traversal
2. **Cryptographic Failures** — weak algorithms, unencrypted data at rest/transit
3. **Injection** — SQL, NoSQL, command, LDAP injection
4. **Insecure Design** — missing rate limiting, insecure direct references
5. **Security Misconfiguration** — default credentials, verbose error messages
6. **Vulnerable Components** — outdated dependencies with known CVEs
7. **Authentication Failures** — weak passwords, session fixation, missing MFA
8. **Software Integrity Failures** — missing integrity checks, insecure deserialization
9. **Logging Failures** — missing security event logging, log injection
10. **SSRF** — server-side request forgery, unvalidated redirects

Each OWASP category maps to specific code patterns the agent searches for.

## Evidence Requirements

Every finding in the audit report must include:

1. **File and line**: exact location in the codebase (`src/api/users.ts:47`)
2. **Attack scenario**: a specific, concrete attack ("An attacker sends a request with `userId=1` to access another user's data")
3. **Proof**: why this is actually exploitable, not just a theoretical concern
4. **Severity**: Critical / High / Medium / Low (using CVSS-like criteria)
5. **Remediation**: specific code change to fix it

No theoretical fluff. If a finding can't be backed by code evidence and a concrete attack scenario, it doesn't appear in the report.

## The Four Red Team Personas

After STRIDE + OWASP, the agent runs adversarial analysis with four hostile personas:

**Opportunist**: Looks for easy wins — default credentials, exposed admin endpoints, public API keys in source code. Low effort, high impact.

**Insider Threat**: Assumes the attacker has read access to the codebase. What can a malicious employee or contractor do?

**Nation-State Actor**: Looks for subtle, long-term compromises. Supply chain attacks, backdoors in dependencies, timing attacks.

**Script Kiddie**: Tests known exploit patterns against common frameworks. CVEs in dependencies, known misconfiguration patterns.

Each persona's findings are merged and deduplicated into the final report.

## Output: 7 Structured Files

Results go in `security/{date}-{slug}/`:

| File | Contents |
|------|----------|
| `threat-model.md` | STRIDE analysis, asset inventory, trust boundaries |
| `findings.md` | All findings with code evidence (Critical/High/Medium/Low) |
| `attack-surface.md` | Enumerated attack surface with entry points |
| `red-team.md` | Findings from the 4 adversarial personas |
| `remediation.md` | Prioritized fix list with specific code changes |
| `summary.md` | Executive summary: finding counts by severity, top 3 risks |
| `security-results.tsv` | Machine-readable findings for CI/CD integration |

## CI/CD Integration

```bash
/autoresearch:security --fail-on High
```

Exit code 1 if any High or Critical findings are found. Use as a CI gate:

```yaml
- name: Security audit
  run: claude -p "/autoresearch:security --fail-on High --diff"
```

`--diff` audits only files changed since the last audit — fast incremental mode for CI.

`--fix` auto-remediates confirmed Critical/High findings. Only confirmed findings (not theoretical) are auto-fixed.

## Key Takeaways

- STRIDE provides systematic threat categorization before diving into specific vulnerabilities
- OWASP Top 10 sweep gives structured coverage of the most common vulnerability classes
- Every finding requires code evidence (file:line + attack scenario) — no theoretical speculation
- Four red team personas provide diverse attack perspectives
- 7 structured output files cover the full audit lifecycle from threat model to remediation
- CI/CD integration with `--fail-on` and `--diff` makes security a continuous process

---

**Next**: [Lecture 10 — 12-Dimension Scenario Exploration](/en/lectures/lecture-10-twelve-dimension-scenarios/)
