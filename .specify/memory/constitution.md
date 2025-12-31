<!-- Sync Impact Report:
Version change: N/A (initial version) → 1.0.0
List of modified principles: N/A (initial creation)
Added sections: All principles and sections based on user requirements
Removed sections: N/A
Templates requiring updates:
- ✅ .specify/templates/plan-template.md: Constitution Check section should reference spec-first development and clean architecture principles
- ⚠ .specify/templates/spec-template.md: May need alignment for spec-driven requirements
- ⚠ .specify/templates/tasks-template.md: May need alignment for task organization based on principles
Follow-up TODOs:
- TODO(RATIFICATION_DATE): Need to set original adoption date
- TODO(LAST_AMENDED_DATE): Update when constitution is amended
-->
# In-Memory Todo CLI Application Constitution

## Core Principles

### Spec-First Development
No code is written without an approved specification. All features must originate from a written specification, and implementation must strictly follow the latest approved spec. If ambiguity exists, clarify via specification updates before coding.

### Deterministic Behavior
CLI actions must produce predictable, testable results. All functionality must be deterministic and verifiable through clear acceptance criteria.

### Simplicity Over Complexity
Focus on simplicity with in-memory only storage and no persistence layer. Avoid premature abstractions and unnecessary complexity. Start with the minimal viable implementation.

### Clean Architecture
Maintain clear separation of concerns between models, services, and CLI interface. Each component should have a single, well-defined responsibility.

### AI-Assisted Development
Leverage Claude Code as the primary implementation agent for spec-driven development. Use AI tools for code generation, refinement, and quality assurance following defined workflows.

### Python Clean Code Standards
Code must follow Python clean code conventions. No unused code, dead logic, or premature abstractions are allowed. Maintain high code quality standards throughout development.

## Technology Standards

The following technology standards are mandatory for this project:
- Programming language: Python >= 3.13
- Environment & dependency management: UV only
- Specification framework: Spec-Kit Plus
- Code generation & refinement: Claude Code
- Operating environment: Linux (WSL 2 compliant)

## Development Workflow

### Specification Governance
- Every feature must originate from a written specification
- Specification changes must be tracked in spec history
- Implementation must strictly follow the latest approved spec
- If ambiguity exists, clarify via specification updates before coding

### Implementation Constraints
- In-memory data storage only (no files, no database)
- Single-user, local CLI only
- No external frameworks (e.g., FastAPI, Click, Typer)
- No network or cloud dependencies
- CLI interface must be human-readable and intuitive
- Errors must be handled gracefully with clear messages

## Governance

This constitution governs all development activities for the In-Memory Todo CLI Application. All code changes, feature implementations, and architectural decisions must comply with these principles. Deviations require explicit approval and constitution amendments.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2025-12-30