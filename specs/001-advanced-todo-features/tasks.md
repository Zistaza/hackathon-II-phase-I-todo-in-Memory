# Implementation Tasks: Advanced Todo Features

**Feature**: Advanced Todo Features (Recurring Tasks and Due Date Reminders)
**Branch**: `001-advanced-todo-features`
**Spec**: [Advanced Todo Features Spec](/home/emizee/hackathon-II-phase-I-todo-in-Memory/specs/001-advanced-todo-features/spec.md)

## Overview

Implementation of advanced intelligent features for the in-memory todo CLI application, specifically recurring tasks and due date/time reminders. The solution extends the existing task model with new attributes for due dates, reminders, and recurrence patterns while maintaining backward compatibility.

## Dependencies

- User Story 1 (P1) must be completed before User Story 3
- User Story 2 (P1) must be completed before User Story 4
- Foundational tasks (Phase 2) must be completed before any user story phases

## Parallel Execution Examples

- T005 [P] [US1] Implement RecurrencePattern model and T006 [P] [US2] Implement due date functionality can run in parallel
- T012 [P] [US1] Create recurrence generation logic and T013 [P] [US2] Create reminder checking logic can run in parallel

## Implementation Strategy

MVP scope includes User Story 1 (Create Recurring Tasks) and User Story 2 (Set Due Dates and Reminders). User Story 3 and 4 are enhancements that can be added incrementally after the core functionality is working.

---

## Phase 1: Setup

Initialize project structure and set up foundational components for the advanced features.

- [x] T001 Create src/models directory structure
- [x] T002 Create src/services directory structure
- [x] T003 Create tests/test_advanced directory structure
- [x] T004 Install pytest for testing advanced features

---

## Phase 2: Foundational Tasks

Implement core models and services that will be used by multiple user stories.

- [x] T005 [P] [US1] [US2] Create enhanced Task model in src/models/task.py with due_date, reminder_time, recurrence_pattern, parent_task_id, and is_recurring_template attributes
- [x] T006 [P] [US1] Create RecurrencePattern model in src/models/recurrence.py with type, interval, days_of_week, end_date, max_occurrences, and next_occurrence attributes
- [x] T007 [P] [US2] Create Reminder model in src/models/reminder.py with task_id, reminder_time, triggered, and triggered_at attributes
- [x] T008 [P] Create in-memory storage structure in src/services/task_storage.py with tasks dict, recurrence_templates dict, reminders dict, and due_tasks_cache list
- [x] T009 [P] Implement datetime utilities in src/services/datetime_utils.py for time zone handling and date calculations
- [x] T010 [P] Create base TaskService in src/services/task_service.py with enhanced task operations

---

## Phase 3: User Story 1 - Create Recurring Tasks (P1)

As a user of the todo CLI app, I want to create tasks that automatically repeat on a schedule so that I don't have to manually add routine tasks every day/week.

**Goal**: Users can create tasks that automatically repeat on a daily, weekly, or custom interval

**Independent Test**: Can be fully tested by creating a recurring task with a specific interval (daily, weekly, custom) and verifying that the system generates new instances of the task at the specified intervals without user intervention.

- [x] T011 [US1] Create RecurrenceService in src/services/recurrence_service.py with create_recurrence_pattern and calculate_next_occurrence methods
- [x] T012 [US1] Implement recurrence generation logic in RecurrenceService to generate new task instances based on patterns
- [x] T013 [US1] Add recurrence validation to TaskService for validating recurrence patterns
- [x] T014 [US1] Extend CLI add command in src/cli/main.py to support --recur option for daily, weekly, and custom patterns
- [x] T015 [US1] Extend CLI add command to support --recur-days option for weekly recurrence patterns
- [x] T016 [US1] Create test for daily recurring task functionality in tests/test_advanced/test_recurrence.py
- [x] T017 [US1] Create test for weekly recurring task functionality in tests/test_advanced/test_recurrence.py
- [x] T018 [US1] Create test for custom recurring task functionality in tests/test_advanced/test_recurrence.py
- [x] T019 [US1] Implement CLI help text for recurring task options in src/cli/main.py

---

## Phase 4: User Story 2 - Set Due Dates and Reminders (P1)

As a user, I want to assign due dates and optional time reminders to tasks so that I can manage my time effectively and be notified of upcoming deadlines.

**Goal**: Users can assign due dates and optional time reminders to tasks

