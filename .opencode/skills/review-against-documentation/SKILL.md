---
name: review-against-documentation
description: Use this skill whenever reviewing an implementation against the project's official documentation, architecture, requirements, backlog, or design decisions.
---

# Purpose

This skill verifies that an implementation matches the project's official documentation instead of only checking code quality.

The goal is to detect inconsistencies between the implementation and the documented requirements.

---

# When to Use

Use this skill whenever:

- Reviewing completed work.
- Validating a finished implementation.
- Comparing code against project documentation.
- Verifying compliance with architectural decisions.
- Checking implementation against backlog tasks.

Do not use this skill for debugging or implementation.

---

# Review Workflow

Follow these steps.

## 1. Identify the implementation

Determine:

- Files involved.
- Modules involved.
- Scope of the implementation.

---

## 2. Identify the applicable documentation

Locate every relevant document.

Examples include:

- Architecture
- Data model
- Workflow
- Technical standards
- Design decisions
- Backlog

Do not ignore relevant documentation.

---

## 3. Compare implementation against documentation

Verify:

- Functional behavior.
- Business rules.
- Module responsibilities.
- Interfaces.
- Naming.
- Expected workflow.
- Constraints.

---

## 4. Detect inconsistencies

Identify:

- Missing functionality.
- Extra functionality.
- Architecture violations.
- Incorrect assumptions.
- Documentation mismatches.

Do not suggest undocumented improvements.

---

## 5. Produce the review

Separate findings into:

### Compliant

Items correctly implemented.

### Non-compliant

Items that violate documentation.

### Missing

Requirements not implemented.

### Risks

Potential future issues.

---

# Mandatory Rules

Always:

- Treat documentation as the source of truth.
- Explain every finding.
- Reference the document that supports each finding.
- Distinguish facts from assumptions.

Never:

- Invent requirements.
- Recommend undocumented changes.
- Ignore architectural decisions.
- Assume undocumented behavior.

---

# Expected Output

Every review must include:

## Summary

Overall compliance.

## Findings

Detailed list.

## Documentation References

Documents supporting each finding.

## Required Corrections

Only corrections justified by documentation.

Wait for user approval before proposing implementation changes.