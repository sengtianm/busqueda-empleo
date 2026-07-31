---
name: project-architecture
description: Use this skill whenever implementing, modifying, reviewing, or refactoring code to ensure every change complies with the project's official architecture and design decisions.
---

# Purpose

This skill ensures that every implementation remains fully aligned with the project's approved architecture.

The project's architecture is the single source of truth for system organization, module responsibilities, dependencies, data flow, and implementation boundaries.

This skill prevents architectural drift during development.

---

# When to Use

Use this skill whenever:

- Implementing new functionality.
- Modifying existing functionality.
- Creating new modules.
- Refactoring code.
- Reviewing architecture compliance.
- Making design decisions.
- Integrating multiple modules.

Do not use this skill for debugging or code style reviews.

---

# Architecture Validation Workflow

Follow these steps before making architectural decisions.

## 1. Understand the requested change

Identify:

- Business objective.
- Scope.
- Modules involved.
- Expected behavior.

Never modify architecture without understanding the complete request.

---

## 2. Identify affected modules

Determine:

- Which module owns the responsibility.
- Which modules interact with it.
- Which interfaces are affected.

Never assign responsibilities to the wrong module.

---

## 3. Respect module boundaries

Every module must have a single responsibility.

Never:

- Duplicate responsibilities.
- Create circular dependencies.
- Couple unrelated modules.
- Bypass defined workflows.

---

## 4. Preserve the approved data flow

Follow the official processing flow.

Never:

- Skip processing stages.
- Merge independent stages.
- Reorder the workflow without approval.
- Introduce hidden execution paths.

---

## 5. Respect the technology stack

Use only the approved technologies.

Never replace or introduce technologies without explicit approval.

---

## 6. Minimize architectural impact

Prefer extending the existing architecture instead of redesigning it.

Architectural changes require explicit approval.

---

## 7. Validate consistency

Before finishing, verify:

- Module responsibilities remain clear.
- Dependencies remain correct.
- Naming remains consistent.
- Public interfaces remain compatible.
- Existing workflows remain intact.

---

# Mandatory Rules

Always:

- Treat the approved architecture as authoritative.
- Respect module ownership.
- Keep responsibilities isolated.
- Preserve loose coupling.
- Prefer consistency over novelty.
- Keep the system modular.

Never:

- Redesign the architecture.
- Introduce undocumented patterns.
- Create unnecessary abstractions.
- Duplicate logic between modules.
- Break module boundaries.
- Add hidden dependencies.
- Modify architectural decisions without approval.

---

# Expected Output

Every architectural review or implementation must include:

## Architecture Assessment

Overall compliance with the approved architecture.

## Affected Modules

List all impacted modules.

## Dependency Impact

Describe any dependency changes.

## Architectural Risks

Identify any risks introduced by the implementation.

## Compliance Status

State whether the implementation fully complies with the approved architecture.

If any architectural conflict exists, stop and request user approval before proceeding.