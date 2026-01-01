# Data Model: Advanced Todo Features

## 1. Core Entities

### 1.1 Task Entity
```python
class Task:
    id: str                    # Unique identifier for the task
    title: str                 # Task description/title
    completed: bool            # Completion status
    created_at: datetime       # When the task was created
    completed_at: datetime     # When the task was completed (optional)

    # New fields for advanced features:
    due_date: datetime         # Due date and time (optional)
    reminder_time: datetime    # Reminder notification time (optional)
    recurrence_pattern: RecurrencePattern  # Recurrence configuration (optional)
    parent_task_id: str        # For recurring tasks, link to original (optional)
    is_recurring_template: bool # Whether this is a template for recurring tasks
```

### 1.2 RecurrencePattern Entity
```python
class RecurrencePattern:
    type: str                  # "daily", "weekly", "custom"
    interval: int              # For custom: every N days/weeks
    days_of_week: List[int]    # For weekly: [0,1,2,3,4] for Mon-Fri
    end_date: datetime         # Optional end date for recurrence
    max_occurrences: int       # Optional limit on number of occurrences
    next_occurrence: datetime  # When the next instance should be created
```

### 1.3 Reminder Entity
```python
class Reminder:
    task_id: str               # Reference to the task
    reminder_time: datetime    # When to trigger the reminder
    triggered: bool            # Whether the reminder has been shown
    triggered_at: datetime     # When the reminder was shown (optional)
```

## 2. Relationships

### 2.1 Task to RecurrencePattern
- One-to-zero-or-one relationship
- A task may have one recurrence pattern or none
- When a task has a recurrence pattern, it generates new task instances

### 2.2 Task to Reminder
- One-to-zero-or-one relationship
- A task may have one reminder or none
- Reminder is tied to a specific task instance

## 3. Validation Rules

### 3.1 Task Validation
- `title` must not be empty
- `due_date` must be in the future (if specified)
- `reminder_time` must be before `due_date` (if both specified)
- `recurrence_pattern` and `parent_task_id` are mutually exclusive (except for generated instances)

### 3.2 RecurrencePattern Validation
- `type` must be one of ["daily", "weekly", "custom"]
- `interval` must be positive if type is "custom"
- `days_of_week` values must be 0-6 if type is "weekly"
- `end_date` must be in the future (if specified)
- `max_occurrences` must be positive (if specified)

### 3.3 Reminder Validation
- `reminder_time` must be in the future
- `task_id` must reference an existing task

## 4. State Transitions

### 4.1 Task State Transitions
```
CREATED (default) → COMPLETED (when marked complete)
COMPLETED → CREATED (when unmarked)
```

### 4.2 Recurring Task Behavior
- When a recurring task is marked complete, the template continues to generate new instances
- Each generated instance is independent of others
- Modifying the recurrence pattern affects future instances only

### 4.3 Reminder State Transitions
```
PENDING (default) → TRIGGERED (when reminder time passes and CLI is active)
```

## 5. In-Memory Storage Structure

### 5.1 Data Storage Approach
```python
# Main storage
tasks: Dict[str, Task] = {}                    # All tasks by ID
recurrence_templates: Dict[str, Task] = {}     # Tasks with recurrence patterns
reminders: Dict[str, Reminder] = {}           # Active reminders by task ID
due_tasks_cache: List[Task] = []              # Cache of tasks sorted by due date
```

### 5.2 Indexing Strategy
- Primary index: tasks by ID (for direct access)
- Secondary indexes:
  - By due date (for upcoming task views)
  - By completion status (for filtering)
  - By recurrence pattern (for generating new instances)

## 6. Data Consistency Rules

### 6.1 Recurrence Consistency
- Parent task and all generated instances share the same recurrence pattern
- When recurrence is canceled, no new instances are generated
- Completed instances do not affect recurrence of future instances

### 6.2 Reminder Consistency
- Each task instance can have at most one reminder
- Reminder times are recalculated when due dates are modified
- Reminders are automatically removed when tasks are deleted

## 7. Data Migration Considerations

### 7.1 From Basic/Intermediate Features
- Existing tasks remain unchanged
- New fields (due_date, reminder_time, recurrence_pattern) default to None
- No data transformation needed for existing tasks