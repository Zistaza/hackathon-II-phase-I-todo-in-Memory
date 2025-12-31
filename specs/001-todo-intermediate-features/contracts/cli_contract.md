# CLI Contract: Todo Application Operations

## Core Operations

### Add Task
- **Command**: `todo add "Task title" --priority high --tags work,study`
- **Input**:
  - title (required, string)
  - priority (optional, enum: high/medium/low, default: medium)
  - tags (optional, comma-separated string list)
- **Output**: Success message with task ID
- **Error cases**: Invalid priority, invalid tag format

### Update Task
- **Command**: `todo update 1 --priority medium --tags work,home`
- **Input**:
  - id (required, integer)
  - title (optional, string)
  - description (optional, string)
  - status (optional, enum: complete/incomplete)
  - priority (optional, enum: high/medium/low)
  - tags (optional, comma-separated string list)
- **Output**: Success message
- **Error cases**: Task not found, invalid inputs

### List Tasks
- **Command**: `todo list` or `todo list --priority high --tag work --sort alpha`
- **Input**:
  - status (optional, enum: complete/incomplete)
  - priority (optional, enum: high/medium/low)
  - tag (optional, string)
  - sort (optional, enum: priority/alpha/created)
- **Output**: Formatted list of tasks with priorities and tags
- **Error cases**: None (empty list if no tasks match filters)

### Search Tasks
- **Command**: `todo search "keyword"`
- **Input**: keyword (required, string)
- **Output**: Formatted list of matching tasks
- **Error cases**: None (empty list if no matches)

### Delete Task
- **Command**: `todo delete 1`
- **Input**: id (required, integer)
- **Output**: Success message
- **Error cases**: Task not found

## Response Format

### Success Response
```
Task [ID] added successfully.
```

### Error Response
```
Error: [descriptive error message]
```

### Task List Format
```
[ID] [PRIORITY] Task title #tag1 #tag2
[ID] [PRIORITY] Task title #tag1 #tag2
```

## Validation Rules

- Task ID must be positive integer
- Priority must be one of: high, medium, low
- Tags must not contain spaces
- Title must not be empty
- Search keyword must not be empty