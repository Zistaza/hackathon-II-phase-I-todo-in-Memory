# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This implementation extends the Basic Level In-Memory Todo CLI Application with Intermediate Level features: Priorities & Tags/Categories, Search & Filter, and Sort Tasks. The architecture maintains clean separation of concerns between models, services, and CLI layer. The implementation follows Python clean code standards and constitution requirements, focusing on deterministic behavior and simplicity over complexity. The solution will provide CLI commands for managing task priorities (high/medium/low), tags (work/home/study), searching by keyword, filtering by status/priority/tag, and sorting by various criteria, all with in-memory storage and under 1-second response times for up to 1000 tasks.

## Technical Context

**Language/Version**: Python 3.13+ (as per constitution)
**Primary Dependencies**: None (no external frameworks allowed per constitution)
**Storage**: In-memory only (no files, no database as per constitution)
**Testing**: pytest (for unit and integration tests)
**Target Platform**: Linux/WSL2 (as per constitution)
**Project Type**: Single CLI application (extending existing Basic Level implementation)
**Performance Goals**: <1 second response for up to 1000 tasks for search, filter, and sort operations
**Constraints**: <1 second response time for operations, deterministic behavior, no external dependencies
**Scale/Scope**: Single-user, local CLI application with up to 1000 tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-First Development ✅
- Following spec-first approach as required by constitution
- Implementation will strictly follow the approved specification

### Deterministic Behavior ✅
- All CLI actions will produce predictable, testable results
- Search, filter, and sort operations will be deterministic with consistent output

### Simplicity Over Complexity ✅
- Maintaining in-memory only storage as per constitution
- No unnecessary complexity added beyond required features
- Following minimal viable implementation approach

### Clean Architecture ✅
- Maintaining clear separation between models, services, and CLI interface
- Each component will have a single, well-defined responsibility

### Python Clean Code Standards ✅
- Code will follow Python clean code conventions
- No unused code or dead logic will be included

### Implementation Constraints ✅
- In-memory data storage only (no files, no database)
- Single-user, local CLI only
- No external frameworks (FastAPI, Click, Typer not used)
- No network or cloud dependencies
- CLI interface will be human-readable and intuitive
- Errors will be handled gracefully with clear messages

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-intermediate-features/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task entity with priority, tags, and other attributes
├── services/
│   ├── todo_service.py  # Core business logic for tasks, filtering, searching, sorting
│   └── validation.py    # Input validation and error handling
└── cli/
    └── main.py          # CLI interface and command routing

tests/
├── unit/
│   ├── models/
│   └── services/
├── integration/
│   └── cli/
└── contract/
    └── task_contract.py

README.md
requirements.txt         # Though no external dependencies per constitution
.pytest_cache/
.gitignore
```

**Structure Decision**: Single project structure selected to maintain simplicity and follow clean architecture principles. The implementation extends the existing Basic Level features while maintaining clear separation of concerns between models, services, and CLI layer as required by the constitution.

## Architecture Sketch

### Separation of Concerns

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│     CLI Layer   │───▶│  Service Layer   │───▶│   Model Layer   │
│                 │    │                  │    │                 │
│ - Command       │    │ - Business Logic │    │ - Task Entity   │
│   Parsing       │    │ - Validation     │    │ - Data Storage  │
│ - Input/Output  │    │ - Filtering      │    │ - Serialization │
│ - Formatting    │    │ - Searching      │    │                 │
└─────────────────┘    │ - Sorting        │    └─────────────────┘
                       │ - Error Handling │
                       └──────────────────┘
```

### Task Entity Design

```python
class Task:
    def __init__(self, id: int, title: str, description: str = "",
                 status: str = "incomplete", priority: str = "medium",
                 tags: list = None, created_at: datetime = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status  # "complete" or "incomplete"
        self.priority = priority  # "high", "medium", "low"
        self.tags = tags if tags is not None else []
        self.created_at = created_at if created_at is not None else datetime.now()
```

### In-Memory Data Structures

#### Primary Storage
- **tasks**: List[Task] - Maintains insertion order and provides natural indexing
- **task_index**: Dict[int, Task] - Provides O(1) lookup by ID

#### Indexing Strategy (for performance)
- **priority_index**: Dict[str, List[Task]] - Tasks grouped by priority
- **tag_index**: Dict[str, List[Task]] - Tasks grouped by tag (for tag-based filtering)
- **status_index**: Dict[str, List[Task]] - Tasks grouped by status

### Service Layer Operations Mapping

```
CLI Commands → Service Methods → Data Operations

todo add "title" --priority high --tags work:
  ──> todo_service.create_task(title="title", priority="high", tags=["work"])
  ──> Add to tasks list and update indexes

todo list --priority high --tag work --sort alpha:
  ──> todo_service.get_filtered_sorted_tasks(priority="high", tags=["work"], sort_by="alpha")
  ──> Use indexes for filtering, then sort results

todo search "keyword":
  ──> todo_service.search_tasks(keyword="keyword")
  ──> Linear search through all tasks for keyword in title/description

todo update 1 --priority high:
  ──> todo_service.update_task(task_id=1, priority="high")
  ──> Update task and refresh relevant indexes
```

### Performance Considerations

For up to 1000 tasks:
- **Search**: O(n) linear search acceptable (n ≤ 1000)
- **Filter**: O(n) with early termination possible
- **Sort**: O(n log n) using Python's built-in sorted()
- **Add/Update/Delete**: O(1) to O(n) depending on index updates

## Design Decisions & Trade-offs

### 1. Filter Combination Logic
- **Decision**: Multiple filters use AND logic
- **Rationale**: More precise results - only tasks matching ALL criteria are returned
- **Alternative**: OR logic (any criteria match) - rejected as too broad

### 2. Tag Filtering Logic
- **Decision**: Multiple tags use OR logic within the tag filter
- **Rationale**: Flexible filtering - tasks with ANY of the specified tags are included
- **Alternative**: AND logic for tags - rejected as too restrictive

### 3. Sorting Implementation
- **Decision**: Use Python's built-in sorted() with custom key functions
- **Rationale**: Leverages optimized Timsort algorithm, stable sorting by default
- **Alternative**: Custom sorting algorithms - rejected as unnecessary complexity

### 4. Data Structure Choice
- **Decision**: List for primary storage, Dict for ID lookup
- **Rationale**: Simple, maintains insertion order, efficient for required operations
- **Alternative**: Custom tree structures - rejected as over-engineering for 1000 tasks

## Testing & Validation Strategy

### Unit Tests
- **Task Model**: Test all field validations and state transitions
- **Service Layer**: Test all business logic functions (CRUD, search, filter, sort)
- **CLI Layer**: Test command parsing and response formatting

### Integration Tests
- **End-to-end**: Test complete command workflows
- **Error handling**: Test all error conditions and edge cases
- **Performance**: Test response times with up to 1000 tasks

### Validation Checks
- **Priority/Tag Assignment**: Verify correct storage and display
- **Search Accuracy**: Verify keyword matching in title and description
- **Filter Correctness**: Verify deterministic results for all filter combinations
- **Sort Correctness**: Verify proper ordering for all sort criteria
- **Performance**: Verify <1 second response time for all operations with up to 1000 tasks

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