**Independent Test**: Can be fully tested by setting due dates and reminders on tasks and verifying that the system displays upcoming tasks with appropriate indicators and timing.

- [x] T020 [US2] Create ReminderService in src/services/reminder_service.py with check_and_trigger_reminders method
- [x] T021 [US2] Implement due date validation in TaskService to ensure due dates are in the future
- [x] T022 [US2] Implement reminder validation in TaskService to ensure reminder time is before due date
- [x] T023 [US2] Extend CLI add command in src/cli/main.py to support --due option for due dates
- [x] T024 [US2] Extend CLI add command in src/cli/main.py to support --remind option for reminders
- [x] T025 [US2] Create get_upcoming_tasks method in TaskService to return tasks sorted by due date
- [x] T026 [US2] Implement overdue task detection in TaskService
- [x] T027 [US2] Create test for due date functionality in tests/test_advanced/test_reminders.py
- [x] T028 [US2] Create test for reminder functionality in tests/test_advanced/test_reminders.py
- [x] T029 [US2] Create test for upcoming task view in tests/test_advanced/test_reminders.py

---

## Phase 5: User Story 3 - Modify and Cancel Recurring Patterns (P2)

As a user, I want to modify or cancel recurring task patterns so that I can adjust my routine tasks when my schedule changes.

**Goal**: Users can modify or cancel recurring task patterns

**Independent Test**: Can be fully tested by modifying or canceling existing recurring tasks and verifying that future instances are updated or removed according to the changes.

- [x] T030 [US3] Extend TaskService to support canceling recurrence patterns
- [x] T031 [US3] Extend TaskService to support updating recurrence patterns
- [x] T032 [US3] Extend CLI modify command in src/cli/main.py to support --cancel-recur option
- [x] T033 [US3] Extend CLI modify command in src/cli/main.py to support --update-recur option
- [x] T034 [US3] Create recurring command in src/cli/main.py with --list, --cancel, and --next options
- [x] T035 [US3] Create test for canceling recurring patterns in tests/test_advanced/test_recurrence.py
- [x] T036 [US3] Create test for updating recurring patterns in tests/test_advanced/test_recurrence.py
- [x] T037 [US3] Create test for recurring command functionality in tests/test_advanced/test_cli_integration.py

---

## Phase 6: User Story 4 - View Upcoming Tasks with Status Indicators (P2)

As a user, I want to see upcoming tasks with clear status, due date, and reminder indicators so that I can prioritize my work effectively.

**Goal**: See upcoming tasks with clear status, due date, and reminder indicators

**Independent Test**: Can be fully tested by viewing the todo list with various task types and verifying that status indicators (due dates, reminders, recurring patterns) are clearly displayed.

- [x] T038 [US4] Extend CLI view command in src/cli/main.py to support --upcoming option
- [x] T039 [US4] Extend CLI view command in src/cli/main.py to support --overdue option
- [x] T040 [US4] Extend CLI view command in src/cli/main.py to support --recurring option
- [x] T041 [US4] Extend CLI view command in src/cli/main.py to support --due-before and --due-after options
- [x] T042 [US4] Enhance task display format in CLI to show due dates, reminders, and recurrence indicators
- [x] T043 [US4] Create reminders command in src/cli/main.py with --list, --triggered, and --upcoming options
- [x] T044 [US4] Create test for upcoming task view in tests/test_advanced/test_cli_integration.py
- [x] T045 [US4] Create test for overdue task view in tests/test_advanced/test_cli_integration.py
- [x] T046 [US4] Create test for recurring task view in tests/test_advanced/test_cli_integration.py

---

## Phase 7: Polish & Cross-Cutting Concerns

Final integration, testing, and polish to ensure all features work together seamlessly.

- [x] T047 Implement comprehensive error handling for all advanced features in src/cli/main.py
- [x] T048 Add input validation for all new CLI options with appropriate error messages
- [x] T049 Create integration tests for all user stories in tests/test_advanced/test_cli_integration.py
- [x] T050 Implement backward compatibility tests to ensure existing functionality still works
- [x] T051 Add performance tests to ensure task operations complete in under 1 second
- [x] T052 Update help text throughout CLI to include examples of new advanced features
- [x] T053 Create comprehensive test suite for edge cases in tests/test_advanced/conftest.py
- [x] T054 Run full test suite to verify no regressions in existing functionality
- [x] T055 Update documentation with usage examples for advanced features
- [x] T056 Perform final integration testing of all advanced features working together