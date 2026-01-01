# Research: Advanced Todo Features

## 1. Recurrence Pattern Algorithms

### 1.1 Common Recurrence Patterns
- **Daily**: Every day, weekdays only, weekends only
- **Weekly**: Every N weeks on specific days
- **Monthly**: By date (e.g., every 15th) or by position (e.g., first Monday of month)
- **Custom**: Every N days/weeks based on user specification

### 1.2 Recommended Approach
For the in-memory todo CLI application, the simplest and most effective approach is to use a pattern-based system:
- Define recurrence as a pattern object with type and parameters
- Use Python's `datetime` module for date calculations
- Calculate next occurrence based on last occurrence and pattern

### 1.3 Pattern Structure
```python
class RecurrencePattern:
    type: str  # "daily", "weekly", "custom"
    interval: int  # for custom patterns (every N days/weeks)
    days_of_week: List[int]  # 0=Monday, 6=Sunday for weekly patterns
```

## 2. Time Handling and Reminders

### 2.1 Time Zone Considerations
- Use system's local time zone as specified in requirements
- Python's `datetime.now()` and `datetime.today()` use local time by default
- Store all times in local timezone to avoid complexity

### 2.2 Reminder Mechanism
- For CLI application, "reminders" mean in-app notifications when the CLI is active
- Check for due tasks/reminders on CLI startup and command execution
- Use simple comparison: `task.due_date <= current_datetime`

### 2.3 Time Comparison Strategy
- Store all datetime values as timezone-naive local datetime objects
- Compare using standard datetime comparison operators
- Use `datetime.now()` for current time comparisons

## 3. In-Memory Storage Considerations

### 3.1 Data Structure Options
- Simple list/dict: Fast access but inefficient for time-based queries
- Sorted list: Better for chronological operations
- Heap/queue: Good for priority-based access (by due date)

### 3.2 Recommended Structure
For this application, a simple list with filtering functions will be sufficient:
- Tasks stored in a list
- Use list comprehensions for filtering by due date, recurrence, etc.
- Performance should be adequate for typical personal todo usage

## 4. CLI Integration Points

### 4.1 New Commands Needed
- `add --recur` or `add -r`: Add recurring tasks
- `add --due` or `add -d`: Add tasks with due dates
- `add --remind` or `add -m`: Add tasks with reminders
- `view --upcoming`: View tasks sorted by due date
- `modify --cancel-recur`: Cancel recurring patterns

### 4.2 Integration with Existing Commands
- Existing `add`, `view`, `complete` commands should work with enhanced tasks
- Minimal disruption to existing user workflows
- Backward compatibility maintained

## 5. Key Decisions

### 5.1 Recurrence Pattern Representation
**Decision**: Use a structured pattern object with type and parameters
**Rationale**: Provides flexibility for different recurrence types while remaining simple to implement and understand
**Alternatives considered**:
- Cron-like syntax (too complex for CLI app)
- Fixed interval enums only (too limiting)

### 5.2 Reminder System Implementation
**Decision**: In-app notifications only (when CLI is active)
**Rationale**: Matches requirements and is feasible for CLI application
**Alternatives considered**:
- Background daemon (too complex, not needed)
- System notifications (requires platform-specific code)

### 5.3 Time Storage Format
**Decision**: Use Python datetime objects in local timezone
**Rationale**: Simple, leverages built-in datetime functionality, matches requirement for local timezone
**Alternatives considered**:
- Unix timestamps (less readable, more complex for date operations)
- ISO strings (requires parsing, less efficient)

## 6. Technical Unknowns Resolved
- **NEEDS CLARIFICATION** → Recurrence algorithm: Use datetime arithmetic with pattern objects
- **NEEDS CLARIFICATION** → Reminder mechanism: In-app notifications when CLI is active
- **NEEDS CLARIFICATION** → Time zone handling: Use system local time zone
- **NEEDS CLARIFICATION** → Storage structure: Simple list with filtering functions