# Quickstart Guide: Intermediate Level Todo CLI

## Setup

1. Ensure Python 3.13+ is installed
2. Install dependencies with UV: `uv sync`
3. Run the CLI: `python -m src.cli.main`

## Basic Commands

### Add a Task
```bash
todo add "Buy groceries"
todo add "Complete project" --priority high
todo add "Meeting notes" --tags work,important
todo add "Weekly review" --priority medium --tags work,planning
```

### List Tasks
```bash
todo list                           # List all tasks
todo list --status complete         # Filter by completion status
todo list --status incomplete       # Filter by completion status
todo list --priority high           # Filter by priority
todo list --priority medium         # Filter by priority
todo list --priority low            # Filter by priority
todo list --tag work                # Filter by tag
todo list --sort priority           # Sort by priority
todo list --sort alpha              # Sort alphabetically
todo list --sort created            # Sort by creation date
```

### Combined Operations
```bash
todo list --priority high --tag work --sort alpha
todo list --status incomplete --sort priority
```

### Update a Task
```bash
todo update 1 "New title" --priority high
todo update 1 "New title" --tags work,urgent
todo update 1 "New title" --status complete
todo update 1 "New title" --priority high --tags work,urgent
```

### Search Tasks
```bash
todo search "groceries"
todo search "project" --sort alpha
todo search "meeting" --sort priority
```

### Complete/Incomplete Tasks
```bash
todo complete 1
todo incomplete 1
```

### Delete a Task
```bash
todo delete 1
```

## Task Display Format

Tasks are displayed in the format:
```
[ID] [STATUS] [PRIORITY] Title #tag1 #tag2
```

Example:
```
ID: 1 [ ] [HIGH] Complete project #work #urgent
ID: 2 [✓] [MEDIUM] Buy groceries #home
ID: 3 [ ] [LOW] Read book #personal
```

## Priority Levels

- HIGH: [HIGH] - Highest priority tasks
- MEDIUM: [MEDIUM] - Normal priority tasks (default)
- LOW: [LOW] - Lowest priority tasks

## Tag Format

- Tags are specified as comma-separated values: `--tags work,urgent,planning`
- Displayed as: `#work #urgent #planning`
- Multiple tags allowed per task

## Filter Logic

- Multiple filters use AND logic (task must match ALL specified criteria)
- Tag filter uses OR logic (task matches if it has ANY of the specified tags)
- Available filters: --status, --priority, --tag
- Available sorts: --sort priority, --sort alpha, --sort created