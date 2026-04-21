# Lecture 09 — STRIDE+OWASP Security Audit

`L01 > L02 > L03 > L04 > L05 > L06 | L07 > L08 > [ L09 ] L10 > L11 > L12`

> *"Every finding must have code-level evidence."* — No theoretical fluff. File, line, attack scenario, proof of exploitability — or it doesn't appear in the report.
>
> **Core idea**: How `/autoresearch:security` makes security audits autonomous and evidence-based — STRIDE threat modeling, OWASP sweep, four red-team personas, and 7 structured output files.

Code examples: [code/](./code/)  
Practice project: [Project 05 — Security Audit Pipeline](/en/projects/project-05-security-audit-pipeline/)

[中文版本 →](/zh/lectures/lecture-09-stride-owasp-security/)

---

## The Problem

Traditional security audits are slow, expensive, and subjective. Findings are often theoretical ("an attacker could potentially...") with no code evidence. The same vulnerabilities appear in audit after audit because there's no systematic sweep.

## The Solution

```
Phase 1: STRIDE sweep
  Map every asset and trust boundary against 6 threat categories
  → asset inventory + trust boundary map

Phase 2: OWASP Top 10 sweep
  Search codebase for patterns of the 10 most common vulnerability classes
  → pattern matches with file:line evidence

Phase 3: Four red-team personas
  Opportunist / Insider Threat / Nation-State / Script Kiddie
  → adversarial findings from 4 attack angles

Phase 4: Output 7 structured files
  findings.md   ← every finding with code evidence
  remediation.md ← prioritized fix list
  security-results.tsv ← CI/CD integration
  + 4 more files
```

Every finding requires: file and line, attack scenario, proof of exploitability, severity, and remediation. No finding appears in the report without all five.

## How It Works

**1. STRIDE threat modeling first.**

Before auditing specific vulnerabilities, map the codebase against six categories:

| Letter | Threat | Classic example |
|---|---|---|
| **S**poofing | Impersonation | JWT without signature verification |
| **T**ampering | Data modification | Unsigned API responses, CSRF |
| **R**epudiation | Deny performing action | Missing audit logs for sensitive ops |
| **I**nformation Disclosure | Sensitive data exposed | Stack traces in 500 responses |
| **D**enial of Service | Make service unavailable | Unbounded loops, no rate limiting |
| **E**levation of Privilege | Gain higher permissions | IDOR, missing authorization checks |

STRIDE produces an asset inventory and trust boundary map — the basis for targeted OWASP scanning.

**2. OWASP Top 10 sweep.**

After STRIDE, systematic sweep against all 10 vulnerability classes — each maps to specific code patterns the agent searches for in the codebase.

**3. Four red-team personas.**

| Persona | Attack angle |
|---|---|
| **Opportunist** | Easy wins: default credentials, exposed admin endpoints, API keys in source |
| **Insider Threat** | Attacker has read access — what can a malicious contractor do? |
| **Nation-State** | Subtle long-term compromise: supply chain, backdoors, timing attacks |
| **Script Kiddie** | Known exploit patterns, CVEs in dependencies, common misconfigurations |

**4. CI/CD integration.**

```bash
/autoresearch:security --fail-on High
```

Exit code 1 if any High or Critical findings exist. Use as a CI gate:

```yaml
- name: Security audit
  run: claude -p "/autoresearch:security --fail-on High --diff"
```

`--diff` audits only files changed since the last audit — fast incremental mode for CI.

## What Changed

| Ad-hoc security review | STRIDE+OWASP audit |
|---|---|
| "Looks secure" with no evidence | Every finding requires file:line + attack scenario |
| Reviews whatever comes to mind | Systematic STRIDE + OWASP coverage |
| Single reviewer's blind spots | Four adversarial personas with different attack angles |
| One-time manual process | CI gate with `--fail-on` and `--diff` |

## Try It

Run the STRIDE matrix and OWASP checklist:

```sh
cd docs/en/lectures/lecture-09-stride-owasp-security/code
python stride_matrix.py
python owasp_checklist.py
```

Questions to think about:

1. In `stride_matrix.py`, which STRIDE category has the most findings in the sample? Why is that category often the most overlooked?
2. In `owasp_checklist.py`, what does the `"patterns"` field contain? How does this make findings grep-able?
3. The Insider Threat persona assumes the attacker has read access to the codebase. What findings does this persona catch that an external attacker wouldn't?
4. Take one endpoint from a project you've built — run through all six STRIDE categories manually and write one finding per category (even if it's "no threat found").

---

**Next**: [Lecture 10 — 12-Dimension Scenario Exploration](/en/lectures/lecture-10-twelve-dimension-scenarios/)
