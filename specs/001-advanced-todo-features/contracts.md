# API Contracts and CLI Integration: Advanced Todo Features

## 1. CLI Command Contracts

### 1.1 Add Task Commands (Enhanced)
```
Command: add "task description" [OPTIONS]

Options:
  --due, -d TEXT        Set due date (format: YYYY-MM-DD or YYYY-MM-DD HH:MM)
  --remind, -m TEXT     Set reminder time (format: YYYY-MM-DD HH:MM)
  --recur, -r TEXT      Set recurrence pattern
    Examples: "daily", "weekly", "every 3 days", "every 2 weeks"
  --recur-days, -rd TEXT  Days for weekly recurrence (e.g., "mon,wed,fri")

Examples:
  add "Buy groceries" --due "2026-01-05"
  add "Team meeting" --recur "weekly" --recur-days "tue,thu"
  add "Daily exercise" --recur "daily" --remind "08:00"
```

### 1.2 View Task Commands (Enhanced)
```
Command: view [OPTIONS]

Options:
  --upcoming, -u        Show tasks sorted by due date (ascending)
  --overdue, -o         Show only overdue tasks
  --recurring, -r       Show only recurring tasks
  --due-before, -db TEXT  Show tasks due before date
  --due-after, -da TEXT   Show tasks due after date

Examples:
  view --upcoming
  view --overdue
  view --recurring
```

### 1.3 Modify Task Commands (Enhanced)
```
Command: modify ID [OPTIONS]

Options:
  --due, -d TEXT        Update due date
  --remind, -m TEXT     Update reminder time
  --cancel-recur        Cancel recurring pattern
  --update-recur TEXT   Update recurrence pattern

Examples:
  modify 123 --due "2026-01-10"
  modify 123 --cancel-recur
  modify 123 --update-recur "every 2 days"
```

### 1.4 New Specific Commands
```
Command: recurring [OPTIONS]

Options:
  --list, -l            List all recurring tasks
  --cancel ID           Cancel a recurring pattern
  --next                Show next occurrences of recurring tasks

Examples:
  recurring --list
  recurring --cancel 123
  recurring --next
```

```
Command: reminders [OPTIONS]

Options:
  --list, -l            List all active reminders
  --triggered, -t       List triggered reminders
  --upcoming, -u        List upcoming reminders

Examples:
  reminders --list
  reminders --upcoming
```

## 2. Input/Output Formats

### 2.1 Task Representation in CLI Output
```
ID: 123
Title: Daily exercise
Status: Pending
Created: 2026-01-01 10:30
Due: 2026-01-02 08:00
Reminder: 2026-01-02 07:30
Recurring: daily (next instance: 2026-01-03 00:00)
```

### 2.2 Compact View Format
```
[123] Daily exercise | Due: 2026-01-02 08:00 | Recurring: daily | Reminder: 07:30
[124] Weekly report | Due: 2026-01-05 | Status: Overdue
```

### 2.3 Date/Time Input Formats
- Due date: `YYYY-MM-DD` (e.g., "2026-01-05")
- Due datetime: `YYYY-MM-DD HH:MM` (e.g., "2026-01-05 14:30")
- Time only: `HH:MM` (assumes today's date, e.g., "08:00")
- Relative: `+N days/hours` (e.g., "+1 day", "+2 hours")

## 3. Error Handling Contracts

### 3.1 Common Error Responses
```
Error: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM
Error: Task ID not found: 123
Error: Cannot set reminder after due date
Error: Invalid recurrence pattern
```

### 3.2 Validation Error Responses
```
Error: Due date must be in the future
Error: Reminder time must be before due date
Error: Task is already completed
Error: Recurrence pattern cannot be modified after creation
```

## 4. Internal API Contracts

### 4.1 Task Service Methods
```python
def add_task(
    title: str,
    due_date: Optional[datetime] = None,
    reminder_time: Optional[datetime] = None,
    recurrence_pattern: Optional[RecurrencePattern] = None
) -> Task:
    """
    Add a new task with optional advanced features
    Returns: Created Task object
    """

def get_upcoming_tasks(
    limit: Optional[int] = None,
    include_recurring: bool = True
) -> List[Task]:
    """
    Get tasks sorted by due date
    Returns: List of Task objects
    """

def check_and_trigger_reminders() -> List[Reminder]:
    """
    Check for reminders that should be triggered
    Returns: List of triggered reminders
    """

def generate_recurring_tasks() -> List[Task]:
    """
    Generate new task instances based on recurrence patterns
    Returns: List of newly created Task objects
    """
```

### 4.2 Recurrence Service Methods
```python
def create_recurrence_pattern(
    pattern_type: str,
    interval: Optional[int] = None,
    days_of_week: Optional[List[int]] = None
) -> RecurrencePattern:
    """
    Create a recurrence pattern object
    Returns: RecurrencePattern object
    """

def calculate_next_occurrence(
    pattern: RecurrencePattern,
    last_occurrence: datetime
) -> datetime:
    """
    Calculate the next occurrence based on pattern
    Returns: datetime for next occurrence
    """
```

## 5. Integration Points

### 5.1 With Existing CLI
- All new options are optional additions to existing commands
- Backward compatibility maintained for existing functionality
- New commands are additions, not replacements

### 5.2 With Existing Data Model
- New fields added to existing Task class as optional attributes
- Existing task operations remain unchanged
- New functionality layered on top of existing structure

### 5.3 Timing Integration
- Recurrence checking occurs on CLI startup
- Reminder checking occurs on each command execution
- Time-based operations use system local time

## 6. User Experience Considerations

### 6.1 Help Text Enhancements
- Enhanced help text for all commands with new options
- Context-sensitive help based on current command state
- Examples included in help output

### 6.2 Feedback Mechanisms
- Visual indicators for due dates and reminders in task lists
- Notification messages when reminders are triggered
- Confirmation prompts for recurrence cancellation

### 6.3 Validation Feedback
- Clear error messages for invalid inputs
- Suggested corrections where possible
- Format examples in error messages