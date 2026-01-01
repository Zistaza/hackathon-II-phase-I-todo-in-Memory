# ADR-0002: Recurrence Pattern and Reminder Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-01
- **Feature:** 001-advanced-todo-features
- **Context:** The In-Memory Todo CLI Application needs to implement recurring tasks and due date reminders while maintaining the in-memory constraint and CLI-only interface. The architecture must handle time-based operations, recurrence pattern calculations, and reminder triggering in a deterministic way that works within the project's constitution requirements for simplicity and clean architecture.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Implement a comprehensive architecture for recurring tasks and reminders with the following components:

- **Recurrence Pattern System**: Pattern-based system using structured objects with type and parameters for calculating next occurrences
- **Time Handling**: Use Python datetime objects with system local timezone for all time operations
- **Reminder Mechanism**: In-app notifications triggered when CLI is active, not background system notifications
- **Data Model Enhancement**: Extend Task model with due_date, reminder_time, and recurrence_pattern attributes
- **Storage Strategy**: Simple dictionary-based in-memory storage with filtering functions for time-based queries
- **CLI Integration**: Extend existing CLI commands with new options (--due, --remind, --recur) while maintaining backward compatibility

## Consequences

### Positive

- Time-based operations are deterministic and testable with controlled time functions
- Architecture maintains backward compatibility with existing functionality
- Simple implementation that follows the "simplicity over complexity" principle
- In-memory only approach avoids persistence complexity while meeting constitution requirements
- Clear separation between task management, recurrence logic, and reminder systems
- Cross-cutting architecture that impacts multiple components in a consistent way

### Negative

- In-app reminder system means notifications only occur when CLI is active (not background notifications)
- Time zone handling is limited to local system timezone (no multi-timezone support)
- Performance may degrade with large numbers of recurring tasks due to simple storage approach
- Requires careful handling of system clock changes and daylight saving time transitions
- Recurrence calculations happen at runtime rather than being pre-computed

## Alternatives Considered

**Alternative A: Cron-like Syntax with Background Daemon**
- Use cron expressions for recurrence patterns with a background process for reminders
- Rejected because it violates the in-memory constraint and adds unnecessary complexity for a CLI application

**Alternative B: Unix Timestamps with Background Services**
- Store all times as Unix timestamps and use system-level background services for reminders
- Rejected because it violates the in-memory only requirement and introduces platform-specific complexity

**Alternative C: External Database with Scheduling Service**
- Use an external database with built-in scheduling capabilities
- Rejected because it completely violates the in-memory and CLI-only constraints in the constitution

**Alternative D: Simple Interval-Based Recurrence Only**
- Limit recurrence to simple daily/weekly intervals without complex pattern support
- Rejected because it would limit user flexibility and not fully address the feature requirements

## References

- Feature Spec: /home/emizee/hackathon-II-phase-I-todo-in-Memory/specs/001-advanced-todo-features/spec.md
- Implementation Plan: /home/emizee/hackathon-II-phase-I-todo-in-Memory/specs/001-advanced-todo-features/plan.md
- Related ADRs: ADR-0001: Clean Architecture Implementation
- Evaluator Evidence: /home/emizee/hackathon-II-phase-I-todo-in-Memory/history/prompts/001-advanced-todo-features/1-advanced-todo-features-plan.plan.prompt.md
