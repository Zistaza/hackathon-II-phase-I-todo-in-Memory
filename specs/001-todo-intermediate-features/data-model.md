# Data Model: Intermediate Level Todo Features

## Task Entity

### Fields
- **id** (int): Unique identifier for the task (auto-incremented)
- **title** (str): Task title/description (required)
- **description** (str): Optional detailed description
- **status** (str): Task completion status ('incomplete' or 'complete')
- **priority** (str): Task priority level ('high', 'medium', 'low') - default: 'medium'
- **tags** (list[str]): List of tags/categories for the task - default: empty list
- **created_at** (datetime): Timestamp of when task was created (immutable)

### Relationships
- No direct relationships - each task is independent

### Validation Rules
- **id**: Must be positive integer, auto-generated
- **title**: Required, non-empty string
- **status**: Must be either 'complete' or 'incomplete'
- **priority**: Must be one of 'high', 'medium', 'low'
- **tags**: List of strings, each tag must be non-empty and contain no spaces
- **created_at**: Auto-generated, immutable once set

### State Transitions
- **status**: Can transition from 'incomplete' to 'complete' and vice versa

## Search/Filter Criteria

### Search Fields
- **keyword**: Text to search in title and description fields

### Filter Fields
- **status**: Filter by completion status ('complete' or 'incomplete')
- **priority**: Filter by priority level ('high', 'medium', 'low')
- **tags**: Filter by tags (match any of the specified tags)

## Sort Criteria

### Sort Options
- **priority**: Sort by priority level (high → medium → low)
- **alpha**: Sort alphabetically by title
- **created**: Sort by creation timestamp (oldest → newest)