# Implementation Tasks: Intermediate Level Features for In-Memory Todo CLI Application

**Feature**: 001-todo-intermediate-features
**Date**: 2025-12-31
**Spec**: specs/001-todo-intermediate-features/spec.md
**Plan**: specs/001-todo-intermediate-features/plan.md

## Implementation Strategy

This implementation extends the Basic Level In-Memory Todo CLI Application with Intermediate Level features: Priorities & Tags/Categories, Search & Filter, and Sort Tasks. The approach follows an MVP-first strategy, delivering core functionality in priority order while maintaining clean architecture principles.

## Phase 1: Setup Tasks

- [ ] T001 Create directory structure for models, services, and CLI layer per implementation plan
- [ ] T002 Set up basic project configuration and requirements (though no external dependencies per constitution)
- [ ] T003 Initialize test directory structure for unit and integration tests

## Phase 2: Foundational Tasks

- [X] T004 [P] Update Task model to include priority, tags, and created_at fields with proper validation
- [X] T005 [P] Extend TaskService to support new task attributes and operations
- [X] T006 [P] Create validation service for priority and tag format validation

## Phase 3: User Story 1 - Add Priorities and Tags to Tasks (P1)

- [X] T007 [US1] Implement CLI command parsing for --priority and --tags flags in add command
- [X] T008 [US1] Implement CLI command parsing for --priority and --tags flags in update command
- [X] T009 [US1] Update Task model to include priority field (high/medium/low) with validation
- [X] T010 [US1] Update Task model to include tags field (list of strings) with validation
- [X] T011 [US1] Update Task model to include created_at field with proper timestamp
- [X] T012 [US1] Implement TaskService methods for creating tasks with priority and tags
- [X] T013 [US1] Implement TaskService methods for updating tasks with priority and tags
- [X] T014 [US1] Update CLI display formatting to show priority as [HIGH], [MEDIUM], [LOW]
- [X] T015 [US1] Update CLI display formatting to show tags as #tag1 #tag2 format
- [X] T016 [US1] Implement validation for priority values (high, medium, low only)
- [X] T017 [US1] Implement validation for tag format (no spaces, non-empty strings)
- [ ] T018 [US1] Write unit tests for Task model with new priority and tag fields
- [ ] T019 [US1] Write unit tests for TaskService methods with priority and tag operations
- [ ] T020 [US1] Write integration tests for CLI commands with priority and tag functionality

## Phase 4: User Story 2 - Filter and Search Tasks (P2)

- [X] T021 [US2] Implement search functionality in TaskService to find tasks by keyword
- [X] T022 [US2] Implement status filtering in TaskService (complete/incomplete)
- [X] T023 [US2] Implement priority filtering in TaskService (high/medium/low)
- [X] T024 [US2] Implement tag filtering in TaskService (OR logic for multiple tags)
- [X] T025 [US2] Implement combined filter logic in TaskService (AND logic between different filter types)
- [X] T026 [US2] Create CLI command parsing for --status, --priority, and --tag filters
- [X] T027 [US2] Create CLI command for search operation with keyword parameter
- [X] T028 [US2] Implement CLI list command with filter parameters
- [ ] T029 [US2] Write unit tests for search functionality in TaskService
- [ ] T030 [US2] Write unit tests for filter operations in TaskService
- [ ] T031 [US2] Write integration tests for combined filter operations
- [ ] T032 [US2] Write integration tests for search functionality in CLI

## Phase 5: User Story 3 - Sort Task Lists (P3)

- [X] T033 [US3] Implement priority sorting in TaskService (high → medium → low)
- [X] T034 [US3] Implement alphabetical sorting in TaskService (by title)
- [X] T035 [US3] Implement creation order sorting in TaskService (oldest → newest)
- [X] T036 [US3] Create CLI command parsing for --sort parameter (priority/alpha/created)
- [X] T037 [US3] Integrate sorting functionality with list and filter operations
- [X] T038 [US3] Ensure sorting does not mutate original task data, only display order
- [ ] T039 [US3] Write unit tests for all sorting operations in TaskService
- [ ] T040 [US3] Write integration tests for sort functionality in CLI

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T041 Implement proper error handling for all new features with descriptive messages
- [X] T042 Update CLI help text to include new command options and examples
- [ ] T043 Create comprehensive integration tests for combined operations (filter + sort)
- [ ] T044 Perform performance testing with up to 1000 tasks to ensure <1 second response times
- [X] T045 Update documentation and quickstart guide with new features
- [X] T046 Run full test suite to ensure no regressions in existing functionality

## Dependencies

- **User Story 1 (P1)**: No dependencies - foundational feature that other stories depend on
- **User Story 2 (P2)**: Depends on User Story 1 (needs priority and tag data to filter)
- **User Story 3 (P3)**: No direct dependencies, but can be enhanced with User Story 1 data

## Parallel Execution Opportunities

- **T004-T006**: Foundational updates can be done in parallel (Task model, TaskService, validation)
- **T007-T017**: User Story 1 implementation can be parallelized across model, service, and CLI layers
- **T021-T028**: User Story 2 implementation can be parallelized across service and CLI layers
- **T033-T037**: User Story 3 implementation can be parallelized across service and CLI layers

## MVP Scope

The MVP scope includes User Story 1 (tasks with priorities and tags) as this is the foundational feature that enables the other functionality. This delivers core value of task categorization while maintaining simplicity.

## Success Criteria

- All tasks in Phase 3 (User Story 1) completed successfully
- Users can create tasks with priority levels (high/medium/low) and tags
- Tasks display properly with [PRIORITY] and #tag formatting
- All existing functionality continues to work without regression
- Performance targets met (<1 second for operations with up to 1000 tasks)